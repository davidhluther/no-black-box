#!/usr/bin/env python3
"""Run, check and report scheduled jobs so none can fail quietly.

Commands
  run JOB [--slot SLOT] [--attempt N]   run one job once, recording before and after
  check [--retry] [--notify]            record missed slots, optionally retry, flag the stuck
  report [--days N]                     list every missed or failed slot in a period

Registry file (JSON), default ./jobs.json. See assets/jobs.example.json.
Outcome rows are appended to one append-only file; nothing is ever rewritten.
A slot is resolved only when a later row for it has status "ok". A slot is flagged
when its retries are used up (or it is not safe to repeat), or when it is still
unresolved escalate_after_minutes (default 240) after its scheduled time.

Safety: standard library only. Writes only the outcomes file, the flags file and
whatever the registered commands themselves write. Secrets come from the
environment and are never printed; text taken from a job's log is scrubbed of
the values of any environment variable whose name contains KEY, TOKEN, SECRET
or PASSWORD. An optional alert webhook comes from the JOB_ALERT_WEBHOOK
environment variable, and its address is never printed.

Exit codes: 0 all resolved, 1 something unresolved or failed, 2 could not run.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
SECRET_NAME = re.compile(r"KEY|TOKEN|SECRET|PASSWORD", re.I)


def now_local():
    return dt.datetime.now().replace(microsecond=0)


def load_registry(path):
    p = Path(path).expanduser()
    if not p.is_file():
        sys.exit(f"could not run: registry {p} not found (copy assets/jobs.example.json)")
    reg = json.loads(p.read_text(encoding="utf-8"))
    base = p.parent
    reg["_base"] = base
    reg["_outcomes"] = base / reg.get("outcomes_file", "job-outcomes/outcomes.ndjson")
    reg["_flags"] = base / reg.get("flags_file", "job-outcomes/flags.md")
    return reg


def read_rows(reg):
    f = reg["_outcomes"]
    rows = []
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    rows.append({"job": "?", "slot": "?", "status": "corrupt-line", "summary": line[:80], "ts": ""})
    return rows


def append_row(reg, **row):
    row["ts"] = now_local().isoformat()
    f = reg["_outcomes"]
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def scrub(text):
    for k, v in os.environ.items():
        if SECRET_NAME.search(k) and v and len(v) >= 6:
            text = text.replace(v, "***")
    return text


def slots_between(job, start, end):
    """Every scheduled slot s with start <= s <= end, as naive local datetimes."""
    sch = job["schedule"]
    hh, mm = (sch.get("time", "00:00").split(":") + ["0"])[:2]
    hh, mm = int(hh), int(mm)
    out = []
    day = start.date()
    while day <= end.date():
        if sch["every"] == "hourly":
            for h in range(24):
                s = dt.datetime.combine(day, dt.time(h, int(sch.get("minute", 0))))
                out.append(s)
        elif sch["every"] == "daily":
            out.append(dt.datetime.combine(day, dt.time(hh, mm)))
        elif sch["every"] == "weekly":
            if WEEKDAYS[day.weekday()] == sch["weekday"].lower()[:3]:
                out.append(dt.datetime.combine(day, dt.time(hh, mm)))
        else:
            sys.exit(f"could not run: unknown schedule 'every': {sch['every']}")
        day += dt.timedelta(days=1)
    return [s for s in out if start <= s <= end]


def due_slots(job, now, lookback_days):
    start = now - dt.timedelta(days=lookback_days)
    if job.get("since"):
        start = max(start, dt.datetime.fromisoformat(job["since"]))
    grace = dt.timedelta(minutes=job.get("grace_minutes", 30))
    return [s for s in slots_between(job, start, now) if s + grace <= now]


def slot_id(s):
    return s.strftime("%Y-%m-%dT%H:%M")


def slot_state(rows, job, slot):
    mine = [r for r in rows if r.get("job") == job and r.get("slot") == slot]
    return mine, any(r["status"] == "ok" for r in mine)


def fill(template, slot):
    d = dt.datetime.strptime(slot, "%Y-%m-%dT%H:%M")
    return template.replace("{slot}", slot).replace("{slot_date}", d.strftime("%Y-%m-%d"))


def run_job(reg, name, slot, attempt):
    job = reg["jobs"][name]
    append_row(reg, job=name, slot=slot, attempt=attempt, status="attempting", summary="started")
    started = dt.datetime.now().timestamp()
    cmd = [fill(str(c), slot) for c in job["command"]]
    cwd = reg["_base"] / job.get("workdir", ".")
    timeout = job.get("timeout_minutes", 30) * 60
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        append_row(reg, job=name, slot=slot, attempt=attempt, status="failed",
                   summary="timed out", cause="timeout", evidence=f"no exit within {job.get('timeout_minutes', 30)} minutes")
        return False
    except OSError as e:
        append_row(reg, job=name, slot=slot, attempt=attempt, status="failed",
                   summary="could not start", cause="cannot-start", evidence=scrub(str(e))[:300])
        return False
    tail = scrub("\n".join((proc.stdout + proc.stderr).strip().splitlines()[-15:]))[:1500]
    if proc.returncode != 0:
        append_row(reg, job=name, slot=slot, attempt=attempt, status="failed",
                   summary=f"exit code {proc.returncode}", cause="nonzero-exit", evidence=tail)
        return False
    out = job.get("output_file")
    if out:
        target = cwd / fill(out, slot)
        if not target.exists() or target.stat().st_mtime < started - 1:
            append_row(reg, job=name, slot=slot, attempt=attempt, status="failed",
                       summary="exit 0 but expected output is missing or not fresh",
                       cause="output-missing", evidence=f"expected {fill(out, slot)}\n{tail}"[:1500])
            return False
    m = re.findall(r"^RESULT:\s*(.+)$", proc.stdout, re.M)
    summary = scrub(m[-1].strip()) if m else "ran; no RESULT line printed"
    append_row(reg, job=name, slot=slot, attempt=attempt, status="ok", summary=summary)
    return True


def flag(reg, name, slot, why, notify):
    key = f"{name}|{slot}"
    f = reg["_flags"]
    f.parent.mkdir(parents=True, exist_ok=True)
    if f.exists() and key in f.read_text(encoding="utf-8"):
        return False
    line = f"- [{now_local().isoformat()}] UNRESOLVED {key}: {why}\n"
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(line)
    hook = os.environ.get("JOB_ALERT_WEBHOOK")
    if notify and hook:
        try:
            req = urllib.request.Request(hook, data=json.dumps({"text": line.strip()}).encode(),
                                         headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=15).read()
        except Exception as e:  # a failed alert is itself a failure; the flags file still holds it
            print(f"alert delivery failed ({type(e).__name__}); flag is in {f}")
    elif notify:
        print("note: JOB_ALERT_WEBHOOK is not set; the flag is only in the flags file")
    return True


def cmd_check(reg, args):
    now = dt.datetime.fromisoformat(args.now) if args.now else now_local()
    unresolved = []
    for name, job in reg["jobs"].items():
        for s in due_slots(job, now, args.lookback_days):
            sid = slot_id(s)
            rows = read_rows(reg)
            mine, ok = slot_state(rows, name, sid)
            if ok:
                continue
            last = mine[-1] if mine else None
            timeout = dt.timedelta(minutes=job.get("timeout_minutes", 30))
            if last is None:
                append_row(reg, job=name, slot=sid, attempt=0, status="missed",
                           summary="no outcome row for this slot after the grace period", cause="missed-slot")
                last = {"status": "missed", "ts": now.isoformat()}
            elif last["status"] == "attempting" and dt.datetime.fromisoformat(last["ts"]) + timeout < now:
                append_row(reg, job=name, slot=sid, attempt=last.get("attempt", 1), status="failed",
                           summary="attempt started but no outcome after the timeout", cause="no-outcome")
                last = {"status": "failed", "ts": now.isoformat()}
            elif last["status"] == "attempting":
                unresolved.append((name, sid, "still running"))
                continue
            attempts = max([r.get("attempt", 0) for r in mine] + [0])
            delays = job.get("retry_delays_minutes", [15, 60, 240])
            if args.retry and job.get("safe_to_repeat", False) and attempts < len(delays) + 1:
                wait = dt.timedelta(minutes=delays[max(attempts - 1, 0)])
                if dt.datetime.fromisoformat(last["ts"]) + wait <= now:
                    print(f"retrying {name} slot {sid} (attempt {attempts + 1})")
                    if run_job(reg, name, sid, attempts + 1):
                        continue
            rows = read_rows(reg)
            mine, ok = slot_state(rows, name, sid)
            if ok:
                continue
            attempts = max([r.get("attempt", 0) for r in mine] + [0])
            exhausted = (not job.get("safe_to_repeat", False)) or attempts >= len(delays) + 1
            stuck_for = now - s
            too_old = stuck_for > dt.timedelta(minutes=job.get("escalate_after_minutes", 240))
            why = mine[-1].get("summary", "") if mine else "missed"
            unresolved.append((name, sid, why))
            if exhausted or too_old:
                if flag(reg, name, sid, why, args.notify):
                    print(f"FLAGGED {name} slot {sid}")
    for n, s, why in unresolved:
        print(f"unresolved: {n} slot {s} ({why})")
    print(f"{len(unresolved)} unresolved slot(s)")
    return 1 if unresolved else 0


def cmd_report(reg, args):
    now = now_local()
    rows = read_rows(reg)
    start = now - dt.timedelta(days=args.days)
    bad = 0
    for name in reg["jobs"]:
        print(f"## {name}")
        for r in rows:
            if r.get("job") == name and r.get("status") in ("missed", "failed") and r.get("ts", "") >= start.isoformat():
                bad += 1
                _, ok = slot_state(rows, name, r["slot"])
                print(f"- slot {r['slot']} {r['status']}: {r.get('summary', '')} ({'later resolved' if ok else 'STILL UNRESOLVED'})")
        oks = [r for r in rows if r.get("job") == name and r["status"] == "ok" and r.get("ts", "") >= start.isoformat()]
        print(f"  ok runs in period: {len(oks)}")
    print(f"{bad} missed or failed row(s) in the last {args.days} days")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--registry", default="jobs.json")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("job"); r.add_argument("--slot"); r.add_argument("--attempt", type=int, default=1)
    c = sub.add_parser("check"); c.add_argument("--retry", action="store_true"); c.add_argument("--notify", action="store_true")
    c.add_argument("--now"); c.add_argument("--lookback-days", type=int, default=7)
    p = sub.add_parser("report"); p.add_argument("--days", type=int, default=7)
    a = ap.parse_args()
    reg = load_registry(a.registry)
    if a.cmd == "run":
        if a.job not in reg["jobs"]:
            print(f"could not run: job '{a.job}' is not in the registry"); return 2
        slot = a.slot
        if not slot:
            ds = slots_between(reg["jobs"][a.job], now_local() - dt.timedelta(days=8), now_local())
            if not ds:
                print("could not run: no slot found; pass --slot YYYY-MM-DDTHH:MM"); return 2
            slot = slot_id(ds[-1])
        ok = run_job(reg, a.job, slot, a.attempt)
        print(("ok" if ok else "FAILED") + f": {a.job} slot {slot}")
        return 0 if ok else 1
    if a.cmd == "check":
        return cmd_check(reg, a)
    return cmd_report(reg, a)


if __name__ == "__main__":
    sys.exit(main())

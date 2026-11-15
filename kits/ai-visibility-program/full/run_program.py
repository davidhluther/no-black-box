#!/usr/bin/env python3
"""Run the AI visibility question battery for every site in a program, and never fail quietly.

Commands (run from your program folder, the one that holds config.json):

  python3 run_program.py run [--site ID] [--slot YYYY-MM] [--dry-run] [--force]
      Runs the API battery for each site, retries a failed site, and writes every
      attempt to program-ledger.csv. A site that already has a good run for the
      slot is skipped unless you pass --force.

  python3 run_program.py check
      Looks at the ledger and prints every site that is missed, failed or waiting
      for its scoring review. Sends an alert if PROGRAM_ALERT_WEBHOOK is set.
      Exits with 1 when anything is wrong. Schedule it daily.

  python3 run_program.py status
      Prints the same table without alerting.

  python3 run_program.py check --test-alert
      Posts a test message to your alert channel, to prove alerts arrive.

  python3 run_program.py check --today YYYY-MM-DD
      Pretends today is that date. For a practice drill only; it changes nothing.

It reads settings from config.json (see config.example.json). It never prints a key.
API keys come from environment variables, as in the single-site kit.
Standard library only.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import date, datetime
from pathlib import Path

LEDGER = "program-ledger.csv"
COLUMNS = ["slot", "site", "attempt", "started", "finished", "exit_code", "status", "note"]


def load_config(path):
    try:
        cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("Cannot read %s as settings (%s). See E41 in fixes.md." % (path, type(exc).__name__), file=sys.stderr)
        sys.exit(2)
    if not isinstance(cfg.get("sites"), list) or not cfg["sites"] or not isinstance(cfg.get("program"), dict):
        print("config.json needs a program block and a non-empty sites list. See E41 in fixes.md.", file=sys.stderr)
        sys.exit(2)
    return cfg


def read_ledger(base):
    p = base / LEDGER
    if not p.is_file():
        return []
    with p.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def append_ledger(base, row):
    p = base / LEDGER
    new = not p.is_file()
    with p.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in COLUMNS})


def alert(cfg, lines):
    """Print the alert and post it. Returns True only when the post succeeded."""
    text = "AI visibility program\n" + "\n".join(lines)
    print(text)
    env_name = (cfg["program"].get("alert") or {}).get("webhook_env", "PROGRAM_ALERT_WEBHOOK")
    url = os.environ.get(env_name, "")
    if not url:
        print("(No alert sent: %s is not set. See E48 in fixes.md.)" % env_name)
        return False
    try:
        req = urllib.request.Request(url, data=json.dumps({"text": text}).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=20).read()
        print("(Alert posted.)")
        return True
    except Exception as exc:  # the alert must never hide the original failure
        print("(Alert could not be posted: %s. See E48 in fixes.md.)" % type(exc).__name__)
        return False


def site_dir(base, site):
    return (base / site["config_file"]).resolve().parent


def run_dir_busy(run_dir):
    """True when another process holds <run dir>/.run.lock (run_api_battery.py takes it
    for the whole run). Never move a run folder that something is still writing."""
    lock_path = run_dir / ".run.lock"
    if not lock_path.is_file():
        return False
    try:
        handle = open(lock_path, "a+")
    except OSError:
        return True
    try:
        try:
            import fcntl
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return True
            fcntl.flock(handle, fcntl.LOCK_UN)
        except ImportError:  # Windows
            import msvcrt
            try:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                return True
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return False
    finally:
        handle.close()


def run_site(base, cfg, site, slot, dry_run, force=False):
    prog = cfg["program"]
    attempts = int(prog.get("max_attempts", 2))
    wait = int(prog.get("retry_wait_minutes", 30)) * 60
    runner = prog.get("runner", "scripts/run_api_battery.py")
    cmd = [sys.executable, runner, "--config", str(base / site["config_file"]), "--run-id", slot]
    if cfg.get("providers"):
        cmd += ["--providers", ",".join(cfg["providers"])]
    cmd += ["--dry-run"] if dry_run else ["--yes"]
    if force and not dry_run:
        cmd += ["--overwrite"]  # --force means redo the slot; the runner refuses otherwise
    sdir = site_dir(base, site)
    (base / "logs").mkdir(exist_ok=True)
    for n in range(1, attempts + 1):
        started = datetime.now().isoformat(timespec="seconds")
        proc = subprocess.run(cmd, capture_output=True, text=True)
        out = (proc.stdout or "") + (proc.stderr or "")
        log = base / "logs" / ("%s-%s-attempt%d.log" % (slot, site["id"], n))
        log.write_text(out, encoding="utf-8")
        errors = sum(1 for ln in out.splitlines() if " ERROR" in ln or " EMPTY" in ln)
        status = "ok" if proc.returncode == 0 else "failed"
        if dry_run:
            status = "dry-run-ok" if proc.returncode == 0 else "dry-run-failed"
        note = "%d question errors" % errors if errors else ""
        run_dir = sdir / "runs" / ("%s-api" % slot)
        busy = proc.returncode != 0 and not dry_run and run_dir_busy(run_dir)
        if busy:
            note = "another run was still writing this slot; nothing was moved or retried"
        append_ledger(base, {"slot": slot, "site": site["id"], "attempt": n, "started": started,
                             "finished": datetime.now().isoformat(timespec="seconds"),
                             "exit_code": proc.returncode, "status": status, "note": note})
        print("%s attempt %d: %s %s" % (site["id"], n, status, note))
        if proc.returncode == 0:
            return True
        if dry_run:
            return False
        if busy:  # in progress elsewhere: its own failure, and no retry can fix it now
            print("%s: %s is in use by another run; left in place. Check again when it finishes."
                  % (site["id"], run_dir))
            return False
        if (run_dir / "scored.csv").is_file():  # never move a reviewed run aside
            print("%s: %s holds a reviewed scored.csv; left in place" % (site["id"], run_dir))
        elif run_dir.is_dir():  # keep the failed evidence, free the name for the retry
            shutil.move(str(run_dir), str(run_dir) + ".failed-%d" % n)
        if n < attempts:
            print("%s: waiting %d minutes before attempt %d" % (site["id"], wait // 60, n + 1))
            time.sleep(wait)
    return False


def cmd_run(args, base, cfg):
    slot = args.slot or date.today().strftime("%Y-%m")
    ledger = read_ledger(base)
    failed = []
    if args.site and not any(s.get("id") == args.site for s in cfg["sites"]):
        print("No site with id %r in the program config." % args.site, file=sys.stderr)
        return 2
    for site in cfg["sites"]:
        if args.site and site["id"] != args.site:
            continue
        if args.force and not args.dry_run and site.get("config_file") and \
                (site_dir(base, site) / "runs" / ("%s-api" % slot) / "scored.csv").is_file():
            print("%s: slot %s is already reviewed (scored.csv exists); refusing --force. "
                  "Move that run folder aside yourself first." % (site.get("id"), slot))
            failed.append(site.get("id", "?"))
            continue
        done = latest_outcome(ledger, slot, site["id"]) == "ok"
        if done and not args.force and not args.dry_run:
            print("%s: slot %s already has a good run; skipping (use --force to redo)." % (site["id"], slot))
            continue
        try:
            ok = run_site(base, cfg, site, slot, args.dry_run, args.force)
        except Exception as exc:  # one bad site must not hide the rest
            print("%s: could not run (%s: %s)" % (site.get("id", "?"), type(exc).__name__, exc))
            append_ledger(base, {"slot": slot, "site": site.get("id", "?"), "attempt": 0,
                                 "started": datetime.now().isoformat(timespec="seconds"),
                                 "finished": datetime.now().isoformat(timespec="seconds"),
                                 "exit_code": "", "status": "dry-run-failed" if args.dry_run else "failed",
                                 "note": type(exc).__name__})
            ok = False
        if not ok:
            failed.append(site.get("id", "?"))
    if failed and not args.dry_run:
        alert(cfg, ["Slot %s: run FAILED for %s after retries." % (slot, ", ".join(failed)),
                    "Logs are in the logs folder. Fix the cause, then run with --site and --force."])
        return 1
    return 1 if failed else 0


def latest_outcome(ledger, slot, site_id):
    """Status of the most recent real attempt (ok or failed) for this site and
    slot, or None. A later failed --force run outranks an earlier ok row."""
    mine = [r["status"] for r in ledger if r["slot"] == slot and r["site"] == site_id
            and r["status"] in ("ok", "failed")]
    return mine[-1] if mine else None


def problems(base, cfg, today):
    prog = cfg["program"]
    slot = today.strftime("%Y-%m")
    due = int(prog.get("run_day_of_month", 3)) + int(prog.get("grace_days", 2))
    review_days = int(prog.get("review_days", 5))
    ledger = read_ledger(base)
    rows, bad = [], []
    for site in cfg["sites"]:
        mine = [r for r in ledger if r["slot"] == slot and r["site"] == site["id"]
                and r["status"] in ("ok", "failed")]
        if mine and mine[-1]["status"] == "ok":
            run_dir = site_dir(base, site) / "runs" / ("%s-api" % slot)
            age = (datetime.now() - datetime.fromisoformat(mine[-1]["finished"])).days
            if not (run_dir / "scored.csv").is_file() and age >= review_days:
                state = "NEEDS REVIEW (scored.csv missing %d days after the run)" % age
                bad.append("%s: %s" % (site["id"], state))
            else:
                state = "ok"
        elif mine:
            state = "FAILED (%d attempts, last exit %s)" % (len(mine), mine[-1]["exit_code"])
            bad.append("%s: %s" % (site["id"], state))
        elif today.day > due:
            state = "MISSED (no run recorded for %s, due by day %d)" % (slot, due)
            bad.append("%s: %s" % (site["id"], state))
        else:
            state = "waiting (due by day %d)" % due
        rows.append((site["id"], state))
    return slot, rows, bad


def cmd_check(args, base, cfg, notify=True):
    if args.test_alert:
        return 0 if alert(cfg, ["This is a test alert. Nothing is wrong."]) else 1
    today = date.fromisoformat(args.today) if args.today else date.today()
    slot, rows, bad = problems(base, cfg, today)
    print("Slot %s" % slot)
    for sid, state in rows:
        print("  %-24s %s" % (sid, state))
    if bad and notify:
        alert(cfg, ["Slot %s needs attention." % slot] + bad)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["run", "check", "status"])
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--site")
    ap.add_argument("--slot", help="label for this run, default is this year and month (YYYY-MM)")
    ap.add_argument("--dry-run", action="store_true", help="check keys and questions, send nothing")
    ap.add_argument("--test-alert", action="store_true", help="post a test message to the alert channel")
    ap.add_argument("--today", help="pretend today is YYYY-MM-DD (practice drills only)")
    ap.add_argument("--force", action="store_true", help="run even if the slot already has a good run")
    args = ap.parse_args()
    cfg_path = Path(args.config).expanduser().resolve()
    cfg = load_config(cfg_path)
    base = cfg_path.parent
    if args.command == "run":
        return cmd_run(args, base, cfg)
    return cmd_check(args, base, cfg, notify=(args.command == "check"))


if __name__ == "__main__":
    sys.exit(main())

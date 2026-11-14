#!/usr/bin/env python3
"""Run a job and write down what happened, or check that every job ran on time.

Two commands, standard library only, no network, no secrets.

  run    Run any command, record the result in a CSV log, retry if you ask,
         and pass the command's exit code through.
           python3 tools/job_log.py run --job feeds --retries 1 -- python3 --version

  check  Read the log and the job list in your config file. Print one line per
         job. Exit 1 if any job has missed its slot, so a scheduler, a chat
         bot or a person can act on it the same day.
           python3 tools/job_log.py check --config config.json

The job list lives in config.json under "schedule" -> "jobs", for example
  {"name": "feeds", "every_days": 7, "grace_days": 1}
A job counts as missed when its last successful run is older than
every_days plus grace_days, or when it has never succeeded. A missed slot is a
failure even when older data is still fine to use.

The log records only the job name, start time, seconds, attempt number and
exit code. It never records the command line, its output or any environment
variable, so it cannot leak a key.
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

FIELDS = ["started", "job", "attempt", "seconds", "exit_code", "status"]
DEFAULT_LOG = "ops/job-log.csv"


def log_path(config: dict, override: str | None) -> Path:
    if override:
        return Path(override)
    return Path(config.get("schedule", {}).get("log_file", DEFAULT_LOG))


def load_config(path: str | None) -> dict:
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        print("job_log: config file is not valid JSON", file=sys.stderr)
        return {}


def append_row(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def cmd_run(args: argparse.Namespace) -> int:
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("job_log run: give a command after --", file=sys.stderr)
        return 2
    config = load_config(args.config)
    path = log_path(config, args.log)
    attempts = max(0, args.retries) + 1
    code = 1
    for attempt in range(1, attempts + 1):
        started = datetime.now()
        t0 = time.time()
        try:
            code = subprocess.call(command)
        except OSError:
            code = 127
        except KeyboardInterrupt:
            code = 130
            append_row(path, {"started": started.strftime("%Y-%m-%dT%H:%M:%S"), "job": args.job,
                              "attempt": attempt, "seconds": round(time.time() - t0, 1),
                              "exit_code": code, "status": "FAILED"})
            raise
        row = {
            "started": started.strftime("%Y-%m-%dT%H:%M:%S"),
            "job": args.job,
            "attempt": attempt,
            "seconds": round(time.time() - t0, 1),
            "exit_code": code,
            "status": "ok" if code == 0 else "FAILED",
        }
        append_row(path, row)
        if code == 0:
            return 0
        if attempt < attempts:
            print("job_log: %s failed (exit %s), retrying in %s seconds"
                  % (args.job, code, args.wait), file=sys.stderr)
            time.sleep(args.wait)
    print("job_log: %s FAILED after %d attempt(s). Tell the job's owner today."
          % (args.job, attempts), file=sys.stderr)
    return code or 1


def read_rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def parse_time(text: str) -> datetime | None:
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S")
    except (TypeError, ValueError):
        return None


def cmd_check(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    jobs = config.get("schedule", {}).get("jobs", [])
    if not jobs:
        print("job_log check: no jobs listed under schedule.jobs in the config file.")
        print("A check with nothing to check is not a pass. Add your jobs.")
        return 2
    path = log_path(config, args.log)
    rows = read_rows(path)
    now = datetime.now()
    missed = 0
    print("%-22s %-10s %-20s %s" % ("job", "state", "last success", "detail"))
    for job in jobs:
        name = job.get("name", "")
        every = float(job.get("every_days", 7))
        grace = float(job.get("grace_days", 1))
        mine = [r for r in rows if r.get("job") == name]
        oks = [parse_time(r["started"]) for r in mine if r.get("status") == "ok"]
        oks = [t for t in oks if t]
        last_ok = max(oks) if oks else None
        limit = timedelta(days=every + grace)
        if last_ok is None:
            state, detail = "MISSED", "never succeeded"
        elif now - last_ok > limit:
            days = (now - last_ok).total_seconds() / 86400
            state, detail = "MISSED", "%.1f days since success, limit %.1f" % (days, every + grace)
        else:
            state, detail = "ok", "within %.1f days" % (every + grace)
        if state == "ok" and mine and mine[-1].get("status") != "ok":
            state, detail = "FAILED", "newest run failed; last success still inside the limit"
        if state != "ok":
            missed += 1
        print("%-22s %-10s %-20s %s" % (name, state,
              last_ok.strftime("%m/%d/%Y %H:%M") if last_ok else "none", detail))
    if missed:
        print("\n%d job(s) MISSED or FAILED. Record it, retry it, and tell the owner today." % missed)
        return 1
    print("\nAll jobs are inside their slots.")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run a command and log the result")
    r.add_argument("--job", required=True, help="short job name, as listed in schedule.jobs")
    r.add_argument("--config", default="config.json")
    r.add_argument("--log", default=None, help="log file (default ops/job-log.csv)")
    r.add_argument("--retries", type=int, default=0, help="extra attempts after a failure")
    r.add_argument("--wait", type=int, default=60, help="seconds to wait between attempts")
    r.add_argument("command", nargs=argparse.REMAINDER)
    r.set_defaults(func=cmd_run)
    c = sub.add_parser("check", help="report any job that missed its slot")
    c.add_argument("--config", default="config.json")
    c.add_argument("--log", default=None)
    c.set_defaults(func=cmd_check)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

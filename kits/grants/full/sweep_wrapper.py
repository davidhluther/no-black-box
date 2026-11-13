#!/usr/bin/env python3
"""Run the weekly grants sweep so that a failure or a missed week can never go unnoticed.

Use this in your computer's scheduler instead of calling sweep.py directly.

  python3 sweep_wrapper.py --engine <path to engine folder> --config <path to your org json>
  python3 sweep_wrapper.py --engine <...> --config <...> --check-fresh 8

What it does
  Run mode      Writes an "attempting" line before work, runs the sweep, then writes "ok" or
                "failed" with the exit code and the end of any error text. On failure it raises
                an alert.
  --check-fresh Looks at the log. If there has been no "ok" line in the last N days (or ever),
                it raises an alert. Schedule this daily. A missed week counts as a failure even
                when older results are still on disk.

How an alert is raised (every step that applies is done)
  1. A file named ALERT-<date>.txt is written in the sweep folder.
  2. A message is printed to the error output.
  3. On a Mac, a desktop notification is tried.
  4. If these settings exist in the environment, an email is sent: SMTP_HOST, SMTP_PORT
     (default 587), SMTP_USER, SMTP_PASSWORD and ALERT_TO. They are read from the
     environment only. This program never prints them or writes them anywhere.

The log is <sweep folder>/wrapper.jsonl, one JSON object per line, append-only.
"""
import argparse
import datetime as dt
import json
import os
import smtplib
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path


def now():
    return dt.datetime.now(dt.timezone.utc)


def log(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": now().isoformat(timespec="seconds"), **row}) + "\n")


def alert(sweep_dir, subject, text):
    stamp = dt.date.today().isoformat()
    (sweep_dir / f"ALERT-{stamp}.txt").write_text(f"{subject}\n\n{text}\n", encoding="utf-8")
    print(f"ALERT: {subject}\n{text}", file=sys.stderr)
    try:  # best effort desktop notification on a Mac
        subprocess.run(["osascript", "-e",
                        f'display notification "{subject}" with title "Grants sweep"'],
                       capture_output=True, timeout=10)
    except Exception:
        pass
    host, to = os.environ.get("SMTP_HOST"), os.environ.get("ALERT_TO")
    if host and to:
        try:
            msg = EmailMessage()
            msg["Subject"], msg["To"] = subject, to
            msg["From"] = os.environ.get("SMTP_USER", to)
            msg.set_content(text)
            with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=30) as s:
                s.starttls()
                if os.environ.get("SMTP_USER") and os.environ.get("SMTP_PASSWORD"):
                    s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
                s.send_message(msg)
        except Exception as e:  # say that the email failed, never include the settings
            print(f"email alert could not be sent ({type(e).__name__}); the ALERT file was still written",
                  file=sys.stderr)


def last_ok(path):
    last = None
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if row.get("event") == "ok":
                last = dt.datetime.fromisoformat(row["at"])
    return last


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engine", required=True, help="the grants-pipeline engine folder (holds sweep.py)")
    ap.add_argument("--config", required=True, help="your organization's config json")
    ap.add_argument("--check-fresh", type=int, metavar="DAYS",
                    help="alert if no successful run was logged in the last DAYS days")
    a = ap.parse_args(argv)
    engine = Path(a.engine).expanduser().resolve()
    sys.path.insert(0, str(engine))
    import gp_common as gp  # the engine's own config loader
    cfg = gp.load_config(a.config)
    sweep_dir = Path(cfg["paths"]["sweep_dir"])
    wlog = sweep_dir / "wrapper.jsonl"

    if a.check_fresh is not None:
        seen = last_ok(wlog)
        age = (now() - seen).days if seen else None
        if seen is None or age > a.check_fresh:
            alert(sweep_dir, "Grants sweep has not run",
                  f"No successful sweep is logged in the last {a.check_fresh} days "
                  f"(last success: {seen.date().isoformat() if seen else 'never'}). "
                  f"Run the sweep by hand and read {wlog}.")
            return 1
        print(f"fresh: last success {seen.date().isoformat()}")
        return 0

    log(wlog, {"event": "attempting"})
    try:
        r = subprocess.run([sys.executable, str(engine / "sweep.py"), "--config", a.config],
                           capture_output=True, text=True, timeout=1800)
        code, tail = r.returncode, (r.stdout + r.stderr)[-300:]
    except Exception as e:
        code, tail = 99, f"{type(e).__name__}: {e}"[:300]
    if code == 0:
        log(wlog, {"event": "ok"})
        return 0
    log(wlog, {"event": "failed", "exit_code": code, "tail": tail})
    alert(sweep_dir, "Grants sweep failed",
          f"The weekly sweep exited with code {code}. End of its output:\n{tail}\n"
          f"Full history is in {sweep_dir / 'runs.jsonl'} and {wlog}.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""One monthly tell-audit run with fixed arguments, so a headless allowlist can name it exactly.

Scores the live sitemap into <runs-dir>/<today ET>/live_scores.csv, finds the newest prior
dated folder that has a live_scores.csv, and prints cohort_compare's table against it. The
runs dir must sit inside the working directory; nothing is written anywhere else.

    /opt/anaconda3/bin/python3 monthly_run.py --sitemap URL --include /resources/ \\
        --selector article --runs-dir planning/seo/tell-audit
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import subprocess
import tempfile
import sys

HERE = Path(__file__).resolve().parent


def today_et() -> str:
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("America/New_York")).date().isoformat()
    except Exception:  # pragma: no cover - no tz database
        return dt.date.today().isoformat()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sitemap", required=True)
    ap.add_argument("--include", required=True)
    ap.add_argument("--selector", required=True)
    ap.add_argument("--runs-dir", required=True)
    a = ap.parse_args()

    cwd = Path.cwd().resolve()
    runs = (cwd / a.runs_dir).resolve()
    if cwd not in runs.parents and runs != cwd:
        print("runs dir %s is outside the working directory; nothing done" % runs, file=sys.stderr)
        return 2
    day = today_et()
    out = runs / day / "live_scores.csv"
    # score_batch.py writes its CSV before it reports an incomplete run, so score
    # into a temp file and replace the dated CSV only after a clean exit; a failed
    # rerun must never overwrite that day's good scores.
    # A unique temp file per run, so two runs on the same day never share or delete one.
    out.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=out.name + ".", suffix=".partial", dir=out.parent)
    os.close(fd)
    tmp = Path(tmp_name)
    code = subprocess.call([sys.executable, str(HERE / "score_batch.py"), "--sitemap", a.sitemap,
                            "--include", a.include, "--selector", a.selector,
                            "--store", str(runs / ".cache"), "--out", str(tmp)])
    if code != 0 or not tmp.is_file():
        tmp.unlink(missing_ok=True)
        print("scoring failed (exit %d); no comparison run%s" % (
            code, "; kept the earlier %s" % out.name if out.is_file() else ""), file=sys.stderr)
        return code or 1
    os.replace(tmp, out)
    prior = sorted(p for p in runs.iterdir()
                   if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name) and p.name < day
                   and (p / "live_scores.csv").is_file())
    print("run dir: %s" % out.parent.relative_to(cwd))
    if not prior:
        print("no prior baseline; this run is the first")
        return 0
    print("baseline: %s" % (prior[-1] / "live_scores.csv").relative_to(cwd))
    return subprocess.call([sys.executable, str(HERE / "cohort_compare.py"), str(out),
                            "--baseline", str(prior[-1] / "live_scores.csv")])


if __name__ == "__main__":
    sys.exit(main())

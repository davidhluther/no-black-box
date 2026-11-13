#!/usr/bin/env python3
"""Check Looker export CSVs against references/tab-layouts.json. Reads files only.

Usage: python3 validate_tabs.py <folder-with-csvs>
Checks headers, date columns (yyyy-mm-dd), and number columns (no commas, % or $).
"""
import csv
import json
import re
import sys
from pathlib import Path

LAYOUT = json.loads((Path(__file__).resolve().parent.parent / "references" / "tab-layouts.json").read_text())
DATE_COLS = {"month", "data_through", "date_added", "due", "date_done"}
NUM_COLS = {"organic_sessions", "organic_users", "engaged_sessions", "key_events", "search_clicks",
            "search_impressions", "search_ctr", "search_avg_position", "clicks", "impressions", "ctr",
            "position", "sessions", "engagement_rate", "search_position"}


def main(folder):
    bad = 0
    for tab, headers in LAYOUT.items():
        f = Path(folder) / f"{tab}.csv"
        if not f.exists():
            print(f"missing: {f.name} (skip if you do not use this tab)")
            continue
        rows = list(csv.reader(f.open(newline="", encoding="utf-8")))
        if not rows or rows[0] != headers:
            print(f"{f.name}: headers do not match. Expected: {','.join(headers)}")
            bad += 1
            continue
        for n, row in enumerate(rows[1:], start=2):
            for h, v in zip(headers, row):
                v = v.strip()
                if not v:
                    continue
                if h in DATE_COLS and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                    print(f"{f.name} row {n}: {h} should be yyyy-mm-dd")
                    bad += 1
                if h in NUM_COLS and not re.fullmatch(r"-?\d+(\.\d+)?", v):
                    print(f"{f.name} row {n}: {h} should be a plain number")
                    bad += 1
    print("ok" if not bad else f"{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))

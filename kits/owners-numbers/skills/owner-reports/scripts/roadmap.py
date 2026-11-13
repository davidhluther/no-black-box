#!/usr/bin/env python3
"""Draft a 12-month roadmap from a targets file.

    python3 roadmap.py TARGETS.csv [--business NAME] [--start-month 2026-10] [--out FILE]

TARGETS.csv columns: metric, baseline, target, quarter, why.
A blank baseline or target prints as "to set". A target is only a real
number when you typed it. The script never invents one, because a target
is chosen with your own numbers in hand.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
from pathlib import Path


def quarters(start: dt.date):
    out = []
    y, m = start.year, start.month
    for i in range(4):
        a = (y * 12 + (m - 1) + 3 * i)
        b = a + 2
        out.append((f"{a % 12 + 1:02d}/{a // 12}", f"{b % 12 + 1:02d}/{b // 12}"))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Draft a 12-month roadmap.")
    ap.add_argument("targets", type=Path)
    ap.add_argument("--business", default="Your business")
    ap.add_argument("--start-month", default=dt.date.today().strftime("%Y-%m"))
    ap.add_argument("--out", type=Path, default=Path("roadmap.md"))
    a = ap.parse_args(argv)
    y, m = map(int, a.start_month.split("-"))
    qs = quarters(dt.date(y, m, 1))
    with a.targets.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    show = lambda v: (v or "").strip() or "to set"
    L = [f"# {a.business} 12-Month Roadmap", "", "Targets marked to set are not decided yet. Choose each one with your own baseline in hand.", ""]
    for i, (s, e) in enumerate(qs, 1):
        L += [f"## Quarter {i}, {s} to {e}", "| Metric | Baseline | Target | Why it matters |", "|---|---|---|---|"]
        mine = [r for r in rows if (r.get("quarter") or "").strip() in (str(i), f"Q{i}")]
        L += [f"| {r['metric']} | {show(r.get('baseline'))} | {show(r.get('target'))} | {r.get('why', '')} |" for r in mine]
        if not mine:
            L.append("| | | | |")
        L += ["", "First action this quarter. ______", ""]
    a.out.write_text("\n".join(L))
    print(a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

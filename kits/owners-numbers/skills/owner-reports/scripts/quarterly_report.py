#!/usr/bin/env python3
"""Quarterly report from up to three monthly scorecard.json files.

    python3 quarterly_report.py MONTH1.json MONTH2.json MONTH3.json [--out FILE]

Observed numbers (what happened each month) are findings. The one naive
projection for next quarter is a what-if: it continues the average monthly
step in a straight line and knows nothing about seasons. Library sections
built from example inputs are listed as what-ifs, never as findings.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as M  # noqa: E402


def trend(values):
    if len(values) < 2:
        return None
    steps = [b - a for a, b in zip(values, values[1:])]
    if all(s >= 0 for s in steps) and any(s > 0 for s in steps):
        word = "rising"
    elif all(s <= 0 for s in steps) and any(s < 0 for s in steps):
        word = "falling"
    elif all(s == 0 for s in steps):
        word = "flat"
    else:
        word = "mixed"
    return {"direction": word, "next_guess": values[-1] + sum(steps) / len(steps)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Quarterly report from monthly scorecards.")
    ap.add_argument("months", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, default=Path("quarterly-report.md"))
    a = ap.parse_args(argv)
    months = [json.loads(p.read_text()) for p in a.months]
    name = months[0]["business"]
    labels = [m["period"].split(" to ")[0][:2] + "/" + m["period"][6:10] for m in months]
    rows = [("Sales", [m["sales"]["total"] for m in months]),
            ("Money in", [m["money"]["money_in"] for m in months]),
            ("Operating costs", [m["money"]["money_out"] for m in months]),
            ("Net operating", [m["money"]["net_operating"] for m in months])]
    L = [f"# {name} Quarterly Report", f"Months covered {', '.join(labels)}", "",
         "## What happened", "| Line | " + " | ".join(labels) + " | Direction |", "|---|" + "---|" * (len(labels) + 1)]
    for label, vals in rows:
        t = trend(vals)
        L.append(f"| {label} | " + " | ".join(M.money(v) for v in vals) + f" | {t['direction'] if t else 'n/a'} |")
    net = sum(v for v in rows[3][1])
    L += ["", f"Across the period the business kept {M.money(net)} after operating costs, before owner draws of {M.money(sum(m['money']['owner_draws'] for m in months))}.", ""]
    t = trend(rows[0][1])
    if t:
        L += ["## One naive look ahead", f"What-if. Continuing the average monthly step in sales would put next month near {M.money(t['next_guess'])}. "
              "This is a straight line and knows nothing about your busy and slow seasons. Name the season next to it before anyone relies on it.", ""]
    last = months[-1]
    L += ["## Where the money sits", ""]
    for key, title in [("cost_to_serve", "What a line really costs to serve"), ("customer_lifetime_value", "What a customer is worth"),
                       ("headcount_payback", "When the next hire pays for itself"), ("working_capital", "Cash caught between paying and getting paid")]:
        v = last["library"][key]
        kind = "Finding" if v["basis"] == "actual" else "What-if with example inputs"
        tail = "" if v["basis"] == "actual" else " Fill in the matching settings to turn this into a finding."
        L.append(f"- {title}. {kind}.{tail}")
    L += ["", "## Decisions for next quarter", "Write the two decisions this report points at, who owns each, and the date each is due.", "",
          "| Decision | Owner | Due |", "|---|---|---|", "| | | |", "| | | |"]
    a.out.write_text("\n".join(L) + "\n")
    print(a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

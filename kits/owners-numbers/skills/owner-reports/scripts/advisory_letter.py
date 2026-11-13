#!/usr/bin/env python3
"""Draft a short monthly advisory letter from one scorecard.json.

    python3 advisory_letter.py scorecard.json [--from NAME] [--to NAME] [--out FILE]

The letter states what moved, names the one thing to look at, and asks one
question. It is a draft for a person to edit and sign, built only from the
scorecard's own numbers. Anything marked what-if on the scorecard stays out
of the body, so a worked example never reads as a finding.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as M  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description="Draft a monthly advisory letter.")
    ap.add_argument("scorecard", type=Path)
    ap.add_argument("--from", dest="sender", default="Your name")
    ap.add_argument("--to", default="Owner")
    ap.add_argument("--out", type=Path, default=Path("advisory-letter.md"))
    a = ap.parse_args(argv)
    o = json.loads(a.scorecard.read_text())
    m, s = o["money"], o["sales"]
    change = (s["total"] - s["prior_total"]) / s["prior_total"] if s["prior_total"] else None
    topic, text = o["flag"]
    L = [f"Dear {a.to},", "",
         f"Here is the short version of {o['period']}. {o['verdict']}", "",
         f"Sales came to {M.money(s['total'])}" + (f", {change*100:+.0f}% against the month before." if change is not None else "."),
         f"Money in was {M.money(m['money_in'])} against {M.money(m['money_out'])} in operating costs. You took {M.money(m['owner_draws'])} in draws.", "",
         f"The one thing to look at this month is {topic.lower()}. {text}", ""]
    if "customers" in o:
        c = o["customers"]
        L += [f"{c['clients_served']} clients came in, {c['new']} of them new.", ""]
    L += ["One question for next time. What would you change about this one thing if it stayed exactly as it is for three more months?", "",
          "Sincerely,", a.sender, ""]
    a.out.write_text("\n".join(L))
    print(a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

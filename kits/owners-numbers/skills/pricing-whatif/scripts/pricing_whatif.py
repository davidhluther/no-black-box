#!/usr/bin/env python3
"""Pricing what-if one-pager from your own price and cost per line.

    python3 pricing_whatif.py LINES.csv [--moves=-10,-5,5,10] [--volume-change=-0.05]
                              [--business NAME] [--out FILE]

LINES.csv columns: line, price, variable_cost, units_per_month.
Variable cost means what one more sale costs you directly (supplies,
card fees, a commission), not rent or salaried pay.

Two kinds of statement stay apart on the page:
  Break-even shift is a finding. It is exact arithmetic from your price
  and cost. It says how much volume a price move can lose (or must win)
  before the move stops paying. It forecasts nothing.
  Volume response is a what-if. You name a volume change, and the page
  shows what that assumption would do. It is never a prediction.
Reads one file, writes one markdown file, makes no network calls.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as M  # noqa: E402


def load(path: Path):
    if not path.exists():
        raise SystemExit(f"E20 Missing file {path.name}. See fixes.md.")
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    need = {"line", "price", "variable_cost"}
    if not rows or not need <= set(rows[0]):
        raise SystemExit("E21 lines.csv needs the columns line, price, variable_cost, units_per_month. See fixes.md.")
    return rows


def shift_words(p):
    s = p["breakeven_volume_shift"]
    if s is None:
        return "no volume recovers this move, because the cut erases what each sale keeps"
    if s < 0:
        return f"you could lose up to {abs(s) * 100:.0f}% of sales and still come out even"
    if s > 0:
        return f"you would need to win {s * 100:.0f}% more sales to come out even"
    return "nothing changes"


def render(rows, moves, vol, business):
    L = [f"# {business} Pricing What-If", "",
         "Break-even shifts below are findings from your own price and cost. Volume rows, when present, are what-ifs built on a volume change you chose.", ""]
    for r in rows:
        price, vc = float(r["price"]), float(r["variable_cost"])
        units = float(r["units_per_month"]) if r.get("units_per_month") else None
        cm = M.contribution_margin(price, vc)
        L += [f"## {r['line']}", f"At {M.money(price)} and {M.money(vc)} of variable cost, each sale keeps {M.money(cm['unit'])}, or {M.pct(cm['ratio'])} of the price.", "",
              "| Price move | New price | Break-even volume shift | Plain reading |", "|---|---|---|---|"]
        for mv in moves:
            p = M.price_sensitivity(price, vc, mv / 100)
            sh = p["breakeven_volume_shift"]
            L.append(f"| {mv:+g}% | {M.money(p['new_price'])} | {'n/a' if sh is None else f'{sh*100:+.1f}%'} | {shift_words(p)} |")
        if vol is not None:
            L += ["", f"What-if. If volume changed by {vol*100:+g}% after each move:", "", "| Price move | Change in contribution | Better off? | Dollars a month |", "|---|---|---|---|"]
            for mv in moves:
                v = M.volume_response(price, vc, mv / 100, vol, units)
                amt = v["contribution_change_amount"]
                L.append(f"| {mv:+g}% | {M.pct(v['contribution_change_ratio'], 1)} | {'yes' if v['better_off'] else 'no'} | {M.money(amt) if amt is not None else 'n/a'} |")
        L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pricing what-if one-pager.")
    ap.add_argument("lines", type=Path)
    ap.add_argument("--moves", default="-10,-5,5,10")
    ap.add_argument("--volume-change", type=float, default=None, help="assumed volume change as a fraction, for example -0.05")
    ap.add_argument("--business", default="Your business")
    ap.add_argument("--out", type=Path, default=Path("pricing-whatif.md"))
    a = ap.parse_args(argv)
    moves = [float(x) for x in a.moves.split(",")]
    a.out.write_text(render(load(a.lines), moves, a.volume_change, a.business))
    print(a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a one-page monthly Owner's Scorecard from your own exports.

    python3 owner_scorecard.py DATA_DIR [--out-dir DIR]

DATA_DIR holds four plain CSV files you export or copy yourself:
  sales.csv     from your point-of-sale system
  bank.csv      from your bank, with a category column you fill in
  bookings.csv  from your booking system (optional if you take no bookings)
  settings.csv  a few numbers only you know (name,value,note)

It only reads those files and writes scorecard.md and scorecard.json into
the output folder. It makes no network calls and changes nothing else.
Every metric is labeled "actual" (built from your numbers) or "what-if"
(at least one input came from the shipped example values).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as M  # noqa: E402

NON_OPERATING = {"transfer", "owner_draw"}
FIXED = {"rent", "utilities", "software", "insurance", "loan_payment", "payroll", "marketing", "other_fixed"}
VARIABLE = {"cogs", "supplies", "tax", "other_variable"}


def read_csv(path: Path, required: list[str], optional=False):
    if not path.exists():
        if optional:
            return []
        raise SystemExit(f"E20 Missing file {path.name}. See fixes.md.")
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
        got = rows[0].keys() if rows else []
    missing = [c for c in required if rows and c not in got]
    if missing:
        raise SystemExit(f"E21 {path.name} is missing columns {missing}. See fixes.md.")
    return rows


def d(s: str) -> dt.date:
    try:
        return dt.date.fromisoformat(s.strip()[:10])
    except ValueError:
        raise SystemExit(f"E23 Could not read the date {s!r}. Use the form 2026-09-01. See fixes.md.")


def num(s, default=0.0):
    try:
        return float(str(s).replace("$", "").replace(",", ""))
    except ValueError:
        return default


def prior_month(start: dt.date):
    end = start - dt.timedelta(days=1)
    return end.replace(day=1), end


def in_range(row, a, b):
    return a <= d(row["date"]) <= b


def money_block(bank, a, b):
    rows = [r for r in bank if in_range(r, a, b)]
    money_in = sum(num(r["amount"]) for r in rows if num(r["amount"]) > 0 and r["category"] not in {"transfer"})
    op_out = -sum(num(r["amount"]) for r in rows if num(r["amount"]) < 0 and r["category"] not in NON_OPERATING)
    draws = -sum(num(r["amount"]) for r in rows if r["category"] == "owner_draw")
    by_cat = defaultdict(float)
    for r in rows:
        if num(r["amount"]) < 0:
            by_cat[r["category"]] += -num(r["amount"])
    return {"money_in": money_in, "money_out": op_out, "owner_draws": draws,
            "net_operating": money_in - op_out, "by_category": dict(by_cat),
            "uncategorized": sum(1 for r in rows if not r.get("category", "").strip())}


def build(data_dir: Path) -> dict:
    sales = read_csv(data_dir / "sales.csv", ["date", "item", "category", "net_sales"])
    bank = read_csv(data_dir / "bank.csv", ["date", "amount", "category"])
    book = read_csv(data_dir / "bookings.csv", ["date", "status", "client_id", "booked_minutes"], optional=True)
    settings = {r["name"]: (r.get("value") or "").strip() for r in read_csv(data_dir / "settings.csv", ["name", "value"])}
    start, end = d(settings["month_start"]), d(settings["month_end"])
    pstart, pend = prior_month(start)

    if not any(in_range(r, start, end) for r in sales) and not any(in_range(r, start, end) for r in bank):
        raise SystemExit("E24 No sales or bank rows fall inside the month in settings.csv. Check month_start and month_end. See fixes.md.")
    mb, pmb = money_block(bank, start, end), money_block(bank, pstart, pend)
    month_sales = [r for r in sales if in_range(r, start, end)]
    prior_sales = [r for r in sales if in_range(r, pstart, pend)]
    sales_total = sum(num(r["net_sales"]) for r in month_sales)
    prior_total = sum(num(r["net_sales"]) for r in prior_sales)
    n_sales = sum(max(num(r.get("quantity", 1), 1), 1) for r in month_sales)

    # Derive what the exports can tell us; the owner's settings win.
    cat = mb["by_category"]
    fixed_cost = sum(v for k, v in cat.items() if k in FIXED)
    variable_cost = sum(v for k, v in cat.items() if k in VARIABLE)
    derived = {}
    if n_sales:
        derived["price_per_sale"] = sales_total / n_sales
        derived["variable_cost_per_sale"] = variable_cost / n_sales
    if fixed_cost:
        derived["fixed_costs_monthly"] = fixed_cost
    merged = {**derived, **{k: v for k, v in settings.items() if v != ""}}
    used, borrowed = M.resolve(merged)

    cash = num(settings.get("cash_on_hand"), None)
    prev_cash = num(settings.get("prior_cash_on_hand"), None)
    out = {"business": settings.get("business_name", "Your business"), "period": f"{start:%m/%d/%Y} to {end:%m/%d/%Y}",
           "money": {**mb, "cash_on_hand": cash, "prior_cash_on_hand": prev_cash,
                     "prior_money_in": pmb["money_in"], "prior_money_out": pmb["money_out"]},
           "sales": {"total": sales_total, "prior_total": prior_total, "count": n_sales,
                     "deposit_gap": mb["money_in"] - sales_total}}

    # Money section: runway is a finding only when cash is real.
    burn = mb["money_out"] - mb["money_in"]
    if cash is not None:
        out["money"]["runway"] = {"months": M.runway(cash, burn)["months"], "basis": "actual"}
    else:
        out["money"]["runway"] = {"months": M.runway(15000.0, max(burn, 1))["months"], "basis": "what-if"}

    # What pays.
    by_item = defaultdict(float)
    for r in month_sales:
        by_item[r["item"]] += num(r["net_sales"])
    top = sorted(by_item.items(), key=lambda kv: -kv[1])[:5]
    cogs = cat.get("cogs", 0.0)
    out["what_pays"] = {
        "top_items": top,
        "gross_margin": {**M.margin(sales_total, cogs), "basis": "actual"},
        "labor_cost": {**M.labor_cost(cat.get("payroll", 0.0), sales_total), "basis": "actual"},
        "contribution": {**M.contribution_margin(used["price_per_sale"], used["variable_cost_per_sale"]),
                         "basis": M.basis_for(["price_per_sale", "variable_cost_per_sale"], borrowed)},
        "break_even": {**M.break_even(used["fixed_costs_monthly"], used["price_per_sale"], used["variable_cost_per_sale"]),
                       "basis": M.basis_for(["price_per_sale", "variable_cost_per_sale", "fixed_costs_monthly"], borrowed)},
    }

    # Customers and capacity from bookings.
    if book:
        month_b = [r for r in book if in_range(r, start, end)]
        done = [r for r in month_b if r["status"] == "completed"]
        before = {r["client_id"] for r in book if d(r["date"]) < start and r["status"] == "completed"}
        clients = {r["client_id"] for r in done if r["client_id"]}
        new = {c for c in clients if c not in before}
        mins = sum(num(r["booked_minutes"]) for r in done)
        lost = sum(num(r["booked_minutes"]) for r in month_b if r["status"] in ("no_show", "canceled"))
        cap = M.capacity_utilization(mins, used["capacity_minutes"])
        out["customers"] = {"clients_served": len(clients), "new": len(new), "returning": len(clients) - len(new),
                            "no_show_rate": M._div(sum(1 for r in month_b if r["status"] == "no_show"), len(month_b)),
                            "cancel_rate": M._div(sum(1 for r in month_b if r["status"] == "canceled"), len(month_b)),
                            "basis": "actual"}
        out["capacity"] = {"booked_minutes": mins, "lost_minutes": lost, **cap,
                           "revenue_per_booked_hour": M._div(sum(num(r["price"]) for r in done if r.get("price")), mins / 60) if mins else None,
                           "basis": M.basis_for(["capacity_minutes"], borrowed)}

    # What-if layer: always labeled.
    inputs_for = lambda names: M.basis_for(names, borrowed)
    ps = M.price_sensitivity(used["price_per_sale"], used["variable_cost_per_sale"], used["price_change_pct"])
    vr = M.volume_response(used["price_per_sale"], used["variable_cost_per_sale"], used["price_change_pct"],
                           used["assumed_volume_change"], used["baseline_units"])
    out["library"] = {
        "price_sensitivity": {**ps, "basis": inputs_for(["price_per_sale", "variable_cost_per_sale", "price_change_pct"])},
        "volume_response": {**vr, "basis": "what-if"},
        "cost_to_serve": {**M.cost_to_serve(used["overhead_pool"], used["allocation_base_total"], used["hours_used_by_line"],
                                            used["line_direct_cost"], used["line_revenue"]),
                          "basis": inputs_for(["overhead_pool", "allocation_base_total", "hours_used_by_line", "line_direct_cost", "line_revenue"])},
        "customer_lifetime_value": {**M.customer_lifetime_value(used["annual_margin_per_customer"], used["retention_rate"]),
                                    "basis": inputs_for(["annual_margin_per_customer", "retention_rate"])},
        "headcount_payback": {**M.headcount_payback(used["hire_monthly_cost"], used["hire_added_contribution"], used["hire_onboarding_cost"]),
                              "basis": inputs_for(["hire_monthly_cost", "hire_added_contribution", "hire_onboarding_cost"])},
        "working_capital": {**M.working_capital(used["current_assets"], used["current_liabilities"]),
                            "basis": inputs_for(["current_assets", "current_liabilities"])},
        "cash_conversion": {**M.cash_conversion_cycle(used["days_inventory"], used["days_receivable"], used["days_payable"]),
                            "basis": inputs_for(["days_inventory", "days_receivable", "days_payable"])},
    }
    out["flag"] = flag(out)
    out["verdict"] = verdict(out)
    out["data_notes"] = notes(mb, bank, sales, start, end)
    return out


def notes(mb, bank, sales, start, end):
    n = []
    if mb["uncategorized"]:
        n.append(f"{mb['uncategorized']} bank rows this month have no category, so they sit outside the cost lines.")
    if not any(in_range(r, start, end) for r in sales):
        n.append("No sales rows fall inside the month. Check the dates in settings.csv.")
    return n


def verdict(o):
    m = o["money"]
    net = m["net_operating"]
    word = "paid for itself" if net >= 0 else "ran short"
    return f"The month {word}, with {M.money(abs(net))} {'left over' if net >= 0 else 'missing'} after operating costs."


def flag(o):
    """One observation to look at. States what the numbers show and stops."""
    m = o["money"]
    if m["net_operating"] < 0:
        r = m["runway"]
        tail = f" At that pace the cash lasts about {r['months']:.1f} months." if r["months"] else ""
        return ("Cash", f"Operating costs ran {M.money(-m['net_operating'])} past money in.{tail}")
    c = o.get("customers")
    if c and (c["no_show_rate"] or 0) > 0.06:
        lost = o["capacity"]["lost_minutes"] / 60
        return ("No-shows and cancellations", f"{M.pct(c['no_show_rate'])} of bookings were no-shows and about {lost:.0f} booked hours were lost to no-shows and cancellations.")
    cap = o.get("capacity")
    if cap and cap["utilization"] is not None and cap["utilization"] < 0.6:
        return ("Open capacity", f"Booked time filled {M.pct(cap['utilization'])} of the available minutes.")
    gm = o["what_pays"]["gross_margin"]["ratio"]
    return ("Margin", f"Gross margin was {M.pct(gm)} of sales. Watch whether it holds next month.")


def tag(basis):
    return "" if basis == "actual" else " (what-if)"


def render_md(o) -> str:
    m, s, w = o["money"], o["sales"], o["what_pays"]
    ch = lambda a, b: "n/a" if not b else f"{(a - b) / b * 100:+.0f}%"
    L = [f"# {o['business']} Owner's Scorecard", f"Period {o['period']}", "", f"**Verdict.** {o['verdict']}", "",
         "## Money in and money out",
         "| Line | This month | Last month |", "|---|---|---|",
         f"| Money in | {M.money(m['money_in'])} | {M.money(m['prior_money_in'])} |",
         f"| Operating costs | {M.money(m['money_out'])} | {M.money(m['prior_money_out'])} |",
         f"| Owner draws | {M.money(m['owner_draws'])} | |",
         f"| Net operating | {M.money(m['net_operating'])} | |"]
    if m["cash_on_hand"] is not None:
        L.append(f"| Cash on hand | {M.money(m['cash_on_hand'])} | {M.money(m['prior_cash_on_hand'])} |")
    r = m["runway"]
    L += ["", f"Sales from the point-of-sale export were {M.money(s['total'])}, {ch(s['total'], s['prior_total'])} against last month. "
          f"Deposits minus sales was {M.money(s['deposit_gap'])}, which is normally card fees and timing.",
          f"Runway{tag(r['basis'])} " + ("is not a useful lens this month because the business funded itself." if r["months"] is None else f"is about {r['months']:.1f} months."),
          "", "## What actually pays", "| Line | Sales |", "|---|---|"]
    L += [f"| {k} | {M.money(v)} |" for k, v in w["top_items"]]
    gm, lc, cm, be = w["gross_margin"], w["labor_cost"], w["contribution"], w["break_even"]
    L += ["", f"Gross margin {M.pct(gm['ratio'])}. Payroll {M.pct(lc['ratio'])} of sales. "
          f"Each average sale keeps {M.money(cm['unit'])} after its own variable cost{tag(cm['basis'])}. "
          f"Break-even is about {M.money(be['revenue'])} of sales a month{tag(be['basis'])}."]
    if "customers" in o:
        c, cap = o["customers"], o["capacity"]
        L += ["", "## Customers and capacity",
              f"{c['clients_served']} clients were served, {c['new']} new and {c['returning']} returning. No-shows were {M.pct(c['no_show_rate'])} and cancellations {M.pct(c['cancel_rate'])} of bookings.",
              f"Booked time filled {M.pct(cap['utilization'])} of available minutes{tag(cap['basis'])}, and about {cap['lost_minutes']/60:.0f} booked hours were lost."]
    t, text = o["flag"]
    L += ["", f"## This month, look at {t.lower()}", text]
    wi = [k for k, v in o["library"].items() if v["basis"] != "actual"]
    if wi:
        L += ["", "## What-ifs", "These use example numbers because the matching inputs in settings.csv are blank. They show how the math works and are not findings about your business: "
              + ", ".join(k.replace("_", " ") for k in wi) + "."]
    for n in o["data_notes"]:
        L += ["", f"Data note. {n}"]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build a monthly Owner's Scorecard.")
    ap.add_argument("data_dir", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("scorecard-output"))
    a = ap.parse_args(argv)
    o = build(a.data_dir)
    try:
        a.out_dir.mkdir(parents=True, exist_ok=True)
        (a.out_dir / "scorecard.json").write_text(json.dumps(o, indent=2, default=str))
        (a.out_dir / "scorecard.md").write_text(render_md(o))
    except OSError as err:
        raise SystemExit(f"E25 Could not write to {a.out_dir}: {err.strerror}. See fixes.md.")
    print(a.out_dir / "scorecard.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

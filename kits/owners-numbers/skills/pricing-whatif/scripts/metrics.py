"""The finance metric library: small pure functions, standard library only.

Every function returns a dict that always carries a "basis" key.
"actual" means every input came from the owner's own numbers.
"what-if" means at least one input was filled in from the shipped example
values, so the result is a worked example and never a finding.
A ratio that would divide by zero comes back as None, because a blank is
more honest than a made-up zero.
"""
from __future__ import annotations

# Example inputs for a made-up business. Used only when the owner leaves a
# setting blank, and every result built from one is labeled "what-if".
EXAMPLE_INPUTS = {
    "price_per_sale": 60.0,
    "variable_cost_per_sale": 18.0,
    "fixed_costs_monthly": 7200.0,
    "overhead_pool": 3000.0,
    "allocation_base_total": 400.0,
    "hours_used_by_line": 120.0,
    "line_direct_cost": 1500.0,
    "line_revenue": 7200.0,
    "annual_margin_per_customer": 420.0,
    "retention_rate": 0.7,
    "hire_monthly_cost": 3600.0,
    "hire_added_contribution": 4800.0,
    "hire_onboarding_cost": 2400.0,
    "current_assets": 16000.0,
    "current_liabilities": 9000.0,
    "days_inventory": 30.0,
    "days_receivable": 10.0,
    "days_payable": 20.0,
    "price_change_pct": 0.05,
    "assumed_volume_change": -0.04,
    "baseline_units": 180.0,
    "capacity_minutes": 9600.0,
}


def resolve(settings: dict) -> tuple[dict, set]:
    """Return (used values, names that fell back to an example value)."""
    used, borrowed = {}, set()
    for name, example in EXAMPLE_INPUTS.items():
        raw = settings.get(name)
        if raw in (None, ""):
            used[name] = example
            borrowed.add(name)
        else:
            used[name] = float(raw)
    return used, borrowed


def basis_for(names, borrowed) -> str:
    return "what-if" if any(n in borrowed for n in names) else "actual"


def _div(a, b):
    return a / b if b else None


def contribution_margin(price, variable_cost):
    unit = price - variable_cost
    return {"unit": unit, "ratio": _div(unit, price)}


def break_even(fixed_costs, price, variable_cost):
    cm = contribution_margin(price, variable_cost)
    if cm["unit"] <= 0:
        return {"units": None, "revenue": None}
    return {"units": fixed_costs / cm["unit"], "revenue": fixed_costs / cm["ratio"]}


def price_sensitivity(price, variable_cost, pct):
    """Exact volume shift a price move can absorb (negative) or must win (positive)."""
    delta = price * pct
    new_unit = price - variable_cost + delta
    if pct == 0:
        shift = 0.0
    elif new_unit > 0:
        shift = -delta / new_unit
    else:
        shift = None
    return {"new_price": price + delta, "new_unit_contribution": new_unit, "breakeven_volume_shift": shift}


def volume_response(price, variable_cost, pct, volume_change, baseline_units=None):
    """Profit under a named volume assumption. Always a what-if."""
    unit = price - variable_cost
    new_unit = unit + price * pct
    mult = 1 + volume_change
    out = {
        "contribution_change_ratio": _div(new_unit * mult, unit) - 1 if unit else None,
        "better_off": new_unit * mult > unit,
        "contribution_change_amount": None,
    }
    if baseline_units is not None:
        out["contribution_change_amount"] = (new_unit * mult - unit) * baseline_units
    return out


def fixed_variable_split(costs):
    """costs is a list of (amount, kind) with kind 'fixed' or 'variable'."""
    fixed = sum(a for a, k in costs if k == "fixed")
    variable = sum(a for a, k in costs if k == "variable")
    total = sum(a for a, _ in costs)
    return {"fixed": fixed, "variable": variable, "total": total,
            "fixed_share": _div(fixed, total), "unmapped": total - fixed - variable}


def runway(cash, monthly_net_burn):
    return {"months": cash / monthly_net_burn if monthly_net_burn > 0 else None}


def cost_to_serve(overhead_pool, base_total, base_used, direct_cost, revenue):
    rate = _div(overhead_pool, base_total)
    if rate is None:
        return {"rate": None, "full_cost": None, "profit": None}
    full = direct_cost + rate * base_used
    return {"rate": rate, "full_cost": full, "profit": revenue - full}


def margin(revenue, cost):
    return {"amount": revenue - cost, "ratio": _div(revenue - cost, revenue)}


def markup_vs_margin(cost, price):
    profit = price - cost
    return {"markup": _div(profit, cost), "margin": _div(profit, price)}


def price_for_margin(cost, target_margin):
    return cost / (1 - target_margin) if 0 <= target_margin < 1 else None


def labor_cost(payroll, revenue):
    return {"ratio": _div(payroll, revenue)}


def headcount_payback(monthly_cost, monthly_added_contribution, onboarding_cost=0.0):
    net = monthly_added_contribution - monthly_cost
    return {"monthly_net": net, "covers_cost": net > 0,
            "months_to_payback": onboarding_cost / net if net > 0 else None}


def capacity_utilization(actual, ceiling):
    return {"utilization": _div(actual, ceiling), "slack": ceiling - actual}


def customer_lifetime_value(annual_margin, retention_rate):
    if retention_rate is None or not 0 <= retention_rate < 1:
        return {"lifetime_years": None, "clv": None}
    years = 1 / (1 - retention_rate)
    return {"lifetime_years": years, "clv": annual_margin * years}


def working_capital(current_assets, current_liabilities):
    return {"working_capital": current_assets - current_liabilities,
            "current_ratio": _div(current_assets, current_liabilities)}


def cash_conversion_cycle(days_inventory, days_receivable, days_payable):
    return {"days": days_inventory + days_receivable - days_payable}


def turnover_cost(annual_departures, onboarding_hours, loaded_hourly_wage):
    per = onboarding_hours * loaded_hourly_wage
    return {"cost_per_departure": per, "annual_cost": per * annual_departures}


def money(n):
    if n is None:
        return "n/a"
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,.0f}"


def pct(n, digits=0):
    return "n/a" if n is None else f"{n * 100:.{digits}f}%"

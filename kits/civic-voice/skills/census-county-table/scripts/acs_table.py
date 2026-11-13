#!/usr/bin/env python3
"""Build a county comparison table from the Census Bureau's American Community Survey (ACS).

Works in: Claude Code (full version), or any computer that has Python 3.9 or newer.
Uses only Python's standard library. Read-only: it asks the Census Bureau for public
numbers and writes two CSV files. It never changes anything online.

Your Census API key (a password-like code from the Census Bureau, see the kit's
shopping list) is read from the environment variable CENSUS_API_KEY. The
script never prints it and never writes it to a file.

Examples
  # See what would be requested, without contacting the Census Bureau:
  python3 acs_table.py --state "Example State" --counties "Alpha,Beta" --dry-run

  # Pull the table (needs CENSUS_API_KEY set in your terminal session):
  python3 acs_table.py --state 37 --counties "Alpha,Beta,Gamma" --include-state \\
      --year 2024 --out my-county-table

Outputs
  <out>-long.csv   one row per county and measure, with margin of error and flags
  <out>-table.csv  one row per measure, one column per county, ready to paste into a sheet
"""
import argparse
import csv
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.census.gov/data/{year}/acs/acs5"
MAX_VARS_PER_CALL = 20  # each one is fetched twice (estimate and margin), and the API allows up to 50 fields per request

# kind "single": one cell. "sum": add several cells. "prop": sum(num) / sum(den).
# "prop_adj": den = sum(den) - sum(den_sub), for tables with a "not computed" row.
# Variable IDs are table_number + "_" + row number; the API adds E (estimate) or M (margin).
DEFAULT_MEASURES = [
    {"measure": "total_population", "label": "Total population", "unit": "persons",
     "kind": "single", "num": ["B01003_001"]},
    {"measure": "median_household_income", "label": "Median household income (inflation-adjusted dollars)",
     "unit": "usd", "kind": "single", "num": ["B19013_001"]},
    {"measure": "poverty_rate", "label": "People below the poverty level, % of people whose poverty status is known",
     "unit": "pct", "kind": "prop", "num": ["B17001_002"], "den": ["B17001_001"]},
    {"measure": "median_gross_rent", "label": "Median gross rent, dollars per month",
     "unit": "usd", "kind": "single", "num": ["B25064_001"]},
    {"measure": "renter_occupied_share", "label": "Renter-occupied homes, % of occupied homes",
     "unit": "pct", "kind": "prop", "num": ["B25003_003"], "den": ["B25003_001"]},
    {"measure": "rent_burdened_30plus",
     "label": "Renters paying 30% or more of income on rent, % of renter households with a computed ratio",
     "unit": "pct", "kind": "prop_adj", "num": ["B25070_007", "B25070_008", "B25070_009", "B25070_010"],
     "den": ["B25070_001"], "den_sub": ["B25070_011"]},
    {"measure": "median_home_value", "label": "Median value of owner-occupied homes, dollars",
     "unit": "usd", "kind": "single", "num": ["B25077_001"]},
    {"measure": "vacancy_rate", "label": "Vacant homes, % of all housing units",
     "unit": "pct", "kind": "prop", "num": ["B25002_003"], "den": ["B25002_001"]},
    {"measure": "no_vehicle_households", "label": "Households with no vehicle, % of occupied homes",
     "unit": "pct", "kind": "prop", "num": ["B25044_003", "B25044_010"], "den": ["B25044_001"]},
    {"measure": "snap_households", "label": "Households receiving SNAP in the past 12 months, % of households",
     "unit": "pct", "kind": "prop", "num": ["B22010_002"], "den": ["B22010_001"]},
    {"measure": "age_65_plus", "label": "People age 65 and over, % of total population",
     "unit": "pct", "kind": "prop",
     "num": ["B01001_%03d" % n for n in (20, 21, 22, 23, 24, 25, 44, 45, 46, 47, 48, 49)],
     "den": ["B01001_001"]},
]

MISSING_BELOW = -222222222  # the Census Bureau uses codes such as -666666666 for "no estimate"


class CensusError(Exception):
    pass


def mask(text, key):
    """Remove the API key from any text before it can be shown."""
    if key:
        text = text.replace(key, "<your-key>")
    return re.sub(r"([?&]key=)[^&\s]+", r"\1<your-key>", text)


def api_get(url, key):
    """Fetch one API URL and return parsed JSON. Raises CensusError with a plain message."""
    req = urllib.request.Request(url, headers={"User-Agent": "civic-voice-acs-table/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", "replace")
            final = resp.geturl()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:200]
        raise CensusError(mask("The Census API said %s %s. %s (fix E17 if it names a variable)"
                               % (e.code, e.reason, detail), key))
    except urllib.error.URLError as e:
        raise CensusError(mask("Could not reach the Census API: %s" % e.reason, key))
    if "missing_key" in final or not body.lstrip().startswith("["):
        raise CensusError("The Census API did not return data. This usually means the key is "
                          "missing or not accepted (fix E16). Check that CENSUS_API_KEY is set.")
    return json.loads(body)


def build_url(year, params, key):
    q = urllib.parse.urlencode(params, safe=",:*")
    url = API.format(year=year) + "?" + q
    if key is not None:
        url += "&key=" + urllib.parse.quote(key, safe="")
    return url


def rows_to_dicts(table):
    header, rows = table[0], table[1:]
    return [dict(zip(header, r)) for r in rows]


def resolve_state(state_arg, year, key):
    if re.fullmatch(r"\d{2}", state_arg):
        return state_arg
    data = rows_to_dicts(api_get(build_url(year, {"get": "NAME", "for": "state:*"}, key), key))
    hits = [d for d in data if d["NAME"].lower() == state_arg.lower()]
    if not hits:
        raise CensusError("No state matched %r. Use the full state name or its two-digit FIPS code." % state_arg)
    return hits[0]["state"]


def num(x):
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    return None if f <= MISSING_BELOW else f


def variables_for(measures):
    seen, out = set(), []
    for m in measures:
        for field in ("num", "den", "den_sub"):
            for v in m.get(field, []):
                if v not in seen:
                    seen.add(v)
                    out.append(v)
    return out


def fetch_geo(year, key, state_fips, geo_kind, measures, county_fips=None):
    """Return {geo_id: {"NAME": str, "cells": {var: (est, moe)}}} for counties or the state."""
    names_vars = variables_for(measures)
    result = {}
    for i in range(0, len(names_vars), MAX_VARS_PER_CALL):
        chunk = names_vars[i:i + MAX_VARS_PER_CALL]
        get = ["NAME"] + [v + "E" for v in chunk] + [v + "M" for v in chunk]
        if geo_kind == "county":
            params = {"get": ",".join(get), "for": "county:*", "in": "state:" + state_fips}
        else:
            params = {"get": ",".join(get), "for": "state:" + state_fips}
        for d in rows_to_dicts(api_get(build_url(year, params, key), key)):
            gid = d["state"] + d.get("county", "")
            if geo_kind == "county" and county_fips is not None and d["county"] not in county_fips:
                continue
            entry = result.setdefault(gid, {"NAME": d["NAME"], "cells": {}})
            for v in chunk:
                entry["cells"][v] = (num(d[v + "E"]), num(d[v + "M"]))
    return result


def sum_est_moe(cells, vars_):
    e, m2 = 0.0, 0.0
    for v in vars_:
        est, moe = cells.get(v, (None, None))
        if est is None:
            return None, None
        e += est
        m2 += (moe or 0.0) ** 2
    return e, math.sqrt(m2)


def prop_moe(x, mx, y, my):
    """Margin of error for a share where x is part of y (ACS handbook formula)."""
    if not y:
        return None, None
    p = x / y
    rad = mx ** 2 - (p ** 2) * (my ** 2)
    if rad < 0:  # the handbook says to use the ratio formula when this goes negative
        rad = mx ** 2 + (p ** 2) * (my ** 2)
    return p, math.sqrt(rad) / y


def compute(m, cells):
    kind = m["kind"]
    if kind == "single":
        return cells.get(m["num"][0], (None, None))
    x, mx = sum_est_moe(cells, m["num"])
    if kind == "sum":
        return x, mx
    y, my = sum_est_moe(cells, m["den"])
    if kind == "prop_adj":
        s, ms = sum_est_moe(cells, m["den_sub"])
        if y is None or s is None:
            return None, None
        y, my = y - s, math.sqrt(my ** 2 + ms ** 2)
    if x is None or y is None:
        return None, None
    p, moe = prop_moe(x, mx, y, my)
    if p is None:
        return None, None
    return p * 100, moe * 100


def differs(a, b):
    """True if two estimates differ by more than their combined margins of error (90% level)."""
    (va, ma), (vb, mb) = a, b
    if None in (va, ma, vb, mb):
        return None
    return abs(va - vb) > math.sqrt(ma ** 2 + mb ** 2)


def fmt(v, unit):
    if v is None:
        return "n/a"
    if unit == "pct":
        return "%.1f%%" % v
    if unit == "usd":
        return "$%s" % format(round(v), ",")
    return format(round(v), ",")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", required=True, help="state name or two-digit FIPS code (for example 37)")
    ap.add_argument("--counties", required=True, help="comma-separated county names, with or without the word County")
    ap.add_argument("--include-state", action="store_true", help="add a row for the whole state, as a yardstick")
    ap.add_argument("--year", default="2024", help="last year of the 5-year period (default 2024, meaning 2020 to 2024)")
    ap.add_argument("--reference", default=None, help="name to compare the others against (default: the state if included, else the first county)")
    ap.add_argument("--moe-threshold", type=float, default=0.30,
                    help="flag a number when its margin of error is bigger than this share of the estimate (default 0.30)")
    ap.add_argument("--measures-file", default=None, help="JSON file with your own measures, same shape as DEFAULT_MEASURES")
    ap.add_argument("--out", default="county-table", help="output file prefix")
    ap.add_argument("--dry-run", action="store_true", help="print the requests (key hidden) and stop")
    a = ap.parse_args()

    measures = DEFAULT_MEASURES
    if a.measures_file:
        with open(a.measures_file) as f:
            measures = json.load(f)

    key = os.environ.get("CENSUS_API_KEY", "").strip()
    wanted = [re.sub(r"\s+county\s*$", "", c.strip(), flags=re.I).lower() for c in a.counties.split(",") if c.strip()]
    if not wanted:
        sys.exit("Give at least one county name.")

    if a.dry_run:
        state_part = a.state if re.fullmatch(r"\d{2}", a.state) else "<state number looked up from %r>" % a.state
        vs = variables_for(measures)
        print("Dry run. Nothing was sent. Counties wanted:", ", ".join(wanted))
        print("Variables needed: %d (each fetched as an estimate and a margin of error, in batches of %d)" % (len(vs), MAX_VARS_PER_CALL))
        for i in range(0, len(vs), MAX_VARS_PER_CALL):
            chunk = vs[i:i + MAX_VARS_PER_CALL]
            get = ["NAME"] + [v + "E" for v in chunk] + [v + "M" for v in chunk]
            print(mask(build_url(a.year, {"get": ",".join(get), "for": "county:*", "in": "state:" + state_part}, "KEYPLACEHOLDER"), "KEYPLACEHOLDER"))
        print("Key present in CENSUS_API_KEY:", "yes" if key else "no (needed for a real run)")
        return

    if not key:
        sys.exit("CENSUS_API_KEY is not set. Request a key at https://api.census.gov/data/key_signup.html "
                 "and set it in your terminal (see setup guide CV-FU-02). Fix E16.")
    try:
        state_fips = resolve_state(a.state, a.year, key)
        counties = fetch_geo(a.year, key, state_fips, "county", measures)
        chosen = {}
        for gid, ent in counties.items():
            base = re.sub(r",.*$", "", ent["NAME"])
            base = re.sub(r"\s+(county|parish|borough|census area|municipality)$", "", base, flags=re.I).lower()
            if base in wanted:
                chosen[gid] = ent
        missing = [w for w in wanted if w not in {re.sub(r"\s+(county|parish|borough|census area|municipality)$", "",
                                                         re.sub(r",.*$", "", e["NAME"]), flags=re.I).lower()
                                                  for e in chosen.values()}]
        if missing:
            raise CensusError("No county matched: %s. Check spelling against the Census Bureau's list." % ", ".join(missing))
        geos = dict(chosen)
        if a.include_state:
            geos.update(fetch_geo(a.year, key, state_fips, "state", measures))
    except CensusError as e:
        sys.exit(str(e))

    order = sorted(geos, key=lambda g: (g == state_fips, geos[g]["NAME"]))
    ref_id = None
    if a.reference:
        for g in geos:
            if a.reference.lower() in geos[g]["NAME"].lower():
                ref_id = g
                break
    if ref_id is None:
        ref_id = state_fips if a.include_state else order[0]

    vintage = "ACS %d-%s 5-year" % (int(a.year) - 4, a.year)
    long_rows, results = [], {}
    for m in measures:
        for g in order:
            val, moe = compute(m, geos[g]["cells"])
            results[(m["measure"], g)] = (val, moe)
    for m in measures:
        for g in order:
            val, moe = results[(m["measure"], g)]
            high = bool(val and moe is not None and moe > a.moe_threshold * abs(val))
            d = None if g == ref_id else differs(results[(m["measure"], g)], results[(m["measure"], ref_id)])
            long_rows.append({
                "geo": geos[g]["NAME"], "measure": m["measure"], "label": m["label"],
                "value": None if val is None else round(val, 2),
                "moe": None if moe is None else round(moe, 2), "unit": m["unit"],
                "moe_high": "yes" if high else "no",
                "differs_from_reference": "reference" if g == ref_id else {True: "yes", False: "no", None: "unclear"}[d],
                "vintage": vintage})

    cols = ["geo", "measure", "label", "value", "moe", "unit", "moe_high", "differs_from_reference", "vintage"]
    with open(a.out + "-long.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(long_rows)
    with open(a.out + "-table.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Measure"] + [geos[g]["NAME"] for g in order])
        for m in measures:
            row = [m["label"]]
            for g in order:
                val, moe = results[(m["measure"], g)]
                high = bool(val and moe is not None and moe > a.moe_threshold * abs(val))
                cell = "n/a" if val is None else "%s +/- %s" % (fmt(val, m["unit"]), fmt(moe, m["unit"]).replace("%", " pts") if m["unit"] == "pct" else fmt(moe, m["unit"]))
                row.append(cell + (" (large margin of error)" if high else ""))
            w.writerow(row)
        w.writerow([])
        w.writerow(["Source: U.S. Census Bureau, American Community Survey, " + vintage + " estimates. "
                    "Margins of error are at the 90 percent confidence level. Compared against: " + geos[ref_id]["NAME"] + "."])
    flagged = sum(1 for r in long_rows if r["moe_high"] == "yes")
    print("Wrote %s-long.csv and %s-table.csv (%d rows, %d flagged for a large margin of error)."
          % (a.out, a.out, len(long_rows), flagged))


if __name__ == "__main__":
    main()

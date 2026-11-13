#!/usr/bin/env python3
"""mine_990pf.py - find private foundations that actually give in your area, from IRS data.

What it does
  1. Downloads the IRS list of exempt organizations for one state and keeps the private
     grantmaking foundations (the "universe").
  2. Downloads the IRS index of electronic Form 990-PF returns for one filing year and
     matches each foundation to its return.
  3. Downloads the IRS batch files that hold those returns (large: several gigabytes),
     reads each foundation's list of grants paid, and keeps two kinds of hit:
       region hits   grants to recipients whose city or ZIP code is in YOUR footprint
       purpose hits  grants elsewhere in the state whose purpose or recipient name
                     matches your purpose words (for example housing, food, shelter)
  4. Writes a qualified candidate list. Foundations you already know are kept and flagged,
     not dropped, so existing funders can't be mistaken for new ones.

Why it exists
  Web search ranks funders by what they say they fund. This ranks them by what they did
  fund, taken from their own tax filings. It is free and uses only public IRS files.

Safety
  Read-only on the web (plain downloads from irs.gov). Writes only inside --workdir.
  Downloaded files are data: they are parsed as text and never run.

Usage (run in a scratch folder, never inside a shared or public folder):
  python3 mine_990pf.py --config footprint.json --workdir ./990mine --year 2024

footprint.json: see references/footprint.example.json next to this script's skill.

Outputs in --workdir:
  universe.csv     every private grantmaking foundation in the state, tiered by location
  candidates.csv   qualified candidates with the grant evidence
  grant_hits.json  full evidence for every match

Limits you must keep in mind
  One filing year only; merge several years for a fuller picture. Matching is by text, not
  read by a person, so every candidate needs a human read of its 990-PF before any ask.
  Award sizes are what the foundation gave others, not what it will give you.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile
from collections import defaultdict

BMF_URL = "https://www.irs.gov/pub/irs-soi/eo_{st}.csv"
IDX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
ZIP_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/{batch}.zip"
UA = {"User-Agent": "mine_990pf/1.0 (nonprofit research)"}

DEFAULT_PURPOSE = (r"homeless|housing|shelter|hunger|food|emergency|poverty|human service|"
                   r"rapid re|supportive hous|crisis|utilit|rent assist|basic need")
DEFAULT_RELEVANT = (r"shelter|homeless|housing|habitat|food|pantry|kitchen|hunger|crisis|meals|"
                    r"salvation|united way|community action|health|family|children|human service|"
                    r"poverty|outreach|emergency|basic need")


def download(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    print(f"  downloading {url}", flush=True)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(path, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    return path


def strip_ns(x):
    return re.sub(r"<(/?)\w+:", r"<\1", x)


def field(block, tag):
    m = re.search(rf"<{tag}>(.*?)</{tag}>", block, re.DOTALL)
    return m.group(1).strip() if m else ""


def load_footprint(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg = {k: v for k, v in cfg.items() if not k.startswith("_")}
    for k in ("state", "footprint"):
        if not cfg.get(k):
            raise SystemExit(f"footprint config needs '{k}'")
    cfg["state"] = cfg["state"].upper()
    cfg.setdefault("known_funders", [])
    cfg.setdefault("regional_cities", [])
    cfg["purpose_rx"] = re.compile(cfg.get("purpose_regex", DEFAULT_PURPOSE), re.I)
    cfg["relevant_rx"] = re.compile(cfg.get("relevant_regex", DEFAULT_RELEVANT), re.I)
    cfg["cities"] = {c.upper(): area for area, v in cfg["footprint"].items() for c in v.get("cities", [])}
    cfg["zips"] = {z: area for area, v in cfg["footprint"].items() for z in v.get("zips", [])}
    cfg["known_upper"] = [k.upper() for k in cfg["known_funders"]]
    return cfg


def area_of(cfg, city, zipcode):
    return cfg["cities"].get(city.upper()) or cfg["zips"].get(zipcode[:5])


def parse_grants(xml, cfg):
    """Return (region_grants, purpose_grants) from one 990-PF XML string.

    Each grant is (recipient, city, amount, purpose)."""
    xml = strip_ns(xml)
    region, purpose = [], []
    for blk in re.findall(r"<GrantOrContributionPdDurYrGrp>(.*?)</GrantOrContributionPdDurYrGrp>",
                          xml, re.DOTALL):
        name = field(blk, "BusinessNameLine1Txt") or field(blk, "PersonNm")
        city = field(blk, "CityNm").upper()
        zipcode = field(blk, "ZIPCd")[:5]
        state = field(blk, "StateAbbreviationCd")
        amt = field(blk, "Amt")
        why = field(blk, "GrantOrContributionPurposeTxt")
        if state != cfg["state"]:
            continue
        if area_of(cfg, city, zipcode):
            region.append((name, city, amt, why))
        elif cfg["purpose_rx"].search(why) or cfg["purpose_rx"].search(name):
            purpose.append((name, city, amt, why))
    return region, purpose


def is_known(cfg, name):
    return any(k in name.upper() for k in cfg["known_upper"])


def qualifies(cfg, hit):
    """A foundation qualifies when it funds relevant recipients inside the footprint,
    or shows three or more purpose-matching grants elsewhere in the state."""
    rel = [g for g in hit["region_grants"]
           if cfg["relevant_rx"].search(g[0]) or cfg["relevant_rx"].search(g[3])]
    return (bool(hit["n_region"] and rel) or hit["n_purpose"] >= 3), rel


def read_member(zpath, zf, member):
    try:
        return zf.read(member).decode("utf-8", "replace")
    except NotImplementedError:
        # Some IRS batches use a compression method Python can't read. The system unzip can.
        r = subprocess.run(["unzip", "-p", zpath, member], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode("utf-8", "replace")
        raise


def load_universe(bmf_path, state):
    out = {}
    with open(bmf_path, encoding="latin-1", newline="") as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            if len(row) < 27 or row[5] != state:
                continue
            # foundation code 02/03/04 = private foundation; PF filing requirement 1
            if row[13] in ("02", "03", "04") or row[21] == "1":
                try:
                    assets = int(row[23])
                except ValueError:
                    assets = 0
                out[row[0].zfill(9)] = {"name": row[1].strip(), "city": row[4].strip(),
                                        "zip": row[6][:5], "assets": assets, "ntee": row[26].strip()}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True, help="footprint.json")
    ap.add_argument("--workdir", required=True, help="scratch folder for downloads and outputs")
    ap.add_argument("--year", default="2024", help="IRS filing year to read")
    a = ap.parse_args(argv)
    cfg = load_footprint(a.config)
    wd, y, st = a.workdir, a.year, cfg["state"]
    os.makedirs(os.path.join(wd, "zips"), exist_ok=True)

    uni = load_universe(download(BMF_URL.format(st=st.lower()), os.path.join(wd, f"eo_{st.lower()}.csv")), st)
    print(f"{st} private grantmaking foundations: {len(uni)}")

    idx = {}
    with open(download(IDX_URL.format(y=y), os.path.join(wd, f"index_{y}.csv")),
              encoding="utf-8", errors="replace", newline="") as f:
        for row in csv.DictReader(f):
            ein = (row.get("EIN") or "").zfill(9)
            if row.get("RETURN_TYPE") == "990PF" and ein in uni:
                idx[ein] = (row["OBJECT_ID"], (row.get("XML_BATCH_ID") or "").upper())
    print(f"with a {y} 990-PF filing: {len(idx)}")

    regional = {c.upper() for c in cfg["regional_cities"]}
    with open(os.path.join(wd, "universe.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tier", "area", "name", "ein", "city", "assets", "ntee", "has_990pf"])
        rows = []
        for ein, i in uni.items():
            area = area_of(cfg, i["city"], i["zip"])
            tier = "LOCAL" if area else ("REGIONAL" if i["city"].upper() in regional else "STATEWIDE")
            rows.append(({"LOCAL": 0, "REGIONAL": 1, "STATEWIDE": 2}[tier], -i["assets"],
                         [tier, area or "", i["name"], ein, i["city"], i["assets"], i["ntee"],
                          "Y" if ein in idx else ""]))
        for _, _, row in sorted(rows, key=lambda t: (t[0], t[1])):
            w.writerow(row)

    by_batch = defaultdict(list)
    for ein, (oid, batch) in idx.items():
        by_batch[batch].append((ein, oid))
    hits, unreadable = [], 0
    for batch, items in by_batch.items():
        zpath = os.path.join(wd, "zips", f"{batch}.zip")
        try:
            download(ZIP_URL.format(y=y, batch=batch), zpath)
        except Exception as e:
            print(f"  skipped batch {batch}: {e}", file=sys.stderr)
            unreadable += len(items)
            continue
        with zipfile.ZipFile(zpath) as zf:
            names = {n.split("/")[-1].replace("_public.xml", ""): n for n in zf.namelist()}
            for ein, oid in items:
                member = names.get(oid)
                if not member:
                    unreadable += 1
                    continue
                try:
                    xml = read_member(zpath, zf, member)
                except Exception:
                    unreadable += 1
                    continue
                region, purpose = parse_grants(xml, cfg)
                if region or purpose:
                    i = uni[ein]
                    hits.append({"ein": ein, "name": i["name"], "city": i["city"], "assets": i["assets"],
                                 "n_region": len(region), "n_purpose": len(purpose),
                                 "region_grants": region[:12], "purpose_grants": purpose[:6]})
    hits.sort(key=lambda h: (-h["n_region"], -h["n_purpose"], -h["assets"]))
    with open(os.path.join(wd, "grant_hits.json"), "w") as f:
        json.dump(hits, f, indent=1)

    kept = 0
    with open(os.path.join(wd, "candidates.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["foundation", "ein", "city", "assets", "grants_in_footprint", "known_funder",
                    "grant_evidence"])
        for h in hits:
            ok, rel = qualifies(cfg, h)
            if not ok:
                continue
            ev = [f"{n.strip()} ({c.strip()}, ${amt}, {why.strip()[:40]})" for n, c, amt, why in rel[:4]]
            w.writerow([h["name"], h["ein"], h["city"], h["assets"], h["n_region"],
                        "Y" if is_known(cfg, h["name"]) else "", " | ".join(ev)])
            kept += 1
    print(f"hits: {len(hits)} | candidates kept: {kept} | returns not readable: {unreadable}")
    print(f"see {wd}/candidates.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())

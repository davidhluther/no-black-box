#!/usr/bin/env python3
"""Field benchmark: score competitor blog corpora with the same instrument
(content-discipline study, Arm 4).

Answers "are we cleaner than the category, or only cleaner than our own past" —
and produces the only numbers in this program that are publishable without
disclosing any brand's private metrics, because tell rates are normalized
per 1,000 words and carry no traffic data.

Read-only and polite: public pages only, sitemap-driven, one request at a
time with a delay, capped sample per site.

Per site you supply a name, a sitemap, a URL substring identifying posts, and
optionally a CSS selector. With no selector the engine falls back to its
generic containers — ALWAYS check the reported extraction stats before
trusting a site's numbers: a wrong container shows up as an implausibly low
median word count, and this script prints that per site so the failure is
visible rather than silent.

    benchmark_corpus.py --config sites.json --store DIR --out bench.csv
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tell_engine import load_canon, parse_html, score_page  # noqa: E402

UA = "Mozilla/5.0 (Macintosh) shared-skills-tell-scorer (public-page benchmark)"
KEY_FEATURES = ["composite_all_per1k", "composite_hard_per1k", "composite_mech_per1k",
                "t1_vocab_per1k", "transitions_per1k", "emdash_per1k",
                "colon_internal_per1k", "neg_parallel_per1k",
                "neg_parallel_sibling_per1k", "title_case_head_frac",
                "meta_commentary_per1k", "tier2_overuse_per1k"]


def sitemap_urls(session, sitemap: str, include: str, cap: int) -> list[str]:
    """Collect post URLs, following one level of sitemap index if present."""
    seen: list[str] = []
    try:
        r = session.get(sitemap, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"    sitemap unreachable: {e}")
        return []
    locs = re.findall(r"<loc>([^<]+)</loc>", r.text)
    children = [u for u in locs if u.endswith(".xml")]
    if children and not any(include in u for u in locs):
        for child in children[:12]:
            try:
                rc = session.get(child, timeout=30)
                locs += re.findall(r"<loc>([^<]+)</loc>", rc.text)
            except requests.RequestException:
                continue
            time.sleep(0.2)
    for u in locs:
        if include in u and not u.endswith(".xml") and u.rstrip("/") != "" and u not in seen:
            seen.append(u)
    return seen[:cap]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--store", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cap", type=int, default=60, help="max posts per site")
    ap.add_argument("--delay", type=float, default=0.4)
    args = ap.parse_args()

    sites = json.loads(Path(args.config).read_text())
    canon = load_canon()
    store = Path(args.store)
    session = requests.Session()
    session.headers["User-Agent"] = UA

    rows, summary = [], []
    for site in sites:
        name = site["name"]
        print(f"[{name}] {site['sitemap']}")
        sdir = store / name.lower().replace(" ", "-")
        sdir.mkdir(parents=True, exist_ok=True)
        urls = sitemap_urls(session, site["sitemap"], site["include"], args.cap)
        print(f"    {len(urls)} post URLs")
        scored = 0
        wcs = []
        for u in urls:
            slug = u.rstrip("/").rsplit("/", 1)[-1] or "index"
            dest = sdir / f"{slug}.html"
            if not (dest.exists() and dest.stat().st_size > 5000):
                try:
                    resp = session.get(u, timeout=30)
                    if resp.status_code != 200:
                        continue
                    dest.write_text(resp.text)
                except requests.RequestException:
                    continue
                time.sleep(args.delay)
            try:
                doc = parse_html(dest.read_text(), site.get("selector"))
            except Exception:
                continue
            if len(doc["blocks"]) < 3:
                continue
            f = score_page(doc["blocks"], canon)
            if f["word_count"] < 250:      # extraction likely failed
                continue
            rows.append({"site": name, "url": u, "slug": slug,
                         "date_published": doc.get("date") or "", **f})
            wcs.append(f["word_count"])
            scored += 1
        med = statistics.median(wcs) if wcs else 0
        flag = "  <-- CHECK SELECTOR (implausible word count)" if 0 < med < 400 else ""
        print(f"    scored {scored}, median words {med:.0f}{flag}")
        summary.append((name, scored, med))

    if not rows:
        print("nothing scored", file=sys.stderr)
        return 1
    import csv as _csv
    with open(args.out, "w", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {len(rows)} rows -> {args.out}")

    # comparison table
    by_site: dict[str, list[dict]] = {}
    for r in rows:
        by_site.setdefault(r["site"], []).append(r)
    print("\n| Site | n | " + " | ".join(f.replace("_per1k", "") for f in KEY_FEATURES) + " |")
    print("|---" * (len(KEY_FEATURES) + 2) + "|")
    for name, rs in sorted(by_site.items(),
                           key=lambda kv: statistics.median(
                               [x["composite_all_per1k"] for x in kv[1]])):
        meds = [statistics.median([x[f] for x in rs]) for f in KEY_FEATURES]
        print(f"| {name} | {len(rs)} | " + " | ".join(f"{m:.2f}" for m in meds) + " |")
    print("\nMedians per 1,000 body words. Lower = fewer house-canon tells.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

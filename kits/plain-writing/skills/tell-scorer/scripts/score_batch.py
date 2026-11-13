#!/usr/bin/env python3
"""Batch tell-scoring CLI — score a corpus (live pages or markdown drafts)
into one CSV row per document, with an optional gate mode.

Sources (pick one):
  --sitemap URL --include SUBSTR   fetch article URLs from a sitemap (politely)
  --urls-file FILE                 fetch a newline list of URLs
  --html-dir DIR                   pre-fetched .html files
  --md-glob 'output/final/*.md'    markdown drafts/finals

Common options:
  --selector CSS                   article container selector (verify on 2-3
                                   pages before trusting a new site)
  --canon PATH                     style_rules.json override (defaults to the
                                   data/style_rules.json)
  --out FILE.csv                   output (default: tell-scores.csv)
  --store DIR                      cache dir for fetched HTML (idempotent)

Gate mode (stream auditing / CI):
  --thresholds FILE.json           per-feature ceilings; any breach prints a
                                   failure line and exits 1. Default config:
                                   ../gate-thresholds.default.json
  --max-age-days N                 with --sitemap: only score pages whose
                                   JSON-LD datePublished is within N days
                                   (audit "what just shipped")

Examples:
  score_batch.py --sitemap https://site.com/sitemap.xml --include /blog/ \
      --selector 'div[class*="post-content"]' --out scores.csv
  score_batch.py --md-glob 'output/final/final_*.md' --thresholds gate.json
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tell_engine import load_canon, parse_html, parse_markdown, score_page  # noqa: E402

UA = "Mozilla/5.0 (Macintosh) shared-skills-tell-scorer (site-owner audit)"


def fetch_urls(urls: list[str], store: Path, delay: float = 0.25) -> list[tuple[str, Path]]:
    import requests
    store.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = UA
    out = []
    for n, url in enumerate(urls, 1):
        slug = url.rstrip("/").rsplit("/", 1)[-1] or f"page-{n}"
        dest = store / f"{slug}.html"
        if not (dest.exists() and dest.stat().st_size > 5_000):
            try:
                resp = session.get(url, timeout=30)
                if resp.status_code == 200:
                    dest.write_text(resp.text)
                else:
                    print(f"  skip {url} (HTTP {resp.status_code})", file=sys.stderr)
                    continue
            except requests.RequestException as e:
                print(f"  skip {url} ({e})", file=sys.stderr)
                continue
            time.sleep(delay)
        out.append((url, dest))
    return out


def sitemap_urls(sitemap: str, include: str) -> list[str]:
    import requests
    resp = requests.get(sitemap, timeout=30, headers={"User-Agent": UA})
    resp.raise_for_status()
    locs = re.findall(r"<loc>([^<]+)</loc>", resp.text)
    return sorted(u for u in locs if include in u and not u.endswith(include))


def main() -> int:
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sitemap")
    src.add_argument("--urls-file")
    src.add_argument("--html-dir")
    src.add_argument("--md-glob")
    ap.add_argument("--include", default="/blog/")
    ap.add_argument("--selector")
    ap.add_argument("--canon")
    ap.add_argument("--out", default="tell-scores.csv")
    ap.add_argument("--store", default=".tell-scorer-cache")
    ap.add_argument("--thresholds")
    ap.add_argument("--max-age-days", type=int)
    args = ap.parse_args()

    canon = load_canon(args.canon)
    docs: list[tuple[str, dict]] = []  # (identifier, parsed doc)

    if args.md_glob:
        for path in sorted(glob.glob(args.md_glob)):
            docs.append((path, parse_markdown(Path(path).read_text())))
    else:
        if args.html_dir:
            pairs = [(p.stem, p) for p in sorted(Path(args.html_dir).glob("*.html"))]
        else:
            urls = (sitemap_urls(args.sitemap, args.include) if args.sitemap
                    else [u.strip() for u in Path(args.urls_file).read_text().splitlines() if u.strip()])
            print(f"{len(urls)} URLs to score")
            pairs = fetch_urls(urls, Path(args.store))
        for ident, path in pairs:
            docs.append((str(ident), parse_html(path.read_text(), args.selector)))

    if args.max_age_days is not None:
        import datetime as dt
        floor = (dt.date.today() - dt.timedelta(days=args.max_age_days)).isoformat()
        docs = [(i, d) for i, d in docs if d.get("date") and d["date"] >= floor]
        print(f"{len(docs)} documents within {args.max_age_days} days")

    rows = []
    problems = []
    for ident, doc in docs:
        if len(doc["blocks"]) < 3:
            problems.append((ident, f"only {len(doc['blocks'])} blocks extracted"))
            continue
        row = {"id": ident, "title": doc.get("title") or "",
               "date_published": doc.get("date") or ""}
        row.update(score_page(doc["blocks"], canon))
        rows.append(row)

    if not rows:
        print("nothing scored", file=sys.stderr)
        return 1
    out = Path(args.out)
    # A headless run cannot `mkdir` first (one command per call), so the dated run
    # dir is made here.
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"scored {len(rows)} -> {out}")
    for ident, why in problems:
        print(f"  EXTRACTION PROBLEM {ident}: {why} — check --selector", file=sys.stderr)

    if args.thresholds:
        tpath = Path(args.thresholds)
        if not tpath.exists():
            tpath = Path(__file__).resolve().parent.parent / "gate-thresholds.default.json"
        conf = json.loads(tpath.read_text())
        # Formatting-density features warn and never fail the gate (styleguide
        # evidence rule, 2026-10-01): the 192-page premise test found no measured
        # citation benefit to language tells and a POSITIVE association for the
        # formatting-weighted composite, so a gate must not push a project into
        # stripping bold, colons or dashes out of a page that already has them.
        warn_only = set(conf.get("_warn_only", []))
        limits = {k: v for k, v in conf.items() if not k.startswith("_")}
        failures, warnings = [], []
        for row in rows:
            for feat, ceiling in limits.items():
                val = row.get(feat)
                if val is not None and float(val) > float(ceiling):
                    bucket = warnings if feat in warn_only else failures
                    bucket.append((row["id"], feat, val, ceiling))
        if warnings:
            print(f"\nGATE WARN (formatting, non-blocking): {len(warnings)} over ceiling "
                  f"on {len({w[0] for w in warnings})} documents")
            for ident, feat, val, ceiling in warnings:
                print(f"  WARN {ident}: {feat} = {val} (ceiling {ceiling})")
            print("  Do NOT remove headings, lists, tables or bold to clear these.")
        if failures:
            print(f"\nGATE: {len(failures)} breaches on {len({f[0] for f in failures})} documents")
            for ident, feat, val, ceiling in failures:
                print(f"  FAIL {ident}: {feat} = {val} (ceiling {ceiling})")
            return 1
        print("\nGATE: clean" + (" (warnings above)" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

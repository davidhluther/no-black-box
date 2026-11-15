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
  --store DIR                      folder that keeps fetched HTML, one file per
                                   full URL; live runs fetch fresh unless
                                   --reuse-cache is given

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
import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tell_engine import load_canon, parse_html, parse_markdown, score_page  # noqa: E402

UA = "Mozilla/5.0 (Macintosh) shared-skills-tell-scorer (site-owner audit)"


def fetch_urls(urls: list[str], store: Path, delay: float = 0.25, reuse: bool = False) -> list[tuple[str, Path]]:
    import requests
    store.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = UA
    out = []
    for n, url in enumerate(urls, 1):
        # Keyed by the full URL, so /blog/a and /news/a never share a file.
        slug = url.rstrip("/").rsplit("/", 1)[-1] or f"page-{n}"
        dest = store / f"{slug[:60]}-{hashlib.sha256(url.encode()).hexdigest()[:16]}.html"
        if not (reuse and dest.exists() and dest.stat().st_size > 5_000):
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
    ap.add_argument("--reuse-cache", action="store_true",
                    help="score pages already in --store instead of fetching them again")
    ap.add_argument("--thresholds")
    ap.add_argument("--max-age-days", type=int)
    args = ap.parse_args()

    # Load the gate config before any fetching, so a bad path fails fast. A
    # missing file is an error: silently gating on the defaults would pass a
    # draft against ceilings nobody chose. The one exception is the bundled
    # default's own name, which the docs pass from the skill folder.
    conf = None
    if args.thresholds:
        tpath = Path(args.thresholds)
        if not tpath.is_file():
            bundled = Path(__file__).resolve().parent.parent / "gate-thresholds.default.json"
            if args.thresholds == bundled.name and bundled.is_file():  # only the bare documented name
                tpath = bundled
            else:
                print(f"thresholds file not found: {args.thresholds}", file=sys.stderr)
                return 2
        try:
            conf = json.loads(tpath.read_text())
        except json.JSONDecodeError as e:
            print(f"thresholds file {tpath} is not valid JSON: {e}", file=sys.stderr)
            return 2
        if not isinstance(conf, dict):
            print(f"thresholds file {tpath} must hold a JSON object", file=sys.stderr)
            return 2

    canon = load_canon(args.canon)
    docs: list[tuple[str, dict]] = []  # (identifier, parsed doc)
    missed = 0  # requested pages that could not be fetched

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
            pairs = fetch_urls(urls, Path(args.store), reuse=args.reuse_cache)
            missed = len(urls) - len(pairs)
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
    # Every requested page must be scored; a partial run is not a clean run.
    incomplete = bool(problems or missed)
    if incomplete:
        print(f"INCOMPLETE: {len(problems)} page(s) not extracted, {missed} not fetched", file=sys.stderr)

    if conf is not None:
        # Formatting-density features warn and never fail the gate (styleguide
        # evidence rule, 2026-10-01): the 192-page premise test found no measured
        # citation benefit to language tells and a POSITIVE association for the
        # formatting-weighted composite, so a gate must not push a project into
        # stripping bold, colons or dashes out of a page that already has them.
        warn_only = set(conf.get("_warn_only", []))
        limits = {k: v for k, v in conf.items() if not k.startswith("_")}
        # Every configured feature must be a real score field; a typo would
        # otherwise switch that ceiling off without a word.
        known = set(rows[0].keys()) - {"id", "title", "date_published"}
        unknown = sorted((set(limits) | warn_only) - known)
        if unknown:
            print(f"\nGATE CONFIG ERROR: unknown feature name(s) in thresholds: "
                  f"{', '.join(unknown)}", file=sys.stderr)
            print(f"  known features: {', '.join(sorted(known))}", file=sys.stderr)
            return 2
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
    return 1 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main())

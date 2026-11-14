#!/usr/bin/env python3
"""Technical SEO audit engine.

Runs deterministic checks against a crawl export and produces a prioritized,
scored findings report. The judgment calls (which checks matter more for this
site, what "business impact" means for this business) belong to the person
running it. This script is the mechanical layer: same crawl in, same findings
out, every time.

Input is the "Internal: All" CSV export from Screaming Frog's SEO Spider
(its free version crawls up to 500 addresses). Stdlib only.

Mobile crawl comparison, structured-data validation, and language-tag checks
are not implemented. They need exports this script doesn't read. The report
says so plainly, so "not checked" is never mistaken for "passed".

Usage:
    python3 analyse_crawl.py internal_all.csv
    python3 analyse_crawl.py internal_all.csv --json
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from urllib.parse import urlparse

NOT_IMPLEMENTED = [
    "Mobile readiness (needs a separate mobile-UA crawl export)",
    "Structured data validation (needs the 'Structured Data:All' export tab)",
    "International SEO / hreflang (needs hreflang data, not in Internal:All)",
]

# category -> (default SEO impact 0-10, default business impact 0-10, default fix effort 0-10)
# Business impact and fix effort are defaults, not facts -- override them
# once you know the actual site/client context. Said explicitly in SKILL.md.
DEFAULT_SCORES = {
    "crawlability": (9, 7, 3),
    "indexability": (8, 7, 4),
    "on_page": (5, 5, 2),
    "architecture": (6, 5, 5),
    "performance": (6, 6, 6),
    "security": (7, 6, 3),
    "ai_readiness": (6, 7, 4),
}

TEXT_CONTENT_TYPE_PREFIX = "text/html"


def priority_score(seo_impact, business_impact, fix_effort):
    """(SEO Impact x 0.4) + (Business Impact x 0.4) + ((10 - Fix Effort) x 0.2)"""
    return round(seo_impact * 0.4 + business_impact * 0.4 + (10 - fix_effort) * 0.2, 2)


def severity_for(score):
    if score >= 8:
        return "Critical"
    if score >= 6.5:
        return "High"
    if score >= 5:
        return "Medium"
    if score >= 3:
        return "Low"
    return "Informational"


def load_internal_csv(path):
    # utf-8-sig, not utf-8: real Screaming Frog exports open with a BOM.
    # Read as plain utf-8, the BOM glues itself onto the first header cell
    # ("Address" becomes "﻿Address"), so every row["Address"] lookup
    # raises KeyError -- caught against a real export, not the synthetic
    # fixture, which (written via Python's own csv module) had no BOM and
    # silently masked this. utf-8-sig strips a BOM if present, no-ops if not.
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def is_html_row(row):
    ct = (row.get("Content Type") or "").lower()
    return ct.startswith(TEXT_CONTENT_TYPE_PREFIX)


def to_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finding(category, url, message, extra_score=None):
    seo, biz, effort = DEFAULT_SCORES[category]
    if extra_score:
        seo, biz, effort = extra_score
    score = priority_score(seo, biz, effort)
    return {
        "category": category,
        "url": url,
        "message": message,
        "seo_impact": seo,
        "business_impact": biz,
        "fix_effort": effort,
        "priority_score": score,
        "severity": severity_for(score),
    }


def check_crawlability(rows):
    findings = []
    for row in rows:
        url = row.get("Address", "")
        status = row.get("Status Code", "")
        redirect_url = row.get("Redirect URL", "")
        if status and status not in ("200", "301", "302", "304"):
            findings.append(finding("crawlability", url, f"Status {status} (not 2xx/3xx)"))
        elif status in ("301", "302") and redirect_url:
            findings.append(finding(
                "crawlability", url,
                f"Redirects ({status}) to {redirect_url} -- internal links should point at the final URL directly",
            ))
    return findings


def check_indexability(rows):
    findings = []
    for row in rows:
        if not is_html_row(row):
            continue
        url = row.get("Address", "")
        indexability = row.get("Indexability", "")
        status_note = row.get("Indexability Status", "")
        if indexability and indexability != "Indexable":
            msg = f"Not indexable ({indexability}"
            msg += f": {status_note})" if status_note else ")"
            findings.append(finding("indexability", url, msg))
    return findings


def check_on_page(rows):
    findings = []
    for row in rows:
        if not is_html_row(row):
            continue
        url = row.get("Address", "")
        if row.get("Indexability") and row.get("Indexability") != "Indexable":
            continue  # already flagged, don't double-count
        status = row.get("Status Code", "")
        if status and status not in ("200", "304"):
            continue  # a redirect/error row has no real content to evaluate;
            # already flagged by check_crawlability, and "missing title" on a
            # 301 is noise, not a finding

        title = row.get("Title 1", "")
        title_len = to_int(row.get("Title 1 Length"))
        if not title:
            findings.append(finding("on_page", url, "Missing title tag"))
        elif title_len > 60:
            findings.append(finding("on_page", url, f"Title too long ({title_len} chars, recommend <=60)"))
        elif title_len < 15:
            findings.append(finding("on_page", url, f"Title very short ({title_len} chars)"))

        desc = row.get("Meta Description 1", "")
        desc_len = to_int(row.get("Meta Description 1 Length"))
        if not desc:
            findings.append(finding("on_page", url, "Missing meta description"))
        elif desc_len > 160:
            findings.append(finding("on_page", url, f"Meta description too long ({desc_len} chars, recommend <=160)"))

        h1 = row.get("H1-1", "")
        if not h1:
            findings.append(finding("on_page", url, "Missing H1"))

        word_count = to_int(row.get("Word Count"))
        if word_count and word_count < 150:
            findings.append(finding("on_page", url, f"Thin content ({word_count} words)"))
    return findings


def check_architecture(rows):
    findings = []
    for row in rows:
        if not is_html_row(row):
            continue
        url = row.get("Address", "")
        depth = to_int(row.get("Crawl Depth"))
        inlinks = to_int(row.get("Unique Inlinks", row.get("Inlinks")))
        if depth >= 4:
            findings.append(finding("architecture", url, f"Crawl depth {depth} (buried {depth} clicks from the homepage)"))
        if inlinks == 0 and depth > 0:
            findings.append(finding("architecture", url, "Orphan page: zero internal inlinks found during the crawl"))
    return findings


def check_performance(rows):
    findings = []
    for row in rows:
        if not is_html_row(row):
            continue
        url = row.get("Address", "")
        perf_score = row.get("Performance Score", "")
        lcp = row.get("Largest Contentful Paint Time (ms)", "")
        cls = row.get("Cumulative Layout Shift", "")
        if perf_score not in ("", None):
            perf_val = to_int(perf_score, default=-1)
            if 0 <= perf_val < 50:
                findings.append(finding("performance", url, f"Low Lighthouse performance score ({perf_val}/100)"))
        if lcp not in ("", None):
            lcp_val = to_int(lcp, default=-1)
            if lcp_val > 4000:
                findings.append(finding("performance", url, f"LCP {lcp_val}ms exceeds 4000ms (poor)"))
        if cls not in ("", None):
            try:
                cls_val = float(cls)
                if cls_val > 0.25:
                    findings.append(finding("performance", url, f"CLS {cls_val} exceeds 0.25 (poor)"))
            except ValueError:
                pass
    return findings


def check_security(rows):
    findings = []
    for row in rows:
        url = row.get("Address", "")
        if url and not url.startswith("https://"):
            findings.append(finding("security", url, "Not served over HTTPS"))
    return findings


def check_ai_readiness(rows, base_url):
    """Live checks against the site's own robots.txt / llms.txt -- not derived
    from the crawl export, since Screaming Frog's Internal:All doesn't carry
    these root-level files unless explicitly crawled as URLs."""
    import urllib.request

    findings = []
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"

    ai_bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]

    try:
        req = urllib.request.Request(f"{root}/robots.txt", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            robots_text = resp.read().decode("utf-8", errors="replace")
        missing = [bot for bot in ai_bots if bot.lower() not in robots_text.lower()]
        if missing:
            findings.append(finding(
                "ai_readiness", f"{root}/robots.txt",
                f"No explicit allow rule found for: {', '.join(missing)} (relies on wildcard default, if any)",
            ))
    except Exception as e:
        findings.append(finding("ai_readiness", f"{root}/robots.txt", f"Could not fetch robots.txt: {e}"))

    try:
        req = urllib.request.Request(f"{root}/llms.txt", headers={"User-Agent": "Mozilla/5.0"})
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        findings.append(finding("ai_readiness", f"{root}/llms.txt", "No llms.txt found at domain root"))

    return findings


def run(csv_path):
    rows = load_internal_csv(csv_path)
    html_rows = [r for r in rows if is_html_row(r)]
    base_url = html_rows[0]["Address"] if html_rows else (rows[0]["Address"] if rows else "")

    all_findings = []
    all_findings += check_crawlability(rows)
    all_findings += check_indexability(rows)
    all_findings += check_on_page(rows)
    all_findings += check_architecture(rows)
    all_findings += check_performance(rows)
    all_findings += check_security(rows)
    if base_url:
        all_findings += check_ai_readiness(rows, base_url)

    all_findings.sort(key=lambda f: -f["priority_score"])

    by_category = defaultdict(list)
    for f in all_findings:
        by_category[f["category"]].append(f)

    category_health = {}
    for cat in DEFAULT_SCORES:
        cat_findings = by_category.get(cat, [])
        penalty = sum(15 if f["severity"] == "Critical" else 8 if f["severity"] == "High" else 3 for f in cat_findings)
        category_health[cat] = max(0, 100 - penalty)

    overall_health = round(sum(category_health.values()) / len(category_health)) if category_health else None

    return {
        "pages_crawled": len(rows),
        "html_pages": len(html_rows),
        "overall_health_score": overall_health,
        "category_health": category_health,
        "findings_count": len(all_findings),
        "findings": all_findings,
        "not_implemented": NOT_IMPLEMENTED,
    }


def print_human(report):
    print(f"\n=== Technical SEO Audit ===")
    print(f"Pages crawled: {report['pages_crawled']} ({report['html_pages']} HTML)")
    print(f"Overall health score: {report['overall_health_score']}/100\n")

    print("Category health:")
    for cat, score in sorted(report["category_health"].items(), key=lambda kv: kv[1]):
        print(f"  {cat:<15} {score}/100")

    print(f"\n{report['findings_count']} findings, highest priority first:\n")
    for f in report["findings"][:40]:
        print(f"  [{f['severity']:<13}] ({f['priority_score']:>4}) {f['category']:<13} {f['url']}")
        print(f"      {f['message']}")
    if report["findings_count"] > 40:
        print(f"\n  ... and {report['findings_count'] - 40} more (use --json for the full list)")

    print("\nNot implemented in this version (not silently skipped -- said plainly):")
    for item in report["not_implemented"]:
        print(f"  - {item}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", help="Path to Screaming Frog 'Internal:All' export CSV")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a human-readable report")
    args = parser.parse_args()

    report = run(args.csv)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)

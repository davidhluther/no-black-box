#!/usr/bin/env python3
"""Common Crawl visibility checker.

Answers a question llms.txt/robots.txt audits don't cover: is this domain
actually reachable by Common Crawl's CCBot? Many AI systems' pretraining
pipelines derive from Common Crawl rather than crawling a site directly, so
CCBot access is a distinct question from "does GPTBot reach us" -- and a
CDN's managed bot rules can silently block CCBot even when robots.txt looks
fully permissive.

Stdlib only. Real public APIs:
  - index.commoncrawl.org (collinfo.json + per-crawl CDX index) for capture
    history and archived robots.txt lookups.
  - data.commoncrawl.org (WARC segment range-fetch) to read the actual
    archived robots.txt bytes for a given month, not just infer from counts.
  - A live HTTP probe with the real CCBot UA string vs. a normal browser UA,
    to catch edge-layer (WAF/CDN) blocks invisible to static robots.txt
    inspection.

Usage:
    python check_visibility.py example.com
    python check_visibility.py example.com --months 12 --json
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

INDEX_SERVER = "https://index.commoncrawl.org"
DATA_SERVER = "https://data.commoncrawl.org"
CCBOT_UA = "CCBot/2.0 (+https://commoncrawl.org/faq/)"
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
AI_BOT_TOKENS = [
    "GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User",
    "anthropic-ai", "PerplexityBot", "Perplexity-User", "CCBot",
    "Google-Extended",
]
# Heuristic signatures for CDN/plugin-managed robots.txt. Best-effort pattern
# matching, not a guarantee -- these strings are what's been observed in the
# wild, not a documented contract from any vendor.
CDN_SIGNATURES = {
    "Cloudflare": [r"cloudflare", r"# This is a robots\.txt file managed by"],
    "Yoast (WordPress)": [r"# START YOAST BLOCK", r"yoast"],
    "Squarespace": [r"squarespace"],
    "Shopify": [r"shopify"],
    "Wix": [r"wix\.com"],
}


def http_get(url, timeout=15, headers=None, retries=3):
    """GET with retry-with-backoff. Common Crawl's public index server is
    known to return transient 5xx under load; a single failed request there
    is not evidence of anything about the target domain."""
    import time
    last_exc = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=headers or {"User-Agent": BROWSER_UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
                last_exc = e
                continue
            raise
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
                last_exc = e
                continue
            raise
    raise last_exc


def recent_crawl_ids(n):
    """Return the n most recent Common Crawl monthly index ids, newest first."""
    status, body = http_get(f"{INDEX_SERVER}/collinfo.json")
    collections = json.loads(body)
    # collinfo.json is already newest-first in practice, but sort defensively
    # on the id (CC-MAIN-YYYY-WW sorts lexicographically in date order).
    ids = [c["id"] for c in collections if c["id"].startswith("CC-MAIN-")]
    ids.sort(reverse=True)
    return ids[:n]


def query_index(crawl_id, url_pattern, limit=None):
    """Query one monthly CDX index for a URL pattern. Returns list of records."""
    q = f"{INDEX_SERVER}/{crawl_id}-index?url={urllib.request.quote(url_pattern, safe='')}&output=json"
    if limit:
        q += f"&limit={limit}"
    try:
        status, body = http_get(q, timeout=20)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        raise
    records = []
    for line in body.decode("utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def fetch_warc_record(record):
    """Range-fetch and decompress a single WARC record given its CDX metadata."""
    import gzip
    filename = record["filename"]
    offset = int(record["offset"])
    length = int(record["length"])
    end = offset + length - 1
    req = urllib.request.Request(
        f"{DATA_SERVER}/{filename}",
        headers={"User-Agent": BROWSER_UA, "Range": f"bytes={offset}-{end}"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read()
    decompressed = gzip.decompress(raw)
    # WARC record: headers, blank line, HTTP response headers, blank line, body.
    parts = decompressed.split(b"\r\n\r\n", 2)
    return parts[2].decode("utf-8", errors="replace") if len(parts) >= 3 else ""


def check_capture_trend(domain, months):
    """Panel 1: capture counts per recent monthly crawl."""
    crawl_ids = recent_crawl_ids(months)
    trend = []
    for cid in crawl_ids:
        records = query_index(cid, f"{domain}/*", limit=1)
        # CDX index API supports a count-only style via limit+showNumPages,
        # but the plain query already tells us presence/absence reliably;
        # for a real count we page the 'numPages'/'pageSize' fields if present.
        count_url = (
            f"{INDEX_SERVER}/{cid}-index?url={urllib.request.quote(domain + '/*', safe='')}"
            f"&output=json&showNumPages=true"
        )
        try:
            _, body = http_get(count_url, timeout=20)
            meta = json.loads(body)
            pages = meta.get("pages", 0)
            page_size = meta.get("pageSize", 5)
            estimated = pages * page_size
        except Exception:
            estimated = len(records)
        trend.append({"crawl": cid, "captured": bool(records), "estimated_pages": estimated})
    return trend


def check_robots_history(domain, months):
    """Panel 2: archived robots.txt per month, checking for AI-bot disallow rules."""
    crawl_ids = recent_crawl_ids(months)
    history = []
    first_block = None
    for cid in crawl_ids:
        records = query_index(cid, f"https://{domain}/robots.txt")
        if not records:
            records = query_index(cid, f"http://{domain}/robots.txt")
        if not records:
            history.append({"crawl": cid, "found": False})
            continue
        record = records[-1]  # most recent capture within that monthly crawl
        try:
            body_text = fetch_warc_record(record)
        except Exception as e:
            history.append({"crawl": cid, "found": True, "error": str(e)})
            continue
        blocked = blocked_bots_in_robots(body_text)
        entry = {"crawl": cid, "found": True, "blocked_bots": blocked}
        history.append(entry)
        if blocked and first_block is None:
            first_block = cid
    return history, first_block


def blocked_bots_in_robots(robots_text):
    """Parse robots.txt text for AI-bot user-agent blocks (Disallow: /)."""
    blocked = []
    current_agents = []
    for raw_line in robots_text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            current_agents = []
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        if key == "user-agent":
            current_agents.append(value)
        elif key == "disallow" and value in ("/", ""):
            if value == "/":
                for agent in current_agents:
                    for token in AI_BOT_TOKENS:
                        if token.lower() == agent.lower() and token not in blocked:
                            blocked.append(token)
    return blocked


def detect_cdn_signature(robots_text):
    """Panel 3: heuristic pattern match against known CDN/plugin robots.txt signatures."""
    hits = []
    for vendor, patterns in CDN_SIGNATURES.items():
        for pattern in patterns:
            if re.search(pattern, robots_text, re.IGNORECASE):
                hits.append(vendor)
                break
    return hits


def live_probe(domain):
    """Panel 4: live request as CCBot vs. a normal browser, to catch edge/WAF blocks."""
    results = {}
    for label, ua in (("ccbot", CCBOT_UA), ("browser", BROWSER_UA)):
        for scheme in ("https", "http"):
            url = f"{scheme}://{domain}/robots.txt"
            try:
                status, body = http_get(url, timeout=10, headers={"User-Agent": ua})
                results[label] = {"status": status, "url": url, "bytes": len(body)}
                break
            except urllib.error.HTTPError as e:
                results[label] = {"status": e.code, "url": url}
                break
            except Exception as e:
                results[label] = {"error": str(e), "url": url}
    ccbot_status = results.get("ccbot", {}).get("status")
    browser_status = results.get("browser", {}).get("status")
    edge_block_suspected = (
        ccbot_status is not None
        and browser_status is not None
        and ccbot_status != browser_status
        and ccbot_status in (403, 406, 429, 503)
    )
    results["edge_block_suspected"] = edge_block_suspected
    return results


def run(domain, months=12):
    domain = domain.replace("https://", "").replace("http://", "").strip("/")
    report = {
        "domain": domain,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "capture_trend": None,
        "robots_history": None,
        "first_ai_block_seen": None,
        "cdn_signatures_current": None,
        "live_probe": None,
    }
    print(f"Checking {domain} against Common Crawl ({months} most recent monthly indexes)...", file=sys.stderr)

    report["capture_trend"] = check_capture_trend(domain, months)

    history, first_block = check_robots_history(domain, months)
    report["robots_history"] = history
    report["first_ai_block_seen"] = first_block

    # Current live robots.txt for the CDN-signature heuristic panel.
    try:
        _, live_robots = http_get(f"https://{domain}/robots.txt", headers={"User-Agent": BROWSER_UA})
        report["cdn_signatures_current"] = detect_cdn_signature(live_robots.decode("utf-8", errors="replace"))
    except Exception:
        report["cdn_signatures_current"] = []

    report["live_probe"] = live_probe(domain)

    return report


def print_human(report):
    print(f"\n=== Common Crawl visibility: {report['domain']} ===\n")

    print("Capture trend (most recent -> oldest):")
    for row in report["capture_trend"]:
        flag = "OK" if row["captured"] else "MISSING"
        print(f"  {row['crawl']:<16} {flag:<8} ~{row['estimated_pages']} pages")

    print("\nRobots.txt history (AI-bot blocks by month):")
    for row in report["robots_history"]:
        if not row.get("found"):
            print(f"  {row['crawl']:<16} no robots.txt captured that month")
            continue
        blocked = row.get("blocked_bots") or []
        if blocked:
            print(f"  {row['crawl']:<16} BLOCKS: {', '.join(blocked)}")
        else:
            print(f"  {row['crawl']:<16} clear")

    if report["first_ai_block_seen"]:
        print(f"\n  First AI-bot block detected in: {report['first_ai_block_seen']}")
    else:
        print("\n  No AI-bot blocks found in the checked window.")

    sigs = report["cdn_signatures_current"]
    print(f"\nCDN/plugin signatures in current robots.txt: {', '.join(sigs) if sigs else 'none detected'}")

    probe = report["live_probe"]
    print("\nLive probe (CCBot UA vs. browser UA):")
    for label in ("ccbot", "browser"):
        info = probe.get(label, {})
        print(f"  {label:<8} status={info.get('status', info.get('error'))} url={info.get('url')}")
    if probe.get("edge_block_suspected"):
        print("  WARNING: CCBot got a different status than a browser did -- possible edge/WAF block")
        print("  invisible to static robots.txt inspection. Check CDN bot-management rules.")
    else:
        print("  No status mismatch between CCBot and browser UA at the edge.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("domain", help="Domain to check, e.g. example.com")
    parser.add_argument("--months", type=int, default=12, help="How many recent monthly crawls to check (default 12)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a human-readable report")
    args = parser.parse_args()

    result = run(args.domain, args.months)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)

#!/usr/bin/env python3
"""Fetch recent items from the RSS/Atom feeds listed in config.json.

Read-only: it only downloads public feed files. It prints a markdown bundle and a
status line per source (ok, empty, or failed) so a dead feed is never mistaken for a
quiet week.

Usage:
    python3 tools/fetch_feeds.py --config config.json [--days 7] [--out bundle.md]

Config shape (see config.example.json):
    {"industry_intel": {"feeds": [{"name": "...", "url": "https://..."}]}}

Standard library only. Needs no keys. Exit code 0 even when some feeds fail, so a
scheduled run still writes its bundle; failed sources are listed at the top.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ATOM = "{http://www.w3.org/2005/Atom}"
USER_AGENT = "no-black-box-idea-kit/0.1 (feed reader; read-only)"


def parse_date(text: str | None):
    if not text:
        return None
    text = text.strip()
    try:
        dt = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def clean(text: str | None, limit: int = 400) -> str:
    text = " ".join((text or "").split())
    return text[:limit]


def parse_feed(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items: list[dict] = []
    if root.tag.endswith("rss") or root.find("channel") is not None:
        for item in root.iter("item"):
            items.append({
                "title": clean(item.findtext("title")),
                "link": clean(item.findtext("link"), 500),
                "date": parse_date(item.findtext("pubDate")),
                "summary": clean(item.findtext("description")),
            })
    else:
        for entry in root.iter(f"{ATOM}entry"):
            link = ""
            for el in entry.findall(f"{ATOM}link"):
                if el.get("rel", "alternate") == "alternate":
                    link = el.get("href", "")
                    break
            items.append({
                "title": clean(entry.findtext(f"{ATOM}title")),
                "link": link,
                "date": parse_date(entry.findtext(f"{ATOM}updated") or entry.findtext(f"{ATOM}published")),
                "summary": clean(entry.findtext(f"{ATOM}summary")),
            })
    return items


def fetch(url: str) -> bytes:
    if not url.startswith(("https://", "http://")):
        raise ValueError("feed address must start with https:// or http://")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read(5_000_000)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--days", type=int, default=None)
    ap.add_argument("--out")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"Config not found: {cfg_path}. Copy config.example.json to config.json first.", file=sys.stderr)
        return 2
    cfg = json.loads(cfg_path.read_text()).get("industry_intel", {})
    feeds = cfg.get("feeds", [])
    days = args.days if args.days is not None else int(cfg.get("window_days", 7))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    statuses: list[str] = []
    sections: list[str] = []
    for feed in feeds:
        name, url = feed.get("name", "unnamed"), feed.get("url", "")
        try:
            items = parse_feed(fetch(url))
        except Exception as exc:  # report, never hide
            statuses.append(f"- FAILED  {name} ({type(exc).__name__}: {exc})")
            continue
        recent = [i for i in items if i["date"] is None or i["date"] >= cutoff]
        statuses.append(f"- {'ok     ' if recent else 'empty  '}{name} ({len(recent)} item(s) in {days} days)")
        if recent:
            lines = [f"## {name}"]
            for i in recent:
                when = i["date"].strftime("%m/%d/%Y") if i["date"] else "undated"
                lines.append(f"- {i['title']} ({when})\n  {i['link']}\n  {i['summary']}")
            sections.append("\n".join(lines))

    bundle = [f"# Feed bundle, last {days} days", "", "## Intake health", *statuses, ""] + [s_ + "\n" for s_ in sections]
    text = "\n".join(bundle) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text)
        print(f"Wrote {args.out}")
        print("\n".join(statuses))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""sweep.py - weekly discovery sweep for an organization's grants pipeline.

Discover and score. Read-only: it queries public sources and writes candidates; it never
contacts a funder. Everything org-specific (keywords, agency lists, news feeds, scoring
words, names to exclude) comes from the config's "sweep" section.

Sources (each is one function returning candidate dicts):
  grants_gov  Grants.gov search2 API, nonprofit-eligible, forecasted or posted
  local_news  local newspaper search feeds (BLOX RSS): local grant and gift stories, kept as
              leads naming who gives in the area (a person reads them)

Outputs (paths.sweep_dir):
  candidates.csv  every candidate ever seen; first_seen/last_seen, score, tier, status
  runs.jsonl      append-only: an "attempting" row before work, then one outcome row per
                  source (scheduled-job-failures rule: record before work, never overwrite)

Usage:
  python3 engine/sweep.py --config orgs/<slug>.json            # run all sources
  python3 engine/sweep.py --config orgs/<slug>.json --dry-run  # print, write nothing
"""
import csv
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gp_common as gp  # noqa: E402

FIELDS = ["key", "source", "funder", "title", "url", "close_date", "award", "score", "tier",
          "why", "status", "first_seen", "last_seen"]

DEFAULTS = {
    "keywords": {},
    "good_agencies": [], "bad_agencies": [],
    "positive": [], "negative": [], "strong": [], "off": [],
    "user_agent": "grants pipeline sweep",
    "grants_gov": {"eligibilities": "12", "opp_statuses": "forecasted|posted", "rows": 50},
    "news": {"feeds": [], "terms": [], "local_paths": [], "skip_paths": ["/ap/", "/national/"],
             "hit_regex": "grant|award|donat|gift|fund|sponsor|raises|giving", "max_age_days": 400,
             "query": "?f=rss&t=article&l=50&s=start_time&sd=desc&q="},
    "scoring": {"base": 20, "good_agency": 25, "bad_agency": -30, "title_pos": 8, "title_pos_cap": 4,
                "title_neg": 12, "syn_strong": 7, "syn_strong_cap": 5, "syn_off": 10,
                "big_floor": 1000000, "big_floor_penalty": 15, "multi_stage": 5,
                "tier2_min": 70, "tier3_min": 45, "news_score": 50, "score_synopsis_min": 30},
}


def settings(cfg):
    """Config 'sweep' section merged over DEFAULTS (one level deep for dicts)."""
    s = cfg.get("sweep", {})
    out = {}
    for k, v in DEFAULTS.items():
        out[k] = {**v, **s.get(k, {})} if isinstance(v, dict) else s.get(k, v)
    out["exclude_names"] = cfg.get("exclude_names", [])
    out["out"] = cfg["paths"]["sweep_dir"]
    return out


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def log(sw, row, dry):
    row = {"at": now(), **row}
    if dry:
        print("log:", row)
        return
    sw["out"].mkdir(parents=True, exist_ok=True)
    with (sw["out"] / "runs.jsonl").open("a") as f:
        f.write(json.dumps(row) + "\n")


def post(sw, url, body):
    headers = {"User-Agent": sw["user_agent"], "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def grants_gov(sw):
    seen = {}
    gg = sw["grants_gov"]
    for stage, terms in sw["keywords"].items():
        for term in terms:
            d = post(sw, "https://api.grants.gov/v1/api/search2",
                     {"keyword": term, "oppStatuses": gg["opp_statuses"],
                      "eligibilities": gg["eligibilities"], "rows": gg["rows"]})
            if d.get("errorcode"):
                raise RuntimeError(f"grants.gov error {d.get('errorcode')}: {d.get('msg')}")
            for h in d["data"].get("oppHits", []):
                c = seen.setdefault(h["number"], {
                    "key": "grantsgov:" + h["number"], "source": "grants.gov",
                    "funder": h.get("agency") or h.get("agencyCode", ""), "agency": h.get("agencyCode", ""),
                    "title": h["title"], "close_date": h.get("closeDate", ""),
                    "url": f"https://www.grants.gov/search-results-detail/{h['id']}",
                    "award": "", "stages": set()})
                c["stages"].add(stage)
    return [c for c in seen.values() if not gp.contains_excluded(c["title"] + " " + c["funder"],
                                                                  sw["exclude_names"])]


def enrich(sw, c, cache):
    """Pull the synopsis once per opportunity; cached so a weekly rerun stays cheap."""
    oid = c["url"].rsplit("/", 1)[-1]
    if oid not in cache:
        d = post(sw, "https://api.grants.gov/v1/api/fetchOpportunity", {"opportunityId": int(oid)})["data"]
        syn = d.get("synopsis") or d.get("forecast") or {}
        cache[oid] = {"desc": re.sub(r"<[^>]+>", " ", syn.get("synopsisDesc") or syn.get("forecastDesc") or "")[:6000],
                      "ceiling": syn.get("awardCeiling") or "", "floor": syn.get("awardFloor") or "",
                      "cost_sharing": syn.get("costSharing"), "agency": syn.get("agencyCode") or c["agency"]}
    e = cache[oid]
    c["desc"] = e["desc"]
    c["award"] = "-".join(x for x in (e["floor"], e["ceiling"]) if x and x != "0")
    c["floor"] = int(float(e["floor"] or 0)) if str(e["floor"]).replace(".", "").isdigit() else 0
    c["cost_sharing"] = e["cost_sharing"]


def parse_feed(text, nw, today=None):
    """Parse one RSS search result into candidate dicts, applying the local-section, age and skip filters."""
    today = today or dt.date.today()
    hit = re.compile(nw["hit_regex"], re.I)
    out = {}
    for title, link, date in re.findall(
            r"<item>.*?<title>(.*?)</title>.*?<link>(.*?)</link>.*?<pubDate>(.*?)</pubDate>",
            text, re.S):
        title = re.sub(r"<!\[CDATA\[|\]\]>", "", title).strip()
        if nw["local_paths"] and not any(x in link for x in nw["local_paths"]):
            continue
        if any(x in link for x in nw["skip_paths"]):
            continue
        if not hit.search(title) or gp.contains_excluded(title, nw["_exclude"]):
            continue
        d = dt.datetime.strptime(date.strip()[:16], "%a, %d %b %Y").date()
        if (today - d).days > nw["max_age_days"]:
            continue
        key = "news:" + link.split("?")[0]
        out[key] = {"key": key, "source": "local news", "funder": "(read story)",
                    "agency": "", "title": title, "url": link.split("?")[0],
                    "close_date": d.isoformat(), "award": "", "stages": set(), "news": True}
    return out


def local_news(sw):
    """Read-only. One query per term per paper, newest first; local sections only."""
    nw = {**sw["news"], "_exclude": sw["exclude_names"]}
    out = {}
    for base in nw["feeds"]:
        for term in nw["terms"]:
            url = base + nw["query"] + urllib.parse.quote(term)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8", "replace")
            out.update(parse_feed(text, nw))
    return list(out.values())


def score(sw, c):
    sc = sw["scoring"]
    if c.get("news"):
        return sc["news_score"], "lead", "local giving story; read it and log the funder"
    t = c["title"].lower()
    s, why = sc["base"], []
    if c.get("agency", "").startswith(tuple(sw["good_agencies"])):
        s += sc["good_agency"]
        why.append("housing/community agency")
    if c.get("agency", "").startswith(tuple(sw["bad_agencies"])):
        s += sc["bad_agency"]
        why.append("research agency")
    pos = [w for w in sw["positive"] if w in t]
    neg = [w for w in sw["negative"] if w in t]
    s += sc["title_pos"] * min(len(pos), sc["title_pos_cap"]) - sc["title_neg"] * len(neg)
    if pos:
        why.append("title: " + ", ".join(pos[:4]))
    if neg:
        why.append("off-fit: " + ", ".join(neg))
    d = c.get("desc", "").lower()
    strong = [w for w in sw["strong"] if w in d]
    off = [w for w in sw["off"] if w in d]
    s += sc["syn_strong"] * min(len(strong), sc["syn_strong_cap"]) - sc["syn_off"] * len(off)
    if strong:
        why.append("synopsis: " + ", ".join(strong[:5]))
    if off:
        why.append("synopsis off-fit: " + ", ".join(off))
    if c.get("floor", 0) >= sc["big_floor"]:
        s -= sc["big_floor_penalty"]
        why.append("floor $%s: partner path" % f"{c['floor']:,}")
    if c.get("cost_sharing"):
        why.append("cost share")
    if len(c.get("stages", ())) > 1:
        s += sc["multi_stage"]
        why.append("matched " + "+".join(sorted(c["stages"])))
    s = max(0, min(100, s))
    tier = "2" if s >= sc["tier2_min"] else "3" if s >= sc["tier3_min"] else "skip"
    return s, tier, "; ".join(why)


def load(sw):
    path = sw["out"] / "candidates.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        # Undo csv_safe's apostrophe so it never stacks across weekly runs.
        return {r["key"]: {k: v[1:] if v[:1] == "'" and gp.csv_safe(v[1:]) == v else v for k, v in r.items()}
                for r in csv.DictReader(f)}


def run(cfg, dry=False):
    sw = settings(cfg)
    today = dt.date.today().isoformat()
    log(sw, {"event": "attempting", "slot": today}, dry)
    rows, failed = load(sw), []
    cache_path = sw["out"] / "grantsgov-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    new = 0
    for name, fn in [("grants_gov", grants_gov), ("local_news", local_news)]:
        try:
            found = fn(sw)
        except Exception as e:  # one source failing must not hide the others
            failed.append(name)
            log(sw, {"event": "failed", "slot": today, "source": name, "reason": repr(e)[:500]}, dry)
            continue
        for c in found:
            if c["source"] == "grants.gov" and score(sw, c)[0] >= sw["scoring"]["score_synopsis_min"]:
                try:
                    enrich(sw, c, cache)
                except Exception as e:
                    log(sw, {"event": "warn", "slot": today, "source": name, "key": c["key"],
                             "reason": repr(e)[:300]}, dry)
            s, tier, why = score(sw, c)
            r = rows.get(c["key"])
            if r is None:
                new += 1
                r = {"key": c["key"], "first_seen": today, "status": "new"}
                rows[c["key"]] = r
            r.update({"source": c["source"], "funder": c["funder"], "title": c["title"],
                      "url": c["url"], "close_date": c["close_date"], "award": c["award"],
                      "score": s, "tier": tier, "why": why, "last_seen": today})
        log(sw, {"event": "ok", "slot": today, "source": name, "found": len(found)}, dry)
    if not dry:
        cache_path.write_text(json.dumps(cache))
    ordered = sorted(rows.values(), key=lambda r: -int(r["score"]))
    if dry:
        for r in ordered[:25]:
            print(r["score"], r["tier"], r["funder"][:30], "|", r["title"][:80])
    else:
        with (sw["out"] / "candidates.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows({k: gp.csv_safe(v) for k, v in r.items()} for r in ordered)
    log(sw, {"event": "done" if not failed else "partial", "slot": today, "new": new,
             "total": len(rows), "failed_sources": failed}, dry)
    print(f"{new} new, {len(rows)} total, failed: {failed or 'none'}")
    return 1 if failed else 0


def main(argv=None):
    args = gp.parse_args(argv, extra=lambda ap: ap.add_argument("--dry-run", action="store_true"),
                         desc=__doc__)
    return run(gp.load_config(args.config), args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

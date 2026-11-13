#!/usr/bin/env python3
"""Cheap pre-brief screen for a candidate topic slate.

WHY THIS EXISTS. A large batch of planned topics was briefed in one go at a larger
organization, and a noticeable share came back HOLD (already covered, or no measurable
demand) after each had already used a research cycle and paid keyword-tool credits.
The per-topic brief gate caught them all, which is the problem: that gate is the
expensive one. This is the cheap pass that goes before it.

WHAT IT CAN AND CANNOT DO, tested rather than assumed. Two of the three checks are
deterministic and produce verdicts. The third cannot, and pretending otherwise was the
first version's mistake:

  DEMAND FLOOR (verdict). Volume below a configured floor with no written rationale.
  Factual threshold, no ambiguity. Topics were being planned at 10 and 50
  searches a month using figures printed in the plan's own table.

  IN-WAVE DEDUPE (verdict). Two candidates in the same slate targeting one keyword.
  Screens compare candidates to EXISTING content and forget to compare them to EACH
  OTHER; that is how two topics in one plan ended up chasing the same term.

  NEAREST EXISTING CONTENT (evidence, NOT a verdict). Stemmed containment against the
  live sitemap, the queue, and staged briefs. This surfaces the closest matches so a
  reviewer can look; it does not decide. In testing against a plan whose outcomes
  were known, title-word similarity scored real duplicates and legitimate new topics
  almost the same, so any threshold that caught most duplicates also flagged most
  of the list, which is not a filter. Whether a candidate duplicates a page depends
  on what that page COVERS, and no title-token method can see that.
  So the evidence is printed and the judgment stays with the reviewer.

  Stemming still matters and is kept: `prepaid business credit cards` scored 0.50
  against the already-live /prepaid-business-card purely on `cards` vs `card`, so the
  page never even appeared in the evidence list.

Usage:
    topic_screen.py --candidates FILE [--config FILE] [--json]

Candidates: JSON list or CSV with `title`, `keyword`, optionally `volume`,
`rationale`, `id`. Everything specific to your organization lives in the config
(the "topic_screen" block of config.json), never here. `--config` accepts either
the whole config.json or a file holding just the topic_screen block.

Exit 0 always — advisory. The caller decides.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.request
from pathlib import Path

# Words that carry no disambiguating signal in a topic phrase. Deliberately small:
# an aggressive stoplist erases the very tokens that separate near-duplicate topics.
STOP = {"a", "an", "the", "for", "of", "to", "in", "on", "and", "or", "vs", "your",
        "with", "how", "what", "is", "are", "guide", "explained", "complete"}

DEFAULTS = {
    # Volume below this is a REVIEW unless the candidate carries a written rationale.
    "demand_floor": 100,
    # Containment score at/above which a candidate is flagged against existing content.
    # 0.8 was tuned against the 14 known HOLDs: it catches them without burying the
    # caller in hub/spoke noise. Lower it and every spoke flags against its pillar.
    "existing_threshold": 0.8,
    # In-wave dedupe is stricter — two candidates this close really are one topic.
    "dedupe_threshold": 0.8,
    "sitemap_url": None,
    "sitemap_file": None,
    "path_filter": "/blog/",
    "briefs_dir": None,
    "board_dump": None,
    # Board stages that constitute prior claim on a topic. Ideas deliberately absent:
    # an idea does not block.
    "blocking_stages": ["Planned", "In production", "Review", "Ready to publish", "Live"],
}


def stem(word: str) -> str:
    """Crude plural fold. Deliberately not a real stemmer.

    The failure this fixes is `cards` vs `card`. A full stemmer (Porter et al.)
    would also fold `payments`->`payment` and `automation`->`autom`, and that last
    kind of over-folding creates false matches between genuinely different topics.
    Trailing-s only, minimum length 4, is the smallest change that fixes the
    observed defect without inventing new ones. `ss` is left alone (`business`).
    """
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokens(text: str) -> set[str]:
    return {stem(w) for w in re.findall(r"[a-z0-9]+", (text or "").lower())
            if w not in STOP and len(w) > 2}


def containment(a: str, b: str) -> float:
    """Overlap scored against the SHORTER side.

    One-sided scoring (`|A & B| / |A|`) is what let the duplicates through: a long
    candidate title dilutes a perfect match below any useful threshold. Containment
    asks "is the smaller phrase essentially contained in the larger one", which is
    the actual question when comparing a topic to a slug.
    """
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def load_config(path: str | None) -> dict:
    cfg = dict(DEFAULTS)
    if path:
        data = json.loads(Path(path).read_text())
        cfg.update(data.get("topic_screen", data))
    return cfg


def load_candidates(path: str) -> list[dict]:
    p = Path(path)
    raw = p.read_text()
    if p.suffix.lower() == ".csv":
        rows = list(csv.DictReader(raw.splitlines()))
    else:
        rows = json.loads(raw)
        if isinstance(rows, dict):                     # {group: [topic, ...]}
            rows = [t for v in rows.values() for t in v]
    out = []
    for r in rows:
        vol = r.get("volume", r.get("vol", ""))
        vol = str(vol).replace(",", "").strip()
        out.append({
            "title": (r.get("title") or "").strip(),
            "keyword": (r.get("keyword") or "").strip(),
            "volume": int(vol) if vol.isdigit() else None,
            "rationale": (r.get("rationale") or "").strip(),
            "id": r.get("id") or r.get("n") or r.get("slug") or "",
        })
    return out


def load_existing(cfg: dict) -> tuple[list[str], list[dict], list[str], list[str]]:
    """Return (live slugs, board items, staged brief slugs). Never fail silently.

    A source that cannot be reached is reported to the caller as INCOMPLETE rather
    than counted as clean — the same fail-soft-never-fail-silent contract the
    per-topic gate uses.
    """
    incomplete = []

    slugs: list[str] = []
    sm = None
    if cfg.get("sitemap_file"):
        try:
            sm = Path(cfg["sitemap_file"]).read_text()
        except OSError:
            incomplete.append("sitemap_file")
    elif cfg.get("sitemap_url"):
        try:
            with urllib.request.urlopen(cfg["sitemap_url"], timeout=30) as fh:
                sm = fh.read().decode("utf-8", "replace")
        except Exception:
            incomplete.append("sitemap_url")
    else:
        incomplete.append("sitemap (not configured)")
    if sm:
        pf = cfg.get("path_filter") or ""
        for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
            if pf and pf not in loc:
                continue
            slugs.append(loc.rstrip("/").split("/")[-1])

    board: list[dict] = []
    if cfg.get("board_dump"):
        try:
            bp = Path(cfg["board_dump"]).expanduser()
            if bp.suffix.lower() == ".csv":
                # A Google Sheet exported as CSV: Queue tab columns title, keyword, stage.
                board = [{"name": r.get("title", ""), "kw": r.get("keyword", ""),
                          "stage": r.get("stage", "")}
                         for r in csv.DictReader(bp.read_text().splitlines())]
            else:
                board = json.loads(bp.read_text())
        except Exception:
            incomplete.append("board_dump")
    else:
        incomplete.append("board (not configured)")

    briefs: list[str] = []
    if cfg.get("briefs_dir"):
        d = Path(cfg["briefs_dir"]).expanduser()
        if d.is_dir():
            briefs = [p.stem.split("_", 1)[-1] for p in d.glob("*_*.md")]
        else:
            incomplete.append("briefs_dir")
    else:
        incomplete.append("briefs (not configured)")

    return slugs, board, briefs, incomplete


def screen(candidates: list[dict], cfg: dict) -> dict:
    slugs, board, briefs, incomplete = load_existing(cfg)
    et = cfg["existing_threshold"]
    dt = cfg["dedupe_threshold"]
    floor = cfg["demand_floor"]
    blocking = set(cfg["blocking_stages"])

    # Normalize up front: screen() is a library entry point as well as the CLI's,
    # and a caller passing plain dicts should not have to know the loader's schema.
    candidates = [{"id": c.get("id", ""), "title": c.get("title", ""),
                   "keyword": c.get("keyword", ""), "volume": c.get("volume"),
                   "rationale": c.get("rationale", "")} for c in candidates]

    results = []
    for i, c in enumerate(candidates):
        probe = c["keyword"] or c["title"]
        findings = []

        # F1 — existing content, scored on the keyword with stemming + containment.
        for s in slugs:
            score = containment(probe, s.replace("-", " "))
            if score >= et:
                findings.append({"filter": "existing-live", "match": f"/{s}",
                                 "score": round(score, 2)})
        for item in board:
            stage = item.get("stage", "")
            if stage not in blocking:
                continue
            score = max(containment(probe, item.get("name", "")),
                        containment(probe, item.get("kw", "")))
            if score >= et:
                findings.append({"filter": "existing-board",
                                 "match": f"{stage}: {item.get('name','')[:60]}",
                                 "score": round(score, 2)})
        for b in briefs:
            score = containment(probe, b.replace("-", " "))
            if score >= et:
                findings.append({"filter": "existing-brief", "match": b,
                                 "score": round(score, 2)})

        # F2 — demand floor. A written rationale is what buys an exception, because
        # deliberate AI-visibility bets on zero-volume terms are legitimate and
        # should have to say so out loud.
        if c["volume"] is not None and c["volume"] < floor:
            if c["rationale"]:
                findings.append({"filter": "below-floor-allowed",
                                 "match": f"volume {c['volume']} < {floor}; rationale given",
                                 "score": 1.0})
            else:
                findings.append({"filter": "below-floor",
                                 "match": f"volume {c['volume']} < {floor}, no rationale",
                                 "score": 1.0})
        elif c["volume"] is None:
            findings.append({"filter": "no-volume",
                             "match": "no volume figure — pull live data before briefing",
                             "score": 1.0})

        # F3 — candidates against each other.
        for j, other in enumerate(candidates):
            if i == j:
                continue
            score = containment(probe, other["keyword"] or other["title"])
            if score >= dt:
                findings.append({"filter": "in-wave-duplicate",
                                 "match": f"{other['id'] or other['title'][:40]}",
                                 "score": round(score, 2)})

        # Only the deterministic checks form a verdict. Existing-content matches are
        # evidence for a human, because token similarity provably does not separate
        # "duplicate" from "legitimate spoke" (see module docstring).
        DECIDING = ("below-floor", "in-wave-duplicate")
        blocking_hits = [f for f in findings if f["filter"] in DECIDING]
        results.append({
            "id": c["id"], "title": c["title"], "keyword": c["keyword"],
            "volume": c["volume"],
            "verdict": "REVIEW" if blocking_hits else "CLEAR",
            "nearest_existing": sorted(
                [f for f in findings if f["filter"].startswith("existing")],
                key=lambda f: -f["score"])[:3],
            "findings": findings,
        })

    return {"incomplete_sources": incomplete, "results": results,
            "summary": {
                "total": len(results),
                "clear": sum(1 for r in results if r["verdict"] == "CLEAR"),
                "review": sum(1 for r in results if r["verdict"] == "REVIEW"),
            }}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--config")
    ap.add_argument("--json", action="store_true", help="machine-readable to stdout")
    args = ap.parse_args()

    cfg = load_config(args.config)
    out = screen(load_candidates(args.candidates), cfg)

    if args.json:
        print(json.dumps(out, indent=1))
        return 0

    s = out["summary"]
    print(f"screened {s['total']} candidates — CLEAR {s['clear']} | REVIEW {s['review']}")
    if out["incomplete_sources"]:
        print(f"\n[INCOMPLETE SOURCES: {', '.join(out['incomplete_sources'])}]")
        print("A source that did not run is NOT a clean result. Compensate before "
              "treating any CLEAR as earned.")
    # Print every candidate, not just REVIEW rows. The nearest-existing evidence is
    # the most useful output for a topic that passed the deterministic checks — that
    # is exactly where a reviewer decides whether to spend a brief — and an earlier
    # version hid it behind the verdict, which defeated the point.
    for r in out["results"]:
        mark = "REVIEW" if r["verdict"] == "REVIEW" else "clear "
        print(f"\n  [{mark}] {r['id'] or ''} {r['title'][:60]}")
        for f in r["findings"]:
            if f["filter"].startswith("existing"):
                continue
            print(f"      {f['filter']:22} {f['match'][:58]}")
        for n in r["nearest_existing"]:
            print(f"      nearest-existing       {n['match'][:58]} ({n['score']})")
        if not r["findings"]:
            print("      (nothing close — no deterministic flags, no near matches)")
    print("\nREVIEW means look, not kill. Containment over-flags hub/spoke pairs by "
          "design.\nSemantic duplicates (different words, same job) still need the "
          "per-topic brief gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

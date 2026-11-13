#!/usr/bin/env python3
"""AI Mode / AI Overviews query classifier for Search Console data.

Closes a gap our own AI-visibility measurement methodology already named:
AI Overviews and AI Mode clicks arrive in Search Console as ordinary organic
search, invisible to referrer-based traffic cuts. There is no official GSC
filter for "this query came from a conversational AI surface" -- but leaked
conversational turns (a follow-up like "yes, go on" logged as a search query)
are a real, documented artifact, and pattern-matching for them is the free,
no-tooling-required way to estimate the slice referrer analysis structurally
can't see.

Technique credited to Jean-Christophe Chouinard, surfaced via a blog-research
pass (suganthan.com/blog/how-to-track-ai-mode-traffic/, Aug 2026). This is a
fresh implementation, not a port -- the original regex pattern wasn't
published verbatim, only its category list.

Precision over recall, deliberately: pure question-word queries ("how to...",
"what is...") are NOT flagged on their own -- that's just normal informational
search and flagging it would drown real signal in noise. What's flagged is
specifically assistant-directed phrasing: imperative prompt verbs, mid-
conversation acknowledgements/follow-ups that make no sense as a fresh search,
and first/second-person requests to an assistant.

Usage:
    # From a GSC query-dimension CSV (columns: query,clicks,impressions,ctr,position)
    python classify_queries.py queries.csv

    # From stdin, one query per line
    cat queries.txt | python classify_queries.py -

    # JSON output for chaining into other tooling
    python classify_queries.py queries.csv --json
"""

import argparse
import csv
import json
import re
import sys

# Each category is (name, weight, compiled pattern). Weight feeds a simple
# additive confidence score -- multiple independent signals on one query
# raise confidence faster than a single weak match.
CATEGORIES = [
    (
        "prompt_verb",
        2,
        re.compile(
            r"\b(write|draft|generate|summarize|summarise|explain|rewrite|"
            r"translate|compare|list|outline|paraphrase|brainstorm|"
            r"act as|pretend (you|to be)|role.?play as)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "assistant_request",
        2,
        re.compile(
            r"\b(can you|could you|would you|please (write|explain|give|tell|"
            r"help|summarize)|give me|help me (write|understand|find)|"
            r"i (want|need) you to)\b",
            re.IGNORECASE,
        ),
    ),
    (
        # Start-anchored, deliberately NOT end-anchored: real leakage is
        # often "<ack phrase>, <more turn text>" ("sounds good, what about
        # the second one"), not just the bare phrase alone. Matching only
        # a full-string equality missed exactly that shape.
        "acknowledgement_or_followup",
        3,
        re.compile(
            r"^(yes,?\s*(go on|continue|please)?\b|ok(ay)?,?\s*(go on|continue)?\b|"
            r"sounds good\b|got it\b|thanks?( you)?\b|sure,?\s*(go on)?\b|"
            r"go on\b|continue\b|keep going\b|one more thing\b|"
            r"what about\b|how about that\b|can you also\b)",
            re.IGNORECASE,
        ),
    ),
    (
        "refusal_or_correction",
        3,
        re.compile(
            r"^(no,?\s*(that.?s|thats)\s*(wrong|not right|not it|not what i "
            r"(meant|asked|wanted))|"
            r"try again|that.?s not what i (meant|asked|wanted)|"
            r"not (that|this) one|actually,? (i meant|no))",
            re.IGNORECASE,
        ),
    ),
    (
        "first_person_request",
        1,
        re.compile(
            r"^(i want|i need|i.?m (trying|looking) to|help me)\b",
            re.IGNORECASE,
        ),
    ),
]

# A bare question-word opener is NOT a signal by itself -- it's the majority
# shape of ordinary informational search. Only escalate a question-word query
# if it ALSO trips one of the categories above (e.g. "explain how tariffs
# work" -- prompt_verb + question word together is a stronger signal than
# either alone would be, so no special handling needed here; this constant
# exists only to document the deliberate omission).
QUESTION_WORDS = re.compile(r"^(how|what|why|when|where|who|which)\b", re.IGNORECASE)

CONFIDENCE_LABELS = [(5, "high"), (3, "medium"), (1, "low")]


def classify(query):
    """Return (matched_categories, score, confidence_label) for one query string."""
    query = query.strip()
    matched = []
    score = 0
    for name, weight, pattern in CATEGORIES:
        if pattern.search(query):
            matched.append(name)
            score += weight
    label = "none"
    for threshold, name in CONFIDENCE_LABELS:
        if score >= threshold:
            label = name
            break
    return matched, score, label


def read_queries(path):
    """Yield (query, extra_fields_dict) from a GSC CSV export, a raw CSV with
    a 'query' column, or plain stdin lines.

    Format is decided by file extension, not by content-sniffing for a comma
    -- a real query like "yes, go on" contains a comma too, and sniffing on
    that basis silently misparses exactly the conversational-leakage rows
    this tool exists to catch (caught by the test suite, not a hypothetical)."""
    if path == "-" or not path.lower().endswith(".csv"):
        source = sys.stdin if path == "-" else open(path, encoding="utf-8")
        try:
            for line in source:
                line = line.strip()
                if line:
                    yield line, {}
        finally:
            if source is not sys.stdin:
                source.close()
        return

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Be tolerant of GSC's export header casing/labels.
        query_key = None
        for candidate in ("query", "Query", "queries", "Queries"):
            if reader.fieldnames and candidate in reader.fieldnames:
                query_key = candidate
                break
        if query_key is None and reader.fieldnames:
            query_key = reader.fieldnames[0]
        for row in reader:
            q = (row.get(query_key) or "").strip()
            if q:
                extra = {k: v for k, v in row.items() if k != query_key}
                yield q, extra


def run(path):
    results = []
    total = 0
    for query, extra in read_queries(path):
        total += 1
        matched, score, label = classify(query)
        if matched:
            results.append({
                "query": query,
                "categories": matched,
                "score": score,
                "confidence": label,
                **extra,
            })
    results.sort(key=lambda r: -r["score"])
    return {"total_queries": total, "flagged": len(results), "results": results}


def print_human(report):
    total = report["total_queries"]
    flagged = report["flagged"]
    pct = (flagged / total * 100) if total else 0.0
    print(f"\n{flagged} of {total} queries flagged ({pct:.1f}%)\n")
    if not report["results"]:
        print("No conversational-leakage patterns matched. On a keyword-heavy")
        print("site this is the expected, correct result -- not a tool failure.")
        return
    by_confidence = {"high": [], "medium": [], "low": []}
    for r in report["results"]:
        by_confidence.setdefault(r["confidence"], []).append(r)
    for label in ("high", "medium", "low"):
        rows = by_confidence.get(label, [])
        if not rows:
            continue
        print(f"--- {label.upper()} confidence ({len(rows)}) ---")
        for r in rows:
            cats = ", ".join(r["categories"])
            extra_bits = " ".join(f"{k}={v}" for k, v in r.items() if k not in ("query", "categories", "score", "confidence"))
            print(f"  [{cats}] {r['query']!r}  {extra_bits}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="GSC query CSV export, or '-' for stdin (one query per line)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a human-readable report")
    args = parser.parse_args()

    report = run(args.input)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)

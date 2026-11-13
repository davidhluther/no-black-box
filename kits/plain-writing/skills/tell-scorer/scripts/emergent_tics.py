#!/usr/bin/env python3
"""Emergent-tic sweep — empirical displacement detector for the quarterly
styleguide re-check (writing-styleguide.md, Displacement watch, 2026-08-25).

Banned tells displace into forms no rule names. A memorized watch list cannot
catch the next one, so this tool surfaces candidates empirically: words,
bigrams, and sentence-openers whose per-1k rate INFLATED in new content
relative to a baseline cohort.

Usage:
    emergent_tics.py --html-dir DIR --selector CSS --split 2026-05-31
    emergent_tics.py --md-glob 'output/final/*.md' --baseline-glob 'archive/*.md'

--split divides HTML documents by their JSON-LD datePublished (baseline is
on-or-before the date). With markdown, supply the two cohorts as globs.

Output: three ranked tables (unigrams, bigrams, sentence-openers) of terms
with rate ratio >= --min-ratio and enough occurrences to matter. READ THEM,
don't auto-ban: topic drift inflates topic nouns (new FX content inflates
"hedging" without any tic existing). The human step is separating "new
subject matter" from "new verbal habit" — the habit gets named in the canon.
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tell_engine import parse_html, parse_markdown  # noqa: E402

WORD_RX = re.compile(r"[a-z][a-z'\-]+")


def prose_of(doc: dict) -> str:
    return " ".join(t for k, t, _ in doc["blocks"] if k in ("p", "li"))


def counts(texts: list[str]) -> tuple[Counter, Counter, Counter, Counter, int]:
    """Term counts plus per-term document frequency (docfreq separates verbal
    habits, which spread across documents, from topic nouns, which cluster)."""
    uni, bi, openers, docfreq = Counter(), Counter(), Counter(), Counter()
    total = 0
    for text in texts:
        words = WORD_RX.findall(text.lower())
        total += len(words)
        uni.update(words)
        bigrams = [f"{a} {b}" for a, b in zip(words, words[1:])]
        bi.update(bigrams)
        docfreq.update(set(words) | set(bigrams))
        for sent in re.split(r"(?<=[.!?])\s+", text):
            w = WORD_RX.findall(sent.lower())
            if len(w) >= 2:
                openers.update([f"{w[0]} {w[1]}"])
    return uni, bi, openers, docfreq, max(total, 1)


def report(name: str, before: Counter, after: Counter, wb: int, wa: int,
           min_after: int, min_ratio: float, top: int,
           docfreq: Counter | None = None, n_docs: int = 1) -> list[str]:
    """Habit candidates first: terms that ALSO existed in the baseline and
    inflated (finite ratio), spread across many documents. Topic nouns brought
    by new subject matter are NEW terms clustered in few documents — those are
    listed after, docfreq-ranked, mostly to be dismissed by the reader."""
    min_df = max(5, int(0.15 * n_docs)) if docfreq is not None else 0
    inflated, new_terms = [], []
    for term, na in after.items():
        if na < min_after:
            continue
        if docfreq is not None and docfreq.get(term, 0) < min_df:
            continue
        ra = na * 1000.0 / wa
        rb = before.get(term, 0) * 1000.0 / wb
        df = docfreq.get(term, 0) if docfreq is not None else 0
        if rb and ra / rb >= min_ratio:
            inflated.append((ra / rb, ra, rb, na, df, term))
        elif not rb:
            new_terms.append((ra, na, df, term))
    inflated.sort(key=lambda r: -r[0])
    new_terms.sort(key=lambda r: -r[2])
    out = [f"\n== {name}: HABIT CANDIDATES — in baseline, inflated >= {min_ratio}x, "
           f"spread over >= {min_df} docs ==",
           f"{'term':28s} {'after/1k':>9s} {'before/1k':>10s} {'ratio':>7s} {'n':>5s} {'docs':>5s}"]
    for ratio, ra, rb, na, df, term in inflated[:top]:
        out.append(f"{term:28s} {ra:9.3f} {rb:10.3f} {ratio:6.1f}x {na:5d} {df:5d}")
    if not inflated:
        out.append("  (none above threshold)")
    out.append(f"-- {name}: new-in-cohort terms (topic vocabulary vs habit — read and judge) --")
    for ra, na, df, term in new_terms[:max(5, top // 2)]:
        out.append(f"{term:28s} {ra:9.3f} {'0.000':>10s} {'NEW':>7s} {na:5d} {df:5d}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html-dir")
    ap.add_argument("--selector")
    ap.add_argument("--split", help="baseline = datePublished on/before this date")
    ap.add_argument("--md-glob")
    ap.add_argument("--baseline-glob")
    ap.add_argument("--min-after", type=int, default=12)
    ap.add_argument("--min-ratio", type=float, default=3.0)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--out")
    args = ap.parse_args()

    before_texts: list[str] = []
    after_texts: list[str] = []
    if args.html_dir:
        if not args.split:
            ap.error("--html-dir needs --split DATE")
        for p in sorted(Path(args.html_dir).glob("*.html")):
            doc = parse_html(p.read_text(), args.selector)
            if not doc["blocks"]:
                continue
            (before_texts if (doc["date"] or "") <= args.split
             else after_texts).append(prose_of(doc))
    elif args.md_glob and args.baseline_glob:
        for path in sorted(glob.glob(args.baseline_glob)):
            before_texts.append(prose_of(parse_markdown(Path(path).read_text())))
        for path in sorted(glob.glob(args.md_glob)):
            after_texts.append(prose_of(parse_markdown(Path(path).read_text())))
    else:
        ap.error("supply --html-dir/--split or --md-glob/--baseline-glob")

    ub, bb, ob, _dfb, wb = counts(before_texts)
    ua, ba, oa, dfa, wa = counts(after_texts)
    nd = len(after_texts)
    lines = [f"baseline: {len(before_texts)} docs, {wb:,} words | "
             f"new: {nd} docs, {wa:,} words"]
    lines += report("unigrams", ub, ua, wb, wa, args.min_after, args.min_ratio,
                    args.top, dfa, nd)
    lines += report("bigrams", bb, ba, wb, wa, args.min_after, args.min_ratio,
                    args.top, dfa, nd)
    lines += report("sentence openers", ob, oa, wb, wa,
                    max(6, args.min_after // 2), args.min_ratio, args.top)
    text = "\n".join(lines)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

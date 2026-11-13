#!/usr/bin/env python3
"""Corpus-fingerprint / uniformity index (content-discipline study, Arm 5).

Per-document tell checks can all pass while a corpus still reads as machine
output, because every page shares one voice. That is a corpus-level property
no per-page validator can see, and the emergent-tic sweep already showed it
exists in practice (a house vocabulary fingerprint in post-guideline content).

This measures it three ways, per cohort:

  style_uniformity   mean pairwise cosine similarity of per-page style vectors
                     (the per-1k tell features, z-scored across the corpus so
                     no single high-variance feature dominates). Higher = pages
                     resemble each other more in measurable style.
  opener_conc        share of sentences whose two-word opener is in the
                     cohort's top 20 openers. Higher = more formulaic entries.
  lexical_repeat     mean pairwise Jaccard overlap of each page's top-40
                     content words, stopwords removed. Topic-sensitive by
                     nature, so read it against cohorts of similar topic mix.

All three are RELATIVE measures. A single number means nothing; the signal is
the trend across cohorts (or against a competitor corpus, Arm 4). Cohorts come
from --date-cuts or --cohort-col, same syntax as cohort_compare.py.

Usage:
  uniformity.py scores.csv --html-dir DIR --selector CSS \
      --date-cuts "2026-05-31:legacy,2026-07-26:june,:current"
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tell_engine import COUNT_FEATURES, parse_html, parse_markdown  # noqa: E402

FEATURES = [f + "_per1k" for f in COUNT_FEATURES] + ["title_case_head_frac"]
WORD_RX = re.compile(r"[a-z][a-z'\-]+")
STOP = set("""the a an and or but of to in for on with as at by from is are was were be been
being it its this that these those we you they he she our your their his her not no if then
than so such can could will would should may might must have has had do does did done get
gets got make makes made use uses used one two three more most other some any all each which
who whom what when where why how there here into over under out up down about after before
between during without within across per via also just only same own too very s t re ve ll d""".split())


def cohort_of(date: str, cuts: list[tuple[str, str]]) -> str:
    if not date:
        return "unknown"
    for ceiling, label in cuts:
        if ceiling == "" or date <= ceiling:
            return label
    return "unknown"


def zscore(rows: list[list[float]]) -> list[list[float]]:
    n, m = len(rows), len(rows[0])
    out = [[0.0] * m for _ in range(n)]
    for j in range(m):
        col = [r[j] for r in rows]
        mu = sum(col) / n
        sd = (sum((x - mu) ** 2 for x in col) / n) ** 0.5
        for i in range(n):
            out[i][j] = 0.0 if sd == 0 else (rows[i][j] - mu) / sd
    return out


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-9
    nb = math.sqrt(sum(y * y for y in b)) or 1e-9
    return dot / (na * nb)


def mean_pairwise(vectors: list, fn, cap: int = 4000, seed: int = 7) -> float:
    """Mean pairwise similarity, sampled when the pair count is large."""
    n = len(vectors)
    if n < 2:
        return float("nan")
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if len(pairs) > cap:
        pairs = random.Random(seed).sample(pairs, cap)
    return sum(fn(vectors[i], vectors[j]) for i, j in pairs) / len(pairs)


def jaccard(a: set, b: set) -> float:
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", help="a score_batch.py CSV (supplies the style vectors)")
    ap.add_argument("--html-dir")
    ap.add_argument("--md-glob")
    ap.add_argument("--selector")
    ap.add_argument("--date-cuts")
    ap.add_argument("--cohort-col")
    ap.add_argument("--date-col", default="date_published")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--out")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.csv_path, newline="")))
    cuts = ([(c.split(":", 1)[0], c.split(":", 1)[1]) for c in args.date_cuts.split(",")]
            if args.date_cuts else [])
    order: list[str] = []
    for r in rows:
        r["_cohort"] = (r.get(args.cohort_col) or "unknown") if args.cohort_col \
            else cohort_of(r.get(args.date_col, ""), cuts)
    if args.date_cuts:
        order = [lab for _, lab in cuts]
    else:
        for r in rows:
            if r["_cohort"] not in order and r["_cohort"] != "unknown":
                order.append(r["_cohort"])

    # style vectors, z-scored across the whole corpus
    ids = [r.get(args.id_col) or r.get("slug") or "" for r in rows]
    raw = [[float(r.get(f) or 0) for f in FEATURES] for r in rows]
    z = zscore(raw)
    vec_by_id = dict(zip(ids, z))
    cohort_by_id = {i: r["_cohort"] for i, r in zip(ids, rows)}

    # text-derived measures
    text_by_id: dict[str, str] = {}
    if args.html_dir:
        for p in sorted(Path(args.html_dir).glob("*.html")):
            doc = parse_html(p.read_text(), args.selector)
            text_by_id[p.stem] = " ".join(t for k, t, _ in doc["blocks"] if k in ("p", "li"))
    elif args.md_glob:
        import glob as _g
        for path in sorted(_g.glob(args.md_glob)):
            doc = parse_markdown(Path(path).read_text())
            text_by_id[path] = " ".join(t for k, t, _ in doc["blocks"] if k in ("p", "li"))

    out_lines = ["| Cohort | n | style_uniformity | opener_conc | lexical_repeat |",
                 "|---|---|---|---|---|"]
    for coh in order:
        members = [i for i in ids if cohort_by_id.get(i) == coh]
        if len(members) < 3:
            continue
        style = mean_pairwise([vec_by_id[i] for i in members], cosine)

        texts = [text_by_id[i] for i in members if i in text_by_id]
        if texts:
            openers, total = Counter(), 0
            bags = []
            for t in texts:
                for sent in re.split(r"(?<=[.!?])\s+", t):
                    w = WORD_RX.findall(sent.lower())
                    if len(w) >= 2:
                        openers[f"{w[0]} {w[1]}"] += 1
                        total += 1
                words = [w for w in WORD_RX.findall(t.lower()) if w not in STOP and len(w) > 2]
                bags.append({w for w, _ in Counter(words).most_common(40)})
            conc = sum(c for _, c in openers.most_common(20)) / max(total, 1)
            lex = mean_pairwise(bags, jaccard)
        else:
            conc = lex = float("nan")
        out_lines.append(f"| {coh} | {len(members)} | {style:.3f} | {conc:.3f} | {lex:.3f} |")

    report = "\n".join(out_lines)
    print(report)
    print("\nRelative measures — read the trend across cohorts, never one number alone.")
    if args.out:
        Path(args.out).write_text(report + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

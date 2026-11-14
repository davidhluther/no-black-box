#!/usr/bin/env python3
"""Compare two scored runs of the same question set, cell by cell.

    python3 visibility_diff.py older_results.csv newer_results.csv [-o report.md]

Each input is a Results export (one row per question and AI product) with the
columns the kit uses: run_id, question_id, ai_product, answer_status, named,
your_site_cited, others_named, qset_version.

Refuses to compare when
  - the two files used different question set versions (the numbers would not
    mean the same thing), or
  - the files mix several versions, or
  - the two runs came from different collection methods (an app run versus an
    API run; products ending in "(API)" are a different instrument).
Brand-check (BV) and control (CT) questions are left out of the headline counts.
Standard library only; read-only.
"""
import argparse
import csv
import sys
from collections import defaultdict


def outcome(row):
    if row.get("answer_status") != "ok":
        return "not scored"
    named = row.get("named") == "y"
    cited = row.get("your_site_cited") == "y"
    if named and cited:
        return "named and cited"
    if named:
        return "named only"
    if cited:
        return "cited only"
    return "crowded out" if (row.get("others_named") or "").strip() else "absent"


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows = [r for r in rows if (r.get("run_id") or "").strip()]
    return rows


def method(rows):
    products = {r["ai_product"] for r in rows}
    return "api" if products and all("(API)" in p for p in products) else (
        "mixed" if any("(API)" in p for p in products) else "app")


def compare(old, new):
    problems = []
    vo, vn = {r.get("qset_version", "") for r in old}, {r.get("qset_version", "") for r in new}
    if len(vo) > 1 or len(vn) > 1:
        problems.append("A file mixes more than one question set version.")
    if vo != vn:
        problems.append(f"Question set versions differ ({sorted(vo)} versus {sorted(vn)}). Do not compare these runs.")
    if method(old) != method(new) or "mixed" in (method(old), method(new)):
        problems.append("The runs used different collection methods (app versus API). Do not compare them.")
    return problems


def table(old, new):
    key = lambda r: (r["ai_product"], r["question_id"])
    skip = lambda r: r["question_id"][:2] in ("BV", "CT")
    o = {key(r): outcome(r) for r in old if not skip(r)}
    n = {key(r): outcome(r) for r in new if not skip(r)}
    shared = sorted(set(o) & set(n))
    only_old, only_new = sorted(set(o) - set(n)), sorted(set(n) - set(o))
    good = ("named and cited", "named only", "cited only")
    moves = []
    for k in shared:
        if o[k] != n[k]:
            moves.append((k[0], k[1], o[k], n[k]))
    per = defaultdict(lambda: [0, 0, 0])  # shared scored, visible old, visible new
    for k in shared:
        if o[k] == "not scored" or n[k] == "not scored":
            continue
        per[k[0]][0] += 1
        per[k[0]][1] += o[k] in good
        per[k[0]][2] += n[k] in good
    lines = ["| AI product | cells scored in both runs | visible before | visible now |", "|---|---|---|---|"]
    for p in sorted(per):
        lines.append(f"| {p} | {per[p][0]} | {per[p][1]} | {per[p][2]} |")
    lines += ["", "Visible means named, cited, or both. Counts only; with this few cells a change of one or two is within normal answer-to-answer variation.", ""]
    lines += ["| AI product | question | before | now |", "|---|---|---|---|"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in moves] or ["| (no cell changed) | | | |"]
    if only_old or only_new:
        lines += ["", f"Cells in only one run (not compared): {len(only_old)} in the older, {len(only_new)} in the newer."]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("older")
    ap.add_argument("newer")
    ap.add_argument("-o", "--output")
    a = ap.parse_args()
    old, new = load(a.older), load(a.newer)
    problems = compare(old, new)
    if problems:
        print("Not comparable:\n  - " + "\n  - ".join(problems), file=sys.stderr)
        return 1
    text = table(old, new)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

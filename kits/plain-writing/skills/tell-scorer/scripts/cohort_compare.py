#!/usr/bin/env python3
"""Cohort comparison over tell-score CSVs — the regression-test view.

Answers "what changed, per rule" between publication eras, before/after a
guideline deployment, or between two arbitrary runs of score_batch.py.

Cohort assignment (pick one):
  --date-cuts "2026-05-31:legacy,2026-07-26:june,:current"
        ascending date ceilings with labels; the empty-ceiling last entry
        catches everything after. Applied to --date-col (default
        date_published).
  --cohort-col COLNAME
        use an existing column as the cohort label.
  --baseline FILE.csv
        two-run compare: FILE is cohort "before", the main CSV is "after".

Output: per-feature cohort means, a Kruskal-Wallis p where scipy is
available and there are 3+ cohorts (2 cohorts get Mann-Whitney), and a
direction read. Markdown to stdout; --out writes it to a file.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tell_engine import COUNT_FEATURES  # noqa: E402

FEATURES = [f + "_per1k" for f in COUNT_FEATURES] + [
    "title_case_head_frac", "composite_hard_per1k", "composite_mech_per1k",
    "composite_all_per1k"]


def read_csv(path: str) -> list[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def assign_cohorts(rows: list[dict], args) -> list[tuple[str, dict]]:
    if args.cohort_col:
        return [(r.get(args.cohort_col, "unknown") or "unknown", r) for r in rows]
    cuts = []
    for part in args.date_cuts.split(","):
        ceiling, label = part.split(":", 1)
        cuts.append((ceiling, label))
    out = []
    for r in rows:
        d = r.get(args.date_col, "") or ""
        label = "unknown"
        for ceiling, lab in cuts:
            if ceiling == "" or d <= ceiling:
                label = lab
                break
        if not d:
            label = "unknown"
        out.append((label, r))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--date-cuts")
    ap.add_argument("--cohort-col")
    ap.add_argument("--baseline")
    ap.add_argument("--date-col", default="date_published")
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.baseline:
        tagged = ([("before", r) for r in read_csv(args.baseline)]
                  + [("after", r) for r in read_csv(args.csv_path)])
        order = ["before", "after"]
    else:
        if not (args.date_cuts or args.cohort_col):
            ap.error("need --date-cuts, --cohort-col, or --baseline")
        tagged = assign_cohorts(read_csv(args.csv_path), args)
        if args.date_cuts:
            # cohort order = the cuts sequence as given (chronological),
            # never first-seen file order
            order = [part.split(":", 1)[1] for part in args.date_cuts.split(",")]
            order = [c for c in order if any(l == c for l, _ in tagged)]
        else:
            seen: list[str] = []
            for label, _ in tagged:
                if label not in seen and label != "unknown":
                    seen.append(label)
            order = seen

    groups: dict[str, list[dict]] = {}
    for label, row in tagged:
        groups.setdefault(label, []).append(row)

    try:
        from scipy import stats as _st
    except ImportError:
        _st = None

    lines = ["| Feature | " + " | ".join(f"{c} (n={len(groups[c])})" for c in order)
             + " | p | read |", "|---" * (len(order) + 3) + "|"]
    for feat in FEATURES:
        vals = {}
        for c in order:
            xs = [float(r[feat]) for r in groups[c] if r.get(feat) not in (None, "")]
            vals[c] = xs
        means = {c: (sum(v) / len(v) if v else float("nan")) for c, v in vals.items()}
        p = ""
        if _st and all(len(v) >= 5 for v in vals.values()):
            try:
                if len(order) >= 3:
                    p = f"{_st.kruskal(*(vals[c] for c in order)).pvalue:.4f}"
                elif len(order) == 2:
                    a, b = (vals[c] for c in order)
                    p = f"{_st.mannwhitneyu(a, b).pvalue:.4f}"
            except ValueError:
                p = "-"
        first, last = means[order[0]], means[order[-1]]
        if first != first or last != last:
            read = "-"
        elif last < first * 0.5:
            read = "improved"
        elif last > first * 1.5 and last > 0.05:
            read = "WORSE"
        else:
            read = "flat"
        lines.append("| " + feat + " | "
                     + " | ".join(f"{means[c]:.3f}" for c in order)
                     + f" | {p} | {read} |")

    report = "\n".join(lines)
    print(report)
    if args.out:
        Path(args.out).write_text(report + "\n")
        print(f"\nwritten -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check a grant draft against your claims register.

  python3 check_draft.py <draft.md> [--claims claims.csv] [--banned banned-phrases.txt]

What it checks, in the draft body only (the text between `<!-- draft -->` and
`<!-- end draft -->`, or the whole file if those markers are missing, so a cover note and
claims appendix can mention deadlines and IDs freely):

  - numbers that match no value in the claims register and are not on the draft's
    `allow:` line (put the ask amount, deadlines and funder figures there)
  - phrases you banned (one regular expression per line in banned-phrases.txt; use it for
    wording your organization never uses about itself)
  - claim IDs in the appendix that do not exist, or whose status is not usable

It also lists open [CONFIRM ...] placeholders. Exit code 1 means at least one flag.
Read-only: it never changes your files and never sends anything anywhere.

claims.csv columns: id, claim, value, as_of, source, status
  status must start with source-verified or external-verified for the claim to count.
  Put one number per row in `value`, written as it appears in drafts (35 for 35%).
"""
import argparse
import csv
import re
import sys
from pathlib import Path

NUM = re.compile(r"(?<![\w.])\$?\d[\d,]*(?:\.\d+)?%?")
USABLE = ("source-verified", "external-verified")


def norm(tok):
    """'$1,234.50' -> {'1234.5'}; '35%' -> {'35', '0.35'}."""
    t = tok.replace("$", "").replace(",", "").rstrip(".")
    pct = t.endswith("%")
    t = t.rstrip("%")
    try:
        v = float(t)
    except ValueError:
        return set()
    out = {f"{v:g}"}
    if pct:
        out.add(f"{v / 100:g}")
    return out


def claim_values(claims_path):
    vals, status = set(), {}
    with open(claims_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            st = (row.get("status") or "").strip().lower()
            status[(row.get("id") or "").strip()] = st
            if not st.startswith(USABLE):
                continue  # unverified numbers never pass the check
            for tok in NUM.findall((row.get("value") or "") + " " + (row.get("claim") or "")):
                vals |= norm(tok)
    return vals, status


def check(text, claims_path, banned=()):
    m = re.search(r"<!-- draft -->(.*?)<!-- end draft -->", text, re.S)
    body = m.group(1) if m else text
    allow = set()
    for line in re.findall(r"^allow:(.*)$", text, re.M | re.I):
        for tok in NUM.findall(line):
            allow |= norm(tok)
    vals, status = claim_values(claims_path)
    problems = []
    scan = re.sub(r"\b[A-Z]{2,8}-\d{2,3}\b", " ", body)  # claim IDs are not numbers
    for tok in sorted(set(NUM.findall(scan))):
        n = norm(tok)
        if not n:
            continue
        v = float(next(iter(n)))
        if v <= 10 and "%" not in tok and "$" not in tok:
            continue  # small counts ("three staff") are fine
        if not (n & (vals | allow)):
            problems.append(f"number not in the claims register or allow: line -> {tok}")
    for pat in banned:
        for hit in re.finditer(pat, body, re.I):
            problems.append(f"banned phrasing -> '{hit.group(0)}'")
    for cid in sorted(set(re.findall(r"\b[A-Z]{2,8}-\d{2,3}\b", text))):
        st = status.get(cid)
        if st is None:
            problems.append(f"claim ID not in the register -> {cid}")
        elif not st.startswith(USABLE):
            problems.append(f"claim {cid} has status '{st}', not usable")
    confirms = re.findall(r"\[CONFIRM[^\]]*\]", body)
    return problems, confirms


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--claims", default="claims.csv")
    ap.add_argument("--banned", default=None)
    a = ap.parse_args(argv)
    banned = []
    if a.banned:
        banned = [ln.strip() for ln in Path(a.banned).read_text(encoding="utf-8").splitlines()
                  if ln.strip() and not ln.startswith("#")]
    problems, confirms = check(Path(a.draft).read_text(encoding="utf-8"), a.claims, banned)
    for p in problems:
        print("FLAG", p)
    print(f"{len(problems)} flag(s); {len(confirms)} open [CONFIRM] placeholder(s)")
    for c in confirms:
        print("  ", c)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

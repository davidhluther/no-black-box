#!/usr/bin/env python3
"""Read-only checker for a capability ledger (CAPABILITIES.md).

Checks: header date present and not stale; the three sections exist; each row
in the Live table has a shipped date and a proof; every proof written as a
backticked file path exists. With --find it lists every line containing a
phrase, so a correction can be made everywhere the old claim appears.

Exit codes: 0 no problems, 1 problems found, 2 could not run.
Standard library only. Writes nothing.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

HEADER = re.compile(r"^Last verified against repo:\s*(\d{4}-\d{2}-\d{2})\s+by\s+(\S.*)$", re.M)
SECTIONS = [("live", r"^##\s*1\.?\s*Live capabilities"),
            ("staged", r"^##\s*2\.?\s*In progress"),
            ("not_built", r"^##\s*3\.?\s*Known NOT built")]
PATHISH = re.compile(r"`([^`\s]+\.[A-Za-z0-9]{1,6}|[^`\s]+/[^`\s]*)`")


def rows(block):
    out = []
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        out.append(cells)
    return out[1:] if out else []  # drop the header row


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ledger")
    ap.add_argument("--root", help="folder that proof paths are relative to (default: the ledger's folder)")
    ap.add_argument("--max-age-days", type=int, default=30)
    ap.add_argument("--find", help="list every line containing this phrase and exit")
    a = ap.parse_args()
    p = Path(a.ledger).expanduser()
    if not p.is_file():
        print(f"could not run: {p} is not a file")
        return 2
    text = p.read_text(encoding="utf-8", errors="replace")
    if a.find:
        hits = [(i, l) for i, l in enumerate(text.splitlines(), 1) if a.find.lower() in l.lower()]
        for i, l in hits:
            print(f"{p.name}:{i}: {l.strip()}")
        print(f"{len(hits)} line(s) contain the phrase")
        return 0
    root = Path(a.root).expanduser() if a.root else p.parent
    problems, notes = [], []
    m = HEADER.search(text)
    if not m:
        problems.append("missing header line 'Last verified against repo: YYYY-MM-DD by <who>'")
    else:
        try:
            age = (dt.date.today() - dt.date.fromisoformat(m.group(1))).days
            if age < 0:
                problems.append("header date is in the future")
            elif age > a.max_age_days:
                problems.append(f"header date is {age} days old (limit {a.max_age_days}); reverify and update it")
        except ValueError:
            problems.append("header date is not a real date")
    spans = {}
    for name, pat in SECTIONS:
        s = re.search(pat, text, re.M | re.I)
        if not s:
            problems.append(f"missing section: {name.replace('_', ' ')}")
        else:
            spans[name] = s.start()
    order = sorted(spans.items(), key=lambda kv: kv[1])
    blocks = {}
    for i, (name, start) in enumerate(order):
        nxt = re.search(r"^##\s", text[start + 3:], re.M)
        blocks[name] = text[start:start + 3 + nxt.start()] if nxt else text[start:]
    if "live" in blocks:
        live = rows(blocks["live"])
        if not live:
            notes.append("Live capabilities table has no rows")
        for r in live:
            label = r[0][:50] if r else "?"
            if len(r) < 4:
                problems.append(f"Live row '{label}' has fewer than four columns")
                continue
            shipped, proof = r[2], r[3]
            if not re.search(r"\d{4}-\d{2}-\d{2}", shipped):
                problems.append(f"Live row '{label}' has no shipped date")
            if not proof or proof.lower() in {"", "tbd", "n/a", "none", "-"}:
                problems.append(f"Live row '{label}' has no proof")
            for ref in PATHISH.findall(proof):
                if ref.startswith(("http", "#")):
                    continue
                if not (root / ref).exists():
                    problems.append(f"Live row '{label}': proof path not found: {ref}")
    for x in notes:
        print("note:", x)
    for x in problems:
        print("problem:", x)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

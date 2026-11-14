#!/usr/bin/env python3
"""Read-only checker for a session brief.

Confirms the file opens with Purpose, Session and Compactions lines, that
Compactions is a whole number, that a 'Settled, never re-ask' section exists,
and warns when the brief is long. With --purpose-was, confirms the Purpose line
still equals the text you recorded when the session began.

Exit codes: 0 fine, 1 problems found, 2 could not run. Standard library only.
"""
import argparse
import re
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("brief")
    ap.add_argument("--max-lines", type=int, default=150)
    ap.add_argument("--purpose-was", help="the Purpose text recorded at session start")
    a = ap.parse_args()
    p = Path(a.brief).expanduser()
    if not p.is_file():
        print(f"could not run: {p} is not a file")
        return 2
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    problems, warns = [], []
    head = [l for l in lines[:6] if l.strip()]
    keys = {}
    for l in head:
        m = re.match(r"^(Purpose|Session|Compactions):\s*(.*)$", l)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    for k in ("Purpose", "Session", "Compactions"):
        if k not in keys or not keys[k]:
            problems.append(f"header line '{k}:' missing or empty in the first lines")
    if "Compactions" in keys and not re.fullmatch(r"\d+", keys["Compactions"].split()[0] if keys["Compactions"] else ""):
        problems.append("Compactions must start with a whole number")
    elif "Compactions" in keys and int(keys["Compactions"].split()[0]) >= 3:
        warns.append("Compactions is 3 or more: hand off now, before resuming task work")
    if not any(re.match(r"^#+\s*Settled, never re-ask", l, re.I) for l in lines):
        problems.append("missing section 'Settled, never re-ask'")
    if len(lines) > a.max_lines:
        warns.append(f"brief is {len(lines)} lines (limit {a.max_lines}); move detail to a file it points to")
    if a.purpose_was is not None and keys.get("Purpose") != a.purpose_was.strip():
        problems.append("Purpose line differs from the recorded text; do not rewrite it, hand off instead")
    for w in warns:
        print("warning:", w)
    for x in problems:
        print("problem:", x)
    print(f"{len(problems)} problem(s), {len(warns)} warning(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

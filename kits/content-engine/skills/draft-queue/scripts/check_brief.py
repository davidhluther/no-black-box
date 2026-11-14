#!/usr/bin/env python3
"""Brief completeness gate.

A brief must have the shape the content-brief template defines before anyone drafts
from it. This script checks that shape and nothing else. It never edits a brief.

  New-post briefs (first line starts "# Content Brief:") need the new-post sections.
  Refresh briefs (first line starts "# Refresh Brief:") need the refresh sections.
  Anything else is refused as a partial or hand-rolled shape.

Exit 0 = complete. Exit 2 = partial (the missing parts are listed). Exit 1 = the file
is missing or unreadable.

Usage: python3 check_brief.py <path-to-brief.md>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CONTENT_REQUIRED = (
    "## Keyword Data",
    "## Strategy Context",
    "## Cross-Project Redundancy Check",
    "**Recommended action:**",
    "## Voice of Customer",
    "## Search Intent",
    "## Verified Statistics",
    "## Internal Link Targets",
    "## Article Outline",
    "## Cost Report",
)
REFRESH_REQUIRED = (
    "## Strategy Context",
    "| Element | Status |",   # the pass/partial/fail scorecard table
    "Statistics",
    "Outline",
    "## Cost Report",
)
MIN_WORDS = 300


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_brief.py <brief-path>", file=sys.stderr)
        return 1
    p = Path(sys.argv[1]).expanduser()
    if not p.exists():
        print(f"BRIEF MISSING: {p}. Briefs come from the content-brief skill.")
        return 1
    try:
        text = p.read_text()
    except OSError as e:
        print(f"BRIEF UNREADABLE: {e}")
        return 1

    missing: list[str] = []
    if re.search(r"^# Content Brief:", text, re.MULTILINE):
        mode, required = "content", CONTENT_REQUIRED
        if not re.search(r"\|\s*Target keyword\s*\|", text):
            missing.append("Keyword Data row: Target keyword")
    elif re.search(r"^# Refresh Brief:", text, re.MULTILINE):
        mode, required = "refresh", REFRESH_REQUIRED
    else:
        print("BRIEF PARTIAL, refusing. It is not a content-brief shape:")
        print("  missing: first heading '# Content Brief:' or '# Refresh Brief:'")
        print("Produce it with the content-brief skill.")
        return 2

    for marker in required:
        if marker not in text:
            missing.append(marker)
    words = len(text.split())
    if words < MIN_WORDS:
        missing.append(f"body substance ({words} words, need {MIN_WORDS})")

    if missing:
        print(f"BRIEF PARTIAL ({mode} mode). Never draft from a partial brief:")
        for m in missing:
            print(f"  missing: {m}")
        print("Produce or complete it with the content-brief skill.")
        return 2
    print(f"brief complete ({mode}): {p.name} ({words} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

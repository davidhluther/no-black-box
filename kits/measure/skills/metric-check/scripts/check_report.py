#!/usr/bin/env python3
"""Warn about gaps in a written report. Reads one .md or .html file; prints warnings; changes nothing.

Checks: (1) sentences that claim a cause with no grade word nearby, (2) fewer than two named
sources, (3) no date range, (4) no mention of definition changes or tracking changes,
(5) no 'single-source' label when only one source is named.
A clean pass is not proof the analysis is right. Usage: python3 check_report.py report.md
"""
import re
import sys

CAUSE = re.compile(r"\b(because|caused by|due to|driven by|the reason|as a result of|explained by)\b", re.I)
GRADE = re.compile(r"\b(holds|weakened|refuted|not verified)\b", re.I)
SOURCES = ["search console", "ga4", "google analytics", "bing", "clarity", "ahrefs", "semrush",
           "looker", "crm", "email platform", "ad platform", "rank tracker"]
DATE = re.compile(r"\b(\d{1,2}/\d{1,2}(/\d{2,4})?|\d{4}-\d{2}-\d{2}|data (runs )?through)\b", re.I)


def main(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"<[^>]+>", " ", text)
    warns = []
    paras = [p for p in re.split(r"\n\s*\n", text) if CAUSE.search(p)]
    for p in paras:
        if not GRADE.search(p):
            warns.append("Causal wording with no grade (holds / weakened / refuted / not verified): " + p.strip()[:90].replace("\n", " ") + "...")
    named = [s for s in SOURCES if s in text.lower()]
    if len(named) < 2:
        warns.append(f"Fewer than two sources named ({', '.join(named) or 'none'}). Check direction on a second independent source.")
    if len(named) < 2 and "single-source" not in text.lower() and "single source" not in text.lower():
        warns.append("Only one source and no 'single-source' label.")
    if not DATE.search(text):
        warns.append("No date range or 'data runs through' date found.")
    if not re.search(r"definition|tracking change|tag change|reclassif", text, re.I):
        warns.append("No mention of definition or tracking changes. Say there were none, or name them.")
    if warns:
        print("\n".join("WARN: " + w for w in warns))
        return 1
    print("No gaps found by this script. Read the analysis yourself anyway.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))

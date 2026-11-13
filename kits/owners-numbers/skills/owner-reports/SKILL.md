---
name: owner-reports
description: Turns monthly Owner's Scorecards into three documents, a quarterly report, a short advisory letter and a 12-month roadmap. Observed numbers are findings, the single look ahead is a labeled what-if, and roadmap targets stay "to set" until the owner types a real number. Use when an owner, bookkeeper or board treasurer wants a quarterly summary, a monthly letter to a partner or board, or a yearly plan built from the numbers.
---

# Owner Reports

Works in: Claude Code (full version). The templates in `references/templates.md` also work by hand in Claude.ai, ChatGPT or any word processor.

## Inputs

- Up to three `scorecard.json` files made by the owner-scorecard skill, for the quarterly report.
- One `scorecard.json`, for the advisory letter.
- A `targets.csv` with columns metric, baseline, target, quarter, why, for the roadmap.

## Commands

```
python3 scripts/quarterly_report.py month1.json month2.json month3.json --out quarterly-report.md
python3 scripts/advisory_letter.py scorecard.json --from "Your name" --to "Owner" --out advisory-letter.md
python3 scripts/roadmap.py targets.csv --business "Your business" --start-month 2026-10 --out roadmap.md
```

Each script only reads the files you name and writes one markdown file. None makes a network call.

## Method

1. Make sure every month has a scorecard first. A report built on a missing month would hide the gap, so say which month is missing.
2. Run the script, then read the draft out loud in plain words and edit it. The scripts write the bones. A person adds the judgment.
3. In the quarterly report keep the look ahead labeled what-if and name the season next to it.
4. In the roadmap pick two or three targets per quarter. A target the owner has not set stays "to set".

## Rules that never bend

- Observed numbers are findings. Anything built on an example input is a what-if and says so.
- The letter states an observation and asks a question. It does not sell anything and does not tell the owner what to decide.
- No outside benchmark replaces the owner's own baseline.
- Dates are written mm/dd/yyyy.

## Reference

`references/templates.md` describes each document's sections.

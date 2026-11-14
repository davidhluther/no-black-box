---
name: ai-traffic-classifier
description: Flag [Search Console](../../glossary.md#search-console) queries that look like leaked AI conversation turns ("yes, go on", "write me a...", "can you explain...") rather than ordinary searches, to estimate a lower bound of AI-driven traffic that source-based reports cannot see. Use when auditing a Search Console query export for conversational AI leakage, or when [GA4](../../glossary.md#ga4) shows little AI traffic and you want a second signal.
---

# AI traffic classifier

Works in: Claude Code (full version), because it runs a small [Python](../../glossary.md#python) [script](../../glossary.md#script). The method also works by eye on a short export.

## Why this exists

Clicks from Google's AI answers arrive in Search Console as ordinary search, so reports that look at where a visit came from cannot see them. There is no official filter. But a documented artifact exists: sometimes a follow-up turn in an AI conversation ("yes, go on") gets logged as if someone typed it into search. Matching that shape is a free way to estimate the slice the other reports miss. The technique comes from Jean-Christophe Chouinard, as described in a blog write-up in August 2026. The category list (prompt verbs, acknowledgements, refusals, follow-ups) was published; the exact pattern was not, so this is a fresh implementation of the categories, not a copy.

## What it claims, and what it does not

A flagged count is a floor ("at least this many"), never the true AI share. Most AI-driven traffic looks like an ordinary query and cannot be told apart. The script favors precision over recall: a bare question word ("how to", "what is") is never flagged alone, because that is the ordinary shape of search. It flags assistant-directed phrasing: instructions, follow-ups that make no sense as a fresh search, and first-person requests to an assistant.

It cannot tell a leaked AI turn from a person who really typed a conversational phrase into Google, which happens rarely. It cannot say which AI product. Read the flagged rows before quoting any count.

## Use

In Search Console choose Performance, then the Queries tab, set the dates, and Export to CSV (Google Sheets or Download CSV). Then:

```
python3 scripts/classify_queries.py queries.csv
python3 scripts/classify_queries.py queries.csv --json
```

A `.csv` file name is required for CSV parsing; anything else is read as one query per line, and `-` reads from standard input. Never mix two businesses' query files in one run.

## Reporting

Record the dates, the number of queries, the flagged count with the confidence breakdown (high, medium, low), and the flagged rows you read. If nothing is flagged, write that down too. On a small site with plain keyword queries it is the expected result, not a failure. Put the figure in `unified-visibility` as a lower bound beside the GA4 AI traffic count; the two measure different things and should not be added together.

## Tuning

The patterns are a starting instrument. Add a pattern only after you have seen real flagged or missed rows in your own data, and re-check that ordinary queries stay clean.

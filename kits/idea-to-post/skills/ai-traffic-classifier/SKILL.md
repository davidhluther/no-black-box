---
name: ai-traffic-classifier
description: Flag Search Console queries that look like leaked turns of an AI conversation (such as "yes, go on" or "can you summarize") instead of ordinary searches. Use to estimate a lower bound for AI Mode and AI Overviews traffic that referrer-based reports cannot see, or to audit a query export for conversational leakage.
---

# AI Mode and AI Overviews query classifier

Works in: Claude Code (full version). It runs a Python script on a CSV file. In Claude.ai or ChatGPT with code running turned on, upload the CSV and ask the model to run it.

## Why this exists

Clicks from Google's AI Overviews and AI Mode reach your site looking like ordinary search. Referrer-based reports (the ones that read where a visitor came from) cannot separate them, and Search Console has no filter for "came from an AI surface". One documented artifact exists: sometimes a follow-up turn in an AI conversation ("yes, go on") is logged in Search Console as if it were a fresh search. Matching for that shape is a free way to estimate the slice nobody else can see.

The technique is credited to Jean-Christophe Chouinard and was surfaced through a 2026 blog post that named the categories (prompt verbs, greetings, acknowledgements, refusals, follow-ups) but published no exact pattern. This is a fresh implementation built from that category list and tested on real data, not a copy of anyone's code.

## What it claims and what it does not

**It estimates a lower bound, not a count.** It catches queries that look like leaked conversational turns. It cannot catch AI traffic that arrives as an ordinary-looking query, which is most of it. Treat any flagged count as "at least this many", never as the true AI Mode share.

**It favors precision over recall on purpose.** A bare question like "how to fix a leaky tap" or "what is a 501(c)(3)" is never flagged by itself, because that is how normal searching looks and flagging it would bury the real signal. What it flags is phrasing aimed at an assistant: command verbs, acknowledgement or follow-up phrases that make no sense as a fresh search, and first-person requests.

Tested on about 250 real queries from a working Search Console property, it produced no false positives, including natural-language queries a naive question-word filter would have flagged. On synthetic examples built from the documented categories it caught eight of ten, and the two ordinary controls stayed clean.

## Run it

Get your queries into a CSV file in either of two ways.

- **Free, by hand.** In Search Console, open Performance, set the dates, then Export and Download CSV. Use the file named like `Queries.csv`. The script reads the first column when no column is called `query`.
- **With the `gsc-read` skill.** Use its capture's query rows, saved to a CSV.

Then:

```bash
python3 scripts/classify_queries.py queries.csv
```

Only a file ending in `.csv` is read as a spreadsheet. Anything else, including `-` for typed input, is read as one query per line. That is deliberate. Guessing the format from a comma once swallowed real queries such as "yes, go on".

Add `--json` for output that other tools can read.

## Known limits

- The patterns are a fresh construction against a described category list. Expect to tune them against real flagged and missed examples from your data. This is a starting instrument.
- It cannot tell a leaked AI conversation from a person who really typed a conversational phrase into Google, which happens, rarely. Read the flagged rows before quoting a count anywhere.
- It works on the query alone. It cannot say which AI service a flagged query came from.
- A site full of keyword-style searches will often return nothing. That is the expected result, not a failure.

## Using it responsibly

- Never quote a flagged count in a report without reading the flagged rows.
- Keep each organization's query data separate. Never mix two sites' queries in one run.
- It makes no network calls, reads no keys, and writes no files.

---
name: topic-screen
description: Screen a list of candidate blog topics before you spend time on briefs. Checks each topic against your existing and planned posts, a minimum search demand, and the other topics on the list, then sorts them into go, look again, and drop. Use after the idea pass and before writing any brief, whenever someone says "which of these should we write" or "do we already have a post on this".
---

# Topic screen

Works in: Claude Code (full version) with the script `topic_screen.py`. The same screen works by paste in Claude Code, Claude.ai, and ChatGPT using the free-version prompt 2.

## Why screen first

A brief costs real time and sometimes paid keyword credits. Topics that are already covered, already planned, duplicated within the same list, or have no measurable search demand should be caught before that cost. The screen is deliberately cheap and deliberately modest about what it knows.

## Read the settings

Read `config.json`, block `topic_screen`, plus `site.sitemap_url` and `queue.stages`. If a source is missing (no sitemap, no queue export, no briefs folder), say which one was not checked. A check that did not run is incomplete, never clean.

## With the script

1. Make a candidates file with `title`, `keyword`, `volume` (monthly searches, if known), and `rationale` for any topic below the floor you still want.
2. Export your Queue tab as CSV into the path named in `topic_screen.board_dump`.
3. Run `python3 topic_screen.py --candidates <file> --config config.json`.
4. Read every candidate's block, including the nearest existing matches for ones marked clear. The matches are evidence, not a verdict. Similar words do not prove the same job, and different words can hide a duplicate.

## Without the script

Ask the user for the list of existing and planned titles, the candidate list, and any search numbers. Do the same three checks by reading.

1. Does each candidate overlap with an existing or planned post? Say which. Call it "different job" when the words overlap but a reader would want something different.
2. Does it overlap with another candidate on the list?
3. Is its monthly search number under the floor? If so, did the user write a reason?

Never guess a search number. Candidates with no number are listed as "no volume, find one before briefing".

## Output

Three lists. **Go** has no deterministic flag. **Look again** has a flag, with one sentence each on what to resolve. **Drop** is for topics the user confirms are covered. Then add one note on acronyms and common nouns. Before a keyword goes into a brief, check what a search for it actually returns; a high-volume phrase can belong to something unrelated to your field.

## What this does not do

It does not decide. REVIEW means look, not kill. It does not find topics worded differently that do the same job; the brief step's redundancy check handles those.

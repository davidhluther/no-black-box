---
name: aeo-trends
description: Report what actually changed between monthly AI visibility runs, and whether it belongs to your business or to the measuring tool. Checks that both runs used the same questions and conditions, reports cell-by-cell flips, and refuses to claim a trend from a single month ([baseline](../../glossary.md#baseline)) or to forecast. Use for month-over-month reviews and "is our work paying off" questions.
---

# AEO trends

Works in: [Claude Code](../../glossary.md#claude-code), Claude.ai, ChatGPT. For a [script](../../glossary.md#script) that does the cell comparison for you, see `visibility-diff`.

## The rule that comes first

Check what changed in the instrument before you credit the business. A different [question set](../../glossary.md#question-set), a different model version, a different location, or a different signed-in state can move the numbers on its own. And never compare an app run with an [API](../../glossary.md#api) run.

## Step 0: Pick the mode

- One run: baseline. State "baseline" where a change would go. Invent no prior and claim no trend. One run is a complete, honest result.
- Two runs: comparison. Cell-accurate changes.
- Three or more: series. Comparison plus a coarse direction for each measure (improving, declining, flat, mixed), judged only by whether every step moves the same way. No slopes, no forecasts, no projected dates.

## Step 1: Diff the run headers

For each pair compare model names, location and connection, signed-in state, skipped questions, and question set version. Questions added or retired start their own series and stay out of the comparison; compare only the questions both runs share, and say how many that is. Any difference is a possible regime shift: report the movement but label each affected number with the confound. A model version change drops that product's changes to unverified.

## Step 2: Measure changes

Over shared questions: named (clean where both runs have a [noise audit](../../glossary.md#noise-audit), otherwise raw to raw, and label which), cited, brand-check identification. Per tracked brand, the change in clean share.

## Step 3: Cell-level flips

Questions are fixed, so flips are exact. Report by cell: missed then named, named then missed, position changes, new or lost cited domains, competitors entering or leaving, software-to-person answer flips. For surprising flips read the raw answers and quote them. When a competitor rises and you fall on the same questions, pair them.

## Step 4: Attribution

Before crediting shipped work (a new listing, page, or profile): check the confounds, check whether the change sits in one product only (more likely the model than you), and state the mechanism as a hypothesis ("the directory listing went live in November and that domain first appears in November answers", likely, not confirmed). Anything behind a live confound stays unverified. The instrument cannot tell "you moved" from "the model moved". Say so whenever it applies.

## Output

`analysis/<run>/trends.md` (300 to 600 words): mode first, confounds second, then what moved, notable flips, and attribution with its uncertainty. Label every number clean or raw.

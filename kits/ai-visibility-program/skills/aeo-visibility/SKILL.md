---
name: aeo-visibility
description: Count how present a business is in AI answers from a scored question run. Reports clean versus raw named counts, [citations](../../glossary.md#citation) to your website, position, per-group presence, and a miss breakdown (someone else named, nobody named, answered with software). Use when asked "how visible are we in AI answers" or for the numbers half of a monthly review. Run answer-noise-audit first.
---

# AEO visibility

Works in: [Claude Code](../../glossary.md#claude-code), Claude.ai, ChatGPT (upload the scored file and the [noise audit](../../glossary.md#noise-audit)).

## The principle

Counts lead and percentages follow. "Named in 3 of 80 cells" is the honest shape at this size. A battery of questions across four AI products is small and exact, not large and fuzzy. A zero is a result, not an error; for a young or small business it is the normal early state.

## What to read

`runs/<run>/scored.csv`, `analysis/<run>/noise-audit.md`, `config.json`. Without a noise audit for the same run, produce raw numbers only and label them "unverified, not citable".

## Step 1: Denominators

Count scored cells. Leave out brand-check (BV) and control (CT) cells from the headline. Skipped, refused, or failed cells shrink the denominator and are never counted as "not named". Show both the planned and the effective number of cells.

## Step 2: Headline numbers

- Named: raw and clean (from the noise audit), over the effective headline cells.
- Cited: cells where your website is among the sources the model listed. Citation often comes before naming, so show it even when names are zero.
- Brand-check identification: how many brand-check cells correctly identify your business. Report separately; never add it to the headline.
- Share among tracked names: your clean mentions divided by all mentions of you and your tracked competitors, with your rank. Use the noise audit's figures; do not recompute cleaning here.

## Step 3: Shape

- Position: how many named cells put you first, second, third or later, in a list, or as an aside.
- Per group: named and cited counts for each question group (local discovery, problem first, cost and education, choosing). A mention on a "who is near me" question is worth more than the same count elsewhere, so say which group it came from.

## Step 4: Misses by type

Classify each headline miss using only the scored columns: someone else named (a visibility gap), nobody named (a category gap), resolved to software (the answer was a tool list, not a business), or control miss (expected).

## Output

`analysis/<run>/visibility.md` (300 to 600 words): the headline counts with denominators, share and rank, the group shape, the miss breakdown, and the small-numbers caveat said once, plainly. Hedge in proportion: counts you can see are certain; why they are what they are is a hypothesis.

## Failure modes

No scored file: stop and say what is needed. No noise audit: raw only, marked not citable.

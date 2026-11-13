---
name: aeo-platforms
description: Compare how ChatGPT, Claude, Gemini, and Perplexity each treat your business in a scored run, kept separate, never blended. Shows per-product named and cited counts, how often each product lists sources at all, how they disagree, the model version each used, and where effort is likely to pay. Use when asked which AI product is friendliest or hardest, or where to focus.
---

# AEO platforms

Works in: [Claude Code](../../glossary.md#claude-code), Claude.ai, ChatGPT.

## The idea

Each product retrieves and cites differently, and one cell per question per product is a small sample. Keep every product on its own row and lean on counts and repeated patterns, not on percentages.

## What to read

The scored file (the run header's model names matter), the [noise audit](../../glossary.md#noise-audit), and the [citations](../../glossary.md#citation) result if it exists (use its per-product link and invented-link counts as they are).

## Step 1: One row per product

Effective cells (minus skipped), clean named count, raw named count, your-site-cited count, brand-check identification, how often the product listed any source at all (this changes what "no citation" means), the average number of other businesses named per answer, and how many answers resolved to software.

## Step 2: Spread

Name the range across products for each headline measure. If a product has more than a quarter of its cells skipped or unscored, call it a blind spot before drawing any conclusion about it. Name the friendliest and the hardest product by clean named count plus identification. If every count is zero, rank by stand-ins (quality of the category description, how often it lists sources, brand-check quality) and label them as stand-ins.

## Step 3: Source differences

Where products disagree on sources for the same question, name the domains each leaned on. Disagreement means each product needs its own route in. Note that a search-first product (Perplexity) usually leans on the open web more than a product answering from what it learned in training.

## Step 4: Confounds

From the run header: model name for each product, signed-in state, location, and anything off-protocol mid-run. Pin every conclusion to a version: "Gemini (as shown in the app on 11/15/2026)". A quiet default-model swap moves scores without your business moving.

## Step 5: Where to focus

Rank products by opportunity: the gap between what the product could say (it lists sources, handles local questions) and what it says about you, where a realistic route in exists. Two or three sentences per product, qualitative. Do not invent weights or scores.

## Output

`analysis/<run>/platforms.md` (300 to 600 words): the per-product table's story, spread and blind spots, friendliest and hardest with the basis, source differences, the version pin, and the focus suggestion as a hypothesis. Never add products together into one "AI score".

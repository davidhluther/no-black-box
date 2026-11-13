---
name: unified-visibility
description: Put every AI visibility source side by side in one honest report, such as your question battery, Google [Search Console](../../glossary.md#search-console), Bing Webmaster Tools, [GA4](../../glossary.md#ga4) AI traffic, and any paid platform exports you happen to have. Checks whether the sources agree in direction and explains the differences before recommending anything. Use for a quarterly summary or when different tools seem to say different things.
---

# Unified visibility

Works in: [Claude Code](../../glossary.md#claude-code), Claude.ai, ChatGPT (upload the files; no connector is needed). Paid platforms are optional and never required.

## The rule

No single tool measures AI visibility. Each sees one slice: your question battery sees what a few fixed questions return, search tools see queries typed into search engines, analytics sees visits that arrived with a clue about where they came from, and paid platforms track their own sets of questions. So the point of this skill is agreement checking: do the directions match, and when they do not, why?

## Sources (use what you have)

| Source | What it sees | How it comes in |
|---|---|---|
| Your question battery | Named, cited, or [crowded out](../../glossary.md#crowded-out), on your fixed questions | `analysis/<run>/summary.md` and the scored file |
| Google Search Console | Queries typed into Google, impressions, clicks | [CSV](../../glossary.md#csv) export, plus `ai-traffic-classifier` for leaked conversational queries |
| Bing Webmaster Tools | The same for Bing, which several AI products draw on | CSV export |
| GA4 AI traffic | Visits whose source looks like an AI product | The AI traffic [channel group](../../glossary.md#channel-group) from the kit |
| Paid AI visibility platforms (optional) | Their own [question sets](../../glossary.md#question-set) and sampled answers | Their CSV exports; the kit never requires one |

If you have no paid platform, say nothing about them. Do not list tools you are not using.

## Step 1: Inventory

For each source say what it is, the date range, and whether it is fresh (a month or less for most). A stale source is shown but flagged.

## Step 2: One table per question, not one score

Do not blend sources into a composite score or give them weights. Any weights would be invented. Build a side-by-side table: for each source, which direction it moved since the last period (up, down, flat, no data) and the plain count behind that.

## Step 3: Agreement check

- Where sources agree in direction, say so and state your confidence.
- Where they disagree, work through the usual reasons before concluding anything: different question sets, different competitors tracked, different AI products or model versions, different collection methods (apps versus [APIs](../../glossary.md#api) versus sampled panels), different dates, or different locations. Name which one applies, or say none was found.
- A change that appears in one source only is a lead, not a finding.

## Step 4: Clean numbers only

Use only battery numbers that have had `answer-noise-audit`. If a source's numbers are not noise-checked, show them as "unverified". For a paid platform, ask whether its tracked name could be confused with another business and whether its question set matches yours.

## Step 5: Recommendations

Rank by what multiple sources support. Write each as a hypothesis with a way to test it next period. Say once what this report cannot see (conversations that never produce a click or a mention you can find).

## Output

`analysis/unified-<period>.md`: inventory, the side-by-side table, the agreement check with explained differences, three to five hypotheses, and a short method and limits section. No composite score.

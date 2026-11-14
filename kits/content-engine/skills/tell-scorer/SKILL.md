---
name: tell-scorer
description: Score articles for AI-sounding habits, one number per rule. Scores a folder of markdown drafts or a whole live blog, compares before and after a writing-rule change, flags the newly inflated words and phrases a ban pushed writers toward, and can act as a pass-or-fail gate on recently published pages. Use for "score our content for AI tells", "did the writing rules improve things", "audit what just shipped", or building a rewrite list.
---

# Tell scorer

Works in: Claude Code (full version). It runs Python scripts from your own computer. Scoring live web pages also needs two add-ons installed once with `pip install requests beautifulsoup4`; scoring markdown files needs neither.

A "tell" is a habit that makes writing read as machine-made: stock words, formulaic transitions, stacked "not just X, but Y" sentences, headings in Title Case. This skill turns "does this read as AI-generated" from a feeling into a number per rule, counted per 1,000 words, so you can say which rule moved and by how much.

It scores your pages against your own rulebook (`../article-check/data/style_rules.json`, the same lists the article checker uses). One feature per rule means a change in the numbers points at one rule, not at a vague overall impression.

## What it can do

1. **Score a collection** (`scripts/score_batch.py`). One spreadsheet row per page with 28 per-rule features plus combined scores. Sources are a sitemap (the list of pages a site publishes), a list of web addresses, saved HTML files, or a folder of markdown files. Drafts and live pages share one model, so their scores compare.
2. **Compare before and after** (`scripts/cohort_compare.py`). Per-rule averages for two groups of pages with a significance test. Group by date cuts (before and after you changed a rule), by an existing column, or by two score files with `--baseline`.
3. **Gate recent pages** (`score_batch.py --thresholds`). Applies a ceiling to each feature and exits with an error when one is exceeded. Features named in the threshold file's `_warn_only` list (by default the dash and colon counts) print a warning and never fail the gate. Pair it with `--max-age-days` to audit only what was published lately. The ceilings in `gate-thresholds.default.json` are starting points: score 20 or more of your own pages, then tune each ceiling to your own writing.
4. **Find new habits** (`scripts/emergent_tics.py`). When you ban a phrase, writers reach for the nearest unbanned one. This lists words, two-word phrases and sentence openers that became more frequent in new content than in an older baseline, ranking verbal habits (spread across many pages) above subject nouns (clustered on a few). Read the list; do not auto-ban it. Separating a new topic from a new tic is your call.
5. **Benchmark a field** (`scripts/benchmark_corpus.py`). Scores competitor or peer sites with the same instrument, politely and read-only, to answer "cleaner than the category, or only cleaner than our past". It prints extraction stats per site and flags implausible word counts, so a wrong selector is visible.
6. **Check uniformity** (`scripts/uniformity.py`). Measures whether every page follows the rules and the whole site still reads as one voice. Compliance narrows variation, so compare against a peer group as a control.
7. **Rank a rewrite list.** Combine the severity (composite percentile) with an opportunity measure you hold, such as visits. Rewrite the prose and keep the headings, lists and tables. Never queue a page for stripping structure.

## Quickstart

```bash
# score the markdown finals in a folder
python3 scripts/score_batch.py --md-glob 'output/final/final_*.md' --out drafts.csv

# score a live blog (check the selector first, see below)
python3 scripts/score_batch.py \
    --sitemap https://example.org/sitemap.xml --include /blog/ \
    --selector 'article' --out scores.csv

# did a rule change help? two score files, before and after
python3 scripts/cohort_compare.py after.csv --baseline before.csv

# date cuts: pages before 06/01 are "old", the rest are "new"
python3 scripts/cohort_compare.py scores.csv --date-cuts "2026-06-01:old,:new"

# gate the last 14 days of published pages
python3 scripts/score_batch.py --sitemap https://example.org/sitemap.xml --include /blog/ \
    --max-age-days 14 --thresholds gate-thresholds.default.json
```

Dates in the scripts use `yyyy-mm-dd` because that sorts correctly.

## Your site's settings

- `--selector`: the CSS selector (a short address for a part of a web page) of the element that holds the article text. Check extraction on two or three pages before you trust a new site. A wrong selector quietly poisons every number, and "EXTRACTION PROBLEM" lines in the output mean it is wrong.
- `--canon`: defaults to the article checker's word list. Point elsewhere only if you keep a separate list.
- Thresholds: copy `gate-thresholds.default.json` into your own folder and tune it.

## Caveats to say out loud

- It counts patterns with regular expressions (text-matching rules). It does not score stacked near-synonym lists or the deeper story-level habits (stating the lesson, tidy resolution, vague allusion), so never imply the composite covers them.
- The colon-capitalization feature counts candidates, not confirmed errors.
- Boilerplate FAQ headings are left out of the heading-case score on purpose.
- The scores measure your rulebook, not what commercial AI detectors would flag. Do not use detector output to decide helped-or-harmed questions.
- A high score flags risk, not proof of machine authorship. A low score is not proof of a human writer.
- How you extract the text matters more than the instrument. Make sure link text and highlighted text survive extraction before comparing anything; scraping that drops them understates the counts.
- The heading-density and formatting counts (bold, colons, dashes) measure scannable structure as much as style. Treat them as information, never as a reason to remove structure.

## When a number goes the wrong way

After a rule change, read the improved rows next to the worsened ones. A rule that improved with a neighbor that got worse is the signature of displacement: the habit moved into a form no rule names. Name the new form, add it to the rulebook, and run the comparison again.

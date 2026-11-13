---
name: tell-scorer
description: Score writing for AI tells, rule by rule, and compare batches over time. Counts each plain-writing rule per 1,000 words for a folder of markdown drafts or a set of live web pages, compares before and after a style change, catches new verbal habits as old ones are banned, and acts as a publish gate with ceilings. Use for "how robotic does this read," "did our new writing rules help," or "check what we just published."
---

# Tell Scorer

Works in: Claude Code (full version)

This skill turns "does this read as machine-written" from a feeling into a number per rule. It scores any set of documents (markdown drafts or web pages) against the plain-writing style guide. One feature per rule, counted per 1,000 words, so a change can be traced to the rule that caused it.

It reads files and, only if you ask it to score live pages, fetches the pages you name. It does not write to your site.

## What it can do

1. **Score a set of documents.** `scripts/score_batch.py` writes one row per document, with about 28 per-rule features and a few combined scores. Sources are a folder or pattern of markdown files, a list of web addresses, saved HTML files, or a sitemap.
2. **Compare two sets.** `scripts/cohort_compare.py` reports per-rule averages and significance for before and after a rule change, or for groups you define by date. This turns "did the new rules work" into a table.
3. **Gate before publishing.** `score_batch.py --thresholds` applies a ceiling to each feature and exits with an error if a draft goes over. The formatting-density features (colons, em-dashes) only warn. Language-tell ceilings block.
4. **Find new habits.** `scripts/emergent_tics.py` lists words, pairs of words, and sentence openers whose rate went up in new writing against an older baseline. Read the list yourself. Some of the rise is new subject matter and some is a new habit, and only you can tell which.
5. **Benchmark against others.** `scripts/benchmark_corpus.py` scores other sites' public posts with the same instrument, politely and read-only, so you can see whether you are cleaner than your field or only than your past.
6. **Check for sameness.** `scripts/uniformity.py` measures how alike the voice is across a whole set of pages. It catches the failure no single-page check sees: every page passes and the whole site reads as one voice.
7. **Run it monthly.** `scripts/monthly_run.py` scores a sitemap into a dated folder and compares it with the last run, so one command each month shows drift.

## Quickstart

```bash
# Score markdown drafts
python3 scripts/score_batch.py --md-glob 'drafts/*.md' --out scores.csv

# Gate one draft before publishing (exit code 1 means a ceiling was passed)
python3 scripts/score_batch.py --md-glob draft.md --thresholds gate-thresholds.default.json --out scores.csv

# Before and after a rule change
python3 scripts/cohort_compare.py after.csv --baseline before.csv

# Score live pages from a sitemap (verify the selector first, see below)
python3 scripts/score_batch.py --sitemap https://www.example.org/sitemap.xml --include /blog/ \
    --selector 'article' --out scores.csv
```

## Setting it up for your site

- **Selector.** For live pages, `--selector` names the part of the page that holds the article text (a CSS selector, a short pattern that picks out one part of a web page). Check two or three pages before you trust a new site. A wrong selector quietly spoils every number, and the script prints an `EXTRACTION PROBLEM` line when word counts look implausible.
- **Word lists.** The script reads `data/style_rules.json` in this skill's folder, the same list the article-check skill uses. Point `--canon` at a different file for a house list.
- **Thresholds.** Copy `gate-thresholds.default.json`, then tune the numbers from your own published writing. The defaults are starting points. Do not copy another organization's ceilings.

## Limits to say out loud

- It is a pattern counter. It cannot score the structural rules (stated lessons, tidy endings, vague allusion), so never imply the total covers them.
- A high score flags risk. It is not proof a machine wrote the text. A low score is not proof a person did.
- It measures your style guide. It does not predict what a commercial AI detector would say, and detector output should not be used to judge writing quality.
- The colon feature counts candidates, not confirmed errors.
- If you supply your own page extraction, confirm that link text and highlighted text survive. Dropping them lowers the counts and hides tells.
- Banning one form tends to push writers toward its sibling. When a row improves, read the rows next to it.
- Never queue a page for "remove the formatting." Fix the sentences and keep the headings, lists, and tables.

## Related skills

plain-writing holds the rules the features come from. article-check judges one draft. copy-lint checks the finished page.

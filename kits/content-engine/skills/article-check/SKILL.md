---
name: article-check
description: Check an article draft against a writing and search-structure rulebook before it goes live. Runs a script that flags banned AI-sounding words, formulaic transitions, em-dash and colon habits, weak headings, missing links, uncited statistics, and answer-first structure, then walks you through fixing every error. Use when asked to validate, check, review, QA or finalize a blog post or article draft.
---

# Article check

Works in: Claude Code (full version). It runs a Python script from your own computer.

This skill is the quality gate between a finished draft and a published post. The script reads a markdown draft (a plain-text file that uses `#` for headings) and prints a report of errors (must fix) and warnings (fix when you can). The checks come from one shared word list, `data/style_rules.json`, which the AI-tell scorer and the copy linter read too, so the three tools never disagree.

## Before you start

- Python 3 installed (the script uses only what ships with Python).
- A draft saved as markdown, by convention in `output/drafts/`.
- Optional: a rules file for your organization. The default, `data/brand-rules/example.json`, is a worked example for a made-up site at example.org. Copy it, change the values to yours, and point the script at it (see "Your own rules" below).

## Step 1: run the checker

```bash
python3 scripts/validate_article.py output/drafts/draft_my-topic.md "my keyword"
```

The keyword is optional. Add `--site example.org` to load the rules named by that site's publish config (see the `publish` skill).

The exit code is 0 when there are no errors and 1 when there are, so a script or a scheduled job can use it as a gate.

## Step 2: read the report

The script checks these areas.

| Check | Severity | What it catches |
|---|---|---|
| Consecutive headings | Error | Subheads with no text between them |
| Heading jumps | Error | An H2 followed straight by an H3 with no introduction |
| Question headings | Warning | H2s and H3s that are not phrased as questions |
| Em-dash spacing and label dashes | Error | A bold label followed by a dash, or a dash that introduces a list |
| Forbidden phrases | Error | AI-sounding vocabulary, formulaic transitions, puffery, meta-commentary |
| Placeholder examples | Error | Invented stand-in actors ("one company") instead of a real, named case |
| Repeated statistics | Warning | The same number stated more than once |
| Uncited statistics | Warning | A figure with no named source |
| Curly quotes and emoji | Error | Smart quotes or emoji characters |
| Length | Error or warning | Below the minimum word count |
| Internal links | Error or warning | Too few unique links to your other posts, or the same link twice |
| Your own banned phrases | Warning | Patterns from the optional `compliance` block in your rules |
| Call to action | Warning | No call to action found |
| Heading count | Error | No H1 or more than one |
| Summary endings | Error | Closing paragraphs that restate what the section just said |
| Negative parallelism | Error | The "not X, but Y" shape, in one sentence or split across two |
| Heading case | Warning | Title Case in H2 or H3 (they should be sentence case) |
| Density measures | Warning | Em-dashes, colons, semicolons, bold spans, long comma lists |
| Fourth wall | Error or warning | The article talking about search engines, other articles, or its own structure |

Errors block. Warnings inform. Formatting measures (dashes, colons, bold) are warnings on purpose: they are never a reason to strip headings, lists, tables or bold from a page.

## Step 3: add the answer-first checks yourself

The script cannot judge these, so do them by reading the draft.

1. **Answer block.** Count the words in the opening paragraph. Forty or fewer passes. Forty-one to sixty is a warning. Over sixty gets rewritten. Also check that it answers the title's question instead of giving background.
2. **Question H2s.** At least 80 percent of H2s should be questions. For each one that is not, suggest a question version.
3. **Comparison table.** An article over 800 words should have at least one table of three or more rows, unless it is a single-concept definition.
4. **Organization mentions.** Search the body, everything before the closing call to action, for your own organization's name. None passes. One or two is a flag for review. Three or more, or customer stories in the body, fails.
5. **Product links.** Count links to your product pages and your own other posts, and compare with the targets in your rules file.
6. **FAQ section.** Five or more question-and-answer pairs passes.
7. **Answer-first sentences.** Under each question heading the first sentence should answer it. Stock throat-clearing openers are warnings.

## Step 4: fix and re-run

1. Read each error message.
2. Open the draft and fix every flagged line.
3. Save and run the checker again.
4. Repeat until no errors remain. Fix warnings when you can.

## Step 5: verify links

Open each internal link in a browser (or ask your AI model to fetch it) and confirm it loads. Remove any that do not resolve.

## Step 6: finalize

Save the passing draft to `output/final/final_my-topic.md` and report the title, keyword, word count, number of H2s and H3s, internal link count, cited statistic count, and "validation passed".

## Your own rules

Everything shaped by one organization lives in a rules file, never in the script. The default file shows every key.

| Key | What it controls |
|---|---|
| `internal_links` | Address patterns that count as your own posts, the minimum number of unique links, and an optional escalation |
| `product_link_placement` | Address patterns for product pages that belong only in the upsell section or a call to action |
| `upsell` | Product addresses and heading patterns that mark the upsell section, plus your organization's name (`label`) |
| `cta_patterns` | Phrases that count as a call to action |
| `compliance` | Your own banned phrases: a list of `{"pattern": "regex", "message": "why"}` pairs, reported as warnings |
| `faq_schema_match` | When true, the FAQ markup in the draft must match the visible FAQ questions and their answers |
| `structure` | Turn on `metadata_table` or `key_takeaways` if your posts need them |

Empty lists switch a check off. An unknown key stops the run on purpose, so a typo can never quietly disable a check.

Ways to supply a file, strongest last: the default example, `--site <id>` (the site's publish config names a file in `checks.brand_rules`), then a `guidelines/VALIDATOR_BRAND_RULES.json` found by walking up from the draft, or the path in the `SEO_VALIDATE_BRAND_RULES` environment variable.

## Adding your own banned words

Open `data/style_rules.json` and add forms to the `restricted_words` block. Each entry is keyed by the plain word and lists the exact forms to flag, so you can ban a jargon verb while leaving its harmless noun sense alone (the shipped list does this for one common verb). The AI-tell scorer and the copy linter pick the change up with no other edit.

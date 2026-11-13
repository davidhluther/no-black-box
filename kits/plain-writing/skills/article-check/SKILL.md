---
name: article-check
description: Check a written draft (markdown) against plain-writing rules with a Python script. Flags banned vocabulary, filler openers and transitions, copycat sentence shapes, em-dash and colon habits, heading case, curly quotes, emojis, repeated statistics, and uncited numbers, with optional blog checks (internal links, FAQ, calls to action). Use when asked to validate, check, QA, or proof an article, post, memo, or page before publishing.
---

# Article Check

Works in: Claude Code (full version). The same word lists work without a program through the free paste-in prompts in the kit's `free/` folder.

This skill runs one Python script over a markdown draft and prints a pass or fail report. It reads files and prints text. It never changes your draft and never uses the internet.

## Run it

For any piece of writing (memo, newsletter, grant text, page copy), use prose mode. It skips blog-structure checks and checks the writing only:

```bash
python3 scripts/validate_article.py draft.md --prose
```

For a blog post that should also have internal links, a call to action, and an FAQ, run it without `--prose`, and give it your own house rules file so those checks fit your site:

```bash
python3 scripts/validate_article.py post.md "target phrase" --brand-rules my-rules.json
```

The optional second argument is the phrase the post is about; the script checks that it appears in the title and opening.

The script exits with 0 when no errors were found and 1 when errors remain. Warnings never fail a run.

## What it checks

| Check | Severity | What it catches |
|---|---|---|
| Heading structure | error | Two headings in a row, a jump from H2 to H3 with no text between |
| Heading case | error | Title case in H2 or H3 headings |
| Forbidden phrases | error | Filler openers, formulaic transitions, meta-commentary, time clichés |
| Banned vocabulary | error | The Tier 1 word list and the restricted list in `data/style_rules.json` |
| Terminology | error | "AI assistant" where "AI model" is meant |
| Placeholder examples | error | "One company..." style invented actors |
| Em-dash label and series intros | error | A bold label followed by a dash, a dash introducing a list |
| Curly quotes and emojis | error | Anything other than straight quotes, any emoji |
| Summary endings | error | "In conclusion" style wrap-ups |
| Negative parallelism | warning | More than one "not just X, but Y" shape, in-sentence or across two sentences |
| Repeated statistics | warning | The same figure stated more than once |
| Uncited statistics | warning | A figure with no named source |
| Colons, em-dashes, semicolons | warning | Counts over the style guide's limits |
| Paragraph length, anaphora, comma lists | warning | Runs the style guide limits |
| Fourth-wall phrases | error or warning | Search-industry jargon in the body (SERP, AEO, "citation slot"), defensive "we don't offer" disclaimers, table-stakes credential claims, winking at the reader as a marketer |

Without `--prose`, it also checks word count, the target phrase, internal links, FAQ presence, and calls to action. These suit a blog post and are noise for everything else. A site whose posts all start with a metadata table and a Key Takeaways box can turn on those two checks with `cms_template_checks` in its rules file.

## Fix loop

1. Run the script.
2. Fix every error by rewriting the sentence. Do not delete headings, lists, tables, or bold to quiet a count.
3. Run it again. Repeat until no errors remain.
4. Read the warnings. Fix those that point at a real weakness. A warning is a prompt to look, and sometimes the right answer is to leave it.
5. Verify every link and every number by hand. The script cannot tell you a statistic is true.

## House rules

All organization-specific values (which links count as internal, which phrases count as a call to action, which pages are product pages) live in one small JSON file. See `data/brand-rules/example.json` for every key, with `example.org` placeholder values. Copy it, change the values, and pass it with `--brand-rules`. Set a list to `[]` to switch that check off. The script refuses to run with an unknown key, so a typo cannot silently turn a check off.

To add or remove banned words, edit `data/style_rules.json`. Each block names its own severity.

## Settings

Read the rules file path from `brand_rules_file` in `config.json` (copied from `config.example.json`) or ask the user. Never write your own rules into a file without showing the user first.

## Related skills

plain-writing holds the full style guide these checks come from. tell-scorer measures tell density across many pages. copy-lint checks the finished web page rather than the draft.

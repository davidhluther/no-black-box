---
name: copy-lint
description: Check the words that actually ship on a website or app (page text, titles, link labels, navigation, table cells, markdown, JSX or TSX components) against plain-writing rules. Catches lowercase-after-colon errors, em-dashes in interface copy, banned vocabulary, wrong case in menus and tables, words that run together in templates, and straight quotes in rendered text. Use before shipping site or app copy, or in a pre-commit check.
---

# Copy Lint

Works in: Claude Code (full version)

A draft checker (article-check) reads a markdown draft before publishing. It never sees a page title, a button label, a menu, or a text element inside a web template, and that is where the mistakes keep hiding. copy-lint reads the finished files and checks the text a visitor actually sees.

It reads files and prints findings. It never edits them.

## Run it

```bash
python3 scripts/copy_lint.py path/to/site        # files or folders to check
python3 scripts/copy_lint.py --explain           # which rules are on and which settings were used
python3 scripts/copy_lint.py --dump page.tsx     # every string the program could see
python3 scripts/copy_lint.py --json src          # findings as data
```

Exit code 0 means clean. Exit code 1 means errors. Exit code 2 means the program could not run. Warnings never fail a run unless you add `--warnings-as-errors`. When a rule seems to miss something, run `--dump` first. Most of the time the string was never picked up.

## Rules

Errors are only the clear mechanical cases. Judgment calls are warnings, because a checker that forces bad rewrites gets turned off.

| Code | Severity | What it catches |
|---|---|---|
| COLON_SENTENCE | error | A complete sentence in lowercase after a colon |
| COLON_LABEL | error | A lowercase "label: value" pattern in text or a list |
| COLON_SKELETON | warning | The same pattern with a capital label |
| COLON_FRAGMENT | warning | Any other lowercase after a colon, correct only for a real fragment or list |
| COLON_BUDGET | warning | More colons in one file than the budget allows |
| EMDASH | error | An em-dash in interface copy |
| EMDASH_DENSITY | warning | Markdown over about one em-dash per 200 words |
| SEMI_DENSITY | warning | Markdown over about one semicolon per 500 words |
| COMMA_SERIES | warning | A series of three or more with no closing "and" or "or" |
| STAT_REPEAT | warning | The same figure stated twice in one file |
| NAV_CASE | error | A declared set of menu labels that is not consistently title case |
| CELL_CASE | error | A table cell that starts in lowercase |
| CAPTION_CASE | error | A caption or stand-alone label that starts in lowercase |
| JSX_SPACING | error | Words that run together at an element boundary in a JSX template |
| JSX_QUOTES | error | Straight quotes inside rendered JSX text, which no build step converts |
| VOCAB | error | Every error-level word block in `data/style_rules.json`, so a new banned word works without a code change |

## Settings for your project

Put settings in `guidelines/COPY_LINT_PARAMS.json` or `.copy-lint.json` in your project. The program looks up the folder tree for either file. No file is fine. It then checks the paths you pass with the defaults. An unknown key stops the run, so a typo cannot quietly drop a rule.

```json
{
  "targets": ["src/app", "src/content"],
  "exclude_dirs": ["node_modules", "__tests__"],
  "suffixes": [".tsx", ".md"],
  "nav_label_sets": [{ "file": "src/components/Header.tsx", "array": "primary" }],
  "allow": ["COLON_FRAGMENT::reviewed phrase"],
  "skip": [],
  "extra_determiners": ["maria's"],
  "colon_budget": 3,
  "guidance_doc": "house-style.md"
}
```

- `allow` lists reviewed exceptions. Write a bare phrase, or `CODE::phrase` to limit it to one rule. Use it for a published name you must quote exactly.
- `skip` takes rule codes or groups: `colon`, `case`, `emdash`, `density`, `series`, `stats`, `vocab`, `jsx`.
- `extra_determiners` lists possessives such as an owner's name, so a real sentence is not mistaken for a fragment.
- `vocab_blocks` names which word blocks to enforce. The default is every error-level block.
- `style_rules_path` or the `COPY_LINT_STYLE_RULES` environment variable points at your own word list. Without either, the program reads `data/style_rules.json` here, then the article-check skill's copy.

## The template gotcha

In some JSX builds, a text element that holds an HTML entity (like `&ndash;`) and wraps across source lines loses the space in front of it at build time. "range is scored" ships as "rangeis scored." The draft looks right, review misses it, and only the built page shows it. The fix is an explicit `{" "}` at the break. copy-lint reports this as JSX_SPACING.

## Adding another file type

The rules do not care about file type. A small plug-in module per type turns a file into pieces of text with a role (prose, heading, label, list item, table cell, data). Two ship today, `nextjs` and `markdown`. A new type lives in `scripts/copylint/` and is registered in `copylint/__init__.py`.

## Related skills

article-check judges a draft. plain-writing holds the rules. tell-scorer measures a whole set of pages.

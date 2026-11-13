---
name: copy-lint
description: Check the words your website actually shows, not just blog drafts. Scans page code and markdown for banned words, em-dashes in interface text, lowercase sentences after colons, headings and menu labels in the wrong case, straight quotes that will show wrongly, and words that run together where code wraps a line. Use before shipping a website change, when copy in menus, buttons, captions or titles needs the same rules as the blog, or when a reviewer keeps finding the same slips on the live site.
---

# Copy lint

Works in: Claude Code (full version). It runs a Python script from your own computer.

The article checker judges a markdown draft before publication. It never sees a page title, a button label, an image description, a menu item, or a line of page code, and those are the places where slips keep surviving review. This skill lints the artifact a reader receives. Run the article checker on drafts and this on the built site.

Both read the same word list in `../article-check/data/style_rules.json`, so a word you add there is enforced in both places. If that file is missing, the linter stops with instructions instead of quietly using an old copy.

## Run it

```bash
python3 scripts/copy_lint.py              # the targets named in your config
python3 scripts/copy_lint.py src/app      # specific files or folders
python3 scripts/copy_lint.py --dump       # show every string the linter can see
python3 scripts/copy_lint.py --explain    # show the settings in use and which rules are live
python3 scripts/copy_lint.py --json       # results in a machine-readable form
```

Exit code 0 means clean, 1 means errors were found, 2 means the linter could not run. Warnings never fail a run unless you add `--warnings-as-errors`. When a rule seems to miss something, run `--dump` first: nine times in ten the string was never extracted.

## What it reports

Errors are only the clear mechanical cases. Every judgment call is a warning, because a linter that forces bad rewrites gets switched off.

| Code | Severity | What it catches |
|---|---|---|
| `COLON_SENTENCE` | Error | A lowercase complete sentence after a colon inside a sentence |
| `COLON_LABEL` | Error | A lowercase "label: value" skeleton |
| `COLON_FRAGMENT`, `COLON_SKELETON`, `COLON_BUDGET` | Warning | Review queue for other colons, and too many colons in one file |
| `EMDASH` | Error | An em-dash in interface text |
| `EMDASH_DENSITY`, `SEMI_DENSITY` | Warning | Dashes or semicolons over the allowed rate in long markdown |
| `COMMA_SERIES` | Warning | A series of three or more items with no closing "and" or "or" |
| `STAT_REPEAT` | Warning | The same full statistic stated twice in one file |
| `NAV_CASE`, `CELL_CASE`, `CAPTION_CASE` | Error | Menu labels, table cells or captions in the wrong case |
| `JSX_SPACING` | Error | Words that run together where an HTML entity and a line wrap meet |
| `JSX_QUOTES` | Error | Straight quotes in page text that nothing will convert |
| `VOCAB` | Error | Banned vocabulary, puffery and formulaic transitions from the shared word list. URLs are skipped; link text is still scanned |

The spacing slip is worth knowing. In React-style page code (JSX), a text node that holds an HTML entity and also wraps across two source lines loses its leading space when the site is built, so "range is scored" ships as "rangeis scored". The source looks fine and review misses it. The fix is an explicit `{" "}` at the join.

## Your settings

The linter reads the nearest `guidelines/COPY_LINT_PARAMS.json` or `.copy-lint.json`, walking up from the folder you run it in. No config is fine: it lints the paths you give it with defaults. An unrecognized key is fatal on purpose, so a typo can never silently drop an exemption or a rule. Environment variables: `COPY_LINT_PARAMS` (config path), `COPY_LINT_SKIP` (rule codes or groups to skip), `COPY_LINT_STYLE_RULES` (path to the word list).

The full key list (targets, folders to exclude, menu label sets, reviewed exemptions, rule groups to skip, colon budget) is in `README.md` beside this file, along with the plug-in layout for adding another page format.

## Heuristics stay conservative

"Is this clause a complete sentence?" is decided from helper verbs, subject pronouns and command forms, with guards for lists and noun phrases. When in doubt the linter says "not a sentence", which demotes a finding to a warning instead of inventing an error.

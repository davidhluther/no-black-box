# copy-lint — the styleguide gate on shipped copy

Mechanical styleguide enforcement for the copy a reader actually receives: JSX
text nodes, metadata titles, aria-labels, table cells, nav labels, shipped
markdown. Built after a site's own script found 156 violations in a tree that had passed
months of human review.

**The gap it closes.** `article-check/scripts/validate_article.py` judges a
markdown *draft* before publication. It never sees a metadata title, an
aria-label, a nav label, or a JSX text node — which is exactly where the
violations kept living, and why the owner kept catching them by reading the
live site. The two are complements, not alternatives: run the validator on
drafts, run this on the built artifact. They overlap only on vocabulary, where
they read the same canonical word list.

## The four design pillars

Change these and it stops working. Each was paid for.

1. **Lint the shipped artifact, not the draft.** The extraction layer's whole
   job is to see what the reader sees. A rule that only runs on prose in a
   `.md` file cannot catch a lowercase stat caption in a React component.
2. **Read the canonical word lists, never fork them.** Terms come from
   `../article-check/data/style_rules.json` — the same JSON the validator
   consumes — and a missing file is a hard exit with instructions, never a
   quiet fallback to a stale inline copy. A silent fallback to an inline copy
   would be a fork with extra steps.
3. **Severity is the design.** Errors are only the unambiguous mechanical
   cases: a lowercase *complete sentence* after a colon, a lowercase label
   skeleton, an em-dash in UI copy, a case outlier in a sibling set. Every
   judgment call — a lowercase fragment after a colon, the per-file colon
   budget, em-dash density in long-form markdown — is a warning. A linter that
   forces bad rewrites gets switched off, and a switched-off linter enforces
   nothing.
4. **Heuristics need a conservative bar.** "Is this clause a complete
   sentence?" is decided by auxiliary-verb, subject-pronoun, and imperative
   tests, with guards for enumerations, dependent openers, and noun phrases
   carrying a relative clause — tuned against real copy until the error tier
   had no false positives. When in doubt the heuristics return "not a
   sentence," which demotes a finding to a warning rather than inventing an
   error.

## Rules

| Code | Severity | What it catches |
|---|---|---|
| `COLON_SENTENCE` | error | Lowercase complete sentence after a sentence-internal colon (AP; styleguide Tier 4 "Colon discipline") |
| `COLON_LABEL` | error | Lowercase `label: value` skeleton in prose or a list item ("calm: 0–1 mph") |
| `COLON_SKELETON` | warn | The same skeleton with a capitalized label |
| `COLON_FRAGMENT` | warn | Any other lowercase-after-colon in prose — correct for a genuine fragment, so it's a review queue |
| `COLON_BUDGET` | warn | More than `colon_budget` sentence-internal colons in one file's body prose |
| `EMDASH` | error | Em-dash in a user-facing string (empty-cell placeholders exempt) |
| `EMDASH_DENSITY` | warn | Shipped markdown over the universal 1-per-200-words ceiling |
| `SEMI_DENSITY` | warn | Shipped markdown over the universal 1-per-500-words semicolon ceiling (entity semicolons in `&rsquo;`/`&rdquo;` excluded) |
| `COMMA_SERIES` | warn | A series of three or more items with no closing `and`/`or` (owner rule, 2026-07-08) |
| `STAT_REPEAT` | warn | The same full statistic stated twice in one file (styleguide Tier 1); table cells and data exempt |
| `NAV_CASE` | error | A declared nav/category label set that isn't uniformly Title Case |
| `CELL_CASE` | error | A table cell whose text starts lowercase |
| `CAPTION_CASE` | error | A stat caption or standalone label that starts lowercase |
| `JSX_SPACING` | error | Words that run together at an element boundary (see the entity gotcha below) |
| `JSX_QUOTES` | error | Straight quotes in rendered JSX text — nothing in a JSX pipeline converts them |
| `VOCAB` | error | Tier 1 vocabulary, puffery, formulaic transitions, and terminology from the canonical lists — every `_severity: error` block, so an owner rule added to `style_rules.json` is live with no code change (that is how the 2026-08-24 "AI models, never AI assistants" rule arrived). URL targets are stripped first; anchor text is still scanned |

### The JSX entity/whitespace gotcha

A JSX text node that carries an HTML entity **and** wraps across source lines
silently loses its leading space in Next 16 / SWC, so this source:

```jsx
<em>range</em> is scored at its midpoint, then taxed for vagueness. A
5&ndash;15 mph range scores lower.
```

ships as "rangeis scored". A single-line node keeps its space, so the bug is
invisible in review and invisible in the source — it only shows up in a
production build. The fix is an explicit `{" "}` at that boundary. Verified
against a production build 2026-07-28; also recorded in the universal
styleguide's Tier 4 mechanics.

## Usage

```bash
python3 scripts/copy_lint.py              # the configured targets
python3 scripts/copy_lint.py src/app      # specific files or dirs
python3 scripts/copy_lint.py --dump       # every string the extractor can see
python3 scripts/copy_lint.py --explain    # resolved config + which rules are live
python3 scripts/copy_lint.py --json       # machine-readable findings
```

Exit status: `0` clean, `1` errors found, `2` the linter could not run. Warnings
never fail a run unless `--warnings-as-errors` is passed. `--dump` is the first
thing to reach for when a rule seems to be missing something: nine times in ten
the string was never extracted.

Environment: `COPY_LINT_PARAMS` (config path), `COPY_LINT_SKIP` (comma list of
rule codes or groups), `COPY_LINT_STYLE_RULES` (path to `style_rules.json`).

## Consumer config

Project values live in the consuming repo, never in this tree — same contract
as the rest of `shared-skills/seo/`. The linter reads the nearest
`guidelines/COPY_LINT_PARAMS.json` or `.copy-lint.json`, walking up from the
working directory. **No config is legal** (the linter then lints the paths you
give it with shared defaults), but an unrecognized key is fatal: a typo'd key
would silently drop an allowlist or a rule skip and the run would still look
clean. Same rule the article checker uses for `VALIDATOR_BRAND_RULES.json`.

```json
{
  "framework": "auto",
  "targets": ["src/app", "src/components", "src/content/posts"],
  "exclude_dirs": ["src/lib", "src/components/ui", "__tests__"],
  "exclude_names": ["unapproved-draft.md"],
  "suffixes": [".ts", ".tsx", ".md"],
  "nav_label_sets": [
    { "file": "src/components/SiteHeader.tsx", "array": "primary" },
    { "file": "src/content/resources.ts", "array": "CATEGORIES", "key": "label" }
  ],
  "allow": ["COLON_FRAGMENT::hands back every field"],
  "skip": ["colon"],
  "extra_determiners": ["sam's"],
  "vocab_blocks": ["tier1_vocab", "puffery", "transitions"],
  "colon_budget": 3,
  "guidance_doc": "guidelines/seo/WRITING_QUALITY.md",
  "root": "..",
  "style_rules_path": ""
}
```

| Key | What it does |
|---|---|
| `framework` | `auto` (dispatch by file extension) or a plugin name — `nextjs`, `markdown` |
| `targets` | Default paths to sweep, relative to the repo root |
| `exclude_dirs` / `exclude_names` | Machinery, vendored code, fixtures, unapproved drafts |
| `suffixes` | Which extensions are copy files at all |
| `nav_label_sets` | Named arrays checked for Title Case agreement; a renamed array is a loud error, not a skipped check |
| `allow` | Reviewed exemptions — also the mechanism for a source-defined cohort label a ban would otherwise force you to paraphrase (`"VOCAB::Best-in-Class"` keeps a source's published tier name citable). Written as a bare substring, or `CODE::substring` to scope it to one rule. Substring, not regex, because a bad regex here fails open on everything |
| `skip` | Rule codes or groups (`colon`, `case`, `emdash`, `density`, `series`, `stats`, `vocab`, `jsx`) |
| `extra_determiners` | Project possessives ("sam's") — without them a real AP violation reads as a fragment and slips through |
| `vocab_blocks` | Which `style_rules.json` blocks to enforce; default is every `error`-severity block. Name blocks explicitly to drop `restricted_words`, which is a brand layer rather than a universal rule |
| `colon_budget` | Sentence-internal colons per file before `COLON_BUDGET` warns |
| `guidance_doc` | Printed in the failure footer — point it at the project's own writing-quality file |
| `root` | Repo root, if it can't be inferred from where the config lives (a config held outside the tree, e.g. in CI) |
| `style_rules_path` | Override the canonical word lists' location |

## The pluggable extraction layer

The rule engine is framework-agnostic; the extraction is not, and that seam is
the point. A plugin turns a file into `Snippet`s — text plus a `role` (`prose`,
`heading`, `label`, `list_item`, `cell`, `data`) and a few structural flags —
and after that the shared rules never see markup again.

`scripts/copylint/<name>.py` exposes:

```python
SUFFIXES: frozenset[str]                     # extensions it claims
extract(rel, src, cfg) -> list[Snippet]      # required
snippet_rules(snips, cfg) -> list[Finding]   # optional: framework mechanics
file_rules(rel, src, cfg) -> list[Finding]   # optional: whole-file checks
```

Register it in `_MODULES` in `copylint/__init__.py`. Shipping today: `nextjs`
(`.ts/.tsx/.js/.jsx`) and `markdown` (`.md/.mdx`). Astro, Vue, Django/Jinja
templates, and plain HTML all fit the same shape.

Put a rule in a plugin **only** when it is genuinely about that framework's
rendering — `JSX_SPACING` and `JSX_QUOTES` qualify, because markdown's renderer
handles both on its own. Everything decidable from a `Snippet` belongs in the
engine, so every framework inherits it.

## Where it fits

Run the article checker on drafts and this linter on the built site. Both read the same word lists in `../article-check/data/style_rules.json`, so a word you add there is enforced in both places. A few older rules (negative-parallelism shapes, formulaic openers, markdown heading case) live in the article checker only, so keep running both.

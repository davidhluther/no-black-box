#!/usr/bin/env python3
"""Copy lint - mechanical styleguide enforcement for SHIPPED copy.

Why this exists: the writing styleguide's rules held only as prose, and prose-only
rules demonstrably don't hold. The styleguide's 2026-07-18 changelog asks every
project to adopt a mechanical copy check; this is the shared implementation,
generalized from a site's own script after it caught 156 violations on a tree
that had passed months of human review.

It lints the artifact a reader actually receives - JSX text nodes, metadata
titles, aria-labels, shipped markdown - which is the gap the draft-stage
validator cannot cover: the article checker's `validate_article.py` judges a markdown draft before
publication and never sees any of those surfaces, and that is exactly where the
violations lived.

  COLON_SENTENCE  error  lowercase complete sentence after a sentence-internal colon
                         (AP violation; styleguide Tier 4 "Colon discipline")
  COLON_LABEL     error  lowercase "label: value" skeleton in prose or a list item
  COLON_SKELETON  warn   the same skeleton with a capitalized label
  COLON_FRAGMENT  warn   any other lowercase-after-colon in prose (flagged for review)
  COLON_BUDGET    warn   more than `colon_budget` sentence-internal colons per file
  EMDASH          error  em-dash in a user-facing string (empty-cell placeholders exempt)
  EMDASH_DENSITY  warn   markdown over the universal 1-per-200-words ceiling
  SEMI_DENSITY    warn   markdown over the universal 1-per-500-words semicolon ceiling
  COMMA_SERIES    warn   a series of three or more items with no closing conjunction
  STAT_REPEAT     warn   the same full statistic repeated inside one file
  NAV_CASE        error  a nav/category label set that isn't uniformly Title Case
  CELL_CASE       error  a table cell whose text starts lowercase
  CAPTION_CASE    error  a stat caption or standalone label that starts lowercase
  JSX_SPACING     error  words that run together at an element boundary
  JSX_QUOTES      error  straight quotes in rendered JSX text (nothing converts them)
  VOCAB           error  Tier 1 banned vocabulary, puffery, or formulaic transitions

Severity is the design. Errors are the unambiguous mechanical cases; every
judgment call is a warning, because a linter that forces bad rewrites gets
switched off, and a switched-off linter enforces nothing.

Word lists are NOT duplicated here. They are read from the canonical shared file
(article-check/data/style_rules.json, the same JSON validate_article.py consumes);
a missing file is a loud failure, never a fork.

Usage:
    python3 copy_lint.py                  # this repo's configured targets
    python3 copy_lint.py PATH...          # lint specific files or dirs
    python3 copy_lint.py --dump           # print every extracted string
    python3 copy_lint.py --json           # machine-readable findings
    python3 copy_lint.py --explain        # show resolved config and rule status

Environment:
    COPY_LINT_PARAMS        path to the consumer config (default: nearest
                            guidelines/COPY_LINT_PARAMS.json or .copy-lint.json)
    COPY_LINT_SKIP          comma list of rule codes or groups to skip
    COPY_LINT_STYLE_RULES   path to style_rules.json

Exit status: 0 clean, 1 violations found, 2 the linter could not run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from copylint import (  # noqa: E402
    Config, ConfigError, Finding, Snippet, get_extractor, line_at, load_config,
    words,
)

SKILL_ROOT = Path(__file__).resolve().parent.parent

# Canonical, shared word lists. This linter never carries its own copy, so the
# lists cannot drift from the article checker's. It reads the sibling skill's
# file and fails loudly if it moved.
STYLE_RULES_CANDIDATES = (
    SKILL_ROOT.parent / "article-check/data/style_rules.json",
)


# ---------------------------------------------------------------------------
# Shared style rules
# ---------------------------------------------------------------------------


def style_rules_path(cfg: Config | None = None) -> Path:
    env = os.environ.get("COPY_LINT_STYLE_RULES")
    if env:
        return Path(env).expanduser()
    if cfg is not None and cfg.style_rules_path:
        return Path(cfg.style_rules_path).expanduser()
    for candidate in STYLE_RULES_CANDIDATES:
        if candidate.exists():
            return candidate
    return STYLE_RULES_CANDIDATES[0]


def load_style_rules(path: Path | None = None, cfg: Config | None = None) -> dict:
    """Load the canonical shared word lists. Loud failure if they're missing."""
    path = path or style_rules_path(cfg)
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(
            f"FATAL: cannot read the canonical style rules at {path}: {exc}\n"
            "copy_lint.py deliberately does not carry its own copy of the word "
            "lists, so the two tools cannot drift apart.\n"
            "Make sure the article-check skill is installed beside this one, or point "
            "COPY_LINT_STYLE_RULES at style_rules.json."
        ) from exc


def banned_terms(rules: dict, blocks: tuple[str, ...] = ()) -> list[tuple[str, str]]:
    """(term, category) pairs to enforce as errors.

    Default is every block the shared rules mark `_severity: error`. A consumer
    can name blocks explicitly with `vocab_blocks` - notably to drop
    `restricted_words`, which is a brand layer rather than a universal rule.
    """
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for key, block in rules.items():
        if not isinstance(block, dict):
            continue
        if blocks:
            if key not in blocks:
                continue
        elif block.get("_severity") != "error":
            continue
        category = block.get("_category", key.upper())
        word_list = block.get("words", [])
        forms = (
            word_list.values() if isinstance(word_list, dict)
            else [{"forms": [w]} for w in word_list]
        )
        for spec in forms:
            for form in spec.get("forms", []):
                low = form.lower()
                if low not in seen:
                    seen.add(low)
                    out.append((low, category))
    if blocks:
        missing = [b for b in blocks if b not in rules]
        if missing:
            raise ConfigError(
                f"FATAL: vocab_blocks names block(s) not in style_rules.json: "
                f"{', '.join(missing)}. Available: {', '.join(k for k in rules if isinstance(rules[k], dict))}"
            )
    return out


# ---------------------------------------------------------------------------
# Sentence heuristics
#
# These decide whether the error tier fires, so they are deliberately
# conservative. Every widening below was measured against a real tree until the
# error tier had no false positives; a permissive version of this is worse than
# no rule at all, because the first bad rewrite it forces is the last day
# anyone runs it.
# ---------------------------------------------------------------------------

EM_DASH = "—"
_PLACEHOLDER = re.compile(r"^[\s—–(){}\[\]/|,.'\"°%$#*+-]*$")

# Finite-verb markers. If one of these turns up in the clause after a colon, the
# clause stands as a sentence and AP requires a capital.
_AUX = {
    "is", "are", "was", "were", "be", "been", "being", "am", "has", "have", "had",
    "does", "do", "did", "can", "cannot", "will", "would", "should", "could",
    "must", "may", "might", "shall", "isn't", "aren't", "wasn't", "weren't",
    "doesn't", "don't", "didn't", "hasn't", "haven't", "won't", "can't",
    "couldn't", "shouldn't", "wouldn't", "it's", "they're", "we're", "you're",
    "there's", "that's", "he's", "she's", "who's", "let's",
}
_SUBJECT_PRONOUNS = {
    "it", "they", "we", "he", "she", "you", "i", "this", "that", "these", "those",
    "there", "who", "nobody", "everybody", "anyone", "someone", "everything",
    "nothing", "one",
}
# Common finite verbs. Not a grammar; a working list that catches the
# "verb-led clause with no auxiliary" case ("it prices the fields").
_FINITE_VERBS = {
    "adds", "applies", "beats", "becomes", "begins", "belongs", "buys", "calls",
    "carries", "changes", "clears", "comes", "costs", "counts", "covers", "cuts",
    "drops", "earns", "ends", "falls", "feels", "finds", "follows", "forfeits",
    "gets", "gives", "goes", "grades", "hands", "happens", "helps", "hits",
    "holds", "includes", "keeps", "knows", "lands", "leads", "leaves", "lets",
    "lists", "lives", "looks", "loses", "makes", "matters", "means", "measures",
    "moves", "needs", "opens", "pays", "picks", "prices", "publishes", "puts",
    "ranks", "reaches", "reads", "requires", "rises", "runs", "says", "scores",
    "sees", "sends", "shows", "sits", "sorts", "splits", "stands", "starts",
    "stays", "stops", "takes", "tells", "tracks", "turns", "uses", "wants",
    "wins", "works",
}
_DETERMINERS = {
    "the", "a", "an", "this", "that", "these", "those", "his", "her", "its",
    "our", "your", "their", "my", "no", "none", "every", "each", "some", "any",
    "all", "both", "most", "many", "few", "several", "another", "one", "two",
}
_PREPOSITIONS = {
    "of", "in", "on", "for", "with", "from", "at", "by", "to", "about",
    "between", "across", "under", "over", "into", "than", "like", "per",
    "against", "around", "near", "during", "through", "within", "past",
}
# A clause opening with one of these is dependent ("how each forecaster did"),
# not a sentence - unless a main clause follows it after a comma.
_SUBORDINATORS = {
    "how", "what", "when", "where", "why", "which", "whether", "if", "because",
    "while", "although", "though", "unless", "until", "since", "after",
    "before", "that", "whose", "whom", "as", "so",
}
_RELATIVIZERS = {"that", "which", "who", "whose", "whom"}
# An opening bare verb is an imperative, and the styleguide names imperatives
# explicitly: they take a capital after a colon like any other sentence.
_IMPERATIVE_OPENERS = {
    "add", "avoid", "bring", "build", "capture", "check", "choose", "click",
    "compare", "consider", "download", "drive", "expect", "find", "follow",
    "get", "give", "go", "grade", "head", "keep", "know", "leave", "look",
    "make", "note", "open", "pack", "pick", "plan", "predict", "print", "put",
    "read", "remember", "save", "see", "send", "set", "skip", "stay",
    "stop", "take", "tap", "tell", "treat", "try", "turn", "use", "visit",
    "wait", "watch", "wear", "write",
}
# What can legitimately follow an imperative verb. Without this, a noun compound
# ("start times, computed") reads as a command.
_IMPERATIVE_FOLLOWERS = _DETERMINERS | _PREPOSITIONS | {
    "it", "them", "us", "you", "me", "your", "how", "what", "when", "where",
    "why", "again", "here", "there", "back", "out", "up", "down", "not",
}
_COLON_SKIP = re.compile(r"\d\s*:\s*\d|https?:|mailto:")


def _determiners(cfg: Config | None) -> set[str]:
    """Project possessives ("sam's", "pat's") read as determiners.

    Without them, "sam's forecast beats the model" scores as a fragment and a
    real AP violation goes unflagged. They're config because they're names.
    """
    return _DETERMINERS | set(cfg.extra_determiners) if cfg else _DETERMINERS


def _is_enumeration(clause: str, cfg: Config | None = None) -> bool:
    """A list of items ("slugs, names, coordinates") rather than a clause.

    Two or more commas whose first item doesn't stand alone as a sentence. AP
    keeps enumerations lowercase after a colon, so these are never errors.
    """
    head = re.split(r"(?<=[.!?])\s", clause)[0]
    if head.count(",") < 2:
        return False
    first_item = head.split(",")[0]
    return not _clause_is_sentence(first_item, allow_enumeration=False, cfg=cfg)


def _has_finite_core(word_list: list[str], cfg: Config | None = None) -> bool:
    """Subject + finite verb, as far as a word list can tell.

    Deliberately conservative, because the error tier has to be trustworthy:
    - a finite verb only counts when something follows it, since the same tokens
      double as plural nouns in final position ("daily accuracy scores for Smithtown");
    - it needs exactly one free determiner ahead of it, so a noun phrase carrying
      a relative clause ("the minute the ridgeline takes the sun off") reads as
      the fragment it is, while "the credibility of the comparison depends on X"
      (second determiner governed by a preposition) still reads as a sentence;
    - an auxiliary right after a relativizer is a relative clause, not a main verb.
    """
    determiners = _determiners(cfg)
    if len(word_list) < 2:
        return False
    if word_list[0] in _IMPERATIVE_OPENERS and word_list[1] in _IMPERATIVE_FOLLOWERS:
        return True
    if len(word_list) < 3:
        return False
    window = word_list[:14]
    for i, word in enumerate(window[:-1]):
        if word in _AUX and (i == 0 or window[i - 1] not in _RELATIVIZERS):
            return True
    if word_list[0] in _SUBJECT_PRONOUNS:
        return True
    free_dets = [
        i
        for i, w in enumerate(window)
        if w in determiners and (i == 0 or window[i - 1] not in _PREPOSITIONS)
    ]
    for i, word in enumerate(window[:-1]):
        if word in _FINITE_VERBS and len([d for d in free_dets if d < i]) == 1:
            return True
    return False


def _clause_is_sentence(clause: str, allow_enumeration: bool = True,
                        cfg: Config | None = None) -> bool:
    """Heuristic: does this clause stand as a complete sentence?"""
    if allow_enumeration and _is_enumeration(clause, cfg):
        return False
    head = re.split(r"[.;!?]", clause)[0]
    word_list = [w.lower().replace("’", "'") for w in words(head)]
    if not word_list:
        return False
    if word_list[0] in _SUBORDINATORS:
        # dependent opener: only a main clause after a comma makes it a sentence
        for tail in head.split(",")[1:]:
            tail_words = [w.lower().replace("’", "'") for w in words(tail)]
            if (tail_words and tail_words[0] not in _SUBORDINATORS
                    and _has_finite_core(tail_words, cfg)):
                return True
        return False
    return _has_finite_core(word_list, cfg)


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


_INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_inline_code(text: str) -> str:
    """Blank inline-code spans, keeping every offset.

    A JSON or YAML snippet quoted inline (`"provisional": true`) is not prose,
    but it forms the exact colon-space-lowercase shape the colon rules look
    for. Fenced blocks are already dropped by the markdown extractor; inline
    spans were the remaining hole (INBOX 2026-08-19 addendum, found clearing 25
    colon findings from a review memo that quoted a dict literal).
    """
    return _INLINE_CODE.sub(lambda m: " " * len(m.group(0)), text)


def _wrap_continuation(snips: list[Snippet]) -> dict[int, str]:
    """Map id(snippet) -> the prose line that continues it.

    Markdown extraction is line-based, so a sentence that wraps mid-clause is
    split across two snippets. A colon landing at end-of-line therefore had its
    right-hand side out of every colon rule's reach - which is how a lowercase
    sentence after a colon shipped to production under the very rule whose
    2026-07-18 changelog entry exists because one already had (INBOX
    2026-08-19). Whitespace normalization across the wrap is the same fix, and
    for the same documented reason, that `strings_from` already applies to the
    shape patterns.

    A colon that genuinely introduces a list or table is NOT a wrap: there the
    next line is a `list_item` or a cell, and it is left alone.
    """
    out: dict[int, str] = {}
    by_path: dict[str, list[Snippet]] = {}
    for s in snips:
        if s.origin == "md":
            by_path.setdefault(s.path, []).append(s)
    for group in by_path.values():
        group.sort(key=lambda s: s.line)
        for a, b in zip(group, group[1:]):
            if (b.line == a.line + 1
                    and b.role == "prose"
                    and a.role in ("prose", "list_item")):
                out[id(a)] = b.text
    return out


def _prose_colons(text: str) -> list[tuple[int, str, str]]:
    """(index, left-side, right-side) for each sentence-internal colon."""
    out = []
    text = strip_inline_code(text)
    for m in re.finditer(r":", text):
        i = m.start()
        if _COLON_SKIP.search(text[max(0, i - 6) : i + 3]):
            continue
        right = text[i + 1 :].strip()
        if not right:  # trailing colon introducing a list or table below
            continue
        out.append((i, text[:i], right))
    return out


def _colon_line(s: Snippet, right: str) -> int:
    """Point the finding at the colon itself, not the top of the paragraph."""
    word_list = words(right)
    if not word_list:
        return s.line
    return s.line_of(r":\s*(?:&\w+;\s*)*" + re.escape(word_list[0]))


def rule_colons(snips: list[Snippet], cfg: Config | None = None) -> list[Finding]:
    findings: list[Finding] = []
    per_file: dict[str, int] = {}
    last_line: dict[str, int] = {}
    budget = cfg.colon_budget if cfg else 3
    continues = _wrap_continuation(snips)
    for s in snips:
        if s.role == "data":
            continue
        text = s.text
        if text.rstrip().endswith(":") and id(s) in continues:
            text = text.rstrip() + " " + continues[id(s)]
        for _i, left, right in _prose_colons(text):
            # The budget is a body-prose rule. A list of grade bands
            # ("90-100: Right (5 rays)") and a "Title: Subtitle" are not the
            # skeleton the styleguide is counting.
            if s.role == "prose":
                per_file[s.path] = per_file.get(s.path, 0) + 1
                last_line[s.path] = s.line
            label_side = re.split(r"[.;!?]", left)[-1].strip()
            label_words = words(label_side)
            is_label = (0 < len(label_words) <= 4
                        and not _clause_is_sentence(left, cfg=cfg))
            line = _colon_line(s, right)
            if is_label and label_side[:1].islower() and s.role in ("prose", "list_item"):
                findings.append(
                    Finding(
                        s.path, line, "COLON_LABEL", "error",
                        f'lowercase label in a "label: value" skeleton - capitalize it '
                        f'or restructure: "{label_side}: {right[:40]}"',
                        s.text,
                    )
                )
                continue
            if not right[0].islower():
                continue
            if _clause_is_sentence(right, cfg=cfg):
                findings.append(
                    Finding(
                        s.path, line, "COLON_SENTENCE", "error",
                        "a complete sentence after a colon takes a capital (AP): "
                        f'"...: {right[:60]}"',
                        s.text,
                    )
                )
            elif is_label and s.role in ("prose", "list_item"):
                findings.append(
                    Finding(
                        s.path, line, "COLON_SKELETON", "warn",
                        f'"label: value" skeleton - the styleguide calls this a machine '
                        f'fingerprint; most read better as a sentence: "{label_side}: {right[:40]}"',
                        s.text,
                    )
                )
            else:
                findings.append(
                    Finding(
                        s.path, line, "COLON_FRAGMENT", "warn",
                        "lowercase after a colon - correct only for a genuine fragment "
                        f'or enumeration: "...: {right[:60]}"',
                        s.text,
                    )
                )
    for path, count in sorted(per_file.items()):
        # Warn only, deliberately: the shared validator warns rather than errors
        # on colon count too, and a long franchise page legitimately runs past
        # an article's budget. The blocking colon rules are the case rules above.
        if count > budget:
            findings.append(
                Finding(path, last_line[path], "COLON_BUDGET", "warn",
                        f"{count} sentence-internal colons in this file's body prose "
                        f"(budget is {budget}) - restructure most as sentences", "")
            )
    return findings


def rule_emdash(snips: list[Snippet], cfg: Config | None = None) -> list[Finding]:
    findings: list[Finding] = []
    md_words: dict[str, int] = {}
    md_dashes: dict[str, list[int]] = {}
    for s in snips:
        if s.origin == "md":
            md_words[s.path] = md_words.get(s.path, 0) + len(words(s.text))
        if EM_DASH not in s.text:
            continue
        if s.origin == "md":
            # Long-form markdown gets the styleguide's density ceiling instead
            # of a per-instance error: prose is where an em-dash can be right.
            md_dashes.setdefault(s.path, []).extend([s.line] * s.text.count(EM_DASH))
            continue
        if _PLACEHOLDER.match(s.text):
            continue  # empty-cell placeholder, e.g. `${hi ?? "-"}`
        for nth in range(s.text.count(EM_DASH)):
            findings.append(
                Finding(
                    s.path, s.line_of(r"—|&mdash;|&#8212;", nth), "EMDASH", "error",
                    "em-dash in UI copy - use a period, comma, or colon "
                    f'(empty-cell placeholders excepted): "{s.text[:70]}"',
                    s.text,
                )
            )
    for path, lines in md_dashes.items():
        allowed = max(1, md_words.get(path, 0) // 200)
        if len(lines) > allowed:
            findings.append(
                Finding(path, lines[0], "EMDASH_DENSITY", "warn",
                        f"{len(lines)} em-dashes in ~{md_words.get(path, 0)} words "
                        f"(ceiling is 1 per 200 words = {allowed})", "")
            )
    return findings


# Entities carry a semicolon that no reader sees; &rsquo;/&rdquo; alone would
# put a well-punctuated page over the ceiling.
_ENTITY = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]{1,9});")


def rule_semicolon_density(snips: list[Snippet], cfg: Config | None = None) -> list[Finding]:
    """Semicolons against the styleguide's Tier 4 ceiling of ~1 per 500 words.

    Same shape and same reason as EMDASH_DENSITY: on long-form prose the
    per-instance question is a judgment call, but the RATE is mechanical, and
    the rate is what the styleguide actually states. Measured on three shipped
    pages: semicolon density ran up to 5.4x the
    ceiling and `lint:copy` passed them clean, because no rule existed.
    """
    findings: list[Finding] = []
    md_words: dict[str, int] = {}
    counts: dict[str, int] = {}
    first_line: dict[str, int] = {}
    for s in snips:
        if s.origin != "md" or s.role == "data":
            continue
        md_words[s.path] = md_words.get(s.path, 0) + len(words(s.text))
        text = strip_inline_code(_ENTITY.sub(" ", s.text))
        n = text.count(";")
        if n:
            counts[s.path] = counts.get(s.path, 0) + n
            first_line.setdefault(s.path, s.line)
    for path, n in sorted(counts.items()):
        allowed = max(1, md_words.get(path, 0) // 500)
        if n > allowed:
            findings.append(
                Finding(path, first_line[path], "SEMI_DENSITY", "warn",
                        f"{n} semicolons in ~{md_words.get(path, 0)} words "
                        f"(ceiling is 1 per 500 words = {allowed}) - most read "
                        "better as two sentences", "")
            )
    return findings


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_SERIES_CONJ = re.compile(r"\b(?:and|or|nor|plus|as well as)\b", re.IGNORECASE)


def rule_comma_series(snips: list[Snippet], cfg: Config | None = None) -> list[Finding]:
    """A series of three or more items must close with a conjunction.

    Owner rule, 2026-07-08, universal styleguide: "Tenure, staff forecasters,
    and stations he owned" - never "tenure, staff forecasters, stations he
    owned." The bare form is a documented AI tell and had never been encoded
    anywhere, which is how "the sick kid, the closed road, the customer of nine
    years" shipped. A warning, not an error: an appositive or a date clause can
    form the same comma shape, and the judgment is the reader's.
    """
    findings: list[Finding] = []
    for s in snips:
        if s.role == "data" or s.origin == "string":
            continue
        for sentence in _SENTENCE_SPLIT.split(strip_inline_code(s.text)):
            parts = [p.strip() for p in sentence.split(",")]
            if len(parts) < 3:
                continue
            tail = parts[-3:]
            if not all(tail):
                continue
            # Short, comma-weight items only. A long trailing clause is prose
            # with commas in it, not a series.
            if any(len(words(p)) > 8 or len(words(p)) == 0 for p in tail):
                continue
            if _SERIES_CONJ.search(",".join(parts[1:])):
                continue
            if any(ch in sentence for ch in ";:"):
                continue
            findings.append(
                Finding(s.path, s.line, "COMMA_SERIES", "warn",
                        "comma series with no closing conjunction - a series "
                        'closes with "and"/"or" before the last item: '
                        f'"{sentence.strip()[:70]}"', s.text)
            )
    return findings


# A "full statistic" is a figure a reader would recognize as the same claim:
# money, a percentage, a decimal, or a thousands-grouped number. Bare small
# integers are excluded - "3 steps" twice is not a repeated statistic.
_STAT = re.compile(
    r"(?<![\w.$])(?:"
    r"\$\s?\d[\d,]*(?:\.\d+)?[KkMmBb]?"      # $198, $1.2M
    r"|\d[\d,]*(?:\.\d+)?\s?%"                # 47%, 12.5 %
    r"|\d{1,3}(?:,\d{3})+"                    # 15,302
    r"|\d+\.\d+[Xx]?"                         # 2.4, 3.4x
    r")(?![\w])"
)


def rule_stat_repeat(snips: list[Snippet], cfg: Config | None = None) -> list[Finding]:
    """The same full statistic stated twice in one file.

    Tier 1 of the styleguide bans the repeated statistic; nothing enforced it,
    which is how "$198 ... $198" shipped inside a single sentence. Table cells
    and data snippets are exempt - a column of figures is data, and repetition
    there is the point.
    """
    findings: list[Finding] = []
    seen: dict[tuple[str, str], int] = {}
    reported: set[tuple[str, str]] = set()
    for s in snips:
        if s.role in ("data", "cell"):
            continue
        for m in _STAT.finditer(strip_inline_code(s.text)):
            stat = re.sub(r"\s+", "", m.group(0))
            key = (s.path, stat.lower())
            if key in seen:
                if key in reported:
                    continue
                reported.add(key)
                findings.append(
                    Finding(s.path, s.line, "STAT_REPEAT", "warn",
                            f'the statistic "{stat}" appears more than once in '
                            f"this file (first at line {seen[key]}) - state a "
                            "figure once and refer back to it", s.text)
                )
            else:
                seen[key] = s.line
    return findings


# A banned word inside a URL is not prose. A published slug cannot be edited to
# clear a linter, so a finding there can never be resolved - it just trains
# people to route links around the checker (for example `streamline`
# flagged inside two live slugs in four files). Anchor
# text sits outside these patterns and is still scanned normally.
_URLISH = re.compile(
    r"https?://\S+|www\.[\w.-]+\S*|\]\([^)]*\)|(?:href|src|to|url)\s*=\s*[\"'][^\"']*[\"']",
    re.IGNORECASE,
)


# A domain, URL, or handle keeps its own casing.
_DOMAINISH = re.compile(r"^(?:https?://|www\.|@)|^[a-z0-9][a-z0-9.-]*\.[a-z]{2,}$")
_CELL_TAGS = {"td", "th"}


def rule_label_case(snips: list[Snippet], cfg: Config | None = None) -> list[Finding]:
    """Labels, table cells, and stat captions start capitalized.

    Sibling label sets drift out of case agreement one edit at a time (a stat row
    reading "season avg / 100 | graded Right | days scored"). Requiring a capital
    on every one of them keeps a set consistent by construction, which is the
    only version of "consistent" a linter can enforce without guessing which
    sibling is the odd one out.
    """
    findings: list[Finding] = []
    for s in snips:
        if s.origin != "jsx" or not s.text[:1].islower():
            continue
        if s.role == "cell" and s.cell_first and s.parent in _CELL_TAGS:
            findings.append(
                Finding(s.path, s.line, "CELL_CASE", "error",
                        f'table cell starts lowercase - cells are labels, not sentence '
                        f'continuations: "{s.text[:60]}"', s.text))
        elif (
            s.parent == "div"
            and s.solitary
            and len(s.text.split()) <= 6
            and s.text[-1] not in ".?!:"
            and not _DOMAINISH.match(s.text)
        ):
            findings.append(
                Finding(s.path, s.line, "CAPTION_CASE", "error",
                        f'caption/label starts lowercase - capitalize it so a sibling set '
                        f'stays consistent: "{s.text[:60]}"', s.text))
    return findings


def rule_vocab(snips: list[Snippet], terms: list[tuple[str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    for s in snips:
        low = _URLISH.sub(" ", s.text).lower()
        for term, category in terms:
            if term not in low:
                continue
            if re.search(rf"(?<![\w-]){re.escape(term)}(?![\w-])", low):
                findings.append(
                    Finding(s.path, s.line, "VOCAB", "error",
                            f'banned term "{term}" ({category}) in user-facing copy: '
                            f'"{s.text[:70]}"', s.text)
                )
    return findings


ENGINE_RULES = ("COLON_SENTENCE", "COLON_LABEL", "COLON_SKELETON", "COLON_FRAGMENT",
                "COLON_BUDGET", "EMDASH", "EMDASH_DENSITY", "SEMI_DENSITY",
                "COMMA_SERIES", "STAT_REPEAT", "CELL_CASE",
                "CAPTION_CASE", "VOCAB")
PLUGIN_RULES = ("NAV_CASE", "JSX_SPACING", "JSX_QUOTES")
ALL_RULES = ENGINE_RULES + PLUGIN_RULES


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def env_skips() -> frozenset[str]:
    from copylint import _expand_skip

    return _expand_skip(os.environ.get("COPY_LINT_SKIP", "").split(","))


def _wanted(path: Path, cfg: Config) -> bool:
    if path.suffix not in cfg.suffixes or path.name in cfg.exclude_names:
        return False
    rel = cfg.rel(path).replace(os.sep, "/")
    return not any(part in rel.split("/") or rel.startswith(part)
                   for part in cfg.exclude_dirs)


def default_targets(cfg: Config) -> list[Path]:
    if not cfg.targets:
        return [cfg.root]
    return [cfg.root / t for t in cfg.targets if (cfg.root / t).exists()]


def iter_files(paths: list[Path], cfg: Config) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_dir():
            out.extend(sub for sub in sorted(p.rglob("*")) if _wanted(sub, cfg))
        elif _wanted(p, cfg):
            out.append(p)
    return out


def extract_file(path: Path, cfg: Config) -> list[Snippet]:
    module = get_extractor(cfg.framework, path.suffix)
    if module is None:
        return []
    return module.extract(cfg.rel(path), path.read_text(encoding="utf-8"), cfg)


def lint(paths: list[Path], cfg: Config | None = None,
         rules: dict | None = None) -> list[Finding]:
    cfg = cfg if cfg is not None else load_config()
    rules = rules if rules is not None else load_style_rules(cfg=cfg)
    terms = banned_terms(rules, cfg.vocab_blocks)
    files = iter_files(paths, cfg)

    snips: list[Snippet] = []
    by_module: dict[object, list[Snippet]] = {}
    findings: list[Finding] = []
    for path in files:
        module = get_extractor(cfg.framework, path.suffix)
        if module is None:
            continue
        rel = cfg.rel(path)
        src = path.read_text(encoding="utf-8")
        extracted = module.extract(rel, src, cfg)
        snips.extend(extracted)
        by_module.setdefault(module, []).extend(extracted)
        if hasattr(module, "file_rules"):
            findings += module.file_rules(rel, src, cfg)

    findings += rule_colons(snips, cfg)
    findings += rule_emdash(snips, cfg)
    findings += rule_semicolon_density(snips, cfg)
    findings += rule_comma_series(snips, cfg)
    findings += rule_stat_repeat(snips, cfg)
    findings += rule_vocab(snips, terms)
    findings += rule_label_case(snips, cfg)
    for module, module_snips in by_module.items():
        if hasattr(module, "snippet_rules"):
            findings += module.snippet_rules(module_snips, cfg)

    skip = cfg.skip | env_skips()
    findings = [
        f for f in findings
        if f.code not in skip and not cfg.allows(f.code, f.text or f.message)
    ]
    return sorted(findings, key=lambda f: (f.path, f.line, f.code))


def _explain(cfg: Config) -> None:
    skip = cfg.skip | env_skips()
    print(f"config       {cfg.source}")
    print(f"repo root    {cfg.root}")
    print(f"style rules  {style_rules_path(cfg)}")
    print(f"framework    {cfg.framework}")
    print(f"targets      {', '.join(cfg.targets) or '(paths given on the command line)'}")
    print(f"excluded     {', '.join(cfg.exclude_dirs) or '(none)'}")
    print(f"allowlist    {len(cfg.allow)} entr{'y' if len(cfg.allow) == 1 else 'ies'}")
    print("rules")
    for code in ALL_RULES:
        print(f"  {'SKIPPED' if code in skip else 'active '}  {code}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", help="files or dirs (default: configured targets)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--dump", action="store_true", help="print every extracted string")
    ap.add_argument("--explain", action="store_true", help="show the resolved config")
    ap.add_argument("--warnings-as-errors", action="store_true")
    ap.add_argument("--config", help="path to a copy-lint config file")
    args = ap.parse_args(argv)

    cfg = load_config(Path(args.config) if args.config else None)

    if args.explain:
        _explain(cfg)
        return 0

    targets = (
        [Path(p) if Path(p).is_absolute() else Path.cwd() / p for p in args.paths]
        if args.paths
        else default_targets(cfg)
    )

    if args.dump:
        for path in iter_files(targets, cfg):
            for s in extract_file(path, cfg):
                print(f"{s.path}:{s.line}\t[{s.origin}/{s.role}]\t{s.text}")
        return 0

    findings = lint(targets, cfg)
    errors = [f for f in findings if f.severity == "error"]
    warns = [f for f in findings if f.severity == "warn"]

    if args.json:
        print(json.dumps([f.__dict__ for f in findings], indent=2))
    else:
        for f in findings:
            mark = "ERROR" if f.severity == "error" else "warn "
            print(f"{mark} {f.path}:{f.line} [{f.code}] {f.message}")
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s)")
        if errors:
            guide = cfg.guidance_doc or "the universal writing styleguide"
            print(f"Copy fails the styleguide. See {guide}.")

    return 1 if errors or (args.warnings_as_errors and warns) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ConfigError as exc:
        print(exc, file=sys.stderr)
        sys.exit(2)

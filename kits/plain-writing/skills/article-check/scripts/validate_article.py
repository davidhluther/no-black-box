#!/usr/bin/env python3
"""
Article Validator (article-check skill, plain-writing kit)
Checks drafts against plain-writing rules, SEO structure, and optional house rules.
Usage: python validate_article.py draft.md [keyword] [--prose] [--brand-rules rules.json]
"""

import os
import sys
import re
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Canonical word lists live in data/style_rules.json (single source of truth,
# drift-checked against the .md rulebooks by tests/test_style_rules_sync.py).
# Loaded once at import so the checks below stay in sync with the rulebook
# without hand-maintained duplicate arrays.
# ---------------------------------------------------------------------------
_STYLE_RULES_PATH = Path(__file__).resolve().parent.parent / "data" / "style_rules.json"


def _load_style_rules():
    try:
        with open(_STYLE_RULES_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        sys.stderr.write(
            f"FATAL: could not load canonical style rules at {_STYLE_RULES_PATH}: {e}\n"
        )
        sys.exit(2)


STYLE_RULES = _load_style_rules()


# ---------------------------------------------------------------------------
# House-rules layer ("brand rules").
#
# Everything specific to one organization lives in a small JSON file: which
# links count as internal, which product pages count as upsell, which phrases
# count as a call to action. The file is found in this order:
#   1. --brand-rules <file> on the command line
#   2. the SEO_VALIDATE_BRAND_RULES environment variable
#   3. guidelines/VALIDATOR_BRAND_RULES.json in a folder above the article
#   4. data/brand-rules/example.json shipped with this skill (example.org)
# Unknown keys in a rules file stop the run, so a typo can never silently turn
# a check off. See data/brand-rules/example.json for every key.
# ---------------------------------------------------------------------------
SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES_PATH = SKILL_ROOT / "data" / "brand-rules" / "example.json"


def _read_rules_file(path):
    with open(path, encoding="utf-8") as f:
        rules = json.load(f)
    if not isinstance(rules, dict):
        raise ValueError("brand rules must be a JSON object")
    return {k: v for k, v in rules.items() if not k.startswith("_")}


DEFAULT_BRAND_RULES = _read_rules_file(DEFAULT_RULES_PATH)

BRAND_RULES = DEFAULT_BRAND_RULES
PROSE_ONLY = False  # set by --prose: skip blog-only checks
BRAND_RULES_PATH = None  # set when a rules file other than the default is loaded


def _find_brand_rules_file(article_path, explicit=None):
    if explicit:
        return Path(explicit)
    env = os.environ.get("SEO_VALIDATE_BRAND_RULES")
    if env:
        return Path(env)
    d = Path(article_path).resolve().parent
    for parent in [d, *d.parents]:
        cand = parent / "guidelines" / "VALIDATOR_BRAND_RULES.json"
        if cand.is_file():
            return cand
    return None


def load_brand_rules(article_path, explicit=None):
    """Merge a house-rules file (if any) over the example defaults.
    Top-level keys replace wholesale, so a house file states each rule set it
    changes in full. Unknown keys are fatal."""
    global BRAND_RULES, BRAND_RULES_PATH
    path = _find_brand_rules_file(article_path, explicit)
    if path is None:
        BRAND_RULES = DEFAULT_BRAND_RULES
        return
    try:
        overrides = _read_rules_file(path)
    except (OSError, ValueError) as e:
        sys.stderr.write(f"FATAL: could not load brand rules at {path}: {e}\n")
        sys.exit(2)
    unknown = set(overrides) - set(DEFAULT_BRAND_RULES)
    if unknown:
        sys.stderr.write(
            f"FATAL: unknown key(s) in {path}: {sorted(unknown)}. "
            f"Known keys: {sorted(DEFAULT_BRAND_RULES)}\n"
        )
        sys.exit(2)
    merged = dict(DEFAULT_BRAND_RULES)
    merged.update(overrides)
    BRAND_RULES = merged
    BRAND_RULES_PATH = path



# Categories that carry their own dedicated check rather than being flagged as
# banned single words. `transitions` is error-level but is reported by the
# formulaic-transition loop (with an occurrence count) in CHECK 4;
# `tier2_overuse` is warn-level and threshold-based (CHECK "AI_TELLS_T2").
# Everything else marked `_severity: error` in style_rules.json is a banned
# word list, and is picked up here WITHOUT a code change, which is how the
# `terminology` category ("AI models", never "AI assistants") is enforced.
_VOCAB_HANDLED_ELSEWHERE = ("transitions", "tier2_overuse")


def _error_level_vocab():
    """Flat list of (form, category) for every error-level banned word.

    Category names, severities, and categories all come from
    data/style_rules.json — nothing here is hardcoded except the two blocks
    that have their own dedicated checks — so a new error-level word block
    added to the JSON is enforced the moment it lands. Both `words` shapes are
    accepted: a flat list of forms (tier1_vocab, puffery) and a lemma-keyed
    dict of {"forms": [...]} (restricted_words, terminology). Deduped, longest
    forms first so multi-word never shadows a single word.
    """
    seen = {}
    for key, block in STYLE_RULES.items():
        if not isinstance(block, dict) or key in _VOCAB_HANDLED_ELSEWHERE:
            continue
        if block.get("_severity") != "error":
            continue
        category = block.get("_category", key.upper())
        word_list = block.get("words", [])
        specs = (
            word_list.values() if isinstance(word_list, dict)
            else [{"forms": [w]} for w in word_list]
        )
        for spec in specs:
            for form in spec.get("forms", []):
                seen.setdefault(form.lower(), category)
    return sorted(seen.items(), key=lambda kv: -len(kv[0]))


class ValidationResult:
    def __init__(self):
        self.errors = []    # Must fix
        self.warnings = []  # Should fix

    def error(self, category, message, line_num=None):
        loc = f" (line {line_num})" if line_num else ""
        self.errors.append(f"[ERROR] [{category}]{loc} {message}")

    def warn(self, category, message, line_num=None):
        loc = f" (line {line_num})" if line_num else ""
        self.warnings.append(f"[WARN]  [{category}]{loc} {message}")

    @property
    def passed(self):
        return len(self.errors) == 0

    def print_report(self):
        if self.errors:
            print("\n--- ERRORS (must fix) ---")
            for e in self.errors:
                print(f"  {e}")
        if self.warnings:
            print("\n--- WARNINGS (should fix) ---")
            for w in self.warnings:
                print(f"  {w}")
        print()
        if self.passed:
            print("=== VALIDATION PASSED ===")
            if self.warnings:
                print(f"    ({len(self.warnings)} warnings to review)")
        else:
            print(f"=== VALIDATION FAILED === ({len(self.errors)} errors, {len(self.warnings)} warnings)")


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_embedded_markup(content):
    """Blank out <style>...</style> and <script>...</script> blocks so CSS/JS
    embedded in a markdown draft is never read as prose (same treatment as
    code fences). Line count is preserved so reported line numbers stay true.
    """
    out = []
    closing = None
    for line in content.split("\n"):
        if closing is None:
            m = re.match(r"\s*<(style|script)\b", line, re.IGNORECASE)
            if m:
                tag = m.group(1).lower()
                if re.search(rf"</{tag}\s*>", line, re.IGNORECASE):
                    out.append("")
                else:
                    closing = tag
                    out.append("")
                continue
            out.append(line)
        else:
            if re.search(rf"</{closing}\s*>", line, re.IGNORECASE):
                closing = None
            out.append("")
    return "\n".join(out)


def strip_code_fences(content):
    """Blank the inside of fenced code blocks so code (a `# comment`, sample
    text) is never read as a heading or prose. The fence lines stay, and a
    ```json block (JSON-LD schema) is kept whole for the schema checks. Line
    count is preserved so reported line numbers stay true.
    """
    out = []
    fence = None  # None outside a block; else True to keep (json) or False to blank
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            fence = stripped[3:].strip().lower().startswith("json") if fence is None else None
            out.append(line)
        elif fence is False:
            out.append("")
        else:
            out.append(line)
    return "\n".join(out)


def get_lines(content):
    return content.split("\n")


# ---------------------------------------------------------------------------
# CHECK 1: Structure — heading hierarchy and content between subheads
# ---------------------------------------------------------------------------
def check_structure(content, lines, result):
    heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$")
    headings = []
    for i, line in enumerate(lines):
        m = heading_pattern.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            headings.append((i + 1, level, text))

    # Check for H1
    h1_count = sum(1 for _, lvl, _ in headings if lvl == 1)
    if h1_count == 0:
        result.error("STRUCTURE", "No H1 found. Article needs exactly one H1 title.")
    elif h1_count > 1:
        result.error("STRUCTURE", f"Found {h1_count} H1 headings. Use exactly one H1 for the article title.")

    faq_pattern = re.compile(r"(faq|frequently asked|common questions)", re.IGNORECASE)

    # Check for consecutive headings without content between them. FAQ H2 →
    # first H3 is a documented exception: FAQ sections by convention go
    # straight from the section heading into the first question, with no
    # editorial preamble.
    for idx in range(len(headings) - 1):
        line_a, level_a, text_a = headings[idx]
        line_b, level_b, text_b = headings[idx + 1]

        between = lines[line_a:line_b - 1]
        content_between = "".join(l.strip() for l in between)

        if content_between:
            continue
        if level_a == 2 and level_b == 3 and faq_pattern.search(text_a):
            continue  # FAQ exception
        result.error(
            "STRUCTURE",
            f"No content between headings. '{text_a}' (line {line_a}) is immediately followed by '{text_b}' (line {line_b}). Add at least one paragraph between them.",
            line_a,
        )

    # Check H2 -> H3 specifically (must have intro content). Same FAQ exception.
    for idx in range(len(headings) - 1):
        line_a, level_a, text_a = headings[idx]
        line_b, level_b, text_b = headings[idx + 1]
        if level_a == 2 and level_b == 3:
            if faq_pattern.search(text_a):
                continue  # FAQ exception
            between = lines[line_a:line_b - 1]
            text_between = " ".join(l.strip() for l in between if l.strip() and not l.strip().startswith("#"))
            word_count = len(text_between.split())
            if word_count < 20:
                result.error(
                    "STRUCTURE",
                    f"H2 '{text_a}' jumps to H3 '{text_b}' with only {word_count} words between them. Add an introductory paragraph (20+ words) between the H2 and its first H3.",
                    line_a,
                )


# ---------------------------------------------------------------------------
# CHECK 2: Subheads — question format and case rules
# ---------------------------------------------------------------------------
def check_subheads(content, lines, result):
    heading_pattern = re.compile(r"^(#{2,3})\s+(.+)$")
    question_words = ("who", "what", "when", "where", "why", "how", "which", "can", "do", "does", "is", "are", "should", "will", "would", "could")

    for i, line in enumerate(lines):
        m = heading_pattern.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()

            # Subheader label separator must be a colon, not an em-dash, per
            # the plain-writing style guide -> "Subheader Label Separator".
            # The body em-dash check skips headings, so this is the only place
            # heading em-dashes get caught.
            if "—" in text:
                result.error(
                    "SUBHEADS_SEPARATOR",
                    f"H{level} '{text}' uses an em-dash. Use a colon as the label "
                    f"separator: '### Step 1: Receive the invoice', not "
                    f"'### Step 1 — Receive the invoice'.",
                    i + 1,
                )

            # Check question format
            is_question = text.endswith("?") or text.lower().startswith(question_words)
            # P-72: whitelist intentional non-question H2s — the FAQ heading and the
            # product-upsell/CTA heading (sentence-case error below still applies).
            _tl = text.lower()
            _is_faq = _tl.startswith("frequently asked questions")
            _is_upsell = level == 2 and any(
                re.search(p, text) for p in BRAND_RULES["upsell"]["heading_patterns"])
            if not is_question and not _is_faq and not _is_upsell and not PROSE_ONLY:
                result.warn(
                    "SUBHEADS",
                    f"H{level} '{text}' is not phrased as a question. Consider rephrasing as a question for SEO/GEO.",
                    i + 1,
                )

            # Check sentence case (first word cap, rest lowercase unless proper noun
            # or accepted acronym). Applies to BOTH H2 and H3 — title case in either
            # is one of the highest-correlation tells for AI-generated marketing
            # content per the writing quality guidelines.
            if level in (2, 3):
                allowed_caps = {
                    "AP", "ERP", "ACH", "CFO", "CEO", "ROI", "B2B", "B2C", "MFA",
                    "SaaS", "Google", "Microsoft", "Excel", "Word", "Sheets", "Docs",
                    "Gmail", "Slack", "Zoom", "Mastercard", "Visa", "Amex",
                    "AmEx", "American", "Express", "SFTP", "API",
                    "CTA", "FAQ", "I", "IT", "US", "UK", "EDI", "BEC", "OCR",
                    "PO", "GL", "AR", "DSO", "DPO", "BCG", "EY", "PwC", "KPMG",
                    "AFP", "NACHA", "AICPA", "CFPB", "IRS", "SBA",
                    "QuickBooks", "Acrobat", "ChatGPT", "Claude", "Gemini",
                }
                # Words that are clearly title-case-only artifacts: short
                # connectors that should ALWAYS be lowercase in sentence case.
                title_case_indicators = {
                    "Of", "In", "On", "For", "And", "Or", "But", "To", "With",
                    "From", "By", "At", "As", "Is", "Are", "A", "An", "The",
                    "Per", "Via",
                }
                # Common domain nouns that are NOT proper nouns. Capitalized
                # mid-heading, each is a near-certain title-case tell. This
                # catches the lone-capitalized-noun case the majority heuristic
                # misses — e.g. "...with Our Payroll Automation", where only
                # "Automation" is wrong (1 of 7 words, under the majority bar).
                title_case_common_nouns = {
                    "Automation", "Software", "Payments", "Payment", "Invoice",
                    "Invoices", "Process", "Processing", "Management", "Controls",
                    "Solution", "Solutions", "Integration", "Integrations",
                    "Workflow", "Workflows", "Platform", "Cards", "Card",
                    "Transfer", "Transfers", "Fees", "Audit", "Terms",
                    "Accounts", "Payable", "Reconciliation", "Vendor", "Vendors",
                    "Spend", "Expense", "Expenses", "Capital", "Flow",
                }
                words = text.rstrip("?:.").split()
                if len(words) > 2:
                    # A word immediately after a colon is a sentence-start and may
                    # be capitalized (house rule: "Float lever: Virtual cards...").
                    # Exempt those positions from the title-case heuristics.
                    def _after_colon(idx):
                        return idx > 0 and words[idx - 1].rstrip(",.;?").endswith(":")
                    # Strong signal: any title-case-indicator word OR a known
                    # common noun capitalized mid-heading is a near-certain tell.
                    indicator_hits = [
                        w for i, w in enumerate(words)
                        if i >= 1 and not _after_colon(i)
                        and (w.rstrip(",.;:?") in title_case_indicators
                             or w.rstrip(",.;:?") in title_case_common_nouns)
                    ]
                    # Weak signal: more than half of mid-heading words start with
                    # a capital letter and aren't in the allowed set.
                    caps = sum(
                        1 for i, w in enumerate(words)
                        if i >= 1 and not _after_colon(i)
                        and w[:1].isupper() and w.rstrip(",.;:?") not in allowed_caps
                    )
                    if indicator_hits or caps > len(words) // 2:
                        result.error(
                            "SUBHEADS_CASE",
                            f"H{level} '{text}' uses title case. H{level} must be "
                            f"sentence case (first word + proper nouns + accepted "
                            f"acronyms only). Title case in subheads is one of the "
                            f"highest-correlation AI-generated tells.",
                            i + 1,
                        )


# ---------------------------------------------------------------------------
# CHECK 3: Em-dash formatting
# ---------------------------------------------------------------------------
def check_emdashes(content, lines, result):
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            continue
        # Find em-dashes without spaces on both sides
        # Pattern: non-space + em-dash, or em-dash + non-space
        if "\u2014" in line:  # Unicode em-dash
            # Check for missing spaces
            matches = re.finditer(r"(\S)\u2014|\u2014(\S)", line)
            for m in matches:
                result.error("FORMATTING", f"Em-dash without spaces. Use ' \u2014 ' (space before and after). Found in: ...{line[max(0,m.start()-15):m.end()+15]}...", i + 1)
        # Check for hyphens used as dashes (word - word pattern)
        if re.search(r"\w\s-\s\w", line):
            # Exclude list items and actual hyphenated ranges
            if not line.strip().startswith("-") and not re.search(r"\d\s?-\s?\d", line):
                result.warn("FORMATTING", f"Possible hyphen used as dash. Replace ' - ' with a comma or a period, or reword; never an em-dash. Check: ...{line.strip()[:60]}...", i + 1)


# ---------------------------------------------------------------------------
# CHECK 3b: Em-dash label intros and em-dash series intros
# ---------------------------------------------------------------------------
# Style guide rule (references/styleguide.md, Tier 4 mechanics). ERROR only on two patterns: a bold lead-in label followed
# by a dash ("**Issuance** — the AP system...", which should read
# "**Issuance.** The AP system..."), and a dash or dash pair that introduces a
# comma list. Every other em-dash (an explanation dash such as "isn't X — it's
# Y", a single dash running to the sentence end, a plain aside pair) is not an
# error; it stays under the warn-only density limit in check_emdashes.
# ---------------------------------------------------------------------------
_DASH = "—–"
# Bold or bold-italic label, then a dash (em/en, spaced or not, or a spaced
# hyphen). Also catches the dash typed inside the bold: "**Issuance —** the".
_LABEL_DASH_RE = re.compile(
    r"(?P<open>\*\*\*|\*\*|__)(?=\S)(?P<label>[^*_\n]{1,80}?)(?<=\S)(?P=open)"
    r"\s*(?:[" + _DASH + r"]|\s-\s)"
    r"|(?P<open2>\*\*\*|\*\*|__)(?=\S)[^*_\n]{1,80}?\s*[" + _DASH + r"]\s*(?P=open2)"
)
# A dash that counts as a sentence dash: any em-dash; an en-dash or hyphen only
# when spaced (so "1–3 days" and "card-processing" are not dashes).
_SENTENCE_DASH_RE = re.compile(r"—|\s–\s|\s-\s")
_ABBREV_RE = re.compile(r"\b(?:e\.g|i\.e|etc|vs|U\.S|Inc|Corp|Co|No|approx)\.$",
                        re.IGNORECASE)


def _split_sentences(text):
    """Sentence spans for dash pairing. Splits after . ! ? followed by space,
    except after common abbreviations, so an aside pair is not broken in two."""
    spans, start = [], 0
    for m in re.finditer(r"[.!?][\"')\]]*\s+", text):
        if _ABBREV_RE.search(text[start:m.start() + 1]):
            continue
        spans.append((start, m.end()))
        start = m.end()
    if start < len(text):
        spans.append((start, len(text)))
    return spans


# A list item never opens with a clause word; "with the old provider, which handled billing, even during
# outages" is an aside with commas, not a series (Codex must-fix on 683d949c).
_CLAUSE_START_RE = re.compile(
    r"(?:which|who|whom|whose|that|where|when|while|whereas|although|though|because|since|even|if|"
    r"unless|as|so|but|yet|then|especially|including|particularly)\b", re.I)


def _list_items(seg):
    """The items of a series in seg, or None. A series has three or more items with 'and' or 'or'
    before the last, with or without the Oxford comma ("limits, expiration, and vendor lock" or
    "limits, expiration and vendor lock"). Parentheticals are dropped; every item but the last is
    5 words or fewer, and no item opens with a clause word. Comma count alone is never proof."""
    chunks = [x.strip() for x in re.sub(r"\([^)]*\)", "", seg).split(",")]
    if len(chunks) < 2:
        return None
    last = chunks[-1]
    oxford = re.match(r"(?:and|or)\s+(\S.*)", last)
    if oxford:
        items = chunks[:-1] + [oxford.group(1)]
    else:
        plain = re.match(r"(\S.*?)\s+(?:and|or)\s+(\S.*)", last)
        if not plain:
            return None
        items = chunks[:-1] + [plain.group(1), plain.group(2)]
    if len(items) < 3 or any(not x or len(x.split()) > 5 for x in items[:-1]):
        return None
    if any(_CLAUSE_START_RE.match(x) for x in items):
        return None
    return items


def _is_comma_list(seg):
    """A dash pair encloses a series (see _list_items)."""
    return _list_items(seg) is not None


def _is_list_tail(seg):
    """A single dash introduces a series in its run to the sentence end (see _list_items)."""
    return _list_items(seg.strip().rstrip(".!?")) is not None


def find_emdash_intros(text):
    """Return [(kind, snippet)] for every banned dash construction in one line
    of body text (or one table cell). kinds: 'label' (bold lead-in + dash) and
    'series' (a dash pair enclosing a comma list, or a single dash whose run to
    the sentence end is a comma list). Explanation dashes and plain asides are
    not reported. Pure function; the refresh planner mirrors this definition."""
    # Link URLs never carry prose dashes; drop them so they can't skew pairing.
    text = re.sub(r"\]\([^)]*\)", "]", text)
    hits, consumed = [], set()
    for m in _LABEL_DASH_RE.finditer(text):
        hits.append(("label", text[m.start():m.end() + 40].strip()))
        for d in _SENTENCE_DASH_RE.finditer(text, m.start(), m.end() + 1):
            consumed.add(d.start())
    for s_start, s_end in _split_sentences(text):
        dashes = [d for d in _SENTENCE_DASH_RE.finditer(text, s_start, s_end)
                  if d.start() not in consumed]
        k = 0
        while k < len(dashes):
            d = dashes[k]
            snippet = text[max(s_start, d.start() - 40):min(s_end, d.end() + 40)].strip()
            if k + 1 < len(dashes):
                inner = text[d.end():dashes[k + 1].start()]
                if _is_comma_list(inner):
                    hits.append(("series", snippet))
                k += 2  # a pair: series (flagged above) or a plain aside (allowed)
                continue
            # Unpaired dash: an error only when what it introduces is a comma list.
            if _is_list_tail(text[d.end():s_end]):
                hits.append(("series", snippet))
            k += 1
    return hits


_EMDASH_INTRO_FIX = {
    "label": "Bold lead-in labels end with a period: '**Issuance.** The AP system...', "
             "never '**Issuance** — the AP system...'.",
    "series": "Don't use an em-dash to introduce a series. Reword (or, if it "
              "earns its place, a colon with AP capitalization).",
}


def check_emdash_intros(content, lines, result):
    in_code = False
    seen_h1 = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue
        if stripped.startswith("# "):
            seen_h1 = True
            continue
        # Headings are covered by the heading em-dash check in check_subheads;
        # the pre-H1 metadata table and HTML comments are not body text.
        if stripped.startswith("#") or stripped.startswith("<!--"):
            continue
        if not seen_h1 and stripped.startswith("|"):
            continue
        cells = stripped.strip("|").split("|") if stripped.startswith("|") else [stripped]
        for cell in cells:
            for kind, snippet in find_emdash_intros(cell):
                result.error(
                    "EMDASH_INTRO",
                    f"Em-dash {kind} intro (style guide, Tier 4 mechanics).  {_EMDASH_INTRO_FIX[kind]} Found: ...{snippet[:90]}...",
                    i + 1,
                )


# ---------------------------------------------------------------------------
# CHECK 4: Forbidden phrases and AI tells
# ---------------------------------------------------------------------------
def check_forbidden_phrases(content, lines, result):
    content_lower = content.lower()

    # Hard errors: phrases that must never appear.
    # Tier 1 hard bans from the plain-writing style guide (references/styleguide.md)
    # are folded into this list. See that file for the canonical rulebook.
    forbidden_errors = [
        # Time clichés
        "in today's fast-paced",
        "in today's digital",
        "in today's business",
        "in today's ever-evolving",
        "ever-evolving world",
        "ever-evolving landscape",
        "increasingly digital world",
        # Meta-commentary
        "it's important to note",
        "it is important to note",
        "it's worth noting",
        "it is worth noting",
        "it is worth considering",
        "no discussion would be complete",
        "in this article, we will",
        "in this article we will",
        "as we've discussed",
        "as we have discussed",
        # Summary openers (banned in short pieces; long-form >1,500 words
        # can override manually by reviewing the warning)
        "in conclusion",
        "in summary",
        "to sum up",
        "in essence",
        # Negative parallelism (explicit form — broader regex in check_ai_writing_tells)
        "not only",
        # Link callouts (weave into prose instead)
        "click here",
        "read more",
        "learn more",
        # Promotional tail phrases
        "stands as a testament",
        "plays a vital role",
        "plays a significant role",
        "watershed moment",
        "continues to captivate",
        "leaves a lasting impact",
        "key turning point",
        "deeply rooted",
        "steadfast dedication",
        "profound heritage",
        # Chat-assistant openers (AI tells)
        "certainly!",
        "great question!",
        "i'd be happy to",
        "i would be happy to",
        "let's dive in",
        # AI self-reference
        "as of my last update",
        "as an ai",
        "as a language model",
    ]

    for phrase in forbidden_errors:
        if phrase in content_lower:
            # Find the line number
            for i, line in enumerate(lines):
                if phrase in line.lower():
                    result.error("AI_TELLS", f"Forbidden phrase found: '{phrase}'", i + 1)
                    break

    # Overused transitions (error-level). Sourced from data/style_rules.json.
    transition_warns = STYLE_RULES["transitions"]["words"]

    for phrase in transition_warns:
        count = content_lower.count(phrase)
        if count > 0:
            for i, line in enumerate(lines):
                if phrase in line.lower():
                    result.error("AI_TELLS", f"Formulaic transition found: '{phrase}' (appears {count}x total)", i + 1)
                    break  # Report first occurrence only

    # Error-level banned vocabulary: Tier 1 hard-ban words, restricted
    # word-forms, and puffery — all sourced from data/style_rules.json so the
    # enforced list can't drift from the .md rulebooks (drift-guarded by
    # tests/test_style_rules_sync.py). Word-boundary matched to avoid substring
    # false positives (e.g. "elevate" inside "elevator").
    # Strip markdown link targets and bare URLs first, so a banned word living
    # inside a real slug (e.g. a post slug like ".../navigate-hidden-...") is not
    # mistaken for banned prose. Anchor text is preserved and still scanned.
    def _strip_urls(s):
        s = re.sub(r"\]\([^)]*\)", "]", s)   # [anchor](url) -> [anchor]
        s = re.sub(r"https?://\S+", "", s)   # bare URLs
        return s
    cleaned = [_strip_urls(l) for l in lines]
    for form, category in _error_level_vocab():
        pattern = re.compile(r"\b" + re.escape(form) + r"\b", re.IGNORECASE)
        for i, line in enumerate(cleaned):
            if pattern.search(line):
                result.error(category, f"Banned word found: '{form}'", i + 1)
                break


# ---------------------------------------------------------------------------
# CHECK 5: Genericized examples
# ---------------------------------------------------------------------------
def check_genericized_examples(content, lines, result):
    patterns = [
        r"one\s+(logistics|manufacturing|tech|healthcare|financial|mid-sized|growing|large)\s+company",
        r"take\s+a\s+(mid-sized|growing|large|small|typical)\s+",
        r"consider\s+a\s+(mid-sized|growing|large|small|typical)\s+",
        r"imagine\s+a\s+(company|business|organization|firm|team)",
        r"let's\s+say\s+(a|your)\s+(company|business|organization|firm)",
        r"for\s+example,?\s+a\s+(mid-sized|growing|large|small)\s+(company|business|manufacturer|firm)",
    ]
    for pattern in patterns:
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                result.error(
                    "EXAMPLES",
                    f"Genericized placeholder example found. Either cite a real company or explain the concept without a placeholder. Line: '{line.strip()[:80]}...'",
                    i + 1,
                )


# ---------------------------------------------------------------------------
# CHECK 6: Paragraph length
# ---------------------------------------------------------------------------
def check_paragraph_length(content, lines, result):
    # Split into paragraphs (blocks separated by blank lines, excluding headings)
    current_para = []
    para_start = 0
    in_code = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):  # P-72: skip fenced blocks (JSON-LD schema, etc.)
            in_code = not in_code
            current_para = []
            continue
        if in_code:
            continue
        if (
            stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("-")
            or stripped.startswith("*")
            or re.match(r"^\d+\.\s", stripped)  # ordered-list item (1. 2. ...) — not prose
        ):
            current_para = []
            continue
        if stripped == "":
            if current_para:
                text = " ".join(current_para)
                sentences = re.split(r"[.!?]+\s", text)
                sentences = [s for s in sentences if len(s.strip()) > 10]
                if len(sentences) > 6:
                    result.warn(
                        "PARAGRAPHS",
                        f"Paragraph has ~{len(sentences)} sentences (target: 5 or fewer). Consider breaking it up.",
                        para_start + 1,
                    )
            current_para = []
        else:
            if not current_para:
                para_start = i
            current_para.append(stripped)


# ---------------------------------------------------------------------------
# CHECK 7: Smart/curly quotes
# ---------------------------------------------------------------------------
def check_quotes(content, lines, result):
    curly = ["\u201c", "\u201d", "\u2018", "\u2019"]
    for i, line in enumerate(lines):
        for q in curly:
            if q in line:
                result.error("FORMATTING", f"Curly/smart quote found. Use straight quotes only.", i + 1)
                return  # Report once


# ---------------------------------------------------------------------------
# CHECK 8: Emoji detection
# ---------------------------------------------------------------------------
def check_emojis(content, lines, result):
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF"
        "\U0000FE00-\U0000FE0F\U0000200D]+",
        re.UNICODE,
    )
    for i, line in enumerate(lines):
        if emoji_pattern.search(line):
            result.error("FORMATTING", f"Emoji found. Remove all emojis.", i + 1)
            return


# ---------------------------------------------------------------------------
# CHECK 9: Repeated statistics
# ---------------------------------------------------------------------------
def check_repeated_stats(content, lines, result):
    # Find all numbers with % or $ that look like statistics
    stat_pattern = re.compile(r"(\$[\d,.]+\s*(?:billion|million|thousand|B|M|K)?|\d+(?:\.\d+)?%)")
    stats_found = {}
    in_code = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):  # P-72: skip fenced blocks (JSON-LD schema)
            in_code = not in_code
            continue
        if in_code or stripped.startswith("#"):
            continue
        matches = stat_pattern.findall(line)
        for stat in matches:
            stat_normalized = stat.strip()
            if stat_normalized in stats_found:
                first_line = stats_found[stat_normalized]
                if abs(i - first_line) > 3:  # Allow nearby references
                    result.warn(
                        "REPETITION",
                        f"Statistic '{stat_normalized}' appears on both line {first_line + 1} and line {i + 1}. Each stat should appear only once.",
                        i + 1,
                    )
            else:
                stats_found[stat_normalized] = i


# ---------------------------------------------------------------------------
# CHECK 10: Bold overuse (not counting table headers or links)
# ---------------------------------------------------------------------------
def check_bold_overuse(content, lines, result):
    bold_count = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            continue  # Skip table rows
        # Count bold instances that aren't links: **text** but not **[text](url)**
        bolds = re.findall(r"\*\*(?!\[)[^*]+\*\*", line)
        bold_count += len(bolds)

    if bold_count > 8:
        result.warn("FORMATTING", f"Found {bold_count} bold instances (excluding tables/links). Use bold sparingly — only for anchor text and table headers.")


# ---------------------------------------------------------------------------
# CHECK 11: Internal links check
# ---------------------------------------------------------------------------
def check_internal_links(content, lines, result):
    """Check internal blog link count, uniqueness, and variety.

    Three rules:
    1. At least the minimum number of internal blog links set in the rules.
    2. No duplicate links (same URL used more than once in the same draft).
    3. Variety counts — repeating the same target across multiple anchors
       does not contribute to the minimum-six target. The unique-URL count
       is what matters.

    Link domains, minimums, and cross-brand counting come from the brand
    rules (guidelines/VALIDATOR_BRAND_RULES.json in the consuming repo).
    """
    cfg = BRAND_RULES["internal_links"]
    if not cfg.get("patterns"):
        return  # no internal-link rule configured
    groups = {name: re.findall(pat, content) for name, pat in cfg["patterns"].items()}
    all_links = [link for links in groups.values() for link in links]
    unique_links = set(all_links)

    min_target = cfg["min_unique"]
    esc = cfg.get("escalation")
    if esc and len(groups.get(esc["when_group"], [])) >= esc["count_at_least"]:
        min_target = esc["min_unique"]

    if not all_links:
        result.error(
            "SEO",
            f"No internal links to {cfg['label']} found. Include at least {min_target} unique internal links per post.",
        )
    elif len(unique_links) < min_target:
        result.warn(
            "SEO",
            f"Only {len(unique_links)} unique internal link(s) found. Aim for at least {min_target} unique internal blog links per post.",
        )

    # Duplicate detection — same URL appearing 2+ times.
    if len(all_links) != len(unique_links):
        from collections import Counter
        counts = Counter(all_links)
        dupes = sorted(u for u, n in counts.items() if n > 1)
        result.error(
            "SEO",
            f"Duplicate internal link(s) detected — each URL should appear only once per article: {', '.join(dupes)}",
        )


def check_product_link_placement(content, lines, result):
    """Product/solution links belong in the upsell section or CTAs only.

    Rule: product page URLs
    (for example `example.org/products/widgets`) must
    NOT appear in body prose. They go in the second-to-last H2 (upsell)
    or in a CTA block. This protects the editorial voice — product links
    in the middle of explanatory prose feel like ads.

    Product URL patterns come from the brand rules.
    """
    if not BRAND_RULES["product_link_placement"]["url_patterns"]:
        return  # no product-link rule configured
    combined = re.compile("|".join(BRAND_RULES["product_link_placement"]["url_patterns"]))

    # Find all H2 lines and partition the body into sections.
    h2_indices = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if len(h2_indices) < 2:
        return  # too short to reason about; other checks will catch it

    # The upsell H2 is conventionally the second-to-last H2 in the article.
    upsell_start = h2_indices[-2]
    # The "FAQ"/last H2 is body too in most posts; allow product links from
    # upsell_start onwards. CTA blocks (markdown links inside blockquotes
    # or callouts) get a pass via the cta_line_set.
    cta_line_set = _detect_cta_lines(lines)

    for i, line in enumerate(lines):
        if i >= upsell_start:
            continue
        if i in cta_line_set:
            continue
        if combined.search(line):
            result.warn(
                "PRODUCT_LINK_PLACEMENT",
                f"Product/solution link found in body prose at line {i + 1}: '{line.strip()[:90]}'. "
                f"Move product links to the upsell section (second-to-last H2) or a CTA block.",
            )


def _detect_cta_lines(lines):
    """Return the line indices that fall inside a CTA block.

    CTA blocks are blockquotes (`> ...`) that include a markdown link, or
    explicit `> **CTA:**`-prefixed callouts. A run of consecutive blockquote
    lines counts as one block.
    """
    cta = set()
    in_block = False
    block_start = None
    block_has_link = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(">"):
            if not in_block:
                in_block = True
                block_start = i
                block_has_link = False
            if "](" in stripped:
                block_has_link = True
        else:
            if in_block and block_has_link:
                cta.update(range(block_start, i))
            in_block = False
            block_start = None
            block_has_link = False
    if in_block and block_has_link:
        cta.update(range(block_start, len(lines)))
    return cta


def check_bulleted_lists(content, lines, result):
    """Articles should have multiple bulleted/numbered lists to break up prose.

    Rule: aim for at least 3
    distinct lists in addition to whatever appears in the Key Takeaways
    box. A single chart + wall-of-text reads like a newspaper column.
    """
    list_starts = 0
    in_list = False
    for line in lines:
        stripped = line.lstrip()
        is_list_item = (
            stripped.startswith("- ") or stripped.startswith("* ")
            or re.match(r"^\d+\.\s", stripped) is not None
        )
        if is_list_item:
            if not in_list:
                list_starts += 1
                in_list = True
        else:
            if line.strip() == "":
                # blank lines don't break a list visually
                continue
            in_list = False

    # The Key Takeaways box contributes one list; require at least 3 more
    # in the body for a total of 4+ list blocks.
    if list_starts < 4:
        result.warn(
            "STRUCTURE",
            f"Only {list_starts} list block(s) detected. Aim for 4+ (Key Takeaways + at least 3 more in the body) to break up prose.",
        )


# ---------------------------------------------------------------------------
# CHECK 12: Keyword in H1 and intro
# ---------------------------------------------------------------------------
def check_keyword_placement(content, lines, result, keyword=None):
    if not keyword:
        return

    kw_lower = keyword.lower()

    # Check H1
    h1_found = False
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            h1_found = True
            if kw_lower not in line.lower():
                result.warn("SEO", f"Target keyword '{keyword}' not found in H1. Consider including it.")
            break
    if not h1_found:
        result.error("SEO", "No H1 heading found.")

    # Check first 150 words (intro)
    text_lines = [l for l in lines if not l.startswith("#") and l.strip()]
    intro_text = " ".join(text_lines[:6]).lower()
    if kw_lower not in intro_text:
        result.warn("SEO", f"Target keyword '{keyword}' not found in the introduction. Include it in the first 100-150 words.")


# ---------------------------------------------------------------------------
# CHECK 13: Word count
# ---------------------------------------------------------------------------
def check_word_count(content, lines, result):
    text_lines = [l for l in lines if not l.strip().startswith("#") and not l.strip().startswith("|") and not l.strip().startswith("-") and l.strip()]
    word_count = sum(len(l.split()) for l in text_lines)
    if word_count < 800:
        result.warn("LENGTH", f"Article is only ~{word_count} words. Most SEO articles should be 1,200+ words.")
    elif word_count > 6000:
        result.warn("LENGTH", f"Article is ~{word_count} words. Consider whether this could be tightened or split into multiple articles.")
    print(f"  Word count: ~{word_count}")


# ---------------------------------------------------------------------------
# CHECK 14: FAQ section
# ---------------------------------------------------------------------------
def check_faq_section(content, lines, result):
    """Verify FAQ section exists and uses the right structure.

    Rules:
    - FAQ section is a single H2 ("Frequently Asked Questions" or similar)
    - Every individual FAQ question is its own H3 (`### Question?`)
    - The legacy `**Question?**` bold-paragraph format is forbidden — Compose
      renders bolded paragraphs as flat prose, losing the accordion-friendly
      structure AI engines expect.
    """
    faq_h2_idx = None
    for i, line in enumerate(lines):
        if re.search(r"^##\s+.*(faq|frequently asked|common questions)", line, re.IGNORECASE):
            faq_h2_idx = i
            break

    if faq_h2_idx is None:
        result.warn(
            "STRUCTURE",
            "No FAQ section found. Add a single H2 ('Frequently Asked Questions') with each Q as an H3.",
        )
        return

    # Identify the lines that belong to the FAQ section: from the FAQ H2 down
    # until either the next H2, the schema fence (```json), or end of file.
    end_idx = len(lines)
    for j in range(faq_h2_idx + 1, len(lines)):
        if lines[j].startswith("## "):
            end_idx = j
            break
        if lines[j].lstrip().startswith("```json"):
            end_idx = j
            break

    h3_count = 0
    bold_question_lines: list[int] = []
    for k in range(faq_h2_idx + 1, end_idx):
        stripped = lines[k].strip()
        if stripped.startswith("### "):
            h3_count += 1
        elif re.match(r"^\*\*[^*]+\?\*\*\s*$", stripped):
            # `**What is X?**` standalone — the forbidden bold-paragraph FAQ
            # pattern.
            bold_question_lines.append(k + 1)

    if bold_question_lines:
        loc_list = ", ".join(str(n) for n in bold_question_lines[:5])
        more = "" if len(bold_question_lines) <= 5 else f" (and {len(bold_question_lines) - 5} more)"
        result.error(
            "FAQ_STRUCTURE",
            f"FAQ section uses forbidden bold-paragraph format for questions at line(s) {loc_list}{more}. "
            f"Convert each `**Question?**` to `### Question?` so Contentful renders proper H3 subsections.",
        )

    if h3_count == 0 and not bold_question_lines:
        result.warn(
            "STRUCTURE",
            "FAQ H2 found but no H3 questions detected inside. Add 3-5 questions as H3s.",
        )


# ---------------------------------------------------------------------------
# CHECK 15: CTA presence
# ---------------------------------------------------------------------------
def check_cta_presence(content, lines, result):
    # Look for CTA-like patterns (links with action text, or common CTA
    # phrases). Patterns come from the brand rules.
    cta_patterns = BRAND_RULES["cta_patterns"]
    cta_count = 0
    for pattern in cta_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            cta_count += 1
    # P-72: the product-upsell section IS a CTA, and it's the trigger that
    # publish-time cta_embed keys off to inject the inline card the validator
    # (running pre-embed) cannot see. Its presence satisfies the CTA requirement.
    # Upsell product URLs and heading patterns come from the brand rules.
    _upsell = BRAND_RULES["upsell"]
    has_upsell = any(u in content for u in _upsell["product_urls"]) or any(
        l.startswith("## ") and any(re.search(p, l) for p in _upsell["heading_patterns"])
        for l in lines)
    if cta_count == 0 and not has_upsell:
        result.warn("CTA", "No CTAs detected. Include at least one mid-article and one end-of-article CTA.")


# ---------------------------------------------------------------------------
# CHECK 16: Source citations for statistics
# ---------------------------------------------------------------------------
def check_citations(content, lines, result):
    stat_pattern = re.compile(r"\d+(?:\.\d+)?%")
    citation_words = ["according to", "per ", "based on", "from ", "reported by", "survey", "study", "report", "research"]
    # P-72: a percentage that is hypothetical/illustrative, a hedged approximation,
    # or part of a range is NOT a sourced claim and needs no citation. Only a bare,
    # specific, unhedged percentage triggers the citation requirement. (Two-way
    # tested: drops illustrative false-positives; still flags real uncited stats.)
    illustrative = re.compile(r"\b(if you|if your|if we|when you|say you|suppose|imagine|for example|e\.g\.|let'?s say|hypothetically)\b", re.I)
    hedge_before = re.compile(r"(about|around|roughly|~|up to|as much as|as low as|as high as|nearly|almost|over|under|less than|more than|a third|half)\s+\S{0,4}$", re.I)
    rng = re.compile(r"\d+(?:\.\d+)?\s*%?\s*(?:to|and|\u2013|-)\s*\d+(?:\.\d+)?\s*%")

    in_code = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):  # skip fenced blocks (JSON-LD schema)
            in_code = not in_code
            continue
        if in_code or stripped.startswith("#") or stripped.startswith("|"):
            continue
        # A real (non-illustrative) percentage claim on this line?
        real_claim = False
        for sent in re.split(r"(?<=[.!?])\s+", line):
            for m in stat_pattern.finditer(sent):
                if illustrative.search(sent) or rng.search(sent):
                    continue
                if hedge_before.search(sent[:m.start()]):
                    continue
                real_claim = True
                break
            if real_claim:
                break
        if not real_claim:
            continue
        line_lower = line.lower()
        has_citation = any(cw in line_lower for cw in citation_words)
        if i + 1 < len(lines):
            has_citation = has_citation or any(cw in lines[i + 1].lower() for cw in citation_words)
        if not has_citation:
            result.warn(
                "CITATIONS",
                f"Statistic found without apparent source citation. Verify attribution: '{line.strip()[:80]}...'",
                i + 1,
            )


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_article.py <draft.md> [keyword] [--prose] [--brand-rules rules.json]")
        print('Example: python validate_article.py draft.md "volunteer scheduling"')
        print("  --prose        skip blog-structure checks (links, FAQ, CTA, word count) and check the writing only")
        print("  --brand-rules  use your own house-rules file instead of the example")
        sys.exit(1)

    argv = list(sys.argv[1:])
    brand_rules_file = None
    prose_only = False
    if "--prose" in argv:
        global PROSE_ONLY
        prose_only = PROSE_ONLY = True
        argv.remove("--prose")
    if "--brand-rules" in argv:
        i = argv.index("--brand-rules")
        if i + 1 >= len(argv):
            print("Error: --brand-rules needs a file path")
            sys.exit(1)
        brand_rules_file = argv[i + 1]
        del argv[i:i + 2]
    if not argv:
        print("Usage: python validate_article.py <draft.md> [keyword] [--prose] [--brand-rules rules.json]")
        sys.exit(1)
    file_path = argv[0]
    keyword = argv[1] if len(argv) > 1 else None

    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    load_brand_rules(file_path, brand_rules_file)

    content = strip_code_fences(strip_embedded_markup(load_file(file_path)))
    lines = get_lines(content)
    result = ValidationResult()

    print(f"\nValidating: {file_path}")
    if BRAND_RULES_PATH is not None:
        print(f"Brand rules: {BRAND_RULES_PATH}")
    if keyword:
        print(f"Keyword: {keyword}")
    print("-" * 50)

    check_structure(content, lines, result)
    check_subheads(content, lines, result)
    check_emdashes(content, lines, result)
    check_emdash_intros(content, lines, result)
    check_forbidden_phrases(content, lines, result)
    check_genericized_examples(content, lines, result)
    check_paragraph_length(content, lines, result)
    check_quotes(content, lines, result)
    check_emojis(content, lines, result)
    check_repeated_stats(content, lines, result)
    check_bold_overuse(content, lines, result)
    if not prose_only:
        check_internal_links(content, lines, result)
        check_product_link_placement(content, lines, result)
        check_bulleted_lists(content, lines, result)
        check_keyword_placement(content, lines, result, keyword)
        check_word_count(content, lines, result)
        check_faq_section(content, lines, result)
        check_cta_presence(content, lines, result)
    check_citations(content, lines, result)
    if not prose_only:
        if BRAND_RULES.get("cms_template_checks"):
            # Only for sites whose posts start with a metadata table and carry a
            # Key Takeaways box. Off in the example rules.
            check_metadata_table(content, lines, result)
            check_key_takeaways(content, lines, result)
        check_upsell_section(content, lines, result)
    check_see_also_callouts(content, lines, result)
    check_ai_writing_tells(content, lines, result)
    check_emdash_frequency(content, lines, result)
    check_colon_frequency(content, lines, result)
    check_this_is_where(content, lines, result)
    check_in_my_experience(content, lines, result)
    check_meta_commentary(content, lines, result)
    check_anaphora(content, lines, result)
    check_long_comma_lists(content, lines, result)
    check_fourth_wall_seo_meta(content, lines, result)
    check_fourth_wall_catalog_disclaimers(content, lines, result)
    check_fourth_wall_genre_commentary(content, lines, result)
    check_fourth_wall_tablestakes(content, lines, result)
    check_fourth_wall_reader_marketer(content, lines, result)
    # House-rule extra check (no-op unless the rules file enables it)
    check_faq_schema_match(content, lines, result)

    result.print_report()
    sys.exit(0 if result.passed else 1)


# ---------------------------------------------------------------------------
# CHECK 17: Contentful metadata table
# ---------------------------------------------------------------------------
def check_metadata_table(content, lines, result):
    required_fields = ["Name", "Page Title", "Permalink", "SEO Title", "SEO Description", "Topic"]
    has_table = False
    found_fields = []
    for line in lines[:40]:  # Metadata table should be near the top
        # Match a bolded field cell tolerant of whitespace before/after the pipes,
        # so both `| **Field**| value |` and `| **Field** | value |` are detected.
        if re.search(r"\|\s*\*\*", line) and re.search(r"\*\*\s*\|", line):
            has_table = True
            for field in required_fields:
                if field.lower() in line.lower():
                    found_fields.append(field)
    if not has_table:
        result.error("METADATA", "No Contentful metadata table found at top of article. Add the CMS fields table before the H1.")
    else:
        missing = [f for f in required_fields if f not in found_fields]
        if missing:
            result.warn("METADATA", f"Metadata table is missing fields: {', '.join(missing)}")


# ---------------------------------------------------------------------------
# CHECK 18: Key Takeaways section
# ---------------------------------------------------------------------------
def check_key_takeaways(content, lines, result):
    has_takeaways = False
    for line in lines:
        if "key takeaway" in line.lower():
            has_takeaways = True
            break
    if not has_takeaways:
        result.error("TAKEAWAYS", "No Key Takeaways section found. Add a Key Takeaways box after the intro, before the first H2.")


# ---------------------------------------------------------------------------
# CHECK 19: Product upsell section
# ---------------------------------------------------------------------------
def check_upsell_section(content, lines, result):
    # Look for brand product page links which indicate the upsell section.
    # Product URLs and heading patterns come from the brand rules.
    cfg = BRAND_RULES["upsell"]
    if not cfg["product_urls"] and not cfg["heading_patterns"]:
        return  # no upsell rule configured
    has_product_link = any(url in content for url in cfg["product_urls"])

    has_upsell_heading = False
    for line in lines:
        if line.startswith("## "):
            for pattern in cfg["heading_patterns"]:
                if re.search(pattern, line):
                    has_upsell_heading = True
                    break

    if not has_product_link and not has_upsell_heading:
        result.error(
            "UPSELL",
            f"No product upsell section detected. Add a second-to-last H2 that connects the article's pain points to a specific {cfg['label']} product with product page links."
        )


# ---------------------------------------------------------------------------
# CHECK 20: "See also" / "For a further look" link callout patterns
# ---------------------------------------------------------------------------
def check_see_also_callouts(content, lines, result):
    patterns = [
        r"(?i)for\s+a\s+(broader|further|deeper|closer|more\s+detailed)\s+look",
        r"(?i)for\s+more\s+on\s+this\s+topic",
        r"(?i)to\s+learn\s+more\s+about\s+.{1,40},?\s+(see|read|check\s+out|visit)",
        r"(?i)check\s+out\s+our\s+guide\s+to",
        r"(?i)walks\s+through\s+.{1,40}\s+in\s+more\s+detail",
    ]
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern, line):
                result.error(
                    "CALLOUT",
                    f"'See also' link callout detected. Weave links into the prose naturally instead of standalone callouts. Line: '{line.strip()[:80]}...'",
                    i + 1,
                )
                break  # One error per line is enough


# ---------------------------------------------------------------------------
# CHECK 21: AI-writing tells (Tier 2 overuse + Tier 3 structural patterns)
# Per the plain-writing style guide. Tier 1 hard bans are
# handled in check_forbidden_phrases above.
# ---------------------------------------------------------------------------
def check_ai_writing_tells(content, lines, result):
    content_lower = content.lower()

    # Word count for threshold math (body only, excluding headings/tables/lists)
    body_lines = [
        l for l in lines
        if not l.strip().startswith("#")
        and not l.strip().startswith("|")
        and not l.strip().startswith("-")
        and not l.strip().startswith("*")
        and l.strip()
    ]
    word_count = sum(len(l.split()) for l in body_lines) or 1
    # Tier 2 threshold: >1 per 500 words
    threshold = max(1, word_count // 500)

    # --- Tier 2: overuse watches (warnings) --- sourced from style_rules.json
    tier_2_terms = STYLE_RULES["tier2_overuse"]["words"]
    for term in tier_2_terms:
        # Word-boundary match for single words; substring for multi-word
        if " " in term:
            count = content_lower.count(term)
        else:
            count = len(re.findall(r"\b" + re.escape(term) + r"\b", content_lower))
        if count > threshold:
            result.warn(
                "AI_TELLS_T2",
                f"Overuse watch: '{term}' appears {count}x (threshold: {threshold} "
                f"per {word_count}-word body). See shared-skills/writing-styleguide.md Tier 2.",
            )

    # --- Tier 3: Negative parallelism (max once per piece) ---
    # The cross-sentence sibling ("The problem isn't X. It's Y.") counts
    # toward the same cap: when the in-sentence forms were banned, writers
    # displaced into this one, so it is counted with them.
    neg_patterns = [
        r"\bnot\s+just\s+[^,.]{1,60},?\s+but\s+",
        r"\bit'?s\s+not\s+[^,.]{1,60},?\s+it'?s\s+",
        r"\bmore\s+than\s+just\s+[^,.]{1,60},?\s+it'?s\s+",
        r"\b(?:isn'?t|aren'?t|is not|are not)\s+(?:just\s+|only\s+|merely\s+)?"
        r"[^.!?]{0,60}[.!?][\"')\]]?\s+It(?:'s|\s+is)\b",
    ]
    neg_hits = []
    for pattern in neg_patterns:
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                neg_hits.append(i + 1)
    if len(neg_hits) > 1:
        result.warn(
            "AI_TELLS_T3",
            f"Negative parallelism used {len(neg_hits)}x (allowed: 1 per piece). "
            f"Lines: {neg_hits[:5]}. Rewrite extras using direct assertion, a question, "
            f"a scenario, or a data comparison.",
        )

    # --- Tier 3: Participle tails (sentence-final "-ing" clauses that add vague importance) ---
    tail_patterns = [
        r",\s+emphasizing\s+(?:its|the|their|this)\b",
        r",\s+reflecting\s+(?:its|the|their|this)\b",
        r",\s+further\s+cementing\b",
        r",\s+solidifying\s+(?:its|the|their|this)\b",
        r",\s+underscoring\s+(?:the|its|their|this)\b",
        r",\s+highlighting\s+(?:its|the|their|this)\b",
    ]
    for pattern in tail_patterns:
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                result.warn(
                    "AI_TELLS_T3",
                    f"Participle tail detected — almost always cuttable. "
                    f"Line: '{line.strip()[:80]}...'",
                    i + 1,
                )
                break  # One flag per pattern

    # --- Tier 3: Promotional tail phrases not already in forbidden_errors ---
    promo_phrases = [
        "a testament to",
        "rich history",
        "rich cultural heritage",
    ]
    for phrase in promo_phrases:
        if phrase in content_lower:
            for i, line in enumerate(lines):
                if phrase in line.lower():
                    result.warn(
                        "AI_TELLS_T3",
                        f"Promotional tail phrase: '{phrase}'. Replace with specifics or delete.",
                        i + 1,
                    )
                    break

    # --- Tier 3: Uniform sentence length (5+ consecutive sentences within 3-word range) ---
    body_text = " ".join(body_lines)
    # Strip markdown artifacts
    body_text = re.sub(r"[*_`\[\]()]", "", body_text)
    sentences = re.split(r"[.!?]+\s+", body_text)
    sentence_lengths = [len(s.split()) for s in sentences if len(s.split()) >= 3]
    for j in range(len(sentence_lengths) - 4):
        window = sentence_lengths[j:j + 5]
        if max(window) - min(window) <= 3:
            result.warn(
                "AI_TELLS_T3",
                f"Uniform sentence length: 5+ consecutive sentences in a 3-word range "
                f"({min(window)}-{max(window)} words). Vary rhythm — mix short punchy "
                f"sentences with longer complex ones.",
            )
            break  # Flag once per article


# ---------------------------------------------------------------------------
# Helper: extract body-prose lines only (exclude metadata table, tables,
# code fences, list items, headings, blockquotes). Used by frequency checks
# that should ignore structural markup.
# ---------------------------------------------------------------------------
def _body_prose_lines(lines):
    out = []
    in_code = False
    in_metadata_table = False
    seen_h1 = False
    for line in lines:
        stripped = line.strip()
        # Code fences (JSON-LD, etc.)
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # H1 marks end of metadata table
        if stripped.startswith("# "):
            seen_h1 = True
            continue
        if not seen_h1 and stripped.startswith("|"):
            in_metadata_table = True
            continue
        if in_metadata_table and not stripped.startswith("|"):
            in_metadata_table = False
        # Other heading levels, tables, lists, blockquotes, html comments
        if (stripped.startswith("#")
                or stripped.startswith("|")
                or stripped.startswith("- ")
                or stripped.startswith("* ")
                or re.match(r"^\d+\.\s", stripped)
                or stripped.startswith(">")
                or stripped.startswith("<!--")
                or stripped == ""):
            continue
        out.append(line)
    return out


# ---------------------------------------------------------------------------
# CHECK 22: Em-dash frequency in body prose
# ---------------------------------------------------------------------------
# Per the plain-writing style guide:
# "Minimize em-dash usage. Use them only where they genuinely add clarity or
# emphasis. Prefer commas, periods, or colons for asides and appositives."
# Threshold: warn at >1 per 200 body-prose words; warn harder at >1 per 100.
# Severity: WARNING only, both bands. Em-dash density is a formatting measure.
# A blocking gate pushes editors into restructuring published prose to clear a
# count, so this check informs and never blocks.
# ---------------------------------------------------------------------------
def check_emdash_frequency(content, lines, result):
    prose_lines = _body_prose_lines(lines)
    prose_text = " ".join(prose_lines)
    word_count = len(prose_text.split()) or 1
    em_count = prose_text.count("—")
    if em_count == 0:
        return
    ratio = em_count / word_count * 1000  # per 1k words
    target_warn = word_count / 200
    target_err = word_count / 100
    if em_count > target_err:
        result.warn(
            "EM_DASH_FREQ",
            f"Em-dash frequency too high: {em_count} em-dashes in {word_count} body "
            f"words ({ratio:.1f} per 1k). Style guide: minimize em-dashes. "
            f"Target: <{int(target_warn)}. Well over the ceiling. "
            f"Replace with commas, periods, or colons for asides when drafting; "
            f"on a published page, do not restructure prose just to clear this.",
        )
    elif em_count > target_warn:
        result.warn(
            "EM_DASH_FREQ",
            f"Em-dash frequency elevated: {em_count} em-dashes in {word_count} body "
            f"words ({ratio:.1f} per 1k). Target: <{int(target_warn)}. "
            f"Replace excess with commas, periods, or colons.",
        )


# ---------------------------------------------------------------------------
# CHECK 23: Colon frequency in body prose
# ---------------------------------------------------------------------------
# Per the plain-writing style guide → Colon Overuse:
# "Using colons to introduce explanations more than 2-3 times per article."
# Excludes colons inside tables, lists, code blocks, time refs (10:30am), URLs.
# ---------------------------------------------------------------------------
def check_colon_frequency(content, lines, result):
    prose_lines = _body_prose_lines(lines)
    colon_count = 0
    flagged = []
    for line in prose_lines:
        # Strip URL colons and time colons
        cleaned = re.sub(r"https?://\S+", "", line)
        cleaned = re.sub(r"\b\d{1,2}:\d{2}(?:\s*[ap]\.?m\.?)?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bp\.m\.|\ba\.m\.", "", cleaned, flags=re.IGNORECASE)
        # Count colons that look like sentence-internal (preceded by a word, followed by space)
        hits = re.findall(r"\w:\s", cleaned)
        if hits:
            colon_count += len(hits)
            if len(flagged) < 5:
                flagged.append(line.strip()[:80])
    if colon_count > 5:
        result.warn(
            "COLON_OVERUSE",
            f"Colon overuse: {colon_count} sentence-internal colons in body prose. "
            f"Style guide limit: 2-3 per article. Restructure most as regular sentences. "
            f"Examples: {flagged[:3]}",
        )


# ---------------------------------------------------------------------------
# CHECK 24: "This is where..." pivot overuse
# ---------------------------------------------------------------------------
# Per the plain-writing style guide → Sentence-Shape Tells:
# "'This is where the pain hits hardest.' Recognizable LLM cadence; rewrite
# without the construction."
# ---------------------------------------------------------------------------
def check_this_is_where(content, lines, result):
    hits = []
    for i, line in enumerate(lines):
        if re.search(r"\bThis is where\b", line, re.IGNORECASE):
            hits.append((i + 1, line.strip()[:80]))
    if len(hits) >= 1:
        result.warn(
            "AI_TELLS_T3",
            f"'This is where...' pivot used {len(hits)}x. Style guide flags this as "
            f"a recognizable LLM cadence. Rewrite without the construction. "
            f"Lines: {[h[0] for h in hits]}",
        )


# ---------------------------------------------------------------------------
# CHECK 25: "In my experience" usage cap
# ---------------------------------------------------------------------------
# Per the plain-writing style guide: "One naked 'In my experience' per article maximum."
# ---------------------------------------------------------------------------
def check_in_my_experience(content, lines, result):
    count = len(re.findall(r"\bin my experience\b", content, re.IGNORECASE))
    if count > 1:
        result.warn(
            "FIRST_PERSON",
            f"'In my experience' used {count}x. Cap is 1 per article. "
            f"Rotate to: client/scenario references, dated observations, genuine "
            f"equivocations, or direct disagreements with consensus.",
        )


# ---------------------------------------------------------------------------
# CHECK 26: Article-about-itself meta-commentary
# ---------------------------------------------------------------------------
# Per the plain-writing style guide: "Sentences that describe what the article
# will cover are explicit AI scaffolding and are flagged by detectors. Cut entirely."
# ---------------------------------------------------------------------------
def check_meta_commentary(content, lines, result):
    patterns = [
        r"\bthis guide (?:covers|walks|explains|examines)\b",
        r"\bthis article (?:covers|walks|explains|will|examines)\b",
        r"\bthis (?:piece|post) (?:covers|walks|explains|will|examines)\b",
        r"\bwe(?:'ll| will) (?:cover|examine|look at|walk through|explore)\b",
        r"\bin what follows\b",
        r"\bby the end of this (?:guide|article|piece)\b",
        r"\bthe sections below\b",
    ]
    hits = []
    for i, line in enumerate(lines):
        for p in patterns:
            m = re.search(p, line, re.IGNORECASE)
            if m:
                hits.append((i + 1, m.group(0)))
                break
    if hits:
        for line_num, phrase in hits[:5]:
            result.warn(
                "META_COMMENTARY",
                f"Article-about-itself meta-commentary: '{phrase}'. "
                f"Style guide says cut on sight. The article should open in the topic, "
                f"not narrate its own structure.",
                line_num,
            )


# ---------------------------------------------------------------------------
# CHECK 27: Anaphora (3+ consecutive sentences starting with same word)
# ---------------------------------------------------------------------------
# Per the plain-writing style guide: "Do not start three or more consecutive
# sentences with the same word, especially 'This' or 'It'."
# Also style guide § Vary sentence rhythm: "Don't use repetitive anaphora"
# ---------------------------------------------------------------------------
def check_anaphora(content, lines, result):
    prose_text = " ".join(_body_prose_lines(lines))
    prose_text = re.sub(r"[*_`]", "", prose_text)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose_text) if s.strip()]
    run = []
    flagged = set()
    for s in sentences:
        first = re.split(r"\W+", s, maxsplit=1)[0].lower() if s else ""
        if first and run and first == run[-1][0]:
            run.append((first, s))
            if len(run) >= 3 and first not in flagged:
                result.warn(
                    "ANAPHORA",
                    f"{len(run)} consecutive sentences start with '{first.title()}'. "
                    f"Style guide bans 3+ consecutive sentence starters (especially "
                    f"'This' or 'It'). Vary openers.",
                )
                flagged.add(first)
        else:
            run = [(first, s)] if first else []


# ---------------------------------------------------------------------------
# CHECK 28: Triplet/quadruplet comma lists in prose
# ---------------------------------------------------------------------------
# Per the plain-writing style guide → Sentence-Shape Tells:
# "Triplet/quadruplet comma lists — 'Bank connectivity, payment file formatting,
# clearing house integration, fraud screening, and real-time tracking.' Break
# up after the second item or convert to prose."
# ---------------------------------------------------------------------------
def check_long_comma_lists(content, lines, result):
    # Match: A, B, C, D, and E  (4+ items)
    pattern = re.compile(
        r"\b\w[\w\s\-]{1,40},\s+\w[\w\s\-]{1,40},\s+\w[\w\s\-]{1,40},\s+\w[\w\s\-]{1,40},?\s+(?:and|or)\s+\w",
        re.IGNORECASE,
    )
    hits = []
    for i, line in enumerate(_body_prose_lines(lines)):
        if pattern.search(line):
            hits.append(line.strip()[:90])
    if len(hits) > 2:
        result.warn(
            "COMMA_LISTS",
            f"{len(hits)} long comma-separated lists (4+ items) in prose. "
            f"Style guide flags triplet/quadruplet comma lists as sentence-shape tells. "
            f"Break up after the second item or convert to a proper bulleted list. "
            f"Examples: {hits[:2]}",
        )


# ---------------------------------------------------------------------------
# Helper: body lines with line numbers (excludes metadata table, H1, code blocks).
# Includes H2/H3 headings — genre commentary can appear in the heading itself.
# ---------------------------------------------------------------------------
def _body_lines_with_numbers(lines):
    out = []
    in_code = False
    in_metadata_table = False
    seen_h1 = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith("# ") and not seen_h1:
            seen_h1 = True
            continue
        if not seen_h1 and stripped.startswith("|"):
            in_metadata_table = True
            continue
        if in_metadata_table and not stripped.startswith("|"):
            in_metadata_table = False
        if in_metadata_table:
            continue
        if stripped.startswith("<!--"):
            continue
        out.append((i + 1, line))
    return out


# ---------------------------------------------------------------------------
# CHECK 29: Fourth-wall — SEO/AEO backstage vocabulary in body
# ---------------------------------------------------------------------------
# Per plain-writing rule: don't break the fourth wall (category 1):
# "SEO and AEO backstage vocabulary belongs in briefs, validators, and editorial
# conversations, not in the article. The reader doesn't think in these terms;
# only the writer does."
# ---------------------------------------------------------------------------
def check_fourth_wall_seo_meta(content, lines, result):
    patterns = [
        (r"\bSERP\b", "SERP", True),
        (r"\bAEO\b", "AEO", True),
        (r"\bAI Overview\b", "AI Overview", False),
        (r"\bAI extractors?\b", "AI extractor(s)", False),
        (r"\bcitation slot\b", "citation slot", False),
        (r"\bcitation chain\b", "citation chain", False),
        (r"\bAEO whitespace\b", "AEO whitespace", False),
        (r"\bthe rest of the SERP\b", "the rest of the SERP", False),
        (r"\bsearch engines like\b", "search engines like...", False),
        (r"\bAI assistants like\b", "AI assistants like...", False),
    ]
    seen = set()
    for line_num, line in _body_lines_with_numbers(lines):
        for pat, label, case_sens in patterns:
            flags = 0 if case_sens else re.IGNORECASE
            if re.search(pat, line, flags) and label not in seen:
                result.error(
                    "FOURTH_WALL_SEO",
                    f"(line {line_num}) SEO/AEO meta-reference in body: '{label}'. "
                    f"This backstage vocabulary belongs in briefs and SEO metadata, "
                    f"not in the article body. See the plain-writing style guide "
                    f"→ Don't Break the Fourth Wall (category 1).",
                )
                seen.add(label)


# ---------------------------------------------------------------------------
# CHECK 30: Fourth-wall — explicit product-catalog disclaimers
# ---------------------------------------------------------------------------
# Plain-writing rule "Don't break the fourth wall" (category 2):
# Don't open with "<Brand> does/doesn't offer X" or drop defensive
# product-portfolio framing in the body. Exception: FAQ answers to direct
# questions are fine.
# ---------------------------------------------------------------------------
def check_fourth_wall_catalog_disclaimers(content, lines, result):
    brand = re.escape(str(BRAND_RULES.get("brand") or "Example Co"))
    patterns = [
        rf"\b{brand} (?:doesn'?t|does not) offer\b",
        r"\bwe (?:don'?t|do not) offer\b",
        rf"\b{brand}'?s products focus\b",
        rf"\b{brand} is not a\b",
    ]
    # Detect FAQ section start to allow answers to direct questions
    faq_start_line = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+.*(?:frequently asked|faq|common questions)", line, re.IGNORECASE):
            faq_start_line = i + 1
            break
    hits = []
    for line_num, line in _body_lines_with_numbers(lines):
        if faq_start_line and line_num >= faq_start_line:
            continue  # FAQ section gets a pass
        for p in patterns:
            m = re.search(p, line, re.IGNORECASE)
            if m:
                hits.append((line_num, m.group(0)))
                break
    for line_num, phrase in hits[:3]:
        result.error(
            "FOURTH_WALL_DISCLAIMER",
            f"(line {line_num}) Product-catalog disclaimer in body: '{phrase}'. "
            f"Don't announce what the company does or doesn't offer in the body. Let the "
            f"content earn its credibility by being useful. FAQ answers to direct "
            f"questions ('Does Example Co offer X?') are the exception. "
            f"See plain-writing rule: don't break the fourth wall (category 2).",
        )


# ---------------------------------------------------------------------------
# CHECK 31: Fourth-wall — commentary about other articles or article's structure
# ---------------------------------------------------------------------------
# Per plain-writing rule: don't break the fourth wall (category 3):
# "Lines that describe the surrounding content landscape or call attention to
# the article's own H2/H3 choices read as the writer congratulating themselves
# rather than helping the reader."
# ---------------------------------------------------------------------------
def check_fourth_wall_genre_commentary(content, lines, result):
    patterns = [
        (r"\bMost [a-z\-]+ articles?\b", "'Most X articles'"),
        (r"\breads similarly across\b", "'reads similarly across'"),
        (r"\btempting to skip\b", "'tempting to skip'"),
        (r"\bUnlike most (?:coverage|articles|guides)\b", "'Unlike most coverage/articles/guides'"),
        (r"\bthe honest answer (?:that |other guides)\b", "'the honest answer that other guides...'"),
        (r"\b(?:this|the) H2 (?:the rest|below|above|that)\b", "'this/the H2 below/above/the rest'"),
        (r"\bthe section (?:below|above) (?:covers|walks|explains|gets)\b",
            "'the section below/above covers/explains/gets...'"),
        (r"\bwhat follows (?:is|includes|covers|is the section)\b", "'what follows is/includes/covers'"),
        (r"\bthe rest of (?:this|the) (?:article|guide|piece|post)\b",
            "'the rest of this/the article/guide/piece'"),
    ]
    hits = []
    for line_num, line in _body_lines_with_numbers(lines):
        for p, label in patterns:
            m = re.search(p, line, re.IGNORECASE)
            if m:
                hits.append((line_num, label, m.group(0)))
                break
    for line_num, label, phrase in hits[:5]:
        result.error(
            "FOURTH_WALL_GENRE",
            f"(line {line_num}) Genre/structure commentary in body: matched {label} "
            f"(phrase: '{phrase}'). Surfacing the surrounding content landscape or "
            f"the article's own H2/H3 structure reads as the writer congratulating "
            f"themselves. Cut and state the substantive point directly. "
            f"See plain-writing rule: don't break the fourth wall (category 3).",
        )


# ---------------------------------------------------------------------------
# CHECK 32: Fourth-wall — table-stakes credentials outside on-topic context
# ---------------------------------------------------------------------------
# Per plain-writing rule: don't break the fourth wall (category 4):
# SOC 2 Type II is table stakes for most business software. Asserting it in
# non-security articles reads as defensive. Allow if the same H2 section discusses security,
# fraud, audit, compliance, BEC, breach, etc.
# ---------------------------------------------------------------------------
def check_fourth_wall_tablestakes(content, lines, result):
    credential_patterns = [
        (r"\bSOC 2(?:\s+Type\s+II)?\s+compliant\b", "SOC 2 Type II compliant"),
        (r"\bPCI(?:\s+DSS)?\s+compliant\b", "PCI DSS compliant"),
        (r"\bISO\s+27001\s+(?:compliant|certified)\b", "ISO 27001"),
    ]
    on_topic_keywords = re.compile(
        r"\b(?:fraud|security|audit|compliance|breach|BEC|attack|threat|vulnerabilit|"
        r"SOX|certif|attestation|vendor evaluation|due diligence|enterprise procurement)\b",
        re.IGNORECASE,
    )
    body = _body_lines_with_numbers(lines)
    body_dict = {n: l for n, l in body}
    body_nums = sorted(body_dict.keys())
    for line_num, line in body:
        for pat, label in credential_patterns:
            if re.search(pat, line, re.IGNORECASE):
                # Look for on-topic keywords in this line and ±3 lines around it
                idx = body_nums.index(line_num)
                window = []
                for j in range(max(0, idx - 3), min(len(body_nums), idx + 4)):
                    window.append(body_dict[body_nums[j]])
                window_text = " ".join(window)
                # Remove the credential phrase itself before checking context
                window_text_clean = re.sub(pat, "", window_text, flags=re.IGNORECASE)
                if not on_topic_keywords.search(window_text_clean):
                    result.warn(
                        "FOURTH_WALL_TABLESTAKES",
                        f"(line {line_num}) Table-stakes credential claim outside an "
                        f"on-topic section: '{label}'. SOC 2 Type II / PCI / ISO are "
                        f"table stakes for most business vendors — asserting them in "
                        f"articles where security, fraud, audit, or compliance isn't "
                        f"the topic reads as defensive. Cut the line, or verify the "
                        f"surrounding section is genuinely on-topic. "
                        f"See plain-writing rule: don't break the fourth wall (category 4).",
                    )


# ---------------------------------------------------------------------------
# CHECK 33: Fourth-wall — reader-as-marketer winking
# ---------------------------------------------------------------------------
# Per plain-writing rule: don't break the fourth wall (category 5):
# Phrases that assume the reader shares the writer's marketing-side perspective.
# ---------------------------------------------------------------------------
def check_fourth_wall_reader_marketer(content, lines, result):
    patterns = [
        r"\bevery (?:B2B )?(?:finance|operations|marketing|nonprofit) (?:leader|team|director)\b",
        r"\beveryone'?s writing about\b",
        r"\bthis question keeps coming up\b",
        r"\bthe conversation (?:around|about) [a-z]+ has shifted\b",
        r"\bthis topic everyone\b",
        r"\bthis is the topic (?:everyone|every B2B)\b",
    ]
    hits = []
    for line_num, line in _body_lines_with_numbers(lines):
        for p in patterns:
            m = re.search(p, line, re.IGNORECASE)
            if m:
                hits.append((line_num, m.group(0)))
                break
    for line_num, phrase in hits[:3]:
        result.error(
            "FOURTH_WALL_READER_MARKETER",
            f"(line {line_num}) Reader-as-marketer winking: '{phrase}'. "
            f"The reader is a practitioner, not a content strategist. "
            f"Cut the framing or replace with the substantive point. "
            f"See plain-writing rule: don't break the fourth wall (category 5).",
        )


# ---------------------------------------------------------------------------
# BRAND CHECK: FAQ schema must match the visible FAQ section
#   Runs only when a brand config enables it ("faq_schema_match": true).
#   The FAQPage JSON-LD must contain exactly the
#   questions in the article's FAQ section — same set, same order. Including
#   body H2 questions in the schema creates a structured-data/content
#   mismatch (Google penalty risk).
# ---------------------------------------------------------------------------
def check_faq_schema_match(content, lines, result):
    if not BRAND_RULES.get("faq_schema_match"):
        return
    # 1) Extract FAQ section H3 questions (between the FAQ H2 and the schema/EOF).
    faq_h2 = re.search(r"^##\s+.*(faq|frequently asked|common questions).*$", content, re.IGNORECASE | re.MULTILINE)
    if not faq_h2:
        return  # check_faq_section already handles a missing FAQ section
    faq_region = content[faq_h2.end():]
    # Stop at the schema comment / code fence if present
    faq_region = re.split(r"<!--\s*FAQ Schema|```json", faq_region)[0]
    # ...and at the next H2, so later H3s are not counted as FAQ questions
    faq_region = re.split(r"^##\s", faq_region, flags=re.MULTILINE)[0]
    faq_questions = [m.strip() for m in re.findall(r"^###\s+(.+?)\s*$", faq_region, re.MULTILINE)]

    # 2) Extract schema question names from the JSON block whose @type is FAQPage.
    schema = None
    for block in re.findall(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL):
        try:
            obj = json.loads(block)
        except ValueError:
            result.error(
                "FAQ_SCHEMA",
                "A JSON-LD block is not valid JSON. Fix the schema so it parses.",
            )
            return
        t = obj.get("@type") if isinstance(obj, dict) else None
        if t == "FAQPage" or (isinstance(t, list) and "FAQPage" in t):
            schema = obj
            break
    if schema is None:
        if faq_questions:
            result.warn(
                "FAQ_SCHEMA",
                "FAQ section present but no FAQPage JSON-LD schema block found. "
                "Generate a schema block whose questions match the FAQ section.",
            )
        return
    try:
        schema_questions = [q.get("name", "").strip() for q in schema.get("mainEntity", [])]
    except (AttributeError, TypeError):
        result.error(
            "FAQ_SCHEMA",
            "FAQPage JSON-LD block has a malformed mainEntity list. Fix the schema so each question has a name.",
        )
        return

    # 3) Compare. Schema must equal the FAQ section exactly (set + order).
    if schema_questions == faq_questions:
        return

    schema_set, faq_set = set(schema_questions), set(faq_questions)
    extra = [q for q in schema_questions if q not in faq_set]
    missing = [q for q in faq_questions if q not in schema_set]

    if extra:
        result.error(
            "FAQ_SCHEMA",
            f"FAQ schema contains {len(extra)} question(s) NOT in the article's FAQ section "
            f"(likely body H2s). Schema must match the visible FAQ only. Remove: {extra[:5]}",
        )
    if missing:
        result.error(
            "FAQ_SCHEMA",
            f"FAQ section has {len(missing)} question(s) missing from the schema. "
            f"Add them so the schema matches the visible FAQ: {missing[:5]}",
        )
    if not extra and not missing and schema_questions != faq_questions:
        result.warn(
            "FAQ_SCHEMA",
            "FAQ schema has the same questions as the FAQ section but in a different order. "
            "Match the order for cleanliness.",
        )


if __name__ == "__main__":
    main()

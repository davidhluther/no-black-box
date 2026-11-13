#!/usr/bin/env python3
"""tell-scorer engine — per-rule AI-tell vector for published or draft prose.

Organization-neutral core. The scoring functions are fixed so scores stay
comparable across sites and across time; only input handling (extraction,
configuration) varies per use.

What it measures: one feature per deployed guideline element from the house
canon — word lists load from `article-check/data/style_rules.json` (the
article checker's single source of truth), pattern rules ported from
`validate_article.py` and the universal writing styleguide tiers 1-4.
Counts normalize per 1,000 body words.

What it deliberately does NOT measure: rule-of-three synonym stacks and the
Tier 5 discourse rules (stated lessons, tidy resolution, named specifics) are
not reliably regex-detectable; consumers should say nothing about them rather
than fake a number.

Inputs it accepts:
  - HTML (live pages): parse_html(html, selector=...) — pass the article
    container's CSS selector for your site; heuristics try <article> and
    <main> otherwise, and a wrong container quietly poisons every feature,
    so verify extraction on 2-3 pages before trusting a new site.
  - Markdown (drafts/finals): parse_markdown(text).

Both produce the same block model, so draft and live scores are comparable.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    _HAVE_BS4 = True
except ImportError:  # markdown-only use works without bs4
    _HAVE_BS4 = False

_DEFAULT_CANON = Path(__file__).resolve().parents[2] / "article-check" / "data" / "style_rules.json"


# ---------------------------------------------------------------------------
# Canon word lists
# ---------------------------------------------------------------------------

def load_canon(canon_path: str | Path | None = None) -> dict:
    rules = json.loads(Path(canon_path or _DEFAULT_CANON).read_text())
    restricted_forms = []
    for entry in rules.get("restricted_words", {}).get("words", {}).values():
        restricted_forms.extend(entry["forms"])
    terminology_forms = []
    for entry in rules.get("terminology", {}).get("words", {}).values():
        terminology_forms.extend(entry["forms"])
    return {
        "t1_vocab": rules["tier1_vocab"]["words"],
        "restricted": restricted_forms,
        "puffery": rules["puffery"]["words"],
        "transitions": rules["transitions"]["words"],
        "tier2": rules["tier2_overuse"]["words"],
        "terminology": terminology_forms,
    }


# Phrase/pattern lists ported from validate_article.py + styleguide tiers 1-4.
META_COMMENTARY = [
    "it's important to note", "it is important to note", "it's worth noting",
    "it is worth noting", "it is worth considering", "no discussion would be complete",
    "in this article, we will", "in this article we will", "as we've discussed",
    "as we have discussed", "in what follows", "the sections below",
]
META_COMMENTARY_RX = [
    r"\bthis guide (?:covers|walks|explains|examines)\b",
    r"\bthis article (?:covers|walks|explains|will|examines)\b",
    r"\bthis (?:piece|post) (?:covers|walks|explains|will|examines)\b",
    r"\bwe(?:'ll| will) (?:cover|examine|look at|walk through|explore)\b",
    r"\bby the end of this (?:guide|article|piece)\b",
]
TIME_CLICHES = [
    "in today's fast-paced", "in today's digital", "in today's business",
    "in today's ever-evolving", "ever-evolving world", "ever-evolving landscape",
    "increasingly digital world", "rapidly changing world",
]
SUMMARY_CLOSERS = ["in conclusion", "in summary", "to sum up", "in essence",
                   "the bottom line is"]
PROMO_TAILS = [
    "stands as a testament", "a testament to", "plays a vital role",
    "plays a significant role", "watershed moment", "continues to captivate",
    "leaves a lasting impact", "key turning point", "deeply rooted",
    "steadfast dedication", "profound heritage", "rich history",
    "rich cultural heritage",
]
LINK_CALLOUTS = ["click here", "read more", "learn more"]
CHAT_OPENERS = ["certainly!", "great question!", "i'd be happy to",
                "i would be happy to", "let's dive in", "let's explore",
                "let's break it down"]
GENERIC_EXAMPLE_RX = [
    r"one\s+(logistics|manufacturing|tech|healthcare|financial|mid-sized|growing|large)\s+company",
    r"take\s+a\s+(mid-sized|growing|large|small|typical)\s+",
    r"consider\s+a\s+(mid-sized|growing|large|small|typical)\s+",
    r"imagine\s+a\s+(company|business|organization|firm|team)",
    r"let's\s+say\s+(a|your)\s+(company|business|organization|firm)",
    r"for\s+example,?\s+a\s+(mid-sized|growing|large|small)\s+(company|business|manufacturer|firm)",
]
NEG_PARALLEL_RX = [
    r"\bnot\s+just\s+[^,.]{1,60},?\s+but\s+",
    r"\bit'?s\s+not\s+[^,.]{1,60},?\s+it'?s\s+",
    r"\bmore\s+than\s+just\s+[^,.]{1,60},?\s+it'?s\s+",
    r"\bnot\s+only\s+[^,.]{1,60},?\s+but\s+",
]
# Cross-sentence sibling ("It isn't X. It's Y.") — the displacement form the
# 2026-08-25 study caught running 2-5x above pre-guideline baseline.
NEG_PARALLEL_SIBLING_RX = (
    r"\b(?:isn'?t|aren'?t|is not|are not)\s+(?:just\s+|only\s+|merely\s+)?"
    r"[^.!?]{0,60}[.!?][\"')\]]?\s+It(?:'s| is)\b"
)
PARTICIPLE_TAIL_RX = [
    r",\s+emphasizing\s+(?:its|the|their|this)\b",
    r",\s+reflecting\s+(?:its|the|their|this)\b",
    r",\s+further\s+cementing\b",
    r",\s+solidifying\s+(?:its|the|their|this)\b",
    r",\s+underscoring\s+(?:the|its|their|this)\b",
    r",\s+highlighting\s+(?:its|the|their|this)\b",
]
COPULA_RX = [r"\bstands as\b", r"\bserves as\b", r"\bfunctions as\b"]
LONG_COMMA_LIST_RX = re.compile(
    r"\b\w[\w\s\-]{1,40},\s+\w[\w\s\-]{1,40},\s+\w[\w\s\-]{1,40},\s+\w[\w\s\-]{1,40},?\s+(?:and|or)\s+\w",
    re.IGNORECASE)
STAT_RX = re.compile(r"(\$[\d,.]+\s*(?:billion|million|thousand|B|M|K)?|\d+(?:\.\d+)?%)")

# Sentence-case heuristic sets, copied verbatim from the article checker's validate_article.py
# check_subheads (2026-08 state) — the deployed enforcement instrument.
ALLOWED_CAPS = {
    "AP", "ERP", "ACH", "CFO", "CEO", "ROI", "B2B", "B2C", "MFA",
    "SaaS", "NetSuite", "Mastercard", "Visa", "Amex",
    "AmEx", "Ramp", "Brex", "Tipalti", "Coupa", "Sage", "Microsoft",
    "Dynamics", "Intacct", "Acumatica", "American", "Express",
    "AvidXchange", "Airbase", "Expensify", "WEX", "SFTP", "API",
    "CTA", "FAQ", "I", "IT", "US", "UK", "EDI", "BEC", "OCR",
    "PO", "GL", "AR", "DSO", "DPO", "BCG", "EY", "PwC", "KPMG",
    "AFP", "IOFM", "NACHA", "AICPA", "CFPB", "IRS", "SBA",
    "QuickBooks", "Acrobat",
}
TITLE_CASE_INDICATORS = {
    "Of", "In", "On", "For", "And", "Or", "But", "To", "With",
    "From", "By", "At", "As", "Is", "Are", "A", "An", "The",
    "Per", "Via",
}
TITLE_CASE_COMMON_NOUNS = {
    "Automation", "Software", "Payments", "Payment", "Invoice",
    "Invoices", "Process", "Processing", "Management", "Controls",
    "Solution", "Solutions", "Integration", "Integrations",
    "Workflow", "Workflows", "Platform", "Cards", "Card",
    "Transfer", "Transfers", "Fees", "Audit", "Terms",
    "Accounts", "Payable", "Reconciliation", "Vendor", "Vendors",
    "Spend", "Expense", "Expenses", "Capital", "Flow",
}

DEFAULT_SELECTORS = [
    "article",
    'div[class*="post-content"]',
    'div[class*="entry-content"]',
    'div[class*="blog-detail_singlePostContent__"]',
    "main",
]


# ---------------------------------------------------------------------------
# Extraction: HTML or markdown -> block model [(kind, text, bold_count)]
# ---------------------------------------------------------------------------

def parse_html(html: str, selector: str | None = None) -> dict:
    """Parse a page into {title, date, blocks}. Pass the article container's
    CSS selector for reliable extraction; heuristics otherwise."""
    if not _HAVE_BS4:
        raise RuntimeError("HTML parsing needs beautifulsoup4 (pip install bs4 lxml)")
    soup = BeautifulSoup(html, "lxml")

    date = None
    title = None
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        for obj in (data if isinstance(data, list) else [data]):
            if isinstance(obj, dict) and obj.get("@type") in ("BlogPosting", "Article", "NewsArticle"):
                date = date or obj.get("datePublished")
                title = title or obj.get("headline")
    if not title and soup.title:
        title = soup.title.get_text(" ", strip=True)

    # A selector often matches many nodes (page-builder themes emit dozens of
    # identical wrapper divs). Take the RICHEST match — most block children —
    # rather than the first, which is usually a header widget and silently
    # produces a near-empty score.
    def _richest(nodes):
        best, best_n = None, -1
        for node in nodes:
            n = len(node.find_all(["p", "li"], recursive=True))
            if n > best_n:
                best, best_n = node, n
        return best

    # Strip chrome BEFORE choosing a container. Doing it after meant a
    # nav/related-posts widget could win "richest" on its link list and then
    # be emptied by the strip, yielding zero blocks (seen on page-builder
    # themes that emit 100+ identical wrapper divs).
    for bad in soup.find_all(["nav", "aside", "footer", "form", "script", "style"]):
        bad.decompose()

    container = None
    for sel in ([selector] if selector else DEFAULT_SELECTORS):
        matches = soup.select(sel)
        if matches:
            container = _richest(matches)
            break

    blocks: list[tuple[str, str, int]] = []
    if container:
        # Prefer direct children (clean CMS containers); fall back to a full
        # descent when the container nests its blocks deeper.
        kids = container.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol",
                                   "table", "blockquote"], recursive=False)
        if len(kids) < 3:
            kids = container.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol",
                                       "table", "blockquote"])
        for child in kids:
            if child.name in ("ul", "ol"):
                for li in child.find_all("li", recursive=False):
                    text = li.get_text(" ", strip=True)
                    if text:
                        blocks.append(("li", text, len(li.find_all(["strong", "b"]))))
            elif child.name == "table":
                continue  # tables are data, not prose (validator precedent)
            else:
                text = child.get_text(" ", strip=True)
                if not text:
                    continue
                kind = child.name if child.name != "blockquote" else "p"
                bold = len(child.find_all(["strong", "b"]))
                if kind == "p" and len(text.split()) <= 3 and bold >= 1:
                    kind = "label"  # pseudo-heading ("Key Takeaways")
                blocks.append((kind, text, bold))
    return {"title": title, "date": (date or "")[:10], "blocks": blocks}


def parse_markdown(text: str) -> dict:
    """Markdown draft/final -> the same block model as parse_html."""
    blocks: list[tuple[str, str, int]] = []
    title = None
    in_code = False
    seen_h1 = False
    para: list[str] = []

    def flush():
        if para:
            t = " ".join(para)
            bold = len(re.findall(r"\*\*[^*]+\*\*", t))
            clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
            clean = re.sub(r"[*_`]", "", clean)
            kind = "label" if len(clean.split()) <= 3 and bold >= 1 else "p"
            blocks.append((kind, clean, bold))
            para.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            flush()
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if m:
            flush()
            level = len(m.group(1))
            htext = m.group(2).strip()
            if level == 1:
                seen_h1 = True
                title = title or htext
            else:
                blocks.append((f"h{min(level, 4)}", htext, 0))
            continue
        if stripped.startswith("|"):
            flush()
            continue  # tables (incl. metadata table before H1) are data
        if not seen_h1 and not stripped:
            continue
        lm = re.match(r"^(?:[-*]|\d+\.)\s+(.+)$", stripped)
        if lm:
            flush()
            t = lm.group(1)
            bold = len(re.findall(r"\*\*[^*]+\*\*", t))
            clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
            clean = re.sub(r"[*_`]", "", clean)
            blocks.append(("li", clean, bold))
            continue
        if stripped == "":
            flush()
        else:
            para.append(stripped)
    flush()
    return {"title": title, "date": "", "blocks": blocks}


# ---------------------------------------------------------------------------
# Scoring — kept identical to the 2026-08-25 study instrument
# ---------------------------------------------------------------------------

def _count_words_boundary(text_lower: str, words: list[str]) -> int:
    n = 0
    for w in words:
        if " " in w:
            n += text_lower.count(w)
        else:
            n += len(re.findall(r"\b" + re.escape(w) + r"\b", text_lower))
    return n


def _sentences(prose: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", prose)
    return [p.strip() for p in parts if len(p.strip()) > 0]


COUNT_FEATURES = [
    "t1_vocab", "restricted", "puffery", "transitions", "tier2_overuse",
    "ai_assistant_term", "meta_commentary", "time_cliche", "summary_closer",
    "promo_tail", "link_callout", "chat_opener", "generic_example",
    "neg_parallel", "neg_parallel_sibling", "this_is_where",
    "participle_tail", "copula_replace", "long_comma_lists",
    "anaphora_runs", "uniform_sentence_runs", "emdash", "semicolon",
    "colon_internal", "colon_ap_violation", "bold_spans",
    "bold_numeric_blocks", "repeated_stats",
]
HARD_FEATURES = ["t1_vocab", "restricted", "puffery", "transitions", "meta_commentary",
                 "time_cliche", "summary_closer", "promo_tail", "chat_opener",
                 "generic_example", "neg_parallel", "neg_parallel_sibling",
                 "this_is_where", "participle_tail", "ai_assistant_term"]
MECH_FEATURES = ["emdash", "colon_internal", "colon_ap_violation", "semicolon",
                 "anaphora_runs", "uniform_sentence_runs", "long_comma_lists",
                 "repeated_stats", "bold_numeric_blocks", "copula_replace"]


def score_page(blocks: list[tuple[str, str, int]], canon: dict) -> dict:
    prose_blocks = [(t, b) for k, t, b in blocks if k in ("p", "li")]
    para_blocks = [(t, b) for k, t, b in blocks if k == "p"]
    heads = [(k, t) for k, t, _ in blocks if k in ("h2", "h3")]
    prose = " ".join(t for t, _ in prose_blocks)
    prose_lower = prose.lower()
    words = len(prose.split()) or 1
    sents = _sentences(prose)

    f: dict[str, float] = {}
    f["word_count"] = words
    f["sentence_count"] = len(sents)
    f["h2_count"] = sum(1 for k, _ in heads if k == "h2")
    f["h3_count"] = sum(1 for k, _ in heads if k == "h3")
    f["li_count"] = sum(1 for k, _, _ in blocks if k == "li")
    f["para_count"] = len(para_blocks)
    f["avg_sentence_len"] = round(words / max(1, len(sents)), 2)
    f["faq_present"] = int(any(re.search(r"faq|frequently asked", t, re.I) for _, t in heads))

    f["t1_vocab"] = _count_words_boundary(prose_lower, canon["t1_vocab"])
    f["restricted"] = _count_words_boundary(prose_lower, canon["restricted"])
    f["puffery"] = _count_words_boundary(prose_lower, canon["puffery"])
    f["transitions"] = _count_words_boundary(prose_lower, canon["transitions"])
    f["tier2_overuse"] = _count_words_boundary(prose_lower, canon["tier2"])
    f["ai_assistant_term"] = _count_words_boundary(prose_lower, canon["terminology"])

    f["meta_commentary"] = (_count_words_boundary(prose_lower, META_COMMENTARY)
                            + sum(len(re.findall(p, prose_lower)) for p in META_COMMENTARY_RX))
    f["time_cliche"] = _count_words_boundary(prose_lower, TIME_CLICHES)
    f["summary_closer"] = _count_words_boundary(prose_lower, SUMMARY_CLOSERS)
    f["promo_tail"] = _count_words_boundary(prose_lower, PROMO_TAILS)
    f["link_callout"] = _count_words_boundary(prose_lower, LINK_CALLOUTS)
    f["chat_opener"] = _count_words_boundary(prose_lower, CHAT_OPENERS)
    f["generic_example"] = sum(len(re.findall(p, prose_lower)) for p in GENERIC_EXAMPLE_RX)

    f["neg_parallel"] = sum(len(re.findall(p, prose, re.IGNORECASE)) for p in NEG_PARALLEL_RX)
    f["neg_parallel_sibling"] = len(re.findall(NEG_PARALLEL_SIBLING_RX, prose))
    f["this_is_where"] = len(re.findall(r"\bThis is where\b", prose, re.IGNORECASE))
    f["participle_tail"] = sum(len(re.findall(p, prose, re.IGNORECASE)) for p in PARTICIPLE_TAIL_RX)
    f["copula_replace"] = sum(len(re.findall(p, prose_lower)) for p in COPULA_RX)
    f["long_comma_lists"] = sum(1 for t, _ in prose_blocks if LONG_COMMA_LIST_RX.search(t))

    runs = 0
    run_len = 1
    prev = None
    for s in sents:
        first = re.split(r"\W+", s, maxsplit=1)[0].lower() if s else ""
        if first and first == prev:
            run_len += 1
            if run_len == 3:
                runs += 1
        else:
            run_len = 1
        prev = first
    f["anaphora_runs"] = runs

    lens = [len(s.split()) for s in sents if len(s.split()) >= 3]
    uni = 0
    j = 0
    while j <= len(lens) - 5:
        window = lens[j:j + 5]
        if max(window) - min(window) <= 3:
            uni += 1
            j += 5
        else:
            j += 1
    f["uniform_sentence_runs"] = uni

    f["emdash"] = prose.count("\u2014") + len(re.findall(r"\s\u2013\s", prose))
    f["semicolon"] = prose.count(";")
    colon_hits = 0
    colon_ap_viol = 0
    for t, _ in prose_blocks:
        cleaned = re.sub(r"https?://\S+", "", t)
        cleaned = re.sub(r"\b\d{1,2}:\d{2}(?:\s*[ap]\.?m\.?)?", "", cleaned, flags=re.I)
        colon_hits += len(re.findall(r"\w:\s", cleaned))
        for m in re.finditer(r"\w:\s+([a-z][^.!?]{20,})", cleaned):
            if len(m.group(1).split()) >= 6:
                colon_ap_viol += 1
    f["colon_internal"] = colon_hits
    f["colon_ap_violation"] = colon_ap_viol

    # Headings. The boilerplate FAQ heading is a template convention, scored
    # separately so it cannot masquerade as body drafting behavior.
    tc = 0
    head_emdash = 0
    faq_tc = 0
    for _, text in heads:
        if "\u2014" in text:
            head_emdash += 1
        if re.search(r"\bfaqs?\b|frequently asked", text, re.IGNORECASE):
            if text != text.capitalize() and any(
                    w[:1].isupper() for w in text.split()[1:]):
                faq_tc += 1
            continue
        h_words = text.rstrip("?:.").split()
        if len(h_words) > 2:
            def _after_colon(idx):
                return idx > 0 and h_words[idx - 1].rstrip(",.;?").endswith(":")
            indicator_hits = [
                w for i, w in enumerate(h_words)
                if i >= 1 and not _after_colon(i)
                and (w.rstrip(",.;:?") in TITLE_CASE_INDICATORS
                     or w.rstrip(",.;:?") in TITLE_CASE_COMMON_NOUNS)]
            caps = sum(1 for i, w in enumerate(h_words)
                       if i >= 1 and not _after_colon(i)
                       and w[:1].isupper() and w.rstrip(",.;:?") not in ALLOWED_CAPS)
            if indicator_hits or caps > len(h_words) // 2:
                tc += 1
    f["title_case_heads"] = tc
    f["heading_emdash"] = head_emdash
    f["faq_head_title_case"] = faq_tc
    non_faq_heads = [t for _, t in heads
                     if not re.search(r"\bfaqs?\b|frequently asked", t, re.IGNORECASE)]
    f["title_case_head_frac"] = round(tc / max(1, len(non_faq_heads)), 3)

    bold_total = sum(b for _, b in prose_blocks)
    f["bold_spans"] = bold_total
    f["bold_numeric_blocks"] = sum(
        1 for t, b in prose_blocks if b >= 1 and STAT_RX.search(t))

    seen: dict[str, int] = {}
    repeats = 0
    for idx, (t, _) in enumerate(prose_blocks):
        for stat in set(STAT_RX.findall(t)):
            if stat in seen and idx - seen[stat] > 1:
                repeats += 1
            else:
                seen.setdefault(stat, idx)
    f["repeated_stats"] = repeats

    for feat in COUNT_FEATURES:
        f[feat + "_per1k"] = round(f[feat] * 1000.0 / words, 3)
    f["composite_hard_per1k"] = round(sum(f[x] for x in HARD_FEATURES) * 1000.0 / words, 3)
    f["composite_mech_per1k"] = round(sum(f[x] for x in MECH_FEATURES) * 1000.0 / words, 3)
    f["composite_all_per1k"] = round(f["composite_hard_per1k"] + f["composite_mech_per1k"]
                                     + f["title_case_heads"] * 1000.0 / words, 3)
    return f

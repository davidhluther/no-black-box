"""Extraction for markdown copy that ships as-is (.md/.mdx).

This is the *shipped* markdown a site renders - native posts, copy decks - not
a draft on its way through the pipeline. Drafts belong to
`seo-validate/scripts/validate_article.py`, which sees structure this linter
deliberately does not (headings hierarchy, link regimes, word counts). Running
both on the same file is fine and intended: they overlap only on vocabulary,
where they read the same canonical word list.

No framework mechanics here. Markdown's renderer converts quotes and collapses
whitespace on its own, so the two JSX rendering rules have no analogue.
"""

from __future__ import annotations

import re

from . import Snippet

SUFFIXES = frozenset({".md", ".mdx"})

_FENCE = re.compile(r"^\s*```")
# Frontmatter keys that carry copy a reader (or a search result) sees.
_META_KEYS = ("title", "summary", "metaTitle", "metaDescription", "description",
              "excerpt", "dek", "subtitle")
_LABEL_META = ("title", "metaTitle", "subtitle")


def extract(rel: str, src: str, cfg) -> list[Snippet]:
    """Frontmatter titles/descriptions plus body prose, headings, and list items."""
    snippets: list[Snippet] = []
    lines = src.split("\n")
    in_front = False
    in_fence = False
    for idx, line in enumerate(lines, start=1):
        if idx == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
                continue
            m = re.match(r"\s*(\w+)\s*:\s*(.*)$", line)
            if m and m.group(1) in _META_KEYS:
                value = m.group(2).strip().strip('"').strip("'")
                if value:
                    role = "label" if m.group(1) in _LABEL_META else "prose"
                    snippets.append(Snippet(rel, idx, value, value, role, "md"))
            continue
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            continue
        text = line.strip()
        if text.startswith("#"):
            role = "heading"
            text = text.lstrip("#").strip()
        elif text.startswith(("- ", "* ", "|")):
            role = "list_item"
            text = text.lstrip("-* ").strip()
        else:
            role = "prose"
        # strip markdown link targets, keeping the anchor text
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
        if re.search(r"[A-Za-z]", text):
            snippets.append(Snippet(rel, idx, text, line.strip(), role, "md"))
    return snippets

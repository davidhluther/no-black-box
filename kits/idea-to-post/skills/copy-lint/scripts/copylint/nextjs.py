"""Extraction and rendering mechanics for Next/React source (.ts/.tsx/.js/.jsx).

Two jobs, and only two:

1. Pull the strings a reader will actually see out of a file that is mostly
   machinery - JSX text nodes, prose-looking string literals, metadata titles
   and descriptions, aria-labels - and tag each one with a role the shared
   rules can reason about without ever seeing markup again.
2. Run the rules that are about *this toolchain's rendering*, not about prose:
   whitespace that JSX drops at an element boundary, and quote characters that
   nothing in a JSX pipeline converts.

Everything else - colons, em-dashes, vocabulary, label case - lives in the
shared rule engine so every framework gets it.

The heuristics here were tuned against a real production tree until the error
tier had no false positives. Loosen them and the error tier stops being
trustworthy, which is how a linter gets switched off.
"""

from __future__ import annotations

import html
import re

from . import Finding, Snippet, blanked, line_at, strip_comments

SUFFIXES = frozenset({".ts", ".tsx", ".js", ".jsx"})


# ---------------------------------------------------------------------------
# Masking machinery that is not copy
# ---------------------------------------------------------------------------

# Attribute/key values that are machinery, not copy.
_TECHNICAL_KEYS = (
    "className|class|href|src|url|rel|target|xmlns|viewBox|fill|stroke|d|id|key|"
    "slug|path|canonical|encodingFormat|contentUrl|license|sizes|type|as|charSet|"
    "content|property|style|onClick|onChange|value|htmlFor|role|itemProp|"
    "strategy|crossOrigin|loading|decoding|preload"
)


def mask_technical(src: str) -> str:
    """Blank out class names, import paths, and other non-copy string values."""
    out = src

    def blank_span(text: str, start: int, end: int) -> str:
        return text[:start] + blanked(text[start:end]) + text[end:]

    # import/export ... from "..."  and  require("...")
    for pattern in (
        r'^\s*(?:import|export)[^\n;]*?from\s*(["\'])(?:(?!\1).)*\1',
        r'^\s*import\s*(["\'])(?:(?!\1).)*\1',
        r'require\(\s*(["\'])(?:(?!\1).)*\1\s*\)',
    ):
        for m in list(re.finditer(pattern, out, re.MULTILINE)):
            out = blank_span(out, m.start(), m.end())

    # technicalKey={...} / technicalKey="..." / "technicalKey": "..."
    key_re = re.compile(rf'(?<![\w$])"?({_TECHNICAL_KEYS})"?\s*[:=]\s*')
    pos = 0
    while True:
        m = key_re.search(out, pos)
        if not m:
            break
        i = m.end()
        if i >= len(out):
            break
        ch = out[i]
        if ch in "\"'":
            j = i + 1
            while j < len(out) and out[j] != ch:
                j += 2 if out[j] == "\\" else 1
            end = min(j + 1, len(out))
        elif ch == "{":
            depth, j = 0, i
            while j < len(out):
                if out[j] == "{":
                    depth += 1
                elif out[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                elif out[j] in "\"'`":
                    quote, j = out[j], j + 1
                    while j < len(out) and out[j] != quote:
                        j += 2 if out[j] == "\\" else 1
                j += 1
            end = min(j + 1, len(out))
        else:
            pos = m.end()
            continue
        out = blank_span(out, i, end)
        pos = end
    return out


# ---------------------------------------------------------------------------
# JSX text nodes
# ---------------------------------------------------------------------------

_JSX_EXPR = re.compile(r"\{[^{}]*\}")
# Interpolated values stand in as "X", not as nothing: a hole would turn
# `${name} forecast for ${date}: ${line}` into a lowercase label skeleton that
# the real rendered string never has.
_PLACEHOLDER_TOKEN = "X"


def _sub_expression(m: re.Match) -> str:
    """`{" "}` keeps its literal spacing; every other expression becomes X."""
    inner = m.group(0)[1:-1].strip()
    if len(inner) >= 2 and inner[0] == inner[-1] and inner[0] in "\"'":
        return inner[1:-1]
    return _PLACEHOLDER_TOKEN


_CELL_TAGS = {"td", "th"}
_BLOCK_TAGS = {
    "p", "li", "button", "a", "summary", "figcaption", "caption",
    "dt", "dd", "blockquote", "label", "option",
} | _CELL_TAGS
_HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "title", "legend"}
_INLINE_TAGS = {"span", "em", "strong", "small", "b", "i", "sup", "sub", "abbr",
                "a", "Link", "code"}
_STACK_TAGS = _BLOCK_TAGS | _HEADING_TAGS | _INLINE_TAGS | {
    "div", "section", "ul", "ol", "table", "tbody", "thead", "tr",
    "header", "footer", "main", "nav", "aside", "figure",
}
_TAG_RE = re.compile(r"<(/?)([a-zA-Z][\w.-]*)((?:[^<>\"']|\"[^\"]*\"|'[^']*')*?)(/?)>")
# Tags whose contents are code, not copy.
_OPAQUE_TAGS = {"style", "script", "Script", "code", "pre"}
_CODEY = re.compile(
    r"=>|===|&&|\|\||;\s*$|\$\{|\breturn\b|\bconst\b|=\s*[\"'{]"
    r"|\)\s*[:?]|[?:]\s*\(\s*$|\bfunction\b|\bnew Date\b|\w+\.\w+\("
)


def _role_from_stack(stack: list[str]) -> str:
    for tag in reversed(stack):
        if tag in _HEADING_TAGS:
            return "heading"
        if tag == "li":
            return "list_item"
        if tag in _CELL_TAGS:
            return "cell"
        if tag in _BLOCK_TAGS:
            return "prose"
    return "prose"


def extract_jsx_text(rel: str, src: str) -> list[Snippet]:
    """Text nodes between JSX tags, with the enclosing element's role.

    Frames track each open element instance so a text node knows its immediate
    parent, whether it is that parent's only text (a caption or cell label
    rather than a phrase inside a sentence), and whether it leads a table cell.
    """
    snippets: list[Snippet] = []
    frames: list[dict] = []
    opaque = 0
    prev_end = 0
    for m in _TAG_RE.finditer(src):
        chunk = src[prev_end : m.start()]
        if chunk.strip() and not opaque:
            cleaned = _JSX_EXPR.sub(_sub_expression, chunk)
            decoded = html.unescape(cleaned)
            flat = " ".join(decoded.split())
            stack = [f["name"] for f in frames]
            if (
                stack  # real JSX text always sits inside an element; a bare
                # `Record<string, DayPlan>` type annotation does not
                and len(re.findall(r"[A-Za-z]", flat)) >= 2
                and not _CODEY.search(flat)
                and "}" not in flat
                and "{" not in flat
            ):
                lead = len(chunk) - len(chunk.lstrip())
                snip = Snippet(
                    path=rel,
                    line=line_at(src, prev_end + lead),
                    text=flat,
                    raw=" ".join(chunk.split()),
                    role=_role_from_stack(stack),
                    origin="jsx",
                    src=src,
                    span=(prev_end + lead, m.start()),
                    parent=frames[-1]["name"],
                )
                frames[-1]["texts"].append(snip)
                for frame in reversed(frames):
                    if frame["name"] in _CELL_TAGS:
                        snip.cell_first = not frame["cell_seen"]
                        frame["cell_seen"] = True
                        break
                snippets.append(snip)
        closing, name, _attrs, self_closing = m.groups()
        if name in _OPAQUE_TAGS and not self_closing:
            opaque = max(0, opaque - 1) if closing else opaque + 1
        if name in _STACK_TAGS:
            if closing:
                names = [f["name"] for f in frames]
                if name in names:
                    while frames:
                        frame = frames.pop()
                        for text in frame["texts"]:
                            text.solitary = len(frame["texts"]) == 1
                        if frame["name"] == name:
                            break
            elif not self_closing:
                frames.append({"name": name, "texts": [], "cell_seen": False})
        prev_end = m.end()
    return snippets


# ---------------------------------------------------------------------------
# String literals
# ---------------------------------------------------------------------------

_PROSE_KEYS = {
    "description", "summary", "blurb", "body", "tagline", "footnote", "subline",
    "text", "answer", "question", "note", "imagealt", "alt", "aria-label",
    "arialabel", "placeholder", "caption", "metadescription", "excerpt", "dek",
}
_LABEL_KEYS = {
    "title", "headline", "name", "label", "schemaname", "kicker", "heading",
    "metatitle", "sitename",
}
_DATA_KEYS = {"keywords", "about", "@type", "@context", "position", "item"}

_STRING_RE = re.compile(
    r'"((?:[^"\\\n]|\\.)*)"' r"|'((?:[^'\\\n]|\\.)*)'" r"|`((?:[^`\\]|\\.)*)`",
    re.DOTALL,
)
_KEY_BEFORE = re.compile(r'["\']?([\w$@-]+)["\']?\s*[:=]\s*$')
_SLUGGY = re.compile(r"^[a-z0-9_\-./#]+$")
_TAILWINDY = re.compile(r"^[a-z0-9\-:/\[\]%.#!$&*_ +]+$")
_CODE_STRING = re.compile(
    r"\bfunction\s*\(|=>|;\s*$|\}\s*;|\{\s*\w[\w-]*\s*:\s*[^}]*\}"
    r"|\bvar\b|\bwindow\.|\bdocument\.|!function|\bnew Date\b"
)


def _looks_like_copy(value: str) -> bool:
    """Reject paths, slugs, class lists, inline code, and other machinery."""
    v = value.strip()
    if len(v) < 2 or not re.search(r"[A-Za-z]", v):
        return False
    if v.startswith(("/", "#", "http", "data:", "@", ".", "-")):
        return False
    if _SLUGGY.match(v):
        return False
    if re.match(r"^\d{4}-\d{2}(-\d{2})?$", v):
        return False
    if _CODE_STRING.search(v):
        return False
    parts = v.split()
    if len(parts) == 1 and _TAILWINDY.match(v) and re.search(r"[:\[\]]", v):
        return False  # a single utility class token, e.g. "sm:grid-cols-2"
    if len(parts) >= 2 and _TAILWINDY.match(v):
        # class lists: all lowercase, hyphen/colon-dense, no sentence punctuation
        dense = sum(1 for w in parts if re.search(r"[-:/\[\]]", w))
        if dense >= max(1, len(parts) // 2) and not re.search(r"[.,?!]", v):
            return False
    return True


def _strip_interpolations(text: str) -> str:
    """Drop `${...}` template holes, braces and all (they nest)."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("${", i):
            depth, i = 1, i + 2
            while i < n and depth:
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                i += 1
            out.append(_PLACEHOLDER_TOKEN)
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def extract_strings(rel: str, src: str) -> list[Snippet]:
    """Prose-looking string literals, tagged by the key they're assigned to."""
    snippets: list[Snippet] = []
    for m in _STRING_RE.finditer(src):
        raw = next(g for g in m.groups() if g is not None)
        value = _strip_interpolations(raw)
        value = value.replace("\\n", " ").replace('\\"', '"').replace("\\'", "'")
        value = " ".join(html.unescape(value).split())
        if not _looks_like_copy(value):
            continue
        before = src[max(0, m.start() - 60) : m.start()]
        key_match = _KEY_BEFORE.search(before.rstrip().replace("\n", " ").rstrip())
        key = key_match.group(1).lower() if key_match else ""
        if key in _DATA_KEYS:
            role = "data"
        elif key in _LABEL_KEYS:
            role = "label"
        else:
            role = "prose"
        snippets.append(
            Snippet(rel, line_at(src, m.start()), value, raw, role, "string",
                    src=src, span=(m.start(), m.end()))
        )
    return snippets


def extract(rel: str, src: str, cfg) -> list[Snippet]:
    stripped = strip_comments(src)
    snippets: list[Snippet] = []
    if rel.endswith((".tsx", ".jsx")):
        snippets += extract_jsx_text(rel, stripped)
    snippets += extract_strings(rel, mask_technical(stripped))
    return snippets


# ---------------------------------------------------------------------------
# Rendering mechanics: quotes
# ---------------------------------------------------------------------------

# Straight quotes render as straight marks in a display face. Markdown gets
# smart quotes from a typographer plugin at render time; JSX gets nothing, so
# the real entities have to be written.
_STRAIGHT_QUOTE = re.compile(r"&quot;|&#0*34;|\"")


def snippet_rules(snips: list[Snippet], cfg) -> list[Finding]:
    findings: list[Finding] = []
    for s in snips:
        if s.origin != "jsx":
            continue
        seg = s.src[s.span[0] : s.span[1]] if s.src else s.raw
        # `{" "}` spacers are code, not copy; blank them without moving offsets
        seg = _JSX_EXPR.sub(lambda m: " " * len(m.group(0)), seg)
        for m in _STRAIGHT_QUOTE.finditer(seg):
            findings.append(
                Finding(s.path,
                        line_at(s.src, s.span[0] + m.start()) if s.src else s.line,
                        "JSX_QUOTES", "error",
                        "straight quote in rendered text - use &ldquo;/&rdquo; (nothing "
                        f'converts quotes in JSX): "{s.text[:60]}"', s.text))
    return findings


# ---------------------------------------------------------------------------
# Rendering mechanics: whitespace at element boundaries
# ---------------------------------------------------------------------------

# Elements that carry their own horizontal spacing, or sit in a flex/grid row
# that spaces them, don't need a text space between them.
_SPACING_CLASS = re.compile(r"\b(?:mx|mr|ml|px|pr|pl|gap|gap-x|space-x)-")
_LAID_OUT = re.compile(r"\b(?:flex|grid|gap-|space-x-|justify-|items-)")
_WORDY = re.compile(r"[A-Za-z0-9]")
_ENTITY = re.compile(r"&(?:[A-Za-z][A-Za-z0-9]*|#\d+);")


def _spacing_finding(rel: str, src: str, pos: int, message: str) -> Finding:
    context = " ".join(src[max(0, pos - 45) : pos + 45].split())
    return Finding(rel, line_at(src, pos), "JSX_SPACING", "error",
                   f'{message} - insert an explicit {{" "}}: "{context}"', "")


def _spacing_findings(rel: str, src: str) -> list[Finding]:
    findings: list[Finding] = []
    stack: list[tuple[str, str]] = []
    opaque = 0
    prev_end = 0
    prev_tag: tuple[str, str, bool] | None = None  # name, attrs, was_closing
    for m in _TAG_RE.finditer(src):
        chunk = src[prev_end : m.start()]
        closing, name, attrs, self_closing = m.groups()
        parent_attrs = stack[-1][1] if stack else ""
        laid_out = bool(_LAID_OUT.search(parent_attrs))
        if not opaque and chunk and _WORDY.search(chunk):
            # A text node that carries an HTML entity AND wraps across lines
            # loses its LEADING space in this toolchain, so `</em> is scored
            # ... 5&ndash;15 mph` ships as "rangeis scored" even though the
            # source has a space. A single-line node keeps it. Verified
            # against a production build, Next 16 / SWC, 2026-07-28.
            # An interpolation splits the run into separate text nodes, so
            # only the segment up to the first `{` is the node in question.
            first_node = chunk.split("{", 1)[0]
            if (
                prev_tag
                and (prev_tag[2] or prev_tag[0] not in _STACK_TAGS)
                and first_node[:1] == " "
                and _ENTITY.search(first_node)
                and "\n" in first_node
            ):
                findings.append(_spacing_finding(
                    rel, src, prev_end,
                    f"the space after </{prev_tag[0]}> is dropped at build time "
                    "(this text node carries an HTML entity and wraps lines)"))
            # left boundary: a closing tag running into this text
            elif prev_tag and prev_tag[2]:
                head = chunk[: len(chunk) - len(chunk.lstrip())]
                body = chunk.lstrip()
                joined = head == "" or "\n" in head
                if (
                    joined
                    and body[:1]
                    and (body[0].isalnum() or body[0] == "(")
                    and not _SPACING_CLASS.search(prev_tag[1])
                    and not laid_out
                ):
                    findings.append(_spacing_finding(
                        rel, src, prev_end,
                        f"</{prev_tag[0]}> runs into the next word"))
            # right boundary: this text running into an opening inline tag
            if (
                not closing
                and name in _INLINE_TAGS
                and chunk.rstrip()[-1:].isalnum()
                and "\n" in chunk[len(chunk.rstrip()) :]
                and not _SPACING_CLASS.search(attrs)
                and not laid_out
            ):
                findings.append(_spacing_finding(
                    rel, src, m.start(), f"text runs into <{name}>"))
        if name in _OPAQUE_TAGS and not self_closing:
            opaque = max(0, opaque - 1) if closing else opaque + 1
        closed_attrs = attrs
        if name in _STACK_TAGS:
            if closing:
                if name in [s[0] for s in stack]:
                    while stack:
                        popped = stack.pop()
                        if popped[0] == name:
                            # the element's own classes, not the closing tag's
                            closed_attrs = popped[1]
                            break
            elif not self_closing:
                stack.append((name, attrs))
        prev_tag = (name, closed_attrs, bool(closing))
        prev_end = m.end()
    return findings


# ---------------------------------------------------------------------------
# Sibling label sets
# ---------------------------------------------------------------------------

_SMALL_WORDS = {
    "a", "an", "and", "the", "or", "nor", "but", "of", "for", "to", "in", "on",
    "at", "by", "vs", "with", "from", "as", "per",
}


def _title_case_violations(label: str) -> list[str]:
    bad = []
    parts = re.split(r"[\s/]+", label.strip())
    for i, word in enumerate(parts):
        core = word.strip("(),.:;’'\"&")
        if not core or not core[0].isalpha():
            continue
        if core[0].isupper():
            continue
        if i > 0 and core.lower() in _SMALL_WORDS:
            continue
        bad.append(core)
    return bad


def _array_body(src: str, name: str) -> tuple[str, int] | None:
    m = re.search(rf"\b(?:const|let|var)\s+{re.escape(name)}\b[^=]*=\s*\[", src)
    if not m:
        return None
    start = m.end()
    depth, i = 1, start
    while i < len(src) and depth:
        if src[i] == "[":
            depth += 1
        elif src[i] == "]":
            depth -= 1
        i += 1
    return src[start : i - 1], start


def _nav_findings(rel: str, src: str, cfg) -> list[Finding]:
    """Nav and category label sets must be uniformly Title Case.

    Sibling label sets drift out of case agreement one edit at a time. The
    named-array wiring is deliberate: a project says which arrays are label
    sets, and a renamed array is an error rather than a silently skipped check.
    """
    findings: list[Finding] = []
    for spec in cfg.nav_label_sets:
        if spec["file"] != rel:
            continue
        name = spec["array"]
        key = spec.get("key", "label")
        found = _array_body(src, name)
        if not found:
            findings.append(
                Finding(rel, 1, "NAV_CASE", "error",
                        f"label set `{name}` not found - the nav check is wired to it; "
                        "update nav_label_sets if it was renamed", ""))
            continue
        body, offset = found
        for m in re.finditer(rf'{re.escape(key)}\s*:\s*"([^"]+)"', body):
            label = m.group(1)
            bad = _title_case_violations(label)
            if bad:
                findings.append(
                    Finding(rel, line_at(src, offset + m.start()), "NAV_CASE", "error",
                            f'"{label}" breaks Title Case among its `{name}` siblings '
                            f"(lowercase: {', '.join(bad)})", label))
    return findings


def file_rules(rel: str, src: str, cfg) -> list[Finding]:
    stripped = strip_comments(src)
    findings = _nav_findings(rel, stripped, cfg)
    if rel.endswith((".tsx", ".jsx")):
        findings += _spacing_findings(rel, stripped)
    return findings

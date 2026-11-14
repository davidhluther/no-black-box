"""Shared model, config, and extractor registry for the shipped-copy linter.

Everything in this package is framework-agnostic except the extractor modules
themselves. The rule engine (`scripts/copy_lint.py`) imports from here; the
extractor plugins import from here; nothing imports the engine, so a new
framework can be added without touching the rules.

Adding a framework
------------------
Write `copylint/<name>.py` exposing:

    SUFFIXES: frozenset[str]                     file extensions it claims
    extract(rel, src, cfg) -> list[Snippet]      required
    snippet_rules(snips, cfg) -> list[Finding]   optional, framework mechanics
    file_rules(rel, src, cfg) -> list[Finding]   optional, whole-file checks

then add it to `_MODULES` below. The engine calls whichever hooks exist. Only
put a rule in a plugin when it is genuinely about that framework's rendering
(JSX whitespace, JSX quoting); everything decidable from a Snippet belongs in
the shared rule engine so every framework inherits it.
"""

from __future__ import annotations

import importlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "Snippet", "Finding", "Config", "load_config", "find_config_path",
    "line_at", "blanked", "strip_comments", "words", "get_extractor",
    "ConfigError",
]


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


@dataclass
class Snippet:
    """One user-facing string, with where it came from.

    `role` and the three structural flags are what let the shared rules stay
    framework-agnostic: an extractor is responsible for saying "this text is a
    table cell / the only text in its element", and the rules never look at
    markup again.
    """

    path: str
    line: int
    text: str  # entities decoded, template/JSX expressions substituted
    raw: str  # as written in the file
    role: str  # prose | heading | label | list_item | cell | data
    origin: str  # jsx | string | md
    src: str = field(default="", repr=False)  # whole file, for line lookup
    span: tuple[int, int] = field(default=(0, 0), repr=False)
    parent: str = ""  # immediate enclosing element, where there is markup
    solitary: bool = False  # the parent element's only text node
    cell_first: bool = False  # leads a table cell

    def line_of(self, pattern: str, nth: int = 0) -> int:
        """Line of the nth match of `pattern` inside this snippet's source span.

        Findings point at the offending word, not at the top of the paragraph
        that contains it. Falls back to the snippet's first line.
        """
        if not self.src:
            return self.line
        seg = self.src[self.span[0] : self.span[1]]
        matches = list(re.finditer(pattern, seg, re.DOTALL))
        if len(matches) <= nth:
            return self.line
        return line_at(self.src, self.span[0] + matches[nth].start())


@dataclass
class Finding:
    path: str
    line: int
    code: str
    severity: str  # error | warn
    message: str
    text: str


class ConfigError(SystemExit):
    """A config problem the operator has to fix. Never a silent default."""


# ---------------------------------------------------------------------------
# Text helpers shared by engine and plugins
# ---------------------------------------------------------------------------


def line_at(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def blanked(match_text: str) -> str:
    """Replace a region with spaces/newlines so offsets and line numbers hold."""
    return "".join("\n" if ch == "\n" else " " for ch in match_text)


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'’]*", text)


def strip_comments(src: str) -> str:
    """Blank out // and /* */ comments without moving any offset.

    Comments are full of em-dashes and colons that never reach a reader, so they
    have to go before anything else runs. String literals are respected, so a
    URL's `//` survives.
    """
    out = list(src)
    i, n = 0, len(src)
    state = None  # None | '"' | "'" | '`' | 'line' | 'block'
    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if state is None:
            if ch == "/" and nxt == "/":
                state = "line"
                out[i] = out[i + 1] = " "
                i += 2
                continue
            if ch == "/" and nxt == "*":
                state = "block"
                out[i] = out[i + 1] = " "
                i += 2
                continue
            if ch in "\"'`":
                state = ch
            i += 1
            continue
        if state in ("line", "block"):
            if state == "line" and ch == "\n":
                state = None
            elif state == "block" and ch == "*" and nxt == "/":
                out[i] = out[i + 1] = " "
                i += 2
                state = None
                continue
            elif ch != "\n":
                out[i] = " "
            i += 1
            continue
        # inside a string literal
        if ch == "\\":
            i += 2
            continue
        if ch == state:
            state = None
        i += 1
    return "".join(out)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Where a consuming repo puts its parameters. Same convention as the rest of
# this kit: brand/project values live in the consuming repo, never here.
CONFIG_NAMES = ("guidelines/COPY_LINT_PARAMS.json", ".copy-lint.json")

_DEFAULT_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".md", ".mdx")

# Rule-group aliases accepted by COPY_LINT_SKIP and `skip`, alongside bare rule
# codes. `heading` is a legacy alias for the label/nav case set (the
# heading-shaped rules in this engine), so it maps there.
RULE_GROUPS = {
    "colon": ("COLON_SENTENCE", "COLON_LABEL", "COLON_SKELETON", "COLON_FRAGMENT",
              "COLON_BUDGET"),
    "case": ("NAV_CASE", "CELL_CASE", "CAPTION_CASE"),
    "heading": ("NAV_CASE", "CELL_CASE", "CAPTION_CASE"),
    "emdash": ("EMDASH", "EMDASH_DENSITY"),
    "density": ("EMDASH_DENSITY", "SEMI_DENSITY"),
    "series": ("COMMA_SERIES",),
    "stats": ("STAT_REPEAT",),
    "vocab": ("VOCAB",),
    "jsx": ("JSX_SPACING", "JSX_QUOTES"),
}


@dataclass
class Config:
    """Everything project-shaped. Defaults suit a typical Next.js site."""

    root: Path = field(default_factory=Path.cwd)
    source: str = "<defaults>"  # where these values came from, for --explain
    framework: str = "auto"
    targets: tuple[str, ...] = ()
    exclude_dirs: tuple[str, ...] = ()
    exclude_names: frozenset[str] = frozenset()
    suffixes: frozenset[str] = frozenset(_DEFAULT_SUFFIXES)
    nav_label_sets: tuple[dict, ...] = ()
    allow: tuple[str, ...] = ()
    skip: frozenset[str] = frozenset()
    extra_determiners: tuple[str, ...] = ()
    vocab_blocks: tuple[str, ...] = ()  # empty = every error-severity block
    colon_budget: int = 3
    guidance_doc: str = ""
    style_rules_path: str = ""

    # -- derived -----------------------------------------------------------

    def rel(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.root))
        except ValueError:
            return str(path)

    def skips(self, code: str) -> bool:
        return code in self.skip

    def allows(self, code: str, text: str) -> bool:
        """Per-consumer exemptions.

        An entry is either a bare substring (exempts any rule) or
        `CODE::substring` (that rule only). Substring, not regex, because these
        get written by whoever is clearing a backlog and a bad regex there fails
        open on everything.
        """
        for entry in self.allow:
            code_part, sep, needle = entry.partition("::")
            if sep:
                if code_part.strip().upper() == code and needle.strip() in text:
                    return True
            elif entry in text:
                return True
        return False


_KNOWN_KEYS = {
    "root", "framework", "targets", "exclude_dirs", "exclude_names", "suffixes",
    "nav_label_sets", "allow", "skip", "extra_determiners", "vocab_blocks",
    "colon_budget", "guidance_doc", "style_rules_path", "_note", "_source",
}


def _expand_skip(values) -> frozenset[str]:
    out: set[str] = set()
    for value in values:
        token = str(value).strip()
        if not token:
            continue
        out.update(RULE_GROUPS.get(token.lower(), (token.upper(),)))
    return frozenset(out)


def find_config_path(start: Path | None = None) -> Path | None:
    """COPY_LINT_PARAMS, else the nearest config walking up from `start`."""
    env = os.environ.get("COPY_LINT_PARAMS")
    if env:
        path = Path(env).expanduser()
        if not path.exists():
            raise ConfigError(
                f"FATAL: COPY_LINT_PARAMS points at {path}, which does not exist."
            )
        return path
    here = (start or Path.cwd()).resolve()
    for directory in (here, *here.parents):
        for name in CONFIG_NAMES:
            candidate = directory / name
            if candidate.exists():
                return candidate
    return None


def load_config(path: Path | None = None, start: Path | None = None) -> Config:
    """Load consumer parameters.

    No config is legal — the linter then reads whatever paths it is given, with
    the shared defaults. That is what makes `copy_lint.py src/` useful in a repo
    that has not adopted it yet. What is NOT legal is an unreadable or
    unrecognized config: a typo'd key would silently drop a project's
    allowlist or its nav-label wiring, and the failure would look like a clean
    run. Same rule the shared validator uses for VALIDATOR_BRAND_RULES.json.
    """
    path = path or find_config_path(start)
    if path is None:
        return Config(root=(start or Path.cwd()).resolve())
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"FATAL: cannot read copy-lint config {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"FATAL: {path} must contain a JSON object.")
    unknown = sorted(set(data) - _KNOWN_KEYS)
    if unknown:
        raise ConfigError(
            f"FATAL: unknown key(s) in {path}: {', '.join(unknown)}\n"
            f"Known keys: {', '.join(sorted(k for k in _KNOWN_KEYS if not k.startswith('_')))}\n"
            "Unknown keys are fatal on purpose - a typo here would silently drop "
            "an allowlist or a rule skip, and the run would still look clean."
        )
    # The repo root is where `targets` and every reported path are resolved
    # from. Inferred from the config's own location, because that is right for
    # a config committed to the repo it configures; `root` overrides for the
    # case it cannot infer (a config held outside the tree, e.g. in CI).
    root = path.parent
    if path.name == "COPY_LINT_PARAMS.json":
        root = path.parent.parent  # guidelines/ sits under the repo root
    if "root" in data:
        root = path.parent / str(data["root"])  # absolute value wins outright
        if not root.is_dir():
            raise ConfigError(f'FATAL: "root" in {path} is not a directory: {root}')
    bad_nav = [n for n in data.get("nav_label_sets", []) if not isinstance(n, dict) or "file" not in n or "array" not in n]
    if bad_nav:
        raise ConfigError(
            f"FATAL: each nav_label_sets entry in {path} needs \"file\" and \"array\" "
            f'(optionally "key", default "label"); bad entries: {bad_nav}'
        )
    return Config(
        root=root.resolve(),
        source=str(path),
        framework=data.get("framework", "auto"),
        targets=tuple(data.get("targets", ())),
        exclude_dirs=tuple(data.get("exclude_dirs", ())),
        exclude_names=frozenset(data.get("exclude_names", ())),
        suffixes=frozenset(data.get("suffixes", _DEFAULT_SUFFIXES)),
        nav_label_sets=tuple(data.get("nav_label_sets", ())),
        allow=tuple(data.get("allow", ())),
        skip=_expand_skip(data.get("skip", ())),
        extra_determiners=tuple(w.lower() for w in data.get("extra_determiners", ())),
        vocab_blocks=tuple(data.get("vocab_blocks", ())),
        colon_budget=int(data.get("colon_budget", 3)),
        guidance_doc=data.get("guidance_doc", ""),
        style_rules_path=data.get("style_rules_path", ""),
    )


# ---------------------------------------------------------------------------
# Extractor registry
# ---------------------------------------------------------------------------

_MODULES = ("nextjs", "markdown")


def _load(name: str):
    return importlib.import_module(f"{__name__}.{name}")


def available() -> tuple[str, ...]:
    return _MODULES


def get_extractor(framework: str, suffix: str):
    """Resolve a plugin. `auto` dispatches on file extension.

    Returns None when nothing claims the suffix, which the driver treats as
    "not a copy file" rather than an error - a repo's target dir will contain
    images and JSON alongside its copy.
    """
    if framework and framework != "auto":
        module = _load(framework)
        return module if suffix in module.SUFFIXES else None
    for name in _MODULES:
        module = _load(name)
        if suffix in module.SUFFIXES:
            return module
    return None

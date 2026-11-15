#!/usr/bin/env python3
"""
design_gate.py — the MECHANICAL layer of the shared design/template consistency gate.

Lays each changed route out in a real browser at every configured viewport and
theme, captures a full-page screenshot, and looks for the three defect classes
that source review cannot see:

  1. VOIDS      — a horizontal band of the page carrying no ink at all, taller
                  than the configured ceiling (default 120px). The motivating
                  case is a 177px void that shipped on a small business site
                  with every mechanical gate green.
  2. OVERFLOW   — the document scrolls horizontally at the viewport width.
  3. ZERO-INK   — a section box that exists in the DOM, occupies area, and
     SECTIONS    contains no ink. A section that rendered as nothing.

It emits a machine-readable report plus the screenshot set, which the JUDGMENT
layer (a reviewing agent that did NOT build the page — see SKILL.md) then audits
against the repo's design-system reference. This script never makes a taste
call; it only measures.

## Why pixels and not the DOM

Everything here is a computed layout fact. A void can be produced by a margin
three wrappers up, a grid row that collapsed, an image that 404'd, a section
that returned null for this data shape — none of which is a string a linter can
grep for, and none of which shows up in a DOM assertion written before the
defect existed. The screenshot is the only artefact that has already integrated
the whole cascade. So the primitive is: read the ink.

## What "ink-free" means

A row of pixels is ink-free when every pixel in it is the same colour, within
`ink_threshold`. That is deliberately background-AGNOSTIC: a 200px band of solid
pine with nothing in it is as empty as 200px of warm paper, and both read as a
hole to a person. Consecutive ink-free rows of the SAME colour form a segment.
A segment taller than the ceiling is a void.

Two refinements, each earned:

  - A full-width hairline rule is itself a uniform row, so a naive reading would
    treat `[80px gap][rule][80px gap]` as one 161px void. A uniform segment no
    taller than `rule_max_px` whose colour differs from the segments on both
    sides is a RULE, and rules are ink: they break a void rather than joining
    two.
  - A void touching the top or bottom edge of the capture is reported at
    severity 2, not 1. Page-top and page-bottom breathing room is a design
    decision; a hole punched between two blocks is not.

## Target fingerprinting — measuring the wrong server is its own failure class

Before it captures anything, the gate fetches one page (the `reference_page`,
falling back to the first route), and records what it actually connected to:
the resolved URL, the HTTP status, the byte count, a short content hash, and
any `<meta name="x-build-id">` the build stamped. All of it lands in
`report.json` under `target`, so two runs can be compared and a changed target
is visible rather than inferred.

This exists because of a real incident. A post-merge re-run
reported 10 severity-1 findings — including the exact voids the branch had just
repaired — because `.design-gate.json` pins `127.0.0.1:3000` and ANOTHER
session's `next dev`, running a DIFFERENT checkout, owned that port. The merged
tree sat unserved on 3100 and was never measured. Nothing errored, no
port-in-use warning fired, and the last line of the log read like a verdict.
Every consumer of this gate pins a localhost port, and every developer machine
runs several dev servers across worktrees: that is the normal state, not an
unlucky one.

The wasted round was the CHEAP outcome. The expensive one is the mirror case —
a stale server still serving the old, PASSING build, handing a broken change a
green. What caught it here was a page height that matched the pre-fix number to
the pixel. That is luck, not method.

So a consuming repo can set `expect_marker`: a string that must appear in the
fingerprint page's HTML (or, prefixed with `!`, must NOT appear) for the run to
count. You set it to the thing your change makes true — normally the build's
git SHA, stamped into a meta tag. If it does not match, the gate exits 2:
COULD NOT RUN, which this contract already words as a failure. A run that
measured something else must not read as red, and a run that measured nothing
must not read as green; both are the same rule.

## Exit codes — a skip is not a pass

  0  gate ran and found no severity-1 defect (PASS, or WARN with sev-2 only)
  1  gate ran and found at least one severity-1 defect (FAIL)
  2  gate COULD NOT RUN — no browser, unreachable base URL, bad config, a
     fingerprint page that answered with an HTTP error, or a target whose
     fingerprint does not match `expect_marker`. Nothing was measured (or what
     was measured was not the thing under test), so this is not evidence of
     anything. A run that skipped any capture (a page taller than
     `max_page_height_px`) is INCOMPLETE and also exits 2: an unmeasured route
     is not a passed route. Read the exit code, never the last line of the
     log. (A different gate in the same project once nearly recorded a green
     because a failure branch was worded like a skip.)

## Usage

    design_gate.py --config config/example-site.example.json
    design_gate.py --config <cfg> --base-url http://127.0.0.1:3100 \
                   --routes /about --expect-marker $(git rev-parse --short HEAD)
    design_gate.py --config <cfg> --serve out/           # static dir, ephemeral port
    design_gate.py --config <cfg> --out .design-gate/pr-91

Requires: playwright (Python) + a Chromium, pillow, numpy. See SKILL.md for the
browser-resolution order and the install line for each consuming repo.
"""

from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
import re
import socketserver
import sys
import threading
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

# ── config ───────────────────────────────────────────────────────────────────

DEFAULTS = {
    "repo": None,
    "base_url": "http://127.0.0.1:3000",
    "routes": ["/"],
    "reference_page": None,
    "design_system": [],
    "banlist": None,
    # A string that must appear in the fingerprint page's HTML for the run to
    # count. Prefix with "!" to require its ABSENCE instead. Normally the git
    # SHA the build stamped into <meta name="x-build-id">. See
    # `fingerprint_target` for why this exists.
    "expect_marker": None,
    "void_ceiling_px": 120,
    "near_ratio": 0.9,
    "report_edge_voids": False,
    "rule_max_px": 4,
    "ink_threshold": 8,
    "min_section_area_px": 4000,
    "viewports": [
        {"name": "mobile", "width": 390, "height": 844},
        {"name": "desktop", "width": 1440, "height": 1000},
    ],
    "themes": ["light", "dark"],
    "dark_mode": {"strategy": "media"},
    "disclosure_selectors": ["details:not([open])"],
    "expand_aria_toggles": False,
    "section_selector": "main section, main > article, main > div[id]",
    "ignore_selectors": [],
    "force_visible_selectors": [],
    "settle_ms": 400,
    "max_page_height_px": 30000,
    "out_dir": ".design-gate",
}

SCHEMA = "design-gate/1"


def load_config(path: Path) -> dict:
    raw = json.loads(path.read_text())
    cfg = dict(DEFAULTS)
    unknown = sorted(set(raw) - set(DEFAULTS))
    if unknown:
        die(f"unknown config key(s) in {path}: {', '.join(unknown)}")
    cfg.update(raw)
    cfg["_config_path"] = str(path)
    return cfg


def die(msg: str, code: int = 2) -> None:
    print(f"\nDESIGN GATE COULD NOT RUN (exit {code}) — {msg}", file=sys.stderr)
    print("Nothing was measured. This is not a pass.", file=sys.stderr)
    sys.exit(code)


# ── findings ─────────────────────────────────────────────────────────────────


@dataclass
class Finding:
    severity: int
    kind: str
    route: str
    viewport: str
    theme: str
    disclosures: str
    message: str
    capture: str = ""
    detail: dict = field(default_factory=dict)


# ── target fingerprinting ────────────────────────────────────────────────────

BUILD_ID_META = re.compile(
    r"""<meta[^>]*\bname=["']x-build-id["'][^>]*\bcontent=["']([^"']*)["']""", re.I)
BUILD_ID_META_REV = re.compile(
    r"""<meta[^>]*\bcontent=["']([^"']*)["'][^>]*\bname=["']x-build-id["']""", re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def fingerprint_target(cfg: dict) -> dict:
    """Fetch ONE page before any capture and record what we actually connected to.

    A design gate reports on the server it reached, not the tree you meant. On
    a machine running several dev servers across worktrees — the normal case —
    a pinned localhost port can belong to a different checkout entirely, and
    nothing about that situation errors: the pages load, the pixels are real,
    and the verdict is confident and about someone else's code. Fingerprinting
    turns that from an invisible substitution into a recorded fact, and, when
    `expect_marker` is set, into an exit 2.

    Deliberately a plain HTTP GET rather than a browser navigation: it happens
    before Chromium is launched, so a mismatch costs one request instead of a
    full capture run, and it reads the HTML the server actually sent rather
    than the DOM after hydration — which is what a build stamp lives in.
    """
    page = cfg.get("reference_page") or (cfg["routes"][0] if cfg["routes"] else "/")
    if not page.startswith("/"):
        page = "/" + page
    url = cfg["base_url"].rstrip("/") + page

    marker = cfg.get("expect_marker")
    mode, needle = "present", marker
    if marker and marker.startswith("!"):
        mode, needle = "absent", marker[1:]
    if marker and not needle:
        die("`expect_marker` is just \"!\" with nothing after it — that asserts nothing")

    req = urllib.request.Request(url, headers={"User-Agent": "design-gate/1 (fingerprint)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status, body, resolved = resp.status, resp.read(), resp.geturl()
    except urllib.error.HTTPError as e:
        # A non-2xx still tells us who is on the other end, so keep the body.
        status, body, resolved = e.code, (e.read() or b""), url
    except Exception as e:
        die(f"could not reach the target to fingerprint it: {url} — "
            f"{type(e).__name__}: {str(e).splitlines()[0][:160]}\n"
            "Nothing is listening there, or the dev server for THIS checkout is on a "
            "different port than the config pins. Pass --base-url explicitly.")

    text = body.decode("utf-8", "replace")
    m = BUILD_ID_META.search(text) or BUILD_ID_META_REV.search(text)
    t = TITLE_RE.search(text)

    fp = {
        "base_url": cfg["base_url"],
        "fingerprint_page": page,
        "url": resolved,
        "status": status,
        "bytes": len(body),
        "content_hash": "sha256:" + hashlib.sha256(body).hexdigest()[:16],
        "build_id": m.group(1) if m else None,
        "title": " ".join(t.group(1).split())[:120] if t else None,
        "expect_marker": marker,
        "marker_mode": mode if marker else None,
        "marker_ok": None,
    }

    if not 200 <= status < 300:
        die(f"the fingerprint page {resolved} answered HTTP {status}, not a success.\n"
            "An error page is not the site under test; capturing it would report a verdict "
            "about the wrong page. Fix the route, set `reference_page` to a page that "
            "exists, or pass the right --base-url.")

    if marker:
        hit = needle in text
        fp["marker_ok"] = hit if mode == "present" else not hit
        if not fp["marker_ok"]:
            observed = (f"its x-build-id is {fp['build_id']!r}"
                        if fp["build_id"] else "it carries no x-build-id meta tag")
            die(
                f"target fingerprint MISMATCH.\n"
                f"  target        {resolved}  (HTTP {status}, {fp['bytes']} bytes, "
                f"{fp['content_hash']})\n"
                f"  expected      {needle!r} to be {mode.upper()} in that page's HTML\n"
                f"  observed      it is {'absent' if mode == 'present' else 'present'}; "
                f"{observed}\n"
                "This is almost always another checkout's dev server answering on the "
                "port the config pins. Serve the tree under test and pass its "
                "--base-url. Refusing to report a verdict about a page that is not "
                "the one under test."
            )

    return fp


# ── the static server (for --serve) ──────────────────────────────────────────


def start_static_server(root: Path) -> tuple[str, socketserver.TCPServer]:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(root), **kw)

        def log_message(self, *a):  # quiet
            pass

    httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{httpd.server_address[1]}", httpd


# ── the in-page probe ────────────────────────────────────────────────────────

PROBE_JS = """
(args) => {
  const { sectionSelector, ignoreSelectors } = args;
  const de = document.documentElement;
  const vw = de.clientWidth;

  const ignored = (el) =>
    ignoreSelectors.some((s) => { try { return el.closest(s); } catch (e) { return false; } });

  /* Horizontal overflow, and who is causing it. Fixed/sticky chrome is measured
     too — a navbar that overflows is a real overflow. */
  const offenders = [];
  if (de.scrollWidth > vw + 1) {
    for (const el of document.querySelectorAll("body *")) {
      if (ignored(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      if (r.right > vw + 1 || r.left < -1) {
        /* Report the OUTERMOST offender in each subtree: a wide child inside a
           wide parent is one defect, not two. */
        if (offenders.some((o) => o.el.contains(el))) continue;
        offenders.push({
          el,
          tag: el.tagName.toLowerCase(),
          cls: (typeof el.className === "string" ? el.className : "").slice(0, 90),
          left: Math.round(r.left),
          right: Math.round(r.right),
          text: (el.textContent || "").trim().replace(/\\s+/g, " ").slice(0, 60),
        });
      }
    }
  }

  /* Section boxes in DOCUMENT coordinates, for the zero-ink test. */
  const sections = [];
  for (const el of document.querySelectorAll(sectionSelector)) {
    if (ignored(el)) continue;
    const s = getComputedStyle(el);
    if (s.display === "none" || s.visibility === "hidden") continue;
    const r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) continue;
    sections.push({
      tag: el.tagName.toLowerCase(),
      id: el.id || "",
      cls: (typeof el.className === "string" ? el.className : "").slice(0, 90),
      top: Math.round(r.top + window.scrollY),
      bottom: Math.round(r.bottom + window.scrollY),
      left: Math.round(r.left + window.scrollX),
      right: Math.round(r.right + window.scrollX),
      textLen: (el.textContent || "").trim().length,
    });
  }

  return {
    scrollWidth: de.scrollWidth,
    clientWidth: vw,
    docHeight: Math.max(de.scrollHeight, document.body ? document.body.scrollHeight : 0),
    overflow: Math.max(0, de.scrollWidth - vw),
    offenders: offenders.map(({ el, ...rest }) => rest).slice(0, 12),
    sections: sections.slice(0, 200),
    disclosures: document.querySelectorAll("details").length,
    h1s: document.querySelectorAll("h1").length,
  };
}
"""

# Kills animation so a capture is never a frame of a transition, and forces
# scroll-reveal elements visible. Without this, a `whileInView` block below the
# fold screenshots at opacity 0 and reads as a void that does not exist for a
# human who scrolled there.
FREEZE_CSS = """
*, *::before, *::after {
  animation-duration: 0s !important;
  animation-delay: 0s !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0s !important;
  transition-delay: 0s !important;
  caret-color: transparent !important;
}
"""


# ── ink analysis ─────────────────────────────────────────────────────────────


def analyse_ink(png_path: Path, cfg: dict) -> dict:
    """Row-uniformity segmentation of a full-page capture. Returns segments and
    a boolean per-row 'has ink' vector for the section test."""
    from PIL import Image
    import numpy as np

    with Image.open(png_path) as im:
        arr = np.asarray(im.convert("RGB"), dtype=np.int16)

    h, w = arr.shape[0], arr.shape[1]
    thr = cfg["ink_threshold"]

    spread = arr.max(axis=1) - arr.min(axis=1)          # (h, 3) per-row colour spread
    uniform = spread.max(axis=1) <= thr                  # (h,) row carries no ink
    row_color = arr.mean(axis=1)                         # (h, 3)

    # Group consecutive uniform rows of the same colour into segments.
    segments = []  # (start, end_exclusive, color)
    i = 0
    while i < h:
        if not uniform[i]:
            i += 1
            continue
        j = i + 1
        while j < h and uniform[j] and abs(row_color[j] - row_color[i]).max() <= thr:
            j += 1
        segments.append((i, j, row_color[i]))
        i = j

    # A short uniform segment whose colour differs from BOTH neighbours is a
    # rule (a hairline, a band edge), which is ink — it must not merge the gaps
    # on either side of it into one void.
    rule_max = cfg["rule_max_px"]
    is_rule = [False] * len(segments)
    for k, (s, e, c) in enumerate(segments):
        if e - s > rule_max:
            continue
        prev_c = segments[k - 1][2] if k > 0 and segments[k - 1][1] == s else None
        next_c = segments[k + 1][2] if k + 1 < len(segments) and segments[k + 1][0] == e else None
        # Neighbours are normally non-uniform (real content) rather than
        # segments; a rule sitting directly between two uniform gaps is the
        # case that matters, and both those gaps differ from it in colour.
        near_prev = prev_c is None or abs(prev_c - c).max() > thr
        near_next = next_c is None or abs(next_c - c).max() > thr
        if near_prev and near_next:
            is_rule[k] = True

    has_ink = ~uniform
    for k, (s, e, _) in enumerate(segments):
        if is_rule[k]:
            has_ink[s:e] = True

    # Re-segment against the corrected ink vector so rules split voids.
    voids = []
    i = 0
    while i < h:
        if has_ink[i]:
            i += 1
            continue
        j = i + 1
        while j < h and not has_ink[j] and abs(row_color[j] - row_color[i]).max() <= thr:
            j += 1
        voids.append({
            "top": i,
            "bottom": j,
            "height": j - i,
            "edge": i == 0 or j == h,
            "color": "#%02x%02x%02x" % tuple(int(round(v)) for v in row_color[i]),
        })
        i = j

    return {"height": h, "width": w, "has_ink": has_ink, "voids": voids}


def rows_have_ink(ink: dict, top: int, bottom: int) -> bool:
    """Cheap pre-filter: do any of the rows this section spans carry ink at all?

    A `False` here is conclusive — no ink in those rows means none in the
    section's box. A `True` is not, because the rows may be carrying a
    full-height sidebar's ink rather than the section's own, so the caller
    follows up with the box crop."""
    h = ink["height"]
    top = max(0, min(h - 1, top))
    bottom = max(top + 1, min(h, bottom))
    return bool(ink["has_ink"][top:bottom].any())


def crop_has_ink(png_path: Path, box: tuple[int, int, int, int], thr: int) -> bool:
    from PIL import Image
    import numpy as np

    left, top, right, bottom = box
    with Image.open(png_path) as im:
        im = im.convert("RGB")
        right = min(right, im.width)
        bottom = min(bottom, im.height)
        if right - left < 2 or bottom - top < 2:
            return True  # too small to judge; do not accuse
        crop = np.asarray(im.crop((left, top, right, bottom)), dtype=np.int16)
    return bool((crop.max(axis=(0, 1)) - crop.min(axis=(0, 1))).max() > thr)


# ── capture + check one (route, viewport, theme, disclosures) ────────────────


def run_case(page, url, route, vp, theme, disclosures, out_dir, cfg, findings, captures):
    from playwright.sync_api import Error as PWError

    tag = f"{slug(route)}__{vp['name']}-{vp['width']}__{theme}__{disclosures}"
    shot = out_dir / "screenshots" / f"{tag}.png"
    shot.parent.mkdir(parents=True, exist_ok=True)

    try:
        page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
        resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
        # An error page lays out fine and can look clean; it is not the route under test.
        # 304 is a cache revalidation of a page that exists.
        if resp is None or not (200 <= resp.status < 300 or resp.status == 304):
            findings.append(Finding(
                1, "http-error", route, vp["name"], theme, disclosures,
                "the route did not answer with a success, so it was not measured: "
                + (f"HTTP {resp.status}" if resp is not None else "no navigation response"),
            ))
            return None
        page.add_style_tag(content=FREEZE_CSS)
        if cfg["force_visible_selectors"]:
            sel = ", ".join(cfg["force_visible_selectors"])
            page.add_style_tag(content=f"{sel} {{ opacity: 1 !important; transform: none !important; }}")
        page.evaluate("() => document.fonts && document.fonts.ready")
        # Walk the page so scroll-reveal content commits, then return to the top.
        page.evaluate(
            """async () => {
              const h = document.documentElement.scrollHeight;
              for (let y = 0; y < h; y += Math.max(200, window.innerHeight * 0.8)) {
                window.scrollTo(0, y);
                await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 30)));
              }
              window.scrollTo(0, 0);
              await new Promise((r) => setTimeout(r, 60));
            }"""
        )
        if disclosures == "open":
            page.evaluate(
                """(sels) => {
                  for (const s of sels) {
                    for (const el of document.querySelectorAll(s)) {
                      if (el.tagName === "DETAILS") el.open = true;
                      else if (el.click) el.click();
                    }
                  }
                }""",
                cfg["disclosure_selectors"],
            )
            if cfg["expand_aria_toggles"]:
                page.evaluate(
                    """() => {
                      for (const el of document.querySelectorAll('[aria-expanded="false"]')) {
                        try { el.click(); } catch (e) {}
                      }
                    }"""
                )
        page.wait_for_timeout(cfg["settle_ms"])

        probe = page.evaluate(PROBE_JS, {
            "sectionSelector": cfg["section_selector"],
            "ignoreSelectors": cfg["ignore_selectors"],
        })

        if probe["docHeight"] > cfg["max_page_height_px"]:
            findings.append(Finding(
                2, "page-too-tall", route, vp["name"], theme, disclosures,
                f"page is {probe['docHeight']}px tall; capture skipped above "
                f"{cfg['max_page_height_px']}px ceiling",
            ))
            return None

        page.screenshot(path=str(shot), full_page=True, animations="disabled")
    except PWError as e:
        findings.append(Finding(
            1, "capture-failed", route, vp["name"], theme, disclosures,
            f"the page could not be laid out and captured: {str(e).splitlines()[0][:160]}",
        ))
        return None

    rel = str(shot.relative_to(out_dir))
    captures.append({
        "route": route, "viewport": vp["name"], "width": vp["width"],
        "theme": theme, "disclosures": disclosures, "path": rel,
        "page_height": probe["docHeight"], "h1_count": probe["h1s"],
    })

    # 1 ── horizontal overflow
    if probe["overflow"] > 1:
        findings.append(Finding(
            1, "overflow", route, vp["name"], theme, disclosures,
            f"document scrolls horizontally by {probe['overflow']}px at "
            f"{probe['clientWidth']}px (scrollWidth {probe['scrollWidth']})",
            rel, {"overflow_px": probe["overflow"], "offenders": probe["offenders"]},
        ))

    # 2 ── voids
    ink = analyse_ink(shot, cfg)
    ceiling = cfg["void_ceiling_px"]
    near = ceiling * cfg["near_ratio"]
    for v in ink["voids"]:
        if v["height"] <= near:
            continue
        if v["edge"]:
            # Paper at the very top or bottom of a capture is not a hole in a
            # page. It is the masthead's breathing room, the footer's, or — on a
            # page shorter than the fold — the viewport itself. Reporting it by
            # default made the clean control noisier than the broken fixtures,
            # which is how a gate teaches people to ignore it.
            if not cfg["report_edge_voids"] or v["height"] <= ceiling:
                continue
            sev, kind = 2, "void-edge"
            msg = (f"{v['height']}px ink-free at the page {'top' if v['top'] == 0 else 'bottom'} "
                   f"(ceiling {ceiling}px, ground {v['color']})")
        elif v["height"] > ceiling:
            sev, kind = 1, "void"
            msg = (f"{v['height']}px of ink-free page between y={v['top']} and "
                   f"y={v['bottom']} (ceiling {ceiling}px, ground {v['color']})")
        else:
            sev, kind = 2, "void-near"
            msg = (f"{v['height']}px ink-free between y={v['top']} and y={v['bottom']} — "
                   f"within {int(cfg['near_ratio'] * 100)}% of the {ceiling}px ceiling, watch it")
        findings.append(Finding(sev, kind, route, vp["name"], theme, disclosures, msg, rel, v))

    # 3 ── zero-ink sections
    for s in probe["sections"]:
        area = (s["right"] - s["left"]) * (s["bottom"] - s["top"])
        if area < cfg["min_section_area_px"]:
            continue
        has = rows_have_ink(ink, s["top"], s["bottom"]) and crop_has_ink(
            shot, (s["left"], s["top"], s["right"], s["bottom"]), cfg["ink_threshold"])
        if not has:
            ident = f"{s['tag']}{('#' + s['id']) if s['id'] else ''}"
            findings.append(Finding(
                1, "zero-ink-section", route, vp["name"], theme, disclosures,
                f"section {ident} occupies {s['right'] - s['left']}×"
                f"{s['bottom'] - s['top']}px and renders no ink"
                + (f" (its DOM text is {s['textLen']} chars — it is there and invisible)"
                   if s["textLen"] else " (and carries no text)"),
                rel, s,
            ))

    return probe


def slug(route: str) -> str:
    s = route.strip("/").replace("/", "-") or "root"
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in s)


# ── judgment packet ──────────────────────────────────────────────────────────


def write_packet(out_dir: Path, cfg: dict, report: dict) -> Path:
    p = out_dir / "judgment-packet.md"
    ds = cfg["design_system"] or ["(none configured — set `design_system` in the config)"]
    lines = [
        "# Design gate — judgment packet",
        "",
        f"Repo: **{cfg['repo'] or '(unnamed)'}**  ·  base URL: `{cfg['base_url']}`  ·  "
        f"generated {report['generated_at']}",
        "",
        "## Target (what was actually measured)",
        "",
    ]
    t = report.get("target") or {}
    lines += [
        f"- Fetched `{t.get('url')}` — HTTP `{t.get('status')}`, {t.get('bytes')} bytes, "
        f"content hash `{t.get('content_hash')}`",
        f"- Build id (`<meta name=\"x-build-id\">`): `{t.get('build_id') or '(none stamped)'}`",
        f"- Expected marker: `{t.get('expect_marker') or '(none set)'}`"
        + (f" — {t.get('marker_mode')}, MATCHED" if t.get("marker_ok") else ""),
        "",
        "If this is not the tree under review, stop: the findings below are about",
        "some other server. Every consumer pins a localhost port and every machine",
        "runs several dev servers.",
        "",
        "The mechanical layer has run. Its verdict is "
        f"**{report['verdict']}** ({report['summary']['severity_1']} severity-1, "
        f"{report['summary']['severity_2']} severity-2).",
        "",
        "## Your job (judgment layer)",
        "",
        "You must NOT be the agent that built these pages. Read every screenshot",
        "below and audit it against the design-system reference for the six",
        "judgment checks in SKILL.md: single label grammar, heading-scale",
        "conformance, spacing rhythm, banned devices, theme parity, and",
        "self-consistency (a page must not contradict its own legend).",
        "",
        "## Reference",
        "",
        "- Design system: " + ", ".join(f"`{d}`" for d in ds),
        f"- Reference page (the canonical example of a conforming page): "
        f"`{cfg['reference_page'] or '(none configured)'}`",
        f"- Banned-device list: `{cfg['banlist'] or '(none configured)'}`",
        "",
        "## Captures",
        "",
    ]
    by_route: dict[str, list] = {}
    for c in report["captures"]:
        by_route.setdefault(c["route"], []).append(c)
    for route, caps in by_route.items():
        lines.append(f"### `{route}`")
        lines.append("")
        for c in caps:
            lines.append(
                f"- `{c['path']}` — {c['viewport']} {c['width']}px, {c['theme']} theme, "
                f"disclosures {c['disclosures']}, page height {c['page_height']}px, "
                f"{c['h1_count']} h1"
            )
        lines.append("")
    if report["findings"]:
        lines += ["## Mechanical findings (already recorded — do not re-report)", ""]
        for f in report["findings"]:
            lines.append(
                f"- **sev{f['severity']} {f['kind']}** `{f['route']}` "
                f"{f['viewport']}/{f['theme']}/{f['disclosures']} — {f['message']}"
            )
        lines.append("")
    lines += [
        "## How to record your findings",
        "",
        "Append a `judgment` object to `report.json` with the same finding shape",
        "(`severity`, `kind`, `route`, `viewport`, `theme`, `message`), then state the",
        "combined verdict. A banned device, a broken theme, or a page contradicting",
        "itself is severity 1 and FAILS the PR ritual. Grammar, scale and rhythm",
        "drift are severity 2 unless they make the page unreadable.",
        "",
    ]
    p.write_text("\n".join(lines))
    return p


# ── main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(description="Mechanical layer of the design consistency gate.")
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--routes", help="comma-separated override of the config's routes")
    ap.add_argument("--base-url", help="override the config's base_url")
    ap.add_argument("--expect-marker", help=(
        "a string that must appear in the fingerprint page's HTML for this run to count "
        "(prefix with '!' to require its absence). Normally the build's git SHA. "
        "A mismatch exits 2 — could not run — rather than reporting a verdict about "
        "whatever server happened to answer."))
    ap.add_argument("--serve", type=Path, help="serve this directory on an ephemeral port and use it as the base URL")
    ap.add_argument("--out", type=Path, help="output directory (default: config out_dir)")
    ap.add_argument("--ceiling", type=int, help="override void_ceiling_px")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not args.config.exists():
        die(f"config not found: {args.config}")
    cfg = load_config(args.config)

    if args.routes:
        cfg["routes"] = [r if r.startswith("/") else "/" + r for r in args.routes.split(",") if r.strip()]
    if args.base_url:
        cfg["base_url"] = args.base_url
    if args.ceiling:
        cfg["void_ceiling_px"] = args.ceiling
    if args.expect_marker:
        cfg["expect_marker"] = args.expect_marker
    if not cfg["routes"]:
        die("no routes to check — pass --routes or set `routes` in the config")

    httpd = None
    if args.serve:
        if not args.serve.is_dir():
            die(f"--serve path is not a directory: {args.serve}")
        cfg["base_url"], httpd = start_static_server(args.serve.resolve())

    out_dir = (args.out or Path(cfg["out_dir"])).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Assert what we are about to measure BEFORE spending a browser on it. A
    # mismatch here costs one HTTP request; discovering it after the fact costs
    # a whole review round, and not discovering it costs a false verdict.
    target = fingerprint_target(cfg)
    if not args.quiet:
        bits = [f"target: {target['url']}", f"HTTP {target['status']}",
                target["content_hash"], f"{target['bytes']}B"]
        if target["build_id"]:
            bits.append(f"x-build-id={target['build_id']}")
        if target["marker_ok"] is not None:
            bits.append(f"marker {target['marker_mode']} OK")
        print("  ·  ".join(bits))

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        die("Playwright is not installed. `pip install playwright && playwright install chromium`, "
            "or point CHROME_PATH at an existing Chrome.")

    findings: list[Finding] = []
    captures: list[dict] = []

    launch_kw = {"args": ["--hide-scrollbars", "--force-device-scale-factor=1"]}
    chrome = os.environ.get("CHROME_PATH") or os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if chrome:
        launch_kw["executable_path"] = chrome

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(**launch_kw)
        except Exception as e:
            try:
                browser = pw.chromium.launch(channel="chrome", args=launch_kw["args"])
            except Exception:
                die("no Chromium could be launched. Install one with `playwright install chromium`, "
                    f"or set CHROME_PATH. Original error: {str(e).splitlines()[0][:160]}")

        dm = cfg["dark_mode"]
        for theme in cfg["themes"]:
            ctx_kw = {"device_scale_factor": 1, "reduced_motion": "reduce"}
            if dm.get("strategy") == "media":
                ctx_kw["color_scheme"] = theme
            ctx = browser.new_context(**ctx_kw)
            if dm.get("strategy") == "localstorage":
                key = dm.get("key", "theme")
                val = dm.get("value", "dark") if theme == "dark" else dm.get("light_value", "light")
                klass = dm.get("class", "dark")
                ctx.add_init_script(
                    f"""try {{ localStorage.setItem({json.dumps(key)}, {json.dumps(val)}); }} catch (e) {{}}
                        document.addEventListener("DOMContentLoaded", () => {{
                          document.documentElement.classList.toggle({json.dumps(klass)}, {json.dumps(theme == 'dark')});
                        }});"""
                )
            page = ctx.new_page()

            for route in cfg["routes"]:
                url = cfg["base_url"].rstrip("/") + route
                for vp in cfg["viewports"]:
                    probe = run_case(page, url, route, vp, theme, "closed",
                                     out_dir, cfg, findings, captures)
                    # A second pass with every disclosure open, but only where a
                    # disclosure exists: a route with no <details> must not
                    # double its capture count for nothing.
                    if probe and probe.get("disclosures"):
                        run_case(page, url, route, vp, theme, "open", out_dir, cfg, findings, captures)
            ctx.close()
        browser.close()

    if httpd:
        httpd.shutdown()

    sev1 = sum(1 for f in findings if f.severity == 1)
    sev2 = sum(1 for f in findings if f.severity == 2)
    verdict = "FAIL" if sev1 else ("WARN" if sev2 else "PASS")
    if not captures:
        verdict = "FAIL"  # zero captures is never a pass, and report.json must say so
    # A skipped capture means a route/viewport/theme went unmeasured: the run is
    # incomplete, never a pass, whatever the other captures found.
    skipped = [asdict(f) for f in findings if f.kind == "page-too-tall"]
    if skipped and captures:
        verdict = "INCOMPLETE"

    report = {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo": cfg["repo"],
        "config": cfg["_config_path"],
        "base_url": cfg["base_url"],
        # What the gate actually connected to. Compare this between runs before
        # comparing findings between runs — see `fingerprint_target`.
        "target": target,
        "ceiling_px": cfg["void_ceiling_px"],
        "reference_page": cfg["reference_page"],
        "design_system": cfg["design_system"],
        "banlist": cfg["banlist"],
        "routes": cfg["routes"],
        "captures": captures,
        "findings": [asdict(f) for f in findings],
        "summary": {
            "routes": len(cfg["routes"]),
            "captures": len(captures),
            "severity_1": sev1,
            "severity_2": sev2,
            "skipped": len(skipped),
        },
        "complete": not skipped and bool(captures),
        "skipped": skipped,
        "verdict": verdict,
        "judgment": {"status": "pending",
                     "note": "the judgment layer has not run; a mechanical PASS is half a gate"},
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2))
    packet = write_packet(out_dir, cfg, report)

    if not args.quiet:
        for f in findings:
            print(f"sev{f.severity}  {f.kind:<20} {f.route}  [{f.viewport}/{f.theme}/"
                  f"{f.disclosures}]  {f.message}")
        print()
    # Checked even with --quiet: zero captures is never a pass.
    if not captures:
        die("0 captures were taken across "
            f"{len(cfg['routes'])} route(s) — nothing was measured")
    # Checked even with --quiet: an unmeasured route is not a passed route.
    if skipped:
        print(f"\nDESIGN GATE INCOMPLETE (exit 2) — {len(skipped)} capture(s) were skipped "
              f"(page taller than {cfg['max_page_height_px']}px), so those routes were not "
              "measured. Raise max_page_height_px or shorten the page, then run again.\n"
              f"report.json says verdict INCOMPLETE: {out_dir / 'report.json'}\n"
              "An unmeasured route is not a pass.", file=sys.stderr)
        sys.exit(2)
    if not args.quiet:
        print(f"DESIGN GATE (mechanical) {verdict} — {sev1} severity-1, {sev2} severity-2 "
              f"across {len(captures)} captures of {len(cfg['routes'])} route(s).")
        print(f"  report:     {out_dir / 'report.json'}")
        print(f"  screenshots:{out_dir / 'screenshots'}")
        print(f"  judgment:   {packet}")
        if verdict != "FAIL":
            print("\nA mechanical PASS is HALF the gate. The judgment layer still has to run,")
            print("and it must be an agent that did not build these pages. See SKILL.md.")

    return 1 if sev1 else 0


if __name__ == "__main__":
    sys.exit(main())

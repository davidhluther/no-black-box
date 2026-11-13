#!/usr/bin/env python3
"""Render a single-series horizontal bar chart from a JSON spec, deterministically.

Usage: render_chart.py spec.json [--params guidelines/VISUAL_ASSETS_PARAMS.json]
Spec: {"title", "subtitle"?, "bars": [{"label", "value", "display", "emph": bool}], "source", "out",
       "palette": {"emph", "base", "text", "muted", "bg"}, "width_px": 1600}
Every printed number comes from the spec's "display" strings, so the QA step is a string
match against the final, never a reading of pixels. One series, so no legend; the emphasized
bar is the only colored mark and every bar is direct-labeled.
"""
import json, sys, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Brand-neutral fallback; brand values come from the consuming repo's VISUAL_ASSETS_PARAMS.json.
DEFAULT = {"emph": "#1F5FAD", "base": "#8A8A8A", "text": "#1A1A1A", "muted": "#666666", "bg": "#FFFFFF"}


def pick_font(prefs=()):
    have = {f.name for f in font_manager.fontManager.ttflist}
    for name in (*prefs, "Helvetica Neue", "Helvetica", "Arial"):
        if name in have:
            return name
    return "DejaVu Sans"


LABEL_CHARS = 26  # fits the 34% label column at 1600 px and 11 pt


def wrap_label(label):
    return "\n".join(textwrap.wrap(label, LABEL_CHARS)) or label


def apply_params(spec, params_path):
    """Merge a brand profile (palette, font_preference, domain_mark) under the spec's own keys."""
    if not params_path:
        return spec
    p = json.load(open(params_path))
    pal = {k: v for k, v in p.get("palette", {}).items() if k in DEFAULT}
    return {"font_preference": p.get("font_preference", []), "domain_mark": p.get("domain_mark", ""),
            **spec, "palette": {**pal, **spec.get("palette", {})}}


def cli(render):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--params", help="consuming repo's guidelines/VISUAL_ASSETS_PARAMS.json")
    a = ap.parse_args()
    print(render(apply_params(json.load(open(a.spec)), a.params)))


def render(spec):
    pal = {**DEFAULT, **spec.get("palette", {})}
    bars = spec["bars"]
    width_px = spec.get("width_px", 1600)
    dpi = 200
    row_in = 0.5
    h_in = 1.9 + row_in * len(bars) + 0.7
    w_in = width_px / dpi
    plt.rcParams["font.family"] = pick_font(spec.get("font_preference", []))
    fig = plt.figure(figsize=(w_in, h_in), dpi=dpi, facecolor=pal["bg"])
    top = 1 - 1.25 / h_in
    bottom = 0.75 / h_in
    ax = fig.add_axes([0.34, bottom, 0.56, top - bottom], facecolor=pal["bg"])
    ys = list(range(len(bars)))[::-1]
    vmax = max(b["value"] for b in bars)
    for y, b in zip(ys, bars):
        color = pal["emph"] if b.get("emph") else pal["base"]
        ax.barh(y, b["value"], height=0.62, color=color, linewidth=0)
        ax.text(b["value"] + vmax * 0.015, y, b["display"], va="center", ha="left",
                fontsize=11, color=pal["text"], fontweight="bold" if b.get("emph") else "normal")
    ax.set_yticks(ys)
    ax.set_yticklabels([wrap_label(b["label"]) for b in bars], fontsize=11, color=pal["text"])
    ax.set_xlim(0, vmax * 1.18)
    ax.set_xticks([])
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(pal["muted"])
    ax.tick_params(axis="y", length=0, pad=8)
    fig.text(0.04, 1 - 0.45 / h_in, spec["title"], fontsize=15, fontweight="bold",
             color=pal["text"], ha="left", va="top")
    if spec.get("subtitle"):
        fig.text(0.04, 1 - 0.85 / h_in, spec["subtitle"], fontsize=10.5, color=pal["muted"], ha="left", va="top")
    fig.text(0.04, 0.32 / h_in, spec["source"], fontsize=9, color=pal["muted"], ha="left", va="center")
    if spec.get("domain_mark"):
        fig.text(0.96, 0.32 / h_in, spec["domain_mark"], fontsize=9, color=pal["muted"], ha="right", va="center")
    fig.savefig(spec["out"], dpi=dpi, facecolor=pal["bg"], metadata={"Software": None})
    plt.close(fig)
    return spec["out"]


if __name__ == "__main__":
    cli(render)

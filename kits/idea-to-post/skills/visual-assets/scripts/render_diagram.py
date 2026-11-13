#!/usr/bin/env python3
"""Render a step diagram (one or more horizontal lanes of numbered steps) from a JSON spec.

Spec: {"title", "subtitle"?, "lanes": [{"name"?, "steps": [{"head", "body"?}], "emph_step"?: int}],
       "footer"?, "out", "width_px": 1600}
Step text is copied verbatim from the final, so QA is a string match. Plain boxes joined by
straight connectors; one magenta step per lane at most (the step the article is about).
"""
import json, sys, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from render_chart import DEFAULT, pick_font, cli


def render(spec):
    pal = {**DEFAULT, **spec.get("palette", {})}
    lanes = spec["lanes"]
    n = max(len(l["steps"]) for l in lanes)
    width_px = spec.get("width_px", 1600)
    dpi = 200
    w_in = width_px / dpi
    lane_h = 1.55
    h_in = 1.25 + lane_h * len(lanes) + (0.5 if spec.get("footer") else 0.25)
    plt.rcParams["font.family"] = pick_font(spec.get("font_preference", []))
    fig = plt.figure(figsize=(w_in, h_in), dpi=dpi, facecolor=pal["bg"])
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w_in); ax.set_ylim(0, h_in); ax.axis("off")
    ax.text(0.32, h_in - 0.35, spec["title"], fontsize=15, color=pal["text"], va="top", ha="left")
    if spec.get("subtitle"):
        ax.text(0.32, h_in - 0.75, spec["subtitle"], fontsize=10.5, color=pal["muted"], va="top", ha="left")
    has_names = any(l.get("name") for l in lanes)
    x0 = 1.55 if has_names else 0.32
    gap = 0.22
    box_w = (w_in - x0 - 0.32 - gap * (n - 1)) / n
    box_h = 1.12
    for li, lane in enumerate(lanes):
        y_top = h_in - 1.0 - li * lane_h
        y = y_top - box_h
        if lane.get("name"):
            ax.text(0.32, y + box_h / 2, "\n".join(textwrap.wrap(lane["name"], 14)), fontsize=10.5,
                    color=pal["text"], va="center", ha="left", fontweight="bold")
        for si, st in enumerate(lane["steps"]):
            x = x0 + si * (box_w + gap)
            emph = lane.get("emph_step") == si + 1
            face = pal["emph"] if emph else "#FFFFFF"
            ink = "#FFFFFF" if emph else pal["text"]
            sub = "#FFFFFF" if emph else pal["muted"]
            ax.add_patch(FancyBboxPatch((x, y), box_w, box_h, boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor=face, edgecolor=pal["muted"] if not emph else face, linewidth=0.8))
            chars = max(10, int(box_w * 16))
            head = "\n".join(textwrap.wrap(f"{si + 1}. {st['head']}", chars))
            ax.text(x + 0.1, y + box_h - 0.1, head, fontsize=9.5, color=ink, va="top", ha="left", fontweight="bold")
            if st.get("body"):
                body = "\n".join(textwrap.wrap(st["body"], int(chars * 1.12)))
                lines = head.count("\n") + 1
                ax.text(x + 0.1, y + box_h - 0.14 - 0.19 * lines, body, fontsize=8, color=sub, va="top", ha="left")
            if si < len(lane["steps"]) - 1:
                ax.plot([x + box_w, x + box_w + gap], [y + box_h / 2] * 2, color=pal["muted"], linewidth=1)
    if spec.get("footer"):
        ax.text(0.32, 0.28, spec["footer"], fontsize=9, color=pal["muted"], va="center", ha="left")
    if spec.get("domain_mark"):
        ax.text(w_in - 0.32, 0.28, spec["domain_mark"], fontsize=9, color=pal["muted"], va="center", ha="right")
    fig.savefig(spec["out"], dpi=dpi, facecolor=pal["bg"], metadata={"Software": None})
    plt.close(fig)
    return spec["out"]


if __name__ == "__main__":
    cli(render)

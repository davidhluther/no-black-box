"""Build the phone-ready funding pipeline page (a single HTML file, publishable as an Artifact).

Reads START-HERE.md, the four tracker CSVs and the funder dossiers in paths.data_dir and
writes paths.html_out. Optional links.json there ({"sheet": url, "folder": url, ...}) adds
Drive links. Names, colors, prose, statuses, stages and dossier tiers come from the config.

Run:  python3 engine/build_page.py --config orgs/<slug>.json
"""
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gp_common as gp  # noqa: E402

DEFAULT_PALETTE = {
    "light": {"bg": "#f6f7f3", "panel": "#ffffff", "fg": "#1f2a24", "muted": "#5d6b62",
              "rule": "#d5ddd6", "accent": "#2f6b4f", "won": "#2f6b4f", "lost": "#9a3b2a",
              "unknown": "#8a6a12", "open": "#36577f"},
    "dark": {"bg": "#141a17", "panel": "#1b231f", "fg": "#e3eae5", "muted": "#9fb0a5",
             "rule": "#2e3a33", "accent": "#7cc4a0", "won": "#7cc4a0", "lost": "#e58c78",
             "unknown": "#e0bd5c", "open": "#8fb4e3"},
    "display": '"Fraunces", Georgia, serif',
    "body": '"Public Sans", system-ui, sans-serif',
    "fonts_url": "",
}
DEFAULT_LINK_LABELS = [["sheet", "Grants Pipeline Tracker (Google Sheet)"],
                       ["doc", "This page as a Google Doc"],
                       ["note", "What to move on soon"],
                       ["folder", "Drive folder"]]
DEFAULT_STATUS_FILTERS = [["all", "All"], ["won", "Awarded"], ["unknown", "Outcome unknown"],
                          ["open", "Prospects"], ["lost", "Declined"]]
DEFAULT_STAT_LABELS = ["grant asks on record", "awarded", "awarded in all",
                       "with no recorded outcome", "named prospects next",
                       "in opening asks to test"]


def money(v):
    v = (v or "").strip()
    # Nonnumeric amounts ("TBD", free text) go into the page as text, never as markup.
    return f"${float(v):,.0f}" if re.fullmatch(r"[\d.]+", v) else html.escape(v)


SAFE_HREF = re.compile(r"^(https?:|mailto:|#)", re.I)


def md(text):
    # Research and dossier text can carry web-sourced strings: no raw HTML, no script: links.
    out = markdown.markdown(text.replace("<", "&lt;"), extensions=["tables"])
    return re.sub(r'href="(?!https?:|mailto:|#)[^"]*"', 'href="#"', out, flags=re.I)


def safe_url(url):
    return url if url and SAFE_HREF.match(url.strip()) else ""


def esc(s):
    return html.escape(s, quote=False)


def tier_cfg(cfg):
    return {"order": ["A", "B", "C"], "default": "A", **cfg.get("dossier_tiers", {})}


def dossiers(cfg):
    out = []
    for p in sorted(cfg["paths"]["dossiers_dir"].glob("*.md")):
        text = p.read_text()
        meta, body = {}, text
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.split("#")[0].strip().strip('"')
            body = m.group(2)
        out.append((meta, body, p.stem))
    order = {t: i for i, t in enumerate(tier_cfg(cfg)["order"])}
    return sorted(out, key=lambda d: (order.get(d[0].get("priority_tier", "C")[:1], 3), d[2]))


def a(text, url):
    t = html.escape(text)
    url = safe_url(url)
    return f'<a href="{html.escape(url)}">{t}</a>' if url else t


def evidence(r):
    parts = []
    for part in (r.get("links") or "").split(" ;; "):
        if "|" in part:
            label, url = part.split("|", 1)
            parts.append(a(label.strip(), url.strip()))
    return " | ".join(parts)


def stage_key(label):
    return re.sub(r"\W+", "-", label.lower()).strip("-")


def css_vars(pal, dark):
    x = pal["dark" if dark else "light"]
    line1 = (f"  --bg: {x['bg']}; --panel: {x['panel']}; --fg: {x['fg']}; "
             f"--muted: {x['muted']}; --rule: {x['rule']};\n")
    line2 = (f"  --accent: {x['accent']}; --won: {x['won']}; --lost: {x['lost']}; "
             f"--unknown: {x['unknown']}; --open: {x['open']};")
    if dark:
        return line1 + line2 + " color-scheme: dark"
    return line1 + line2 + f"\n  --display: {pal['display']}; --body: {pal['body']};\n"


def build(cfg):
    P = cfg["paths"]
    TXT = cfg["text"]["page"]
    org = cfg["org"]["name"]
    pal = {**DEFAULT_PALETTE, **cfg["theme"].get("page", {})}
    sclass = gp.status_class(cfg)
    won_names = gp.roles(cfg, "awarded", "awarded_reduced")
    unknown_names = gp.roles(cfg, "unknown")
    prospect_names = gp.roles(cfg, "prospect")

    start = P["start_here"].read_text()
    title_line, _, rest = start.partition("\n")
    intro, _, sections = rest.partition("\n## ")
    links = {}
    if P["links_json"].exists():
        links = json.loads(P["links_json"].read_text())

    pipe = gp.read_csv(P["pipeline_csv"])
    won = [r for r in pipe if r["status"] in won_names]
    total = sum(float(r["award"]) for r in won if r["award"])
    unknown = sum(r["status"] in unknown_names for r in pipe)
    asks = sum(r["status"] not in prospect_names for r in pipe)
    prospects = [r for r in pipe if r["status"] in prospect_names]

    trs = []
    for r in pipe:
        cls = sclass.get(r["status"], "open")
        amt = money(r["award"]) if r["status"] in won_names else money(r["request"])
        trs.append(
            f'<tr data-s="{cls}"><td><b>{a(r["funder"], r.get("funder_url"))}</b>'
            f'<span class="sub">{html.escape(r["purpose"])}</span></td>'
            f'<td class="st {cls}">{html.escape(r["status"])}</td>'
            f'<td class="num">{amt}</td>'
            f'<td>{html.escape(r["decision"] or r["submitted"])}</td>'
            f'<td class="notes">{html.escape(r["notes"])}'
            f'<span class="src">Source: {html.escape(r["source"])}</span>'
            f'<span class="src">Links: {evidence(r)}</span></td></tr>')

    intel = "".join(
        f'<tr><td><b>{a(r["stream"], r.get("funder_url"))}</b></td><td>{html.escape(r["verdict"])}</td>'
        f'<td class="notes">{html.escape(r["action"])}'
        f'<span class="src">Links: {evidence(r)}</span></td></tr>'
        for r in gp.read_csv(P["intel_csv"]))

    stages = [(stage_key(s), s) for s in cfg.get("stages", [])]
    wide = []
    for r in gp.read_csv(P["wider_net_csv"]):
        key = stage_key(r["stage"])
        if key not in [k for k, _ in stages]:
            stages.append((key, r["stage"]))
        wide.append(
            f'<tr data-g="{key}"><td><b>{a(r["funder"], r.get("funder_url"))}</b>'
            f'<span class="sub">{html.escape(r["stage"])} | {html.escape(r["lens"])}</span></td>'
            f'<td class="st">{html.escape(r["verdict"])}</td>'
            f'<td>{html.escape(r["award"])}</td><td>{html.escape(r["window"])}</td>'
            f'<td class="notes">{html.escape(r["angle"])}'
            f'<span class="src">How: {html.escape(r["path"])}</span>'
            f'<span class="src">Needs: {html.escape(r["prereq"])}</span>'
            f'<span class="src">Links: {evidence(r)}</span></td></tr>')
    stage_btns = "".join(
        f'<button type="button" data-g="{k}" aria-pressed="false">{html.escape(label)}</button>'
        for k, label in stages)

    dos = []
    for meta, body, slug in dossiers(cfg):
        name = meta.get("funder", slug)
        line = " | ".join(x for x in (f'Tier {meta.get("priority_tier", "?")}',
                                       meta.get("status", ""), meta.get("city_state", "")) if x)
        dos.append(f'<details id="{slug}"><summary><span class="dn">{html.escape(name)}</span>'
                   f'<span class="dm">{html.escape(line)}</span></summary>'
                   f'<div class="dbody">{md(body)}</div></details>')

    idx = gp.read_csv(P["dossier_index_csv"])
    slug_of = {}
    if P["dossier_urls"].exists():
        slug_of = {u: s for s, u in json.loads(P["dossier_urls"].read_text()).items()}

    def name_cell(r):
        n = html.escape(r["funder"])
        slug = slug_of.get(r["dossier"])
        if slug:
            return f'<a href="#{slug}">{n}</a>'
        return a(r["funder"], "https://projects.propublica.org/nonprofits/search?q=" + quote_plus(r["funder"]))

    idx_rows = "".join(
        f'<tr data-t="{html.escape(r["tier"])}"><td><b>{name_cell(r)}</b>'
        f'<span class="sub">{html.escape(r["city"])}</span></td><td>{html.escape(r["tier"])}</td>'
        f'<td>{html.escape(r["status"])}</td><td>{html.escape(r["ask"])}</td>'
        f'<td class="notes">{html.escape(r["angle"])}</td></tr>'
        for r in idx)

    tc = tier_cfg(cfg)
    pressed = lambda on: str(on).lower()  # noqa: E731
    tier_btns = (f'<button type="button" data-t="all" aria-pressed="{pressed(tc["default"] == "all")}">All tiers</button>\n'
                 + "\n".join(f'<button type="button" data-t="{t}" aria-pressed="{pressed(tc["default"] == t)}">Tier {t}</button>'
                             for t in tc["order"]))
    status_btns = "\n".join(
        f'<button type="button" data-f="{k}" aria-pressed="{pressed(k == "all")}">{esc(label)}</button>'
        for k, label in TXT.get("status_filters", DEFAULT_STATUS_FILTERS))

    link_html = ""
    if links:
        parts = [a(label, links[key])
                 for key, label in TXT.get("link_labels", DEFAULT_LINK_LABELS) if safe_url(links.get(key))]
        link_html = '<p class="links">' + " | ".join(parts) + "</p>"

    labels = TXT.get("stat_labels", DEFAULT_STAT_LABELS)
    stats = "\n".join(f"<div><b>{v}</b><span>{esc(l)}</span></div>" for v, l in zip(
        (asks, len(won), f"${total:,.0f}", unknown, len(prospects),
         f"${sum(float(r['request']) for r in prospects if r['request']):,.0f}"), labels))

    fonts_url = pal.get("fonts_url")
    page = TEMPLATE.format(
        title=esc(TXT.get("title", f"{org} Funding Pipeline")),
        h1=esc(TXT.get("h1", f"{org} Funding Pipeline")),
        css_comment=TXT.get("css_comment", "Layout: wide tables that scroll in place, prose at full width."),
        fonts_link=f'<link rel="stylesheet" href="{fonts_url}">\n' if fonts_url else "",
        vars_light=css_vars(pal, False), vars_dark_media=css_vars(pal, True),
        vars_dark_attr=css_vars(pal, True),
        intro=md(intro), sections=md("## " + sections), links=link_html, stats=stats,
        wider_intro=esc(TXT.get("wider_intro", "")),
        pipeline_intro=esc(TXT.get("pipeline_intro", "")),
        foot=esc(TXT.get("foot", "")),
        pipe_rows="".join(trs), intel=intel, org=esc(org),
        wide_rows="".join(wide), stage_btns=stage_btns, nwide=len(wide),
        status_btns=status_btns, tier_btns=tier_btns,
        dossiers="".join(dos) or "<p>Dossiers are still being written.</p>",
        ndossiers=len(dos), idx_rows=idx_rows, nidx=len(idx))
    gp.assert_clean(cfg, page, "page")
    P["html_out"].write_text(page)
    return P["html_out"]


TEMPLATE = """<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{fonts_link}<style>
/* {css_comment} */
:root {{
{vars_light}}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
{vars_dark_media} }} }}
:root[data-theme="dark"] {{
{vars_dark_attr} }}
body {{ background: var(--bg); color: var(--fg); font: 16px/1.6 var(--body); }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding-block: 28px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
h1, h2, h3 {{ font-family: var(--display); font-weight: 650; text-wrap: balance; line-height: 1.2; }}
h1 {{ font-size: clamp(1.9rem, 4vw, 2.8rem); margin: 0 0 .4rem; }}
h2 {{ font-size: 1.45rem; margin: 2.4rem 0 .6rem; padding-top: 1.2rem; border-top: 1px solid var(--rule); }}
h3 {{ font-size: 1.1rem; margin: 1.4rem 0 .3rem; }}
a {{ color: var(--accent); }}
blockquote {{ margin: 1rem 0; padding: .9rem 1.1rem; background: var(--panel); border: 1px solid var(--rule); border-radius: 6px; }}
blockquote p {{ margin: 0; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1px; background: var(--rule);
  border: 1px solid var(--rule); border-radius: 6px; overflow: hidden; margin: 1.4rem 0; }}
.stats div {{ background: var(--panel); padding: .8rem 1rem; }}
.stats b {{ display: block; font: 650 1.6rem/1.1 var(--display); font-variant-numeric: tabular-nums; }}
.stats span {{ color: var(--muted); font-size: .85rem; }}
.links {{ font-weight: 600; }}
.scroll {{ overflow-x: auto; border: 1px solid var(--rule); border-radius: 6px; background: var(--panel); }}
table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
th, td {{ text-align: left; vertical-align: top; padding: .6rem .7rem; border-bottom: 1px solid var(--rule); }}
th {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); position: sticky; top: 0; background: var(--panel); }}
td.num {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
td .sub, td .src {{ display: block; color: var(--muted); font-size: .8rem; }}
td.notes {{ min-width: 260px; }}
td.st {{ font-weight: 700; white-space: nowrap; }}
.won {{ color: var(--won); }} .lost {{ color: var(--lost); }} .unknown {{ color: var(--unknown); }} .open {{ color: var(--open); }}
.filters {{ display: flex; flex-wrap: wrap; gap: .5rem; margin: .6rem 0; }}
.filters button {{ font: 600 .85rem var(--body); padding: .35rem .8rem; border: 1px solid var(--rule); border-radius: 6px;
  background: var(--panel); color: var(--fg); cursor: pointer; }}
.filters button[aria-pressed="true"] {{ background: var(--accent); border-color: var(--accent); color: var(--bg); }}
.filters button:focus-visible, summary:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
details {{ border: 1px solid var(--rule); border-radius: 6px; background: var(--panel); margin: .5rem 0; }}
summary {{ cursor: pointer; padding: .75rem 1rem; display: flex; flex-wrap: wrap; gap: .2rem 1rem; align-items: baseline; }}
.dn {{ font: 650 1.05rem var(--display); }}
.dm {{ color: var(--muted); font-size: .85rem; }}
.dbody {{ padding: 0 1rem 1rem; min-width: 0; overflow-wrap: anywhere; }}
.dbody table {{ display: block; overflow-x: auto; }}
.dbody h2 {{ font-size: 1.05rem; margin: 1.2rem 0 .3rem; padding-top: 0; border-top: 0; }}
.cols {{ display: grid; grid-template-columns: minmax(0, 1fr); gap: 0 2.5rem; }}
@media (min-width: 900px) {{ .cols {{ grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); }} }}
.cols > div {{ min-width: 0; }}
.foot {{ color: var(--muted); font-size: .85rem; margin-top: 2.5rem; }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>
<div class="wrap">
<h1>{h1}</h1>
<div class="cols"><div>{intro}</div><div>
<div class="stats">
{stats}
</div>{links}</div></div>
{sections}

<h2 id="wider">Wider net ({nwide} sources by roadmap stage)</h2>
<p>{wider_intro}</p>
<div class="filters" role="group" aria-label="Filter by stage">
<button type="button" data-g="all" aria-pressed="true">All stages</button>
{stage_btns}
</div>
<div class="scroll"><table id="wide"><thead><tr><th>Funder</th><th>Verdict</th><th>Award</th><th>Next window</th><th>{org} angle</th></tr></thead>
<tbody>{wide_rows}</tbody></table></div>

<h2 id="pipeline">Pipeline</h2>
<p>{pipeline_intro}</p>
<div class="filters" role="group" aria-label="Filter by status">
{status_btns}
</div>
<div class="scroll"><table id="pipe"><thead><tr><th>Funder</th><th>Status</th><th>Amount</th><th>Date</th><th>Notes</th></tr></thead>
<tbody>{pipe_rows}</tbody></table></div>

<h2 id="intel">Funder intel</h2>
<div class="scroll"><table><thead><tr><th>Funding stream</th><th>Verdict</th><th>What to do</th></tr></thead><tbody>{intel}</tbody></table></div>

<h2 id="dossiers">Funder dossiers ({ndossiers})</h2>
<p>Tap a funder to open its research file.</p>
{dossiers}

<h2 id="index">Funder dossier index ({nidx})</h2>
<div class="filters" role="group" aria-label="Filter by tier">
{tier_btns}
</div>
<div class="scroll"><table id="idx"><thead><tr><th>Funder</th><th>Tier</th><th>Status</th><th>Suggested ask</th><th>{org} angle</th></tr></thead>
<tbody>{idx_rows}</tbody></table></div>
<p class="foot">{foot}</p>
</div>
<script>
function wire(groupSel, attr, tableId, rowAttr) {{
  const btns = document.querySelectorAll(groupSel);
  const apply = v => {{
    btns.forEach(b => b.setAttribute("aria-pressed", String(b.dataset[attr] === v)));
    document.querySelectorAll("#" + tableId + " tbody tr").forEach(tr => {{
      tr.hidden = !(v === "all" || tr.dataset[rowAttr] === v);
    }});
  }};
  btns.forEach(b => b.addEventListener("click", () => apply(b.dataset[attr])));
  const start = [...btns].find(b => b.getAttribute("aria-pressed") === "true");
  if (start) apply(start.dataset[attr]);
}}
wire("button[data-f]", "f", "pipe", "s");
wire("button[data-t]", "t", "idx", "t");
wire("button[data-g]", "g", "wide", "g");
</script>
"""


def main(argv=None):
    args = gp.parse_args(argv, desc=__doc__)
    cfg = gp.load_config(args.config)
    print(build(cfg))


if __name__ == "__main__":
    main()

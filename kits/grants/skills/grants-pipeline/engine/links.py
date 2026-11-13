"""Resolve every pipeline row to clickable links.

Adds two columns to pipeline-rows.csv, funder-intel.csv and wider-net.csv in paths.data_dir:
  funder_url  the funder's dossier (Drive Doc) or official page
  links       "Label|URL ;; Label|URL" for each piece of evidence in `source`

Links only point inside the organization's own world: its Drive (minutes, grant files,
financial reports), the pipeline folder's research Docs and dossiers, and public web pages.
Never personal email or another organization's files (config exclude_names enforces this).

Inputs: the Drive map (paths.drive_map_glob: a JSON list of [path, id, mime, url]), the
dossier-urls.json and research-urls.json maps, the url overrides file (paths.url_overrides:
{"funder_urls": {...}, "wide_urls": {...}}) and the config links.rules / links.row_rules.

Run:  python3 engine/links.py --config orgs/<slug>.json   (then rebuild workbook and page)
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gp_common as gp  # noqa: E402

PROPUBLICA = "https://projects.propublica.org/nonprofits/search?q="
DEFAULT_MINUTES = {"name_template": "Board Meeting {m}/{d}/{y}", "label_template": "Minutes {m}/{d}/{y}"}


class Ctx:
    """Everything a rule can look up."""

    def __init__(self, cfg, dmap, dossiers, research, funder_urls, wide_urls):
        self.cfg = cfg
        L = cfg.get("links", {})
        self.dmap, self.dossiers, self.research = dmap, dossiers, research
        self.funder_urls, self.wide_urls = funder_urls, wide_urls
        self.skip_hosts = tuple(L.get("skip_hosts", ()))
        self.minutes_cfg = {**DEFAULT_MINUTES, **L.get("minutes", {})}


def load_map(cfg):
    g = cfg["paths"].get("drive_map_glob")
    if not g:
        return []
    files = sorted(g.parent.glob(g.name))
    if not files:
        raise SystemExit(f"no Drive map matches {g}")
    return [tuple(x) for x in json.loads(files[-1].read_text())]


def load_overrides(cfg):
    p = cfg["paths"].get("url_overrides")
    if not p:
        return {}, {}
    d = json.loads(Path(p).read_text())
    return d.get("funder_urls", {}), d.get("wide_urls", {})


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def drive_find(dmap, frag, folder_ok=True):
    """Best Drive file whose path contains the fragment (normalized)."""
    parts = frag.split("/")
    hits = []
    while parts and not hits:  # fall back to the enclosing folder
        f = norm("/".join(parts))
        hits = [x for x in dmap if f in norm(x[0]) and (folder_ok or "folder" not in x[2])]
        parts = parts[:-1]
    if not hits:
        return None
    hits.sort(key=lambda x: ("folder" in x[2], len(x[0])))
    return hits[0][3].split("?")[0]


def minutes(dmap, token, mcfg=None):
    """Find board minutes by "m/d/yyyy" or "m/yyyy" token using the configured Drive file naming."""
    mcfg = mcfg or DEFAULT_MINUTES
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", token)
    if m:
        mo, d, y = m.groups()
        y = y if len(y) == 4 else "20" + y
        name = mcfg["name_template"].format(m=int(mo), d=int(d), y=y)
        for p, _, t, u in dmap:
            if p.strip().endswith(name):
                return mcfg["label_template"].format(m=int(mo), d=int(d), y=y), u.split("?")[0]
    m = re.fullmatch(r"(\d{1,2})/(\d{4})", token)
    if m:
        mo, y = m.groups()
        pat = (re.escape(mcfg["name_template"]).replace(r"\{m\}", str(int(mo)))
               .replace(r"\{d\}", r"(\d+)").replace(r"\{y\}", y) + "$")
        for p, _, t, u in sorted(dmap):
            mm = re.search(pat, p.strip())
            if mm:
                return mcfg["label_template"].format(m=int(mo), d=mm.group(1), y=y), u.split("?")[0]
    return None


def apply_rule(rule, text, ctx, add):
    kind = rule["type"]
    if kind == "urls":
        for u in re.findall(r"https?://[^\s;,)]+", text):
            add(re.sub(r"^https?://(www\.)?", "", u).split("/")[0], u)
    elif kind == "research_slug":
        for slug in re.findall(rule["pattern"], text):
            add(rule.get("label", "Research: {slug}").format(slug=slug), ctx.research.get(slug))
    elif kind == "research_all":
        if rule["token"] in text:
            for slug, u in ctx.research.items():
                add(rule.get("label", "Research: {slug}").format(slug=slug), u)
    elif kind == "dossier_slug":
        for slug in re.findall(rule["pattern"], text):
            add(rule.get("label", "Dossier"), ctx.dossiers.get(slug))
    elif kind == "minutes_phrase":
        for block in re.findall(rule["pattern"], text, flags=re.I):
            for tok in re.findall(r"\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}/\d{4}", block):
                hit = minutes(ctx.dmap, tok, ctx.minutes_cfg)
                if hit:
                    add(*hit)
    elif kind == "drive_path":
        for frag in re.findall(rule["pattern"], text):
            frag = re.sub(r"\.(pdf|docx)$", "", frag.strip().rstrip("/"))
            add(frag.split("/")[-1] or frag, drive_find(ctx.dmap, frag))
    elif kind == "text_match":
        if not re.search(rule["pattern"], text):
            return
        if "minutes" in rule:
            hit = minutes(ctx.dmap, rule["minutes"], ctx.minutes_cfg)
            if hit:
                add(*hit)
        elif "drive_find" in rule:
            add(rule["label"], drive_find(ctx.dmap, rule["drive_find"], rule.get("folder_ok", True)))
        elif "funder_url" in rule:
            add(rule["label"], ctx.funder_urls.get(rule["funder_url"]))
        else:
            add(rule["label"], rule.get("url"))
    else:
        raise ValueError(f"unknown links rule type: {kind}")


def resolve(text, ctx):
    out = []

    def add(label, url):
        if url and (label, url) not in out and not any(h in url for h in ctx.skip_hosts):
            out.append((label, url))

    for rule in ctx.cfg.get("links", {}).get("rules", [{"type": "urls"}]):
        apply_rule(rule, text, ctx, add)
    return out


def row_rules(r, key, links, ctx):
    """Config links.row_rules: add links by what the row's source text and funder name contain."""
    for rr in ctx.cfg.get("links", {}).get("row_rules", []):
        if rr.get("source_contains") and rr["source_contains"] not in r["source"]:
            continue
        if rr.get("name_contains") and rr["name_contains"] not in r[key]:
            continue
        if rr.get("name_contains_any") and not any(x in r[key] for x in rr["name_contains_any"]):
            continue
        for add in rr.get("add_dossier", []):
            links.append((add["label"], ctx.dossiers.get(add["slug"])))
        every = rr.get("research_all_if_name_contains")
        for slug, u in ctx.research.items():
            if slug in rr.get("research", []) or (every and every in r[key]):
                links.append((f"Research: {slug}", u))
    return links


def entry_urls(cfg, skip_hosts):
    ents = []
    for f in cfg["paths"]["research_dir"].glob("*.md"):
        cur = None
        for line in f.read_text().splitlines():
            m = re.match(r"#{2,3}\s+(?:\d+\.\s*)?(.*)", line)
            if m:
                cur = m.group(1).strip()
                continue
            if cur and re.search(r"(?i)\bsources?\b", line[:30]):
                urls = [u for u in re.findall(r"https?://[^\s|)\]>,]+", line)
                        if not any(h in u for h in skip_hosts)]
                if urls:
                    ents.append((cur, urls[0]))
                    cur = None
    return ents


def toks(s):
    stop = {"the", "and", "through", "with", "fund", "grant", "grants", "program", "foundation",
            "for", "community"}
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2 and w not in stop}


def run(cfg):
    P = cfg["paths"]
    funder_urls, wide_urls = load_overrides(cfg)
    dossiers = json.loads(P["dossier_urls"].read_text()) if P["dossier_urls"].exists() else {}
    research = json.loads(P["research_urls"].read_text()) if P["research_urls"].exists() else {}
    ctx = Ctx(cfg, load_map(cfg), dossiers, research, funder_urls, wide_urls)
    plugin = gp.load_plugin(cfg)
    excluded = cfg.get("exclude_names", [])
    fallback = cfg.get("links", {}).get("fallback_search_url", PROPUBLICA)
    by_name = {}
    for slug, url in dossiers.items():
        by_name[norm(slug.replace("-", " "))] = url
    ents = entry_urls(cfg, ctx.skip_hosts)

    preset = {r["funder"]: r.get("funder_url", "")
              for r in csv.DictReader(open(P["wider_net_csv"])) if r.get("funder_url")}

    def funder_url(name, wide=False):
        # A wide row keeps the official URL it was given unless wide_urls overrides it.
        if wide and preset.get(name) and name not in wide_urls:
            return preset[name]
        explicit = wide_urls if wide else funder_urls
        if name in explicit:  # an explicit override beats the fuzzy dossier match below
            return explicit[name]
        n = norm(name)
        for k, u in by_name.items():
            if k in n or n in k:
                return u
        if wide:
            t = toks(name)
            best = max(ents, key=lambda e: len(t & toks(e[0])), default=None)
            return best[1] if best and len(t & toks(best[0])) >= 2 else ""
        return funder_urls.get(name, "")

    summary = []
    for fname, key, wide in ((P["pipeline_csv"], "funder", False),
                             (P["intel_csv"], "stream", False),
                             (P["wider_net_csv"], "funder", True)):
        rows = list(csv.DictReader(open(fname, newline="")))
        fields = [f for f in rows[0].keys() if f not in ("funder_url", "links")] + ["funder_url", "links"]
        missing = 0
        for r in rows:
            r["funder_url"] = funder_url(r[key], wide)
            links = resolve(r["source"], ctx)
            links = row_rules(r, key, links, ctx)
            if plugin and hasattr(plugin, "extra_links"):
                links = plugin.extra_links(r, key, links, ctx)
            links = [(a, b) for a, b in links if b
                     and not gp.contains_excluded(a + " " + b, excluded)]
            if gp.contains_excluded(r["funder_url"], excluded):
                r["funder_url"] = ""
            if not r["funder_url"]:
                r["funder_url"] = links[0][1] if links else (
                    fallback + re.sub(r"\s+", "+", re.sub(r"\(.*?\)", "", r[key]).strip()))
            if not links:
                label = "Tax filings" if "propublica" in r["funder_url"] else "Funder page"
                links = [(label, r["funder_url"])]
            links = [(a, b) for a, b in links if b]
            r["links"] = " ;; ".join(f"{a}|{b}" for a, b in links)
            missing += not links
        with open(fname, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        summary.append(f"{Path(fname).name}: {len(rows)} rows, {sum(bool(r['funder_url']) for r in rows)} "
                       f"funder links, {len(rows) - missing} with evidence links")
    return summary


def main(argv=None):
    args = gp.parse_args(argv, desc=__doc__)
    cfg = gp.load_config(args.config)
    for line in run(cfg):
        print(line)


if __name__ == "__main__":
    main()

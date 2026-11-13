"""Build an organization's Grants Pipeline Tracker workbook from its config.

Tabs: Pipeline, Wider Net, Scoring & Rubric, Dashboard, Funder Intel, Funder Dossier Index.
Org names, colors, prose, status list, tier thresholds and file paths all come from the
config (templates/org.example.json documents every key).

Inputs (paths.data_dir):
  pipeline-rows.csv   one row per ask, past and planned
  funder-intel.csv    one row per funding stream, with a verdict
  dossier-index.csv   one row per prospect
  wider-net.csv       one row per non-local funding source, by roadmap stage
Output: paths.xlsx_out

Run:  python3 engine/build_xlsx.py --config orgs/<slug>.json
"""
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gp_common as gp  # noqa: E402


def read_rows(path):
    return [{k: gp.no_formula(v) for k, v in r.items()} for r in gp.read_csv(path)]

WRAP = Alignment(wrap_text=True, vertical="top")
PROPUBLICA = "https://projects.propublica.org/nonprofits/search?q="


class Style:
    """Colors and fonts from config theme.xlsx; defaults are neutral."""

    def __init__(self, cfg):
        t = {"head": "FF1E5A42", "title": "FF21503B", "sub": "FF55605A", "link": "FF1F4E9E",
             "blue": "FF1F4E9E", "calc": "FFEDEEEA", "input": "FFFFF8DC", "confirm": "FFFFF2A8",
             **cfg.get("theme", {}).get("xlsx", {})}
        self.TITLE = Font(b=True, sz=16, color=t["title"])
        self.SUB = Font(sz=10, color=t["sub"])
        self.HEAD = Font(b=True, sz=11, color="FFFFFFFF")
        self.HEADFILL = PatternFill("solid", fgColor=t["head"])
        self.CALC = PatternFill("solid", fgColor=t["calc"])      # grey: formula, don't type
        self.INPUT = PatternFill("solid", fgColor=t["input"])    # tint: score inputs
        self.CONFIRM = PatternFill("solid", fgColor=t["confirm"])  # yellow: replace with records
        self.BLUE = Font(color=t["blue"])                        # assumption
        self.LINK = Font(color=t["link"], u="single")


def num(v):
    v = (v or "").replace("$", "").replace(",", "").strip()
    try:
        return float(v)
    except ValueError:
        return v or None


def date(v):
    """m/d/yy or m/d/yyyy -> real date so date math works; partial dates ("2023", "8/2024") stay text."""
    for fmt in ("%m/%d/%y", "%m/%d/%Y"):  # two-digit or four-digit year
        try:
            return datetime.strptime(v.strip(), fmt)
        except (ValueError, AttributeError):
            continue
    return v or None


def links_of(r):
    out = []
    for part in (r.get("links") or "").split(" ;; "):
        if "|" in part:
            label, url = part.split("|", 1)
            out.append((label.strip(), url.strip()))
    return out


def link(S, cell, url, text=None):
    if url:
        cell.hyperlink = url
        if text is not None:
            cell.value = gp.no_formula(text)
        cell.font = S.LINK


def link_row(S, ws, n, funder_col, src_col, r, extra=2):
    """Funder name opens its dossier or page; Source opens the first evidence;
    the next `extra` columns hold any further evidence links."""
    link(S, ws.cell(n, funder_col), r.get("funder_url"))
    ev = links_of(r)
    if ev:
        link(S, ws.cell(n, src_col), ev[0][1])
    for j, (label, url) in enumerate(ev[1:1 + extra], 1):
        link(S, ws.cell(n, src_col + j), url, label)


def header(S, ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row, i, c)
        cell.font, cell.fill, cell.alignment = S.HEAD, S.HEADFILL, WRAP
    ws.row_dimensions[row].height = 30
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[ws.cell(row, i).column_letter].width = w


def tiers(cfg):
    t = {"t1_min": 25000, "t2_min": 5000,
         "names": ["T1 · Transform", "T2 · Sustain", "T3 · Automate"], **cfg.get("tiers", {})}
    return t


def pipeline(cfg, S, wb):
    T = cfg["text"]["xlsx"]
    tr = tiers(cfg)
    T1, T2 = tr["t1_min"], tr["t2_min"]
    statuses = ",".join(s["name"] for s in cfg["statuses"])
    unknown = gp.roles(cfg, "unknown")
    marker = T.get("confirm_marker", "CONFIRM")
    ws = wb.active
    ws.title = "Pipeline"
    ws["A1"] = T.get("pipeline_title", f"{cfg['org']['full_name']}: Grants Pipeline Tracker")
    ws["A1"].font = S.TITLE
    ws["A2"] = T.get("pipeline_sub", "")
    ws["A2"].font, ws["A2"].alignment = S.SUB, WRAP
    ws.merge_cells("A2:V2")
    ws.row_dimensions[2].height = 42
    cols = ["Funder", "Program / Purpose", "Locality", "Request $", "Tier\n(auto)", "Status",
            "Submitted", "Decision\ndate", "Award $", "Award /\nRequest", "Elig.\nOK?",
            "Mission\n1-5", "Geo\n1-5", "Fund-area\n1-5", "Reln\n1-5", "Report-ease\n1-5",
            "Fit\n/25", "P(win)\n%", "Effort\nhrs", "EV\n$/hr", "Flags", "Notes", "Source",
            "Link 2", "Link 3"]
    header(S, ws, 4, cols, [26, 32, 12, 11, 8, 16, 11, 11, 11, 9, 7, 8, 7, 9, 7, 10, 7, 8, 8, 9,
                            22, 44, 40, 18, 18])
    rows = read_rows(cfg["paths"]["pipeline_csv"])
    for i, r in enumerate(rows):
        n = 5 + i
        vals = [r["funder"], r["purpose"], r["locality"], num(r["request"]), None, r["status"],
                date(r["submitted"]), date(r["decision"]), num(r["award"]), None, r["elig"],
                num(r["mission"]), num(r["geo"]), num(r["fund_area"]), num(r["reln"]),
                num(r["report_ease"]), None, num(r["p_win"]), num(r["effort"]), None,
                r["flags"], r["notes"], r["source"]]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(n, c, v)
            cell.alignment = WRAP
        link_row(S, ws, n, 1, 23, r)
        ws.cell(n, 5, f'=IF(D{n}="","",IF(D{n}>={T1},"T1",IF(D{n}>={T2},"T2","T3")))')
        ws.cell(n, 10, f'=IF(AND(I{n}<>"",D{n}<>"",N(D{n})>0),I{n}/D{n},"")')
        ws.cell(n, 17, f'=IF(N(L{n})=0,"",SUM(L{n}:P{n}))')
        ws.cell(n, 20, f'=IF(AND(N(D{n})>0,N(R{n})>0,N(S{n})>0),ROUND(D{n}*(R{n}/100)/S{n},0),"")')
        for c in (5, 10, 17, 20):
            ws.cell(n, c).fill = S.CALC
        for c in range(12, 17):
            ws.cell(n, c).fill = S.INPUT
        for c in (18, 19):
            ws.cell(n, c).font = S.BLUE
        for c in (4, 9):
            ws.cell(n, c).number_format = '"$"#,##0'
        ws.cell(n, 10).number_format = "0%"
        for c in (7, 8):
            ws.cell(n, c).number_format = "m/d/yy"
        ws.cell(n, 20).number_format = '"$"#,##0'
        if marker in (r["notes"] or "") or r["status"] in unknown:
            ws.cell(n, 6).fill = S.CONFIRM
    last = 4 + len(rows) + 60
    dv = DataValidation(type="list", formula1=f'"{statuses}"', allow_blank=True)
    dv.add(f"F5:F{last}")
    yn = DataValidation(type="list", formula1='"Y,N"', allow_blank=True)
    yn.add(f"K5:K{last}")
    score = DataValidation(type="decimal", operator="between", formula1="1", formula2="5",
                           allow_blank=True)
    score.add(f"L5:P{last}")
    for v in (dv, yn, score):
        ws.add_data_validation(v)
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:Y{4 + len(rows)}"


def rubric(cfg, S, wb):
    """Render config text.xlsx.rubric: null = blank row, {"title"|"h"|"sub": text}, or a list = table row."""
    tr = tiers(cfg)
    T1, T2 = tr["t1_min"], tr["t2_min"]
    ws = wb.create_sheet("Scoring & Rubric")
    ws.column_dimensions["A"].width = 26
    for c in "BCDE":
        ws.column_dimensions[c].width = 30

    def fill(s):
        return s.replace("{t1}", f"{T1:,}").replace("{t2}", f"{T2:,}").replace("{t1m1}", f"{T1 - 1:,}")

    r = 1
    for item in cfg["text"]["xlsx"].get("rubric", []):
        if item is None:
            r += 1
            continue
        if isinstance(item, dict):
            (kind, text), = item.items()
            font = {"title": S.TITLE, "h": Font(b=True, sz=12), "sub": S.SUB}[kind]
            ws.cell(r, 1, fill(text)).font = font
            ws.cell(r, 1).alignment = WRAP
            if kind == "sub":
                ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
                ws.row_dimensions[r].height = 30
        else:
            item = [fill(x) for x in item]
            is_head = item[0] in ("Tier", "Criterion")
            for c, v in enumerate(item, 1):
                cell = ws.cell(r, c, v)
                cell.alignment = WRAP
                if is_head:
                    cell.font, cell.fill = S.HEAD, S.HEADFILL
            if len(item) == 1:
                ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
                ws.row_dimensions[r].height = 48 if len(item[0]) > 120 else 18
        r += 1


def dashboard(cfg, S, wb):
    D = cfg["text"]["xlsx"].get("dashboard", {})
    notes = D.get("notes", {})
    plan = D.get("plan")
    names = tiers(cfg)["names"]
    ws = wb.create_sheet("Dashboard")
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 70
    ws["A1"] = D.get("title", "Dashboard: updates automatically")
    ws["A1"].font = S.TITLE
    ws["A2"] = D.get("subtitle", "Refreshes as the Pipeline tab is filled in.")
    ws["A2"].font = S.SUB
    P = "Pipeline!F:F"

    def cnt(*roles):
        return "+".join(f'COUNTIF({P},"{n}")' for n in gp.roles(cfg, *roles))

    def sm(col, *roles):
        return "+".join(f'SUMIF({P},"{n}",Pipeline!{col}:{col})' for n in gp.roles(cfg, *roles))

    won = cnt("awarded", "awarded_reduced")
    declined = cnt("declined")
    open_ = cnt("submitted", "pending")
    rows = [
        ("Volume", None, None, None),
        ("Asks made (all time)", "=" + "+".join(x for x in (open_, won, declined, cnt("unknown")) if x),
         notes.get("asks"), None),
        ("Prospects and LOIs not yet asked", "=" + cnt("prospect", "loi"), None, None),
        ("Waiting on a decision", "=" + open_, None, None),
        (None, None, None, None),
        ("Outcomes", None, None, None),
        ("Awarded (count)", f"={won}", None, None),
        ("Declined (count)", "=" + declined, notes.get("declined"), None),
        ("Outcome unknown (count)", "=" + cnt("unknown"), notes.get("unknown"), None),
        ("Win rate (decided outcomes)", f'=IFERROR(({won})/({won}+{declined}),"—")',
         notes.get("win_rate"), "pct"),
        ("$ awarded (all time)", "=" + sm("I", "awarded", "awarded_reduced"), None, "usd"),
        ("$ requested, still open", "=" + sm("D", "submitted", "pending"), None, "usd"),
        ("$ in named prospects", "=" + sm("D", "prospect"), notes.get("prospects"), "usd"),
        ("Avg award ÷ request", '=IFERROR(AVERAGEIF(Pipeline!J:J,"<>",Pipeline!J:J),"—")', None, "pct"),
        (None, None, None, None),
        ("Mix by tier", None, None, None),
        (f"{names[0]} (count)", '=COUNTIF(Pipeline!E:E,"T1")', None, None),
        (f"{names[1]} (count)", '=COUNTIF(Pipeline!E:E,"T2")', None, None),
        (f"{names[2]} (count)", '=COUNTIF(Pipeline!E:E,"T3")', None, None),
    ]
    planned_row = None
    if plan:
        y, m, d = plan["since_date"]
        rows += [
            (None, None, None, None),
            (plan["heading"], None, None, None),
            (plan["planned_label"], plan["planned_amount"], plan.get("planned_note"), "usd"),
            (plan["since_label"], f'=SUMIFS(Pipeline!I:I,Pipeline!H:H,">="&DATE({y},{m},{d}))',
             plan.get("since_note"), "usd"),
        ]
        planned_row = 4 + len(rows) - 2
    r = 4
    for a, b, c, fmt in rows:
        if a:
            ws.cell(r, 1, a).font = Font(b=(b is None))
        if b is not None:
            ws.cell(r, 2, b).fill = S.CALC
            if fmt == "usd":
                ws.cell(r, 2).number_format = '"$"#,##0'
            if fmt == "pct":
                ws.cell(r, 2).number_format = "0%"
        if c:
            ws.cell(r, 3, c).font = S.SUB
        r += 1
    if planned_row:
        ws.cell(planned_row, 2).fill = S.CONFIRM
        ws.cell(planned_row, 2).font = S.BLUE


def intel(cfg, S, wb):
    T = cfg["text"]["xlsx"]
    ws = wb.create_sheet("Funder Intel")
    ws["A1"] = T.get("intel_title", "Funder intel: funding streams and verdicts")
    ws["A1"].font = S.TITLE
    ws["A2"] = T.get("intel_sub", "")
    ws["A2"].font, ws["A2"].alignment = S.SUB, WRAP
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 30
    header(S, ws, 4, ["Funder / stream", "Verdict", "What to do", "Source", "Link 2", "Link 3"],
           [34, 30, 80, 40, 18, 18])
    for i, r in enumerate(read_rows(cfg["paths"]["intel_csv"])):
        for c, k in enumerate(("stream", "verdict", "action", "source"), 1):
            ws.cell(5 + i, c, r[k]).alignment = WRAP
        link_row(S, ws, 5 + i, 1, 4, r)
    ws.freeze_panes = "B5"


def wider_net(cfg, S, wb):
    T = cfg["text"]["xlsx"]
    org = cfg["org"]["name"]
    ws = wb.create_sheet("Wider Net")
    ws["A1"] = T.get("wider_title", "Wider net: funding beyond local relationships, by roadmap stage")
    ws["A1"].font = S.TITLE
    ws["A2"] = T.get("wider_sub", "")
    ws["A2"].font, ws["A2"].alignment = S.SUB, WRAP
    ws.merge_cells("A2:J2")
    ws.row_dimensions[2].height = 44
    cols = ["Stage", "Lens", "Funder / program", "Verdict", f"How {org} gets it", "Award",
            "Next window", "Prerequisites", f"{org} angle", "Source", "Link 2", "Link 3"]
    header(S, ws, 4, cols, [10, 14, 34, 16, 48, 30, 30, 36, 48, 34, 18, 18])
    rows = read_rows(cfg["paths"]["wider_net_csv"])
    for i, r in enumerate(rows):
        for c, k in enumerate(("stage", "lens", "funder", "verdict", "path", "award", "window",
                               "prereq", "angle", "source"), 1):
            ws.cell(5 + i, c, r[k]).alignment = WRAP
        link_row(S, ws, 5 + i, 3, 10, r)
    ws.freeze_panes = "D5"
    ws.auto_filter.ref = f"A4:L{4 + len(rows)}"


def dossier_index(cfg, S, wb):
    T = cfg["text"]["xlsx"]
    org = cfg["org"]["name"]
    ws = wb.create_sheet("Funder Dossier Index")
    ws["A1"] = T.get("dossier_title", "Funder Dossier Index: every prospect, sorted by tier")
    ws["A1"].font = S.TITLE
    ws["A2"] = T.get("dossier_sub", "")
    ws["A2"].font, ws["A2"].alignment = S.SUB, WRAP
    ws.merge_cells("A2:J2")
    ws.row_dimensions[2].height = 44
    cols = ["Funder", "City", "Tier", "Status", f"{org} relationship",
            "Suggested ask", f"{org} angle", T.get("dossier_evidence_header", "Evidence"), "Dossier"]
    header(S, ws, 4, cols, [32, 14, 6, 13, 22, 20, 46, 60, 34])
    rows = read_rows(cfg["paths"]["dossier_index_csv"])
    for i, r in enumerate(rows):
        for c, k in enumerate(("funder", "city", "tier", "status", "relationship",
                               "ask", "angle", "evidence", "dossier"), 1):
            cell = ws.cell(5 + i, c, r[k])
            cell.alignment = WRAP
        if r["dossier"].startswith("http"):
            link(S, ws.cell(5 + i, 9), r["dossier"], "Open dossier")
            link(S, ws.cell(5 + i, 1), r["dossier"])
        else:
            link(S, ws.cell(5 + i, 1), PROPUBLICA + quote_plus(r["funder"]))
            link(S, ws.cell(5 + i, 9), PROPUBLICA + quote_plus(r["funder"]), "Tax filings")
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = f"A4:I{4 + len(rows)}"


def check_excluded(cfg, wb):
    """No cell value or hyperlink may mention an excluded name."""
    names = cfg.get("exclude_names", [])
    if not names:
        return
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                for v in (cell.value, cell.hyperlink.target if cell.hyperlink else None):
                    if isinstance(v, str) and gp.contains_excluded(v, names):
                        raise SystemExit(f"refusing to write workbook: {ws.title}!{cell.coordinate} "
                                         f"mentions an excluded name")


def build(cfg):
    S = Style(cfg)
    wb = Workbook()
    pipeline(cfg, S, wb)
    wider_net(cfg, S, wb)
    rubric(cfg, S, wb)
    dashboard(cfg, S, wb)
    intel(cfg, S, wb)
    dossier_index(cfg, S, wb)
    check_excluded(cfg, wb)
    out = cfg["paths"]["xlsx_out"]
    wb.save(out)
    return out


def main(argv=None):
    args = gp.parse_args(argv, desc=__doc__)
    cfg = gp.load_config(args.config)
    print(build(cfg))


if __name__ == "__main__":
    main()

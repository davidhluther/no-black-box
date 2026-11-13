#!/usr/bin/env python3
"""
fetch_clarity.py - Pull a Microsoft Clarity project's dashboard data via the
Clarity Data Export API and write it into a project-local measurement series.

The API is one endpoint with hard limits (verified 2026-08-26 against
https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api
and mirrored in ../references/clarity-surface-inventory.md):

    GET https://www.clarity.ms/export-data/api/v1/project-live-insights
    Authorization: Bearer <token>

  * numOfDays is 1, 2 or 3 - the last 24/48/72 hours from NOW. No date range.
  * 10 requests per project per day. 3 dimensions max. 1000 rows, no pagination.
  * There is NO project-id parameter: the token IS the project scope.

Because the window is 3 days and Clarity keeps recordings only 30, history only
exists if we keep it. This script appends each pull to a dated file so a daily
cron builds the time series the API cannot give you.

BOUNDARY (see ../SKILL.md): one token per Clarity project, and data stays with
the project it came from. This script refuses to read a token from inside a git
folder and refuses to write output into the skill's own folder.

Usage:
  # verify the request shape with no token and no network:
  python3 fetch_clarity.py --project my-site --dimensions Source --dry-run

  # a real pull, appended to a project-local series:
  python3 fetch_clarity.py --project my-site --dimensions Source \\
      --out ./measurement/clarity

  # AI-referral view (Traffic by Source, AI sources flagged)
  python3 fetch_clarity.py --project my-site --ai-referrals --format table

  # UX friction triage (rage/dead/error clicks by URL)
  python3 fetch_clarity.py --project my-site --ux-triage --format table

Stdlib only - no pip installs, matching the other tools in seo/.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
TOKEN_DIR = Path(os.environ.get("CLARITY_TOKEN_DIR", Path.home() / ".config/clarity"))
BUDGET_DIR = Path(os.environ.get("CLARITY_BUDGET_DIR", Path.home() / ".cache/clarity"))
DAILY_REQUEST_BUDGET = 10  # per project, per Microsoft's documented quota
SKILL_DIR = Path(__file__).resolve().parent.parent

# Documented dimension names. The docs spell one of them "Country/Region" but
# only ever show "OS" in a live example, so the exact wire spelling of that one
# is UNVERIFIED - see SKILL.md "What we could not verify". Aliases below are a
# convenience, not a claim about the API.
DIMENSIONS = ["Browser", "Device", "Country/Region", "OS", "Source",
              "Medium", "Campaign", "Channel", "URL"]
DIMENSION_ALIASES = {
    "country": "Country/Region", "region": "Country/Region",
    "country/region": "Country/Region", "os": "OS", "url": "URL",
    "browser": "Browser", "device": "Device", "source": "Source",
    "medium": "Medium", "campaign": "Campaign", "channel": "Channel",
}

# Metric names Clarity documents returning. Used for --metrics filtering and for
# the two canned views. The docs explicitly say more may appear, so this is a
# filter list, never a schema.
UX_FRICTION_METRICS = ["Rage Click Count", "Dead Click Count", "Error Click Count",
                       "Excessive Scroll", "Quickback Click", "Script Error Count"]

# Referrer hosts treated as AI assistants. A maintained heuristic, not a Clarity
# feature - Clarity's own AI referral attribution lives in the (dashboard-only)
# Citation dashboard. Substring match against the source/referrer string.
AI_SOURCE_HOSTS = [
    "chatgpt.com", "chat.openai.com", "openai.com",
    "perplexity.ai", "copilot.microsoft.com", "edgeservices.bing.com",
    "bing.com/chat", "gemini.google.com", "bard.google.com",
    "claude.ai", "you.com", "poe.com", "phind.com",
    "chat.mistral.ai", "deepseek.com", "grok.com", "x.ai", "meta.ai",
]


# ---------------------------------------------------------------- token / paths

def _inside_git_repo(path: Path) -> bool:
    for parent in [path] + list(path.parents):
        if (parent / ".git").exists():
            return True
    return False


def token_env_name(project: str) -> str:
    return "CLARITY_TOKEN_" + re.sub(r"[^A-Za-z0-9]+", "_", project).upper()


def provisioning_help(project: str) -> str:
    return f"""
No Clarity API token found for project '{project}'.

This is a one-time, per-project setup, and only a Clarity project ADMIN can do
it. Claude cannot do it for you - it requires signing in.

  1. Sign in at https://clarity.microsoft.com/ and open the project.
  2. Settings -> Data Export -> Generate new API token.
  3. Name it (4-32 chars; letters, digits, - _ . only; no spaces; unique per
     project). Suggested: clarity-export-{project}
  4. Copy the token - it is shown once.
  5. Store it OUTSIDE any git repo:

       mkdir -p {TOKEN_DIR}
       printf '%s' 'PASTE_TOKEN_HERE' > {TOKEN_DIR / (project + '.token')}
       chmod 600 {TOKEN_DIR / (project + '.token')}

     Or export it for one shell:  export {token_env_name(project)}='...'

The token carries the project scope - there is no project-id parameter - so a
token reaches that project's data and nothing else. Keep one token per Clarity
project and never share it between projects.

Re-run with --dry-run to check the request shape without a token.
""".rstrip()


def resolve_token(project: str, token_file: str | None) -> str:
    if token_file:
        p = Path(token_file).expanduser()
        if not p.exists():
            sys.exit(f"--token-file not found: {p}")
        if _inside_git_repo(p):
            sys.exit(f"Refusing to read a Clarity token from inside a git repo: {p}\n"
                     f"Tokens live in {TOKEN_DIR} (mode 600), never in a repo.")
        return p.read_text().strip()

    for env in (token_env_name(project), "CLARITY_API_TOKEN"):
        val = os.environ.get(env)
        if val:
            return val.strip()

    default = TOKEN_DIR / f"{project}.token"
    if default.exists():
        return default.read_text().strip()

    sys.exit(provisioning_help(project))


def assert_writable_out(out: Path) -> None:
    resolved = out.expanduser().resolve()
    try:
        resolved.relative_to(SKILL_DIR)
    except ValueError:
        return
    sys.exit(f"Refusing to write Clarity data into the skill folder ({resolved}).\n"
             "The skill is shared; your data is not. Write to your own folder "
             "(for example ./measurement/clarity/).")


# ------------------------------------------------------------------ API request

def normalize_dimensions(raw: list[str]) -> list[str]:
    out = []
    for d in raw:
        d = d.strip()
        if not d:
            continue
        canonical = DIMENSION_ALIASES.get(d.lower(), d)
        if canonical not in DIMENSIONS:
            sys.exit(f"Unknown dimension {d!r}. Documented dimensions: "
                     + ", ".join(DIMENSIONS))
        if canonical in out:
            sys.exit(f"Duplicate dimension {canonical!r}.")
        out.append(canonical)
    if len(out) > 3:
        sys.exit("The API accepts at most 3 dimensions per request.")
    return out


def build_request(num_days: int, dimensions: list[str]) -> tuple[str, dict]:
    if num_days not in (1, 2, 3):
        sys.exit("--days must be 1, 2 or 3 - the API supports no other window.")
    params = {"numOfDays": str(num_days)}
    for i, d in enumerate(dimensions, start=1):
        params[f"dimension{i}"] = d
    return f"{API_URL}?{urllib.parse.urlencode(params)}", params


def budget_path(project: str) -> Path:
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    return BUDGET_DIR / f"{project}-{today}.count"


def check_and_record_budget(project: str) -> int:
    """Track calls against Microsoft's 10/project/day quota. UTC day, matching
    the API's stated timezone. Advisory - the server is the real enforcer."""
    p = budget_path(project)
    used = int(p.read_text().strip()) if p.exists() else 0
    if used >= DAILY_REQUEST_BUDGET:
        sys.exit(f"Daily budget exhausted for '{project}': {used}/"
                 f"{DAILY_REQUEST_BUDGET} requests already made today (UTC). "
                 f"The API will return 429. Counter: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(str(used + 1))
    return used + 1


def call_api(url: str, token: str, timeout: int = 60):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:800]
        hint = {
            401: "Missing, invalid, or expired token. Re-mint it: Settings -> Data Export.",
            403: "Token is not authorized for this operation (project admin required).",
            400: "Invalid request parameters - check --days (1-3) and dimension spelling.",
            429: "Exceeded the documented 10 requests/project/day limit. Wait for the UTC day to roll.",
        }.get(e.code, "")
        if e.code == 500 and not body.strip():
            hint = ("Empty-bodied 500. Known intermittent Clarity behavior "
                    "(microsoft/clarity#1085, filed 2026-05-15). Retry later; "
                    "an empty 500 is NOT 'no data'.")
        sys.exit(f"HTTP {e.code} from Clarity. {hint}\nBody: {body!r}")
    except urllib.error.URLError as e:
        sys.exit(f"Network error calling Clarity: {e.reason}")
    if not raw.strip():
        sys.exit("Clarity returned an empty body with a 200. Treat as a failed "
                 "call, not as zero traffic.")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(f"Clarity returned non-JSON:\n{raw[:800]}")


# -------------------------------------------------------------------- shaping

def flatten(payload) -> list[dict]:
    """[{metricName, information: [{...}]}] -> flat rows.

    Deliberately schema-free: the docs say additional metrics and fields may
    appear, so every key in `information` is carried through untouched.
    """
    rows = []
    if not isinstance(payload, list):
        payload = [payload]
    for block in payload:
        if not isinstance(block, dict):
            continue
        metric = block.get("metricName", "Unknown")
        info = block.get("information") or []
        if not isinstance(info, list):
            info = [info]
        for item in info:
            if isinstance(item, dict):
                rows.append({"metric": metric, **item})
            else:
                rows.append({"metric": metric, "value": item})
    return rows


def largest_block_size(payload) -> int:
    """Row count of the largest single metric block (the flattened total is not it)."""
    sizes = []
    if not isinstance(payload, list):
        payload = [payload]
    for block in payload:
        if not isinstance(block, dict):
            continue
        info = block.get("information") or []
        if not isinstance(info, list):
            info = [info]
        sizes.append(len(info))
    return max(sizes, default=0)


def truncated_blocks(payload, cap: int = 1000) -> list[str]:
    """Return metric names of blocks whose row count is at/above the API's cap.

    The 1,000-row cap is documented as applying per metric block, not to the
    flattened total across blocks (confirmed 2026-09-01: a 1,240-row flattened
    pull across nine blocks, largest block 156, had its truncation flag clear
    upstream). A large flattened total is therefore not itself evidence of
    truncation — only a single block at or above the cap is. Per-block
    behavior at exactly `cap` remains unverified; treating `>= cap` as
    truncated is the conservative reading pending a confirmed boundary case.
    """
    hits = []
    if not isinstance(payload, list):
        payload = [payload]
    for block in payload:
        if not isinstance(block, dict):
            continue
        info = block.get("information") or []
        if not isinstance(info, list):
            info = [info]
        if len(info) >= cap:
            hits.append(str(block.get("metricName", "Unknown")))
    return hits


def is_ai_source(value) -> bool:
    if not value:
        return False
    v = str(value).strip().lower().lstrip("/")
    for prefix in ("https://", "http://", "www."):
        if v.startswith(prefix):
            v = v[len(prefix):]
    return any(host in v for host in AI_SOURCE_HOSTS)


def annotate_ai_referrals(rows: list[dict]) -> list[dict]:
    """Flag rows whose Source/Referrer field looks like an AI assistant.

    Note what this is NOT: Clarity's own AI referral attribution lives in the
    dashboard-only Citation dashboard. This is a referrer-host heuristic over
    API data, and it inherits every weakness of referrer-based AI measurement
    (see seo/ai-traffic-classifier for the gap it cannot close).
    """
    keys = ("Source", "Referrer URL", "ReferrerUrl", "Referrer", "Channel")
    for row in rows:
        hit = next((row[k] for k in keys if k in row and is_ai_source(row[k])), None)
        row["ai_source"] = bool(hit)
    return rows


# --------------------------------------------------------------------- output

def render_table(rows: list[dict]) -> str:
    if not rows:
        return "(no rows)"
    cols, seen = [], set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                cols.append(k)
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    line = "  ".join(c.ljust(widths[c]) for c in cols)
    out = [line, "  ".join("-" * widths[c] for c in cols)]
    for r in rows:
        out.append("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))
    return "\n".join(out)


def render_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    cols, seen = [], set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                cols.append(k)
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def write_series(out_dir: Path, project: str, record: dict) -> Path:
    """One JSON file per project per UTC day, holding every pull made that day.

    Append rather than overwrite: at 10 calls/day the pulls are cheap and
    losing one to a same-day rerun would be silent data loss.
    """
    assert_writable_out(out_dir)
    out_dir = out_dir.expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    day = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    path = out_dir / f"{project}-{day}.json"
    existing = []
    if path.exists():
        try:
            existing = json.loads(path.read_text())
            if not isinstance(existing, list):
                existing = [existing]
        except json.JSONDecodeError:
            existing = []
    existing.append(record)
    path.write_text(json.dumps(existing, indent=2))
    return path


# ----------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Pull Microsoft Clarity dashboard data via the Data Export API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Token setup: run with --dry-run, or without a token, to see the steps.")
    ap.add_argument("--project", required=True,
                    help="Project slug. Selects the token and labels the output. "
                         "NOT sent to the API - the token carries project scope.")
    ap.add_argument("--days", type=int, default=1, choices=[1, 2, 3],
                    help="numOfDays: last 24/48/72 hours. Default 1.")
    ap.add_argument("--dimensions", default="",
                    help="Up to 3, comma-separated: " + ", ".join(DIMENSIONS))
    ap.add_argument("--metrics", default="",
                    help="Comma-separated metric names to keep (client-side filter; "
                         "the API returns everything regardless).")
    ap.add_argument("--ai-referrals", action="store_true",
                    help="Shorthand: --dimensions Source, plus an ai_source flag "
                         "on rows whose referrer looks like an AI assistant.")
    ap.add_argument("--ux-triage", action="store_true",
                    help="Shorthand: --dimensions URL, filtered to the friction "
                         "metrics (rage/dead/error clicks, excessive scroll, "
                         "quickback, script errors).")
    ap.add_argument("--out", help="Directory in the CONSUMING project's repo to "
                                  "append the pull to. Omit to print only.")
    ap.add_argument("--format", choices=["json", "csv", "table"], default="json")
    ap.add_argument("--token-file", help="Explicit token path (must be outside any git repo).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the exact request and exit. No token, no network.")
    ap.add_argument("--no-budget-check", action="store_true",
                    help="Skip the local 10/day counter (the server still enforces).")
    args = ap.parse_args(argv)

    dims = [d for d in args.dimensions.split(",") if d.strip()]
    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]

    if args.ai_referrals and args.ux_triage:
        sys.exit("--ai-referrals and --ux-triage are separate pulls; each costs one "
                 "of the 10 daily requests. Run them one at a time.")
    if args.ai_referrals and not dims:
        dims = ["Source"]
    if args.ux_triage:
        if not dims:
            dims = ["URL"]
        if not metrics:
            metrics = list(UX_FRICTION_METRICS)

    dims = normalize_dimensions(dims)
    url, params = build_request(args.days, dims)

    if args.dry_run:
        tok_default = TOKEN_DIR / f"{args.project}.token"
        print("DRY RUN - nothing was sent.\n")
        print(f"  GET {url}")
        print("  Authorization: Bearer <token>")
        print("  Content-Type: application/json\n")
        print(f"  project slug : {args.project} (local label; not an API parameter)")
        print(f"  params       : {json.dumps(params)}")
        print(f"  metric filter: {', '.join(metrics) if metrics else '(none, keep all)'}")
        print(f"  token source : {token_env_name(args.project)} env var, "
              f"else CLARITY_API_TOKEN, else {tok_default}")
        print(f"  budget file  : {budget_path(args.project)} "
              f"({DAILY_REQUEST_BUDGET}/day documented limit)")
        if args.out:
            assert_writable_out(Path(args.out))
            day = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
            print(f"  would append : {Path(args.out).expanduser() / (args.project + '-' + day + '.json')}")
        print("\n  equivalent curl:")
        print(f"    curl -s '{url}' -H 'Authorization: Bearer $TOKEN' "
              "-H 'Content-Type: application/json'")
        return 0

    token = resolve_token(args.project, args.token_file)
    if args.out:
        assert_writable_out(Path(args.out))
    if not args.no_budget_check:
        used = check_and_record_budget(args.project)
        if used >= DAILY_REQUEST_BUDGET - 2:
            print(f"[warn] {used}/{DAILY_REQUEST_BUDGET} daily requests used for "
                  f"'{args.project}'.", file=sys.stderr)

    payload = call_api(url, token)
    rows = flatten(payload)
    if metrics:
        wanted = {m.lower() for m in metrics}
        rows = [r for r in rows if str(r.get("metric", "")).lower() in wanted]
        if not rows:
            print("[warn] Metric filter matched nothing. Metrics present in this "
                  "response: " + ", ".join(sorted({str(r.get('metric')) for r in flatten(payload)})),
                  file=sys.stderr)
    if args.ai_referrals:
        rows = annotate_ai_referrals(rows)

    hit_blocks = truncated_blocks(payload)
    record = {
        "project": args.project,
        "fetched_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "request": {"url": API_URL, "params": params},
        "row_count": len(rows),
        "truncated_at_api_row_cap": bool(hit_blocks),
        "truncated_blocks": hit_blocks,
        "largest_metric_block_rows": largest_block_size(payload),
        "rows": rows,
    }
    if record["truncated_at_api_row_cap"]:
        print("[warn] Metric block(s) hit the documented 1,000-row cap and cannot "
              "be paginated: " + ", ".join(hit_blocks) + ". Narrow the dimensions.",
              file=sys.stderr)

    if args.out:
        path = write_series(Path(args.out), args.project, record)
        print(f"appended -> {path}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(record, indent=2))
    elif args.format == "csv":
        print(render_csv(rows), end="")
    else:
        print(render_table(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

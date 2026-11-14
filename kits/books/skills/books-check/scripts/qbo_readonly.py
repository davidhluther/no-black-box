#!/usr/bin/env python3
"""books-check: read-only QuickBooks Online pulls.

THE PROMISE: this script never changes your books. It sends GET requests to
the QuickBooks Online accounting service (reports and SELECT queries) and
nothing else. The one POST it can send goes to Intuit's sign-in service to
trade a refresh token for a new access token. That is not your books.

How the promise is enforced in code, not just in this note:
  * Every network call goes through one function, _send().
  * _send() refuses any method except GET, and refuses POST everywhere except
    Intuit's token address.
  * A GET may only reach the QuickBooks accounting host, and only the paths
    for reports, queries and company info.
  * Queries must begin with SELECT.
  * "selftest" checks all of this offline and counts the network calls in
    this file's own source (there must be exactly one).

Settings come from environment variables (never from the command line):
  QBO_CLIENT_ID, QBO_CLIENT_SECRET   from your Intuit developer app
  QBO_REFRESH_TOKEN                  from the Intuit OAuth Playground
  QBO_REALM_ID                       the company ID, shown by the Playground
  QBO_ENV                            "production" (default) or "sandbox"
  QBO_TOKEN_FILE                     optional; where the newest refresh token
                                     is kept (default ~/.config/books-check/token.json)
  BOOKS_CHECK_OUT                    optional; output folder (default ./books-check-output)

Commands:
  python3 qbo_readonly.py selftest
  python3 qbo_readonly.py check
  python3 qbo_readonly.py pull ProfitAndLoss --start 2026-01-01 --end 2026-06-30
  python3 qbo_readonly.py pull GeneralLedger --start 2026-01-01 --end 2026-06-30 --method Accrual
  python3 qbo_readonly.py query "select * from Deposit where TxnDate >= '2026-01-01'"
  python3 qbo_readonly.py flatten books-check-output/<file>.json   (reports or saved queries)
  python3 qbo_readonly.py bracket --account "Other Income" --start 2026-01-01 --end 2026-12-31

Dates on the command line are yyyy-mm-dd because the QuickBooks service
requires that form. Standard library only.
"""
import argparse
import ast
import base64
import csv
import datetime
import decimal
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API_HOSTS = {
    "production": "https://quickbooks.api.intuit.com",
    "sandbox": "https://sandbox-quickbooks.api.intuit.com",
}
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
ALLOWED_PATH = re.compile(r"^/v3/company/\d+/(reports/[A-Za-z]+|query|companyinfo/\d+)$")
REPORTS = {
    "ProfitAndLoss", "ProfitAndLossDetail", "BalanceSheet", "GeneralLedger",
    "JournalReport", "TransactionList", "TrialBalance", "CashFlow",
    "AgedReceivables", "AgedReceivableDetail", "AgedPayables", "AgedPayableDetail",
}
MINOR = os.environ.get("QBO_MINOR_VERSION", "75")
_SECRET_ENV = ("QBO_CLIENT_SECRET", "QBO_REFRESH_TOKEN", "QBO_CLIENT_ID")


class ReadOnlyViolation(Exception):
    """Raised when code tries to do anything other than read."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never follow a redirect: it would skip the host and path checks in _send
    and could carry the sign-in header to another address."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ReadOnlyViolation(f"The server tried to redirect (HTTP {code}); redirects are never followed.")


_OPENER = urllib.request.build_opener(_NoRedirect())


# --------------------------------------------------------------------------
# The single gate every network call passes through
# --------------------------------------------------------------------------
def _send(method, url, headers=None, body=None):
    method = str(method).upper()
    if method == "GET":
        if body is not None:
            raise ReadOnlyViolation("A GET request may not carry a body.")
        parts = urllib.parse.urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in API_HOSTS.values():
            raise ReadOnlyViolation("GET is only allowed to the QuickBooks accounting service.")
        if not ALLOWED_PATH.match(parts.path):
            raise ReadOnlyViolation("GET is only allowed for reports, queries and company info.")
        if parts.path.endswith("/query"):
            q = urllib.parse.parse_qs(parts.query).get("query", [""])[0]
            check_select(q)
    elif method == "POST":
        if url != TOKEN_URL:
            raise ReadOnlyViolation("POST is only allowed to Intuit's sign-in token address.")
    else:
        raise ReadOnlyViolation(f"{method} is never allowed. This tool only reads.")
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    with _OPENER.open(req, timeout=60) as resp:
        return json.load(resp)


# --------------------------------------------------------------------------
# Settings and tokens (secrets are never printed)
# --------------------------------------------------------------------------
def _redact(text):
    for name in _SECRET_ENV:
        val = os.environ.get(name)
        if val:
            text = text.replace(val, "[hidden]")
    return text


def _need(name):
    val = os.environ.get(name, "").strip()
    if not val:
        sys.exit(f"Missing setting {name}. See setup guide BK-FU-03 (step BK-FU-03-3). Fix code E31.")
    return val


def _token_file():
    return pathlib.Path(os.environ.get("QBO_TOKEN_FILE") or pathlib.Path.home() / ".config" / "books-check" / "token.json")


def _out_dir():
    return pathlib.Path(os.environ.get("BOOKS_CHECK_OUT") or "books-check-output")


def _api_base():
    env = os.environ.get("QBO_ENV", "production").strip().lower()
    if env not in API_HOSTS:
        sys.exit("QBO_ENV must be production or sandbox.")
    return API_HOSTS[env]


def _refresh_token_to_use():
    """Intuit hands back a new refresh token on each refresh. Keep the newest one
    in a private file, but let a freshly pasted token in the environment win."""
    env_token = _need("QBO_REFRESH_TOKEN")
    f = _token_file()
    if f.exists():
        try:
            saved = json.loads(f.read_text())
            if saved.get("seeded_from") == env_token and saved.get("refresh_token"):
                return saved["refresh_token"], env_token
        except (ValueError, OSError):
            pass
    return env_token, env_token


def _save_token(new_refresh, seeded_from):
    f = _token_file()
    try:
        f.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps({"refresh_token": new_refresh, "seeded_from": seeded_from,
                              "saved_at": datetime.datetime.now().isoformat(timespec="seconds")})
        # Write a private temp file next to the real one, then swap it in, so a
        # failed write never destroys the only copy of the refresh token.
        tmp = f.with_name(f.name + f".tmp{os.getpid()}")
        fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, "w") as fh:
                fh.write(payload)
                fh.flush()
                os.fsync(fh.fileno())
            os.chmod(str(tmp), 0o600)
            os.replace(str(tmp), str(f))
        except OSError:
            try:
                tmp.unlink()
            except OSError:
                pass
            raise
    except OSError:
        print("Warning: could not save the newest token. The next run may need a fresh token. Fix code E33.", file=sys.stderr)


_ACCESS = {}


def _access_token():
    if "token" in _ACCESS:
        return _ACCESS["token"]
    cid, secret = _need("QBO_CLIENT_ID"), _need("QBO_CLIENT_SECRET")
    refresh, seed = _refresh_token_to_use()
    basic = base64.b64encode(f"{cid}:{secret}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": refresh}).encode()
    try:
        tok = _send("POST", TOKEN_URL, {"Authorization": "Basic " + basic, "Accept": "application/json",
                                         "Content-Type": "application/x-www-form-urlencoded"}, body)
    except urllib.error.HTTPError as e:
        detail = _redact(e.read().decode("utf-8", "replace"))[:300]
        sys.exit(f"Intuit refused the sign-in (HTTP {e.code}). {detail}\nThe refresh token is probably old or was pasted wrong. Fix code E32.")
    _ACCESS["token"] = tok["access_token"]
    if tok.get("refresh_token"):
        _save_token(tok["refresh_token"], seed)
    return _ACCESS["token"]


def _get(path_tail, params):
    realm = _need("QBO_REALM_ID")
    if not realm.isdigit():
        sys.exit("QBO_REALM_ID should be digits only. Fix code E31.")
    url = f"{_api_base()}/v3/company/{realm}/{path_tail}?" + urllib.parse.urlencode({**params, "minorversion": MINOR})
    try:
        return _send("GET", url, {"Authorization": "Bearer " + _access_token(), "Accept": "application/json"})
    except urllib.error.HTTPError as e:
        detail = _redact(e.read().decode("utf-8", "replace"))[:400]
        hint = {401: "Access was refused. Fix code E32.", 403: "This login may not see that company. Fix code E34.",
                429: "Too many requests. Wait a minute and retry. Fix code E36."}.get(e.code, "See fixes.md.")
        sys.exit(f"QuickBooks answered HTTP {e.code}. {hint}\n{detail}")


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------
def _write_json(name, payload):
    out = _out_dir()
    out.mkdir(parents=True, exist_ok=True)
    f = out / name
    f.write_text(json.dumps(payload, indent=1))
    f.chmod(0o600)
    return f


def cmd_check(_a):
    realm = _need("QBO_REALM_ID")
    data = _get(f"companyinfo/{realm}", {})
    info = data.get("CompanyInfo", {})
    print("Connected, read-only. Company:", info.get("CompanyName", "(name not shown)"), "| Country:", info.get("Country", "?"))


def cmd_pull(a):
    if a.report not in REPORTS:
        sys.exit("Report must be one of: " + ", ".join(sorted(REPORTS)))
    params = {"start_date": a.start, "end_date": a.end, "accounting_method": a.method}
    for item in a.param or []:
        k, _, v = item.partition("=")
        if not re.fullmatch(r"[a-z_]+", k) or not v:
            sys.exit("--param needs key=value with a lowercase key, for example summarize_column_by=Month")
        params[k] = v
    data = _get(f"reports/{a.report}", params)
    f = _write_json(f"{datetime.date.today()}-{a.report}-{a.start}_to_{a.end}.json", data)
    print("Wrote", f)


def check_select(q):
    if not q.strip().lower().startswith("select"):
        raise ReadOnlyViolation("Queries must be SELECT statements.")
    return q.strip()


def cmd_query(a):
    q = check_select(a.q)
    data = _get("query", {"query": q})
    f = _write_json(f"{datetime.datetime.now():%Y-%m-%d-%H%M%S}-query.json", {"query": q, "result": data})
    print("Wrote", f)


def _num(text):
    try:
        return decimal.Decimal(str(text).replace(",", "").replace("$", "").strip())
    except (decimal.InvalidOperation, ValueError):
        return None


def flatten_report(rep):
    """Turn a QuickBooks report (nested sections) into flat rows for a spreadsheet."""
    cols = [(c.get("ColTitle") or c.get("ColType") or f"col{i}") for i, c in
            enumerate(rep.get("Columns", {}).get("Column", []))]
    rows = []

    def values(cd):
        return [c.get("value", "") for c in cd]

    def walk(block, path):
        for r in (block or {}).get("Row", []):
            if "Rows" in r or "Header" in r:
                label = values(r["Header"]["ColData"])[0] if "Header" in r else ""
                sub = path + ([label] if label else [])
                walk(r.get("Rows"), sub)
                if "Summary" in r:
                    rows.append(["Summary", " > ".join(sub)] + values(r["Summary"]["ColData"]))
            elif "ColData" in r:
                rows.append(["Data", " > ".join(path)] + values(r["ColData"]))

    walk(rep.get("Rows"), [])
    return ["Kind", "Section"] + cols, rows


def _flat_dict(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = prefix + k
        if isinstance(v, dict):
            out.update(_flat_dict(v, key + "."))
        elif isinstance(v, list):
            out[key] = json.dumps(v, separators=(",", ":")) if v else ""
        else:
            out[key] = "" if v is None else v
    return out


def flatten_query(saved):
    """Turn a saved query result into one row per entity line (or per entity when it has no lines).
    A Line.LinkedTxn cell that is empty means that line is not tied to another transaction."""
    resp = saved.get("result", saved).get("QueryResponse", {})
    rows = []
    for name, items in resp.items():
        if not isinstance(items, list):
            continue
        for item in items:
            lines = item.get("Line") if isinstance(item.get("Line"), list) and item.get("Line") else [None]
            base = _flat_dict({k: v for k, v in item.items() if k != "Line"})
            for ln in lines:
                row = {"Entity": name, **base}
                if ln is not None:
                    row.update(_flat_dict(ln, "Line."))
                rows.append(row)
    header = []
    for r in rows:
        for k in r:
            if k not in header:
                header.append(k)
    return header, [[r.get(h, "") for h in header] for r in rows]


def cmd_flatten(a):
    src = pathlib.Path(a.file)
    rep = json.loads(src.read_text())
    if "query" in rep and "result" in rep:
        header, rows = flatten_query(rep)
    else:
        header, rows = flatten_report(rep)
    dest = pathlib.Path(a.output) if a.output else src.with_suffix(".csv")
    with open(dest, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    dest.chmod(0o600)
    print("Wrote", dest, f"({len(rows)} rows)")


def find_amount(rep, name, col=1):
    """Find a line in a report by its label and return the number in column col."""
    want = name.strip().lower()
    hit = []

    def walk(block):
        for r in (block or {}).get("Row", []):
            for key in ("Header", "Summary"):
                cd = r.get(key, {}).get("ColData") if key in r else None
                if cd and cd[0].get("value", "").strip().lower() in (want, "total for " + want):
                    if len(cd) > col and _num(cd[col].get("value")) is not None:
                        hit.append(_num(cd[col]["value"]))
            if "ColData" in r:
                cd = r["ColData"]
                if cd and cd[0].get("value", "").strip().lower() == want and len(cd) > col and _num(cd[col].get("value")) is not None:
                    hit.append(_num(cd[col]["value"]))
            walk(r.get("Rows"))

    walk(rep.get("Rows"))
    return hit[-1] if hit else decimal.Decimal(0)  # totals come last in a section


def bracket(fetch, start, end, max_calls=40, min_days=1):
    """Date an amount by splitting the window in halves until it is pinned down.
    fetch(start_date, end_date) -> Decimal. Returns (leaf windows, calls used)."""
    calls = [0]
    leaves = []

    def go(s, e, depth):
        if calls[0] >= max_calls:
            raise RuntimeError("call limit reached")
        calls[0] += 1
        amt = fetch(s, e)
        print("  " * depth + f"{s} to {e}: {amt}")
        if amt == 0:
            return
        span = (e - s).days + 1
        if span <= min_days:
            leaves.append((s, e, amt))
            return
        mid = s + datetime.timedelta(days=span // 2 - 1)
        before = len(leaves)
        go(s, mid, depth + 1)
        go(mid + datetime.timedelta(days=1), e, depth + 1)
        if len(leaves) == before:
            leaves.append((s, e, amt))

    try:
        go(start, end, 0)
    except RuntimeError:
        print("Stopped early at the call limit. Raise --max-calls or start with a narrower window.")
    return leaves, calls[0]


def cmd_bracket(a):
    s, e = datetime.date.fromisoformat(a.start), datetime.date.fromisoformat(a.end)

    def fetch(ws, we):
        rep = _get("reports/ProfitAndLoss", {"start_date": str(ws), "end_date": str(we),
                                              "accounting_method": a.method})
        return find_amount(rep, a.account)

    print(f"Bracketing '{a.account}' ({a.method}) from {s} to {e}. Use each window's own total, never a monthly table.")
    leaves, calls = bracket(fetch, s, e, a.max_calls, a.min_days)
    print(f"\nPostings landed in these windows ({calls} report calls):")
    for ws, we, amt in leaves:
        print(f"  {ws} to {we}: {amt}")


def cmd_selftest(_a):
    ok = True

    def expect_block(label, fn):
        nonlocal ok
        try:
            fn()
            print("FAIL (was allowed):", label)
            ok = False
        except ReadOnlyViolation:
            print("ok, blocked:", label)

    api = API_HOSTS["production"] + "/v3/company/123/reports/ProfitAndLoss"
    expect_block("POST to the accounting service", lambda: _send("POST", api, body=b"{}"))
    expect_block("PUT to the accounting service", lambda: _send("PUT", api))
    expect_block("DELETE to the accounting service", lambda: _send("DELETE", api))
    expect_block("GET with a body", lambda: _send("GET", api, body=b"x"))
    expect_block("GET to another website", lambda: _send("GET", "https://example.org/v3/company/123/reports/X"))
    expect_block("GET to a write path (invoice)", lambda: _send("GET", API_HOSTS["production"] + "/v3/company/123/invoice"))
    expect_block("query that is not SELECT", lambda: check_select("delete from Invoice"))
    expect_block("GET query that is not SELECT", lambda: _send("GET", API_HOSTS["production"] + "/v3/company/123/query?query=delete+from+Invoice"))
    expect_block("a redirect to another address", lambda: _NoRedirect().redirect_request(
        None, None, 302, "Found", {}, "https://example.org/steal"))
    tree = ast.parse(pathlib.Path(__file__).read_text())
    counts = {"urlopen": 0, "Request": 0}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
            if isinstance(fn, ast.Attribute) and name == "open" and getattr(fn.value, "id", "") == "_OPENER":
                name = "urlopen"  # the one network call goes through the no-redirect opener
            if name in counts:
                counts[name] += 1
    if counts == {"urlopen": 1, "Request": 1}:
        print("ok, exactly one network call in this file's source")
    else:
        print("FAIL, network calls found:", counts)
        ok = False
    rep = {"Columns": {"Column": [{"ColTitle": ""}, {"ColTitle": "Total"}]},
           "Rows": {"Row": [{"Header": {"ColData": [{"value": "Income"}]},
                             "Rows": {"Row": [{"ColData": [{"value": "Other Income"}, {"value": "1,500.00"}]}]},
                             "Summary": {"ColData": [{"value": "Total for Income"}, {"value": "1500.00"}]}}]}}
    h, rows = flatten_report(rep)
    if find_amount(rep, "Other Income") == decimal.Decimal("1500.00") and len(rows) == 2 and h[:2] == ["Kind", "Section"]:
        print("ok, flatten and find_amount work on a sample")
    else:
        print("FAIL, flatten or find_amount")
        ok = False
    qh, qr = flatten_query({"query": "q", "result": {"QueryResponse": {"Deposit": [
        {"Id": "9", "TxnDate": "2026-03-01", "Line": [{"Amount": 100, "LinkedTxn": [{"TxnId": "5"}]}, {"Amount": 50}]}]}}})
    if len(qr) == 2 and "Line.LinkedTxn" in qh and qr[1][qh.index("Line.LinkedTxn")] == "":
        print("ok, query flatten shows a deposit line with no linked transaction")
    else:
        print("FAIL, flatten_query", qh, qr)
        ok = False
    sample = {(datetime.date(2026, 3, 1), datetime.date(2026, 3, 1)): decimal.Decimal(500)}

    def fake(ws, we):
        return sum(v for (d, _), v in sample.items() if ws <= d <= we)

    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        leaves, _ = bracket(fake, datetime.date(2026, 1, 1), datetime.date(2026, 12, 31))
    if leaves and leaves[0][0] == leaves[0][1] == datetime.date(2026, 3, 1):
        print("ok, bracket pins an example amount to one day")
    else:
        print("FAIL, bracket", leaves)
        ok = False
    print("SELFTEST PASSED" if ok else "SELFTEST FAILED")
    sys.exit(0 if ok else 1)


def main():
    p = argparse.ArgumentParser(description="Read-only QuickBooks Online pulls. Never changes your books.")
    s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("selftest").set_defaults(fn=cmd_selftest)
    s.add_parser("check").set_defaults(fn=cmd_check)
    pr = s.add_parser("pull")
    pr.add_argument("report")
    pr.add_argument("--start", required=True)
    pr.add_argument("--end", default=str(datetime.date.today()))
    pr.add_argument("--method", choices=["Accrual", "Cash"], default="Accrual")
    pr.add_argument("--param", action="append")
    pr.set_defaults(fn=cmd_pull)
    q = s.add_parser("query")
    q.add_argument("q")
    q.set_defaults(fn=cmd_query)
    fl = s.add_parser("flatten")
    fl.add_argument("file")
    fl.add_argument("-o", "--output")
    fl.set_defaults(fn=cmd_flatten)
    br = s.add_parser("bracket")
    br.add_argument("--account", required=True)
    br.add_argument("--start", required=True)
    br.add_argument("--end", required=True)
    br.add_argument("--method", choices=["Accrual", "Cash"], default="Accrual")
    br.add_argument("--max-calls", type=int, default=40)
    br.add_argument("--min-days", type=int, default=1)
    br.set_defaults(fn=cmd_bracket)
    a = p.parse_args()
    try:
        a.fn(a)
    except ReadOnlyViolation as e:
        sys.exit(f"Blocked to protect your books: {e}")


if __name__ == "__main__":
    main()

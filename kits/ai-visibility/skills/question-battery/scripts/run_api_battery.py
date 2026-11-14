#!/usr/bin/env python3
"""Run a frozen question set against AI models through their official developer APIs.

What this is
    A careful, slow, plain-Python runner (standard library only). It asks each
    question once per provider with that provider's web search turned on, saves
    the full answer plus the sources the model listed, and writes a DRAFT scored
    file you then read and correct. It never edits your questions and never
    prints your API keys.

What this is not
    API answers are not the answers a customer sees in the ChatGPT, Claude,
    Gemini, or Perplexity apps. The apps add their own instructions, memory, and
    location handling. So every file this script writes is tagged "-api", and
    you must never score or compare an API run against a hand-run app run.

Keys come from environment variables only:
    OPENAI_API_KEY  ANTHROPIC_API_KEY  GEMINI_API_KEY  PERPLEXITY_API_KEY
Model names come from config.json ("api_models") or AV_MODEL_<PROVIDER>.

Usage
    python3 run_api_battery.py --config config.json --dry-run
    python3 run_api_battery.py --config config.json --providers anthropic,openai --yes
    python3 run_api_battery.py --self-test

Written against each vendor's own API documentation as read on 11/13/2026.
Vendors change request shapes and model names; if a provider returns an error,
read its message, then check the vendor's current docs (see the kit's fixes page).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

PROVIDERS = {
    "openai": {"env": "OPENAI_API_KEY", "label": "ChatGPT (API)"},
    "anthropic": {"env": "ANTHROPIC_API_KEY", "label": "Claude (API)"},
    "gemini": {"env": "GEMINI_API_KEY", "label": "Gemini (API)"},
    "perplexity": {"env": "PERPLEXITY_API_KEY", "label": "Perplexity (API)"},
}
ID_RE = re.compile(r"\b([A-Z]{2}-\d{2})\b")
RESULT_COLUMNS = ["run_id", "question_id", "ai_product", "answer_status", "named", "position",
                  "your_site_cited", "cited_domains", "others_named", "resolved_to",
                  "qset_version", "notes"]


# ----------------------------------------------------------------- questions
def parse_questions(path: Path) -> list[dict]:
    """Read '### ID' header lines each followed by one fenced block of question text."""
    out, cur, fence, buf, seen = [], None, False, [], set()
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("```"):
            if not fence:
                fence, buf = True, []
            else:
                fence = False
                if cur and cur not in seen and buf:
                    out.append({"id": cur, "text": "\n".join(buf).strip(),
                                "group": cur.split("-")[0]})
                    seen.add(cur)
                cur = None
            continue
        if fence:
            buf.append(line)
        elif s.startswith(("#", "**")) and ID_RE.search(s):
            cur = ID_RE.search(s).group(1)
    return out


def is_frozen(path: Path, config: dict) -> bool:
    text = path.read_text(encoding="utf-8").lower()
    return "status: frozen" in text or bool(config.get("question_set", {}).get("frozen_on"))


# ------------------------------------------------------------------ HTTP
def post_json(url: str, headers: dict, payload: dict, timeout: int) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:300]
            last = RuntimeError(f"HTTP {e.code}: {redact(body)}")
            if e.code in (429, 500, 502, 503, 529) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise last
        except urllib.error.URLError as e:
            last = RuntimeError(f"network error: {e.reason}")
            if attempt < 2:
                time.sleep(5)
                continue
            raise last
    raise last  # pragma: no cover


def redact(text: str) -> str:
    for p in PROVIDERS.values():
        v = os.environ.get(p["env"])
        if v:
            text = text.replace(v, "[key hidden]")
    return text


# -------------------------------------------------------------- providers
# Each returns: {"text": str, "sources": [{"url","title"}], "queries": [str], "model": str}
def call_openai(model, prompt, key, cfg):
    out = post_json("https://api.openai.com/v1/responses",
                    {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    {"model": model, "input": prompt, "tools": [{"type": "web_search"}]},
                    cfg["timeout"])
    return parse_openai(out, model)


def parse_openai(out, model):
    text, sources, queries = [], [], []
    for item in out.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    text.append(part.get("text", ""))
                    for a in part.get("annotations", []) or []:
                        if a.get("type") == "url_citation":
                            sources.append({"url": a.get("url", ""), "title": a.get("title", "")})
        elif item.get("type") == "web_search_call":
            act = item.get("action") or {}
            if act.get("query"):
                queries.append(act["query"])
            queries.extend(act.get("queries") or [])
    return {"text": "\n".join(text).strip(), "sources": sources, "queries": queries,
            "model": out.get("model", model)}


def call_anthropic(model, prompt, key, cfg):
    headers = {"x-api-key": key, "content-type": "application/json",
               "anthropic-version": os.environ.get("ANTHROPIC_VERSION", "2026-10-21")}
    tool = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5}
    loc = cfg.get("location") or {}
    if loc:
        tool["user_location"] = {"type": "approximate", **{k: v for k, v in loc.items()
                                 if k in ("city", "region", "country", "timezone") and v}}
    messages = [{"role": "user", "content": prompt}]
    merged = {"content": []}
    for _ in range(4):  # a long search turn may pause; resend to continue
        out = post_json("https://api.anthropic.com/v1/messages", headers,
                        {"model": model, "max_tokens": 2048, "messages": messages, "tools": [tool]},
                        cfg["timeout"])
        merged["content"].extend(out.get("content", []))
        merged["model"] = out.get("model", model)
        if out.get("stop_reason") != "pause_turn":
            break
        messages = [{"role": "user", "content": prompt},
                    {"role": "assistant", "content": merged["content"]}]
    return parse_anthropic(merged, model)


def parse_anthropic(out, model):
    text, sources, queries = [], [], []
    for b in out.get("content", []):
        t = b.get("type")
        if t == "text":
            text.append(b.get("text", ""))
            for c in b.get("citations", []) or []:
                if c.get("url"):
                    sources.append({"url": c["url"], "title": c.get("title", "")})
        elif t == "server_tool_use" and b.get("name") == "web_search":
            q = (b.get("input") or {}).get("query")
            if q:
                queries.append(q)
        elif t == "web_search_tool_result" and isinstance(b.get("content"), list):
            for r in b["content"]:
                if r.get("url"):
                    sources.append({"url": r["url"], "title": r.get("title", "")})
    return {"text": "".join(text).strip(), "sources": sources, "queries": queries,
            "model": out.get("model", model)}


def call_gemini(model, prompt, key, cfg):
    out = post_json("https://generativelanguage.googleapis.com/v1beta/interactions",
                    {"x-goog-api-key": key, "Content-Type": "application/json",
                     "Api-Revision": os.environ.get("GEMINI_API_REVISION", "2026-05-20")},
                    {"model": model, "input": prompt, "tools": [{"type": "google_search"}]},
                    cfg["timeout"])
    return parse_gemini(out, model)


def parse_gemini(out, model):
    text, sources, queries = [], [], []
    for step in out.get("steps", []):
        if step.get("type") == "model_output":
            for part in step.get("content", []):
                if part.get("type") == "text":
                    text.append(part.get("text", ""))
                    for a in part.get("annotations", []) or []:
                        if a.get("type") == "url_citation":
                            sources.append({"url": a.get("url", ""), "title": a.get("title", "")})
        elif step.get("type") == "google_search_call":
            queries.extend((step.get("arguments") or {}).get("queries") or [])
    return {"text": "\n".join(text).strip(), "sources": sources, "queries": queries,
            "model": out.get("model", model)}


def call_perplexity(model, prompt, key, cfg):
    body = {"effort": "fast", "input": prompt}
    if model:
        body["model"] = model
    out = post_json("https://api.perplexity.ai/v1/agent",
                    {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    body, cfg["timeout"])
    return parse_perplexity(out, model)


def parse_perplexity(out, model):
    text, sources = [], []
    for item in out.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("text"):
                    text.append(part["text"])
        elif item.get("type") == "search_results":
            for r in item.get("results", []):
                sources.append({"url": r.get("url", ""), "title": r.get("title", "")})
    return {"text": "\n".join(text).strip(), "sources": sources, "queries": [],
            "model": out.get("model", model or "default")}


CALLERS = {"openai": call_openai, "anthropic": call_anthropic,
           "gemini": call_gemini, "perplexity": call_perplexity}


# -------------------------------------------------------------- drafting
def domain_of(url: str) -> str:
    m = re.match(r"^(?:https?://)?(?:www\.)?([^/\s:?#]+)", url.strip(), re.I)
    return m.group(1).lower() if m else ""


def draft_row(run_id, q, provider, result, cfg_all):
    biz = cfg_all.get("business", {})
    name = (biz.get("name") or "").lower()
    site = (biz.get("website_domain") or "").lower().replace("www.", "")
    text_low = result["text"].lower()
    domains = sorted({domain_of(s["url"]) for s in result["sources"] if s.get("url")} - {""})
    name_hit = bool(name) and name in text_low
    site_hit = bool(site) and any(d == site or d.endswith("." + site) for d in domains)
    same = [e["name"] for e in cfg_all.get("same_names", [])
            if e.get("name") and e["name"].lower() in text_low and "everyday" not in e.get("kind", "")]
    named = "y" if (name_hit or site_hit) else ("same-name" if same else "n")
    note = "DRAFT by script, read the answer and correct this row"
    if name_hit and same:
        note += "; a same-name entry also appears, check which business is meant"
    return {"run_id": run_id, "question_id": q["id"], "ai_product": PROVIDERS[provider]["label"],
            "answer_status": "ok" if result["text"] else "failed",
            "named": named, "position": "" if named != "y" else "check",
            "your_site_cited": ("y" if site_hit else "n") if domains else "none_given",
            "cited_domains": "; ".join(domains), "others_named": "", "resolved_to": "",
            "qset_version": cfg_all.get("question_set", {}).get("version", ""), "notes": note}


# ------------------------------------------------------------------ main
def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    return cfg


def model_for(provider: str, cfg: dict) -> str:
    return os.environ.get(f"AV_MODEL_{provider.upper()}") or cfg.get("api_models", {}).get(provider, "")


def run(args) -> int:
    cfg_path = Path(args.config).expanduser().resolve()
    cfg = load_config(cfg_path)
    base = cfg_path.parent
    qfile = base / cfg.get("question_set", {}).get("file", "questions.md")
    if not qfile.exists():
        print(f"Cannot find your question file at {qfile}. Run fill_questions.py first.", file=sys.stderr)
        return 2
    questions = parse_questions(qfile)
    if not questions:
        print("No questions were found. Each needs a '### ID' line, then a fenced block.", file=sys.stderr)
        return 2
    settings = {"timeout": cfg.get("api_settings", {}).get("timeout_seconds", 120),
                "location": cfg.get("api_location", {})}
    pause = cfg.get("api_settings", {}).get("pause_seconds", 3)
    wanted = [p.strip() for p in args.providers.split(",")] if args.providers else list(PROVIDERS)
    plan = []
    print(f"questions : {len(questions)} from {qfile.name}")
    print(f"frozen    : {'yes' if is_frozen(qfile, cfg) else 'NO'}")
    for p in wanted:
        if p not in PROVIDERS:
            print(f"unknown provider {p!r}; choose from {', '.join(PROVIDERS)}", file=sys.stderr)
            return 2
        has_key = bool(os.environ.get(PROVIDERS[p]["env"]))
        model = model_for(p, cfg)
        ok = has_key and (model or p == "perplexity")
        print(f"  {p:11s} key: {'found' if has_key else 'MISSING (' + PROVIDERS[p]['env'] + ')'}  "
              f"model: {model or '(none set)'}  -> {'will run' if ok else 'skipped'}")
        if ok:
            plan.append((p, model))
    calls = len(plan) * len(questions)
    print(f"planned calls: {calls} (each one may cost money on your own account)")
    if args.dry_run or not args.yes:
        print("Nothing was sent. Add --yes (and remove --dry-run) to run for real.")
        return 0
    if not plan:
        print("No provider is ready. Set a key and a model name first.", file=sys.stderr)
        return 1
    if not is_frozen(qfile, cfg) and not args.allow_unfrozen:
        print("Your question set is not frozen. Freeze it first, or use --allow-unfrozen for a throwaway test.",
              file=sys.stderr)
        return 1

    run_id = args.run_id or date.today().strftime("%Y-%m")
    out_dir = base / "runs" / f"{run_id}-api"
    if out_dir.exists() and not args.overwrite:
        print(f"{out_dir} already exists, so a run with this ID was saved before. Pick a new --run-id, "
              "or add --overwrite to replace it.", file=sys.stderr)
        return 1
    (out_dir / "answers").mkdir(parents=True, exist_ok=True)
    draft_rows, exit_code = [], 0
    started = datetime.now().isoformat(timespec="seconds")
    for provider, model in plan:
        key = os.environ[PROVIDERS[provider]["env"]]
        md = [f"# Answers from {PROVIDERS[provider]['label']}, run {run_id}", "",
              "> Collected through the developer API, not the consumer app. Do not score these",
              "> next to hand-run app answers, and do not compare the two.", "",
              f"Run started: {started}", f"Model requested: {model or 'provider default'}",
              f"Question set version: {cfg.get('question_set', {}).get('version', '')}", ""]
        jsonl = (out_dir / f"{provider}-api.jsonl").open("w", encoding="utf-8")
        for i, q in enumerate(questions, 1):
            try:
                res = CALLERS[provider](model, q["text"], key, settings)
                err = ""
            except Exception as exc:  # report per question, keep going
                res, err = {"text": "", "sources": [], "queries": [], "model": model}, redact(str(exc))
                exit_code = 1
            md += [f"### {q['id']}", "", "Question:", "```", q["text"], "```", "",
                   "Answer (verbatim):", "", res["text"] or f"`not collected` {err}", ""]
            if res["sources"]:
                md += ["Sources listed:", ""] + [f"- {s['url']}" for s in res["sources"]] + [""]
            jsonl.write(json.dumps({"id": q["id"], "model": res["model"], "error": err,
                                    "sources": res["sources"], "searches": res["queries"]}) + "\n")
            row = draft_row(run_id, q, provider, res, cfg)
            if err:
                row["answer_status"], row["notes"] = "failed", "API error, see the .jsonl file"
            draft_rows.append(row)
            print(f"  [{provider} {i}/{len(questions)}] {q['id']} {'ok' if not err else 'ERROR'}")
            if i < len(questions):
                time.sleep(pause)
        jsonl.close()
        (out_dir / "answers" / f"{provider}-api.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with (out_dir / "scored-draft.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=RESULT_COLUMNS)
        w.writeheader()
        w.writerows(draft_rows)
    print(f"Wrote {out_dir}. scored-draft.csv is a DRAFT. Read each answer and correct the row.")
    return exit_code


# ------------------------------------------------------------- self test
def self_test() -> int:
    o = parse_openai({"model": "m", "output": [
        {"type": "web_search_call", "action": {"type": "search", "query": "q one"}},
        {"type": "message", "content": [{"type": "output_text", "text": "Maple Hair Studio is good.",
         "annotations": [{"type": "url_citation", "url": "https://www.example.org/a", "title": "A"}]}]}]}, "m")
    assert o["text"].startswith("Maple") and o["sources"][0]["url"].endswith("/a") and o["queries"] == ["q one"]
    a = parse_anthropic({"content": [
        {"type": "text", "text": "Searching. "},
        {"type": "server_tool_use", "name": "web_search", "input": {"query": "salon"}},
        {"type": "web_search_tool_result", "content": [{"type": "web_search_result", "url": "https://x.test/1", "title": "t"}]},
        {"type": "text", "text": "Answer.", "citations": [{"type": "web_search_result_location", "url": "https://x.test/1"}]}]}, "m")
    assert a["text"] == "Searching. Answer." and len(a["sources"]) == 2 and a["queries"] == ["salon"]
    g = parse_gemini({"steps": [{"type": "google_search_call", "arguments": {"queries": ["a", "b"]}},
        {"type": "model_output", "content": [{"type": "text", "text": "Hi", "annotations": [
            {"type": "url_citation", "url": "https://g.test", "title": "g"}]}]}]}, "m")
    assert g["text"] == "Hi" and g["queries"] == ["a", "b"] and g["sources"][0]["url"] == "https://g.test"
    p = parse_perplexity({"output": [{"type": "search_results", "results": [{"url": "https://p.test", "title": "p"}]},
        {"type": "message", "content": [{"text": "Yo [1]"}]}]}, "")
    assert p["text"] == "Yo [1]" and p["sources"][0]["url"] == "https://p.test"
    cfg = {"business": {"name": "Maple Hair Studio", "website_domain": "example.org"},
           "same_names": [{"name": "Maple Studio", "kind": "another business"}], "question_set": {"version": "v1"}}
    row = draft_row("2026-11", {"id": "LD-01"}, "openai", o, cfg)
    assert row["named"] == "y" and row["your_site_cited"] == "y", row
    row2 = draft_row("2026-11", {"id": "LD-01"}, "gemini", {"text": "Try Maple Studio", "sources": [], "queries": []}, cfg)
    assert row2["named"] == "same-name" and row2["your_site_cited"] == "none_given", row2
    print("self-test passed (parsers checked against the response shapes in vendor docs, not live calls)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--providers", help="comma list: openai,anthropic,gemini,perplexity")
    ap.add_argument("--run-id", help="label for this run, default is this year and month")
    ap.add_argument("--dry-run", action="store_true", help="check everything, send nothing")
    ap.add_argument("--yes", action="store_true", help="really send the questions")
    ap.add_argument("--allow-unfrozen", action="store_true")
    ap.add_argument("--overwrite", action="store_true", help="replace an earlier run with the same run ID")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    return self_test() if args.self_test else run(args)


if __name__ == "__main__":
    sys.exit(main())

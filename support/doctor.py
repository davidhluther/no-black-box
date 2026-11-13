#!/usr/bin/env python3
"""Check-up for the full version of a no-black-box kit.

Usage:  python3 support/doctor.py <kit-id> [--root DIR] [--report] [--no-prompt]

Checks the basics, prints one support code, and offers a plain-text report.
It never prints or stores secret values, file contents, or file paths.
Environment variables are checked by NAME only. Standard library only.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

DEFAULT_STEPS = {
    "python": "01-1",
    "kit": "01-3",
    "config": "01-4",
    "env": "03-3",
    "command": "01-5",
}
# Problem codes shared by every kit (see guides/getting-help.md).
CODES = {"python": "E90", "kit": "E91", "config_missing": "E92",
         "config_invalid": "E93", "env": "E94", "command": "E95"}
REPORT_NAME = "support-report.txt"


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def env_file_names(*dirs):
    """Return NAME set from .env files. Values are never kept."""
    names = set()
    for d in dirs:
        f = Path(d) / ".env"
        if not f.is_file():
            continue
        try:
            for line in f.read_text(encoding="utf-8").splitlines():
                m = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\S.*)?$", line)
                if m and (m.group(2) or "").strip().strip("'\"") not in ("",):
                    names.add(m.group(1))
        except OSError:
            pass
    return names


def parse_version(text):
    nums = re.findall(r"\d+", text)
    return tuple(int(n) for n in nums[:3]) or (0,)


def run_checks(kit_id, root):
    """Return (checks, meta). Each check is dict(kind, name, ok, severity, code, step)."""
    checks = []
    kit_dir = root / "kits" / kit_id
    expect = {}
    kit_ok = kit_dir.is_dir()
    if kit_ok and (kit_dir / "doctor.json").is_file():
        try:
            expect = load_json(kit_dir / "doctor.json")
        except (OSError, ValueError):
            expect = {}
    steps = dict(DEFAULT_STEPS)
    steps.update(expect.get("steps", {}))

    def add(kind, name, ok, code, severity="fail"):
        checks.append({"kind": kind, "name": name, "ok": ok,
                       "code": code, "severity": severity, "step": steps[kind]})

    # Python version
    need = str(expect.get("python_min", "3.9"))
    have = sys.version_info[:3]
    add("python", "Python %s or newer" % need, have >= parse_version(need), CODES["python"])

    # Kit folder
    add("kit", "kit folder present", kit_ok, CODES["kit"])

    # config.json
    config_name = expect.get("config_file", "config.json")
    cfg_path = kit_dir / config_name
    if kit_ok:
        if not cfg_path.is_file():
            add("config", config_name + " present", False, CODES["config_missing"])
        else:
            try:
                cfg = load_json(cfg_path)
                add("config", config_name + " is valid JSON", True, CODES["config_invalid"])
                for key in expect.get("config_required_keys", []):
                    add("config", "config key '%s' filled in" % key,
                        isinstance(cfg, dict) and cfg.get(key) not in (None, "", []),
                        CODES["config_invalid"])
            except (OSError, ValueError):
                add("config", config_name + " is valid JSON", False, CODES["config_invalid"])

    # Required environment variable NAMES (set in environment or a .env file)
    file_names = env_file_names(kit_dir, root, Path.cwd())
    for name in expect.get("required_env", []):
        add("env", "key name %s is set" % name,
            bool(os.environ.get(name)) or name in file_names, CODES["env"])

    # Optional commands
    for cmd in expect.get("optional_commands", []):
        add("command", "optional tool '%s' on PATH" % cmd,
            shutil.which(cmd) is not None, CODES["command"], severity="optional")

    version = str(expect.get("version") or read_plugin_version(kit_dir) or "0.0.0")
    code = str(expect.get("code") or kit_id[:2].upper())
    return checks, {"version": version, "code": code, "kit_ok": kit_ok}


def read_plugin_version(kit_dir):
    for rel in (".claude-plugin/plugin.json", "plugin.json"):
        p = kit_dir / rel
        if p.is_file():
            try:
                return load_json(p).get("version")
            except (OSError, ValueError, AttributeError):
                return None
    return None


def support_code(checks, meta):
    failures = [c for c in checks if not c["ok"] and c["severity"] == "fail"]
    first = failures[0] if failures else None
    guide_step = first["step"] if first else "00-0"
    problem = first["code"] if first else "E00"
    # Hash covers pass/fail of every check by name only, never values.
    basis = "|".join("%s:%s" % (c["name"], int(c["ok"])) for c in checks)
    basis += "|" + meta["code"] + meta["version"] + guide_step + problem
    digest = hashlib.sha256(basis.encode()).digest()
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    h = "".join(alphabet[b % len(alphabet)] for b in digest[:3])
    return "%s-FU-%s-%s-v%s-%s" % (meta["code"], guide_step, problem, meta["version"], h)


def build_report(kit_id, checks, meta, code):
    lines = ["No Black Box check-up report",
             "Support code: " + code,
             "Kit: %s (version %s)" % (kit_id, meta["version"]),
             "Python: %s | System: %s" % (platform.python_version(), platform.system()),
             "", "Checks (names and results only):"]
    for c in checks:
        mark = "ok" if c["ok"] else ("skip" if c["severity"] == "optional" else "FAIL")
        lines.append("  [%s] %s (step %s-%s%s)" % (
            mark, c["name"], meta["code"] + "-FU", c["step"],
            "" if c["ok"] else ", problem " + c["code"]))
    lines += ["", "Not included: passwords, keys or their values, file contents, "
              "file paths, and your organization's details."]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check-up for a no-black-box kit (full version).")
    ap.add_argument("kit_id")
    ap.add_argument("--root", default=None, help="repo folder (default: parent of support/)")
    ap.add_argument("--report", action="store_true", help="write the report file without asking")
    ap.add_argument("--no-prompt", action="store_true", help="never ask questions")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else Path(__file__).resolve().parent.parent
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", a.kit_id):
        print("Kit id should look like 'grants' or 'board-packet'.")
        return 2

    checks, meta = run_checks(a.kit_id, root)
    for c in checks:
        mark = "ok  " if c["ok"] else ("skip" if c["severity"] == "optional" else "FAIL")
        print("[%s] %s" % (mark, c["name"]))
    hard = [c for c in checks if not c["ok"] and c["severity"] == "fail"]
    print()
    print("All basics passed." if not hard else "%d problem(s) found. Fix the first one and run again." % len(hard))
    code = support_code(checks, meta)
    print("Your support code:", code)

    report = build_report(a.kit_id, checks, meta, code)
    do_report = a.report
    if not do_report and not a.no_prompt and sys.stdin.isatty():
        print("\nThis is exactly what a report would contain:\n")
        print(report)
        ans = input("\nSave this report to %s so you can send it? [y/N] " % REPORT_NAME)
        do_report = ans.strip().lower().startswith("y")
    if do_report:
        Path(REPORT_NAME).write_text(report + "\n", encoding="utf-8")
        print("Saved %s in the current folder. Nothing was sent anywhere." % REPORT_NAME)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())

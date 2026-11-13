#!/usr/bin/env python3
"""Pre-publish gate: run the plain-writing checks on one or more markdown files.

Runs, in order:
  1. article-check (validate_article.py --prose) for banned words and patterns
  2. tell-scorer gate (score_batch.py --thresholds) for tell density
  3. copy-lint (copy_lint.py) for colon, dash, and case rules

Exit code 0 means every check passed. Exit code 1 means at least one check
found an error. Exit code 2 means the gate could not run (a sibling skill is
missing or Python is too old). Warnings never fail the gate.

Usage:
  python3 prepublish_gate.py draft.md [more.md ...]
  python3 prepublish_gate.py --rules my-rules.json draft.md
  python3 prepublish_gate.py --skills-dir /path/to/skills draft.md

The skills are found next to this one (../../article-check, ../../tell-scorer,
../../copy-lint). Use --skills-dir if you keep them somewhere else.

This script only reads your files. It never changes them and never sends
anything over the network.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def find_skills(skills_dir):
    base = Path(skills_dir).expanduser().resolve() if skills_dir else Path(__file__).resolve().parents[2]
    found = {
        "article-check": base / "article-check" / "scripts" / "validate_article.py",
        "tell-scorer": base / "tell-scorer" / "scripts" / "score_batch.py",
        "copy-lint": base / "copy-lint" / "scripts" / "copy_lint.py",
    }
    thresholds = base / "tell-scorer" / "gate-thresholds.default.json"
    missing = [name for name, path in found.items() if not path.is_file()]
    if missing or not thresholds.is_file():
        sys.stderr.write(
            "Could not find these skills next to the gate: "
            + ", ".join(missing or ["tell-scorer thresholds"])
            + f"\nLooked in {base}. Use --skills-dir to point at the folder that holds them.\n"
        )
        sys.exit(2)
    return found, thresholds


def run(label, cmd):
    print(f"\n=== {label} ===", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    out = (result.stdout or "") + (result.stderr or "")
    print(out.rstrip() or "(no output)")
    return result.returncode


def main():
    ap = argparse.ArgumentParser(description="Run the plain-writing checks before you publish.")
    ap.add_argument("files", nargs="+", help="markdown files to check")
    ap.add_argument("--rules", help="your own house-rules JSON for article-check")
    ap.add_argument("--thresholds", help="your own tell-scorer thresholds JSON")
    ap.add_argument("--skills-dir", help="folder that holds article-check, tell-scorer, and copy-lint")
    args = ap.parse_args()

    if sys.version_info < (3, 9):
        sys.stderr.write("This gate needs Python 3.9 or newer.\n")
        return 2

    skills, default_thresholds = find_skills(args.skills_dir)
    thresholds = args.thresholds or str(default_thresholds)
    py = sys.executable
    failures = []

    for name in args.files:
        path = Path(name)
        if not path.is_file():
            sys.stderr.write(f"File not found: {name}\n")
            return 2
        print(f"\n##### {name}")
        cmd = [py, str(skills["article-check"]), str(path), "--prose"]
        if args.rules:
            cmd += ["--brand-rules", args.rules]
        if run("article-check", cmd) != 0:
            failures.append((name, "article-check"))
        with tempfile.TemporaryDirectory() as tmp:
            cmd = [py, str(skills["tell-scorer"]), "--md-glob", str(path.resolve()),
                   "--thresholds", thresholds, "--out", str(Path(tmp) / "scores.csv")]
            code = run("tell-scorer gate", cmd)
        if code != 0:
            failures.append((name, "tell-scorer"))
        if run("copy-lint", [py, str(skills["copy-lint"]), str(path)]) != 0:
            failures.append((name, "copy-lint"))

    print("\n" + "-" * 50)
    if failures:
        print("GATE FAILED. Fix these before publishing:")
        for name, check in failures:
            print(f"  {name}: {check}")
        return 1
    print("GATE PASSED. Warnings above are worth a look but do not block.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

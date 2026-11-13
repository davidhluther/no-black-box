#!/usr/bin/env python3
"""Stable-final gate: a final exists, the validator reports 0 errors, and it has not changed for N minutes.

Usage: check_stable.py <slug> [--repo <consuming repo, default cwd>] [--quiet-min 5]
Prints one line: STABLE <slug> <sha256_16>  or  NOT-STABLE <slug> <reason>. Exit 0 only when stable.
"""
import argparse, hashlib, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
# The article-check skill sits beside this one in the skills folder.
VALIDATOR = os.path.normpath(os.path.join(HERE, "..", "..", "article-check", "scripts", "validate_article.py"))

ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("--repo", default=os.getcwd())
ap.add_argument("--quiet-min", type=float, default=5)
ap.add_argument("--validator", default=VALIDATOR)
ap.add_argument("--final", help="path override; default <repo>/output/final/final_<slug>.md")
a = ap.parse_args()

final = a.final or os.path.join(a.repo, "output", "final", f"final_{a.slug}.md")
if not os.path.exists(final):
    print(f"NOT-STABLE {a.slug} no final at {final}"); sys.exit(1)
age_min = (time.time() - os.path.getmtime(final)) / 60
if age_min < a.quiet_min:
    print(f"NOT-STABLE {a.slug} changed {age_min:.1f} min ago (< {a.quiet_min})"); sys.exit(1)
r = subprocess.run([sys.executable, a.validator, final], capture_output=True, text=True, cwd=a.repo)
out = r.stdout + r.stderr
m = re.search(r"(\d+)\s+errors?", out, re.I)
if m:
    errors = int(m.group(1))
elif "VALIDATION PASSED" in out and r.returncode == 0:
    errors = 0  # the validator prints no error count when it passes
else:
    errors = None
if errors is None:
    print(f"NOT-STABLE {a.slug} could not read validator error count (exit {r.returncode})"); sys.exit(1)
if errors:
    print(f"NOT-STABLE {a.slug} validator reports {errors} errors"); sys.exit(1)
sha = hashlib.sha256(open(final, "rb").read()).hexdigest()[:16]
print(f"STABLE {a.slug} {sha}")

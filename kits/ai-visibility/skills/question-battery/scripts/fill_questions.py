#!/usr/bin/env python3
"""Fill the question template with your own business details and check it.

    python3 fill_questions.py --config config.json            writes questions.md as a DRAFT
    python3 fill_questions.py --config config.json --freeze   writes it marked FROZEN

Checks, in plain words
  - every curly-bracket placeholder was filled
  - no question outside the brand-check group (BV) names your business or owner
  - there are exactly 28 questions with unique codes
Standard library only. Reads config.json, writes questions.md next to it.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "references" / "questions-template.md"
FIELD_MAP = {"business_type": "type", "service": "service", "town": "town", "region": "region",
             "business_name": "name", "owner_name": "owner_name"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--freeze", action="store_true")
    ap.add_argument("--template", default=str(TEMPLATE))
    args = ap.parse_args()
    cfg_path = Path(args.config).expanduser().resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    biz = cfg["business"]
    values = {k: biz.get(v, "") for k, v in FIELD_MAP.items()}
    comps = biz.get("competitors") or [""]
    values["competitor_1"] = comps[0]
    missing = [k for k, v in values.items() if not v or v.lower().endswith("(replace)")]
    if missing:
        print("These config fields are empty: " + ", ".join(missing), file=sys.stderr)
        return 1

    lines = Path(args.template).read_text(encoding="utf-8").splitlines()
    out, fence, qid, problems, ids = [], False, None, [], []
    for line in lines:
        s = line.strip()
        if s.startswith("### "):
            qid = s[4:].split()[0]
            ids.append(qid)
        if s == "```":
            fence = not fence
            out.append(line)
            continue
        if fence and qid:
            for k, v in values.items():
                line = line.replace("{" + k + "}", v)
            if re.search(r"[{}]", line):
                problems.append(f"{qid} still has a curly bracket")
            if not qid.startswith("BV"):
                low = line.lower()
                for label in ("business_name", "owner_name"):
                    if values[label] and values[label].lower() in low:
                        problems.append(f"{qid} names your {label.replace('_', ' ')}, which hands the AI the answer")
        out.append(line)
    if len(ids) != 28 or len(set(ids)) != len(ids):
        problems.append(f"expected 28 unique question codes, found {len(ids)}")
    if problems:
        print("Fix these first:\n  - " + "\n  - ".join(problems), file=sys.stderr)
        return 1

    version = cfg.get("question_set", {}).get("version", "v1")
    status = (f"Status: FROZEN on {date.today().strftime('%m/%d/%Y')} (version {version}). Never edit a question; retire and add."
              if args.freeze else "Status: DRAFT, not frozen yet.")
    out = [ln for ln in out if not ln.startswith("Placeholders")]
    out.insert(2, "Keep the casual wording. Never edit a question once frozen; retire it and add a new code.")
    body = "\n".join(out).replace("# Question template (28 questions)", "# Your question set", 1)
    (cfg_path.parent / "questions.md").write_text(status + "\n\n" + body + "\n", encoding="utf-8")
    print(status)
    if args.freeze:
        print("Now put the same date and version in config.json under question_set (frozen_on, version).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# AV-FU-05: Run and Clean

Time, about 30 minutes plus waiting. Remember that a run through a company's developer service is not what a customer sees in the apps. The runner tags everything "-api", and you must never compare an [API](../glossary.md#api) run with a hand run. If you want the customer's view, keep doing the hand-run in AV-FR-04 as well.

1. **AV-FU-05-1.** Start small. Run one company, and check the result before spending on the rest:
   ```
   python3 scripts/run_api_battery.py --config config.json --providers anthropic --yes
   ```
   You'll know it worked when it prints a line for each of the 28 questions and then "Wrote runs/...-api". If every line says ERROR, read the first message. A 401 or 403 usually means a wrong key (E37). A 429 means a limit or no credit (E38). A "model not found" means a wrong model name (E35).

2. **AV-FU-05-2.** Read the answers. Open `runs/<run>-api/answers/anthropic-api.md` and read at least five answers in full, then the `.jsonl` file's "searches" lines to see what the model searched for. These are often not what the customer asked.
   You'll know it worked when the answers are real answers, with sources listed. If the answers are empty, check that [web search](../glossary.md#web-search) is allowed on that account (E37).

3. **AV-FU-05-3.** Run the rest. Repeat with each other company you set up, or run them all at once by leaving out `--providers`.
   You'll know it worked when `runs/<run>-api/` holds one answers file per company, one `.jsonl` file each, and `scored-draft.csv`.

4. **AV-FU-05-4.** Correct the draft. Open `scored-draft.csv` in Google Sheets. Every row says "DRAFT by [script](../glossary.md#script)". For each row, read the answer and fix named, position, your_site_cited, others_named, and resolved_to. The script only matches your name and website. It does not understand the answer.
   You'll know it worked when no row still says DRAFT. Save it as `runs/<run>-api/scored.csv`.

5. **AV-FU-05-5.** Ask [Claude Code](../glossary.md#claude-code): "Use the answer-noise-audit skill on runs/<run>-api." It reads the scored file and the answers and writes `analysis/<run>-api/noise-audit.md`.
   You'll know it worked when the audit lists raw and clean counts, removals with quoted lines, and untracked names. If it says there is no [same-name](../glossary.md#same-name) list, go back to guide AV-FU-04 step 1.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FU-05-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

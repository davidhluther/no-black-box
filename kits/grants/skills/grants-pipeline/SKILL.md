---
name: grants-pipeline
description: Stand up or refresh a grants pipeline for a small nonprofit. Builds a tracker workbook, a phone-friendly page, funder dossiers, wide-net and local research, a link on every row, and a weekly read-only discovery sweep of Grants.gov and local news. Use when someone asks for a grants pipeline, a funding prospect list or a grant search for an organization.
---

# Grants pipeline

Works in: Claude Code (full version). It runs Python scripts on your own computer. The free and low-cost versions of this kit do the same job with Google Sheets, see `free/` in the kit.

A repeatable process for finding and tracking grants for a small nonprofit. The code is in `engine/`, one config file per organization is in `orgs/` (start from `orgs/example.json`), and blank starting files are in `templates/`.

Read the organization's details from its config file. If the user has the kit's `config.json`, use it for the name, EIN, service area, folders and names to exclude. Ask only for what you cannot find.

## What the organization gets

- A tracker workbook with these tabs: Pipeline (every ask since records begin plus open prospects, with tier, fit and expected-value formulas), Scoring and Rubric, Dashboard (win rate, dollars awarded, open asks), Wider Net, Funder Intel (one verdict per funding stream) and Funder Dossier Index.
- A phone-ready page that shows the same tables with stage filters.
- A start-here document for the board: why the pipeline exists, what finished projects teach funders, the roadmap, what needs attention now and what could not be found.
- Funder dossiers for the top local and regional prospects (see the `funder-research` skill).
- A link on every row. The funder name opens the funder's page, the organization's own dossier or a tax-filing search. The evidence columns open the minutes, applications or research behind the row.
- A weekly discovery sweep. It reads Grants.gov and local news, scores what it finds into tiers, and never contacts a funder.

## Steps

Run these in order the first time. A refresh reruns steps 4 and 5. Step 6 keeps the sweep going every week.

### Step 1: Intake

Collect the legal name and EIN (the nine-digit tax ID), the service area, the stages of the organization's work (for example land, build, buyer, repair for a land trust; or outreach, intake, placement for a food bank), who sits on the board, where its files live, and any names that must never appear in its pages (usually another organization you also serve).

Copy `templates/org.example.json` to `orgs/<slug>.json` and fill it in. `templates/org.example.md` explains every setting. Keep the organization's data and outputs in its own folder. Only the config lives with the engine.

### Step 2: Mine the organization's own records first

List the files in the organization's shared drive into a JSON list of path, id, type and URL. Keep that list out of any shared repository, because it names applicants and donors. Then read the grant applications, award and decline letters, board minutes, financial reports and the record of finished projects.

Every past ask goes in `pipeline-rows.csv` with its outcome. An outcome nobody recorded stays "Outcome Unknown" rather than a guess. Write `request`, `award`, `p_win` (a whole number such as 40) and `effort` as plain numbers with no dollar signs or commas, and dates as m/d/yy or m/d/yyyy. Every CSV needs at least one data row before the builders will run.

### Step 3: Foundation tax filings

Pull Form 990-PF filings (the yearly tax return of a private foundation, which lists every grant it paid) for foundations that give in the service area. The `funder-research` skill has the method and scripts. Sort foundations into tiers by how close their giving is to the organization's work and write `dossier-index.csv`. Write full dossiers only for the top ten or so.

### Step 4: Seven research passes

Brief each pass with the organization's facts, its known funders (mark those "known", never "new") and the excluded names. Each pass writes a dated `.md` and `.csv` under the organization's `research/` folder.

1. Federal and state programs the organization can apply to directly, plus partner paths.
2. National intermediaries and networks.
3. Corporate and employer giving, including bank community-investment money.
4. Creative and population lenses, such as heritage, veterans, survivors, elders, and land and title work. Money outside the organization's usual field counts.
5. Peer nonprofits' funders. Pick ten to 15 comparable organizations, then search the tax-filing sites for each peer's name inside other filers' grant lists. Run these searches slowly, and never try to get past a CAPTCHA (the "prove you are human" test). A burst of about 20 searches once tripped one.
6. Local news. Grant and gift stories from the last five years in the area's papers, across every sector. Check each story's own date.
7. Congregations, civic clubs and giving circles.

Mark every claim verified (seen at the source, with the URL), secondary or unverified. Spot-check the main claims yourself and open every funder URL before it goes in. A guessed web address once turned out to be a gambling spam site. Prospects go into `wider-net.csv`, sorted by stage. Strong local ones also get a row in `funder-intel.csv`.

### Step 5: Links, build, sync

```bash
python3 engine/links.py --config orgs/<slug>.json
python3 engine/build_xlsx.py --config orgs/<slug>.json
python3 engine/build_page.py --config orgs/<slug>.json
```

- Recalculate the workbook in a spreadsheet program before converting it to a native Google Sheet, then read the links and the Dashboard back to confirm they survived.
- The organization's own folder is the single source. Update Drive copies in place by file name.
- Look at the page at phone width (375 pixels) and at desktop width.

### Step 6: Schedule the sweep

```bash
python3 engine/sweep.py --config orgs/<slug>.json --dry-run
```

Run it weekly with your computer's scheduler (cron on Mac or Linux, Task Scheduler on Windows). Wrap the run so that every attempt, success and failure is recorded: the sweep already appends an "attempting" row before work and an outcome row per source to `sweep/runs.jsonl`. Add a same-day alert when a run fails or a week passes with no run. A missed slot counts as a failure even when older results are still fresh.

### Step 7: Tiers for automation

| Tier | What | Approval |
|---|---|---|
| 1, board-led | Large or relationship asks | The board, case by case |
| 2, reviewed | Mid-size open calls with a real fit | A batch approval from the board's lead |
| 3, automated long shots | Short forms and letter-of-inquiry emails, usually under $10,000 | One standing approval for the tier |

Nothing goes out in the organization's name until its board approves the tiers. The sending identity is the board's choice.

## Guardrails

- Standalone assets. One organization's pipeline never names or links another organization's, and never points into another organization's folders.
- Nothing is sent, shared or submitted without the person's per-action yes. Do not create funder-portal accounts or type passwords.
- Public roles. If a board member holds a public seat that could touch an ask, another member carries that ask.
- Sources outrank research. Where a research file disagrees with a grant letter, the books or the minutes, the source document wins.
- Write in plain language. Every number in a draft traces to a source (see the `grant-drafting` skill).

## Files

- `engine/`: the shared code. Every script takes `--config`.
- `templates/`: config example and its reference for every setting, CSV headers and a start-here skeleton.
- `orgs/example.json`: a complete example config with invented values. Copy it, never edit it in place.

---
name: clarity-analytics
description: Pull Microsoft Clarity (free website behavior analytics) data into a regular measurement routine, read its AI visibility reports, and find pages where visitors rage-click or click on things that do nothing. Use when asked to check Clarity, see whether AI crawlers send anyone back, add behavior evidence to a report, or diagnose a page that frustrates visitors. Reads only; tokens come from environment variables or a private token file.
---

# Clarity analytics

Works in: Claude Code (full version) for the script. The dashboard reading steps work for anyone, with no script.

Plain words used below:
- session (one visit to your site)
- Clarity (Microsoft Clarity, a free tool that shows how visitors click and scroll on a site)
- API (a way for two programs to talk, like a waiter carrying orders between you and the kitchen)
- CSV (a plain table saved as text, one row per line with commas between the columns)
- environment variable (a named setting your computer holds for programs to read, so a secret never has to be written in a file)
- token (a long secret code that proves a program may read your data, like a key card)




Microsoft Clarity is a free tool that records how visitors use a site: where they click, how far they scroll, where they get stuck. Clarity says on its home page that it is "free forever" with "no limits on traffic" (checked 11/13/2026). It also reports visits that arrive from AI tools, and, if you connect your hosting, how often AI crawlers read your pages compared with how many visitors they send back.

## Read config first

Read `config.json` for the Clarity project name. One project, one token, one folder of data. Never put one site's token or data into another site's work.

## What the Clarity data download can and cannot do

- The download (the official term is "Data Export API", a way for a program to ask Clarity for numbers) has one address, needs a token, and allows 10 requests per project per day, only the last one to three days, three breakdowns at most, and 1,000 rows with no paging. The 1,000-row limit applies to each metric block.
- There is no setting for which project: the token decides.
- Citation and AI crawler views (page citations, share of authority, grounding queries, bot activity, the scrape-to-referral card) exist in the dashboard only. Download the widget CSV by hand.
- Recordings are kept 30 days. History exists only if you capture it. Because the download shows only 1 to 3 days, run it every day if you want a trend.

The full inventory with sources is in `references/clarity-surface-inventory.md`.

## Setup (once, by the Clarity project admin)

1. Sign in at https://clarity.microsoft.com and open the project.
2. Settings, Data Export, Generate new API token. Name it with four to 32 letters, digits, hyphens, underscores or periods.
3. Copy it at once; Clarity shows it once.
4. Store it where no shared folder sees it, either as an environment variable or in a private token file:

```bash
export CLARITY_TOKEN_MY_SITE='paste-token-here'
```

or

```bash
mkdir -p ~/.config/clarity
printf '%s' 'paste-token-here' > ~/.config/clarity/my-site.token
chmod 600 ~/.config/clarity/my-site.token
```

The script refuses to read a token from inside a version-controlled folder and never prints it. Rotate the token whenever someone with project access leaves.

## Workflows

### 1. Daily pull into your own folder

```bash
python3 scripts/fetch_clarity.py --project my-site --dimensions Source,Medium,Channel --days 1 --out ./measurement/clarity
```

`--dry-run` prints the exact request without sending it. Each pull is appended to a dated file with the request and time recorded, so any number in a report traces back to a call. The script counts its own daily calls and refuses the eleventh. A workable plan: one call grouped by Channel, one by Source, Medium and Channel, leaving eight for questions. Use `--days 1` on a daily schedule; overlapping windows double count.

### 2. AI visits and AI crawlers

- Channel value `AiPlatform` (and `PaidAiPlatform`) in a pull separates AI visits. Crossed with Source it names the assistant.
- `python3 scripts/fetch_clarity.py --project my-site --ai-referrals --format table` flags known AI assistant hosts in the Source breakdown. It is a guess based on the referring address, not Clarity's own classification. Report it as a floor.
- The dashboard path (AI Visibility, Bot Activity) needs your hosting provider connected. Read the AI Scrape-to-Referral card, download its CSV, and check it against the Citation view.
- Google AI features: Clarity sorts some Google visits into the AI channel, but a click from an AI Overview on an ordinary results page looks like normal search. Report the AI number as a floor and never as "AI Overview traffic".

Claims not to make: bot activity is not usage (a crawler visit does not prove your content was cited); share of authority is computed only over queries where you were cited at all, so it is not a share of all AI answers; scrape-to-referral ratios cover only domains Clarity could map.

### 3. Friction triage

```bash
python3 scripts/fetch_clarity.py --project my-site --ux-triage --format table
```

Lists rage clicks (rapid repeated clicks), dead clicks (clicks that do nothing), error clicks, excessive scrolling, quick backs and script errors per page. Counts are raw. Divide by the page's sessions before ranking pages. On a large site the 1,000-row limit hides pages, so use the dashboard filtered to one page instead. Use the dashboard heatmap and recordings for the reason. Do not take numbers from Clarity's AI summaries; take them from the download or a widget CSV.

## Reporting

For every Clarity figure in a report, record the period (a rolling UTC window for the download), which surface it came from (download, widget CSV or dashboard) and the caveats above. Run `metric-check` before explaining any move.

## Not verified

The tests that shipped with this script use a documented sample, not a live account. The wire spelling of the Country/Region breakdown, the exact metric names in live responses and whether the per-block row cap counts exactly 1,000 as truncated are unconfirmed. The script reports the raw status and body and never treats an empty reply as "no traffic".

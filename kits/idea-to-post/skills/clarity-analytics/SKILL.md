---
name: clarity-analytics
description: Pull Microsoft Clarity data into your regular measurement habit. Saves daily snapshots through Clarity's export (which only ever shows the last one to three days), reads which AI services send visitors back, and ranks pages by rage clicks and dead clicks. Use when asked to check Clarity, see whether AI crawlers or AI referrals are worth anything, add behavior evidence to a report, or find where visitors struggle on a page.
---

# Microsoft Clarity in your measurement routine

Works in: Claude Code (full version). It runs a Python script from your own computer, using only what ships with Python. A scheduled daily run is optional and is set up with your computer's own scheduler.

Clarity is free, collects every visit without sampling, and records how people use pages: where they click, scroll and give up. Since 2026 it also includes an AI Visibility area that answers a question few other tools do: do the AI crawlers visiting your site send anyone back?

Its export only keeps the last one to three days and its recordings last 30. History exists only if you save it. This skill makes saving it routine.

## Where each kind of data lives

The export is one endpoint, `GET https://www.clarity.ms/export-data/api/v1/project-live-insights`, with a bearer token (a long password-like string). Its limits are tight (checked against Microsoft's documentation on 08/26/2026; recheck, because Clarity changes fast):

- 10 requests per project per day.
- One to three days of data, counted back from the moment of the call. No date range.
- Up to three breakdowns (dimensions) per call, and 1,000 rows per metric block, with no paging.
- No project setting: the token decides which project you get.

Metrics include traffic, engagement time, scroll depth, popular pages, referrer URL, and the friction counters: rage click, dead click, error click, excessive scroll, quick-back click and script error. Breakdowns include browser, device, country or region, operating system, source, medium, campaign, channel and URL.

Everything about AI visibility except one channel field is dashboard-only: citations, bot activity, the scrape-to-referral card, heatmaps and recordings have no export. The full list with sources is in `references/clarity-surface-inventory.md`.

Two facts matter most:

- **Citations need only domain verification** (the tracking code, Search Console or Bing Webmaster Tools). They show page citations, share of authority, AI referral traffic and grounding queries, which are the questions AI services actually ran to find your content. That last one is the most interesting free artifact in the product.
- **Bot Activity needs a connected CDN** (the service that delivers your pages from nearby servers). Microsoft lists Fastly, Cloudflare and Amazon CloudFront, with Azure Front Door and a WordPress plugin named elsewhere. It reads server-side logs, not the page tag. Check the live list in Settings, then AI Visibility, before concluding anything about your host.

## Setup

One token per Clarity project, from an environment variable. The steps are in `references/setup.md`. Running the script with no token prints the same steps.

## Workflows

### Workflow 1: a daily pull into your own folder

```bash
python3 scripts/fetch_clarity.py --project my-site --days 1 \
    --dimensions Source,Medium,Channel --out ./measurement/clarity
```

`Source,Medium,Channel` is the recommended standing call. The Channel breakdown is where AI attribution lives, and Medium separates populations that share a source. Pair it with a plain `--dimensions Channel` call, which leaves eight of the ten daily calls for questions.

Each pull is appended to `my-site-YYYY-MM-DD.json` (UTC date) in the folder you name, with the request details and the fetch time stored beside the rows, so any number in a report traces back to the call that made it. The script counts calls in a small file under `~/.cache/clarity/` and refuses the eleventh instead of wasting it on an error.

The 1,000-row flag is worked out per metric block, and `truncated_blocks` names which block hit the cap. A large total across several blocks is not truncation.

Do not run `--days 3` every day and read it as three days of new data: consecutive windows overlap. Use `--days 1` daily. Use `--days 3` once to catch up after a gap, and say in your notes that the window overlaps.

`--dry-run` prints the exact address, settings, token source, output path and an equivalent `curl` command without touching the token or the network. Do this before scheduling anything.

### Workflow 2: do AI crawlers send anyone back

The scrape-to-referral card itself is dashboard-only. For a monthly or quarterly report:

1. In Clarity, open Dashboards, then AI Visibility, then Bot Activity, and set the period.
2. Read the AI Scrape-to-Referral Ratio card and its breakdown by AI service: who sends visitors back, and who scrapes a lot and returns little.
3. Download the widget's CSV into your measurement folder. The dashboard period moves on; the CSV is what lasts.
4. Cross-check against AI Visibility, then Citation. Bot Activity says who accessed your pages. Citation says whether access led to credit. Microsoft says they are different signals.
5. For behavior rather than counts, use the card's link into Recordings filtered to one AI source. What an AI-referred visitor actually did is the part counts never show.

For the trend line between dashboard reads:

```bash
python3 scripts/fetch_clarity.py --project my-site --ai-referrals --format table
```

That pulls traffic by Source and flags rows whose referrer matches a maintained list of AI hosts (`AI_SOURCE_HOSTS` in the script). It is a referrer-host guess over export data, not Clarity's own attribution. Most AI-influenced visits carry no AI referrer at all, so report it as a floor and never as the AI share.

**Google's AI surfaces are a floor too.** In a Source, Medium and Channel pull, `google` and `organic` can split across two channels in the same window: most to `OrganicSearch`, a few to `AiPlatform`. Clarity is classifying per session on something the export does not show. The channel says "AI" but not whether it was AI Mode, an AI Overview or Gemini. A click from an AI Overview citation on an ordinary results page looks like any blue-link click and sits uncounted in `OrganicSearch`. Never present that `AiPlatform` number as AI Overview traffic. Search Console cannot close the gap from the other side, because its search-appearance list has no AI value.

Medium also separates bot populations that Source lumps together. On one property a single assistant host split into an empty-medium variant with hundreds of bot sessions and a `referral` variant with none. Join on source and medium, never source alone.

**Three claims not to make**, all from Microsoft's own wording:

- Bot activity is not usage. Requests do not show that content was retrieved, cited or surfaced in an AI answer.
- Share of authority is computed over queries where your domain was cited at all, so it runs higher than a share of all AI answers.
- Scrape-to-referral ratios cover only correctly mapped domains. A partly mapped property does not give a site-wide ratio.

### Workflow 3: rage clicks and dead clicks

Friction counters are the cheapest behavior evidence for an audit or a redesign argument. A speed audit says a page is slow; a rage-click count says visitors are fighting it.

```bash
python3 scripts/fetch_clarity.py --project my-site --ux-triage --format table
```

That is the URL breakdown filtered to the six friction counters, so findings land per page. Two cautions:

- On a large site the 1,000-row cap returns an arbitrary subset of pages, not the busiest. For named pages, use the dashboard filtered by URL, which keeps 30 days (see `references/clarity-surface-inventory.md`).
- Counts are raw, not rates. Divide by that page's sessions before ranking pages, or the busiest page always wins.

Then go to the dashboard for the why: open the page's heatmap and filter Recordings to that page and friction type. Clarity's AI summaries of recordings are a fair first pass, but they do arithmetic unreliably. Never take a number from a summary into a report. Take it from the export or a widget CSV.

## Keep each organization's data apart

The skill is shared; the data is not. One token per Clarity project, one output folder per project, and never a chart from one organization in another's report. The script refuses to write into the skills folder.

## Reporting what you found

Write findings in your own measurement notes. For anything quoted, record the period (and that the export window is rolling and UTC), which surface it came from (export call, widget CSV or dashboard read, which differ in reliability and retention), and the caveats above, word for word when a number goes to leadership.

## What the script has not proven

Written from Microsoft's documentation and a few live pulls. Check these on your first real run:

1. The response shape beyond Microsoft's one published sample. The script flattens `{metricName, information[]}` and keeps every field it sees.
2. The exact spelling of the `Country/Region` breakdown. If it returns an error, try `Country`.
3. Whether metric names in the documentation match the names in real responses. `--metrics` filters on the client, and warns with the names actually present when nothing matches.
4. Which metric and breakdown pairs work together.
5. Whether a block of exactly 1,000 rows counts as truncated. The script treats `>= 1000` as truncated, to be safe.
6. Reliability. An empty-bodied server error was reported against healthy projects in 2026 (microsoft/clarity issue 1085). The script reports the raw status and never reads an empty answer as "no traffic".

A property with no `AiPlatform` row has no AI referral traffic in that window. That is a fact about the traffic, not a gap in the export. Do not explore with an undimensioned call: it returns metric names with no values, so it cannot see the answer and wastes a call from a tight budget.

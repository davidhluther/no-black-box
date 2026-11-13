---
name: gsc-read
description: Read Google Search Console data without changing anything. Captures the last seven days against the seven days before for one site, lists queries that are new, gone, spiking or dropping, and optionally checks whether named pages are indexed and which sitemaps are listed. Use when asked "what changed in search this week", "which queries dropped", "is this page indexed", or when a report needs Search Console figures from a script instead of copying from the web screen.
---

# Search Console read

Works in: Claude Code (full version). A free version without scripts is in the kit's `free/` folder (the web export and the Sheets pull).

Plain words used below:
- GA4 (Google Analytics 4, Google's free tool that counts visits to a website)
- session (one visit to your site)
- impression (one time a page was shown in a search result, clicked or not)
- Search Console (Google's free report of how your site appears in Google search)
- API (a way for two programs to talk, like a waiter carrying orders between you and the kitchen)
- environment variable (a named setting your computer holds for programs to read, so a secret never has to be written in a file)
- service account (a login that belongs to a program instead of a person)
- skill (a folder of written instructions an AI tool follows to do one job the same way each time)




Search Console is Google's free report of how your site appears in Google search. This skill reads it, never writes to it. The script asks for read-only permission only; it cannot submit sitemaps, remove pages or change settings.

## Read config first

Read `config.json` for the site as Search Console names it: `sc-domain:example.org` for a whole domain, or a full address such as `https://www.example.org/` for one address prefix. Ask if unclear. Never ask for a password.

## Setup (once, with the user)

1. In Google Cloud, create a service account (a robot login that belongs to a program, not a person) and download its key file. The kit's setup guide walks through it.
2. In Search Console, Settings, Users and permissions, add the service account's email as a user with "Restricted" access. Restricted is read-only.
3. Put the key file outside any folder that is shared or backed up to a public place. Point to it with an environment variable (a named setting your computer holds for a program; the program reads it by name so the secret never appears in files):

```bash
export GSC_SA_KEY="/path/to/key-file.json"
export GSC_SITES="sc-domain:example.org"
```

4. Install the two libraries once: `pip install google-api-python-client google-auth`.

## Run a capture

```bash
python3 scripts/gsc_read.py --site sc-domain:example.org --out gsc-2026-11-13.json
python3 scripts/gsc_read.py --site sc-domain:example.org --out gsc-2026-11-13.json --inspect https://www.example.org/page-to-check/
python3 scripts/verify_capture.py --site sc-domain:example.org --file gsc-2026-11-13.json
```

The first command compares the latest complete seven days with the seven days before. It stops three days short of today because Search Console data settles slowly. `--end yyyy-mm-dd` sets a different last day.

## Reading the result

- `deltas` classifies each query as new, gone, spike, drop or neutral. A spike or drop means clicks moved by at least five, or impressions by at least 50 and at least half. New and gone mean only that the query appeared in one window's returned rows and not the other.
- Search Console returns a limited set of rows and hides rare queries for privacy. So "gone" does not prove nobody searched it. Say "not returned", not "disappeared".
- Days are Pacific time, not your local time.
- Inspection results and sitemap lists are snapshots of today, not of either window.
- If a window reports `local_limit_reached`, the capture hit the script's row cap and should not be adopted until you narrow it.

## Before you act on a move

Run `metric-check`. Confirm direction on a second independent source (GA4 organic sessions for the same pages and dates, or Bing Webmaster Tools). A Search Console export, its API and any tool that merely shows Search Console figures are one source.

## What this skill will not do

Write to Search Console, request indexing, remove URLs, or read sites that are not listed in `GSC_SITES`.

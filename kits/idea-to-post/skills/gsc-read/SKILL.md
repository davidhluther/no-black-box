---
name: gsc-read
description: Read Google Search Console data safely and read-only, for the last two seven-day windows. Saves one signed file of search queries (clicks, impressions, position), a list of which queries are new, gone, spiking or dropping, optional page-indexing checks, and your sitemap status. Use when asked to pull Search Console data, see what changed in search this week, check whether pages are indexed, or feed search numbers into a report.
---

# Search Console read

Works in: Claude Code (full version). It runs a Python script on your computer and signs in to Google with a key file you control.

Google Search Console is Google's free tool that shows which searches bring people to your site. This skill reads it, changes nothing, and writes the result to a file with a fingerprint so nobody can edit the numbers by accident.

Free alternative with no setup: in Search Console, open Performance, choose the last seven days, then Export and Download CSV. Do that for the previous seven days too, and compare by hand or paste both files into your AI model. This skill automates exactly that.

## What the capture holds

- Two windows of seven days each: the current one and the one before. Each is a list of search queries with clicks, impressions, click rate and average position.
- A comparison of the two: each query is marked `new`, `gone`, `spike`, `drop` or `neutral`. Spike and drop mean clicks moved by five or more, or impressions moved by 50 or more and by half or more of the earlier amount.
- Optional page checks (`--inspect`): Google's current view of whether a page is indexed. Up to 20 pages.
- Your sitemap list and its status.
- A fingerprint (`capture_sha256`) of everything else.

Dates follow Pacific time, because that is how Google buckets its days. The newest day is three days back, because recent days are still being filled in. That lag is a rule of thumb and not proof that older days are final.

## Setup (once)

Full steps with screenshots-in-words are in `references/setup.md`. The short version:

1. Make a Google Cloud service account (a robot login) with a key file, and enable the Search Console API.
2. In Search Console, add the robot's email address as a user of your property.
3. Install the two Python add-ons: `pip install google-api-python-client google-auth`.
4. Set two environment variables (settings your computer remembers for a program):
   - `GSC_SA_KEY` is the path to the key file.
   - `GSC_APPROVED_SITES` is a comma-separated list of the properties this tool may read, such as `sc-domain:example.org`.

The key file is a password. Keep it outside any project folder and never paste it into a chat or a screenshot.

## Run it

```bash
python3 gsc_read.py --site sc-domain:example.org --out captures/gsc-2026-11-13.json
python3 gsc_read.py --site sc-domain:example.org --out captures/gsc-2026-11-13.json \
    --inspect https://example.org/blog/my-post https://example.org/about
```

`--end YYYY-MM-DD` sets the last day of the current window (it cannot be newer than three days ago). Exit code 0 means a file was written. 2 means a bad input or a missing setting. 1 means Google refused or the write failed, and in that case no file is published, so an old file is never mistaken for a fresh one.

The tool has no way to change anything in your Search Console. It asks for read-only permission, and it refuses any property not in your approved list.

## Check a capture before you trust it

```bash
python3 verify_capture.py --site sc-domain:example.org --file captures/gsc-2026-11-13.json
```

It exits 0 only when the file is today's capture for that site, the fingerprint matches, and neither window hit the 100,000-row limit. Anything else prints one reason and exits 1, and you should pull fresh data instead.

## How to read it honestly

- The rows are only what Google returned. Google hides rare queries for privacy and caps the list, so a query missing this week is not proof people stopped searching it.
- `new` and `gone` mean "present in one window's rows and absent in the other's", nothing more.
- Page checks and sitemap status are snapshots from today, not measurements from either window.
- A spike or drop is a prompt to look, not a reason to change a page. Check what else moved: the season, a news event, a change to your own page.
- Pair this with a second source before acting (Bing Webmaster Tools, your site analytics). When two sources disagree, find out why first.

## Pairing

`ai-traffic-classifier` reads the query column of this capture (or of a CSV download) to estimate how many queries look like leaked AI conversation turns.

---
name: baseline-data
description: Defines and maintains the small shared snapshot that the other website checks read, so each check doesn't pull the same numbers again. The snapshot has four tables, which are search queries and rankings, the page list, the keyword list, and the competitor list, plus a date. Explains where each comes from, how old is too old, and which checks read or update which table. Use when setting up a check-up, when several checks need the same data, or when asked whether the numbers are fresh.
---

# Baseline data

Works in: Claude Code, Claude.ai, ChatGPT. In the free version the four tables are tabs in the Google Sheet. In the full version they are files in a `baseline` folder.

A snapshot, taken once per cycle (monthly is plenty for a small business), keeps every check working from the same numbers. When the snapshot is fresh, a check reads it. When it isn't, the check says so and asks whether to refresh first.

## The four tables

| Table | Where it comes from | Used by |
|---|---|---|
| Queries | Search Console, Performance report, last 90 days, with the page dimension on | cannibalization, consolidate, action-plan |
| Pages | A crawl export, or the sitemap plus a hand-filled list | internal-links, cannibalization, meta-fix, blog-index |
| Keywords | The keyword-discovery output (plus a paid tool if you have one) | keyword-discovery, market-analysis |
| Competitors | The competitor list from the scorecard, with rating, review count, and speed | site-scorecard, local-seo |

## Columns

Queries: query, impressions, clicks, click-through rate, average position, main page, number of distinct pages shown for it. More than one page for the same query is the first sign of pages competing with each other (see `cannibalization`).

Pages: address, title, main heading, status code, word count, links in, links out, description, page type (service, blog, landing, other), indexable or why not, canonical address, structured data types, clicks from the home page.

Keywords: phrase, source, topic, type, the business's position if known, the page that ranks, volume if a paid tool was used.

Competitors: business, website, rating, review count, primary category, mobile speed score, structured data present, distance.

## Freshness

- Under 30 days old: use it, and note the date in the output.
- 30 days or older: warn, and ask whether to refresh or proceed.
- Missing: say the result will have less context, and offer to build it. If the user says go ahead, pull what the check needs directly.

Write the snapshot date in a `baseline-date` cell or file.

## Who writes and who reads

Most checks only read. Keyword-discovery may add rows to the Keywords table and refresh the Competitors table, and then updates the date. Nothing else changes the snapshot, so two checks in the same cycle can't disagree about the same page.

## Refreshing

1. Export the last 90 days of queries and pages from Search Console.
2. Update the pages table from a fresh crawl, or from the sitemap and your own notes.
3. Refresh the competitor row for each competitor from their listing and PageSpeed Insights.
4. Write the date.
5. Report the row counts.

## Rules

- A snapshot describes one site. Don't mix sites.
- Keep it free of passwords, keys, and customer details.
- If a pull failed, write the date of the last good pull and note the failure in the log, so a gap shows up the same day.

---
name: technical-seo-audit
description: Runs a repeatable, prioritized technical check of a website from a crawl export. Finds broken pages, pages search engines can't index, missing or badly sized titles and descriptions, missing headings, thin pages, pages buried deep or linked from nowhere, slow pages, insecure pages, and whether AI crawlers are allowed in robots.txt. Scores each finding by search impact, business impact, and effort. Use when asked to audit, crawl-check, or find technical SEO problems on a site, or to rank a backlog of known fixes.
---

# Technical SEO audit

Works in: Claude Code (full version). It runs a small Python script on your computer. If you don't have that, the free version of this check is the "Technical basics" prompt in `prompts.md`, which uses Search Console and PageSpeed Insights instead.

A crawl is a robot visiting every page of a site and writing down what it finds, the way a search engine does. The crawl export is the spreadsheet of results. Screaming Frog's SEO Spider is a desktop program that does this. Its free version crawls up to 500 web addresses, which covers most small business sites (limit checked 11/13/2026 at screamingfrog.co.uk).

## What it checks

Seven categories, each with a starting score for search impact, business impact, and effort (see `references/impact-scoring.md`).

1. Crawlability: pages that return errors, and redirects the site still links to.
2. Indexability: pages blocked from search with `noindex`, or pointed at another page as the "real" one.
3. On-page elements: missing, too short, or too long title; missing or too long description; missing main heading; thin content. Redirect and error rows are skipped, because a redirect has no content to judge.
4. Site architecture: pages four or more clicks from the home page, and pages with no internal links pointing at them.
5. Performance: speed scores, when the crawl included them. Zeros mean "not collected", not "perfect".
6. Security: pages served over HTTP instead of HTTPS.
7. AI readiness: whether `robots.txt` names the main AI crawlers, and whether an `llms.txt` file exists (a plain-text summary some AI tools read; it's new, and its value is not proven).

Not covered, and every report says so: mobile readiness (needs a separate crawl as a phone), structured data validation (use `local-schema`), and international language tags.

## Steps

### 1. Get a crawl export

Crawl the site you own with a crawler, then export the table that lists every address ("Internal: All") as a CSV. Don't rebuild the CSV by copying text from a preview. Titles often contain a pipe character ("Page | Site name"), and splitting on it misaligns the columns silently.

### 2. Add business context

Before running the script, ask what the site sells, which pages bring in money, and whether a redesign or move is in progress. The scores are starting points. Change them when you know better. A business that lives on page speed should weight performance higher. A brand-new site should weight crawlability and indexability higher, because nothing else matters until search engines can reach it.

### 3. Run the script

```
python3 scripts/analyse_crawl.py internal_all.csv
```

Add `--json` for machine-readable output. Findings are sorted by priority: (search impact x 0.4) + (business impact x 0.4) + ((10 - effort) x 0.2).

### 4. Write the report

Group by category and severity, lead with Critical and High, and show the category health scores, not just the overall one. Name every "not covered" item.

## Severity bands

| Score | Severity |
|---|---|
| 8 and up | Critical |
| 6.5 to 7.99 | High |
| 5 to 6.49 | Medium |
| 3 to 4.99 | Low |
| under 3 | Informational |

Each category starts at 100 and loses 15 points per Critical finding, eight per High, and three for anything else. The overall score is the plain average, so one badly broken category can't hide behind several healthy ones.

## Rules

- Crawl only sites you own or have permission to crawl.
- One crawl per run. Don't re-crawl to "refresh" a number.
- If a crawl couldn't run, record that in your notes. A missing run is a result, not silence.

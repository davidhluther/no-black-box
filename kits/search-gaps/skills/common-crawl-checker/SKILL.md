---
name: common-crawl-checker
description: Checks whether a website is actually reachable by Common Crawl's crawler (CCBot), the free web archive that many AI models draw their training data from. Looks at capture history, archived robots.txt files, known hosting and plugin fingerprints, and a live test as CCBot versus a normal browser to catch blocks that robots.txt doesn't show. Use when asked about AI crawler access, whether a new site has been picked up, or why a site never appears in AI answers although robots.txt looks open.
---

# Common Crawl visibility check

Works in: Claude Code (full version). It runs a small Python script that talks to Common Crawl's public servers. No account or key is needed. The free by-hand version is at the end.

Common Crawl is a nonprofit that visits much of the public web a few times a year and publishes the archive for anyone to use. A large share of the data AI models learn from comes from archives like it, so whether its crawler (named CCBot) can read your site is a separate question from whether ChatGPT's or Claude's own crawlers can.

A website's `robots.txt` is a plain file at the site's root that tells crawlers where they may go. A site can look fully open there and still turn crawlers away at a different layer, such as a content delivery network (the service that sits in front of a site to speed it up and filter traffic). Cloudflare's default bot settings are the common example, and a manual look at robots.txt never shows it.

## What it checks

1. Capture trend. Does the domain appear in recent monthly Common Crawl indexes, and roughly how many pages?
2. robots.txt history. Archived copies across recent months, parsed for rules that block AI crawlers, with the month a block first appeared.
3. Hosting and plugin fingerprints. A best-effort match against known patterns (Cloudflare, Yoast, Squarespace, Shopify, Wix). It is pattern matching, not a vendor's own statement. A miss means "no known pattern matched", not "none".
4. Live test. A request as CCBot and one as a normal browser. When CCBot gets a refusal (403, 406, 429, or 503) and the browser gets a normal page, something at the edge is blocking it.

## Run it

```
python3 scripts/check_visibility.py example.org --months 12
```

Add `--json` for machine-readable output. The script uses only Python's standard library.

## How to read it

Treat the output as a diagnosis, not a verdict.

- Missing from recent crawls and the live test is clean: probably too new. Common Crawl runs about monthly, with a lag. That's a timing fact, not a problem.
- Missing from recent crawls and the live test shows a refusal: something is actively blocking CCBot. Check the content delivery network's bot settings first. That's the most common real cause.
- Present in the past, with an AI-crawler block first seen in a recent month: something changed. A redesign, a new service in front of the site, or a plugin update. Match that month to what changed.

## Limits, said plainly

- Page counts come from the index's own pagination. They're a sample, not every page.
- Fingerprint detection is observed patterns, not a documented interface from any vendor.
- Common Crawl's index server sometimes returns errors under load. The script retries. One failed run says nothing about your site, so rerun later.

## Free by-hand version

Open `your-site/robots.txt` in a browser and read it for lines naming `CCBot`, `GPTBot`, `ClaudeBot`, `PerplexityBot`, or `Google-Extended` followed by `Disallow: /`. Then log in to the hosting or security service in front of the site and look at its bot or AI-crawler settings. That covers the most common cause.

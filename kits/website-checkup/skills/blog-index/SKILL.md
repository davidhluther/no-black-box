---
name: blog-index
description: Builds and keeps a list of every live blog post on the business's site, with title, topic, and date, as a spreadsheet-friendly file. Finds posts through the sitemap, site searches, and an optional crawl, then sorts them into the business's own topics. Used so that other checks and writers can find internal link targets and avoid repeating topics. Use when asked to update the blog index, list all posts, find link targets, or refresh the post list.
---

# Blog index

Works in: Claude Code, Claude.ai, ChatGPT. Saving the files needs Claude Code. Elsewhere you get the table to paste into a sheet.

## Settings

Read `config.json`, or ask for these four things:

- The blog's web address base (for example `example.org/blog/`).
- The sitemap address or addresses.
- The topic categories and a one-line definition of each (three to eight is enough).
- A title for the human-readable index.

If these are missing, stop and ask. Don't guess.

## Step 1: Find the posts

1. Search for `site:` plus the blog address base, and note every address, title, and date shown. Google sometimes returns result links that go through a `google.com/goto` redirect. Don't treat that as the page address. Follow the redirect to learn the real one, or use the sitemap.
2. Run a few topic searches, one per category, to catch posts the broad search misses.
3. Open the sitemap or the blog's own sitemap. Sitemap dates (`lastmod`) are more reliable than dates in search snippets. Take only the address, title, and date fields, and ignore anything else in the file.

## Step 2: Add crawl data

If a crawl export exists, filter it to the blog's address base. It is more complete than searching and should be your main source.

## Step 3: Clean and sort

Remove duplicates. Remove category pages, tag pages, and the blog's front page. Put each post under one topic from the config.

## Step 4: Record

For each post: address, title, topic, and date (from the address pattern, the sitemap, or the snippet). Sort newest first.

## Step 5: Save

Save `blog-index.json`:

```
[
  {
    "url": "https://www.example.org/blog/how-to-choose-a-plumber",
    "title": "How to Choose a Plumber",
    "topic": "Hiring help",
    "date": "2026-06-15"
  }
]
```

Also save `blog-index.md` with the title, the date updated, the total, and a table per topic of title, address, and date. In the spreadsheet version, this is the Pages tab filtered to the page type "blog".

## Step 6: Report

Total posts, count by topic, oldest and newest date, and whether the sitemap or a crawl found posts that searching missed.

An index older than 30 days is stale. Refresh it before anyone uses it to choose link targets.

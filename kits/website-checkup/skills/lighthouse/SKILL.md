---
name: lighthouse
description: Checks page speed, accessibility, and basic quality on the pages that matter, using free tools. Measures real-visitor (field) data and lab test data separately, and puts field data first, since that is what Google uses. Flags pages that fail the three Core Web Vitals, finds the common causes, and ranks fixes. Use when asked about page speed, Core Web Vitals, Lighthouse, performance scores, a slow site, or technical page quality.
---

# Speed and page quality

Works in: Claude Code, Claude.ai, ChatGPT. You run the free test pages and paste in results, or Claude Code runs the free test if an API key is set.

## The tools, all free to use

- PageSpeed Insights (pagespeed.web.dev). Type a page address and get both kinds of data below. See the page itself for current usage limits.
- Chrome DevTools, Lighthouse tab, built into Chrome. Same lab test, run on your own computer.
- The Chrome UX Report (CrUX) is the source of the "real-world" numbers. Its API is free, with a limit of 150 requests a minute (checked 11/13/2026 at developer.chrome.com). Most small sites don't need the API, because PageSpeed Insights shows the same data.

Two kinds of data, and they can disagree:

- Field data is measured from real visitors using Chrome. Google uses it. A page without enough visitors has none.
- Lab data is a simulated test with a deliberately slow phone and network. It is useful for finding causes, not for judging severity. A lab test can show a ten-second load for a page real visitors load in three.

## Step 1: Choose the pages

Use pages given by the user. Otherwise: the home page, the contact or booking page, the main service pages, and the five blog posts or pages with the most search clicks (from Search Console). Ten to 15 pages is plenty. Never more than 20.

Before testing, open each address in a browser and confirm it loads. A blank or error result on a page that doesn't exist is not a finding. Don't write "blocked" or "slow" from a missing score alone.

## Step 2: Test

For each page, run PageSpeed Insights on the mobile tab, then the desktop tab. Record:

- Field: loading (LCP), responsiveness (INP), layout shift (CLS), and the pass or fail verdict, or "no field data".
- Lab: performance, accessibility, best practices, and SEO scores; page weight; request count.

Thresholds (good, needs improvement, poor): LCP 2.5 seconds or less, up to 4 seconds, above. INP 200 milliseconds or less, up to 500, above. CLS 0.1 or less, up to 0.25, above. Flag any category score below 50.

## Step 3: Read it honestly

Lead with field data. Where lab and field disagree sharply, say so and explain that field data reflects real visitors. Use lab results only for causes: oversized images, scripts that block the page, missing image descriptions, a slow web host.

A test run on a busy computer is noisy. Note it and don't compare it with last month.

## Step 4: Report

Write a short report with the date and a table for field data (page, LCP, INP, CLS, pass or fail, source), a table for lab scores by page (mobile first), the worst five pages with the specific causes, issues that repeat across pages with a fix for each, and a ranked fix list grouped by effort. Hand technical items to whoever maintains the site.

## Never

- Judge severity from lab numbers.
- Test a page you haven't confirmed exists.
- Test more than 20 pages in one run.

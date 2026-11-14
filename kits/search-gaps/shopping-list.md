# Shopping List

This is the real list of moving parts. Nothing here is hidden behind a vendor name, and most items can be skipped or swapped. For each one you get what it is, why the kit uses it, what it costs, a cheaper or free route, whether you can skip it, and where you have room to choose.

No vendor prices are printed. Where a price matters, the line says "see current pricing" and names the vendor's own page. Every account and key is explained in [Keys and accounts](../../guides/keys-and-accounts.md). A key goes in an environment variable (a named setting your computer holds in memory), never in `config.json` or a shared folder.

## Required

### Claude Code and a Claude plan

- **What it is.** [Claude Code](glossary.md#claude-code) runs Claude on your computer, where it can read your exports and write the reports.
- **Why.** Every [skill](glossary.md#skill) in this kit runs in it, and the scripts run from it.
- **Cost.** See current pricing at claude.com/pricing for the plans that include Claude Code.
- **Cheaper or free.** The small-business kits run most of the same skills in a chat window. See [Choose your version](choose-your-version.md).
- **Skip it?** No. This is the full team version.
- **Room to choose.** Give each analyst their own seat, so the work is attributable. See [Keys and accounts](../../guides/keys-and-accounts.md) for the sign-in and the optional developer key.

### Python

- **What it is.** [Python](glossary.md#python) runs the small scripts (the [crawl](glossary.md#crawl) analysis, the [Common Crawl](glossary.md#common-crawl) check, and the check-up).
- **Why.** It does the arithmetic the same way every time.
- **Cost.** Free at python.org.
- **Skip it?** No. Check it in step SG-FU-01-1.

### Search Console, one property per site

- **What it is.** [Search Console](glossary.md#search-console) is Google's free report for your own sites.
- **Why.** It is the only source of real clicks, impressions, and positions for your pages, and it feeds the [baseline](glossary.md#baseline), [cannibalization](glossary.md#cannibalization), and consolidation.
- **Cost.** Free. See Google's page at search.google.com/search-console for current terms.
- **Skip it?** Not for a team. Without it, those checks have no evidence and say so.
- **Room to choose.** Ask for read access for the person who runs the checks, rather than a shared login. See [Keys and accounts](../../guides/keys-and-accounts.md).

### A crawler

- **What it is.** [Screaming Frog](glossary.md#screaming-frog) or a similar desktop crawler that exports every page of a site as a table.
- **Why.** The technical audit, internal links, and metadata checks read the export.
- **Cost.** The vendor has a free tier with a page limit and a paid license. See current pricing at screamingfrog.co.uk.
- **Cheaper or free.** The site audit in your [SEO](glossary.md#seo) platform, if you have one, if you can export the same columns. Any crawler works that exports titles, status codes, word counts, link counts, and depth.
- **Skip it?** You can skip the technical audit, but then you have no list of what is broken.

### One owner for the schedule

Not a purchase, but the most common reason these programs stall. Name one person who owns the [run log](glossary.md#run-log) and one owner per site. Guide SG-FU-02 explains the roles.

## Strongly recommended

### A link database such as Ahrefs

- **What it is.** [Ahrefs](glossary.md#ahrefs) is a paid platform that records which sites link to which. The `backlink-gap` skill is written around it, and expects a key named `AHREFS_API_KEY`.
- **Why.** It is the only way to see which sites link to several competitors and not to you.
- **Cost.** See current pricing at ahrefs.com. API access can be a separate plan, so check before you buy.
- **Cheaper or free.** The free path covers your own links with Search Console and [Bing Webmaster Tools](glossary.md#bing-webmaster-tools). [Semrush](glossary.md#semrush) or another database works if you export its referring-domain lists and give the files to Claude with the same tier rules. That route is untested in this kit.
- **Skip it?** Yes, and the report says so on its first line. You lose the competitor comparison, nothing else.
- **Room to choose.** Pull at most six competitors per site, as the skill's rules say, so reports stay comparable.

### Bing Webmaster Tools

- **What it is.** Bing's free site report.
- **Why.** A second source of queries and inbound links, and a check that directions agree across platforms.
- **Cost.** Free. See the page at bing.com/webmasters for terms.
- **Skip it?** Yes, but you give up a cross-check you will want when someone asks "how do we know."

### GA4

- **What it is.** [GA4](glossary.md#ga4) is Google's traffic and conversion tool.
- **Why.** The kit's checks are search-side. GA4 is where you confirm that a change reached visits and conversions, and it is the usual source for the leader summary.
- **Cost.** Free for standard use. See Google's page for limits.
- **Skip it?** Yes for running the checks. No for reporting results to leaders.

## Optional

### PageSpeed Insights key

- **What it is.** [PageSpeed Insights](glossary.md#pagespeed-insights) is Google's speed test. A key lifts the request limits.
- **Why.** The `lighthouse` skill can run the test for you when a key is set as `GOOGLE_API_KEY`. Without one, you paste results in by hand.
- **Cost.** See Google's page for limits. Keys are created in Google Cloud Console. See [Keys and accounts](../../guides/keys-and-accounts.md).
- **Skip it?** Yes.

### Microsoft Clarity

- **What it is.** A free tool that records how visitors move through a page.
- **Why.** Useful after a consolidation or a metadata change, to see what visitors do on the page. No skill reads it.
- **Cost.** See current terms at clarity.microsoft.com.
- **Skip it?** Yes.

### Looker Studio

- **What it is.** [Looker Studio](glossary.md#looker-studio) is Google's free dashboard tool.
- **Why.** If leaders want a dashboard, build one from the register and Search Console. The kit produces the tables, not the dashboard.
- **Skip it?** Yes. A one-page summary does the job for many teams.

### Review and forum sources

- **What it is.** Public pages. Google Maps, app stores, and review sites for reviews. Public forums for threads.
- **Why.** `review-mining` and `reddit-research` read pages you paste or fetch politely. Reading public Reddit pages needs no key. A review site's data service may issue a key. See [Keys and accounts](../../guides/keys-and-accounts.md) before you pay for any.
- **Skip it?** Yes. You can paste the reviews yourself.

### A CMS API, a CRM, and an AI-visibility platform

- **A [CMS](glossary.md#cms) API.** No skill here writes to your CMS. The skills draft titles, markup, and merged pages, and your editors publish them. A CMS API only matters if you build your own publishing step, and then it is your build.
- **A CRM.** No skill reads one. Your CRM is where you confirm that search changes reached pipeline, which belongs in the leader summary and not in this kit.
- **An AI-visibility platform.** AI answers have their own kit, [AI visibility](../ai-visibility/start-here.md). Use it next to this one, since a gap in links or content often shows up there first.

## What you can run with nothing paid

The technical audit, `cannibalization`, `consolidate`, `internal-links`, `meta-fix`, `schema-gen`, `lighthouse`, `common-crawl-checker`, `competitor-content`, `review-mining`, `reddit-research`, `autocomplete-paa`, `persona-jury`, and `research-synthesis`, plus the free path of `backlink-gap` and `keyword-discovery`. These need only a Claude plan, Python, Search Console, and a crawl export.

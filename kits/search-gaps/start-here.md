# Search and Competitor Gaps: Start Here

Leaders ask why a competitor outranks you on the pages that matter, and the answer comes back as three screenshots from three tools, each pulled on a different day. Nobody can say which of last quarter's fixes worked, the [backlink](glossary.md#backlink) list has no owner, and the technical audit is a score nobody can reproduce.

That is the black box in a team setting. Not a secret, just a pile of reports with no shared dates, no owners, and no way to rerun them. This kit replaces it with one repeatable gap review that your team runs on a schedule and can defend line by line.

## What your team will have at the end

- One shared [baseline](glossary.md#baseline) (queries, pages, keywords, competitors, and a date) that every check reads, so two analysts never disagree about the same page.
- A [gap register](glossary.md#gap-register), one list of findings with the evidence behind each, an owner, a due date, and a check-back date.
- A [run log](glossary.md#run-log) that shows every scheduled slot, whether it ran, and what happened when it did not.
- A one-page summary for leaders that says what changed, what you found, what ships next, and what the checks could not see.

## Who this is for

An [SEO](glossary.md#seo) manager, content operations owner, or marketing lead who runs many pages through a [CMS](glossary.md#cms), pays for at least one SEO platform, and gets asked "how do we know." You don't need to learn SEO here. You need a method that holds up when someone challenges the numbers.

This is the full team version and needs [Claude Code](glossary.md#claude-code). If your team is two people and a free [Search Console](glossary.md#search-console) login, the small-business versions of the same method live in [Website check-up](../website-checkup/start-here.md) and [Customer-language research](../customer-research/start-here.md), and they run in a spreadsheet and a chat window. [Choose your version](choose-your-version.md) shows the difference.

## The 17 skills and what each does

A [skill](glossary.md#skill) is a saved set of instructions Claude Code loads when a task matches. These come from the two small-business kits and are unchanged. Your guides here cover what changes at team scale: scheduling, many sites, owners, and reporting.

| Skill | What it does | Needs a paid platform |
|---|---|---|
| `baseline-data` | Builds and dates the shared snapshot the other checks read | No |
| `technical-seo-audit` | Scores [crawl](glossary.md#crawl) findings by search impact, business impact, and effort | No (needs a crawl export) |
| `keyword-discovery` | Builds the list of searches around your topics and finds what you never addressed | Optional, for volume |
| `backlink-gap` | Finds sites that link to competitors and not to you, in tiers, with anchor profile | Yes, for the competitor view |
| `cannibalization` | Finds your own pages competing for the same query | No |
| `consolidate` | Checks that a merge is right, picks the winner, drafts the page and the [redirect](glossary.md#redirect) plan | No |
| `internal-links` | Finds [orphan pages](glossary.md#orphan-page), buried pages, and guide-to-service gaps, with exact links to add | No |
| `meta-fix` | Rewrites titles, descriptions, headings, and sharing text with options and reasons | No |
| `schema-gen` | Writes [JSON-LD](glossary.md#json-ld) [structured data](glossary.md#structured-data) from a page's visible content | No |
| `lighthouse` | Checks speed and quality, [field data](glossary.md#field-data) first, against [Core Web Vitals](glossary.md#core-web-vitals) | No |
| `common-crawl-checker` | Tests whether [Common Crawl](glossary.md#common-crawl)'s crawler can reach you | No |
| `competitor-content` | Maps what competitors publish, how deeply, and what nobody covers | No |
| `review-mining` | Pulls customer wording out of public reviews, with exact quotes | No |
| `reddit-research` | Reads public forums for how people describe the problem | No |
| `autocomplete-paa` | Collects search-box suggestions and People Also Ask questions | No |
| `persona-jury` | Pre-screens wording against personas built from real quotes | No |
| `research-synthesis` | Merges all the customer evidence into one phrase list with counts | No |

Sixteen of the 17 do their whole job without a paid platform. A paid link database is needed for the one thing nobody can see for free, which is how many sites link to your competitors. Every report says on its first line which path it used.

## How the pieces fit

1. The baseline gets refreshed, so every later check works from the same dated numbers.
2. Own-site checks run: technical audit, [cannibalization](glossary.md#cannibalization), internal links, speed, crawler access.
3. Competitor checks run: backlink gap, competitor content, keyword gaps.
4. Customer-language checks run on a slower cycle and supply the wording evidence.
5. Findings go into the gap register with an owner. The run log records that the slot happened.
6. A person cross-checks direction against a second platform before anything reaches a leader.

## What you need

- Claude Code and [Python](glossary.md#python) on the computer that runs the checks.
- Read access to [Search Console](glossary.md#search-console) for each site, and a crawl export for each ([Screaming Frog](glossary.md#screaming-frog) or similar).
- One person who owns the schedule, and a named owner for each site.
- Optional but useful: [Ahrefs](glossary.md#ahrefs) or another link database, [Bing Webmaster Tools](glossary.md#bing-webmaster-tools), and [GA4](glossary.md#ga4).

The [shopping list](shopping-list.md) names every platform and key, and says which skills still work without it.

## Where to start

1. [SG-FU-01: Set up the team workspace](setup/SG-FU-01-set-up-the-team-workspace.md)
2. [SG-FU-02: Run it on a schedule](setup/SG-FU-02-run-it-on-a-schedule.md)
3. [SG-FU-03: Owners, evidence, and reporting](setup/SG-FU-03-owners-evidence-and-reporting.md)

If something breaks, look up its code in [fixes](fixes.md). To see why this kit exists, read [what David built](what-david-built.md).

> **Want it fitted to your stack?** Pigasus Group sets these up for in-house teams: your platforms, your CMS, your reporting cadence. Start at https://pigasus.group/contact.

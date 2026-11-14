# Measurement and Exec Reporting: Start Here

A leader asks whether AI search is costing pipeline. [GA4](glossary.md#ga4) says organic is flat, [Search Console](glossary.md#search-console) says clicks are down, an AI-visibility tool says mentions are up, and the [CRM](glossary.md#crm) says leads fell. Each number is defensible, and nobody can say which one to act on. That is the black box in team form: a dashboard everyone reads, a cause nobody tested, and a monthly deck that answers "what happened" without ever answering "how do you know."

This kit gives an in-house team a monthly cycle that answers the second question. You will have tracking you can trust, a rule that no number is explained until it has been checked on a second independent platform, a view of AI-driven traffic that is honest about being a [floor](glossary.md#floor), and a report leaders can read in five minutes.

## What the team will have at the end

- A [source map](glossary.md#source-map) that says which platforms measure which question, so "direction" is always confirmed on at least two that do not share upstream data.
- Tracking events added through [Google Tag Manager](glossary.md#google-tag-manager) in a way that is additive, reversible and tested before publishing.
- A named owner for every pull, check and report, and a log that shows a missed slot the same day it happens.
- A [GA4](glossary.md#ga4) channel for AI referrals and a count of Search Console queries that look like leaked AI conversation turns, both reported as lower bounds.
- A monthly report where every figure carries its source, filter and date range, every move carries graded causes, and every finding ends with an action and an owner.
- A flat-table export that keeps a [Looker Studio](glossary.md#looker-studio) dashboard current, and a final evidence review before the report leaves the team.

## Which skill does what

The skills already exist. This kit does not copy them. It shows how a team runs them together, and it links to the pages that teach each one.

| [Skill](glossary.md#skill) | What it does for the team | Needs |
|---|---|---|
| `ga4-events-setup` | Plans custom events, writes a [Tag](glossary.md#tag) Manager import file of new prefixed pieces, builds the AI referral channel | Tag Manager and GA4 access; the planning part needs no keys |
| `gsc-read` | Captures Search Console week over week, lists new, lost, spiking and dropping queries, checks indexing | A read-only [service account](glossary.md#service-account) |
| `clarity-analytics` | Pulls [Clarity](glossary.md#clarity) behavior data and its AI visits, finds rage-click pages | A Clarity token (read-only) |
| `ai-traffic-classifier` | Flags Search Console queries shaped like leaked AI turns, as a floor | A Search Console query export |
| `metric-check` | Defines each moved number, tests the measurement, grades causes, confirms direction on a second source | Nothing; it works on figures you give it |
| `monthly-report` | Writes the report from the checked numbers and your [change log](glossary.md#change-log) | The numbers and the change log |
| `looker-export` | Writes one validated [CSV](glossary.md#csv) per dashboard tab | A Google Sheet behind the dashboard |
| `evidence-review` | Grades findings and borrowed statistics before the report goes to leaders | Nothing |

Six of these come from the [Measure what matters kit](../measure/start-here.md): `ga4-events-setup`, `metric-check`, `gsc-read`, `clarity-analytics`, `looker-export` and `monthly-report`. `ai-traffic-classifier` comes from the [AI search kit](../ai-visibility/start-here.md), and `evidence-review` from the [Plain writing kit](../plain-writing/start-here.md).

## What the team needs

- Claude Code on at least one machine, a plan that includes it, and someone comfortable at a terminal. See [Install Claude](../../guides/install-claude.md).
- Read access to GA4, Search Console and your tag [container](glossary.md#container). [Bing Webmaster Tools](glossary.md#bing-webmaster-tools) and a rank tracker or SEO platform make the direction checks stronger.
- **A change log that someone keeps.** Launches, edits, tracking changes, campaigns and outside events, with dates.
- One person who owns the report and one who owns the data pulls. They can be the same person on a small team.

The [shopping list](shopping-list.md) names every dependency, what it costs to find out, and which skills still work without a paid platform. Plan on about half a day to set up and about two hours a month to run.

## Where to go next

1. Read [Choose your version](choose-your-version.md) if you run a smaller shop and want the free or low-cost path.
2. Start the team setup with [MR-FU-01](setup/MR-FU-01-set-up-the-team-and-the-source-map.md).
3. Keep the [fixes table](fixes.md) open when a pull misses or two platforms disagree.
4. See [what David built](what-david-built.md) for the problem this came from.

> **Want it fitted to your stack?** Pigasus Group sets these up for in-house teams: your platforms, your [CMS](glossary.md#cms), your reporting cadence. Start at https://pigasus.group/contact.

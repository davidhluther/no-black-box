---
name: monthly-report
description: Write a monthly website performance report for a board, a boss or a client, covering search traffic, site visits, leads and AI visibility, with every number sourced, every cause graded and every gap named. Use when asked for a monthly report, a performance summary, a board update or a "how did the website do this month" write-up. Pulls from Search Console, GA4 and optional tools, and runs the metric-check skill on every move before the report is finished.
---

# Monthly report

Works in: Claude Code, Claude.ai, ChatGPT for writing the report from numbers you paste in. Pulling numbers by script or connector needs Claude Code (full version).

Plain words used below:
- GA4 (Google Analytics 4, Google's free tool that counts visits to a website)
- event (one recorded action, such as a page view, a download click or a form being sent)
- key event (an event you count as a goal reached, such as a completed contact form)
- session (one visit to your site)
- impression (one time a page was shown in a search result, clicked or not)
- click-through rate (the share of views that became clicks)
- Search Console (Google's free report of how your site appears in Google search)
- Looker Studio (Google's free dashboard tool)
- Clarity (Microsoft Clarity, a free tool that shows how visitors click and scroll on a site)
- CSV (a plain table saved as text, one row per line with commas between the columns)
- single-source (a figure confirmed on only one platform)
- skill (a folder of written instructions an AI tool follows to do one job the same way each time)




Question the report answers: "How did search and AI visibility track this month, and what does the reader need to know or decide?"

## Read config first

Read `config.json` for the organization name, site address, GA4 property ID, report month format and the list of sources the organization actually has. If a source is missing, say so in the report; do not skip the section silently.

## Inputs

1. Last month's report, if any, so the same measures are used.
2. Search Console figures for the month and the month before: clicks, impressions, click-through rate (the share of views that became clicks) and average position, by query and by page. Use the `gsc-read` skill or the Search Console web export.
3. GA4 figures for the same two months: sessions, engaged sessions, key events (conversions), organic search sessions, AI referral sessions (see `ga4-events-setup`).
4. Optional: Bing Webmaster Tools, Clarity, an AI-answer tracker, ad platform or email platform results, and a list of changes the organization made.
5. A change log: every launch, edit, redesign, tracking change, campaign and outside event (a search engine update, an outage) with its date.

## Steps

1. **Confirm the data.** Both months cover full calendar months, same length or normalized per day. Note the date each source runs through; Search Console lags a few days.
2. **Pull the numbers into one table.** One row per measure, columns for this month, last month, the change, source and filter. Put it in the Looker Studio data sheet if there is one (see `looker-export`).
3. **Flag moves.** Anything up or down by more than a threshold you set (start at 20% and at least 100 events behind it) gets a block from `metric-check`.
4. **Run `metric-check` on each flagged move.** Define the measure, check the measurement, grade the causes, confirm direction on two independent sources. Do not write a cause until this is done.
5. **Write the report** using the shape below.
6. **Read it back** against the rules below, then send.

## Shape of the report

1. Bottom line (three sentences: what happened, why we think so and how sure, what to do).
2. The numbers table (every figure has its source and date range).
3. Flagged moves, each as a `metric-check` block.
4. What worked and what is broken (short lists, tied to the change log).
5. AI visibility, in its own section, with the floor-not-total note.
6. Next month: actions, owners and dates.
7. Caveats: tracking changes, data gaps, anything marked single-source or not computable.

## Rules that carry the method

- **No naked numbers.** Every number names its source, filter and date range. Paid and organic are always labeled. Search figures name the engine.
- **Define the measure.** Say what a lead is. Do not substitute a related measure when the one you want is unavailable (key events on AI referrals are not "leads from AI").
- **Rates name their basis.** "Share of prompts with a mention" and "share of posts cited" are different rates. Say which, and never mix tracker question sets in one table.
- **Not computable means a named gap.** Never estimate a number the data cannot give. Write "not available this month, because ...".
- **Growth multiples use actuals.** Never divide by a projection.
- **A tracking or definition change is never a drop.** If one happened this month, compare like with like or leave the figure out and say why. If a site move or redesign is under way, say which changes come from the move and which from performance.
- **Tools that summarize other tools.** Treat a tool that shows Search Console numbers as Search Console.
- **Third-party statistics need a primary source.** Do not quote a figure from a newsletter. Find the original, or describe the trend without the number.
- **Never put test or staging web addresses in the report.** Check every link.
- **Tell the reader what to do.** Each finding ends with an action and an owner.

## Output

A document in Markdown (and a Word or PDF copy if the reader wants one, made with whatever tool the user has). Name it `monthly-report-<org>-<yyyy-mm>.md`. Keep a copy of the numbers table beside it as CSV so next month's report can compare.

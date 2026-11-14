---
name: looker-export
description: Turn monthly report numbers into flat, consistent tables in a Google Sheet that Looker Studio (Google's free dashboard tool) reads, so a dashboard updates itself each month. Produces one CSV per tab with exact headers, upload steps, and a check that headers match the layout. Use when asked to build or refresh a dashboard, push report data to a sheet, or prepare data for Looker Studio.
---

# Looker export

Works in: Claude Code, Claude.ai, ChatGPT for the table layouts and checks. The script `scripts/validate_tabs.py` needs Python 3.

Plain words used below:
- GA4 (Google Analytics 4, Google's free tool that counts visits to a website)
- channel group (a way of sorting visits into labeled buckets such as Organic Search, Direct and Email)
- Search Console (Google's free report of how your site appears in Google search)
- Looker Studio (Google's free dashboard tool)
- CSV (a plain table saved as text, one row per line with commas between the columns)
- skill (a folder of written instructions an AI tool follows to do one job the same way each time)




Looker Studio draws charts from a data source. The simplest data source for a small organization is a Google Sheet where each tab is a flat table: one row per month (or per item), one column per fact, no merged cells, no notes inside the table. This skill keeps those tabs consistent so charts never break.

## Read config first

Read `config.json` for the sheet name and the organization name. Tab names and headers come from `references/tab-layouts.json`.

## Steps

1. **Gather the month's numbers** from the report's numbers table (see `monthly-report`).
2. **Write one CSV per tab** into a folder named `looker-export/`, with headers exactly as in `references/tab-layouts.json`. Dates as `yyyy-mm-dd`. Numbers with no thousands commas, no percent signs (store 0.042, not 4.2%), no currency symbols. Blank means missing; never write 0 for missing.
3. **Check them:** `python3 scripts/validate_tabs.py looker-export/`. It reports wrong or missing headers, non-numeric cells in number columns, and dates in the wrong format. Fix everything it lists.
4. **Write `UPLOAD_INSTRUCTIONS.md`** for the user with the first-time and monthly steps below.
5. **Tell the user** what was saved and where, and offer to help lay out the Looker Studio report.

## Tabs

| Tab | One row per | Source | How often |
|---|---|---|---|
| Monthly traffic | month | GA4, Search Console | monthly |
| Search queries | month and query | Search Console | monthly (top 50) |
| Top pages | month and page | GA4, Search Console | monthly (top 30) |
| AI referrals | month and AI source | GA4 channel group "Channels with AI" | monthly |
| Flagged moves | flagged move | metric-check blocks | monthly |
| Actions | action | the report's next-month list | when updated |

Optional extras: Competitors, Content published, Page speed. Add them to the layout file first, then export.

## First-time setup (for the user)

1. Create a Google Sheet with the name in `config.json`.
2. Make one tab per row of the table above, same names.
3. File, Import, Upload each CSV into its tab, choosing "Replace current sheet" the first time.
4. In Looker Studio, Create, Report, Add data, Google Sheets, choose the sheet and one tab. Repeat per tab you want to chart.
5. Build the charts. Share the report with "Viewer" access for readers.

## Monthly refresh

Append the new rows under the existing ones (Import, "Append to current sheet"). Never replace, because history is the point. Looker Studio re-reads the sheet on its own; use its Refresh data button if a chart looks stale.

## Safety

The data sheet holds totals, not people. Never put names, email addresses or form entries in a tab. Check sharing settings on the sheet before sharing the dashboard.

# Run Your Monthly Check (Free, Guide 5)

This is the routine you repeat each month. It takes about 45 minutes once the sheet is set up. The point is to check a number before anyone explains it.

1. **MM-FR-05-1.** Update the sheet. Add last month's rows to "Monthly traffic", "Search queries", "Top pages" and "AI referrals" the way guide 2 and guide 4 showed. Write the date each source runs through in the "data_through" column. [Search Console](../glossary.md#search-console) runs a few days behind.
   You'll know it worked when the newest row in every tab has last month's date. Click Kit help, then "Run check-up" and confirm the code ends in E00; if not, see fixes.md.

2. **MM-FR-05-2.** Find the moves. Compare this month's row with last month's. Mark any measure that moved by more than 20 percent and has at least 100 [events](../glossary.md#event) behind it. Small numbers swing by chance, so a 50 percent change on eight visits is not a finding.
   You'll know it worked when you have a short list of measures to look at, possibly none. None is a fine answer.

3. **MM-FR-05-3.** For each move, run the check. Open a free AI model, paste prompt 4 from `free/prompts.md` with your numbers (totals only), and answer its questions about what changed: tracking, forms, [tags](../glossary.md#tag), site edits, campaigns, outside events. Also open `free/checklist-metric-check.md`. The check asks four things in order. Is the number real (same dates, same definition, no tracking change inside the window)? What could have caused it? For each cause, what is the evidence for and against, graded holds, weakened or refuted? Which second source agrees?
   You'll know it worked when each move has a graded list of causes in your "Flagged moves" tab. If the AI model states a cause as fact with no grade, tell it to grade it or write "not verified". A tracking change you made in guide 3 is never a drop or a gain; compare like with like.

4. **MM-FR-05-4.** Confirm the direction on a second independent source. For search traffic, compare Search Console clicks with [GA4](../glossary.md#ga4) organic [sessions](../glossary.md#session) for the same pages and dates. Bing Webmaster Tools is a good third. Sources that read the same upstream data count as one. Use prompt 5 in `free/prompts.md` if they disagree. Write the result in the "sources_agree" column: yes, no or [single-source](../glossary.md#single-source).
   You'll know it worked when every move has a yes, no or single-source. If sources disagree, write "direction disputed" and do not act on the figure yet; the usual reasons are a feed that starts late, address variants like www or a trailing slash, and different day boundaries (it's E17).

5. **MM-FR-05-5.** Write the report. Paste your numbers table and flagged moves into prompt 7 in `free/prompts.md`. Read what comes back. Every number needs a source, a filter and a date range. Anything that could not be measured is listed as not available, never guessed.
   You'll know it worked when a reader who has never seen your analytics could follow the bottom line. Run prompt 8 on the finished report and fix what it finds.

6. **MM-FR-05-6.** Send it and save it. Add the sheet link and the report to the same folder, named with the month, such as "report 2026-09". Use `free/checklist-monthly-report.md` as your last check before sending.
   You'll know it worked when the checklist is fully ticked. Put a reminder on your calendar for the same day next month. If you ever skip a month, write it in the sheet instead of letting it pass quietly, so the gap is visible later.

If this routine becomes a chore, the [low-cost version](MM-LC-01-pull-search-console-into-your-sheet.md) fills the sheet for you.

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

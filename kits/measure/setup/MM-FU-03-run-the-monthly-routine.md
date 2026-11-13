# Run the Monthly Routine (Full, Guide 3)

With [skills](../glossary.md#skill) and read-only access in place, the monthly routine is a short conversation with Claude Code and a few checks. About 30 minutes a month.

1. **MM-FU-03-1.** Pull the numbers. Ask Claude Code to use gsc-read for the latest capture, then verify it (the skill includes `verify_capture.py`), and to pull [Clarity](../glossary.md#clarity) with `--days 1` into your own measurement folder. Also export last month's [GA4](../glossary.md#ga4) totals, or read them from your sheet if you also use the low-cost pulls.
   You'll know it worked when you have a dated [Search Console](../glossary.md#search-console) file that the verifier calls "adoptable", a Clarity file, and GA4 totals. If the verifier says "not adoptable", read its one-line reason; the capture is probably a day old or hit the row cap.

2. **MM-FU-03-2.** Run the checks before writing. Ask: "Use metric-check on every number that moved more than 20 percent." For each move it defines the measure, checks the measurement, grades causes (holds, weakened or refuted), confirms the direction on a second independent source and ends with an action and an owner. Run `python3 scripts/check_report.py` on the draft later to catch gaps.
   You'll know it worked when each move has a block shaped like `assets/flagged-move-template.md`. If two sources disagree, the block says "direction disputed" and nothing recommends acting on it.

3. **MM-FU-03-3.** Write the report. Ask: "Use monthly-report for last month." Give it the change log: every launch, edit, tracking change, campaign and outside [event](../glossary.md#event), with dates.
   You'll know it worked when you have `monthly-report-<name>-<yyyy-mm>.md` with a bottom line, a numbers table with sources and dates, graded moves, an AI visibility section shown as a floor, actions and caveats.

4. **MM-FU-03-4.** Update the dashboard. Ask: "Use looker-export for last month." It writes one [CSV](../glossary.md#csv) per tab and runs `validate_tabs.py` to check headers, dates and number formats. Import the CSVs by appending to your sheet (never replace; history is the point). [Looker Studio](../glossary.md#looker-studio) redraws on its own.
   You'll know it worked when the validator prints "ok" and the dashboard shows the new month.

5. **MM-FU-03-5.** Never let a scheduled pull fail quietly. If you schedule any of these with your computer's scheduler, make it write a line to a log you read, and make a miss visible the same day: an email, a message or a note in your sheet. Run it again by hand after a miss and record the gap.
   You'll know it worked when you can show, for any month, either the data or a note saying why it is missing.

6. **MM-FU-03-6.** Run the kit's check-up command from the repository folder: `python3 support/doctor.py measure`. Copy the support code it prints.
   You'll know it worked when it prints a code and says what it checked. Keep the code with your report in case you need help.

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

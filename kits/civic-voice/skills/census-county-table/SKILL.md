---
name: census-county-table
description: Pull American Community Survey (the Census Bureau's yearly sample survey) numbers such as income, poverty, rent, and age for the counties you choose, with the margin of error (the plus-or-minus amount) beside every number and a flag where a number is too uncertain to lean on. Free route uses data.census.gov or Census Reporter and a spreadsheet. Full route runs a short program in Python (a programming language, with nothing extra to install) against the Census Bureau's data service with your own key, read from a setting held in memory instead of a file. Use when a resident, civic group, or nonprofit needs county figures for a comment, a grant, or a community report. Neutral and read-only.
---

# Census county table

Works in: Claude Code (full version) for the script (a small program in a text file that does one job). The free route below works in any web browser plus a spreadsheet.

The American Community Survey (ACS) is the Census Bureau's yearly survey that estimates income, rent, poverty, age, and housing for every county. The numbers are estimates drawn from a sample, so every one comes with a margin of error (the plus-or-minus amount that goes with an estimate). This skill (a folder of written instructions an AI program can load for a job) gets the numbers, keeps the margins attached, and says which comparisons the data can and cannot support.

## Ground rules

1. **Estimates, not counts.** Say "an estimated 14%," never "14% of residents." Always carry the margin of error and the period ("2020 to 2024 5-year estimates").
2. **Use five-year estimates for small counties.** They are based on more responses and are steadier. One-year estimates exist only for places with larger populations. Say which one you used.
3. **Do not claim a difference the data cannot show.** Two estimates differ only if the gap is bigger than their combined margins of error (see `references/margin-of-error.md`). Otherwise write "not clearly different."
4. **Flag the shaky numbers.** The script flags a number when its margin of error is more than 30% of the estimate. That cutoff is this kit's rule of thumb, not a Census Bureau standard. The user may change it.
5. **Nothing secret in files.** The Census key is read from the environment variable (a named setting held in memory for one terminal (a window where you type instructions instead of clicking) session) `CENSUS_API_KEY`. Never print it, paste it into a chat, save it in a file, or put it in a screenshot.
6. **Source line every time.** "U.S. Census Bureau, American Community Survey, 2020 to 2024 5-year estimates, retrieved mm/dd/yyyy." Link the table or tool you used.
7. **No political positions.** Report what the numbers show and what they cannot show.

## Read the settings

Read `config.json` for the state, the counties, the period (`census.year`), and whether to include a statewide row. If missing, ask for those three things.

## Step 1: Decide what you need

Ask: which counties (and the state for a yardstick)? Which questions (income, poverty, rent, housing cost burden, age, vehicles, benefit use)? What will the numbers be used for (a comment, a grant, a report)? Pick at most a dozen measures. The default list is in `references/measures.md`, with the Census table number behind each one.

## Step 2a: Free route (no key, no code)

1. **Census Reporter.** Open censusreporter.org, search for a county, and open its profile. Use the "compare" feature to put several places side by side. Every number shows its margin of error. Copy into the tracker sheet.
2. **data.census.gov.** Search the table number (for example B19013 for median household income), choose "Geos" and pick the counties, choose the 5-year ACS vintage, and download the table as a CSV (a plain table saved as text with commas between the columns). Each estimate has a paired margin-of-error column (named with an M).
3. Paste into the sheet using the `free/templates/county-numbers.csv` layout. Add the margin-of-error flag column by comparing each margin to the estimate.
4. Add the source line, vintage, and retrieval date on the sheet.

## Step 2b: Full route (script)

The script asks the Census Bureau's API (a way for two programs to talk, like a waiter carrying orders to the kitchen) for the numbers.

1. Check the key: `echo "${CENSUS_API_KEY:+key is set}"` prints "key is set" without showing the key. If empty, the user requests a key at api.census.gov/data/key_signup.html and sets it in their terminal for the session.
2. Preview with no network: `python3 -I scripts/acs_table.py --state "<state>" --counties "<A,B,C>" --include-state --dry-run`.
3. Run: `python3 -I scripts/acs_table.py --state "<state>" --counties "<A,B,C>" --include-state --year 2024 --out county-table`. The state can be the two-digit code.
4. The script writes `county-table-long.csv` (one row per county and measure) and `county-table-table.csv` (one row per measure, one column per county, with the margin beside each number and a note where it is large).
5. If it stops with "did not return data," that is usually the key (fix E16). If it names a variable, the Census table list changed (fix E17); check the variable on the Census Bureau's variable list for that year.

## Step 3: Check before you use it

- Open the table and check two numbers by hand against Census Reporter or data.census.gov for one county.
- Look at the flagged rows. Either drop the measure, combine groups, use a bigger area, or report the number with its margin and a plain warning.
- Confirm the period (vintage) on every table.
- For any county-versus-county or county-versus-state claim, use the `differs_from_reference` column. "unclear" means a number was missing.

## Step 4: Write it up

Give the user a short, plain paragraph per measure and one sentence on what the margin means, such as "The estimate is 14.2%, plus or minus 2.1 points, so the true figure is probably between about 12% and 16%." Never rank counties unless the differences are clear. Add the source line.

## What to hand back

The CSV files and where they are, the vintage, the flagged measures, and the comparisons that are and are not clear.

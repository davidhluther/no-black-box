# Fixes for Owner's Numbers

Find the code the [check-up](glossary.md#check-up) or [script](glossary.md#script) printed, read what you see, and follow the fix. If a fix does not work, send the code and the step ID to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

| Code | What you see | Why | The fix | Step |
|---|---|---|---|---|
| E01 | The check-up says a [tab](glossary.md#tab) is missing, or a [formula](glossary.md#formula) shows #REF! | A tab name is misspelled or a tab was deleted | Rename the tab to exactly Settings, Sales, Bank, Bookings, Scorecard or [Metrics](glossary.md#metric). Capital letters count. Re-import the template if one is gone | ON-FR-01-3 |
| E02 | The check-up says a header row does not match | A column is missing, out of order or renamed | Copy the header row from the matching file in `free/templates/` and rearrange your columns to match | ON-FR-02-4 |
| E03 | Month start or end is flagged | The date is blank, typed as text, or the end is before the start | Retype the dates in rows 3 and 4 of Settings in a form like 09/01/2026. They should sit on the right of the cell | ON-FR-03-1 |
| E04 | Business name is flagged | Settings B2 is empty | Type your business name in B2 | ON-FR-03-1 |
| E05 | Sales tab has no data rows | The [export](glossary.md#export) was not pasted, or it was pasted above the header | Paste the rows under the header row, starting in A2 | ON-FR-02-4 |
| E06 | Bank tab has no data rows | Same as E05 for the bank file | Paste the rows under the header row, starting in A2 | ON-FR-02-5 |
| E07 | Some Bank rows have no category | Category is empty on those rows | Fill every row with one word from the list in the guide. Use prompt 1 in `free/prompts.md` for suggestions, and check them | ON-FR-02-6 |
| E08 | Some Bank rows use a category not on the list | A typo, such as "supply" for supplies, or a new word | Change the word to one on the list. If none fits, use other_fixed or other_variable | ON-FR-02-6 |
| E09 | Dates are stored as text | The export came in as words, not dates | Select the column, choose Format, Number, Date. If it stays on the left, use Data, Split text to columns, then format as a date | ON-FR-02-8 |
| E10 | Scorecard shows #NAME?, #VALUE!, #REF! or #N/A | A formula broke, a tab was renamed, or a column holds text where a number belongs | Check tab names first (E01). Then check that net_sales, amount and booked_minutes hold numbers only, with no dollar signs typed as text | ON-FR-03-7 |
| E11 | Bookings tab is empty | You did not paste booking rows | Fine if you take no bookings. The customers and capacity numbers stay empty. Otherwise paste the booking report | ON-FR-02-7 |
| E12 | No rows fall inside the month | The month dates on Settings do not match the dates in your data | Fix the dates on Settings, or paste the right month of data | ON-FR-03-2 |
| E13 | Settings formulas are missing | Column D or E was overwritten | Copy the formulas back from `free/formulas.md` (Settings section) into rows 5 to 29 | ON-FR-03-7 |
| E14 | Metrics shows an error value | A Settings input is text or a formula points at a moved row | Check Settings column D has numbers. If you inserted rows, undo them | ON-FR-03-7 |
| E15 | Sign-in loop, an account that is not allowed, or no Extensions menu | The wrong account, a work account that blocks add-ons, or a plan limit | Sign in with a personal Google account. If you use a work account, ask its administrator whether [Apps Script](glossary.md#apps-script) is on | ON-FR-01-1 |
| E16 | No Kit help menu, or Google blocks the check-up | The page was not reloaded, or the program was not authorized | Reload the Sheet and wait a few seconds. Authorize again through Advanced, then Go to the project | ON-FR-01-8 |
| E17 | An imported file replaced another tab | The Import location was set to replace the sheet | Choose Edit, Undo. Import again with "Insert new sheet(s)" | ON-FR-01-3 |
| E20 | The script prints "Missing file" | A [CSV](glossary.md#csv) is not in the folder or has a different name | Name the files exactly sales.csv, bank.csv, bookings.csv and settings.csv. Bookings is optional | ON-FU-03-2 |
| E21 | The script prints "missing columns" | A header differs from the layout | Match the header row in `free/templates/` | ON-FU-02-2 |
| E22 | python3 is not found, or the version is below 3.9 | [Python](glossary.md#python) is not installed or is old | Install Python from python.org/downloads. On Windows, type py in place of python3 | ON-FU-01-2 |
| E23 | The script cannot read a date | A date uses a form like 09/01/2026 in a CSV | Rewrite dates as 2026-09-01 | ON-FU-02-5 |
| E24 | No rows fall inside the month | month_start and month_end do not cover your data | Edit settings.csv | ON-FU-03-2 |
| E25 | The script cannot write the output folder | The path is wrong or the folder is locked | Choose a folder you own, such as Documents | ON-FU-01-4 |
| E30 | The [AI model](glossary.md#ai-model)'s numbers differ from the Sheet or from your own sense | It misread a file, skipped rows or mixed up money in and sales | Ask it to list the rows it added. Trust the Sheet or the script, and tell it which number was wrong | ON-LC-02-4 |
| E31 | The AI model did not read a file, ignored the instructions, or says the text is too long | The file did not attach, a column is missing, or too much was pasted into the Instructions box | Attach the files again, check the header rows, and paste only the instructions | ON-LC-01-3 |
| E32 | A number appears that you never gave, with no [what-if](glossary.md#what-if) label | The AI model assumed an input | Tell it to label the result what-if, name the assumed input, and ask you for the real number | ON-LC-02-5 |
| E33 | An account number or a person's name is in an export | The bank file kept a column you do not need | Delete that column before attaching or pasting. If it was shared, delete the chat and tell your bank if a full account number was exposed | ON-FR-02-2 |

## Codes for the other kit steps

A [support code](glossary.md#support-code) reads in this order, for example ON-FR-03-1-E03-v0.1.0-7KQ. ON is the kit, FR the free version, 03-1 the guide and step where the first problem sits, E03 the problem, v0.1.0 the kit version, and 7KQ a check on the results. The check-up never reads what is inside your cells.

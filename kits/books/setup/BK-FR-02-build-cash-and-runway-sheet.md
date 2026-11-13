# BK-FR-02: Build the Monthly Cash and Runway Sheet

You will end with a Google Sheet that tracks cash month by month and tells you how many months the money lasts. About 30 minutes. It uses only numbers you type from bank statements and QuickBooks reports. It never connects to QuickBooks, so it cannot change your books.

The sheet is seven [tabs](../glossary.md#tab) (labeled pages along the bottom of a Google Sheet). Each tab starts from a [CSV](../glossary.md#csv) file (a plain table saved as text) in the kit's `free/cash-runway-template` folder. If you have not downloaded the kit yet, follow [get the kit files](../../../guides/get-the-files.md) first. All starting numbers are invented examples that you will replace.

## Steps

1. **BK-FR-02-1.** Make a new Google Sheet at sheets.google.com and name it "Treasurer cash and [runway](../glossary.md#runway)". For each of the seven CSV files in the `free/cash-runway-template` folder, click File, Import, Upload, choose the file, pick Insert new sheet(s), and click Import data. Google names each new tab after its file, such as "Settings.csv", so rename each tab right after you import it: double-click the tab name, delete ".csv", and press Enter. Delete the empty "Sheet1" at the end.
   You'll know it worked when the bottom of the sheet shows these tabs spelled exactly like this: Settings, Accounts, Commitments, Monthly cash, Runway, QB Profit and Loss, QB [Balance Sheet](../glossary.md#balance-sheet). If a tab name is still different (a ".csv" left on the end, or a capital letter missing), double-click the tab name to fix it. It's E04.

2. **BK-FR-02-2.** Look at row 1 of each tab and compare it with the list in `cash-runway-formulas.md`. Settings should start with "Setting, Value, Note", for example.
   You'll know it worked when each header row matches word for word. If one differs, retype it (E08).

3. **BK-FR-02-3.** Open the Settings tab and replace the six example values in column B (rows 2 to 7): organization name, fiscal year start month, reserve target in months, minimum cash floor, first month shown, and opening cash balance. The opening balance is your total cash the day before the first month, from your bank statements.
   You'll know it worked when no cell in B2 to B7 is empty. If the [check-up](../glossary.md#check-up) later says a setting is empty, it's E07.

4. **BK-FR-02-4.** Open Monthly cash. Replace the example Cash in and Cash out numbers with your own, one row per month, as positive numbers from your bank statements or the QuickBooks bank [register](../glossary.md#register). Then open Accounts and Commitments and replace the example rows. Finally open Runway.
   You'll know it worked when Runway shows numbers in rows 2 to 12 and no cell shows a red error such as #REF! or #NAME?. If you see one, it's E03.
   Runway means how many months you can keep operating before the cash runs out. If your average net change is not negative, the sheet says "Not shrinking" instead of a number.

5. **BK-FR-02-5.** On the Accounts tab, type each account's balance from QuickBooks (Books balance) and from the bank statement (Bank balance) for the same date. Mark Yes under Restricted for money that can be spent only for a named purpose. That is [restricted funds](../glossary.md#restricted-funds).
   You'll know it worked when the Difference column shows a number for each account. A Difference of zero means the books agree with the bank. A number that is not zero is your first question to investigate, and `free/prompts.md` section 2 shows how.

## What to do next

Add the check-up button with guide BK-FR-03. Each month, follow `free/monthly-routine-checklist.md`.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-FR-02-3). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

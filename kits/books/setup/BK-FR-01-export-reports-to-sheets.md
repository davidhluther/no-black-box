# BK-FR-01: Export Your QuickBooks Reports to Google Sheets

You will end with three QuickBooks reports sitting in Google Sheets, ready to read or paste into an AI model. About 25 minutes. This guide only looks at your books. Exporting a report cannot change them, and nothing here asks you to add, edit, send, or delete anything. Everything is [read-only](../glossary.md#read-only) (able to look but not touch).

QuickBooks changes its screens often. The names below are what we saw, and yours may differ a little. The idea is the same: find the report, set the dates, find the Export button.

## Before you start

You need a QuickBooks Online login that can see reports and a Google account. If you do not have a Google account, see [Keys and accounts](../../../guides/keys-and-accounts.md).

Guide BK-FR-02 uses the kit's own template files. You can download them now or when you get there. The shared guide [get the kit files](../../../guides/get-the-files.md) shows how to download them from https://github.com/davidhluther/no-black-box and unzip them on Windows, Mac or a Chromebook.

## Steps

1. **BK-FR-01-1.** Open Google Sheets (Google's free spreadsheet app) at sheets.google.com and sign in. Click the blank page with a plus sign.
   You'll know it worked when you see an empty grid. If you see a sign-in loop, it's E05.

2. **BK-FR-01-2.** In a new browser window, open QuickBooks Online at qbo.intuit.com and sign in. Look at the company name in the top corner and make sure it is the right organization.
   You'll know it worked when you see the QuickBooks home screen with your organization's name. If you see the wrong company, use the company switcher at the top and pick the right one (E12).

3. **BK-FR-01-3.** In the left menu, click Reports. You want the [balance sheet](../glossary.md#balance-sheet), which lists what you own and what you owe on one day. In the search box, type "Balance Sheet" and open it. Set the date to the last day of the month you are reporting, for example 09/30/2026. Under the accounting method, choose Accrual. Click Run report.
   You'll know it worked when you see a list of accounts with amounts. If you see no amounts, widen the date and run again (E38).
   An accounting method tells QuickBooks when to count money. [Accrual basis](../glossary.md#accrual-basis) counts it when earned or owed, and [cash basis](../glossary.md#cash-basis) counts it when it moves in the bank. Use the same one for every report you export, and write down which one.

4. **BK-FR-01-4.** Click the Export button near the top right of the report (it may look like an arrow pointing out of a box). Choose Export to Excel, or Export to Google Sheets if your screen offers it.
   You'll know it worked when a file downloads, or a new Google Sheet opens. If you can't find an Export button, it's E01.
   Exporting writes a copy of what is on the screen. It does not touch your books.

5. **BK-FR-01-5.** If a file downloaded, go back to the Google Sheet from step 1. Click File, then Import, then Upload, and drop the file in. Choose Insert new sheet(s), then Import data.
   You'll know it worked when a new [tab](../glossary.md#tab) (a labeled page along the bottom of the sheet) appears with your report. If the numbers look like text with a dollar sign and cannot be added, it's E02.

6. **BK-FR-01-6.** Repeat steps 3 to 5 for two more reports. For the [profit and loss report](../glossary.md#profit-and-loss-report), search "Profit and Loss", set the same accounting method, and run it once for the month and once for the fiscal year to date. Then, only if you will do the cash checks, export the [general ledger](../glossary.md#general-ledger) report for the month (search "General Ledger"). It lists every entry, one line each.
   You'll know it worked when you have a tab for each report. A profit and loss report is long, so scroll to the bottom to see the net income line.

7. **BK-FR-01-7.** Check one number. Pick the total cash on the balance sheet. Compare the number in your Google Sheet with the number on the QuickBooks screen. They should match to the cent.
   You'll know it worked when they match. If they differ, you may have exported a different date or method (E39).

8. **BK-FR-01-8.** Protect people's privacy before you share any report with an AI model. In your Google Sheet, delete columns that show customer, donor, or employee names, or replace them with "Person 1", "Person 2". Do not paste bank account numbers, tax IDs, or addresses.
   You'll know it worked when you can scroll through the tab and see no names you would not say aloud in a public meeting.

## What to do next

Go to guide BK-FR-02 to build the monthly cash and [runway](../glossary.md#runway) sheet, or to BK-FR-03 to ask questions about the reports you just exported.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

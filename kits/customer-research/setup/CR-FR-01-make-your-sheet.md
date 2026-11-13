# CR-FR-01: Make Your Sheet

You will build one Google Sheet with five [tabs](../glossary.md#tab) and add the [check-up](../glossary.md#check-up) button. Time: about 25 minutes. You need a Google account and nothing else. The files you import are in this kit's [free folder](../free/).

1. **CR-FR-01-1.** Open Google Sheets (Google's free spreadsheet app) at sheets.google.com and sign in with your organization's Google account. Click the large "+" or "Blank spreadsheet" and name it "Customer research" by clicking "Untitled spreadsheet" at the top left.
   You'll know it worked when you see a blank grid with your new name on top. If you see a sign-in loop that keeps returning you to the sign-in page, it's E09.

2. **CR-FR-01-2.** Make the [Config](../glossary.md#config) [tab](../glossary.md#tab) (one page inside a spreadsheet, shown along the bottom edge). Choose File, then Import, then Upload, and select `config.csv` from the free folder. For "Import location" choose "Insert new sheet(s)", then click "Import data". Rename the new tab to exactly `Config` by double-clicking its name at the bottom.
   You'll know it worked when a tab named Config shows three columns called key, value, and note. If the import replaced your whole spreadsheet or squeezed everything into one column, it's E10. If the check-up later says the tab is missing, it's E01.

3. **CR-FR-01-3.** Repeat step 2 with `sources.csv` and name the tab exactly `Sources`.
   You'll know it worked when the tab shows one heading row with seven columns, starting with source_id. Problems here show as E02 or E10.

4. **CR-FR-01-4.** Repeat step 2 with `quotes.csv` and name the tab exactly `Quotes`.
   You'll know it worked when the tab shows a heading row with ten columns, starting with quote_id and ending with keep. Problems show as E03 or E10.

5. **CR-FR-01-5.** Repeat step 2 with `themes.csv` and name the tab exactly `Themes`.
   You'll know it worked when the heading row starts with [theme](../glossary.md#theme) and ends with action. Problems show as E04 or E10.

6. **CR-FR-01-6.** Repeat step 2 with `wording-tests.csv` and name the tab exactly `WordingTests` (no space).
   You'll know it worked when the heading row starts with test_id and ends with decision. Problems show as E05 or E10.

7. **CR-FR-01-7.** Add the check-up button. In your Sheet choose Extensions, then Apps Script (a tool built into Google Sheets that lets you attach small programs). A code editor opens with a file called Code.gs. Delete everything in it, open `checkup.gs` from the free folder in any text editor, copy all of it, paste it in, and click the disk icon to save. Name the [project](../glossary.md#project) "Customer research" if it asks.
   You'll know it worked when the editor shows your pasted text and no red error mark. The first time you run it, Google may say the app "hasn't been verified" because you wrote it yourself, not a company. Click "Advanced", then "Go to Customer research (unsafe)", then Allow. That warning is E13, and the script only reads your own Sheet.

8. **CR-FR-01-8.** Close the Apps Script tab, go back to your Sheet, and reload the page. A new menu called "Help" appears after a few seconds. Click Help, then "Run check-up".
   You'll know it worked when a box shows a [support code](../glossary.md#support-code) and a report that says all checks passed, except that the Config settings still need filling in, which is the next guide. If no Help menu appears, it's E11. If the report lists a missing tab, find that code in [fixes](../fixes.md) and go back to the step it names.

When the check-up passes the tab checks, go on to [CR-FR-02](CR-FR-02-collect-quotes.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like CR-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

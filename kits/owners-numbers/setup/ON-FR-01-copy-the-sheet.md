# ON-FR-01 Copy the Sheet and Add the Check-Up

You will build the empty scorecard Sheet from six template files and add a Kit help menu that tests it. Nothing here needs your real data yet.

1. **ON-FR-01-1.** Open [Google Sheets](../glossary.md#google-sheets) (Google's free spreadsheet app) at sheets.google.com and sign in with a Google account. For help with accounts, see the [keys and accounts guide](../../../guides/keys-and-accounts.md).
   You'll know it worked when you see a page of blank or recent spreadsheets. If you loop back to the sign-in page, or Google says the account is not allowed, it's E15.
2. **ON-FR-01-2.** Click Blank spreadsheet. Click "Untitled spreadsheet" at the top left and type Owner's Scorecard.
   You'll know it worked when the new name shows at the top. If nothing changes, click once more on the name and press Enter.
3. **ON-FR-01-3.** Import the six template files from the kit's `free/templates/` folder, one at a time. Choose File, then Import, then Upload, drag in `Settings.csv`, and under Import location pick "Insert new sheet(s)". Click Import data. Repeat for `Sales.csv`, `Bank.csv`, `Bookings.csv`, `Scorecard.csv` and `Metrics.csv`. Each [CSV](../glossary.md#csv) (a plain text table) becomes its own [tab](../glossary.md#tab) along the bottom.
   You'll know it worked when you see six new tabs. If a file lands on top of another one, it's E17. Use Edit, then Undo, and import again with "Insert new sheet(s)".
4. **ON-FR-01-4.** Rename each tab to exactly Settings, Sales, Bank, Bookings, Scorecard and [Metrics](../glossary.md#metric). Right-click a tab, choose Rename, type the name, and press Enter. Spelling and capital letters matter.
   You'll know it worked when the six names match this list. A misspelled tab is E01.
5. **ON-FR-01-5.** Delete the empty first tab called Sheet1. Right-click it and choose Delete.
   You'll know it worked when only six tabs remain. If a [formula](../glossary.md#formula) shows an error such as #REF!, a tab name from step 4 is wrong. That is E01.
6. **ON-FR-01-6.** Make results that rest on guesses easy to spot. On the Scorecard tab, select columns A to D. Choose Format, then Conditional formatting. Under "Format cells if" pick "Custom formula is", type `=$C1="what-if"`, pick a grey italic style, and click Done. Repeat on the Metrics tab.
   You'll know it worked when the basis column on Settings later shows grey text for example values. Nothing changes visibly yet.
7. **ON-FR-01-7.** Add the [check-up](../glossary.md#check-up). In the Sheet choose Extensions, then [Apps Script](../glossary.md#apps-script). ([Apps Script](../glossary.md#apps-script) is Google's way of adding a small program to a Sheet.) Delete the sample code, open `free/checkup.gs` from the kit in any text editor, copy all of it, paste it into the Apps Script window, and click the save icon. Name the project Owner's Numbers Check-Up.
   You'll know it worked when the window shows the pasted code with no red marks. If you cannot find an Extensions menu, it's E15.
8. **ON-FR-01-8.** Close the Apps Script tab and reload the Sheet. Wait a few seconds. A Kit help menu appears next to the other menus. Choose Kit help, then Run check-up. Google asks you to authorize the program. Click Continue, pick your account, click Advanced, then "Go to Owner's Numbers Check-Up", then Allow. The program only works on this one Sheet.
   You'll know it worked when a box titled Check-up result opens with a [support code](../glossary.md#support-code). At this point it will list problems about empty data tabs. That is normal. If no Kit help menu appears, it's E16.

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

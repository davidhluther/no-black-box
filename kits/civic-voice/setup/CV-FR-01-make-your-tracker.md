# CV-FR-01: Make Your Tracker

Free version, guide 1. You will make one [Google Sheet](https://sheets.google.com) with six tabs, and add a [check-up](../glossary.md#check-up) button that tells you whether it is set up right. It takes about 30 minutes. You need a Google account (see the [keys and accounts guide](../../../guides/keys-and-accounts.md) if you do not have one).

1. **CV-FR-01-1.** Open Google Sheets (Google's free spreadsheet app) at sheets.google.com and sign in. Click the blank "+" tile to start a new spreadsheet. Click the title at the top left and rename it "Civic voice tracker".
   You'll know it worked when you see an empty grid with your new title. If Google keeps sending you back to the sign-in page, it's E07.

2. **CV-FR-01-2.** Bring in the six tab templates. In the kit's `free/templates` folder, download these [CSV](../glossary.md#csv) files (a plain table saved as text): `meetings.csv`, `comments.csv`, `records-requests.csv`, `county-numbers.csv`, `transcripts.csv`, and `settings.csv`. In your sheet, choose File, then Import, then Upload, drag one file in, choose "Insert new sheet(s)", and click Import data. Repeat for each file. Then rename each new tab at the bottom to exactly: Meetings, Comments, Records requests, County numbers, Transcripts, Settings (capital first letter, same spelling, a space where shown).
   You'll know it worked when you see six tabs along the bottom with those names. If a whole row of headings landed in one cell, it's E06. If you skip a tab, the check-up will report E01.

3. **CV-FR-01-3.** Look at the first row of each tab. It should hold the column headings from the template, in the same order, with nothing added before them. Do not rename the headings; the check-up and the date highlighter look for them by name. You may add extra columns to the right.
   You'll know it worked when each tab's first row reads like "Meeting date, Body, Item number..." for Meetings. If the check-up later says a header differs, it's E02.

4. **CV-FR-01-4.** Open the Settings tab and fill in the Value column for three rows: your_name_or_group, state, and body_name. The other rows are optional. Use plain words, such as "Example Neighbors Association" or the name of your state.
   You'll know it worked when the three Value cells are no longer empty. If the check-up later says a setting is empty, it's E03.

5. **CV-FR-01-5.** Add the check-up button. Choose Extensions, then [Apps Script](../glossary.md#apps-script) (Google's built-in way to add small programs to a sheet). A code editor opens in a new tab. Delete anything already in the editor. Open the kit's `free/checkup.gs` file, copy all of it, paste it into the editor, and click the disk icon to save. If it asks for a project name, type "Civic voice check-up".
   You'll know it worked when the editor shows the pasted code with no red marks. If you cannot find Extensions, you are probably in a different Google app (not Sheets).

6. **CV-FR-01-6.** Go back to your sheet tab and reload the page (press F5, or Command and R on a Mac). Wait a few seconds.
   You'll know it worked when a new menu called Help appears in the menu bar (Google has its own Help menu as well; yours holds "Run check-up"). If it does not appear, it's E04.

7. **CV-FR-01-7.** Click Help, then "Run check-up." The first time, Google asks for permission. Because you pasted the [script](../glossary.md#script) yourself, Google shows a warning that the app is not verified. Click Review permissions, pick your account, click Advanced, then "Go to Civic voice check-up (unsafe)," then Allow. (The script is limited to this one spreadsheet, and you can read all of it in the Apps Script tab first.) Run the check-up again if it did not open the result.
   You'll know it worked when a window shows a [support code](../glossary.md#support-code) ending with "OK," such as CV-FR-01-7-OK-v0.1.0 followed by three characters, and a report box that lists your tabs, whether headers match, and whether three settings are filled. If it shows a different code, find it in the [fixes table](../fixes.md). If the permission screen will not let you through, it's E05.

## What the check-up reads and never reads

It reads tab names, whether each header row matches, and whether three Settings cells are filled or empty. It never reads or reports what you typed in your rows or the words in your Settings cells, and it sends nothing anywhere. The report box shows exactly what you could share.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CV-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# Set Up Your Measurement Sheet (Free, Guide 1)

You will make one Google Sheet that holds your monthly website numbers, plus a Help menu that checks the sheet is set up correctly. It takes about 20 minutes. You need a Google account. Nothing here costs money.

1. **MM-FR-01-1.** Open Google Sheets (Google's free spreadsheet app) at sheets.google.com and sign in. Click the blank "+" to start a new spreadsheet. Name it by clicking "Untitled spreadsheet" at the top left and typing your organization's name followed by "measurement data".
   You'll know it worked when you see a blank grid with your title above it. If you get stuck in a sign-in loop or see the wrong account's picture at the top right, it's E04.

2. **MM-FR-01-2.** Add the five data tabs (a tab is one page of the sheet, shown along the bottom). Download these five files from the kit's `free/` folder: `monthly-traffic.csv`, `search-queries.csv`, `top-pages.csv`, `ai-referrals.csv` and `flagged-moves.csv`. A [CSV](../glossary.md#csv) is a plain table saved as text that any spreadsheet can open. For each file, choose File, then Import, then Upload, drag the file in, choose "Insert new sheet(s)" and click "Import data". Rename each new tab so it matches the file in plain words: "Monthly traffic", "Search queries", "Top pages", "AI referrals" and "Flagged moves". Spelling and capital letters must match exactly.
   You'll know it worked when you see five tabs along the bottom, each with a header row in row 1 and one example row under it. If a tab shows everything squashed into column A, it's E02. Delete the example rows when you add real data.

3. **MM-FR-01-3.** Add a sixth tab for your settings. Import `config-tab.csv` the same way and rename the tab "Config". Column A holds the setting names and column B holds your values. Replace the example values in column B: your organization's name, your [Search Console](../glossary.md#search-console) site name (you will find it in guide 2, so leave a note for now), your [GA4](../glossary.md#ga4) property number (guide 2), and the month you are reporting on (for example 2026-09). Never type a password or a key into this sheet.
   You'll know it worked when all four rows in column B are filled. If the check-up later says a cell is empty, it's E03.

4. **MM-FR-01-4.** Add the check-up. In the sheet, click Extensions, then [Apps Script](../glossary.md#apps-script). A new browser tab opens with a code editor. Delete anything in the box, open `checkup.gs` from the kit's `free/` folder in any text editor, copy all of it, paste it into the box, and click the disk icon to save. Name the project "Check-up" if asked. Click Run (the triangle) once. Google will ask you to allow the script; click "Review permissions", choose your account, and allow. If Google warns the app is not verified, click "Advanced" and then "Go to Check-up (unsafe)". That warning appears because you wrote the script yourself and have not submitted it to Google. It's safe here because the script only reads this one sheet, and you can read every line of it.
   You'll know it worked when the Run finishes with no red error. If you see "Authorization required" and it never lets you through, it's E11.

5. **MM-FR-01-5.** Go back to your sheet and reload the page (press the circular arrow in your browser). After a few seconds a "Help" menu appears next to "Extensions". Click Help, then "Run check-up". Two small windows appear. The first shows a support code. The second shows a plain-text report of tab names and whether headers match. Neither contains any numbers or words you typed into your data.
   You'll know it worked when the code ends in `E00`, for example `MM-FR-01-3-E00-v0.1.0-7KQ`. If the code ends in another number, look it up in [fixes.md](../fixes.md), fix that one thing, and run the check-up again. If no Help menu appears after a minute, it's E05.

Next: [Open your free data tools](MM-FR-02-open-your-free-data-tools.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

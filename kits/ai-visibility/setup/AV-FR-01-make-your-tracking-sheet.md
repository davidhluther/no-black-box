# AV-FR-01: Make Your Tracking Sheet

Time, about 30 minutes. You will build a Google Sheet with six tabs and add the [check-up](../glossary.md#check-up) button. You need a Google account. See [Keys and accounts](../../../guides/keys-and-accounts.md) if you need one.

The kit's files are in the `free/` folder. On GitHub, open a file and use the Download raw file button, or copy its text.

1. **AV-FR-01-1.** Open Google Sheets (Google's free spreadsheet app) at sheets.google.com and sign in. Click the plus button to start a blank spreadsheet. Name it "AI visibility check".
   You'll know it worked when you see an empty grid with a tab named Sheet1 at the bottom. If you get stuck in a sign-in loop, it's E24.

2. **AV-FR-01-2.** Import the first tab. Choose File, Import, Upload, and pick `Config.csv` from the `free/` folder. For "Import location" choose "Replace current sheet". Leave "Convert text to numbers, dates, and formulas" ticked. Click Import data. Double-click the tab name at the bottom and rename it exactly `Config` (capital C, no spaces).
   You'll know it worked when the tab holds a table with the columns key, value, and what to put here, and the first row is business_name. If the file is greyed out, or all the data lands in one column, it's E14.

3. **AV-FR-01-3.** Repeat step 2 five more times, but this time choose "Insert new sheet(s)" for the import location, so each file becomes its own tab. Use these exact tab names, with the same capital letters and no spaces. Import `Questions.csv` as `Questions`, `Runs.csv` as `Runs`, `Results.csv` as `Results`, `SameNames.csv` as `SameNames`, and `Summary.csv` as `Summary`.
   You'll know it worked when you see six tabs along the bottom, in any order, and on the Questions tab the last column shows readable questions, not text that starts with an equals sign. If a question cell shows `#NAME?` or `#REF!`, it's E04. If a cell shows the formula as plain text, it's E14. If a tab name is wrong, it's E01.

4. **AV-FR-01-4.** Add the check-up button. In the sheet menu choose Extensions, then [Apps Script](../glossary.md#apps-script). A new tab opens with a file called Code.gs. Select all the text in it and delete it. Open `checkup.gs` from the `free/` folder, copy all of it, and paste it into the empty file. Click the disk icon (Save). Name the [project](../glossary.md#project) "AI visibility check-up" if asked.
   You'll know it worked when the editor shows the pasted code with no red marks and no error banner. If Save is greyed out or a red banner appears, it's E12.

5. **AV-FR-01-5.** Go back to your spreadsheet tab and reload the page. After a few seconds a new menu called Help appears at the top. Click Help, then Run check-up. Google asks you to authorize the [script](../glossary.md#script). Click Review permissions, choose your account, and read the screen. The script only asks to see and change this one spreadsheet. If Google says the app is not verified, click Advanced and then "Go to AI visibility check-up (unsafe)". That wording appears for every script you write yourself. Click Allow. Run Help, Run check-up again.
   You'll know it worked when a box titled Check-up appears with a [support code](../glossary.md#support-code) and a list of what still needs filling in. Right now it will say E03 (setup cells still hold the example text), and that is expected. If no Help menu appears, it's E12. If Google keeps asking for permission, it's E13.

6. **AV-FR-01-6.** Delete the example rows. On the Runs tab and the Results tab, delete row 2 (right-click the row number, Delete row). On the SameNames tab, leave the examples for now. You will replace them in guide AV-FR-02.
   You'll know it worked when Runs and Results show only their heading row. If the Summary tab shows errors, it's E21.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# AS-FR-02: Make Your Google Sheet and Check-Up Button

Time about 25 minutes. You'll finish with a Google Sheet that holds your [voice sheet](../glossary.md#voice-sheet), a log of ad versions you test, your settings, and a Help menu with a check-up.

1. **AS-FR-02-1.** Open [Google Sheets](../glossary.md#google-sheets) at sheets.google.com and sign in. Click "Blank spreadsheet." Name it "Ad and Social."
   You'll know it worked when you see a blank grid with your title at the top left. If you see a sign-in loop, it's E01.
2. **AS-FR-02-2.** Rename the first tab (the tab is the label at the bottom) to Voice. Open [voice.csv](../free/voice.csv) in any program that opens plain text, such as Notepad or TextEdit, copy everything, click cell A1 and paste. If the cells don't split into columns, use Data, then "Split text to columns."
   You'll know it worked when row 1 reads Section, Entry, Notes. Missing tab is E10, wrong headings is E11. Now replace the example entries with your voice sheet from guide AS-FR-01.
3. **AS-FR-02-3.** Click the plus at the bottom left to add a tab named [Variants](../glossary.md#variant). Paste the contents of [variants.csv](../free/variants.csv) into A1.
   You'll know it worked when row 1 has ten headings starting with Date and ending with What we learned (E11 if not).
4. **AS-FR-02-4.** Add a tab named Config. Paste [config-cells.csv](../free/config-cells.csv) into A1.
   You'll know it worked when column A lists nine settings (E10 or E11 if not).
5. **AS-FR-02-5.** Fill in column B of Config for every row. Skip "Who approves posts" if it doesn't apply.
   You'll know it worked when no required row is blank (E12).
6. **AS-FR-02-6.** Open the menu Extensions, then Apps Script (Google's built-in place for small helper programs). Delete any text in the editor. Copy everything from [checkup.gs](../free/checkup.gs), paste it in, and click the disk icon to save. Name the [project](../glossary.md#project) "Ad and Social."
   You'll know it worked when the file saves with no red message. Close the Apps Script tab and reload your sheet.
7. **AS-FR-02-7.** After the sheet reloads, look for a new menu called Help next to the others. Click Help, then "Run check-up." Google asks for permission the first time. Click through, choose your account, and if it warns the app isn't verified, choose Advanced and continue. The script is plain text you just pasted, and it reads only this sheet.
   You'll know it worked when a box opens with a support code and a short report. If there's no Help menu, it's E09. If Google's permission screen confuses you, it's E13.
8. **AS-FR-02-8.** Read the report. A code with "-OK-" in the middle (for example AS-FR-02-7-OK-v0.1.0 followed by three letters) means every tab, heading and setting is in place. Anything else, look up its problem code in [fixes](../fixes.md).
   You'll know it worked when the report shows "found, headings match" for all three tabs.

> **How to get help.** Write down the step ID where you got stuck (it looks like AS-FR-02-7). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

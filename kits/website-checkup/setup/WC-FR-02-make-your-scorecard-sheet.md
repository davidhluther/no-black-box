# WC-FR-02: Make Your Scorecard Sheet

You will build a [Google Sheet](../glossary.md#google-sheet) with seven tabs, add a "Kit help" menu that checks the sheet for you, and fill in your business details. About 30 minutes.

If you get stuck, the check-up button in your sheet prints a [support code](../glossary.md#support-code), a short code that tells a helper which step failed. The box at the bottom says where to send it.

1. **WC-FR-02-1.** Download the template files. Open the kit's `free` folder on GitHub. For each file whose name ends in `-tab.csv`, click its name, then click the download button (an arrow pointing down, at the top right of the file view). Put all seven in one folder on your computer. A [CSV](../glossary.md#csv) file is a plain table that spreadsheets can open.
   You'll know it worked when your folder has seven files: config, [scorecard](../glossary.md#scorecard), summary, baseline16, pages, competitors, and monthly. If a download opens as text in the browser instead, use "Save page as" and keep the `.csv` ending, and see E07 if the sheet rejects it later.

2. **WC-FR-02-2.** Open sheets.google.com and start a blank sheet. Name it "Website check-up" at the top left. Then add tabs along the bottom (the plus sign) until you have seven, and name them exactly as follows, with capital letters as shown: Config, Scorecard, Summary, Baseline16, Pages, Competitors, Monthly. Right-click a tab and choose Rename.
   You'll know it worked when the seven names appear along the bottom. A misspelled tab name is the most common problem, and it's E07.

3. **WC-FR-02-3.** Fill each tab from its file. Click the tab, then File, Import, Upload, and choose the matching file (Config tab with `config-tab.csv`, and so on). Under "Import location", choose "Replace current sheet". Leave "Convert text to numbers, dates, and formulas" ticked. Do this seven times. Afterward, select column D on the Summary tab and choose Format, Number, Percent.
   You'll know it worked when each tab has a heading row, and the Summary tab shows seven sections with zeros or blanks. If a tab shows the wrong table, you used the wrong file for it, and it's E07. If the Summary tab shows `#REF!` or `#DIV/0!`, it's E14.

4. **WC-FR-02-4.** Open the Config tab and fill in the Value column. Write the business name exactly as it appears on your Google listing. Write your site address starting with [https](../glossary.md#https)://. Choose a business type (for example restaurant, home services, dental, retail, professional services). Add your town or area, and up to five competitors. Leave `version` as FR.
   You'll know it worked when the first four settings are filled. Anything left blank is E08, and an address that doesn't start with https:// is E21.

5. **WC-FR-02-5.** Add the check-up button. In the sheet, choose Extensions, then [Apps Script](../glossary.md#apps-script). This opens [Apps Script](../glossary.md#apps-script), Google's free tool for adding small programs to a sheet. Delete the sample code in the editor, open `checkup.gs` from the kit's `free` folder, copy everything, paste it into the editor, and click the disk icon to save. Name the [project](../glossary.md#project) "Website check-up".
   You'll know it worked when the editor shows the pasted code and no red error marks. If you see an error saying a name is not defined, you pasted only part of the file, and it's E10.

6. **WC-FR-02-6.** Go back to the sheet and reload the page. After a few seconds a "Kit help" menu appears next to the usual menus. Click Kit help, then Run check-up. The first time, Google asks you to allow the script. Choose your account, click "Advanced", then "Go to Website check-up (unsafe)", then tick **Select all** and click **Continue**. That warning shows for every personal script. This script reads only this sheet and sends nothing out.
   You'll know it worked when a window opens with a [support code](../glossary.md#support-code) and says "All checks passed". If the Kit help menu never appears, it's E10. If Google blocks the allow screen, it's E09. Any other message lists a code to look up in the fixes table.

> **How to get help.** Write down the step ID where you got stuck (it looks like WC-FR-02-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

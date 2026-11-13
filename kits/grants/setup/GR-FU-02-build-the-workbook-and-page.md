# GR-FU-02: Build the Workbook and the Page

**What you'll have.** An Excel workbook with live formulas (calculations typed into cells), a phone-friendly web page of the same tables, and a link on every row to the funder's page, your dossier (a short file of what you have learned about one funder) or a tax-filing search. **Time.** About 30 minutes. **You need.** A finished [GR-FU-01](GR-FU-01-install-the-skills-and-engine.md).

If you get stuck, the check-up (a button or command that tests your setup) prints a support code (a short code that tells a helper which step failed and holds none of your information). The last box on this page says how to use it.

1. **GR-FU-02-1.** Open a terminal (the screen where you type instructions), move into the engine folder, and add the links. Replace the config path with yours.

   ```bash
   cd kits/grants/skills/grants-pipeline
   python3 engine/links.py --config ~/Documents/my-org-grants/my-org.json
   ```

   You'll know it worked when it prints a line for each CSV, such as "pipeline-rows.csv: 12 rows, 12 funder links". If it stops with "list index out of range", a CSV has no data rows, which is E28.

2. **GR-FU-02-2.** Build the workbook.

   ```bash
   python3 engine/build_xlsx.py --config ~/Documents/my-org-grants/my-org.json
   ```

   You'll know it worked when it prints the path of a new .xlsx file in your data folder. If it says a name appears in the output, one of your excluded names is in your data, which is E29.

3. **GR-FU-02-3.** Build the page.

   ```bash
   python3 engine/build_page.py --config ~/Documents/my-org-grants/my-org.json
   ```

   You'll know it worked when it prints the path of a new .html file. Open it in a browser. If a number in the request column made it stop with "could not convert string to float", remove dollar signs and commas from that column, which is E28.

4. **GR-FU-02-4.** Look at the page on a phone-width window and on a wide one. Narrow your browser window to about the width of a phone, scroll through every section, and check that the stage filters work.
   You'll know it worked when the tables scroll sideways inside their boxes and the filter buttons show only matching rows.

5. **GR-FU-02-5.** Put the workbook in Google Drive (Google's online file storage) and open it with Google Sheets (Google's free spreadsheet app), then confirm the formulas and links survived. Check the Dashboard tab and click two funder links.
   You'll know it worked when Tier, Fit and dollars-per-hour columns show numbers and clicked links open the right pages. The organization's own data folder stays the one master copy; update the Drive copy by re-uploading under the same name.

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

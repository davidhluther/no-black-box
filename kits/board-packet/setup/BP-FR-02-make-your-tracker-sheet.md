# Make Your Tracker Sheet

This guide takes about 20 minutes. You will end with one Google Sheet (Google's free spreadsheet) with four tabs, filled in with your organization's details. A tab is one of the pages along the bottom of a spreadsheet. This sheet is the [tracker sheet](../glossary.md#tracker-sheet). It lists your reports and people, holds your settings, and later carries the kit's [check-up](../glossary.md#check-up).

Each step has an ID. If you get stuck, note the ID. Once the check-up from guide BP-FR-04 is installed (the full version uses a command named `doctor` instead), it prints a [support code](../glossary.md#support-code) you can send along with the ID.

The tabs come from four small files in the kit. Each is a CSV file (plain text with commas between the columns, which every spreadsheet program can open).

**Getting the files.** You need these four files from the kit. If you have not yet downloaded the kit, follow [get the kit files](../../../guides/get-the-files.md). It shows how to download everything from https://github.com/davidhluther/no-black-box and unzip it, or how to grab one file by opening it on GitHub and clicking the **Download raw file** button (the icon with a down arrow, at the top right of the file). Either way, the files end up in your Downloads folder.

- [Settings.csv](../free/templates/Settings.csv)
- [Reports.csv](../free/templates/Reports.csv)
- [Contacts.csv](../free/templates/Contacts.csv)
- [Month.csv](../free/templates/Month.csv)

1. **BP-FR-02-1.** Open Google Sheets at sheets.google.com and sign in. Click **Blank spreadsheet**. Click the words "Untitled spreadsheet" at the top left and type `Board Packet Tracker`.
   You'll know it worked when you see an empty grid titled Board Packet Tracker. If you land in a sign-in loop, it's E26.

2. **BP-FR-02-2.** Make the Settings tab. Click **File**, then **Import**, then **Upload**, and drag in `Settings.csv` (or click **Browse** and choose it from Downloads). Under **Import location** choose **Insert new sheet(s)**. Leave **Separator type** on "Detect automatically" and leave **Convert text to numbers, dates, and formulas** ticked. Click **Import data**.
   You'll know it worked when a new tab named Settings appears at the bottom, with the headings Setting, Value, and Notes in the first row. If the tab has another name, double-click the tab name and type `Settings`. If every row sits in one column, the import used the wrong separator. Redo it and choose **Comma** (E05).

3. **BP-FR-02-3.** Do the same with `Reports.csv`. The new tab must be named `Reports`, and its first row must read Order, Report, Owner, Role in packet, In combined packet, Filename keyword, Active, Received this month, Link or note.
   You'll know it worked when you can see eight rows of example reports. If a heading is slightly different, retype it exactly (E06).

4. **BP-FR-02-4.** Do the same with `Contacts.csv`. Name the tab `Contacts`. Its headings are Name, Email, Group, Role, Active.
   You'll know it worked when you see five example people. If not, it's E07.

5. **BP-FR-02-5.** Do the same with `Month.csv`. Name the tab `Month`. Its headings are Item, Value, Notes.
   You'll know it worked when you see rows such as meeting_date and month_folder_name, and the last row, missing_reports_auto, shows either nothing or a list of report names. If that cell shows an error, re-import with **Convert text to numbers, dates, and formulas** ticked, and check that the Reports tab is named exactly `Reports` (E08).
   Finally, right-click the empty tab called "Sheet1" at the bottom, choose **Delete**, and confirm.

6. **BP-FR-02-6.** Fill in the Settings tab. Replace the example text in the **Value** column (column B) with your own. The ten rows the check-up requires are org_name, board_name, meeting_time, meeting_location, chair_name, secretary_name, sender_name, root_folder_name, transcripts_folder_name, and email_subject_pattern. Type the folder names exactly as you made them in guide BP-FR-01. Leave the square brackets in email_subject_pattern alone, because the kit fills those in. Fill in the rest if you want them, and clear any example you do not need.
   You'll know it worked when no required row is blank. If one is, the check-up names it (E09).

7. **BP-FR-02-7.** Fill in the Contacts tab. Replace the examples with your real people, one per row. Under **Group** type To for the chair, Cc for the staff who write reports, and [Bcc](../glossary.md#bcc) for everyone else on the board. Type Yes under **Active** for each person who should get the email. Use the address you want the email to go to.
   You'll know it worked when there is at least one person in the To group and every email address has an @ sign and a dot after it. Why Bcc: it hides addresses from each other (the full name is blind carbon copy). If the chair is the only To person, nobody else's address is shown. If a row looks wrong, it's E13 or E14.

8. **BP-FR-02-8.** Fit the Reports tab to your own agenda. Each row is one report you expect. Change the **Report** and **Owner** names. Set **Role in packet** to agenda, report, or minutes (the minutes row must stay). Set **In combined packet** to Yes for anything that goes in the single combined PDF and No for anything you share by its own link, such as financials. Set the **Filename keyword** to one word that will appear in that report's file name. Delete rows you do not use, and add rows if your agenda names more. Keep one row with **Role in packet** set to minutes, and give each row its own **Order** number.
   You'll know it worked when each row has an order number, the minutes row is last, and at least one row says Yes under Active. If not, it's E10, E11, or E12.

**Where you are now.** Your folders and sheet exist and are filled in. Guide BP-FR-04 adds the check-up that tests all this. Guide BP-FR-03 puts the checklist, email template, and prompts where you can reach them. Do them in any order.

> **How to get help.** Write down the step ID where you got stuck (it looks like BP-FR-02-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

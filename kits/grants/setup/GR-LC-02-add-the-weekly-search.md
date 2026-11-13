# GR-LC-02: Add the Weekly Search

**What you'll have.** A Sweep (a search that runs by itself every week) tab in your tracker that fills itself every week with new federal funding notices from Grants.gov (the US government's public list of grant opportunities), scored by simple word rules, plus a SweepLog tab and an email if a run fails or a week is missed. **Time.** About 30 minutes. **You need.** The tracker, the file sweep.gs from the low-cost folder of the kit, and a working check-up ([GR-FR-02](GR-FR-02-add-the-check-up-button.md)).

If you get stuck, the check-up (a button or command that tests your setup) prints a support code (a short code that tells a helper which step failed and holds none of your information). The last box on this page says how to use it.

The weekly search is a script (a small program) that runs inside your spreadsheet on a schedule, called a trigger (an instruction that runs a program on a schedule). It asks Grants.gov a public question, writes the answers into your sheet, and never contacts a funder. The only thing that leaves your sheet is your search words, which go to Grants.gov. Federal grants fit some organizations and not others, so judge each row on its own eligibility rules.

1. **GR-LC-02-1.** In your tracker, click Extensions, then Apps Script (a free Google tool that runs small programs inside a spreadsheet). In the left list, click the plus sign beside Files and choose Script. Name the new file sweep.
   You'll know it worked when a second file named sweep appears in the left list. If you see no Apps Script, it's E10.

2. **GR-LC-02-2.** Delete the starter text in the new file. Open sweep.gs from the low-cost folder in Notepad or TextEdit, copy everything, paste it in, and save.
   You'll know it worked when the file starts with "Grants kit weekly sweep".

3. **GR-LC-02-3.** Edit the search words. Near the top, change the words between the quotation marks in keywords, positiveWords, negativeWords, goodAgencies and badAgencies to fit your work. Keep the quotation marks, commas and square brackets exactly as they are. Save.
   You'll know it worked when the file still saves without red marks. Words that match your work (such as "food pantry") belong in keywords. If you break the punctuation, undo with Ctrl+Z (Command+Z).

4. **GR-LC-02-4.** Run it once by hand. In the toolbar, pick runWeeklySweep from the function list and click Run. Google asks permission to connect to an outside service and to send email as you. Follow the same screens as in GR-FR-02-6 and allow them.
   You'll know it worked when two new tabs, Sweep and SweepLog, appear in your tracker. If the log says "failed", it's E21. If a permission screen has no Advanced link, it's E11.

5. **GR-LC-02-5.** Open the Sweep tab. Each row is one notice, with its agency, title, closing date, a link, a score and a tier.
   You'll know it worked when at least a few rows appear. If it's empty but the log says "done", your search words may be too narrow, which is E22.

6. **GR-LC-02-6.** Set the schedule. Pick installSweepTriggers from the function list and click Run. Click the clock icon in the left bar to see the Triggers list.
   You'll know it worked when the Triggers list shows runWeeklySweep (weekly) and checkSweepFreshness (daily). If the list is empty, it's E23.

7. **GR-LC-02-7.** Test the alarm. In the sweep file, change maxDaysWithoutSuccess from 8 to 0, save, pick checkSweepFreshness and click Run. Then change it back to 8 and save.
   You'll know it worked when an email arrives at the address in Settings ("Grants contact email"). If it doesn't, check your spam folder, then E24.

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-LC-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

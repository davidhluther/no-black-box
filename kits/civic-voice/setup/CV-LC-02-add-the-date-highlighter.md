# CV-LC-02: Add the Date Highlighter

Low-cost version, guide 2 (optional). You will add a small [Apps Script](../glossary.md#apps-script) to your tracker that colors due dates: light red when a date has passed and light yellow when it falls in the next three days. It sends no email and changes only the colors of those date cells. Allow 10 minutes. You need the tracker from [CV-FR-01](CV-FR-01-make-your-tracker.md).

1. **CV-LC-02-1.** In your tracker, choose Extensions, then Apps [Script](../glossary.md#script). In the left list, click the plus next to Files, choose Script, and name it "deadlines."
   You'll know it worked when you see a new empty file called deadlines in the list.

2. **CV-LC-02-2.** Open `free/deadlines.gs` from the kit, copy all of it, paste it into the empty file, and click the disk icon to save.
   You'll know it worked when the file shows the code with no red marks. You should keep `checkup.gs` in the same project, because its menu code adds the new menu.

3. **CV-LC-02-3.** Go back to your sheet and reload the page.
   You'll know it worked when a menu called "Civic voice" appears. If it does not, it's E22.

4. **CV-LC-02-4.** Test it with a made-up row. On the Records requests tab, add a row with a Response due date of yesterday and a Status of "Sent." Click Civic voice, then "Highlight due dates." The first time, Google asks for permission as in [CV-FR-01-7](CV-FR-01-make-your-tracker.md).
   You'll know it worked when the date cell turns light red and a small note says one cell was highlighted. If nothing changes, make sure the headings still read "Response due" and "Status" exactly, and see E22. Then delete the test row.

5. **CV-LC-02-5.** Use it each week. Open the tracker, click Civic voice, then "Highlight due dates." Use "Clear highlights" to remove the colors.
   You'll know it worked when overdue dates are red and near ones are yellow. Rows with a Status such as Received, Closed, Withdrawn, or Delivered are skipped.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CV-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

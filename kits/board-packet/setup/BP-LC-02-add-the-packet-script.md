# Add the Packet Script

This guide takes about 15 minutes. It assumes guide BP-FR-04 is finished, so your [tracker sheet](../glossary.md#tracker-sheet) already has the [check-up](../glossary.md#check-up) installed. You will add a second file of [Apps Script](../glossary.md#apps-script) (Google's free tool for small programs inside Sheets and Drive) that adds three menu items to your sheet.

Each step has an ID. If you get stuck, note the ID. Once the [check-up](../glossary.md#check-up) from guide BP-FR-04 is installed (the full version uses a command named `doctor` instead), it prints a [support code](../glossary.md#support-code) you can send along with the ID.

- Make this month's folder.
- Make numbered PDF copies of the reports, in packet order.
- Write the board email as a Gmail draft.

**What it cannot do.** Apps Script has no built-in way to merge PDFs into one file. This script makes the numbered copies and a list of the order. Guide BP-LC-03 shows the simplest free way to do the merge. It also only converts Google Docs, Sheets, and Slides, plus files that are already PDFs. A Word or Excel file in the folder is listed as "not converted" and needs one extra step, described in E22.

**What it promises.** It never sends email, it only makes a draft. It never deletes your files, except its own earlier PDF copies in the folder it creates. It never changes who can open anything. Step BP-LC-02-7 shows you how to check the first promise yourself.

1. **BP-LC-02-1.** Open your Board Packet Tracker sheet. Click **Extensions**, then **Apps Script**.
   You'll know it worked when the editor opens with your existing `Code.gs` file in the left list. If Extensions has no Apps Script item, it's E28.

2. **BP-LC-02-2.** Click the **+** beside **Files** at the top left, choose **Script**, type `packet`, and press Enter.
   You'll know it worked when a new empty file called `packet.gs` appears under Files. If it does not, click **+** again.

3. **BP-LC-02-3.** Open [packet.gs](../low-cost/packet.gs) on GitHub, click **Copy raw file**, click inside the new empty file, select everything, and paste. Click the disk icon to save.
   You'll know it worked when the file shows lines starting with `/**` and `Board packet helper`, and there is no red error mark. If a red mark shows, select all, delete, and paste again.

4. **BP-LC-02-4.** Go to the **Settings** tab of your sheet. Make sure the row `combined_packet_filename` has a value, such as `board-packet-combined.pdf`.
   You'll know it worked when the cell is not blank. If it is blank, the check-up reports E20.

5. **BP-LC-02-5.** Go back to the sheet and reload the page. Wait about 10 seconds.
   You'll know it worked when a new menu called **Board packet** appears, next to the **Help** menu. If only **Help** shows, it's E29.

6. **BP-LC-02-6.** Click **Board packet**, then **1. Make this month's folder**. Google asks for permission.
   Click **Review permissions**, pick your account, and click **Advanced**, then **Go to Board packet kit (unsafe)**, then **Allow**. Google words one of the permissions as "Read, compose, send, and permanently delete all your email from Gmail". That is Google's single, broad Gmail permission, and it is the only one Apps Script offers for creating drafts. This script uses only the part that creates a draft. Step BP-LC-02-7 shows you how to confirm that.
   You'll know it worked when, after you allow it, a box tells you this month's folder is ready, with a link. If you get an error beginning E15, E16, or E20, the Month tab or a folder name does not match your Drive (E15, E16, E20).

7. **BP-LC-02-7.** Check the "never sends" promise yourself. In the Apps Script editor, click inside `packet.gs`, press Ctrl+F (Command+F on a Mac), and search for `send(`. Then search for `MailApp`.
   You'll know it worked when both searches find nothing. The one Gmail call in the file is `createDraft`. If either search finds something, stop and send the support code (see the box below), because the file has been changed from the kit's version.

8. **BP-LC-02-8.** Run **Help**, then **Run check-up** once more.
   You'll know it worked when the support code starts with `BP-FR-00-0`. If not, fix the problems listed and rerun.

> **How to get help.** Write down the step ID where you got stuck (it looks like BP-LC-02-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

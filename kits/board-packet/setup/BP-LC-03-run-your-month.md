# Run Your Month

This guide takes about 30 minutes each month once you know it. It assumes guides BP-LC-01 and BP-LC-02 are finished.

Each step has an ID. If you get stuck, note the ID. Once the [check-up](../glossary.md#check-up) from guide BP-FR-04 is installed (the full version uses a command named `doctor` instead), it prints a [support code](../glossary.md#support-code) you can send along with the ID.

1. **BP-LC-03-1.** Open the **Month** tab. Fill in `meeting_date`, `month_folder_name`, and `prior_meeting_date`. Clear the **Received this month** column on the **Reports** tab. Click **Board packet**, then **1. Make this month's folder**.
   You'll know it worked when a box tells you the folder is ready. If it says E21, the name in `month_folder_name` does not match any folder you made. Fix the name in the sheet, or rename the folder.

2. **BP-LC-03-2.** Put each report in the month folder, with its keyword in the file name. Mark each as Yes under **Received this month**.
   You'll know it worked when the `missing_reports_auto` cell on the Month tab lists only the reports still missing.

3. **BP-LC-03-3.** Write last meeting's minutes in your [AI Project](../glossary.md#ai-project). Open your `Board packet` project, paste the [transcript](../glossary.md#transcript) in parts, and ask for notes, then minutes, then a check against the transcript. The project already holds the style guide. You still give it the attendance list each time.
   You'll know it worked when you have minutes where every motion is recorded and every unclear point is in square brackets. A person must read them before the board does (E42).

4. **BP-LC-03-4.** Make the minutes a Google Doc, and put it in **this** month's folder. These minutes are for last month's meeting, and this month's meeting is where the board approves them. Make the [digest](../glossary.md#digest) in the same chat and save it in the private transcripts folder.
   You'll know it worked when the minutes Doc is in this month's folder, saved as a real Doc (not a shortcut, which the script cannot convert), and the digest sits next to the transcript.

5. **BP-LC-03-5.** Click **Board packet**, then **2. Make PDF copies**. A box says how many copies were made and which files could not be converted.
   You'll know it worked when a folder called `PDF copies` appears in the month folder holding numbered files such as `01 - Agenda.pdf` and `02 - Director's report.pdf`, plus a tab called **Last run** listing the order. If a file was not converted, open it in Drive and choose **File**, **Save as Google Docs** (or Sheets), then run this step again (E22). If the box says no files were found, it's E23.

6. **BP-LC-03-6.** Merge the numbered PDFs into one. [Apps Script](../glossary.md#apps-script) cannot do this itself, so use the simplest free route for your computer.
   - On a Mac, open the `PDF copies` folder in Finder and select the numbered files that are in the packet (not those starting "Separate"). Hold Control, click one, choose **Quick Actions**, then **Create PDF**. Apple documents this on its support site. Check the page order, because Apple says the pages follow the order you selected the files in.
   - On Windows or any computer, use PDFsam Basic (pdfsam.org, free, open source). It runs on your own computer, so your board papers are not uploaded anywhere. Choose **Merge**, add the files in order, and run it.
   - Avoid free merge websites for board papers. They require you to upload the files to a stranger's server.
   Name the result exactly as in your `combined_packet_filename` setting and drag it into the month folder.
   You'll know it worked when one PDF opens with the agenda first and the prior minutes last. A community-written Apps Script library that merges PDFs does exist, and it can be added to this project. The kit has not tested it, so it is not part of the guide.

7. **BP-LC-03-7.** Click **Board packet**, then **3. Make the email draft**. A box tells you the draft is waiting and lists anything to check.
   You'll know it worked when you open Gmail, click **Drafts**, and find the email with the right subject, the To, Cc, and [Bcc](../glossary.md#bcc) people, and a link for the combined packet and for the files folder. The script never sends it. If the box says E24, the Contacts tab has no active person in the To group. If it says E25, the combined packet file was not found. Check the name in your settings against the file in the month folder.

8. **BP-LC-03-8.** Open every link in a private browser window. Ask your reviewer to read the draft. Add anything the script could not know, such as a link for a one-time item. When the reviewer approves it, send it from Gmail.
   You'll know it worked when every link opens the way you set it up in BP-FR-01-5: after you sign in with a board member's address if you kept Restricted, or with no sign-in if you chose Anyone with the link. If one does not, fix the sharing in Drive first (E27). If the draft is not in Drafts, see E44.

> **How to get help.** Write down the step ID where you got stuck (it looks like BP-LC-03-5). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# Run Your First Month

This guide takes about 45 minutes the first time and less after that. It walks the monthly cycle once, using the free version. It is separate from the four setup guides.

Each step has an ID. If you get stuck, note the ID. Once the [check-up](../glossary.md#check-up) from guide BP-FR-04 is installed (the full version uses a command named `doctor` instead), it prints a [support code](../glossary.md#support-code) you can send along with the ID.

You will use a [transcript](../glossary.md#transcript) (a written record of what was said at the meeting) and an [AI model](../glossary.md#ai-model) (a program that reads and writes text, such as ChatGPT, Claude, or Gemini). You need a free account with one of them. Practice first with [sample-transcript.md](../free/sample-transcript.md), an invented meeting, so you can see what good output looks like before you use real material.

1. **BP-FR-05-1.** Open the **Month** tab of your [tracker sheet](../glossary.md#tracker-sheet). Fill in `meeting_date` (mm/dd/yyyy), `month_folder_name` (for example `2027 January`), and `prior_meeting_date`. Open the **Reports** tab and clear the column **Received this month**.
   You'll know it worked when the Month tab shows this month's dates. If missing_reports_auto shows an error, check the Reports tab is named exactly `Reports` (E08).

2. **BP-FR-05-2.** Get the reports in. Ask each owner to put their file in this month's folder inside `Board Secretary Files`, with its keyword in the file name, or email it to you and put it there yourself. As each arrives, type Yes under **Received this month**.
   You'll know it worked when the Month tab's missing_reports_auto cell lists only the reports that have not come. That sentence goes into your email.

3. **BP-FR-05-3.** Get last meeting's transcript. You have three free routes, and the right one depends on your meeting tools.
   - Google Meet. Google lists transcripts for Business Standard and higher editions of Workspace (checked 11/13/2026). The free Workspace for Nonprofits edition lists no recording, so check what your account offers.
   - Zoom. A free account records to your own computer. Zoom's automatic transcript comes from a cloud recording, which needs a paid plan. Sources disagree on whether a local recording carries a transcript, so open your own account's settings and check.
   - Your own typed notes. This always works. Use [Prompt](../glossary.md#prompt) 6 in [prompts.md](../free/prompts.md) instead of Prompts 1 and 2.
   You'll know it worked when you have either a text transcript or your typed notes. Put a copy of the transcript in `Board Meeting Transcripts (private)`, in the folder for board meetings. Never put it in a month folder.

4. **BP-FR-05-4.** Write the minutes. Open an AI model's chat page. Split the transcript into parts of about 10 pages, or as much as the AI accepts in one paste, and paste Prompt 1 from [prompts.md](../free/prompts.md) followed by each part in turn. Then paste Prompt 2, filling in the attendance and your style guide.
   You'll know it worked when the model gives you minutes with your headings and every motion recorded. If the model says the text is too long or stops partway, use smaller parts (E43).

5. **BP-FR-05-5.** Check the minutes. Open a new chat and run Prompt 3, which compares the draft with the transcript. Fix everything it flags, and read the whole draft yourself.
   You'll know it worked when the lists of mismatched names, numbers, and motions come back empty or you have fixed each one. A model can invent a name or a vote. Only you can catch that (E42).

6. **BP-FR-05-6.** Make the minutes a Google Doc. Paste the final text into a new Doc, then use **File**, **Download**, **PDF** if your board wants a PDF. Put the Doc in **this** month's folder. These minutes are for last month's meeting, and this month's meeting is where the board approves them. That is why minutes always land in the month after the meeting they record.
   You'll know it worked when the minutes sit in this month's folder beside the reports.

7. **BP-FR-05-7.** Write the [digest](../glossary.md#digest). Run Prompt 4 in the same chat that has the transcript and finished minutes. Save the result as a Google Doc in `Board Meeting Transcripts (private)`, named with the meeting date.
   You'll know it worked when the digest has five headings, and the "In the transcript but not in the minutes" list is not empty. If it is empty, check that the model had both documents.

8. **BP-FR-05-8.** Combine the packet. Your free route is by hand. In the month folder, open each report. For each Google Doc or Sheet, choose **File**, **Download**, **PDF**. On a Mac, select the downloaded PDFs in Finder in agenda order, hold Control, click one, and choose **Quick Actions**, **Create PDF** (Apple describes this on its support site). On Windows, use a free merge program that runs on your own computer, such as PDFsam Basic at pdfsam.org. Save the result in the month folder as `board-packet-combined.pdf`.
   You'll know it worked when one PDF opens with the agenda first and last month's minutes last. Why not automatic? [Apps Script](../glossary.md#apps-script) has no built-in way to merge PDFs. The low-cost version lines up the PDFs for you, and the full version merges them in one step.

9. **BP-FR-05-9.** Write the email. Open your email template Doc. Use Prompt 5 in [prompts.md](../free/prompts.md), or fill the brackets in yourself. Create a new message in Gmail, paste it in, add the To, Cc, and [Bcc](../glossary.md#bcc) addresses from your Contacts tab, and add each link by selecting its words and clicking the link icon. Leave it as a draft.
   You'll know it worked when the message sits in Gmail's **Drafts** with every link in place.

10. **BP-FR-05-10.** Check, review, and send. Open every link in a private browser window. Ask your reviewer to read the draft. When they approve it, send it.
    You'll know it worked when every link opens the way you set it up in BP-FR-01-5: after you sign in with a board member's address if you kept Restricted, or with no sign-in if you chose Anyone with the link. If one does not, fix the sharing in Drive first (E27).

> **How to get help.** Write down the step ID where you got stuck (it looks like BP-FR-05-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

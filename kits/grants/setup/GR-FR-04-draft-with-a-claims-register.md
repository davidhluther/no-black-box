# GR-FR-04: Draft With a Claims Register

**What you'll have.** A filled claims register (your table of facts about the organization, each with its source), and a draft in which a checker has confirmed every number matches a verified claim. **Time.** About an hour the first time, then 30 minutes a draft. **You need.** The tracker, your annual report, audit and IRS letter, the [paste-in prompts (messages you paste into ChatGPT, Claude or Gemini)](../free/prompts.md), the file draft-check.gs from the free folder and the [before you submit checklist](../free/docs/before-you-submit-checklist.md).

If you get stuck, the check-up (a button or command that tests your setup) prints a support code (a short code that tells a helper which step failed and holds none of your information). The last box on this page says how to use it.

Drafts are drafts. A person reviews and sends them. Nothing in this guide sends anything to a funder.

1. **GR-FR-04-1.** Gather your own documents: the last annual report, the last audit or financial statements, your IRS determination letter and any board-approved program descriptions.
   You'll know it worked when the documents are open on your desk or in a folder. If you lack an audit, use the treasurer's year-end report and mark claims from it "external-verified" only if a public page repeats them.

2. **GR-FR-04-2.** Fill the Claims tab. Paste text from one document into [Prompt](../glossary.md#prompt) 4 and paste the rows it returns into the Claims tab, one claim per row. Check each row against the document yourself. Put the document name and page in Source. Use the Status words source-verified (you read it in your own document), external-verified (you read it on a named web page on a stated date), unverified, conflict or do-not-use. Keep one number per row, written as it appears in drafts (35 for 35 percent).
   You'll know it worked when every claim you will use has a Source and a status. The check-up shows E13 if a verified claim has no Source.

3. **GR-FR-04-3.** Install the draft checker. Open Extensions, then Apps Script (a free Google tool that runs small programs inside a spreadsheet). In the left list, click the plus sign beside Files and choose Script. Name it draft-check. Delete the starter text, open draft-check.gs from the free folder in Notepad or TextEdit, copy everything, paste it in, and save. Close the tab and reload your tracker.
   You'll know it worked when the Kit help menu now lists "Check draft numbers" below "Run check-up". If it doesn't, it's E15. Google may ask for permission again, as in GR-FR-02-6.

4. **GR-FR-04-4.** Write a first draft. Use Prompt 5 in a free AI model (a program that reads and writes text when you message it, such as ChatGPT, Claude or Gemini), pasting in your dossier (a short file of what you have learned about one funder), your program and only the rows of your claims register that are usable. The prompt makes the AI model tag each fact with its claim ID and leave a [CONFIRM] note where a fact is missing.
   You'll know it worked when the draft has claim IDs in square brackets and a [CONFIRM] note wherever it needed a fact you had not given.

5. **GR-FR-04-5.** Check the numbers. On the DraftCheck tab, paste the draft into cell B1. In B2, type the numbers that are not claims, such as the ask amount and deadlines, separated by commas. Click Kit help, then "Check draft numbers".
   You'll know it worked when rows appear from row 6 down listing each number and a verdict. "NOT IN REGISTER" means you must either fix the draft or add a verified claim with a source. If nothing appears, or the sheet says it is empty, it's E16.

6. **GR-FR-04-6.** Get a fresh pair of eyes. Open a brand-new chat and paste Prompt 6 with the funder's guidelines and your draft, then walk through the before you submit checklist with a second person.
   You'll know it worked when each problem found is either fixed or written in the cover note.

7. **GR-FR-04-7.** Get approval and send. Show the draft and checklist to the person the board named in [tier approvals](../free/docs/tier-approvals.md). That person, not the AI model, sends it, and you update the Pipeline row (Status, Submitted, Deadline, Next step).
   You'll know it worked when the row shows Submitted with today's date, and the Dashboard's "Open asks" goes up by one.

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

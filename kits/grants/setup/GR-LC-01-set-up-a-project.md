# GR-LC-01: Set Up a Project With Your Kit Documents

**What you'll have.** A saved workspace in your AI plan that already knows your tracker's rules, your claims register (a table of every fact you may state about your organization, each with its source) and the kit's method, so you stop pasting the same background into every chat. **Time.** About 30 minutes. **You need.** The free version working ([GR-FR-01](GR-FR-01-make-your-tracker.md) and [GR-FR-02](GR-FR-02-add-the-check-up-button.md)) and one paid AI plan of about $20 a month, from ChatGPT, Claude or Gemini. See the [shopping list](../shopping-list.md) for current prices.

If you get stuck, the check-up (a button or command that tests your setup) prints a support code (a short code that tells a helper which step failed and holds none of your information). The last box on this page says how to use it.

A Project is a saved workspace in ChatGPT or Claude that keeps a set of instructions and files, called knowledge files (a document the AI model (a program that reads and writes text when you message it, such as ChatGPT, Claude or Gemini) can read when it answers), which the AI model reads whenever you chat inside it. Choose one product. You don't need two.

1. **GR-LC-01-1.** Sign up for one plan. Pick ChatGPT, Claude or Gemini, and follow the vendor's own sign-up page. Use the same sign-in your organization will keep. Sign-up help is in the [keys and accounts guide](../../../guides/keys-and-accounts.md).
   You'll know it worked when you can open the product and see a "Projects" or similar option in its menu. If your plan has no Projects feature, use a pinned chat and paste the instructions at the top of each new conversation.

2. **GR-LC-01-2.** Create a Project named Grants kit.
   You'll know it worked when an empty Project with that name appears in your list.

3. **GR-LC-01-3.** Paste the instructions. Open chatgpt/instructions.md from the kit, copy everything, and paste it into the Project's instructions box. Save.
   You'll know it worked when the instructions box shows the text beginning "You are a grants and giving helper". If the box refuses it as too long, it's E20.

4. **GR-LC-01-4.** Upload the knowledge files. Follow the numbered list in chatgpt/knowledge-files.md. For items 15 to 17, download your Claims, Funders and Pipeline tabs from Google Sheets (File, Download, Comma-separated values) and rename them claims.csv, funders.csv and pipeline.csv before you upload.
   You'll know it worked when the Project lists all the files you uploaded. If an upload fails on a file type, convert nothing; skip that file and note which one for the help request.

5. **GR-LC-01-5.** Test that it answers from your files. In the Project, ask "What do Tier 1, Tier 2 and Tier 3 mean in this tracker?"
   You'll know it worked when the answer matches your Rubric tab. If it invents different rules, check that Rubric.csv is uploaded.

6. **GR-LC-01-6.** Test that it refuses to guess. Ask "What is the deadline for the Example Family Foundation?"
   You'll know it worked when it says the deadline is not in what you gave it and tells you where to look. If it gives a date, the instructions weren't saved; repeat step 3 and test again.

7. **GR-LC-01-7.** Refresh your three tab exports (claims, funders, pipeline) once a month, or after any big change, by deleting the old file from the Project and uploading the new one.
   You'll know it worked when the Project's files show today's version.

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-LC-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

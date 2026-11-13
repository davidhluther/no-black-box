# IP-FR-04: Draft and Check

You will write the draft from the brief and then check it three ways: a built-in word check in Google Docs, a plain-language check [prompt](../glossary.md#prompt), and a fact check where you open every source. Allow about two hours.

1. **IP-FR-04-1.** Start a new chat. Paste your context block (prompt 0), wait for "ready", then paste prompt 8 followed by your brief.
   You'll know it worked when you receive a full draft that follows your outline. If it ignores your rules or invents statistics, it's E07 or E08.

2. **IP-FR-04-2.** Copy the draft into a new Google Doc in your drafts folder, named with the post's title.
   You'll know it worked when the draft shows in the Doc with its headings.

3. **IP-FR-04-3.** Add the draft check to the Doc. In the Doc, choose Extensions, then [Apps Script](../glossary.md#apps-script), delete the starter code, paste in [doc-check.gs](../free/doc-check.gs), save, and reload the Doc. A "Draft check" menu appears after a few seconds. Allow the permissions when asked.
   You'll know it worked when the menu appears. If it does not, it's E13; if Google warns the app is unverified, see E06.

4. **IP-FR-04-4.** Click Draft check, then Check this draft. Read the message: banned words, long paragraphs, curly quotes, colons, word count, and how many numbers need a source. Fix what it lists.
   You'll know it worked when the message shows no banned words and no long paragraphs.

5. **IP-FR-04-5.** Run prompt 9 on the draft, read the list of problems, and tick the ones you agree with. Then run prompt 10 with only those fixes.
   You'll know it worked when the revised draft comes back with a list of changed sentences. Review each change; the [AI model](../glossary.md#ai-model) sometimes edits more than you asked.

6. **IP-FR-04-6.** Run prompt 11 to list every number, date, name, and claim. Open the source for each one and confirm it says what the post says.
   You'll know it worked when every claim has a source you opened or has been cut. This is the step that stops invented facts from going live (E08).

7. **IP-FR-04-7.** Add a real example from your own organization wherever the draft shows a bracket that says to add one. A real detail (a place, a first name used with permission, a real number from your own records) is what makes a post read as written by a person.
   You'll know it worked when no bracket remains.

8. **IP-FR-04-8.** Ask one person who did not write it to read the draft from the top to the bottom.
   You'll know it worked when they can tell you, in one sentence, what the post helps them do. If they cannot, revise the opening.

9. **IP-FR-04-9.** Set the [Queue](../glossary.md#queue) row's stage to Review and paste the draft's link into draft_link.
   You'll know it worked when the Queue row shows both.

Next, [IP-FR-05, images, packaging, and publishing](IP-FR-05-images-package-publish.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

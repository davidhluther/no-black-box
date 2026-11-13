# BK-FR-03: Add the Check-Up Button and Ask Your First Question

You will end with a Help menu in your sheet that tests your setup, and one real question answered about your books by an AI model. About 25 minutes. Nothing here connects to QuickBooks.

## Steps

1. **BK-FR-03-1.** Open your "Treasurer cash and [runway](../glossary.md#runway)" sheet. Click Extensions, then [Apps Script](../glossary.md#apps-script). A new window opens.
   You'll know it worked when you see a code editor with a file called Code.gs. Apps Script is a small programming tool built into Google Sheets. It is free with your Google account.

2. **BK-FR-03-2.** Delete everything in the editor. Open `free/checkup.gs` from this kit, select all of it, copy, and paste it into the editor. Click the disk icon to save.
   You'll know it worked when the editor shows the new code starting with a long comment about the "Books kit [check-up](../glossary.md#check-up)". The program reads only this sheet. It never reads QuickBooks and it reports counts and yes or no answers only, never amounts or names.

3. **BK-FR-03-3.** Click Run (the triangle) with the function onOpen chosen at the top. Google will ask you to review permissions. Click Review permissions, pick your account, and if you see "Google hasn't verified this app", click Advanced, then Go to the project name, then Allow.
   You'll know it worked when the run finishes with no red message. Google words this permission broadly because Apps Script permissions are broad. The code is short, and you can read it first. If you decide not to allow it, the free version still works without the check-up (E06).

4. **BK-FR-03-4.** Go back to your sheet and reload the page. Look at the menu bar.
   You'll know it worked when a Help menu appears next to the other menus. If it does not, wait ten seconds and reload once more (E05).

5. **BK-FR-03-5.** Click Help, then Run check-up. A box opens with a [support code](../glossary.md#support-code), a result line, and a report.
   You'll know it worked when the code ends in "E00" before the version number, such as BK-FR-03-5-E00-v0.1.0 followed by three characters. That means every check passed. Any other E number is in `fixes.md`, and the step shown in the code is the step to repeat.
   A support code is a short code that tells a helper which step failed and what went wrong. It holds none of your figures. The box shows exactly what the optional report contains before you copy anything.

6. **BK-FR-03-6.** Open a free ChatGPT, Claude, or Gemini chat. Open `free/prompts.md` and paste the standing instruction from section 1. Then paste your exported [balance sheet](../glossary.md#balance-sheet) from guide BK-FR-01, and paste the first question in section 2.
   You'll know it worked when the AI model answers with cash accounts and labels each figure Books. If it gives numbers that are not on your report, say so and ask it to quote the row (E09). If it says the report is too long, paste only the cash section (E10).

7. **BK-FR-03-7.** Check one figure from the answer against the QuickBooks screen.
   You'll know it worked when the two agree. Get in the habit: every figure you will repeat in a meeting gets checked against QuickBooks first.

## What to do next

Use `free/monthly-routine-checklist.md` once a month. If you want an AI model to look at live books instead of pasted reports, see guide BK-LC-01 or BK-LC-02.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-FR-03-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

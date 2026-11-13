# IP-FR-01: Make Your Workspace

You will build the Google Sheet that tracks every post, copy the checklist, and run the [check-up](../glossary.md#check-up). This takes about 30 minutes and no software installs. You will need a Google account and a web browser.

1. **IP-FR-01-1.** Open Google Sheets (Google's free spreadsheet app) at sheets.google.com and sign in with your Google account.
   You'll know it worked when you see a blank grid or a list of your spreadsheets. If you land in a sign-in loop, it's E01.

2. **IP-FR-01-2.** Click the blank spreadsheet to start a new one and name it "Idea to Live Post" (click the title at the top left).
   You'll know it worked when the name shows at the top left of the page. If you cannot create files, ask whoever runs your Google account to let you; see E01.

3. **IP-FR-01-3.** Add four tabs named exactly Ideas, [Queue](../glossary.md#queue), Measure, and Setup. For each one, open the matching file in the [free folder](../free/) (ideas.csv, queue.csv, measure.csv, setup.csv), download it with the download button on the file's page, then in your sheet choose File, then Import, then Upload, pick the file, and choose "Insert new sheet(s)". Rename each new tab to its exact name (capital first letter, no spaces).
   You'll know it worked when four tabs show at the bottom, each with a header row and one example row. If a tab is missing or named differently, it's E02.

4. **IP-FR-01-4.** On each tab, delete the example row (the one that says "delete this row") but leave the header row, row 1, exactly as it is.
   You'll know it worked when each tab shows only its headers. If you changed a header name by accident, retype it from the matching [CSV](../glossary.md#csv) file; this is E03.

5. **IP-FR-01-5.** Open the Setup tab and fill in the value column for these keys: org_name, audience, voice_notes, site_url (starting with https://), blog_path, and one_call_to_action. Leave search_console_property and bing_site_url blank for now. Keep the version row set to FR.
   You'll know it worked when no required row has an empty value. A blank required value is E04.

6. **IP-FR-01-6.** Add the check-up button. In the sheet, choose Extensions, then Apps Script (Google's tool for adding small programs to a sheet). Delete any code in the editor, paste in everything from [checkup.gs](../free/checkup.gs), and click the save icon.
   You'll know it worked when the editor shows your pasted code and no red error marks. If the menu does not appear in the next step, it's E05.

7. **IP-FR-01-7.** Go back to your sheet and reload the page. After a few seconds a Kit help menu appears next to the other menus. Click Kit help, then Run check-up. Google asks you to allow the script. Click through the [prompts](../glossary.md#prompt) and allow it.
   You'll know it worked when a pop-up window appears. Google may say the app is not verified, because you wrote it yourself; this is expected, and E06 shows the clicks to take.

8. **IP-FR-01-8.** Read the pop-up. It shows one [support code](../glossary.md#support-code) and the full report that would be shared. The report lists only tab names, header names, and whether each Setup value is filled or empty. It never shows what you typed.
   You'll know it worked when the code ends in OK, like IP-FR-00-0-OK-v0.1.0 followed by three characters. If it shows a different code, find that code's problem in [fixes](../fixes.md).

9. **IP-FR-01-9.** In Google Drive, make a folder called "Idea to Live Post" with these folders inside it: ideas, briefs, drafts, images, and measure. Then open [post-checklist.md](../free/post-checklist.md), copy its contents into a new Google Doc, and name it "Post checklist (template)".
   You'll know it worked when you can see the five folders and the template Doc. If you cannot create folders, see E01.

Next, [IP-FR-02, pick ideas and topics](IP-FR-02-pick-ideas-and-topics.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

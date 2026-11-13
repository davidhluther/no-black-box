# IP-LC-03: Pull Search Data

You will have your Sheet ask Search Console (Google's free tool that shows which searches reach your site) for the last 28 days of page and search data and write it to a tab. The script only asks for data and cannot change anything in Search Console. It was written for this kit and has not yet been tested against a live account, so run it on a small test first and report problems through the help box. Allow about 30 minutes.

1. **IP-LC-03-1.** Make sure your site is verified in Search Console and that the property name (it looks like sc-domain:example.org) is in the search_console_property row of your Setup tab. See guide IP-FR-03 and the [keys and accounts guide](../../../guides/keys-and-accounts.md) if not.
   You'll know it worked when the row is filled and Search Console shows the property as verified. If not, it's E10.

2. **IP-LC-03-2.** Open Extensions, then [Apps Script](../glossary.md#apps-script). Add a new script file named gscpull and paste in [gsc-pull.gs](../free/gsc-pull.gs). Save.
   You'll know it worked when the editor shows the new file with no red error marks.

3. **IP-LC-03-3.** In the Apps Script editor, open the settings page (the gear icon) and turn on "Show appsscript.[json](../glossary.md#json) manifest file in editor". Open the manifest file, and replace its contents with [appsscript.json](../free/appsscript.json) from the kit. Save.
   You'll know it worked when the manifest lists five permission lines (called scopes) and saves without an error.

4. **IP-LC-03-4.** Reload the Sheet. A Search data menu appears. Click Search data, then Pull last 28 days. Allow the permissions, including permission to view Search Console data.
   You'll know it worked when a SearchData tab appears with rows. Google may warn the app is unverified because you wrote it; this is E06.

5. **IP-LC-03-5.** Open the Log tab and read the newest row. It says ok, empty, or FAILED with a reason.
   You'll know it worked when the row says ok. An HTTP 403 or "[API](../glossary.md#api) not enabled" message is E11. An empty result on a brand-new site is normal; Search Console only has data from the day you verified.

6. **IP-LC-03-6.** Click Search data, then Pull every Monday morning.
   You'll know it worked when you see the confirmation message. A quiet Log on a Monday means the schedule failed; this is E20.

7. **IP-LC-03-7.** Ask your [AI model](../glossary.md#ai-model) to read the SearchData tab and name the searches that show you often but earn few clicks. Use [prompt](../glossary.md#prompt) 17 as the model.
   You'll know it worked when it lists searches you can check against the tab. Never accept a number you cannot find in the tab.

Next, [IP-LC-04, run a post from idea to live](IP-LC-04-run-the-flow.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-LC-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

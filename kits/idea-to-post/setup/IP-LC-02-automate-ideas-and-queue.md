# IP-LC-02: Automate Ideas and the Queue

You will have your Google Sheet collect the week's headlines from [feeds](../glossary.md#feed) you choose. A feed (the machine-readable list of a site's newest posts) lets the sheet check sources for you on a schedule. Allow about 30 minutes.

1. **IP-LC-02-1.** In your Sheet, add a tab named Feeds. Import [feeds.csv](../free/feeds.csv) into it as you did for the other tabs in guide IP-FR-01, then replace the example rows with real feed addresses of sites you chose, one per row, with a name in the first column.
   You'll know it worked when the Feeds tab shows a name and a web address starting with https:// on each row. If you do not know a site's feed address, try the site's address with /feed or /rss on the end, or search the site's name with the word RSS.

2. **IP-LC-02-2.** Open Extensions, then [Apps Script](../glossary.md#apps-script). Click the plus beside Files, choose Script, name it feeds, and paste in [feeds.gs](../free/feeds.gs). Click save. Make sure the [project](../glossary.md#project) also contains the [check-up](../glossary.md#check-up) code from IP-FR-01 as its own file.
   You'll know it worked when the editor shows two or more files and no red error marks. If the check-up menu stops appearing, it's E05.

3. **IP-LC-02-3.** Reload the Sheet. A new Ideas menu appears next to Help. Click Ideas, then Fetch feeds now, and allow the permissions when Google asks.
   You'll know it worked when new rows appear on the Ideas tab and a Log tab appears. Google may warn the app is unverified because you wrote it; E06 shows the clicks.

4. **IP-LC-02-4.** Open the Log tab. Each feed shows ok, empty, or FAILED with a reason.
   You'll know it worked when each feed you expect shows ok. A FAILED row is E09.

5. **IP-LC-02-5.** Click Ideas, then Run every Monday morning. This asks Google to run the fetch each Monday at 7 a.m.
   You'll know it worked when you see the confirmation message. A schedule that stops without telling you is the real risk, so each Monday check that the Log tab has a new row; if it does not, it's E20.

6. **IP-LC-02-6.** In your [Project](../glossary.md#project) or in Claude, ask the [AI model](../glossary.md#ai-model) to read the new rows on the Ideas tab and work through the industry-intel steps: open each original source, rate it A to D, and say which items deserve a post. Paste the rows into the chat if your plan cannot read your Sheet directly.
   You'll know it worked when each kept idea has a source you read and a rating. If the AI model gives a rating for something it could not open, it's E08.

7. **IP-LC-02-7.** Run the topic-screen skill (or [prompt](../glossary.md#prompt) 2) with your existing posts and the ideas. Add survivors to the [Queue](../glossary.md#queue) tab at stage Screened.
   You'll know it worked when the Queue shows each go idea at stage Screened.

Next, [IP-LC-03, pull search data](IP-LC-03-pull-search-data.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-LC-01-3). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

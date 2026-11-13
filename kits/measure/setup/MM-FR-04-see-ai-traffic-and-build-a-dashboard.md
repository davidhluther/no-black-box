# See AI Traffic and Build a Dashboard (Free, Guide 4)

You will give visits from AI tools their own line in Google Analytics 4, then draw your sheet as a dashboard that updates itself. About 40 minutes.

1. **MM-FR-04-1.** Open [GA4](../glossary.md#ga4) and click the gear (Admin), then "Data display", then "[Channel groups](../glossary.md#channel-group)". A [channel group](../glossary.md#channel-group) sorts visits into labeled buckets such as Organic Search and Direct. Click "Create new channel group" and name it "Channels with AI". Google moves menus around from time to time. If these names differ, search Google's help for "GA4 custom channel group" and look for the page with the newest date; it's E23.
   You'll know it worked when you see a form asking for channel names and conditions.

2. **MM-FR-04-2.** Add the AI channel. Click "Add new channel", name it "AI Traffic", and set the condition to "Source" and "matches [regex](../glossary.md#regex)". A [regex](../glossary.md#regex) is a short text pattern, like a stencil. Paste the one line from the kit's `overrides/ga4-events-setup/references/ai-sources-regex.txt`. It matches the websites of ChatGPT, Perplexity, Copilot, Gemini, Claude and a few others. Add the AI channel first, then add the default channels (Direct, Organic Search, Referral and so on) beneath it. Order matters: GA4 checks channels from the top and the first match wins, so AI Traffic has to sit above Referral. Save.
   You'll know it worked when the group saves with AI Traffic at the top of the list. Google may let you apply the group to past data too; check Google's help to see whether yours does, because the answer depends on the type of report.

3. **MM-FR-04-3.** Read it. Click Reports, then Acquisition, then "Traffic acquisition". Above the table click the dropdown that says "[Session](../glossary.md#session) primary channel group" and choose your group's name. You should see AI Traffic as its own row.
   You'll know it worked when the row exists. A row with very low numbers or zero is normal for many small sites, and it is not a failure; see E15 if you expected more. Treat the number as a floor, never the total. Many AI answers send visitors with no sign of where they came from ([AI referral traffic](../glossary.md#ai-referral-traffic) is only the part that can be seen), and a click from an AI summary on a Google results page looks like ordinary search.

4. **MM-FR-04-4.** Copy last month's AI Traffic numbers into your "AI referrals" tab. Click the AI Traffic row to see which sources it holds, and enter one row per source (month, source, sessions, engaged sessions, key [events](../glossary.md#event)). In the note column write "floor, not total".
   You'll know it worked when the tab shows each source with numbers. If the source list is empty but you know AI tools send visits, it's E15.

5. **MM-FR-04-5.** Build the dashboard. Open Looker Studio (Google's free dashboard tool) at lookerstudio.google.com and sign in with the same Google account. Click "Create", then "Report". Choose "Google Sheets" as the data source, choose your measurement sheet and the "Monthly traffic" tab, and click "Add". Click "Add to report" if asked.
   You'll know it worked when a blank report opens with your sheet's columns listed on the right. If you see "Data set configuration error" or an empty list, it's E16.

6. **MM-FR-04-6.** Add three charts. Use the "Add a chart" menu. Choose a time series chart with month on the horizontal axis and search_clicks and organic_sessions as the lines. Add two scorecards (big single numbers) for key_events and search_clicks. Add a table fed by the "AI referrals" tab (use Add data again). Give the report a title that says what it is, for example "Website numbers, by month".
   You'll know it worked when the charts show the example rows. Replace the example rows in the sheet with real ones and the charts update after a refresh.

7. **MM-FR-04-7.** Share it safely. Click Share at the top right, choose "Manage access", and add the people who need to see it as "Viewer". Do not choose "Anyone with the link" unless you are sure no names, emails or private notes are in the sheet. The sheet should hold totals only.
   You'll know it worked when the people you named can open it. Check the sharing settings of the sheet itself too; a dashboard reader may need access to the data behind it.

Next: [Run your monthly check](MM-FR-05-run-your-monthly-check.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

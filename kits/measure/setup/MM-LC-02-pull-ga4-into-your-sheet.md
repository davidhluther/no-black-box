# Pull GA4 Into Your Sheet (Low Cost, Guide 2)

You will add a second small program that fills in last month's [GA4](../glossary.md#ga4) numbers, then make both run by themselves each month, with an email if one ever fails. About 30 minutes.

1. **MM-LC-02-1.** Switch on the Google Analytics connection. In the [Apps Script](../glossary.md#apps-script) editor click the "+" beside "Services" in the left list, choose "Google Analytics Data [API](../glossary.md#api)", leave the name as AnalyticsData and click Add. This connects the program to GA4 through an [API](../glossary.md#api) (a way for two programs to talk, like a waiter carrying orders between you and the kitchen).
   You'll know it worked when "AnalyticsData" appears under Services. If you cannot find it in the list, it's E20.

2. **MM-LC-02-2.** Add the program. Click "+" beside Files, choose Script, name it `pull-ga4`, and paste in everything from the kit's `free/pull-ga4.gs`. Save. Your Config tab's "ga4_property_id" must hold the number from the free guide 2.
   You'll know it worked when `pullGa4LastMonth` appears in the function dropdown.

3. **MM-LC-02-3.** Run it once with `pullGa4LastMonth`. Allow the permissions when asked. The program asks for GA4 numbers about the organic search channel and about visits whose source matches the AI sites listed at the top of the file.
   You'll know it worked when a pop-up says "Added GA4 rows for" and two dates. If you get "AnalyticsData is not defined", it's E20. If you get a permission error about the property, the Google account you are using needs at least Viewer access to the GA4 property; it's E19.

4. **MM-LC-02-4.** Check the AI rows. Open the "AI referrals" tab. Each row is one AI tool that sent visitors, with its [sessions](../glossary.md#session) and key [events](../glossary.md#event), and the note "floor, not total". The AI list at the top of `pull-ga4.gs` is a short, hand-kept list of AI websites. If a tool you care about is missing, add its address to the list inside the quote marks, separated by a vertical bar.
   You'll know it worked when you see at least one source, or an empty tab if no AI visits reached you last month. Empty is a fact about your traffic, not a failure.

5. **MM-LC-02-5.** Make both programs run each month. In Apps Script click the clock icon ([Triggers](../glossary.md#trigger)), then "Add Trigger". Choose `pullSearchConsoleLastMonth`, "Time-driven", "Month timer", day 3, any hour; then under "Failure notification settings" choose "Notify me immediately". Repeat for `pullGa4LastMonth`. Day 3 matters because [Search Console](../glossary.md#search-console) runs a few days behind.
   You'll know it worked when both triggers show in the list. A program you rely on that fails or skips its turn must never fail quietly, so keep the failure email on. When one arrives, run the program by hand and look for the cause in fixes.md. Write the missed month in your sheet's notes so the gap stays visible.

Next: [Use your AI plan as your analyst](MM-LC-03-use-your-ai-plan-as-your-analyst.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-LC-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

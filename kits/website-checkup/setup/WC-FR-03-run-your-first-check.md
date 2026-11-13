# WC-FR-03: Run Your First Check

You will test your site, read your Google listing, fill in the [scorecard](../glossary.md#scorecard), and turn the results into a plan. About two hours the first time. Take a break between steps. Keep `free/prompts.md` open in another tab.

If you get stuck, the check-up button in your sheet prints a [support code](../glossary.md#support-code), a short code that tells a helper which step failed. The box at the bottom says where to send it.

1. **WC-FR-03-1.** Test your speed. Open pagespeed.web.dev ([PageSpeed Insights](../glossary.md#pagespeed-insights)), paste your home page address, and click Analyze. Look at the Mobile tab. Write the score into the Pages tab (column I, "Mobile score") on a row for your home page. If a box titled "Discover what your real users are experiencing" appears, copy the three numbers ([LCP](../glossary.md#lcp), [INP](../glossary.md#inp), [CLS](../glossary.md#cls)) into columns J, K, and L. Repeat for one or two more key pages.
   You'll know it worked when the Pages tab has a score for each page. If the page says there isn't enough real-world data, that's normal for small sites, and it's E05. If the test fails to load your page, it's E06.

2. **WC-FR-03-2.** Fill in the Competitors tab. Search your business type and town in Google Maps. For you and each of three to five nearby competitors, copy the name, rating, review count, and main category shown on the listing. Add their website addresses.
   You'll know it worked when you have a row per business. If your own business doesn't appear, it's E13.

3. **WC-FR-03-3.** Read your Google listing with `free/local-checklist.md` open beside you. On the Scorecard tab, set the Result column (D) for checks G1 to G11 and L1 to L7. Use only Pass, Partial, Fail, or Unknown. Paste the page address you looked at into "Evidence link". Choose Unknown when you can't see something.
   You'll know it worked when each of those rows has a result. If you type another word, the Points column stays blank, and it's E22.

4. **WC-FR-03-4.** Do the reviews, markup, and positioning checks. For reviews (R1 to R6), compare your rating and count with the competitors you listed. For markup (D1 to D5), view your home page source and paste [prompt](../glossary.md#prompt) 5 from `free/prompts.md` into an [AI model](../glossary.md#ai-model) chat along with it. For positioning (P1 to P3), paste prompt 7 with your home page, Google description, and social bio.
   You'll know it worked when the AI's answers include quotes from your own pages. If it reports errors in your markup, test the page at validator.schema.org and see E19. If it says it can't open web pages, paste the text yourself, and it's E11. If it gives numbers you didn't supply, discard the answer and repeat, and it's E12.

5. **WC-FR-03-5.** Check your search visibility. In [Search Console](../glossary.md#search-console), open Performance and set the date range to three months. Copy the clicks, impressions, and average position into a new row in the Monthly tab. Then set checks V1 to V4 on the Scorecard tab. For V3, type `site:` followed by your address into Google (for example `site:example.org`) and see whether your home page appears.
   You'll know it worked when the Monthly tab has one row. If Search Console shows no data, it's E02.

6. **WC-FR-03-6.** Go through the Baseline16 tab and `free/checklist-16-item.md`. For each of the 16 items, write Done, Needs done, or Not applicable in the Status column, and where you looked.
   You'll know it worked when all 16 rows have a status. Test your forms for item 10 by sending a message through each one and waiting for it to arrive.

7. **WC-FR-03-7.** Read the Summary tab. Each section shows points, possible points, a percent, and a reading. Sections with fewer than 60% of their checks answered show "Not enough checked to grade", which is fine. Then paste your findings into prompt 13, "Turn findings into a plan", and ask the AI model for your action plan. Copy the plan into a new Google Doc.
   You'll know it worked when you have a short list of fixes in order. If the Summary tab shows `#DIV/0!`, you haven't filled any results in that section yet, and it's E14.

Next time: run the check again once a month using prompt 15, which takes about 15 minutes. To make speed numbers arrive by themselves, see the low-cost version, [WC-LC-02](WC-LC-02-monthly-speed-pulls.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like WC-FR-03-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at [https](../glossary.md#https)://pigasus.group/contact. Setup questions are free.

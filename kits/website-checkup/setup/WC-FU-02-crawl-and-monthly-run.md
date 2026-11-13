# WC-FU-02: Crawl and Monthly Run

You will run a [crawl](../glossary.md#crawl) of your site for the technical audit, check whether AI crawlers can reach you, and set up the monthly routine. About an hour. Do [WC-FU-01](WC-FU-01-install-in-claude-code.md) first.

If you get stuck, the doctor command prints a [support code](../glossary.md#support-code), a short code that tells a helper which step failed. The box at the bottom says where to send it.

1. **WC-FU-02-1.** Crawl your site. Install [Screaming Frog](../glossary.md#screaming-frog) from screamingfrog.co.uk (its free version covers up to 500 addresses). Open it, type your site address, and click Start. When it finishes, choose Export, then the "Internal" tab, then "All", and save the file as `internal_all.csv`.
   You'll know it worked when the file opens as a table with one row per page. If the columns look mixed up, you re-saved it from a spreadsheet, and it's E15. Use the original export.

2. **WC-FU-02-2.** Run the technical audit. In [Claude Code](../glossary.md#claude-code), type: "Run the technical [SEO](../glossary.md#seo) audit on internal_all.csv." It runs a small script. To run it yourself, type:

   ```
   python3 skills/technical-seo-audit/scripts/analyse_crawl.py internal_all.csv
   ```

   You'll know it worked when you see a health score, a score per category, and findings in order. If it says it can't read the file, it's E15.

3. **WC-FU-02-3.** Check [Common Crawl](../glossary.md#common-crawl) visibility. Replace example.org with your [domain](../glossary.md#domain):

   ```
   python3 skills/common-crawl-checker/scripts/check_visibility.py example.org --months 12
   ```

   You'll know it worked when it prints capture counts and the live test. Timeouts or server errors from Common Crawl are common, and one failed run says nothing about your site. Wait an hour and rerun, and see E20.

4. **WC-FU-02-4.** Optional. If you have a paid [Ahrefs](../glossary.md#ahrefs) account, ask: "Run the [backlink](../glossary.md#backlink) gap with Ahrefs." Without one, ask for the free path: "Run the backlink gap using only my own links."
   You'll know it worked when the report says on its first line which path it used. If it asks for an Ahrefs key you don't have, choose the free path.

5. **WC-FU-02-5.** Set your monthly routine. Put a repeating calendar reminder on the first of each month: "Run the website check-up." In Claude Code, the monthly run is: "Run the monthly check-up: refresh the [baseline](../glossary.md#baseline), rerun the [scorecard](../glossary.md#scorecard), and update the action plan." If you miss a month, run it the day you notice and write the reason in the Monthly tab's Notes column.
   You'll know it worked when the reminder repeats. A missed month should leave a note, never a blank.

6. **WC-FU-02-6.** Run the doctor command again.

   ```
   python3 support/doctor.py website-checkup
   ```

   You'll know it worked when every item passes. Keep the support code with your monthly notes.

> **How to get help.** Write down the step ID where you got stuck (it looks like WC-FU-02-3). Run `python3 support/doctor.py website-checkup` and copy the support code it prints. Then send both to Pigasus Group at [https](../glossary.md#https)://pigasus.group/contact. Setup questions are free.

# Pull Search Console Into Your Sheet (Low Cost, Guide 1)

You will add a small program to your measurement sheet that fills in last month's search numbers with one click. The low-cost version assumes you finished the free guides, so the sheet, tabs, Config and check-up already work. [Apps Script](../glossary.md#apps-script) is free; the only paid part of this version is one roughly 20 dollars a month AI plan, which guide 3 covers. About 30 minutes.

1. **MM-LC-01-1.** Open your measurement sheet, click Extensions, then [Apps Script](../glossary.md#apps-script) (Google's free tool for adding small programs to a sheet). In the left list click the gear (Project Settings) and tick "Show appsscript.json manifest file in editor".
   You'll know it worked when a file called appsscript.json appears in the file list on the left.

2. **MM-LC-01-2.** Give the program read-only permission. Click appsscript.json and make sure it contains an "oauthScopes" list with these three lines, adding the list if it is missing (keep any other lines that are already there):
   `"https://www.googleapis.com/auth/webmasters.readonly"`, `"https://www.googleapis.com/auth/spreadsheets"` and `"https://www.googleapis.com/auth/script.external_request"`. The first line lets the program read [Search Console](../glossary.md#search-console) and nothing more; it cannot change a setting or submit anything.
   You'll know it worked when the file saves without a red mark. If a comma is missing between lines, the editor underlines the spot; it's E18.

3. **MM-LC-01-3.** Add the program. Click Code.gs (or "+" and then Script to add a new file), and paste in everything from the kit's `free/pull-search-console.gs`. Click the disk icon to save. The check-up script from the free version stays in its own file; both can live in the same project.
   You'll know it worked when you can pick `pullSearchConsoleLastMonth` from the dropdown at the top. Your Config tab's "site_url" must hold the Search Console site name from the free guide 2, such as sc-domain:example.org.

4. **MM-LC-01-4.** Run it once. Choose `pullSearchConsoleLastMonth` in the dropdown and click Run. Google asks you to allow it, as in the free guide; click "Review permissions", pick your account, then "Advanced" and "Go to (project name)" if you see an unverified-app notice, then "Allow". Read the list of permissions: they should be Search Console (read only) and your spreadsheets.
   You'll know it worked when a pop-up says "Added Search Console rows for" and two dates. If you get a red error mentioning 403 or "no access", it's E19. If the "unverified app" notice never lets you through, it's E11.

5. **MM-LC-01-5.** Check the rows. Go back to the sheet. "Monthly traffic" has a new row with search clicks, [impressions](../glossary.md#impression), [click-through rate](../glossary.md#click-through-rate) and average position. "Search queries" has up to 50 rows and "Top pages" up to 30. Leave the [GA4](../glossary.md#ga4) columns for guide 2.
   You'll know it worked when real numbers appear. Search Console shows a limited set of rows and hides rare searches, so the page may not match the Search Console graph exactly. Click Help, then "Run check-up" to confirm the sheet's headers still match.

Next: [Pull GA4 into your sheet](MM-LC-02-pull-ga4-into-your-sheet.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-LC-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# GR-FR-01: Make Your Tracker

**What you'll have.** A spreadsheet in Google Sheets (Google's free spreadsheet app) with seven tabs (the labelled pages along the bottom of a spreadsheet) that hold your settings, every ask, what you know about each funder, your claims, and a dashboard. **Time.** About 40 minutes. **You need.** A Google account and a computer with a web browser. No command line (a screen where you type instructions instead of clicking) and no installing.

If you get stuck, the check-up (a button or command that tests your setup) prints a support code (a short code that tells a helper which step failed and holds none of your information). The last box on this page says how to use it.

If any step goes differently from what it says, the "if" line tells you which code to look up in [fixes](../fixes.md).

1. **GR-FR-01-1.** Open Google Sheets at sheets.google.com and sign in with the Google account your organization will use. Click the large "Blank" box to start a new spreadsheet. Click the title at the top left ("Untitled spreadsheet") and type Grants tracker.
   You'll know it worked when you see an empty grid and your title on the top left. If you see a sign-in loop that keeps returning to the sign-in page, it's E17. If you applied for Google Workspace for Nonprofits (Google's free offer of its office apps to eligible nonprofits) and it is still waiting, use a regular Google account for now, which is E18.

2. **GR-FR-01-2.** Get the kit's files. Follow the shared guide [get the kit files](../../../guides/get-the-files.md) (steps NB-FR-07-1 to NB-FR-07-6) to download the kit from https://github.com/davidhluther/no-black-box and unzip it. The folder is named "no-black-box-main". Inside it, open the folders in this order: kits, grants, free, tracker. If you only want to try one file, the same guide shows how to download just that file.
   You'll know it worked when you see seven CSV files (plain tables saved as text) such as Settings.csv and Pipeline.csv. Google turns each one into a tab. If you can't find the tracker folder or the files open as text in your browser, it's E19.

3. **GR-FR-01-3.** Bring in the Settings tab. In your Google Sheet, click File, then Import, then the Upload tab, then "Browse". Choose Settings.csv. Under "Import location", pick "Insert new sheet(s)". Spreadsheets run formulas (calculations typed into a cell). Leave the box labelled "Convert text to numbers, dates, and formulas" ticked, because the Pipeline tab's formulas work out Tier, Fit and Dollars per hour, and they stop working if the box is unticked. Click "Import data".
   You'll know it worked when a new tab named Settings appears at the bottom with 14 rows of labels. If your existing tab was overwritten instead, press Ctrl+Z (Command+Z on a Mac) to undo, then pick "Insert new sheet(s)", which is E09. If the tab has a different name, double-click the name and type Settings exactly.

4. **GR-FR-01-4.** Bring in the Pipeline tab the same way, using Pipeline.csv ("Insert new sheet(s)", conversion box ticked).
   You'll know it worked when the tab named Pipeline has a first row of headings that ends with Tier, Fit (out of 25) and Dollars per hour, and the example row shows Tier 2, 20 and 500 in those three columns. If those three show an error such as #REF! or #ERROR!, it's E04. If everything landed in column A, it's E09.

5. **GR-FR-01-5.** Bring in the Funders tab, using Funders.csv.
   You'll know it worked when a tab named Funders has 19 column headings starting with Funder and ending with Next step. If the headings are wrong, it's E02.

6. **GR-FR-01-6.** Bring in the Claims tab, using Claims.csv. This is your claims register (a table of every fact you may state about your organization, each with its source).
   You'll know it worked when a tab named Claims shows the headings ID, Claim, Value, As of, Source and Status, plus two example rows. If not, it's E02.

7. **GR-FR-01-7.** Bring in the Dashboard tab, using Dashboard.csv.
   You'll know it worked when the Value column fills with numbers, such as 1 beside "Prospects (count)" and 10000 beside "Prospects ($ requested)". If you see #REF! or #ERROR!, it's E04. If numbers look odd or formulas fail, check the region setting described in E04.

8. **GR-FR-01-8.** Bring in the Rubric tab, using Rubric.csv.
   You'll know it worked when a tab named Rubric lists the rules for tiers, fit scores and status words. If not, it's E02.

9. **GR-FR-01-9.** Bring in the DraftCheck tab, using DraftCheck.csv. You'll use it in guide 4.
   You'll know it worked when a tab named DraftCheck shows three instruction lines and the headings "Number found", "Matches your Claims tab?" and "Claim IDs" in row 5. If not, it's E02.

10. **GR-FR-01-10.** Delete the empty starter tab. Right-click the tab called Sheet1 at the bottom, choose Delete, and confirm.
    You'll know it worked when your seven tabs remain and Sheet1 is gone. If Sheet1 holds anything you typed, skip this step.

11. **GR-FR-01-11.** Fill in the Settings tab. Click the Settings tab and type your details into the Value column (column B) beside each label. Don't insert, move or rename rows, because formulas on other tabs read fixed rows. Fill in the short name, legal name, EIN (the nine-digit tax ID on your IRS letter, like 00-0000000), grants contact name and email, the Tier 1 and Tier 2 minimums (25000 and 5000 are already there; change them to fit your budget), and the fiscal-year start date as mm/dd/yyyy, for example 07/01/2026. The others are optional now.
    You'll know it worked when every labelled row you filled shows your text and the date sits right-aligned, which means Sheets read it as a date. If a number or date looks wrong, it's E05, E06, E07 or E08.

12. **GR-FR-01-12.** Delete the example rows. On the Pipeline tab, right-click the row number 2 on the left and choose "Delete row". Do the same for row 2 on Funders, and for rows 2 and 3 on Claims. Never delete row 1.
    You'll know it worked when each tab holds only its headings. The Dashboard will show zeros.

13. **GR-FR-01-13.** Share the sheet with one other person. Click the blue Share button at the top right, type a colleague's or board member's email address, and set them to "Editor". A grants tracker that lives in one person's head or account is a risk.
    You'll know it worked when the Share button shows two people. If Google says it can't share outside your organization, ask whoever manages your Google account.

Next, add the check-up button in [GR-FR-02](GR-FR-02-add-the-check-up-button.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# WC-LC-02: Monthly Speed Pulls

You will make your sheet fetch speed numbers for your key pages on the first of each month, so you never forget. About 30 minutes. It uses an [API](../glossary.md#api) (a way for programs to talk to each other) offered by Google, and a free key.

If you get stuck, the check-up button in your sheet prints a [support code](../glossary.md#support-code), a short code that tells a helper which step failed. The box at the bottom says where to send it.

1. **WC-LC-02-1.** Get a PageSpeed key. Follow the steps for the speed-test key in [Keys and accounts](../../../guides/keys-and-accounts.md). Copy the key somewhere private for a moment. An [API key](../glossary.md#api-key) works like a password. Never paste it into a cell or share a screenshot of it.
   You'll know it worked when you have a long string of letters and numbers. If Google asks you to create a billing account, stop and read the keys guide, and see E18.

2. **WC-LC-02-2.** Save the key in the script. In your sheet, choose Extensions, then [Apps Script](../glossary.md#apps-script). Click the gear icon ([Project](../glossary.md#project) Settings), scroll to "Script Properties", click "Add script property", type `PAGESPEED_API_KEY` as the name, paste your key as the value, and save.
   You'll know it worked when the property shows in the list. Run the check-up from the Help menu. If it reports no key, it's E18.

3. **WC-LC-02-3.** Add the monthly script. In the editor, click the plus next to Files, choose Script, name it `monthly-pulls`, delete the sample code, paste in the contents of `monthly-pulls.gs` from the kit's `free` folder, and save.
   You'll know it worked when the editor shows two files, `checkup` and `monthly-pulls`. Reload the sheet. A "Pull speed now" item should appear under Help. If not, it's E10.

4. **WC-LC-02-4.** List your pages. On the Pages tab, type up to 20 addresses in column A, starting at row 2. Put your home page first. Each must start with [https](../glossary.md#https)://.
   You'll know it worked when the addresses are in column A with nothing in between.

5. **WC-LC-02-5.** Click Help, then Pull speed now. If Google asks permission, allow it, as in [WC-FR-02-6](WC-FR-02-make-your-scorecard-sheet.md). Wait one to two minutes.
   You'll know it worked when scores appear in column I of the Pages tab, and a new row appears on the Monthly tab. If a Notes cell says "Speed pull failed", the reason follows it. HTTP 429 means too many requests and it's E18. If Google blocks the allow screen, it's E09.

6. **WC-LC-02-6.** Make it automatic. In the editor, pick `createMonthlyTrigger` from the function list at the top and click Run. Then click the clock icon ([Triggers](../glossary.md#trigger)) at the left. You'll see one [trigger](../glossary.md#trigger) for `pullSpeedNow`, monthly. Click its three dots, choose Edit, and under "Failure notification settings" choose "Notify me immediately".
   You'll know it worked when the trigger appears. If it doesn't, run `createMonthlyTrigger` again. A run that fails will email you the same day, so you won't discover a missing month weeks later.

7. **WC-LC-02-7.** Click Help, then Run check-up, and confirm it says all checks passed.
   You'll know it worked when the report is clear. Any other code is in the fixes table.

> **How to get help.** Write down the step ID where you got stuck (it looks like WC-LC-02-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

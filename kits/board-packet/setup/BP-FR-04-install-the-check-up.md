# Install the Check-Up

This guide takes about 10 minutes. You will add a small program to your [tracker sheet](../glossary.md#tracker-sheet) that checks your setup and prints a [support code](../glossary.md#support-code).

Each step has an ID. If you get stuck, note the ID. This guide installs the [check-up](../glossary.md#check-up) itself, so until step 6 there is no support code to send, only the step ID. After that, the check-up prints a support code you can send along with the ID.

The program is written in [Apps Script](../glossary.md#apps-script), a free tool from Google that runs small programs inside your Sheets and Drive. You paste the program in once, and then it is just a menu. You never type a command.

You do not have to trust this blindly. The program is one file, [checkup.gs](../free/checkup.gs), with plain comments at the top that say what it does and does not do. Open it and read the first 20 lines before you paste it. It never reads what you typed into your cells, never sends anything anywhere, and never changes your sheet or your Drive.

1. **BP-FR-04-1.** Open your Board Packet Tracker sheet. Click **Extensions** in the menu bar, then **Apps Script**.
   You'll know it worked when a new browser tab opens with a code editor and a file called `Code.gs`. If Extensions has no Apps Script item, your organization's Google administrator may have switched Apps Script off (E28).

2. **BP-FR-04-2.** Click inside the editor, press Ctrl+A (Command+A on a Mac) to select everything, and press Delete. Open [checkup.gs](../free/checkup.gs) on GitHub, click **Copy raw file**, go back to the editor, and paste.
   You'll know it worked when the editor shows many lines starting with `/**` and `Board packet check-up`. If you still see `function myFunction`, the old text was not deleted. Select all and delete again.

3. **BP-FR-04-3.** Click the disk icon (**Save project**). Click "Untitled project" at the top and type `Board packet kit`. Click **Rename**.
   You'll know it worked when the project has its new name. If a red error line appears, you probably missed a few lines when copying. Select all, delete, and paste again.

4. **BP-FR-04-4.** Above the editor, open the drop-down beside the **Run** button (it lists the program's parts by name) and choose `onOpen`. Click **Run**. A box says **Authorization required**. Click **Review permissions**, choose your Google account, and read the screen.
   Google will say "Google hasn't verified this app". That is normal for a program you made yourself. Click **Advanced**, then **Go to Board packet kit (unsafe)**, then **Allow**. The program asks to see and manage the spreadsheets and Drive files it works with. The check-up only reads folder names, but Google's permission wording is broad.
   You'll know it worked when the log at the bottom says "Execution completed". If the Advanced link is missing, try a different browser or a personal Google account, and it's E28.

5. **BP-FR-04-5.** Go back to the tracker sheet tab and reload the page (the circular arrow in your browser, or Ctrl+R / Command+R). Wait about 10 seconds.
   You'll know it worked when the menu bar shows two menus named **Help**. Google's own Help menu is the last one on the right. The one we added is to the left of Google's own, so use that one: its only item is "Run check-up". If you see only one Help menu and it has no "Run check-up", it's E29.

6. **BP-FR-04-6.** Click **Help**, then **Run check-up**.
   You'll know it worked when a box appears with a code like `BP-FR-00-0-E00-v0.1.0-7KQ` and a report. If the code starts with something other than `BP-FR-00-0`, the check-up found something to fix. The report lists each problem with its E code. Look the code up in [fixes.md](../fixes.md), fix it, and run the check-up again. Repeat until the code starts with `BP-FR-00-0`.

7. **BP-FR-04-7.** Read the report on screen. This is everything that would be shared if you copy it. It holds counts and yes-or-no answers, never names, addresses, folder names, or the text of any cell.
   You'll know it worked when you can see that for yourself. The Copy report button is optional. Use it only if you decide to ask for help.

**You are done with free setup.** Total time across guides BP-FR-01 to BP-FR-04 is about 50 minutes if nothing goes wrong, which most people spread over a couple of sittings. Guide BP-FR-05 walks through your first month.

> **How to get help.** Write down the step ID where you got stuck (it looks like BP-FR-04-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

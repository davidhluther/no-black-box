# GR-FR-02: Add the Check-Up Button

**What you'll have.** A Kit help menu in your tracker (your Google Sheets spreadsheet, Google's free spreadsheet app) with a check-up (a button that tests your sheet's setup). It prints one short support code (a code that tells a helper which step failed). The code holds none of your information. **Time.** About 15 minutes. **You need.** The tracker from [GR-FR-01](GR-FR-01-make-your-tracker.md) and the file checkup.gs in the free folder of the kit you downloaded (see [get the kit files](../../../guides/get-the-files.md) if you need it again).

The check-up is a small program (a script) written for Apps Script (a free tool built into Google Sheets that runs small programs for your spreadsheet). You paste it in; you do not write any code. The check-up only looks at the shape of your sheet. It never reads or reports what is in your cells, and it sends nothing anywhere.

1. **GR-FR-02-1.** In your tracker, click Extensions, then Apps Script. A new browser tab opens with a page of code.
   You'll know it worked when the new tab says "Apps Script" at the top and shows a file named Code.gs. If a "Build automations with Gemini" box covers the page, close it with its X. If the Extensions menu has no Apps Script, or you see an error about permissions, it's E10.

2. **GR-FR-02-2.** Click inside the code box, press Ctrl+A (Command+A on a Mac) to select everything, and press Delete.
   You'll know it worked when the code box is empty.

3. **GR-FR-02-3.** Open the file checkup.gs from the free folder you downloaded, using any plain text program (Notepad on Windows, or TextEdit on a Mac). Press Ctrl+A (Command+A) to select all, then Ctrl+C (Command+C) to copy.
   You'll know it worked when you can see a long file that starts with "Grants kit check-up (free version)". If the file opens in a word processor with odd formatting, close it and use Notepad or TextEdit instead.

4. **GR-FR-02-4.** First click "Untitled project" at the top, type Grants kit, and click Rename. Google shows this name on the permission screen in step 6; if you rename later, it may still say "Untitled project". Then click in the Apps Script code box, delete anything already there, and paste with Ctrl+V (Command+V). Click the disk icon (Save project).
   You'll know it worked when the pasted code is there and the Save icon turns grey. You can read every line before you go on. If you see red marks under the code, delete everything and paste again.

5. **GR-FR-02-5.** Close the Apps Script tab. In your tracker tab, reload the page (the circular arrow in the browser, or Ctrl+R / Command+R). Wait about five seconds.
   You'll know it worked when a new menu named Kit help appears at the right end of the menu bar, after Google's own Help and Accessibility menus. Google's Help menu doesn't have the check-up; use Kit help. If it doesn't, it's E10.

6. **GR-FR-02-6.** Click Kit help, then "Run check-up". The first time, a box says "Authorization required". Click "OK". A new window opens; choose your account. You may see "Google hasn't verified this app". That is expected, because you made this script yourself rather than publishing it to the public. Click "Advanced", then the "Go to ... (unsafe)" link. It may say "Untitled project" instead of Grants kit, because Google keeps the name from the first save. The next page lists two permissions, each with a tick box: to view and manage spreadsheets this script is installed in, and to show its own small window. Tick "Select all", then click "Continue". The window says "Authorization successful" and closes or can be closed. The script asks only to work with this one spreadsheet. Click Kit help, then "Run check-up" again.
   You'll know it worked when a small window opens titled "Grants kit check-up". If the warning page offers no "Advanced" link, it's E11.

7. **GR-FR-02-7.** Read the window. It shows a support code, such as GR-FR-02-7-E00-v0.1.0-V72, and a plain-text report you can read before you copy anything. Nothing is sent from this window. If the code contains E00, everything checks out. If it contains another code, such as E05, look that code up in [fixes](../fixes.md) and follow its fix, then run the check-up again.
   You'll know it worked when you see a code ending in a version and three letters or numbers. Run it again after each fix; the code changes as problems clear.

You can run the check-up any time. It is the first thing to do when something looks wrong.

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

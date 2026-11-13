# PW-LC-03: Add the Word Check to Google Docs

You'll end with two new menus in a Google Doc. One highlights banned words and phrases in yellow. The other, Help, runs a check-up that prints a [support code](../glossary.md#support-code). It takes about 15 minutes. You don't need the [command line](../glossary.md#command-line).

The menus come from Apps Script (a free tool inside Google Docs for adding small programs, like writing your own extra buttons). The [script](../glossary.md#script) reads only the Doc it's attached to. It never sends your text anywhere and never changes your words.

1. **PW-LC-03-1.** Open the Google Doc you want to check, or paste the example draft into a new Doc. Open [example-draft.md](../free/example-draft.md), copy it, and paste it into a blank Doc if you want a safe test.
   You'll know it worked when your text appears in the Doc.
2. **PW-LC-03-2.** In the Doc, choose Extensions, then Apps Script.
   You'll know it worked when a new browser tab opens with a code editor that already holds a few lines such as "function myFunction." If you opened the editor from script.google.com instead, the check-up will report E10.
3. **PW-LC-03-3.** Open [checkup.gs](../free/checkup.gs) in this kit, and click the Raw button so you see plain text. Select all, copy. In the editor, select all existing text, delete it, and paste.
   You'll know it worked when the editor shows the whole file, ending with a function called runCheckup. If words are missing, it's E11. If the check-up later says a pattern isn't valid, it's E12.
4. **PW-LC-03-4.** Click the disk icon (Save [project](../glossary.md#project)). If it asks for a name, call it "Plain writing word check."
   You'll know it worked when the tab title shows your project name and the save icon turns gray.
5. **PW-LC-03-5.** Choose the function `onOpen` from the drop-down near the top (it shows a function name next to Run and Debug). Click Run. Google asks you to review permissions. Pick your account. A warning that "Google hasn't verified this app" is normal for a script you added yourself (it's E07). Click Advanced, then the "Go to Plain writing word check" link, then Allow.
   You'll know it worked when the execution log at the bottom says "Execution completed." If the permission box keeps coming back, it's E09.
6. **PW-LC-03-6.** Go back to the Doc tab and reload the page (Ctrl+R on Windows, Command+R on a Mac).
   You'll know it worked when the menu bar shows two new menus, Plain writing and Help. If they don't appear, it's E08. If the first menu click says the script can't read the Doc, it's E13.
7. **PW-LC-03-7.** Choose Help, then Run check-up.
   You'll know it worked when a box shows a support code like `PW-LC-03-0-OK-v0.1.0-XXX`, where the last three characters vary, and says "Setup looks right." If it shows a different code, the box says what failed. Use that code in the [fixes](../fixes.md) table. The box shows exactly what would be shared if you choose to send it. It holds test results only, never your text.
8. **PW-LC-03-8.** Choose Plain writing, then Highlight banned words.
   You'll know it worked when words such as "robust," "testament," "seamless," "Moreover," and "In conclusion" turn yellow in the example draft, and a box says how many matches it highlighted. Rewrite each one, then choose Clear highlights.

The word lists are at the top of the script. To allow a word, delete it from the list. To ban another, add it. Saving the change takes effect next time you reload the Doc.

This check covers words and phrases only. It can't judge structure, so walk through your checklist (guide `PW-FR-02`) after it.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like PW-LC-03-5). If you set up the Google Docs word check, run Help, then Run check-up, and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

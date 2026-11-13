# AV-LC-01: Add the Logging Menu

Time, about 20 minutes. You will add a second [Apps Script](../glossary.md#apps-script) file to the sheet from the free version. It gives you an "AI visibility" menu with "Log an answer", which saves the answer and fills in a best-guess Results row for you. You must have finished guides AV-FR-01 to AV-FR-03 first, with a [frozen](../glossary.md#frozen) [question set](../glossary.md#question-set).

1. **AV-LC-01-1.** Open your "AI visibility check" sheet. Choose Extensions, then Apps [Script](../glossary.md#script) (the menu item you used in guide AV-FR-01). In the left list, next to Files, click the plus button and choose Script. Name the new file `LogAnswers`.
   You'll know it worked when the file list shows Code.gs and LogAnswers. If the plus button is missing, it's E12.

2. **AV-LC-01-2.** Open `low-cost/log-answers.gs` from the kit, copy all of it, and paste it into the empty LogAnswers file. Click Save.
   You'll know it worked when the editor shows the code with no red marks. If Save fails, it's E12.

3. **AV-LC-01-3.** Make sure Code.gs still holds the [check-up](../glossary.md#check-up) code from the free version. The check-up file calls the logging file when it opens the sheet, so both menus appear. Go back to the sheet and reload the page.
   You'll know it worked when the top menu bar shows both Kit help and AI visibility. If AI visibility is missing, it's E22.

4. **AV-LC-01-4.** Click AI visibility, then Log an answer. Google asks you to authorize the new script. Follow the same steps as in AV-FR-01-5. It only asks to see and change this spreadsheet.
   You'll know it worked when a form opens with boxes for question code, AI product, answer text, sources, other businesses named, and run label. If Google keeps asking, it's E13.

5. **AV-LC-01-5.** Try it with one real answer. Type the question code, for example LD-01. Choose the product. Paste the whole answer. Paste any sources it listed into the sources box. In "Other businesses named" list the businesses the answer names, separated by semicolons. Pick what the answer settled on. Click Log it.
   You'll know it worked when the form says "Logged LD-01..." and a new row appears on the Results tab, with a note saying "guessed by script, check it". The full answer is saved on a new tab called Answers. If you see a red "Problem:" message, it's E23.

6. **AV-LC-01-6.** Read the row. The script guesses by matching your business name and website address in the text. It does not understand the answer. Correct anything wrong, especially position and [same-name](../glossary.md#same-name) answers.
   You'll know it worked when you agree with the row. Trust your reading over the script's.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-LC-01-3). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

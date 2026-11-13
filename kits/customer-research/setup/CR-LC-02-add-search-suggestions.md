# CR-LC-02: Add Search Suggestions

You will add an [Apps Script](../glossary.md#apps-script) that collects the suggestions a search box offers (called [autocomplete](../glossary.md#autocomplete)) into your Sheet. Time: about 20 minutes.

1. **CR-LC-02-1.** In your Sheet, choose Extensions, then Apps Script. Click the plus sign next to Files, choose Script, and name it `autocomplete`. Open `autocomplete.gs` from the [free folder](../free/), copy all of it, paste it into the new file, and click the disk icon.
   You'll know it worked when the editor lists two files, Code.gs (the [check-up](../glossary.md#check-up)) and autocomplete. If you see an error mark, copy again and check nothing was cut off.

2. **CR-LC-02-2.** Make the Autocomplete [tab](../glossary.md#tab) by importing `autocomplete.csv` the same way as in [CR-FR-01](CR-FR-01-make-your-sheet.md) step 2, and name it exactly `Autocomplete`.
   You'll know it worked when the tab shows four columns: date_collected, seed_term, suggestion, kept. If the check-up reports it, it's E06.

3. **CR-LC-02-3.** Make the RunLog tab by importing `runlog.csv` the same way and naming it exactly `RunLog`.
   You'll know it worked when the tab shows five columns starting with run_time. If the check-up reports it, it's E07.

4. **CR-LC-02-4.** Reload the Sheet. A new menu, "Customer research", appears next to Help. Choose "Pull search suggestions now" and allow the permissions when asked (see E13 if Google warns you). Wait about two minutes.
   You'll know it worked when the Autocomplete tab fills with rows and the RunLog tab shows a row with status ok. If the log says FAILED, or an alert says Google returned nothing, it's E12.

5. **CR-LC-02-5.** Paste the suggestions into [prompt](../glossary.md#prompt) P7 in the Project (or any [AI model](../glossary.md#ai-model)) to group them. Add the useful ones to the Quotes tab with the source type "search suggestion", and mark the kept column yes for the ones you use.
   You'll know it worked when you have a short list of questions and phrases your community actually types.

Next, go to [CR-LC-03](CR-LC-03-monthly-routine.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like CR-FR-01-3). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

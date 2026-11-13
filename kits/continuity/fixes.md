# Fixes for the Continuity Kit

Find the code the [check-up](glossary.md#check-up) printed, read what you see, and follow the fix. If a fix does not work, send the code and the step ID to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

| Code | What you see | Why | The fix | Step |
|---|---|---|---|---|
| E01 | The check-up says the BusTest or Churn [tab](glossary.md#tab) is missing | A tab name is misspelled or a tab was deleted | Rename the tab to exactly BusTest or Churn, with those capital letters. Re-import the template file if one is gone | CK-FR-01-2 |
| E02 | The check-up says a header row does not match | A column was moved, renamed or deleted | Copy the first row from `free/templates/BusTest.csv` or `Churn.csv` back into row 1 | CK-FR-01-2 |
| E03 | The check-up says questions still need an answer | A yes or no was left blank before the first no | Answer in order. Type yes or no until the first no, then stop and leave the rest blank | CK-FR-01-5 |
| E04 | The check-up says an answer is something other than yes or no | A typo, such as "y" or "maybe" | Type exactly yes or no. If you are unsure, type no | CK-FR-01-5 |
| E05 | The check-up says the five function names changed | A row was renamed, moved or deleted | Put the five functions back in order in column A, as in the template | CK-FR-01-2 |
| E06 | A score cell in column E is empty or shows an error | The formula was deleted or typed over | Copy the formula from a working score cell, or from the template, into the empty one | CK-FR-01-7 |
| E07 | The total, band or verdict cells are empty | A formula in B8 to B13 was deleted | Copy them back from `free/templates/BusTest.csv` | CK-FR-01-7 |
| E08 | A sign-in loop, or Google says the account is not allowed | The wrong account, or a work account that blocks add-ons | Sign in with a personal Google account. If you use a work account, ask its administrator whether [Apps Script](glossary.md#apps-script) is allowed | CK-FR-01-1 |
| E09 | No Kit help menu appears, or Google blocks the check-up | The page was not reloaded, or the program was not authorized | Reload the Sheet and wait. Authorize again through Advanced, then Go to the project | CK-FR-01-3 |
| E10 | The [AI model](glossary.md#ai-model) skipped a question, scored without asking, or kept asking after a no | The instructions were not saved, or the chat is not inside the project | Open the chat from inside the project, check that the instructions are saved, and say "ask the three questions in order and stop at the first no" | CK-LC-01-5 |
| E11 | A [runbook](glossary.md#runbook) has a step you never told the AI model | It filled a blank with a guess | Delete the step, put "______" back, and ask it to leave any unknown as a blank | CK-LC-02-4 |
| E12 | A password, recovery code or account number was typed into a chat or a document | It slipped in while answering | Delete the chat or the text, change that password or code now, and tell your bank if a full account number was shared. Write only where the secret is kept | CK-LC-02-5 |

## Reading a support code

A [support code](glossary.md#support-code) reads in this order, for example CK-FR-01-5-E04-v0.1.0-7KQ. CK is the kit, FR the free version, 01-5 the guide and step where the first problem sits, E04 the problem, v0.1.0 the kit version, and 7KQ a short check on the results. The check-up never reads the sentences you wrote.

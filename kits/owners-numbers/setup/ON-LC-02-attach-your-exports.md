# ON-LC-02 Attach Your Exports and Read the Page

You will give the Project last month's real files and compare its page to a quick check.

1. **ON-LC-02-1.** Get the four files ready. Either save the data [tabs](../glossary.md#tab) from your Sheet with the [export](../glossary.md#export) menu, or follow steps ON-FR-02-1 to ON-FR-02-3 in [ON-FR-02](ON-FR-02-add-your-exports.md) and save sales.[csv](../glossary.md#csv), bank.csv and bookings.csv by hand. Add a settings.csv with the columns name, value and note, using `free/examples/settings.csv` as the model.
   You'll know it worked when you have four files with the expected column names. A missing column is E31.
2. **ON-LC-02-2.** Open each file and delete any column that holds an account number, card number or a person's name that the scorecard does not need. Keep client_id, which should be a code, not a name.
   You'll know it worked when no column holds an account number. If the [AI model](../glossary.md#ai-model) ever repeats an account number, stop and it's E33.
3. **ON-LC-02-3.** In a new chat inside the project, attach all four files and type Build the Owner's Scorecard for [month and year]. Use only my files.
   You'll know it worked when the answer begins with a verdict and uses my business name. If the AI model asks which month, give it the dates.
4. **ON-LC-02-4.** Check three numbers against your own sense of the month: money in, operating costs and cash on hand. If you also keep the Sheet, compare against its Scorecard tab.
   You'll know it worked when the figures agree. A difference of more than a few dollars is E30. Ask "Show me which rows you added up for money in".
5. **ON-LC-02-5.** Ask Which results are [what-ifs](../glossary.md#what-if) and what input did you assume? Every borrowed number must be named. If the AI model filled a blank setting with its own guess without saying so, it's E32. Tell it to label the result what-if, and to ask you for the number.
   You'll know it worked when each [what-if](../glossary.md#what-if) line names the input behind it.
6. **ON-LC-02-6.** Fill in one more setting in settings.csv, such as fixed_costs_monthly, attach the new file, and ask for the page again.
   You'll know it worked when the [break-even](../glossary.md#break-even) line changes from what-if to actual.
7. **ON-LC-02-7.** Save the page. Copy the answer into a Google Doc or ask the AI model for a PDF-ready version, and name it with the month.
   You'll know it worked when you can open it on your phone.

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-LC-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

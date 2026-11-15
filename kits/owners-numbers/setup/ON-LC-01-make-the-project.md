# ON-LC-01 Make the AI Project

You will set up a saved workspace where an [AI model](../glossary.md#ai-model) reads your [exports](../glossary.md#export) and writes the scorecard. You need a paid plan from ChatGPT or Claude that includes Projects. See the [shopping list](../shopping-list.md) for the current prices and the [keys and accounts guide](../../../guides/keys-and-accounts.md) for signing up.

1. **ON-LC-01-1.** Sign in to ChatGPT at chatgpt.com or Claude at claude.ai with a plan that includes Projects. Look for Projects in the left sidebar.
   You'll know it worked when you can see a Projects item. If you only see a free plan's chat box, check the plan page. If you cannot sign in, it's E15.
2. **ON-LC-01-2.** Click New project and name it Owner's Numbers. An [AI Project](../glossary.md#ai-project) is a saved workspace where standing instructions and files stay put between chats.
   You'll know it worked when an empty project page opens with a place for instructions and a place for files.
3. **ON-LC-01-3.** Open `chatgpt/instructions.md` from the kit. Copy everything below the line of dashes. Paste it into the project's Instructions box and save. It is under 8,000 characters so it fits in a ChatGPT [Custom GPT](../glossary.md#custom-gpt), a ChatGPT Project or a Claude Project.
   You'll know it worked when the instructions show in the box and begin with "You are a careful numbers helper". If the box says the text is too long, you pasted more than the instructions. It's E31.
4. **ON-LC-01-4.** Upload the helper files listed in `chatgpt/knowledge-files.md` (a [knowledge file](../glossary.md#knowledge-file) is a document the AI model can read every time). Do not upload your own exports here.
   You'll know it worked when the project lists the files by name.
5. **ON-LC-01-5.** Test with the invented example. Start a chat in the project, attach `free/examples/sales.csv`, `bank.csv`, `bookings.csv` and `settings.csv`, and type Build the Owner's Scorecard for September 2026.
   You'll know it worked when the answer starts with a verdict saying the month paid for itself, shows money in and out, lists top items, and ends with one thing to look at. If it does not mention [what-if](../glossary.md#what-if) labels at the end, ask "Which results are what-ifs?" If it never read a file, it's E31.
6. **ON-LC-01-6.** Add the optional export menu to your Sheet. In the Sheet choose Extensions, then [Apps Script](../glossary.md#apps-script), add a second file named export-csv, and paste `free/export-csv.gs`. Save and reload the Sheet.
   You'll know it worked when an Owner's Numbers menu appears. Choosing Save data [tabs](../glossary.md#tab) as [CSV](../glossary.md#csv) in Drive creates four files in a Drive folder you own called owners-numbers-data, and the message that follows links to it. A folder of that name someone else shared with you is never used. If no menu appears, it's E16. Skip this step if you do not use the Sheet.

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-LC-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

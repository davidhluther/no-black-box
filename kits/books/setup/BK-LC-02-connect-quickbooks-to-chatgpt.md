# BK-LC-02: Connect QuickBooks to ChatGPT, Read-Only

You will end with ChatGPT able to look at your live QuickBooks books, with creating, sending, and deleting off the table. About 40 minutes.

Intuit announced a QuickBooks [plugin](../glossary.md#plugin) for ChatGPT in the same post as its Claude [connector](../glossary.md#connector), on 07/28/2026: https://www.intuit.com/blog/news-social/quickbooks-expands-into-claude-and-chatgpt-with-new-sales-invoicing-payroll-and-lending-features/. A plugin is ChatGPT's word for an add-on that lets it look inside another service using your own sign-in.

## Read this first

Intuit's post says the tools can create, update, send, and delete invoices and estimates, among other actions. This kit uses only the looking tools and declines everything else. Intuit's post names no ChatGPT plan, so check which plan you need at https://chatgpt.com/pricing before you pay for one. It also says some features require a QuickBooks Online subscription and that payments features are not available outside the U.S.

## Steps

1. **BK-LC-02-1.** Sign in to ChatGPT at chatgpt.com and sign in to QuickBooks Online in another browser window. Use an account that can see reports.
   You'll know it worked when both load. If QuickBooks says you lack permission, it's E16.

2. **BK-LC-02-2.** In ChatGPT, open the place where you add apps or plugins (the menu is called Apps, Plugins, or Connectors, depending on your version) and search for "Intuit QuickBooks".
   You'll know it worked when you see the Intuit QuickBooks entry. If it is missing, your plan or region may not offer it yet (E13).

3. **BK-LC-02-3.** Click it, then sign in to QuickBooks with your own login and pick the right company.
   You'll know it worked when ChatGPT shows QuickBooks as connected. If it picked the wrong company, disconnect and repeat (E12).

4. **BK-LC-02-4.** Read the permissions screen and what it lists. Note any item that creates, edits, sends, or deletes.
   You'll know it worked when you can name the tools you will not allow.

5. **BK-LC-02-5.** Open a new chat with the QuickBooks plugin turned on. Paste the standing instruction from `free/prompts.md` section 1 and the section 9 line about using only tools that read or search. Ask: "What is the cash balance on each bank account as of the last day of last month?"
   You'll know it worked when ChatGPT answers with account names and amounts that match the QuickBooks [balance sheet](../glossary.md#balance-sheet). If it offers to create, send, or delete anything, say no (E14). ChatGPT usually shows an approval box before it acts. Choose Deny.

6. **BK-LC-02-6.** Check the profit and loss basis as in guide BK-LC-01, step 7: ask which basis it used, then run the same report in QuickBooks on both bases.
   You'll know it worked when you know whether the plugin matches your accrual or cash report (E15).

## What to do next

Go to BK-LC-03.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-LC-02-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# BK-LC-01: Connect QuickBooks to Claude, Read-Only

You will end with Claude able to look at your live QuickBooks books and answer questions, with every tool that could change anything switched off or declined. About 40 minutes.

A [connector](../glossary.md#connector) is an add-on that lets an AI model such as Claude look inside another service using your own sign-in. The company that makes QuickBooks publishes an official one for Claude, and it announced the connector, along with a [plugin](../glossary.md#plugin) for ChatGPT, on its own blog on 07/28/2026: https://www.intuit.com/blog/news-social/quickbooks-expands-into-claude-and-chatgpt-with-new-sales-invoicing-payroll-and-lending-features/

## Read this first

Intuit's connector is not [read-only](../glossary.md#read-only) by design. Intuit's post says it can create, update, send, and delete invoices and estimates, create payment links, and add customers and products, and adds that every action stays reviewable by you. This kit uses only the looking tools. You will decline everything else, and step BK-LC-01-6 shows how to make that stick.

Intuit's post says payments features are not available outside the U.S. and that a QuickBooks Online subscription is required for some features. Plan on a U.S. QuickBooks Online company. If your company is outside the U.S., check with Intuit before you start.

## Steps

1. **BK-LC-01-1.** Confirm what you need. You need a QuickBooks Online login that is an administrator or can see reports, and a Claude account. Claude Pro is $20 a month with monthly billing (checked 11/13/2026). Claude's pricing page also lists connectors on the free plan, but check that the QuickBooks connector works on yours: see https://claude.com/pricing.
   You'll know it worked when you can sign in to both QuickBooks and Claude in two browser windows. If QuickBooks says you lack permission, it's E16.

2. **BK-LC-01-2.** In Claude, open Settings, then Connectors (the label may read Integrations or Customize). Click the button to browse or add a connector.
   You'll know it worked when you see a list of services you can connect.

3. **BK-LC-01-3.** Find QuickBooks (published by Intuit) and click Connect. A QuickBooks sign-in window opens. Sign in with your own QuickBooks login. If you manage more than one company, pick the correct company on the screen that follows.
   You'll know it worked when Claude shows QuickBooks as connected. If QuickBooks is not in the list, it's E11. If the wrong company is attached, disconnect and repeat, picking the right one (E12).

4. **BK-LC-01-4.** Read the permissions screen before you click Allow. It lists what Claude may do. Intuit, not this kit, decides that list.
   You'll know it worked when you have read it. Notice which items say create, edit, send, or delete. Those are what you will keep switched off.

5. **BK-LC-01-5.** Start a new chat and paste the standing instruction from `free/prompts.md` section 1, plus the line from section 9: "Use only the tools that read or search. Do not use any tool that creates, updates, sends, or deletes." Then ask a first question: "What is the cash balance on each bank account as of the last day of last month?"
   You'll know it worked when Claude answers with account names and amounts. Check the total against the QuickBooks [balance sheet](../glossary.md#balance-sheet). If Claude asks to run a tool that creates or sends something, click Deny (E14).

6. **BK-LC-01-6.** Make the safe choice stick. In Claude's connector settings for QuickBooks, look for a list of the tools. If each tool has a choice such as always allow, needs approval, or blocked, set every tool whose name suggests create, update, send, delete, or run to blocked. Leave the search and read tools on needs approval.
   You'll know it worked when the write tools show as blocked. If your settings do not list tools one by one, rely on the standing instruction and on clicking Deny, and never click Allow on anything that creates or sends.
   Menu names change. If this setting is missing on your screen, the Deny habit is the protection.

7. **BK-LC-01-7.** Test the trap that catches most people. Ask: "What is net income for last month on the profit and loss, and is it cash or [accrual basis](../glossary.md#accrual-basis)?" Then run the same report in QuickBooks on both bases and compare.
   You'll know it worked when you know which basis the connector uses. In one connector version we saw its profit and loss was [cash basis](../glossary.md#cash-basis) only, while the balance sheet was accrual basis. If yours differs from your QuickBooks screen, it's E15. Details are in guide BK-LC-03.

## What to do next

Go to BK-LC-03 for the habits that keep answers trustworthy. If you use ChatGPT instead, see BK-LC-02.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-LC-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

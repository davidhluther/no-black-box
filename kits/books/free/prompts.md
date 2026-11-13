# Questions to Ask Your Books

Paste-in [prompts](../glossary.md#prompt) (the messages you give an AI model) for your QuickBooks reports. They work in the free plans of ChatGPT, Claude, and Gemini, and they work the same way with the low-cost [connector](../glossary.md#connector). Nothing here asks the AI model to change anything. Every prompt only reads.

All names, amounts, and dates in the examples below are invented examples.

## How to use this pack

1. Export the report you need from QuickBooks (guide BK-FR-01) and open it in Google Sheets.
2. Start a new chat and paste the standing instruction first.
3. Paste the report's cells, or upload the file if your AI model accepts uploads.
4. Paste one question at a time. Check any number that matters against the QuickBooks screen before you act on it.

## 1. The standing instruction (paste this first, every chat)

```
You are helping a volunteer treasurer read QuickBooks reports. Rules:
- Work only from the report I paste. If a number is not in it, say "not in the report" and do not guess.
- Show the row or label each number came from.
- Label every figure as Books (from the report), Bank (only if I give you a bank figure), or Estimate (your arithmetic, with the arithmetic shown).
- Never suggest I create, edit, send, or delete anything in QuickBooks. Suggest what to look at or ask, and I will decide.
- Tell me the report's date range and whether it is cash basis or accrual basis. If the report does not say, ask me.
- Use plain words. Define any accounting term the first time you use it.
```

## 2. Cash questions

Use the [balance sheet](../glossary.md#balance-sheet) and the [general ledger](../glossary.md#general-ledger).

```
From this balance sheet, list every cash and bank account with its balance on the report date. Then list any account that looks like a holding account rather than a bank (for example Undeposited Funds) and say why it is not the same as bank cash.
```

```
My bank statement says [example: $30,500.00] for the operating checking account on [example: 09/30/2026]. The books say what for the same account on the same date? Give the difference and list the three most likely causes, in order, from the general ledger lines I pasted.
```

```
In this general ledger, find any entry in the account "Opening Balance Equity". For each one, show the date and amount, and tell me whether the same amount appears as the running balance of a bank account on that date. A match to the cent suggests the opening balance was counted twice.
```

```
Show me the last date there is any entry in each bank account. If one account has had no entries for more than 45 days, flag it. It may mean the bank connection stopped.
```

## 3. What we owe

```
From this balance sheet and this aged payables report, make a table of everything we owe: liabilities by account, the amount, and whether it is due within 30 days. Add a final row for the total due within 30 days.
```

```
List any liability account that has not changed in more than 90 days and whose balance is over [example: $1,000]. For each, name what it might be and what document would confirm it (a letter, an invoice, a statement).
```

```
List payroll-related accounts (wages, payroll taxes, retirement withholdings). Show the balance and the last entry date for each. A tax or withholding balance that never changes may mean it is not being paid or is not being entered.
```

## 4. Income and spending

```
From this profit and loss report, give the five largest income lines and the five largest expense lines with amounts and percent of total. Note anything that looks unusual for a small [food bank / salon / club].
```

```
Compare this month's profit and loss with the same report for last month, which I pasted second. List every line that moved by more than [example: 20%] and more than [example: $500]. Give the dollar change and percent. Do not explain causes you cannot see in the reports.
```

```
Are there any income lines that only have one entry this year? List them with the date and amount. One-time income can make a month look healthier than it is.
```

## 5. Spotting mistakes

```
Look through this general ledger for: (a) the same amount posted twice on the same date, (b) entries with no description, (c) round-number entries over [example: $5,000], and (d) entries dated after today. List each with date, account, and amount.
```

```
Which entries in this journal report are manual journal entries rather than bank, invoice, or bill transactions? List them with date, accounts used, and amount. Manual entries deserve a second look because nothing outside the books backs them up.
```

```
This profit and loss report is cash basis and this balance sheet is accrual basis. Explain in plain words why the net income on one will not equal the change in equity on the other, and tell me what to compare instead.
```

## 6. Restricted money

```
From this balance sheet and the grants list I pasted below, tell me how much of our cash is restricted. For each grant, give the amount received, the amount spent, and the amount left. Do not guess a grant's purpose. If it is not in what I pasted, say so.
```

## 7. How long will the cash last

```
Using the Monthly cash tab I pasted, work out the average net cash change over the last three months. Then tell me how many months the free cash lasts at that pace. Show the arithmetic. Free cash means cash now, minus restricted cash, minus bills committed but unpaid.
```

```
What single assumption would change the runway answer the most? Give me a version of the answer with that assumption 20% better and 20% worse.
```

## 8. Getting ready for a board meeting

```
Draft three plain-language sentences the treasurer could say aloud at the board meeting: where cash stands, the biggest change since last month, and the one thing to watch. Use only figures from the reports I pasted and label which report each came from.
```

```
Write a list of the five questions a careful board member is most likely to ask about these reports, with the answer I can give or the place I need to look.
```

## 9. Asking a connector (low-cost version)

When you use Intuit's connector, begin each chat with the standing instruction above, then add this line.

```
Use only the tools that read or search. Do not use any tool that creates, updates, sends, or deletes. If the only way to answer is a tool that changes something, tell me and stop.
```

Then ask the same questions, naming the date range each time. Check the first answer against the QuickBooks screen. See guide BK-LC-03.

## 10. After any answer

```
What would make your answer wrong? Name the two most likely reasons and what I would check in QuickBooks to find out.
```

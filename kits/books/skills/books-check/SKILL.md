---
name: books-check
description: Reads a QuickBooks Online company's books without ever changing them, to find why the books and the bank disagree, date a mystery entry, list an account line by line, and check audit history. Uses a small Python (a common programming language) program that sends only GET requests (messages that say "show me this" and cannot change anything), enforced in code with a self-test, or Intuit's QuickBooks connector (an add-on that lets an AI model read another service) with its write tools declined. Use when a treasurer or owner asks whether the cash balance is real, what is owed, when an entry was posted, or wants a QuickBooks report pulled for review.
---

# Books Check

Works in: Claude Code (full version). The recipes also work as plain instructions in Claude.ai or ChatGPT when the user pastes exported reports (see the kit's free and low-cost versions).

## The promise, and your part in it

This skill never changes the books. The program is a script (a small program saved as a text file) that sends GET requests only, and it enforces that in code. Your part:

- Run only the commands listed under "Commands" below. Never write a new network call, never use another HTTP method, never use `curl` against QuickBooks.
- If a QuickBooks connector (an add-on that lets an AI model read another service) is attached, call only tools that read, search, or report. Never call a tool that creates, updates, sends, voids, or deletes, even when the user asks. Say why and offer the read-only (able to look but not touch) route.
- Never print, log, echo, or ask for a client secret (the private password that goes with your Intuit setup), refresh token (a longer-lived pass that gets new short-lived ones), or password. If the user pastes one into the chat, tell them to replace it and do not repeat it.
- If the user asks for something that would change the books, stop, explain that this kit looks and never touches, and suggest they do it in QuickBooks themselves or with their bookkeeper.

## Settings

Read the user's `config.json` (copied from the kit's `config.example.json`) for the organization's name, fiscal year start, accounting method, and output folder. If it is missing, ask. Secrets are never in that file. They are environment variables (named settings stored on the computer outside any shared file): `QBO_CLIENT_ID`, `QBO_CLIENT_SECRET`, `QBO_REFRESH_TOKEN`, `QBO_REALM_ID`, and `QBO_ENV` (`production` or `sandbox`). Intuit's setup is in `references/intuit-app-setup.md`.

## Commands

Run from the folder holding `scripts/qbo_readonly.py`. Dates are yyyy-mm-dd.

```
python3 scripts/qbo_readonly.py selftest
python3 scripts/qbo_readonly.py check
python3 scripts/qbo_readonly.py pull ProfitAndLoss --start 2026-01-01 --end 2026-09-30 --method Accrual
python3 scripts/qbo_readonly.py query "select * from Deposit where TxnDate >= '2026-01-01'"
python3 scripts/qbo_readonly.py flatten books-check-output/<file>.json
python3 scripts/qbo_readonly.py bracket --account "Other Income" --start 2026-01-01 --end 2026-12-31
```

Run `selftest` first in every new session. If it does not print SELFTEST PASSED, stop. `pull` accepts these reports: ProfitAndLoss, ProfitAndLossDetail, BalanceSheet, GeneralLedger, JournalReport, TransactionList, TrialBalance, CashFlow, AgedReceivables, AgedReceivableDetail, AgedPayables, AgedPayableDetail. `--param key=value` adds a report option such as `account=123` or `summarize_column_by=Month`. `query` accepts SELECT statements only. Saved files hold names and amounts, so keep them in a private folder and never in a shared drive or email.

## Method

1. State the question, the date range, and the accounting method, either accrual basis (money counts when it is earned or owed) or cash basis (money counts when it moves in or out of the bank). Use one method per comparison.
2. Pull the smallest set of reports that can answer it.
3. Work in the flattened CSV (a plain text table that Google Sheets can open). Label every figure Books (from QuickBooks), Bank (a figure the user got from a statement), or Estimate (your arithmetic, shown).
4. Name what would make the answer wrong, and the one check the user can do on the QuickBooks screen.
5. Save the files with the pull date in the name and write one sentence per finding with its source file and line.

## Recipes

`references/recipes.md` has the full steps for each. In brief:

- Book-versus-bank cash check without statements: five tests on the general ledger (starting balance counted twice, payroll in the wrong account, last day the bank feed (the automatic download of bank transactions into QuickBooks) was worked, deposits booked to income while payments sit in Undeposited Funds (a holding account for payments not yet matched to a deposit), then add up the causes).
- Dating a posting: `bracket`, which narrows a profit and loss line by halves.
- Register (the line-by-line list for one account, with a running balance) extraction: a general ledger pull for one account, tied to the balance sheet (a snapshot of what is owned and owed on one date) movement.
- Audit history: entry creation times from queries; who-changed-what from the QuickBooks screens.
- Connector traps: `references/connector-traps.md`.

## When the user needs more than this can see

The accounting service's reports do not list who changed an entry, and some reports render slowly or lazily on screen. Say so, and give the screen route in `references/recipes.md` instead of guessing. A statement from the bank is the only proof of the real balance. This skill supports a reconciliation (matching every line on the statement to the books); it does not replace one.

## Example numbers

Every amount in this skill's files is an invented example. Never reuse them as findings.

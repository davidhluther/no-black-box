# Books Check Recipes

Every recipe only reads. All amounts and dates are invented examples.

Terms used here, in plain words. A general ledger (the list of every entry in the books, grouped by account) is the most complete report QuickBooks makes. A journal entry (a hand-made entry that moves money between accounts with no invoice or bank item behind it) is the kind most worth a second look. Accrual basis (counting money when it is earned or owed) counts money when earned or owed, and cash basis (counting money only when it moves in or out of the bank) counts it when it moves.

## 1. Pull and flatten

1. `selftest`, then `check`.
2. `pull BalanceSheet`, `pull ProfitAndLoss`, and `pull GeneralLedger` for the same dates and the same method.
3. `flatten` each saved file. Open the CSVs (a plain text table that Google Sheets can open) in a spreadsheet. Reports flatten to Kind, Section, and one column per report column. Saved queries flatten to one row per line, with `Line.LinkedTxn` empty where a line is not tied to another transaction.

## 2. Book-versus-bank cash check without statements

Use when the books and a bank figure (a verbal balance, an online screen) disagree, and statements are not yet in hand.

Setup. Pull `GeneralLedger` for the period and flatten it. Note the bank figure and its date, and who gave it.

1. Opening balance counted twice. Find entries in the Opening Balance Equity (a holding account QuickBooks creates for starting balances). For each, compare the amount with the bank account's own running balance on that date. A match to the cent is a sign the balance was already in the account, not proof.
2. Payroll in the wrong account. Sum payroll-provider journal entries credited to the old or closed bank account. Compare with that account's balance. A payroll that left the real bank but never reached its register (the line-by-line list for one account, with a running balance) makes the books look richer than the bank.
3. Last day the bank feed (the automatic download of bank transactions that someone approves or matches) was worked. A feed that stops is easy to miss. Sort each bank account's entries by date. A last entry weeks ago means everything since is missing.
4. Deposits entered twice. Undeposited Funds (a holding account for payments received but not yet matched to a bank deposit) should shrink when deposits are matched. Run `query "select * from Deposit where TxnDate >= '<start>' and TxnDate <= '<end>'"` and `flatten` it. Lines whose `Line.LinkedTxn` is empty were booked straight to income. If the same payments still sit in Undeposited Funds, income is counted twice.
5. Add the causes. Example: books $42,000.00, bank $30,500.00, gap $11,500.00. Test 1 finds a $9,800.00 opening-balance entry equal to the account's balance that day. Test 2 finds a $1,700.00 payroll credited to the old account. $9,800.00 plus $1,700.00 equals $11,500.00, so the gap is explained. Anything left is probably bills not yet entered. Label the remainder "unexplained, needs the statement".

Output. A short table of causes with amounts and the file and line each came from, then the remaining gap.

## 3. Dating an opaque posting by bracketing

Use when a profit and loss line holds an amount nobody can place in time and no journal-entry read is available.

1. `bracket --account "<exact line name>" --start <yyyy-mm-dd> --end <yyyy-mm-dd> --method <Accrual|Cash>`.
2. The script (a small program saved as a text file) pulls the profit and loss for the whole window, then the two halves, and keeps splitting any window whose amount is not zero until it reaches single days or runs out of its call limit.
3. Read the final list of windows. Example: $18,000.00 of Other Income in the year becomes $6,000.00 on 11/02/2026 and $12,000.00 on 11/23/2026.
4. Use each window's own total. Never use a month-by-month table from the same report, because tables can fail to add up to the line items.
5. Then look in QuickBooks, on the screen, at entries dated in those windows.

## 4. Register extraction

A register is the line-by-line list of everything in one account, with a running balance.

1. `query "select Id, Name, AccountType from Account where Name like '%<word>%'"` and read the Id.
2. `pull GeneralLedger --start <date> --end <date> --param account=<Id>` and `flatten`.
3. Check that the opening balance plus the movement in the CSV equals the account's balance on the balance sheet (a snapshot of what is owned and owed on one date) for the end date. Report any difference to the cent.

## 5. Audit history and late postings

The reports this skill is allowed to read do not say who changed an entry.

- When was it entered? `query "select * from JournalEntry where TxnDate >= '<start>'"`. Each entry carries a MetaData block with a creation time. An entry created months after its date is worth a question.
- Who changed it? On the QuickBooks screen, open the entry, scroll to the bottom, and open More, then Audit history. The Audit log under the gear icon filters by date and user. Browsing these changes nothing, as long as you close without saving.
- Finding an entry by amount. QuickBooks's own search box accepts an exact amount. A report row may not open when clicked; use search instead.

## 6. Connector recipes

When only a connector (an add-on that lets an AI model read another service) is available, call read tools only and see `connector-traps.md`. Date an entry by asking for the profit and loss line alone over successively narrower windows (recipe 3 by hand).

## 7. Labels and wording

Label every figure Books, Bank, or Estimate. Say "not found where I looked" rather than "does not exist". Give each claim its report, date range, and basis. End with what would make the finding wrong.

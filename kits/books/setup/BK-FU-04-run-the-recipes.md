# BK-FU-04: Run the Recipes

You will end with the checks an outside accountant would charge for: pulling the full books, comparing them with the bank, placing a mystery entry in time, and listing every line of one account. About 60 minutes the first time. Every command here only reads.

All amounts and dates in this guide are invented examples. Replace them with yours. Dates on the command line are written yyyy-mm-dd because QuickBooks requires that form.

Before each session, open a [terminal](../glossary.md#terminal) (a window for typed commands), load your settings, and move into your folder:

```
source ~/.config/books-check/env.sh && cd ~/Desktop/books-check
```

## Steps

1. **BK-FU-04-1.** Pull the three core reports and turn them into spreadsheet files. A [balance sheet](../glossary.md#balance-sheet) is a snapshot of what you own and owe, a [profit and loss report](../glossary.md#profit-and-loss-report) shows income and spending over a period, and the [general ledger](../glossary.md#general-ledger) lists every entry by account.

   ```
   python3 qbo_readonly.py pull BalanceSheet --start 2026-01-01 --end 2026-09-30 && python3 qbo_readonly.py pull ProfitAndLoss --start 2026-01-01 --end 2026-09-30 && python3 qbo_readonly.py pull GeneralLedger --start 2026-01-01 --end 2026-09-30
   ```

   Reports come on [accrual basis](../glossary.md#accrual-basis) unless you add `--method Cash`. Use the same one every time and write it down. Each pull saves a [JSON](../glossary.md#json) file (a text format programs use to pass data) in the folder `books-check-output`. Turn each into a [CSV](../glossary.md#csv) (a table you can open in Google Sheets):

   ```
   python3 qbo_readonly.py flatten books-check-output/YYYY-MM-DD-GeneralLedger-2026-01-01_to_2026-09-30.json
   ```

   You'll know it worked when a .csv file sits beside each .json file and opens in Google Sheets with account sections and amounts. Replace YYYY-MM-DD with the day you ran it. If a report is empty, it's E38.

2. **BK-FU-04-2.** Run the book-versus-bank cash check. Get your bank statement balance for the same date, then open the general ledger CSV in Google Sheets and run these five tests on your main bank account, in order.

   - Test a, opening balance twice. Filter the Section column for [Opening Balance Equity](../glossary.md#opening-balance-equity) (a holding account QuickBooks creates for starting balances). For each entry, compare its amount with the bank account's own running balance on that date. A match to the cent is a sign, not proof, that the starting balance was already in the account and was entered again.
   - Test b, payroll in the wrong account. Add up payroll-provider journal entries credited to an old or closed bank account and compare the total with that account's balance.
   - Test c, the last day anyone worked the [bank feed](../glossary.md#bank-feed) (the automatic download of bank transactions). Sort each bank account's entries by date. A last entry weeks ago means the feed stopped, and everything since is missing.
   - Test d, deposits entered twice. In QuickBooks, [Undeposited Funds](../glossary.md#undeposited-funds) (a holding account for payments not yet matched to a deposit) should empty when deposits are matched. A balance that never shrinks may mean the deposit was booked straight to income. Run the query below to list deposits, and step 4 shows how to read the result.
   - Test e, add it up. Invented example: the books say $42,000.00, the bank says $30,500.00, and the gap is $11,500.00. Test a finds an opening balance entry of $9,800.00 that equals the account's balance that day. Test b finds a $1,700.00 payroll credited to the old account that never reached the main [register](../glossary.md#register). Together $9,800.00 and $1,700.00 make $11,500.00, so the gap is explained.

   ```
   python3 qbo_readonly.py query "select * from Deposit where TxnDate >= '2026-01-01' and TxnDate <= '2026-09-30'"
   ```

   You'll know it worked when you can write one sentence per cause with its amount. Whatever remains unexplained is probably bills nobody has entered. Only a statement from the bank settles it, and nothing in this kit replaces a [reconciliation](../glossary.md#reconciliation) (matching every line on the statement to the books).

3. **BK-FU-04-3.** Place a mystery posting in time by bracketing it. Say the profit and loss shows $18,000.00 of "Other Income" in 2026 and nobody knows when it was entered. The [script](../glossary.md#script) splits the year in halves and keeps splitting where the amount is not zero.

   ```
   python3 qbo_readonly.py bracket --account "Other Income" --start 2026-01-01 --end 2026-12-31
   ```

   You'll know it worked when the script prints a tree of windows and ends with a list such as `2026-11-02 to 2026-11-02: 6000.00`. It uses each window's own total, never a month-by-month table, because tables can fail to add up. The default limit is 40 report requests; raise it with --max-calls only if you need to. If the numbers look odd, it's E39.

4. **BK-FU-04-4.** List every line of one account (a [register](../glossary.md#register), the line-by-line list with a running balance). First find the account's ID with a query:

   ```
   python3 qbo_readonly.py query "select Id, Name, AccountType from Account where Name like '%Checking%'"
   ```

   Then pull the general ledger for that account only, using its ID in place of 123:

   ```
   python3 qbo_readonly.py pull GeneralLedger --start 2026-01-01 --end 2026-09-30 --param account=123
   ```

   You'll know it worked when the CSV shows one account with a balance column that agrees with the balance sheet movement over the same dates. For the deposits query from step 2, flatten it the same way. In the CSV, a Line.LinkedTxn cell that is empty means that deposit line is not tied to a payment. Those lines are the ones to look at.

5. **BK-FU-04-5.** Find entries posted long after their date. Backdated entries are normal at year end and worth a look otherwise.

   ```
   python3 qbo_readonly.py query "select * from JournalEntry where TxnDate >= '2026-01-01'"
   ```

   You'll know it worked when each entry's file record shows a date on the entry and a separate "MetaData" block with a creation time. A creation time months after the entry date is the thing to ask about.

6. **BK-FU-04-6.** For who made or edited an entry, use the QuickBooks screen, not the script. Open the entry in QuickBooks, scroll to the bottom, and open More, then Audit history. QuickBooks also has an Audit log under the gear icon (Settings) where you can filter by date and user. These screens look and do not change anything, as long as you click Cancel or close without saving.
   You'll know it worked when you can see who added the entry and when. The script cannot read this, because the accounting service does not offer it in the reports this kit allows.

7. **BK-FU-04-7.** Save your work. Copy the output folder's CSV files into a private folder with the pull date in the name, and write one sentence per finding. Do not put the JSON files in a shared drive or an email, since they hold names and amounts.
   You'll know it worked when each finding in your notes points to a file, a date, and a line.

## What to do next

Turn what you found into a monthly report with the `treasurer-report` skill, or the free templates in `free/treasurer-report-template.md`.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-FU-04-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
> The full version's check-up is a command. Run `python3 support/doctor.py books` and copy the support code it prints.

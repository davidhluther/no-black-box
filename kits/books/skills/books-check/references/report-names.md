# Report Names and Useful Options

Names accepted by `qbo_readonly.py pull`. Option names go through `--param key=value` and are passed to QuickBooks as written. Option support varies by report, so if a report ignores one, try another pull.

| Report | What it shows | Useful options |
|---|---|---|
| ProfitAndLoss | Income and expenses over a period | `summarize_column_by=Month` (the breakdown table may not tie to line items) |
| ProfitAndLossDetail | Every entry behind each profit and loss line | `account`, `account_type` |
| BalanceSheet | What is owned and owed on one date | `summarize_column_by` |
| GeneralLedger | Every entry, grouped by account, in date order | `account` (an account Id) |
| JournalReport | Every journal entry (a hand-made entry that moves money between accounts) | |
| TransactionList | Transactions in date order | `account` |
| TrialBalance | Balance of every account on a date | |
| CashFlow | Cash in and out by activity | |
| AgedReceivables, AgedReceivableDetail | What customers owe, by age | |
| AgedPayables, AgedPayableDetail | What the organization owes, by age | |

Always pass `--method Accrual` or `--method Cash`, and say which in the finding. Dates are yyyy-mm-dd.

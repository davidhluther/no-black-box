# Connector Traps

Seen in one QuickBooks connector (an add-on that lets an AI model read another service) for Claude in October 2026. Intuit updates its connector, so test each trap on the version you have before relying on it. Intuit's own announcement says the connector can also create, send, and delete invoices and estimates; this skill never uses those tools.

1. The profit and loss may use only cash basis (money counts when it moves in or out of the bank). In the version tested, the profit and loss tool was cash basis while the balance sheet (a snapshot of what is owned and owed on one date) was accrual basis (counting money when it is earned or owed). They tie only through the change in accounts receivable (what customers owe). Never subtract one from the other. Test by running the same report in QuickBooks on both bases.
2. Monthly breakdown tables may not tie. In the version tested, the month-by-month table did not add up to the line items. Use each window's own line total.
3. No journal-entry or register (the line-by-line list for one account, with a running balance) tool. A connector may have no way to list every journal entry (a hand-made entry that moves money between accounts) line or an account register. Use a report export or the `books-check` script (a small program saved as a text file) for those.
4. Dates matter. State exact start and end dates in every request. "This year" can mean a different range than you expect.
5. Write tools exist. Decline any request to create, update, send, or delete. Block those tools in the connector's settings if the settings allow it.
6. Wrong company. A login that manages several companies may attach the wrong one. Check the company name in the first answer.
7. Output filtering. If the connector returns more rows than you can read, filter with a short script on the saved text. Do not paste unfiltered private data into a shared chat.

Connector recipes that rely on these traps: dating a posting by narrowing the profit and loss window (recipes.md, section 3), and checking an aged receivables report against the balance sheet.

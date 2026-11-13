# BK-LC-03: Safe Habits and Connector Traps

You will end with a short routine that keeps [connector](../glossary.md#connector) answers trustworthy and a way to place a mystery entry in time. About 30 minutes. It uses only questions.

The same habits apply to the Claude connector (BK-LC-01) and the ChatGPT plugin (BK-LC-02). The traps below were seen in one connector version in October 2026. Intuit updates its connector, so test each one on yours before you rely on it.

## Steps

1. **BK-LC-03-1.** Ask the questions pack, not free-form requests. Open `free/prompts.md`, paste the standing instruction, then ask sections 2, 3, and 7 in your connected chat.
   You'll know it worked when each answer names the report and date range it used. If it does not, ask: "Which report and which dates did you use?" (E17).

2. **BK-LC-03-2.** Always say the date range. Ask for "01/01/2026 through 09/30/2026", never "this year".
   You'll know it worked when the date range in the answer matches the one you typed. A mismatch is the most common reason for an answer that disagrees with the QuickBooks screen (E17).

3. **BK-LC-03-3.** Learn the cash-basis trap. Ask for the profit and loss for a period, then run the same report in QuickBooks on [cash basis](../glossary.md#cash-basis) and on [accrual basis](../glossary.md#accrual-basis). The two differ because accrual basis counts money when it is earned or owed, and [cash basis](../glossary.md#cash-basis) counts it when it moves.
   You'll know it worked when you can say which basis the connector used. If the connector is cash only while the [balance sheet](../glossary.md#balance-sheet) is accrual, the two will not tie, except through the change in what people owe you (accounts receivable). Never subtract one from the other. See E15.

4. **BK-LC-03-4.** Do not trust the monthly breakdown table. If the connector's profit and loss shows a month-by-month table, compare it with the line totals for a single month asked for on its own.
   You'll know it worked when you use the single-window total. In the version we tested, the monthly table did not agree with the individual line items.

5. **BK-LC-03-5.** Date an unknown entry by narrowing the window. Say a profit and loss line shows an amount you cannot explain, for example $18,000 of other income in a year. Ask for that line alone for the whole year, then for each half, then each month, then each half-month, then each week. When a window's total drops to zero, the entry is in the other window. Stop when you reach a few days. An invented example: $18,000 in the year, $0 in the first half, $18,000 in the second half, $0 in July through September, and then $6,000 and $12,000 in two different weeks of November.
   You'll know it worked when you can say "$6,000 posted the week of 11/02/2026 and $12,000 the week of 11/23/2026." Then look at QuickBooks for entries on those dates. A connector has no list of every [journal entry](../glossary.md#journal-entry), so this narrowing is the workaround.

6. **BK-LC-03-6.** Know what the connector cannot show. It cannot list every journal entry line or an account [register](../glossary.md#register) (a line-by-line list with a running balance). For those, use a report export (BK-FR-01) or the full version (BK-FU-04).
   You'll know it worked when you stop asking the connector for things it has no tool for and switch to an export.

7. **BK-LC-03-7.** Every month, run the routine in `free/monthly-routine-checklist.md`, using the connector for the pulling and the sheet from guide BK-FR-02 for the figures.
   You'll know it worked when your cash sheet's numbers each have a source you could show someone.

## What to do next

If a question needs entry-level detail, the full version is the next step: BK-FU-01.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-LC-03-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

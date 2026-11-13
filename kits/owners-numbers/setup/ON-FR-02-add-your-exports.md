# ON-FR-02 Add Your Exports

You will bring last month's real numbers into the Sheet. Work on one month at first. You can add history later.

1. **ON-FR-02-1.** [Export](../glossary.md#export) your sales for last month from your [point-of-sale system](../glossary.md#point-of-sale-system) (the register or app where you ring up sales). Look for Reports, then Sales or Items, then Export. Choose [CSV](../glossary.md#csv) and a date range that covers the whole month plus the month before, which lets the scorecard compare them.
   You'll know it worked when you have a file whose name ends in .csv. If your system only exports a PDF, ask its support for an item-level CSV, or copy the rows by hand.
2. **ON-FR-02-2.** Download your bank's transactions for the same two months as a CSV. Open the file in Sheets and delete any column that holds an account number, a card number or a name. The kit only needs date, description and amount.
   You'll know it worked when no column holds an account number. If you cannot tell, treat it as E33 and delete the column.
3. **ON-FR-02-3.** If you take bookings, export a booking report from your booking tool with date, service, staff, booked minutes, status and client. If you do not take bookings, skip this step and step 7.
   You'll know it worked when each row has a status such as completed, no_show or canceled. The words must match those three exactly, so rename them in the file if they differ.
4. **ON-FR-02-4.** Paste the sales export into the Sales [tab](../glossary.md#tab) under its header row, in this column order: date, item, category, quantity, net_sales, client_id. Net sales is the total for that line. If your export has different column names, rearrange the columns to match, and leave client_id empty if your system does not give one.
   You'll know it worked when the Sales tab's first row is the header and the rows below are your sales. If the header row is wrong, it's E02. If the tab is empty, it's E05.
5. **ON-FR-02-5.** Paste the bank rows into the Bank tab under its header row, in this column order: date, description, amount, category. Money in is positive and money out is negative. Leave category empty for now.
   You'll know it worked when negative numbers show for payments. If the tab has no rows, it's E06.
6. **ON-FR-02-6.** Fill in the category column on every Bank row, using only these words: sales_deposit, other_income, cogs, supplies, payroll, rent, utilities, software, insurance, marketing, loan_payment, tax, other_fixed, other_variable, owner_draw, transfer. Cogs means the cost of the goods you sell. Mark a move between your own accounts as transfer and your own pay as owner_draw. Neither counts as a business cost. A free [AI model](../glossary.md#ai-model) can suggest tags (see prompt 1 in [prompts.md](../free/prompts.md)), but you check each one.
   You'll know it worked when the column has no blanks. Blank rows are E07 and a word not on the list is E08.
7. **ON-FR-02-7.** Paste the booking rows into the Bookings tab in this order: date, service, staff, booked_minutes, status, client_id, price.
   You'll know it worked when the status column holds only completed, no_show and canceled. An empty tab is allowed but it's E11 as a reminder that customer and capacity numbers stay empty.
8. **ON-FR-02-8.** Make sure dates are real dates. Click a date cell. Real dates sit on the right side of the cell. Text dates sit on the left. If they sit on the left, select the date column, choose Format, then Number, then Date.
   You'll know it worked when all dates in the column align right. Text dates are E09.
9. **ON-FR-02-9.** Run Kit help, then Run [check-up](../glossary.md#check-up).
   You'll know it worked when every line about the Sales, Bank and Bookings tabs says OK. Any FIX line names a code. Look it up in [fixes.md](../fixes.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-FR-01-3). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

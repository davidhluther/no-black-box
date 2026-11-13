# ON-FU-02 Prepare Your Four Files

You will gather your own [exports](../glossary.md#export) into one folder, using the same layouts as the free version.

1. **ON-FU-02-1.** Make a folder named owners-numbers-data in a place you can find again, such as Documents.
   You'll know it worked when the folder shows in your file browser.
2. **ON-FU-02-2.** Export sales for the month and the month before from your [point-of-sale system](../glossary.md#point-of-sale-system) as a [CSV](../glossary.md#csv). Arrange the columns as date, item, category, quantity, net_sales, client_id. Save it as sales.csv in the folder.
   You'll know it worked when the first line of the file is exactly `date,item,category,quantity,net_sales,client_id`. A missing column is E21.
3. **ON-FU-02-3.** Download bank rows for the same two months. Delete any account-number or name column. Add a category column using only the words sales_deposit, other_income, cogs, supplies, payroll, rent, utilities, software, insurance, marketing, loan_payment, tax, other_fixed, other_variable, owner_draw and transfer. Save it as bank.csv with the columns date, description, amount, category.
   You'll know it worked when negative amounts are payments and every row has a category. The [script](../glossary.md#script) reports uncategorized rows but never guesses. If an account number slipped through, remove it before going on. That is E33.
4. **ON-FU-02-4.** If you take bookings, save a booking report as bookings.csv with the columns date, service, staff, booked_minutes, status, client_id, price. Status is completed, no_show or canceled.
   You'll know it worked when the status column holds only those three words. Skip the file if you take no bookings. The script handles that.
5. **ON-FU-02-5.** Copy `assets/example/settings.csv` from the owner-scorecard folder into your folder. Edit the business_name, month_start and month_end, then fill what you know in cash_on_hand, prior_cash_on_hand and capacity_minutes. Leave unknown values blank.
   You'll know it worked when month_start and month_end use the form 2026-09-01. A date the script cannot read is E23.

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

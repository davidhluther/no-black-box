# Cash and Runway Sheet: Layout and Formulas

The monthly cash-and-[runway](../glossary.md#runway) sheet (how many months you can keep going at the current pace) is seven [tabs](../glossary.md#tab) (the labeled pages along the bottom of a Google Sheet). Each tab's layout is a [CSV](../glossary.md#csv) file (a plain table saved as text) in the `cash-runway-template` folder beside this page. The file name is the tab name. All amounts in the files are invented examples.

If a formula arrives as plain text after import, type it in again from the lists below. Google Sheets formulas always start with an equals sign.

## Tab names, exactly as written

`Settings`, `Accounts`, `Commitments`, `Monthly cash`, `Runway`, `QB Profit and Loss`, `QB Balance Sheet`

The [check-up](../glossary.md#check-up) button looks for these names. A different spelling or capital letter counts as missing (fix E04).

## Settings (cells B2 to B7 are required)

| Row | Setting | What to enter |
|---|---|---|
| 2 | Organization name | Your organization's name |
| 3 | Fiscal year start month | A number from 1 to 12 |
| 4 | Reserve target in months | For example 3 |
| 5 | Minimum cash floor | A dollar amount below which you want a warning |
| 6 | First month shown | The first day of the first month, yyyy-mm-dd |
| 7 | Opening cash balance | Total cash the day before that month, from your bank statements |

## Accounts

Columns: Account, Kind, Restricted, Books balance, Bank balance, Difference, As of, Note. One row per bank or holding account. Type Yes or No in Restricted.

Difference (F2 and down): `=IF(OR(D2="",E2=""),"",D2-E2)`

A Difference that is not zero means the books and the bank disagree on that date. It is the signal to run the book-versus-bank check in `prompts.md` section 2.

## Commitments

Columns: Item, Amount, Due, Restricted use, Note. List money that is owed or promised but not yet paid: the next payroll, a tax notice, deposits held for others, a repair you approved. Amounts are positive numbers.

## Monthly cash

Columns: Month, Cash in, Cash out, Net, Ending cash, Note. Twelve rows. Type Cash in and Cash out as positive numbers, taken from the bank statement or the QuickBooks bank [register](../glossary.md#register).

| Cell | Formula |
|---|---|
| Month, row 2 | `=TEXT(EDATE(Settings!$B$6,0),"yyyy-mm")` |
| Month, row 3 | `=TEXT(EDATE(Settings!$B$6,1),"yyyy-mm")`, and so on down to row 13 |
| Net, row 2 | `=IF(AND(B2="",C2=""),"",B2-C2)` |
| Ending cash, row 2 | `=IF(D2="","",Settings!$B$7+D2)` |
| Ending cash, row 3 | `=IF(D3="","",E2+D3)`, copied down |

## Runway

| Row | Measure | Formula in column B |
|---|---|---|
| 2 | Cash now | `=LOOKUP(9.99E+307,'Monthly cash'!E2:E100)` |
| 3 | Restricted cash | `=SUMIF(Accounts!C2:C100,"Yes",Accounts!D2:D100)` |
| 4 | Committed but unpaid | `=SUM(Commitments!B2:B100)` |
| 5 | Free cash | `=B2-B3-B4` |
| 6 | Average monthly net, last three months | `=IFERROR(AVERAGE(OFFSET('Monthly cash'!D1,COUNT('Monthly cash'!D2:D100)-2,0,3,1)),"")` |
| 7 | Average monthly cash out, last three months | the same formula using column C |
| 8 | Months of runway | `=IF(B6="","",IF(B6>=0,"Not shrinking",B5/-B6))` |
| 9 | Months of reserve | `=IF(OR(B7="",B7=0),"",B5/B7)` |
| 10 | Reserve target in months | `=Settings!B4` |
| 11 | Gap to target (months) | `=IF(B9="","",B9-B10)` |
| 12 | Months until cash falls below the floor | `=IF(B6="","",IF(B6>=0,"Not shrinking",MAX(0,(B2-Settings!B5)/-B6)))` |

Free cash is a rough measure. It treats all cash on the Monthly cash tab as one pile and subtracts restricted balances and commitments. It does not know about prepaid income you still owe in service, such as tuition paid for months not yet taught. List those on the Commitments tab if they matter.

## QB Profit and Loss and QB Balance Sheet

These two tabs are landing pads. Paste a QuickBooks export below row 2 (guide BK-FR-01). Nothing in the formulas depends on them. They exist so you can ask an AI model about the report and look at the same figures yourself.

## Reading the example

The example rows show an organization that takes in a little less each month than it spends. The average net over the last three months is negative, so Months of runway shows a number. If your average net is zero or better, the cell shows "Not shrinking" instead.

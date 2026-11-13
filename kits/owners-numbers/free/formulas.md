# Formulas for the Owner's Scorecard Sheet

This page spells out every [formula](../glossary.md#formula) in the free version, so you can type them yourself, check them, or change them. The files in `templates/` already contain them, which means a [formula](../glossary.md#formula) in this page and the one in your [Google Sheets](../glossary.md#google-sheets) cell are the same text.

You need six [tabs](../glossary.md#tab) (the labeled pages along the bottom of a spreadsheet), named exactly Settings, Sales, Bank, Bookings, Scorecard and [Metrics](../glossary.md#metric). The first four hold data and the last two hold results.

## The basis rule

Every result carries a basis, either "actual" or "[what-if](../glossary.md#what-if)". A result is actual only when every input came from your own numbers or your own [exports](../glossary.md#export). If an input cell on Settings is blank, the sheet borrows the example value beside it and marks the result "what-if". A [what-if](../glossary.md#what-if) shows how the math works. It is never a [finding](../glossary.md#finding) about your business, and you should not quote it as one.

## The four data tabs

Paste your exports under these headers, keeping the column order. Dates must be real dates (Google Sheets right-aligns a real date).

| Tab | Columns, in order | Where it comes from |
|---|---|---|
| Sales | date, item, category, quantity, net_sales, client_id | your [point-of-sale system](../glossary.md#point-of-sale-system) export. Net sales is the line total |
| Bank | date, description, amount, category | your bank's [CSV](../glossary.md#csv) download. Money in is positive. You fill in the category |
| Bookings | date, service, staff, booked_minutes, status, client_id, price | your booking report. Status is completed, no_show or canceled |
| Settings | name, your_value, example_value, used_value, basis | the table below |

Bank categories the formulas know about are sales_deposit, other_income, cogs, supplies, payroll, rent, utilities, software, insurance, marketing, loan_payment, tax, other_fixed, other_variable, owner_draw and transfer. A transfer between your own accounts and an owner draw are never counted as operating costs.

## Settings tab

Column D (used_value) is `=IF(B5="",C5,B5)` in row 5 and copied down to row 29, and column E (basis) is `=IF(B5="","what-if","actual")` in the same way. Rows 8 to 10 start with a formula in column B that reads your own exports from the Scorecard tab, so they come out actual as soon as your data is in.

| Row | name | example_value | what to enter |
|---|---|---|---|
| 2 | business_name |  | Your business name. |
| 3 | month_start |  | First day of the month you are reviewing (a real date). |
| 4 | month_end |  | Last day of that month. |
| 5 | cash_on_hand | 15000 | Cash in the bank on the last day of the month. Leave blank if you do not know. |
| 6 | prior_cash_on_hand | 15500 | Cash in the bank a month earlier. |
| 7 | capacity_minutes | 9600 | Minutes of work you could have booked in the month. Chairs or rooms times open minutes. |
| 8 | price_per_sale | 60 | Average price of one sale. Fills itself from your sales export. |
| 9 | variable_cost_per_sale | 18 | What one more sale costs directly. Fills itself from your exports. |
| 10 | fixed_costs_monthly | 7200 | Costs that land every month no matter what you sell. Fills itself from your bank categories. |
| 11 | overhead_pool | 3000 | Shared costs (rent, software) you want to spread across lines. |
| 12 | allocation_base_total | 400 | The total of what you spread them over, such as all booked hours. |
| 13 | hours_used_by_line | 120 | How much of that total one service line used. |
| 14 | line_direct_cost | 1500 | Direct cost of that line (supplies, commission). |
| 15 | line_revenue | 7200 | Revenue from that line. |
| 16 | annual_margin_per_customer | 420 | What one customer earns you in a year after their own costs. |
| 17 | retention_rate | 0.7 | The share of customers who come back year to year, from 0 to 0.99. |
| 18 | hire_monthly_cost | 3600 | Monthly wage plus taxes and benefits for a possible hire. |
| 19 | hire_added_contribution | 4800 | Extra contribution a month that hire makes possible. |
| 20 | hire_onboarding_cost | 2400 | One-time cost to hire and train. |
| 21 | current_assets | 16000 | Cash, money owed to you and stock on hand. |
| 22 | current_liabilities | 9000 | Bills and loan payments due within a year. |
| 23 | days_inventory | 30 | Average days stock sits before it sells. |
| 24 | days_receivable | 10 | Average days customers take to pay you. |
| 25 | days_payable | 20 | Average days you take to pay suppliers. |
| 26 | price_change_pct | 0.05 | The price change you want to test, as a decimal. 0.05 is a 5 percent increase. |
| 27 | assumed_volume_change | -0.04 | The volume change you assume afterward. -0.04 is four percent fewer sales. |
| 28 | baseline_units | 180 | Sales per month before the change. |
| 29 | target_margin | 0.6 | The [margin](../glossary.md#margin) you wish each sale had, as a decimal. |

## Scorecard tab

Column A is the label, B the formula, C the basis and D a plain reading. Row numbers matter, because other tabs point at them.

| Row | Label | Formula in column B | Basis in column C |
|---|---|---|---|
| 1 | Verdict | `=IF(B8>=0,"The month paid for itself","The month ran short")&", with "&TEXT(ABS(B8),"$#,##0")&IF(B8>=0," left over"," missing")&" after operating costs."` |  |
| 2 | Month start | `=Settings!D3` |  |
| 3 | Month end | `=Settings!D4` |  |
| 5 | Money in | `=SUMIFS(Bank!C:C,Bank!C:C,">0",Bank!A:A,">="&Settings!D3,Bank!A:A,"<="&Settings!D4,Bank!D:D,"<>transfer")` | actual |
| 6 | Operating costs | `=-SUMIFS(Bank!C:C,Bank!C:C,"<0",Bank!A:A,">="&Settings!D3,Bank!A:A,"<="&Settings!D4,Bank!D:D,"<>transfer",Bank!D:D,"<>owner_draw")` | actual |
| 7 | Owner draws | `=-SUMIFS(Bank!C:C,Bank!A:A,">="&Settings!D3,Bank!A:A,"<="&Settings!D4,Bank!D:D,"owner_draw")` | actual |
| 8 | Net operating | `=B5-B6` | actual |
| 9 | Cash on hand | `=Settings!D5` | `=Settings!E5` |
| 10 | Change in cash | `=Settings!D5-Settings!D6` | `=Settings!E5` |
| 11 | [Runway](../glossary.md#runway) in months | `=IF(B6-B5>0,Settings!D5/(B6-B5),"funded itself")` | `=Settings!E5` |
| 12 | Sales from the point-of-sale export | `=SUMIFS(Sales!E:E,Sales!A:A,">="&Settings!D3,Sales!A:A,"<="&Settings!D4)` | actual |
| 13 | Sales last month | `=SUMIFS(Sales!E:E,Sales!A:A,">="&EDATE(Settings!D3,-1),Sales!A:A,"<"&Settings!D3)` | actual |
| 14 | Sales change | `=IF(B13=0,"n/a",B12/B13-1)` | actual |
| 15 | Deposits minus sales | `=B5-B12` | actual |
| 17 | Sales counted | `=SUMIFS(Sales!D:D,Sales!A:A,">="&Settings!D3,Sales!A:A,"<="&Settings!D4)` | actual |
| 18 | Average sale | `=IF(B17=0,"",B12/B17)` | actual |
| 19 | Cost of goods | `=-SUMIFS(Bank!C:C,Bank!A:A,">="&Settings!D3,Bank!A:A,"<="&Settings!D4,Bank!D:D,"cogs")` | actual |
| 20 | [Variable costs](../glossary.md#variable-cost) | `=-SUMPRODUCT(SUMIFS(Bank!C:C,Bank!D:D,{"cogs";"supplies";"tax";"other_variable"},Bank!A:A,">="&Settings!D3,Bank!A:A,"<="&Settings!D4))` | actual |
| 21 | [Variable cost](../glossary.md#variable-cost) per sale | `=IF(B17=0,"",B20/B17)` | actual |
| 22 | [Fixed costs](../glossary.md#fixed-cost) | `=-SUMPRODUCT(SUMIFS(Bank!C:C,Bank!D:D,{"rent";"utilities";"software";"insurance";"loan_payment";"payroll";"marketing";"other_fixed"},Bank!A:A,">="&Settings!D3,Bank!A:A,"<="&Settings!D4))` | actual |
| 23 | Gross margin | `=IF(B12=0,"n/a",(B12-B19)/B12)` | actual |
| 24 | Payroll as share of sales | `=IF(B12=0,"n/a",-SUMIFS(Bank!C:C,Bank!A:A,">="&Settings!D3,Bank!A:A,"<="&Settings!D4,Bank!D:D,"payroll")/B12)` | actual |
| 25 | Kept by each average sale | `=Settings!D8-Settings!D9` | `=IF(COUNTIF(Settings!E8:E9,"what-if")>0,"what-if","actual")` |
| 26 | Share of price kept | `=IF(Settings!D8=0,"n/a",B25/Settings!D8)` | `=C25` |
| 27 | [Break-even](../glossary.md#break-even) sales dollars | `=IF(B25>0,Settings!D10/B26,"no break-even")` | `=IF(COUNTIF(Settings!E8:E10,"what-if")>0,"what-if","actual")` |
| 29 |  | `=QUERY(Sales!A:E,"select B, sum(E) where A >= date '"&TEXT(Settings!D3,"yyyy-mm-dd")&"' and A <= date '"&TEXT(Settings!D4,"yyyy-mm-dd")&"' group by B order by sum(E) desc limit 5 label sum(E) ''",0)` |  |
| 36 | Bookings this month | `=COUNTIFS(Bookings!A:A,">="&Settings!D3,Bookings!A:A,"<="&Settings!D4)` | actual |
| 37 | No-show rate | `=IF(B36=0,"n/a",COUNTIFS(Bookings!A:A,">="&Settings!D3,Bookings!A:A,"<="&Settings!D4,Bookings!E:E,"no_show")/B36)` | actual |
| 38 | Cancellation rate | `=IF(B36=0,"n/a",COUNTIFS(Bookings!A:A,">="&Settings!D3,Bookings!A:A,"<="&Settings!D4,Bookings!E:E,"canceled")/B36)` | actual |
| 39 | Clients served | `=IFERROR(COUNTA(UNIQUE(FILTER(Bookings!F2:F5000,(Bookings!A2:A5000>=Settings!D3)*(Bookings!A2:A5000<=Settings!D4)*(Bookings!E2:E5000="completed")))),0)` | actual |
| 40 | New clients | `=B39-B41` | actual |
| 41 | Returning clients | `=IFERROR(COUNTA(UNIQUE(FILTER(Bookings!F2:F5000,(Bookings!A2:A5000>=Settings!D3)*(Bookings!A2:A5000<=Settings!D4)*(Bookings!E2:E5000="completed")*ISNUMBER(MATCH(Bookings!F2:F5000,FILTER(Bookings!F2:F5000,(Bookings!A2:A5000<Settings!D3)*(Bookings!E2:E5000="completed")),0))))),0)` | actual |
| 42 | Completed booked minutes | `=SUMIFS(Bookings!D:D,Bookings!E:E,"completed",Bookings!A:A,">="&Settings!D3,Bookings!A:A,"<="&Settings!D4)` | actual |
| 43 | Lost minutes | `=SUMIFS(Bookings!D:D,Bookings!E:E,"no_show",Bookings!A:A,">="&Settings!D3,Bookings!A:A,"<="&Settings!D4)+SUMIFS(Bookings!D:D,Bookings!E:E,"canceled",Bookings!A:A,">="&Settings!D3,Bookings!A:A,"<="&Settings!D4)` | actual |
| 44 | [Capacity use](../glossary.md#capacity-use) | `=IF(Settings!D7=0,"n/a",B42/Settings!D7)` | `=Settings!E7` |
| 46 | The one thing | `=IF(B8<0,"Cash. Operating costs ran past money in.",IF(AND(ISNUMBER(B37),B37>0.06),"No-shows and cancellations.",IF(AND(ISNUMBER(B44),B44<0.6),"Open capacity.","Gross margin. Watch whether it holds.")))` | actual |

Row 28 labels the top five items. The formula in A29 uses `QUERY`, a Google Sheets function that groups and sorts a range, and fills five rows below it. Rows 30 to 34 stay empty so it can spill.

## Metrics tab

This tab holds the whole [metric library](metric-library.md). Column A is the metric, B the formula, C the basis and D a plain reading.

| Row | Metric | Formula in column B | Basis in column C |
|---|---|---|---|
| 2 | Unit contribution | `=Settings!D8-Settings!D9` | `=IF(COUNTIF(Settings!E8:E9,"what-if")>0,"what-if","actual")` |
| 3 | Contribution ratio | `=IF(Settings!D8=0,"n/a",B2/Settings!D8)` | `=C2` |
| 4 | Break-even sales count | `=IF(B2>0,Settings!D10/B2,"no break-even")` | `=IF(COUNTIF(Settings!E8:E10,"what-if")>0,"what-if","actual")` |
| 5 | Break-even sales dollars | `=IF(B2>0,Settings!D10/B3,"no break-even")` | `=C4` |
| 6 | Price move break-even volume shift | `=IF((B2+Settings!D8*Settings!D26)>0,-Settings!D8*Settings!D26/(B2+Settings!D8*Settings!D26),"no volume recovers it")` | `=IF(COUNTIF(Settings!E8:E9,"what-if")+COUNTIF(Settings!E26,"what-if")>0,"what-if","actual")` |
| 7 | Contribution change under assumed volume | `=((B2+Settings!D8*Settings!D26)*(1+Settings!D27))/B2-1` | what-if |
| 8 | Dollars a month under that assumption | `=((B2+Settings!D8*Settings!D26)*(1+Settings!D27)-B2)*Settings!D28` | what-if |
| 9 | Fixed share of costs | `=IFERROR(Scorecard!B22/(Scorecard!B22+Scorecard!B20),"n/a")` | actual |
| 10 | Runway in months | `=Scorecard!B11` | `=Scorecard!C11` |
| 11 | [Overhead](../glossary.md#overhead) allocation rate per hour | `=IF(Settings!D12=0,"n/a",Settings!D11/Settings!D12)` | `=IF(COUNTIF(Settings!E11:E12,"what-if")>0,"what-if","actual")` |
| 12 | Full cost of the line | `=Settings!D14+B11*Settings!D13` | `=IF(COUNTIF(Settings!E11:E14,"what-if")>0,"what-if","actual")` |
| 13 | Profit of the line after overhead | `=Settings!D15-B12` | `=IF(COUNTIF(Settings!E11:E15,"what-if")>0,"what-if","actual")` |
| 14 | Gross margin | `=Scorecard!B23` | actual |
| 15 | [Markup](../glossary.md#markup) | `=IF(Settings!D9=0,"n/a",(Settings!D8-Settings!D9)/Settings!D9)` | `=C2` |
| 16 | Margin | `=B3` | `=C2` |
| 17 | Price for the target margin | `=Settings!D9/(1-Settings!D29)` | `=IF(COUNTIF(Settings!E9,"what-if")+COUNTIF(Settings!E29,"what-if")>0,"what-if","actual")` |
| 18 | Payroll as share of sales | `=Scorecard!B24` | actual |
| 19 | Hire monthly net | `=Settings!D19-Settings!D18` | `=IF(COUNTIF(Settings!E18:E19,"what-if")>0,"what-if","actual")` |
| 20 | Months to pay back onboarding | `=IF(B19>0,Settings!D20/B19,"does not cover its cost")` | `=IF(COUNTIF(Settings!E18:E20,"what-if")>0,"what-if","actual")` |
| 21 | Capacity use | `=Scorecard!B44` | `=Scorecard!C44` |
| 22 | Customer lifetime in years | `=IF(AND(Settings!D17>=0,Settings!D17<1),1/(1-Settings!D17),"n/a")` | `=IF(COUNTIF(Settings!E17,"what-if")>0,"what-if","actual")` |
| 23 | [Customer lifetime value](../glossary.md#customer-lifetime-value) | `=IF(ISNUMBER(B22),Settings!D16*B22,"n/a")` | `=IF(COUNTIF(Settings!E16:E17,"what-if")>0,"what-if","actual")` |
| 24 | [Working capital](../glossary.md#working-capital) | `=Settings!D21-Settings!D22` | `=IF(COUNTIF(Settings!E21:E22,"what-if")>0,"what-if","actual")` |
| 25 | Current ratio | `=IF(Settings!D22=0,"n/a",Settings!D21/Settings!D22)` | `=C24` |
| 26 | [Cash conversion](../glossary.md#cash-conversion) in days | `=Settings!D23+Settings!D24-Settings!D25` | `=IF(COUNTIF(Settings!E23:E25,"what-if")>0,"what-if","actual")` |

## Format it so what-ifs are obvious

1. Select columns A to D on Scorecard and Metrics.
2. Open Format, then Conditional formatting, and pick "Custom formula is".
3. Enter `=$C1="what-if"` and choose grey italic text.

Now any result without real input looks different at a glance.

## Limits worth knowing

- The client counts look at rows 2 to 5,000 of Bookings. Extend the range if your file is longer.
- New clients means not seen earlier in your own file. If your file starts this month, every client looks new.
- Runway reads "funded itself" in a month with no net burn, because runway is the wrong lens then.
- Break-even needs a positive amount kept per sale. Otherwise it says "no break-even".
- If you change a row, change the formulas that point at it. Run the [check-up](../glossary.md#check-up) afterward.

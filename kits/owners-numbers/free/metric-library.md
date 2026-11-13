# Metric Library

Thirteen [metrics](../glossary.md#metric), each one a plain question an owner asks. Every metric has a basis rule.

**The basis rule.** A metric is "actual" only when every input came from the owner's own numbers or their [exports](../glossary.md#export). If any input is borrowed from an example value, the result is a "[what-if](../glossary.md#what-if)". A what-if shows how the math works and is never reported as a [finding](../glossary.md#finding) about the business.

| # | Metric | Question it answers | Inputs | [Formula](../glossary.md#formula) |
|---|---|---|---|---|
| 1 | [Contribution margin](../glossary.md#contribution-margin) | What does each sale keep after its own cost? | price, [variable cost](../glossary.md#variable-cost) per sale | price - variable cost; divide by price for the ratio |
| 2 | [Break-even](../glossary.md#break-even) | How much has to sell before the month stops losing money? | [fixed costs](../glossary.md#fixed-cost), price, variable cost | fixed costs / contribution per sale (sales needed); fixed costs / contribution ratio (dollars needed) |
| 3 | Price sensitivity | How much volume can a price move lose, or must it win, before it stops paying? | price, variable cost, price change | -(price x change) / (contribution + price x change) |
| 4 | Fixed versus variable split | Which costs move with volume and which land no matter what? | cost list tagged fixed or variable | fixed total / all costs |
| 5 | [Runway](../glossary.md#runway) | How many months of cash are left at the current burn? | cash on hand, monthly net burn | cash / burn, only when burn is above zero |
| 6 | [Cost to serve](../glossary.md#cost-to-serve) | What does a service or customer really cost once [overhead](../glossary.md#overhead) lands? | overhead pool, an allocation base (hours), the line's hours, direct cost, revenue | direct cost + (overhead / all hours) x line hours; profit = revenue - that |
| 7 | [Margin](../glossary.md#margin) | What is left after cost, at each level? | revenue, cost of goods, all costs | (revenue - cost) / revenue |
| 8 | [Markup](../glossary.md#markup) versus margin | Am I pricing on the number I meant? | cost, price | markup = profit / cost; margin = profit / price; price for a target margin = cost / (1 - margin) |
| 9 | Labor cost | Is payroll in a healthy band? | payroll, revenue | payroll / revenue |
| 10 | [Headcount payback](../glossary.md#headcount-payback) | When does the next hire pay for itself? | monthly loaded cost, monthly added contribution, onboarding cost | onboarding cost / (added contribution - loaded cost), only when that gap is above zero |
| 11 | [Capacity use](../glossary.md#capacity-use) | Can I serve more than I already do? | minutes or seats used, ceiling | used / ceiling |
| 12 | [Customer lifetime value](../glossary.md#customer-lifetime-value) | What is a customer worth beyond one visit? | annual margin per customer, yearly [retention](../glossary.md#retention) | annual margin x 1 / (1 - retention) |
| 13 | [Working capital](../glossary.md#working-capital) and [cash conversion](../glossary.md#cash-conversion) | How much money is trapped between paying and getting paid? | current assets, current liabilities, days of stock, days to collect, days to pay | assets - liabilities; days of stock + days to collect - days to pay |

## Traps worth saying out loud

- Markup of 50% is a margin of 33%. Owners who mark up by the margin they wanted underprice every job.
- Break-even needs the contribution to be above zero. When it is zero or negative the [script](../glossary.md#script) prints n/a, because no amount of volume reaches break-even.
- A price move's break-even shift needs no forecast. A volume response needs an assumed volume change, and that makes it a what-if.
- Lifetime value is sensitive to retention. Moving retention from 70% to 80% changes the lifetime from about 3.3 years to 5 years.
- Runway is the wrong lens on a month that funded itself.

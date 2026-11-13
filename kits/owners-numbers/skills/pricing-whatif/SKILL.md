---
name: pricing-whatif
description: Shows an owner what a price change can afford to do. For each service or product line it computes what each sale keeps, then the exact volume a price move can lose or must win before it stops paying (a finding), and optionally a worked what-if on a volume change the owner names. Use when someone asks whether to raise or cut a price, or how much business they can lose from a price increase.
---

# Pricing What-If

Works in: Claude Code (full version). The same steps work in Claude.ai and ChatGPT by hand, using the formulas below.

## Two kinds of statement, kept apart

- Break-even volume shift is a finding. It is exact arithmetic from the owner's own price and variable cost. It forecasts nothing.
- Volume response is a what-if. The owner names a volume change, and the page shows what that assumption would do. It is never a prediction of demand.

## Input

A `lines.csv` file with columns line, price, variable_cost, units_per_month. Variable cost is what one more sale costs directly (supplies, card fees, a commission). Rent and salaried pay are not variable.

## Method

1. Ask for one row per main line. Check price and variable cost against a recent invoice or receipt.
2. Run `python3 scripts/pricing_whatif.py lines.csv --moves=-10,-5,5,10`. Add `--volume-change=-0.05` only when the owner states a volume change they actually expect.
3. Read each line back. Example wording: "At a 5% increase you could lose about 5% of sales and still come out even. Whether you would lose more than that is your call, and nothing here predicts it."
4. Point out any line where a cut leaves nothing per sale. The script prints that no volume recovers the move.

## Formulas

- Contribution per sale = price - variable cost.
- Break-even volume shift = -(price x change) / (contribution + price x change). Negative means room to lose volume. Positive means volume that must be won.
- Contribution change under an assumed volume change = (new contribution x (1 + volume change)) / old contribution - 1.

## Rules that never bend

- Never present a volume response as a forecast.
- Never use an industry rule of thumb in place of the owner's price and cost.
- A price is a decision for the owner. State what the arithmetic allows and stop.

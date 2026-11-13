---
name: owner-scorecard
description: Builds a one-page monthly Owner's Scorecard from a small business's own exports (point-of-sale sales, a categorized bank CSV, a booking report, and a short settings file). Reports money in and out, what pays, customers, capacity and one thing to look at. Runs the 13-metric finance library, and labels any metric without real input as a what-if, never a finding. Use when an owner wants a monthly numbers page, break-even, cost to serve, runway or margin.
---

# Owner Scorecard

Works in: Claude Code (full version). The method also works in Claude.ai and ChatGPT with the exports uploaded to a Project, following the same rules below.

## What this produces

One page a business owner reads in two minutes. A one-line verdict, then money in and out, what actually pays, customers and capacity, and a single flagged thing to look at. Every number is labeled either "actual" (built from the owner's own files) or "what-if" (at least one input came from an example value).

## Inputs

Four plain CSV files in one folder. Layouts are in the kit's `free/` folder and in `assets/example/`.

- `sales.csv` with columns date, item, category, quantity, net_sales, client_id
- `bank.csv` with columns date, description, amount, category. Money in is positive. The owner fills the category.
- `bookings.csv` with columns date, service, staff, booked_minutes, status, client_id, price. Optional.
- `settings.csv` with columns name, value, note. Blank values are allowed and mean "I do not know this number".

If the owner has no CSV yet, help them export one from their point-of-sale system, bank and booking tool, then paste the first rows to check the columns.

## Method

1. Read `settings.csv` first. Confirm month_start and month_end.
2. Check the bank categories. Any row without one is counted and reported, never guessed.
3. Run `python3 scripts/owner_scorecard.py DATA_DIR --out-dir OUT`. The script only reads the four files and writes `scorecard.md` and `scorecard.json`.
4. Read the page back to the owner in plain words. Say which sections are findings and which are what-ifs.
5. Offer the next step the flag points at. Do not recommend a decision the numbers cannot support.

## Rules that never bend

- A metric with any borrowed input is a what-if. Say so on the page and when you speak.
- Never fill a blank setting with a guess. Ask for the number, or leave the what-if label on.
- Money in is bank deposits, not sales. The gap between the two is card fees and timing, and the page shows it.
- Owner draws and transfers are not operating costs.
- Report the data, then stop. The one flagged item states what the numbers show and does not tell the owner what to decide.
- Do not mix in outside benchmarks in place of the owner's own numbers.
- Never print or store bank account numbers. If an export contains them, tell the owner to delete that column first.

## Reference

`references/metric-library.md` holds the 13 metrics with their formulas and the basis rule. Read it before explaining any metric.

## Support code

If something fails, the script prints an error code such as E21 and the plain-words fix is in the kit's `fixes.md`.

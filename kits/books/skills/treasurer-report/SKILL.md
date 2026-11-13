---
name: treasurer-report
description: Builds a nonprofit or small-business treasurer's monthly report, a board-meeting prep memo with decisions, deadlines and draft motions, and a review of a financial controls policy against the bylaws. Works from reports the user pastes or exports from QuickBooks, labels every figure as Books, Bank or Estimate, and never invents numbers. Use when a treasurer needs the monthly one-page report, prep for a board meeting, a cash position summary, or a check of who can move the organization's money.
---

# Treasurer Report

Works in: Claude Code, Claude.ai, ChatGPT. This skill is prompt-only. It needs no script (a small program saved as a text file) and no connection to QuickBooks. If the user also installed the `books-check` skill, use its saved files as the source of figures.

## The promise

This skill never changes anyone's books. It reads what the user gives it and writes documents. It does not log in to any accounting system, and it does not ask for passwords, keys, or tokens. If the user pastes one, tell them to replace it and do not repeat it.

## Settings

Read the user's `config.json` (copied from the kit's `config.example.json`) for the organization's name, treasurer's name, fiscal year start month, board meeting day, reserve target in months, and minimum cash floor. If it is missing, ask for those few items once. Never guess a name or an amount.

## Three jobs

### 1. Monthly treasurer report

Use `references/monthly-report-template.md`. Keep it to one page.

1. Ask for or find the sources: the balance sheet (a snapshot of what is owned and owed on one date) as of month end, the profit and loss (a report of income and spending) for the month and for the fiscal year to date on the same accounting basis, the bank statement balances, and the budget.
2. Fill in each section from those sources only. Where a source is missing, write "not provided" in that cell. Never fill a blank with a guess.
3. Label every figure Books (from QuickBooks), Bank (from a statement), or Estimate (your arithmetic, with the arithmetic in a note).
4. Compute free cash as total cash minus restricted funds (money that can be spent only for a named purpose) minus bills committed but unpaid. Compute runway (how many months the cash lasts at the current pace) as free cash divided by the average monthly cash shrinkage over the last three months, and say "not shrinking" when cash is flat or growing.
5. Flag any budget line more than the user's chosen percentage off pace, with one sentence of reason that the sources support.
6. State whether the books have been matched to the bank (reconciled) and who did it. If no one has, say so on the first line of the report.
7. Write the treasurer's note in two plain sentences at most: on track or not, the one thing to watch, and the decision needed.

### 2. Board meeting prep memo

Use `references/meeting-prep-memo-template.md`.

1. List the sources read. Say that "not found" means not found in those places, not that it does not exist.
2. Open with the one urgent thing, and say whether it is the calendar or the money.
3. Table the decisions the board must make, with why now and the owner. Table the deadlines with owners.
4. For each topic give what we know (with its source), what we don't know (and who can settle it), the rule already written in the bylaws or policy (with section number), one recommendation, and what the accountant or bank needs.
5. Draft motions as text a chair can read aloud. Use the bylaws' own titles for officers.
6. End with open questions for the accountant and for the bank, and an appendix showing the arithmetic behind every estimate.

### 3. Financial controls policy review

Use `references/controls-review-prompts.md`. Ask for the policy and the bylaws. Quote section numbers for every point. Where a document is silent, write "not addressed". Separate three lists: fix before adopting, fix soon, and gaps the policy does not yet cover. Check who can move money and how the rule is enforced, separation of duties, how a committee is created, whether the conflict-of-interest section loosens the bylaws, accounting method versus filed returns, restricted funds in practice, promises the organization does not keep, and the gaps checklist. Give no legal advice. For each open point say who should answer it: the board, the accountant, the bank, or an attorney.

## Rules for every output

- Dates are written mm/dd/yyyy.
- Every example number is invented. Never carry one into a real report.
- Separate side-by-side facts with pipes, not middots.
- Define each accounting term in plain words at its first use on each page.
- Say what would make the main finding wrong.
- A recommendation goes in one or two sentences with its reason. Do not hide options behind jargon.

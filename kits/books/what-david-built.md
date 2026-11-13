# What David Built: The Books Kit

This page tells the story behind the kit for readers who want the background, meaning the problem David Luther was solving and what the kit shows about how he works.

## The problem

When a small organization's books and its bank disagree, almost nobody on the board can say why. The treasurer is a volunteer. Often the bookkeeper is part time or gone. The accounting software is made for people who already speak its language, so every simple question ("is our cash balance real?") turns into a paid hour and an answer nobody can check.

David Luther ran into this firsthand as a volunteer treasurer for a small private school and for a county housing nonprofit. In one case the operating account in the books looked healthy while the director's own figure for the bank was far lower. In the other, the board needed to know who could move the organization's money, whether a tax return would be ready in time, and whether the written financial controls would hold up. He had no wish to hand each question to an outside firm, and no wish to risk changing the books of an organization that depended on them.

## What he made

A set of working methods, then a kit that teaches them.

First, a rule. Look, never touch. David wrote a small program that can only ask QuickBooks to show him things. The rule is not a promise in a document. It is enforced inside the code, which refuses anything but a request to look and proves that to itself in a self-test before it connects.

Second, a set of checks an outside accountant would run, written down so a volunteer can repeat them. Together they find the usual causes of a gap between the books and the bank, such as a starting balance counted twice, a payroll that never reached the right account, a bank connection that quietly stopped, and deposits recorded in two places. A mystery entry gets placed in time by narrowing a report window until the amount is pinned to a few days. The recipes also warn about the traps in AI [connectors](glossary.md#connector), such as a report that silently uses a different accounting basis from the rest of the books.

Third, the human side of the work. That means a monthly treasurer report a board member can read in minutes, a prep memo that lists the decisions, deadlines, and open questions before a meeting, and a set of [prompts](glossary.md#prompt) for checking a financial controls policy against the organization's bylaws.

Then the kit itself. It gives the same answers three ways: free, using QuickBooks report exports, Google Sheets, and a free AI model; low cost, using Intuit's official QuickBooks connector with strict habits; and full, using the program, a developer account, and the recipes. Every setup step carries an ID and a fix code so a helper can find a stuck reader quickly, and a [check-up](glossary.md#check-up) button reports a [support code](glossary.md#support-code) with none of the organization's figures in it.

## What it changed

A treasurer can answer a question about the books in a sitting instead of waiting for a firm. Board members hear figures labeled as coming from the books, from the bank, or as an estimate, so no one confuses a guess with a fact. Untouched books matter for an organization that cannot afford a surprise. And the explanation of what went wrong comes with a trail from each claim to a report, a date, and a line.

## Skills this shows

- Financial analysis and controls. Reconciling books to the bank, spotting double counting, restricted-fund tracking, and reviewing a controls policy against bylaws.
- Safe engineering. A tool whose safety limit is built into the code and tested, with secrets kept out of files and screens.
- Working with AI honestly. Prompts that force a model to quote its source, label estimates, and say "not in the report" instead of guessing, plus a clear view of what AI connectors can and cannot do.
- Plain-language teaching. Writing for readers who have never used a command line, and testing the explanation, not just the code.
- Nonprofit governance. Board reporting, meeting preparation, and decision memos that make a volunteer board's job possible.
- Systems design. Three versions of one idea, each usable on its own and each upgradeable from the one before.

## Credit

Designed and written by David Luther. His working philosophy runs through the whole kit. Technology and finance are full of black boxes, partly because they are complicated and partly because explaining them is a product. Plain explanations, shared freely, open them. A hair salon or a small food bank should not have to pay for the answer to a simple question about its own books.

If you want this kit fitted to your organization, Pigasus Group does that work: https://pigasus.group/contact.

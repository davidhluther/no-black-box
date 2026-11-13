# Books: Check Your QuickBooks Without Changing It

This kit only looks at your books. It never changes them.

By the end of this kit you can answer plain questions about your QuickBooks books, such as "is the cash balance real?", "what do we owe?", and "how many months can we keep going?", and you can turn the answers into a one-page monthly report for a board. You do it without paying a bookkeeper or consultant for each question, and without any risk of altering the books while you look.

**The safety promise.** The code only sends [GET requests](glossary.md#get-request) (messages that say "show me this" and cannot add, edit, or delete anything), and that rule is enforced in the program itself, not just promised in a document. The AI [connector](glossary.md#connector) path uses only questions, and the connector's tools that create, send, or delete things are never used. Everything here is [read-only](glossary.md#read-only) (able to look but not touch). If a step ever asks you to add, edit, send, or delete something in QuickBooks, stop and see fix E14 in [fixes.md](fixes.md).

## Who this is for

A volunteer treasurer of a small food bank. The owner of a hair salon who keeps her own books. A board member who has been handed a QuickBooks login and a question nobody can answer. You know what a bank statement is. You do not need to know what an [API](glossary.md#api) or a command line is, and the kit explains each one as it comes up.

## The black box

Accounting software is a black box on purpose, or close to it. The screens are made for people who already know the vocabulary, so the simple questions ("does the bank agree with us?") end up costing a bookkeeper's hour, and the answers come back as a report you cannot check. This kit opens the box. It teaches the checks an outside accountant would run, gives you tools to run them yourself, and shows you how to confirm any answer against the QuickBooks screen.

## What you will have at the end

| Version | What you get | Time to set up |
|---|---|---|
| Free | QuickBooks report exports in Google Sheets, a pack of questions to paste into a free AI model, a monthly cash and [runway](glossary.md#runway) sheet, and a [check-up](glossary.md#check-up) button | About an hour and a half over a few sittings (three short guides of about 25 to 30 minutes each) |
| Low cost | The above, plus Intuit's official QuickBooks connector in Claude or its [plugin](glossary.md#plugin) in ChatGPT, so an AI model can read your live books and answer in seconds | About an hour more |
| Full | A small program that pulls any report straight from QuickBooks, plus step-by-step recipes for the checks accountants charge for | A few hours, most of it Intuit's developer setup |

The kit also includes a second skill, `treasurer-report`: a monthly treasurer report template, a board-meeting prep memo, and [prompts](glossary.md#prompt) for reviewing a financial controls policy. It uses whatever numbers you pulled above.

[Choose your version](choose-your-version.md) shows the three side by side and how to switch later. The [shopping list](shopping-list.md) lists every account and cost.

## What it will and won't do

It will find the usual causes of "the books say one thing and the bank says another": an opening balance counted twice, a payroll that never reached the [register](glossary.md#register), deposits booked in two places, a [bank feed](glossary.md#bank-feed) nobody has worked since spring. It will help you place a mystery entry in time, list what is already owed, and estimate how long the cash lasts.

A [reconciliation](glossary.md#reconciliation) against real bank statements, a tax preparer, and an audit all stay outside its reach. Every figure it produces is labeled as coming from the books, from the bank, or as an estimate, and the numbers in this kit's examples are invented.

## Where to begin

Not sure which version? Start free. Everything free carries forward, so nothing is wasted if you move up. The first guide is [BK-FR-01, Export your reports to Google Sheets](setup/BK-FR-01-export-reports-to-sheets.md).

If you get stuck, every guide ends with a help box. Questions about setup are free to ask.

## What David built

This kit comes from work David Luther did as a volunteer treasurer. [What David built](what-david-built.md) tells that story for readers who want the background.

## Want this set up for you?

Pigasus Group can set up the full version, and in particular Intuit's [developer app](glossary.md#developer-app), which is the fiddly part. Setup questions are free. If you want someone to fit the kit to your organization, tell us a little about it at https://pigasus.group/contact. Nothing in this kit is held back to make that sale; every step is written down here.

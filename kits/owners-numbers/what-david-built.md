# What David Built for Owner's Numbers

This page is the story behind the kit, written for anyone deciding whether David Luther can do this kind of work. It covers the problem he saw, what he made, and the skills it took.

## The problem

A small business owner usually knows the month felt busy, but not whether it paid. The answer sits in three programs that never talk to each other: the register, the bank and the booking calendar. A bookkeeper can reconcile them, and a consultant can build a dashboard, but both cost money, and both tend to hand back the same template everyone else gets. The owner's real questions are plain ones. Can I afford to hire? What does my most popular service really cost me once rent is counted? How much business can I lose from a price increase before it stops paying?

David Luther ran into this while building assessment tools at Pigasus Group for owners of salons, restaurants, clinics and trades businesses. The consulting work needed a monthly page an owner would actually read, and a way to answer pricing and hiring questions without inventing figures.

## What he made

A monthly scorecard that turns an owner's own [exports](glossary.md#export) into a single page with a verdict first, then money in and out, what pays, customers, capacity and one flagged thing to look at. Under it sits a library of finance measures written as ordinary questions, each with its [formula](glossary.md#formula) spelled out.

The design choice that matters most is the honesty rule. Every measure is labeled either an actual or a [what-if](glossary.md#what-if). A result is an actual only when every input came from the owner. If an input is missing, the tool borrows a labeled example and the result stays a what-if, never a [finding](glossary.md#finding). The pricing tool follows the same rule. The [break-even](glossary.md#break-even) shift of a price change is exact arithmetic from the owner's own price and cost, while any guess about how customers will react is kept separate and marked as an assumption.

He also built the surrounding documents: a quarterly report, a short advisory letter and a year-long roadmap, where a target stays blank until the owner chooses it.

For this public kit he rebuilt the work three ways. A [Google Sheets](glossary.md#google-sheets) version with every formula written out, so an owner can check it. An [AI Project](glossary.md#ai-project) version, with instructions that carry the same rules. And small [Python](glossary.md#python) [scripts](glossary.md#script) that read plain files and make no network calls. A [check-up](glossary.md#check-up) button in the Sheet tests the setup and prints a [support code](glossary.md#support-code) without reading any cell contents.

## What it changed

Owners can see their own month in two minutes, in their own numbers. The what-if label stops a practice calculation from being quoted as fact, which is the mistake a rushed spreadsheet or an enthusiastic [AI model](glossary.md#ai-model) makes most often. The same files work in all three versions, so an owner can start free and move up without redoing anything.

## Skills it shows

- Turning managerial accounting into plain-language tools for non-specialists.
- Designing for honesty. Separating findings from assumptions in the data model, the screen and the prose.
- Spreadsheet engineering, including formulas, a conditional-format convention and an [Apps Script](glossary.md#apps-script) check-up that tests structure without reading private data.
- Writing standard-library Python that only reads files, fails with coded, plain-words errors and is tested on invented data.
- Writing AI model instructions with explicit rules, privacy limits and refusal conditions.
- Technical writing for readers with no background, with a glossary, step IDs and a fixes table.

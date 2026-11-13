# What David Built: Grants and Giving

This page tells the story behind the kit for anyone who wants to know what David Luther made, why, and what it shows about how he works.

## The problem

Small nonprofits chase grants the hard way. The person in charge of grants is usually also in charge of five other jobs, and the records are scattered across old emails, board minutes and one person's memory. Nobody can say which funders said no last year, which ones gave once and were never thanked properly, or which numbers in a draft came from an audit and which came from a guess. Paid funder databases are sold as the answer, yet they show what funders say about themselves, not what they do. And AI models (a program that reads and writes text when you message it, such as ChatGPT, Claude or Gemini) make the old problem worse in a new way, because they will fluently invent a funder, a deadline or a statistic.

## What David built

David Luther built a grants pipeline for small organizations, first for a small rural nonprofit and then for other community groups, and has turned it into this kit. It has these working parts.

1. **A record-first method.** Before anyone is called a prospect, the pipeline searches the organization's own grant reports, minutes and bank records. Several supposed new prospects turned out to be past funders that had been recorded in only one place.
2. **Research from primary sources.** The research method ranks funders by what their own tax filings show they actually gave, and checks it against their published guidelines. Every claim is marked verified, secondary or unverified, with a web address and a date. A search over a whole state's foundation filings was written as a script and then rewritten so any organization can point it at its own area.
3. **A claims register** (a table of every fact a draft may state, each with its source) **and a number checker.** Every fact a draft may state about the organization sits in one table with its source. A small program flags any number in a draft that the table does not support. The same check was rebuilt as a spreadsheet feature so a volunteer can use it with no tools.
4. **A tracker, a phone page and a weekly search.** An engine builds a workbook and a phone-friendly page from plain tables, adds a link to every row, and runs a weekly read-only search of federal grants and local news. It records every attempt, and it alerts someone the same day when a run fails or a week is missed.
5. **A giving-channels pack.** Page text, donor letters and a recording method for gifts from donor-advised funds (a charitable account a donor holds at a sponsor, from which the donor recommends gifts), matching gifts (a gift where an employer matches an employee's own donation), monthly donors, stock, IRA distributions and wills.

For this release David rebuilt the free version on Google Workspace, so a volunteer can set it up in under an hour without a command line (a screen where you type instructions instead of clicking). He added a check-up (a Help menu button that tests the setup) that produces a support code (a short code a helper can read) with none of the organization's data in it, and a draft checker that works in a spreadsheet. The low-cost and full versions add a saved AI workspace, a scheduled search and the full engine.

## What it changed

Boards now see one picture of every ask, past and planned, instead of a pile of documents. Drafts can be traced line by line to a source, which makes review quicker and mistakes rarer. Funders that web searches missed showed up in the tax filings. Past gifts that nobody had logged were found before anyone approached those funders as strangers. Approval rules for large, mid-size and small asks are written down, so small grants no longer wait for a meeting. A missed week is now a visible event rather than silence.

## Skills it shows

- Turning public records into usable research, including tax filings and government data feeds.
- Designing AI workflows with guardrails: sources outrank summaries, every claim is graded, people approve everything that goes out, and the AI is never the source of facts.
- Writing programs in Python (a programming language) and in Apps Script (a free Google tool that runs small programs inside a spreadsheet), with tests, safe read-only behavior and failure alerts.
- Systems thinking about reliability, such as logging an attempt before the work starts and treating a missed run as a failure.
- Plain-language technical writing for readers who have never used a command line, with numbered steps, printed step IDs and a fixes table.
- Product judgment about who a tool is for, which version a volunteer can finish, and what a free version must keep.
- Working with nonprofit boards, staff and volunteers on governance, conflicts of interest and approval rules.

## Why David works this way

So much of how technology and fundraising work is kept in a black box, partly because it is complicated and partly because some people profit from keeping it there. David's view is that a small food bank should not have to pay someone to answer simple questions about the tools it relies on. This kit explains the method in plain terms and gives every step away. Paid help, through Pigasus Group at [https://pigasus.group/contact](https://pigasus.group/contact), buys David's time to fit the work to one organization's particular funders and records. It never buys a step held back.

# Choose Your Version

There are three versions. All three do the same job, which is finding funders, tracking asks and drafting from sourced facts. They differ in how much the computer does for you. You can start free and move up later without redoing your work.

## Side by side

| | Free | Low cost | Full |
|---|---|---|---|
| What you need | A Google account, such as one from Google Workspace for Nonprofits (Google's free offer of its office apps to eligible nonprofits), and the free version of ChatGPT, Claude or Gemini | Everything in free, plus one AI plan of about $20 a month | Everything in low cost, plus a computer that can run Claude Code, and optional paid research tools |
| Setup time | Five short guides, about an hour each at most, over a few sittings (about four hours if you do all five), no command line (a screen where you type instructions instead of clicking) | About an hour more | Half a day, with some typing in a terminal (the screen where you type instructions) |
| Tracker | Google Sheet built from CSV files (plain tables saved as text) you import | The same sheet | The sheet, plus a built workbook and a phone page made by the engine |
| Finding funders | Prompts (messages you paste into ChatGPT, Claude or Gemini) and checklists; you read the funder's own pages and tax filings | Same, in a ChatGPT or Claude Project that remembers your documents | Same, plus a script that reads IRS tax data for a whole state |
| Weekly search of Grants.gov (the US government's public list of grant opportunities) | By hand | A script in your sheet runs it every week and emails you if it fails | The engine's sweep (a search that runs by itself every week) runs on your computer's schedule |
| Drafting with a claims register (a table of every fact you may state about your organization, each with its source) | [Prompt](glossary.md#prompt) plus the DraftCheck tab | Same, with the register loaded into a Project | A skill (a folder of written instructions that a chat program can follow) drafts and a program checks numbers |
| Giving channels | Templates and a checklist | Same | Same, with a skill that fits the pages to your voice |
| Who it suits | A volunteer with a few spare hours over a few weeks | A staff member who writes grants every month | An organization with someone comfortable with technology, or a helper |
| Kit code in step IDs | FR | LC | FU |

Prices are in the [shopping list](shopping-list.md).

## What the free version gives up

It gives up depth and speed, not honesty. You paste in more text yourself, you run the weekly search by hand, and there is no whole-state tax-filing search. The tracker, the claims register, the draft checker and the giving-channels pack are the same in every version.

## How to switch later

- Free to low cost. Keep your Google Sheet. Add the weekly search script (guide GR-LC-02), and upload the kit's documents to a ChatGPT or Claude Project (GR-LC-01). Nothing you entered changes.
- Low cost to full. Export the Pipeline, Funders and Claims tabs as CSV files (File, then Download, then Comma-separated values). The engine reads CSV files with the same column names. Guide GR-FU-01 explains the match.
- Moving down is safe too. The sheet works on its own if you stop paying for anything.

## Claude Code only

Two parts of the full version need Claude Code or another computer with Python (a programming language), because they run programs on your own machine. They are the `grants-pipeline` engine and the whole-state tax-filing search in `funder-research`. The other skills work in Claude Code, Claude.ai and ChatGPT.

## Want this set up for you?

Setup questions are free, and you can ask them at [https://pigasus.group/contact](https://pigasus.group/contact). If you would rather have someone fit the full version to your organization, that is paid work that covers David Luther's time. The knowledge itself is all here.

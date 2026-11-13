# Choose Your Version

This kit only looks at your books. It never changes them.

All three versions keep your books [read-only](glossary.md#read-only) (able to look but not touch). They differ in how much work you do by hand and how deep the checks go.

| | Free | Low cost | Full |
|---|---|---|---|
| Version code | FR | LC | FU |
| How the numbers get to the AI model | You export reports from QuickBooks and paste them in | An official Intuit [connector](glossary.md#connector) (an add-on that lets an AI model read another service) lets the AI model look at your live books | A small [script](glossary.md#script) (a program saved as a text file) pulls any report and saves it to your computer |
| AI model | A free plan of ChatGPT, Claude, or Gemini | One paid plan of Claude or ChatGPT, about $20 a month (see the [shopping list](shopping-list.md)) | Claude Code, or any AI model you paste the saved files into |
| Cash and [runway](glossary.md#runway) sheet | Yes, with a [check-up](glossary.md#check-up) button | Yes, same sheet | Yes, same sheet, filled from the script's files |
| Questions pack | Yes | Yes, plus live questions | Yes, plus the recipes |
| Book-versus-bank cash check | By hand from exported reports | Partly; the connector has no entry-by-entry list | Full, from the [general ledger](glossary.md#general-ledger) |
| Dating an unknown entry | Not practical | Yes, by narrowing the [profit and loss report](glossary.md#profit-and-loss-report) | Yes, and the script automates it |
| Entry-by-entry detail | Report exports | Limited | Complete |
| Setup time | About an hour | About two hours | A few hours |
| Needs a command line | No | No | Yes, a few typed lines |
| Needs a developer account | No | No | Yes, free from Intuit |
| Who it fits | A volunteer treasurer with a monthly question or two | A treasurer who wants fast answers and has a QuickBooks Online subscription | Someone who wants complete, repeatable checks, or inherited messy books |
| Works in | Any AI model, any browser | Claude or ChatGPT | Claude Code (full version) |

## How to decide

Start free if you are unsure. The cash sheet and the questions pack are the same in every version, so moving up costs you nothing.

Pick low cost when you ask questions often and the export-and-paste routine wears you down. The connector is faster, with one trap: its profit and loss answer may be on a different basis than your books (see fix E15).

Pick full when a question needs entry-level detail, such as "which entry doubled our opening balance?" or "when was this posted?". The connector cannot answer those, and the script can. Intuit's developer setup is the slow part, and guides BK-FU-01 and BK-FU-02 walk through it step by step.

## How to switch later

Free to low cost. Keep your Google Sheet. Add the connector with guide BK-LC-01 or BK-LC-02, and keep using the same questions pack.

Low cost to full. Keep both. The connector stays handy for quick questions while the script handles deep checks. Start at guide BK-FU-01.

Full back down. Delete nothing. The saved files remain in the output folder, and the free sheet works from them.

## One rule in every version

Your books are never changed. Free only exports. Low cost asks questions, and you decline any offer to create or send anything. Full uses a script that refuses to send anything but a request to look, and its own self-test proves it (guide BK-FU-03).

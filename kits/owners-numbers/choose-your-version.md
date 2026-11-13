# Choose Your Version of Owner's Numbers

All three versions read the same four [CSV](glossary.md#csv) files (sales, bank, bookings and settings) and use the same 13 measures. They differ in who does the arithmetic and how much you click.

| | Free (FR) | Low cost (LC) | Full (FU) |
|---|---|---|---|
| What it costs | No purchase. A Google account is enough to start (checked 11/13/2026). | One AI plan. Claude Pro was $20 a month billed monthly (checked 11/13/2026). For ChatGPT, see the current price at chatgpt.com/pricing. | The Low cost plan or Claude Code access, plus a computer that can run [Python](glossary.md#python). See each vendor's page for current prices. |
| Who does the arithmetic | [Formulas](glossary.md#formula) in your [Google Sheets](glossary.md#google-sheets) file | An [AI model](glossary.md#ai-model) reading your files, plus the same Sheet to check it | Small [scripts](glossary.md#script) that only read your files |
| What you do each month | Paste three [exports](glossary.md#export), read one [tab](glossary.md#tab) | Attach three exports to a chat, read the page, ask follow-ups | Drop three files in a folder, run one command |
| Depth | Full [metric](glossary.md#metric) library, pricing [what-if](glossary.md#what-if), report templates | Same, with plain-language explanations and drafted reports | Same, plus repeatable runs and a record of each month |
| Privacy | Your data stays in your Google account | You upload files to an AI company. Read its data terms | Files stay on your computer unless you share them |
| Setup time | An estimate of one afternoon for your first month | An estimate of half an hour after the Sheet exists | A careful afternoon the first time |
| Good for | First look, a tight budget, checking the others | Owners who want things explained and drafted | Owners or helpers who want the same report every month |
| Needs a [command line](glossary.md#command-line)? | No | No | Yes, for a few copy-and-paste commands |
| What it cannot do | No automatic drafting of letters (use the prompts) | The AI model can slip, so the Sheet is your check | Needs more setup |

## How to switch later

- Free to Low cost. Keep your Sheet. Export its Sales, Bank, Bookings and Settings tabs as CSV files (File, then Download, then CSV) and attach them to your [AI Project](glossary.md#ai-project).
- Low cost to Full. Put the same four CSV files in a folder and run the script. The layouts match, so nothing changes.
- Full back to Free. Paste the same CSV files into the Sheet's data tabs.

## Room to choose

You do not need all three. If you only want the pricing what-if, the [formulas](free/formulas.md) or the prompts are enough on their own. If a measure does not fit your business, such as inventory for a pure service shop, leave its inputs blank. It will show as a what-if and stay out of your way.

Each paid piece is listed with a cheaper option in the [shopping list](shopping-list.md). Ready to begin? Go to [ON-FR-01](setup/ON-FR-01-copy-the-sheet.md).

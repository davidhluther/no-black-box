# Choose Your Version

All three versions run the same monthly cycle. They differ in how much the computer does for you, and in what you have to install. Start with the free version unless you already know you want more. You keep everything when you move up.

| | Free | Low cost | Full |
|---|---|---|---|
| What it costs | Nothing beyond your Google account | One AI plan, roughly $20 a month (see the shopping list) | A paid AI plan or account for [Claude Code](glossary.md#claude-code), and a computer you control |
| Setup | Four short guides of 10 to 20 minutes each, plus about 45 minutes for your first month, no [command line](glossary.md#command-line) | About an hour more on top of free, no command line | An afternoon, uses the [command line](glossary.md#command-line) for installs |
| What does the work | You, with prompts pasted into a free [AI model](glossary.md#ai-model) | You, with an [AI Project](glossary.md#ai-project) that already knows your rules, plus menu buttons in your sheet | The AI tool, following five written [skills](glossary.md#skill) |
| Minutes | Paste a [transcript](glossary.md#transcript) in parts, run three prompts | Same prompts, saved in the Project so you only paste the transcript | The meeting-minutes skill reads the transcript and builds the Word file |
| [Digest](glossary.md#digest) of what the minutes leave out | A [prompt](glossary.md#prompt) | A saved prompt | The meeting-digest skill |
| Transcript | You supply it (Meet, Zoom, or your typed notes) | Same | Can make one from a recording on your own computer with [Whisper](glossary.md#whisper) |
| Combined PDF | By hand, using a free merge route on your computer | Numbered PDF copies made for you, then a short manual merge | Converted, ordered, blank pages removed, and merged in one step |
| Board email | A template you fill in and paste into Gmail | Written as a Gmail draft for you, never sent | Written as a Gmail draft, or saved as a file if drafts are not available |
| [Check-up](glossary.md#check-up) | A Help menu in the [tracker sheet](glossary.md#tracker-sheet) that prints a [support code](glossary.md#support-code) | The same menu | A command named `doctor` that prints a code |
| Works in | Google Docs, Sheets, Drive, Gmail, and any AI model | Google tools plus ChatGPT or Claude | Claude Code only |

## What you give up at each step

The free version does the most by hand, and it is complete. Nothing is held back. You paste prompts, run the merge yourself, and write the email in Gmail.

The low-cost version leaves one manual step, the PDF merge, because [Apps Script](glossary.md#apps-script) has no built-in way to merge PDFs.

The full version asks the most of you at install time. Once it is running, a month's packet is a single request to the tool. It also keeps recordings on your own computer, which matters if your board talks about people and money.

## Room to choose

- Many boards stay on free forever. If your meetings are small and your reports few, the paste-in prompts are quicker than any tool.
- If you hold meetings on a video service that gives you transcripts, the low-cost version saves the most time. If you only have recordings, Whisper in the full version is the free way to get a transcript.
- The full version works well for a staff member who already uses Claude Code. It is a poor first choice for a volunteer who has never opened a [terminal](glossary.md#terminal).
- You can mix them. Run the free prompts and add the low-cost menu later.

## How to switch later

Free to low cost. Make an AI Project with guide BP-LC-01, then add the packet script with BP-LC-02. Your tracker sheet, folders, and checklist stay exactly as they are.

Low cost to full. Install the tools with BP-FU-01. Your Drive folders stay. Your tracker sheet's settings carry over to `config.json`, which uses the same names.

Full back down. Keep using the folders and the sheet. The prompts in `free/prompts.md` do the same jobs by hand.

# Choose Your Version

This kit has two versions, and the low-cost one is the top version. A full version (one that adds programming tools, paid connections, and scheduled jobs) is not planned. Customer research is reading and sorting, and the expensive extras would not make your answers more accurate. They would only make the same sorting faster for organizations that run dozens of studies a year.

## Side by side

| | Free | Low cost |
|---|---|---|
| Setup code | CR-FR | CR-LC |
| Monthly cost | $0 | One AI plan (see the [shopping list](shopping-list.md)) |
| [AI model](glossary.md#ai-model) | A free plan of ChatGPT, Claude, or Gemini | One paid plan of the same products |
| Where your method lives | [Prompts](glossary.md#prompt) you paste each time | A saved [Project](glossary.md#project) that already holds your method and your words |
| Collecting quotes | By hand into the Google Sheet | By hand, plus an [Apps Script](glossary.md#apps-script) that pulls search suggestions for you |
| Finding [themes](glossary.md#theme) | Paste quotes in batches | Paste or upload a whole sheet at once |
| Simulated panel | Yes, with the prompt in [prompts.md](free/prompts.md) | Yes, with [persona](glossary.md#persona) cards saved in the Project |
| Monthly refresh | You remember to do it | A monthly [trigger](glossary.md#trigger) runs the search-suggestion pull and records every run |
| [Skill](glossary.md#skill) files | Not needed | Optional (see below) |
| [Check-up](glossary.md#check-up) button | Yes | Yes |
| Time per research round | About a half day | About two hours |

## What you give up in the free version

Speed is what you give up in the free version, not accuracy. Free plans cap how much text you can paste in one sitting, so you work in smaller batches, and you paste the method prompt again each time. The quotes you collect and the themes you find are the same either way.

## Why no extra tooling is needed

Judgment is the expensive part of customer research, such as deciding whether a quote is about price or about trust, and that stays with you in both versions. The AI model speeds up the sorting, and a spreadsheet holds the evidence. Fancier tools exist for scraping thousands of reviews or monitoring forums around the clock, but a small organization has dozens of relevant comments, not thousands. At that size, reading them yourself is the better research, and the sheet keeps it organized. If your volume grows past what you can read, that is the time to look at tools, and the quotes you have already collected carry over to any of them.

## About the skills

Each part of the method also exists as a [skill](glossary.md#skill) (a saved set of instructions an AI model can follow). Claude Code and Claude.ai can load them; the folders sit in `overrides/` in this kit's source and are copied into the public repo's `skills/` folder when the kit is exported. They do the same job as the prompts. Use them if your AI plan supports skills. Otherwise paste the prompts.

## Switching later

- From free to low cost: keep your Google Sheet exactly as it is. Add the two Apps Script files, create a Project, and paste the instructions from the `chatgpt/` folder. Nothing gets rebuilt.
- From low cost to free: cancel the plan. The Sheet and your quotes stay, and you go back to pasting prompts.

## One honest limit for every version

Both versions read public words from public places. They cannot tell you what customers think in private, what people who never post online think, or what your regulars would say if you asked them. Asking real people stays on your list in every version.

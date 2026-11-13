# Choose Your Version

All three versions run the same [question set](glossary.md#question-set) and use the same sheet layout. The difference is how much typing you do and how much runs for you. Pick the lowest one that works, and move up only when you feel the pain.

| | Free | Low cost | Full |
|---|---|---|---|
| Code in guides | FR | LC | FU |
| What you pay | Nothing | One paid AI plan (see each vendor's page for the current price) | Pay-as-you-go use of each AI company's developer service, plus the [Claude Code](glossary.md#claude-code) plan or usage, if you use it |
| Where it runs | Free AI apps in your browser, Google Sheets | The same, plus your paid AI plan and a logging [script](glossary.md#script) in the sheet | Your computer, with Claude Code and your own keys |
| Who asks the questions | You, by hand | You, by hand | A script, through each company's developer service |
| What you see | What a customer sees in the apps | What a customer sees in the apps | What the developer service returns, which is different |
| Recording results | You fill each row | A menu fills the row for you and you correct it | The runner writes a draft file you correct |
| [Same-name](glossary.md#same-name) check | By hand with the SameNames tab | The AI plan helps you check | Skills do the check and write it up |
| Noise check | By hand, plus a repeat test | The AI plan helps | A skill does it |
| Analysis | You read the Summary tab | The AI plan reads your results | Seven analysis skills and a summary |
| [Search Console](glossary.md#search-console) and [GA4](glossary.md#ga4) | GA4 channel recipe | Same | Same, plus a classifier for leaked AI queries |
| Time per month | About two hours | About one hour | About 20 minutes plus reading |
| Paid tracking platforms | Not needed | Not needed | Named, never required |
| Works without Claude Code | Yes | Yes | No |

## An important difference

An answer through a developer service is not the answer a customer sees in the ChatGPT, Claude, Gemini, or Perplexity apps. The apps add their own hidden instructions, memory, and location handling. The kit therefore keeps the two apart. It tags developer runs "-api" and refuses to compare one with the other. If you move from free to full, keep running the free version by hand too, or start the full version as a new [baseline](glossary.md#baseline).

## Which one first

- Start free. Most owners get everything they need there.
- Move to low cost when typing each row becomes the chore. The logging script saves most of the work.
- Move to full when you track several businesses, or you want the questions run on a schedule you control.

## Switching later

- Free to low cost. Keep the sheet as it is. Add the logging script to it (guide AV-LC-01). Nothing already recorded changes.
- Low cost to full. Your `config.json` holds the same details as your Config tab. Run the same question set, tagged as a developer run, and start its own series.
- Any time. The question set version in your Config tab is the one fact that must carry over. Change it only when you retire or add a question, and then start a new series.

## Want this set up for you?

You can do every version yourself. If you want help fitting one to your situation, the contact details are on [Start here](start-here.md#want-this-set-up-for-you), and setup questions are free.

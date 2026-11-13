# Choose Your Version

All three versions use the same method. They differ in who does the typing. You can start free and move up later without redoing anything, because every version uses the same sheet, tabs and settings file.

| | Free | Low cost | Full |
|---|---|---|---|
| What you need | A Google account | The free setup plus one AI plan | Claude Code, some comfort with a terminal |
| Who gathers the numbers | You, by exporting from [GA4](glossary.md#ga4), [Search Console](glossary.md#search-console) and [Clarity](glossary.md#clarity) | Small programs in your sheet pull Search Console and GA4 each month | The [skills](glossary.md#skill) fetch the data themselves, including Clarity |
| Who writes the report | A free AI model with paste-in prompts | One AI plan with your Project loaded | Claude Code runs the `monthly-report` skill |
| Adds tracking [events](glossary.md#event) | By hand in [Google Tag Manager](glossary.md#google-tag-manager), one at a time | Same as free | Builds an import file of all events at once, with a name-collision check |
| AI traffic channel | You create the [channel group](glossary.md#channel-group) by hand | Same, plus a pull of the AI rows | Same, plus Clarity's AI channel through the script |
| Dashboard | [Looker Studio](glossary.md#looker-studio) from your sheet | Same, filled automatically | Same, with a header and format check before you import |
| Time each month | About 45 minutes | About 20 minutes | About 30 minutes, mostly reading |
| Checks the setup | Kit help menu in the sheet: Run check-up | Same | `python3 support/doctor.py measure` |
| Cost | No cost for the tools in this version, but see each vendor page for current terms | One AI plan; see ChatGPT's and Claude's price pages | A Claude plan that includes Claude Code, plus free tools |
| Where it works | Any browser | Any browser | Claude Code (full version) |
| Setup guides | [FR-01 to FR-05](setup/MM-FR-01-set-up-your-measurement-sheet.md) | [LC-01 to LC-03](setup/MM-LC-01-pull-search-console-into-your-sheet.md) | [FU-01 to FU-03](setup/MM-FU-01-install-the-skills.md) |

## What you give up in the free version

Time and some depth. You copy numbers by hand, you add events one at a time, and the AI model cannot see your accounts, so it works only from what you paste. Nothing in the method is held back. The check that grades every cause and confirms direction on a second source is the same in every version.

## Switching later

- Free to low cost: add two files to the [Apps Script](glossary.md#apps-script) project in your existing sheet, then paste the Project instructions into your AI plan. The sheet does not change.
- Low cost to full: install Claude Code, copy `config.example.json` to `config.json`, and give the scripts read-only access. The tabs and headers stay the same, so last year's rows keep working.

## Not sure

Start free. If you finish guide 5 and the monthly routine feels like a chore, that is the moment to move up. Want help deciding? Setup questions are free; see [Want this set up for you?](start-here.md#want-this-set-up-for-you) on the start page.

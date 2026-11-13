# Choose Your Version

All three versions run the same method and produce the same kind of [scorecard](glossary.md#scorecard). They differ in how much the computer does for you and how deep the checks go. The free version is complete for a small business. Start there unless you already know you want more.

## Side by side

| | Free | Low cost | Full |
|---|---|---|---|
| Version code in step IDs | WC-FR | WC-LC | WC-FU |
| What you need | A Google account, a free [AI model](glossary.md#ai-model) chat (ChatGPT, Claude, or Gemini), a browser | The free version, plus one paid AI plan that supports [Projects](glossary.md#project) | The low-cost version, plus [Claude Code](glossary.md#claude-code), a computer that can run it, and optional paid tools |
| Cost | No charge for the tools used. See each vendor's page for current terms | One AI plan. See the current price on the vendor's page | The AI plan, plus anything paid you choose to add (see the shopping list) |
| How you work | Copy a [prompt](glossary.md#prompt) from `free/prompts.md`, fill in brackets, paste it into a chat, copy the answer into the [Google Sheet](glossary.md#google-sheet) | Load the kit's files into a Project once. Each new chat already knows the method. A small [Apps Script](glossary.md#apps-script) in your sheet pulls speed numbers each month | Install the kit as a [plugin](glossary.md#plugin). The AI model reads your settings file, runs the checks, and saves reports to a folder |
| Setup time | An afternoon | About an hour more | An afternoon, with the shopping list in hand |
| Typing in a [command line](glossary.md#command-line) | None | None | A few lines, shown in full |
| Scorecard and 16 basics | By hand, in the sheet | By hand, with an AI model reading the pages | The AI model fills in the sheet or a report file |
| Speed numbers | You run [PageSpeed Insights](glossary.md#pagespeed-insights) and copy results | Pulled monthly into the sheet | Pulled by script, plus a site [crawl](glossary.md#crawl) |
| Competitor link comparison | Not available. You can see your own links | Your own links only | With a paid link tool |
| Site crawl for technical problems | The [Search Console](glossary.md#search-console) Pages report and a prompt | Same | [Screaming Frog](glossary.md#screaming-frog) export and a script |
| Monthly reminder | You set one | The sheet runs the speed pull by itself | You set a reminder, and the doctor command checks the setup |
| Gives up | The most typing and copying | Competitor links and the crawl | Nothing, but it needs the most setup |

## Which one do I pick?

- You have an afternoon and want a clear picture: free.
- You already pay for an AI plan and would like the method built in, with less pasting: low cost.
- You manage several sites, want a real crawl, or want the competitor link comparison: full.

## What each [skill](glossary.md#skill) does in each version

A [skill](glossary.md#skill) is a saved set of instructions an AI model follows to do one job the same way each time. In the free version, a prompt in `free/prompts.md` does a similar job.

| Skill | Free | Low cost | Full |
|---|---|---|---|
| site-scorecard | Prompts 1 to 7 and the Scorecard tab | Skill in a Project | Skill |
| local-seo | Prompts 2, 3, and 6, and `local-checklist.md` | Skill in a Project | Skill |
| local-schema | Prompt 5 | Skill in a Project | Skill |
| keyword-discovery | Prompt 12 and the Search Console export | Skill in a Project | Skill, plus an optional paid keyword source |
| market-analysis | Not packaged | Skill in a Project | Skill, with three research helpers at once |
| technical-seo-audit | Prompt 8 | Prompt 8 | Skill and script (needs a crawl export) |
| action-plan | Prompt 13 | Skill in a Project | Skill |
| baseline-data | The Pages, Competitors, and Monthly tabs | Same | Files in a folder |
| [cannibalization](glossary.md#cannibalization) | Prompt 11 | Skill in a Project | Skill |
| consolidate | Not packaged | Skill in a Project | Skill |
| internal-links | By hand with the Search Console Links report | Skill in a Project | Skill, with a crawl export |
| lighthouse | Prompt 4 | Prompt 4, plus monthly pulls | Skill |
| meta-fix | Prompt 9 | Skill in a Project | Skill |
| schema-gen | Prompt 5 | Skill in a Project | Skill |
| backlink-gap | Your own links by hand | Your own links by hand | Competitor comparison with a paid link tool. Full version only |
| blog-index | Not packaged | Skill in a Project (you paste the [sitemap](glossary.md#sitemap)) | Skill |
| common-crawl-checker | By-hand steps in the skill's last section | Same | Skill and script |

## Switching later

- Free to low cost. Keep your sheet. In the Config tab, change `version` from FR to LC. Then follow [WC-LC-01](setup/WC-LC-01-load-the-kit-into-a-project.md) and [WC-LC-02](setup/WC-LC-02-monthly-speed-pulls.md).
- Low cost to full. Copy the Config tab into a [config file](glossary.md#config-file) (the guide shows how), then follow [WC-FU-01](setup/WC-FU-01-install-in-claude-code.md). Your sheet keeps working.
- Back down. Nothing is locked in. Every version writes to the same sheet layout.

## Not sure?

If two versions both sound right, start with the free one. It takes an afternoon, and nothing you build there is wasted. The [start page](start-here.md) says where to ask for help.

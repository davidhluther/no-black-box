# Choose Your Version

This kit is the full team version only. It assumes [Claude Code](glossary.md#claude-code), developer keys for the AI companies you track, and a computer that can run a scheduled job. There is no free or low-cost edition of the team program, because a program that runs many sites on a schedule is exactly what the free versions are not built for.

## Is this the right kit

| You are | Start with |
|---|---|
| One brand, one site, no analytics team, and you want to learn the method | [AI visibility check, free version](../ai-visibility/choose-your-version.md) |
| One brand, one person, a paid AI plan, and you want less typing | [AI visibility check, low-cost version](../ai-visibility/choose-your-version.md) |
| A team tracking several sites, markets or product lines, with leaders asking for monthly numbers | This kit |
| A team that already runs the single-site full version and now needs a schedule, owners and a leader report | This kit, from guide AP-FU-03 |

## What this kit adds to the single-site full version

| | Single-site full version | This kit |
|---|---|---|
| Sites and markets | One, one `config.json` | Many, one folder and one [frozen](glossary.md#frozen) [question set](glossary.md#question-set) each, one program `config.json` |
| Who runs it | Whoever installed it | A named owner, backup and reviewer per site |
| Running it | By hand each month | `run_program.py` on a schedule, with retries |
| A missed month | You notice | A [ledger](glossary.md#ledger) records it and a check alerts the team the same day |
| Reading results | You read the summary | A monthly leader report with sources side by side and a noise statement |
| Platform disagreement | You list reasons | A standing step before any recommendation, and a place to record the reason |
| Skills | The same 14 | The same 14, unchanged |

## One difference to keep in mind

An answer from a developer service is not the answer a customer sees in the apps. The kit tags developer runs "-api" and refuses to compare them with hand runs. Teams that want the customer view as well should keep a small hand-run [series](glossary.md#series) using the [free version's method](../ai-visibility/setup/AV-FR-04-run-the-questions.md) and report it separately.

## Switching later

- From the single-site free or low-cost version. Keep your frozen question set and its version label. Create one site folder from it (guide AP-FU-01), run the [API](glossary.md#api) battery as a new series, and keep the old hand-run results as they are.
- From the single-site full version. Move each site's folder under `sites/`, add the program `config.json`, and begin at guide AP-FU-03.
- To a smaller team. Run one site folder with the single-site kit. Nothing in a site folder depends on the program file.

## Want it fitted to your stack?

You can run all of it yourself. If you would rather have it fitted to your platforms, [CMS](glossary.md#cms) and reporting cadence, the contact details are on [Start here](start-here.md).

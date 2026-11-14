# Set Up the Team and the Source Map (MR Full, Guide 1)

This guide covers what is different at team scale: who owns what, one settings file per site, and a written map of which platforms answer which question. It does not repeat tool installation. About 90 minutes, mostly in a meeting.

You will use the skills from the [Measure what matters kit](../../measure/start-here.md), the [AI search kit](../../ai-visibility/start-here.md) and the [Plain writing kit](../../plain-writing/start-here.md). For install and accounts, use the shared [Install Claude](../../../guides/install-claude.md) and [Keys and accounts](../../../guides/keys-and-accounts.md) guides.

1. **MR-FU-01-1.** Install Claude Code on the machine that will run the pulls, using [Install Claude](../../../guides/install-claude.md), and confirm [Python](../glossary.md#python) 3 with `python3 --version`. A shared machine or a small server beats a laptop, because scheduled pulls need something that is on.
   You'll know it worked when the terminal prints a version number for Claude Code and for Python. If a command is "not found", it's E22.

2. **MR-FU-01-2.** Add the kits that carry the skills. In Claude Code, add the no-black-box marketplace using the address on the repository's front page, then install `measurement-reporting`. The exported kit includes all eight skills, so you do not install the other three separately.
   You'll know it worked when typing `/` in Claude Code lists `metric-check`, `monthly-report`, `gsc-read`, `clarity-analytics`, `ga4-events-setup`, `looker-export`, `ai-traffic-classifier` and `evidence-review`. If one is missing, it's E22.

3. **MR-FU-01-3.** Make one settings file per site, product or market. Copy `config.example.json` to a folder named for the site, for example `sites/example-org/config.json`, and fill in that site's [Search Console](../glossary.md#search-console) name, [GA4](../glossary.md#ga4) property and measurement IDs, [Tag Manager](../glossary.md#google-tag-manager) [container](../glossary.md#container) ID and [Clarity](../glossary.md#clarity) project. Add the team fields: `report_owner`, `data_owner`, `report_reader` and `report_day`. Never put a secret in this file. Keep each site's data in its own folder, and never mix two sites' exports in one run.
   You'll know it worked when each site folder has a `config.json` with no example.org left in it. If a [skill](../glossary.md#skill) reads the wrong site, it's E29.

4. **MR-FU-01-4.** Write the owner table and keep it with the settings files. One row per recurring job, with one name per row, not a team name.

   | Job | Owner | Backup | When |
   |---|---|---|---|
   | Search Console capture and verify | Name | Name | Weekly, Monday |
   | Clarity pull | Name | Name | Daily or weekly |
   | GA4 totals export | Name | Name | First working day |
   | [Change log](../glossary.md#change-log) kept current | Name | Name | Continuous |
   | Direction checks and flagged moves | Name | Name | Before the report |
   | Report written | Name | Name | By the fifth working day |
   | Evidence review sign-off | Someone who did not write it | Name | Before it ships |
   | Dashboard refresh | Name | Name | After the report |

   You'll know it worked when every job has a named owner and a named backup, and the sign-off person is not the writer. An unowned job is the usual cause of E30.

5. **MR-FU-01-5.** Write the source map, which is the center of the cross-platform rule. For each question a leader will ask, list the platforms that measure it and mark which ones read the same upstream data, because those count as one source.

   | Question | Independent sources, use at least two | Counts as one |
   |---|---|---|
   | Did search traffic move? | Search Console, [Bing Webmaster Tools](../glossary.md#bing-webmaster-tools), GA4 organic sessions, a rank tracker or SEO platform | The Search Console screen, its export, its [API](../glossary.md#api) and any tool that only shows Search Console data |
   | Did [AI visibility](../glossary.md#ai-visibility) move? | Two or more AI-visibility platforms, your own monthly question battery, GA4 AI referrals, Clarity's AI channel | Two views of the same platform |
   | Did visits and leads move? | GA4, your [marketing automation](../glossary.md#marketing-automation) platform, your [CRM](../glossary.md#crm), ad platform reports | Two dashboards reading one GA4 property |

   Add your own rows for ads, email or sales-assisted pipeline. Write down which platform you believe when comparable sources disagree and why.
   You'll know it worked when someone outside the team can read the map and say, for any report figure, which two sources should back it. If a platform sits in two rows with different upstream data, note it, because that is where [direction disputed](../glossary.md#direction-disputed) figures come from.

6. **MR-FU-01-6.** Agree the flag rules before any report is written. Set `flag_threshold_percent` (start at 20) and `flag_threshold_events` (start at 100) in each settings file. Decide who may change a definition (what counts as a lead, which forms count) and require the change log to record it.
   You'll know it worked when the change log has a first row dated today that says "definitions agreed" and lists them. A tracking or definition change inside a comparison window is never reported as a drop or a gain; if it happens, go to E31.

7. **MR-FU-01-7.** Run the kit's check-up from the repository folder: `python3 support/doctor.py measurement-reporting`. It checks the Python version, the kit folder and that the settings file is valid with the key fields filled in. It reports names only, never values.
   You'll know it worked when it prints a support code that ends in E00, which means nothing it checks was wrong. Keep the code with your owner table. If it prints another code, find it in the [fixes table](../fixes.md).

Next: [Connect the data and schedule the pulls](MR-FU-02-connect-the-data-and-schedule-the-pulls.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MR-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

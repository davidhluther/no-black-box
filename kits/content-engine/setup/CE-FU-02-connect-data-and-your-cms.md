# CE-FU-02: Connect Your Data and Your CMS

You'll end with read access to your search and analytics sources, keys stored where your team can use them safely, and a chosen publish path for each site. Allow half a day, mostly waiting for access approvals. Ask for access first and do the rest while you wait.

1. **CE-FU-02-1.** Decide where keys live before you create any. For one person, [environment variables](../glossary.md#environment-variable) on their computer are enough. For a team, use the secret store your company already has, and give each person or job its own key so one can be revoked alone. Read [keys and accounts](../../../guides/keys-and-accounts.md) and [get and store your keys](../../ai-visibility/setup/AV-FU-02-get-and-store-your-keys.md) from the AI visibility kit, which covers the mechanics.
   You'll know it worked when you can say where each key will live and who can read it. If a key ever lands in a chat, a config file, or a commit, it's E17.

2. **CE-FU-02-2.** Get read-only access to [Search Console](../glossary.md#search-console) for every site in scope. Ask the property owner to add your Google account (or the one your job uses) as a user. Put the property name in the matching config file under `measurement.search_console_property`.
   You'll know it worked when Search Console lets you open the property and export the Performance report as a [CSV](../glossary.md#csv). Save one export in `measure/` named for the date. No access or an empty report is E09.

3. **CE-FU-02-3.** Pull Search Console data on a schedule if you want it unattended. The automatic pull is the gsc-read [skill](../glossary.md#skill), which ships in the Idea to live post kit and is set up in [IP-FU-02, connect your data](../../idea-to-post/setup/IP-FU-02-connect-your-data.md). To use it, also install that plugin (`/plugin install idea-to-post@no-black-box`), and name the plugin when you ask for a skill that exists in both. The simpler route is that a person drops a fresh export into `measure/` every week. Either way, record it as a job in `schedule.jobs` so a missed week shows up.
   You'll know it worked when a new file appears in `measure/` on the day you expect. A pull that returns far fewer rows than the export is E09.

4. **CE-FU-02-4.** Add [Bing Webmaster Tools](../glossary.md#bing-webmaster-tools) and [GA4](../glossary.md#ga4) read access, and note each platform's date range and country filter. The date window and filters differ between platforms, which is the usual reason two of them disagree.
   You'll know it worked when you can state, for each source, which dates and which countries a number covers. This pays off at step 4 of [CE-FU-04](CE-FU-04-owners-gates-and-reporting-to-leaders.md) and in E07.

5. **CE-FU-02-5.** Connect your SEO platform, if you have one. Create a read-only key as the platform's own help page shows, store it under the name `SEO_PLATFORM_API_KEY` (or your team's naming), and set `research.paid_keyword_tool` in the config to the platform's name. Check how many calls your plan allows per month and write that number and the owner in your ops notes.
   You'll know it worked when content-brief can read a keyword overview without asking you to paste the key. If it asks, the variable isn't visible to the window you started [Claude Code](../glossary.md#claude-code) from; it's E16. content-brief lists each paid call and its cost in the brief's last section, so review those weekly. When you run out of [quota](../glossary.md#quota), briefs carry a READ INCOMPLETE flag and wait for the next window; this is E10.

6. **CE-FU-02-6.** Choose the publish path for each site. A git-based site uses the publish skill's pull-request flow. A site on a [CMS](../glossary.md#cms) uses the adapter pattern in `skills/publish/references/cms-adapter.md`. Pick the lowest safety level your team has actually run: manual paste, [dry run](../glossary.md#dry-run) plus manual, draft creation, then full publish. Write the choice in each config under `publish.adapter` and keep `dry_run_first` and `require_human_confirmation` set to true.
   You'll know it worked when each site's config names its path. Create the CMS key with the least access that works (drafts only, no delete) and store it as in step 1. A CMS call that rejects a field or fails to save is E11.

7. **CE-FU-02-7.** (Optional.) Agree on a [CRM](../glossary.md#crm) export. Ask your CRM owner for a report of leads or opportunities by landing page and campaign, saved as a CSV in `measure/`. The kit reads exports and never writes to a CRM.
   You'll know it worked when the export has a page or campaign column you can match to your URLs and a date column. Note how the CRM attributes a lead, because leaders will ask.

8. **CE-FU-02-8.** Re-run the [check-up](../glossary.md#check-up) from the repo's top folder.

   ```bash
   python3 support/doctor.py content-engine
   ```

   You'll know it worked when the code still ends in OK.

Next, [CE-FU-03, run the weekly cycle on a schedule](CE-FU-03-run-the-weekly-cycle-on-a-schedule.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CE-FU-02-3). Run `python3 support/doctor.py content-engine` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

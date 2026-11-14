# SG-FU-02: Run It on a Schedule

You will set a cadence, name who owns each slot, [crawl](../glossary.md#crawl) each site, run the checks in order, and set the rule for a slot that fails. About two hours for the first full cycle, then much less. Do [SG-FU-01](SG-FU-01-set-up-the-team-workspace.md) first.

The skills don't start themselves. A person, or your team's own scheduler, starts each run, and the [run log](../glossary.md#run-log) is what proves it happened. [Claude Code](../glossary.md#claude-code) also has a non-interactive mode if you want a scheduler to start a run. Read its documentation first, keep the automation simple, and read the result the same day.

If you get stuck, the check-up command prints a [support code](../glossary.md#support-code) that tells a helper which step failed. The box at the bottom says where to send it.

1. **SG-FU-02-1.** Set the cadence and the owner of each slot. These are starting points. Change them to fit your publishing rhythm, then keep them fixed for a quarter so month-over-month reads are comparable.

   | Slot | Starting cadence | Why |
   |---|---|---|
   | [Baseline](../glossary.md#baseline) refresh | Monthly | A baseline older than 30 days gets a warning, so monthly keeps it current |
   | Technical audit, crawler access, speed | Monthly | Fixes ship continuously, and new breakage appears |
   | [Cannibalization](../glossary.md#cannibalization) and internal links | Monthly for large sites, quarterly for small ones | They read the baseline, so they cost little once it is fresh |
   | [Backlink](../glossary.md#backlink) gap | Quarterly | Link profiles move slowly, and the paid pull has a cost |
   | Competitor content and keyword gaps | Quarterly | Competitors publish on weeks, not days |
   | Customer-language research | Twice a year, and before a major rewrite | Reviews and forum wording change slowly |

   Write the owner's name against each slot in `config.json` under `cadence`, and freeze the competitor set for the quarter. Changing it midway breaks comparisons (E19).
   You'll know it worked when every slot has one named owner and a next date. A slot with no owner is a slot that will be missed.

2. **SG-FU-02-2.** Open the [run log](../glossary.md#run-log) and enter the planned slots for the quarter. One row per site per slot, with the planned date and owner, and the status set to "planned". Put the same dates in the owners' calendars.
   You'll know it worked when a leader can open one file and see what is due next week. If two people keep separate copies, that is E14.

3. **SG-FU-02-3.** Crawl each site and save the export in that site's folder. Use [Screaming Frog](../glossary.md#screaming-frog) or your own crawler, and export the full internal list untouched. [WC-FU-02-1](../../website-checkup/setup/WC-FU-02-crawl-and-monthly-run.md) shows the clicks. For a site too large to crawl in one pass, crawl one section at a time and keep each export separate. Only crawl sites you own or have permission to crawl.
   You'll know it worked when the file opens as a table with one row per page. If the columns look mixed up, you re-saved it from a spreadsheet, and it's E07. If the crawl ended early, was blocked, or missed logged-in pages, record what it missed, and see E08.

4. **SG-FU-02-4.** Refresh the [baseline](../glossary.md#baseline) and read its date. Export the last 90 days of queries and pages from [Search Console](../glossary.md#search-console) for each site, then ask Claude: "Refresh the baseline for each site in config.json and tell me the date of each." One person writes the baseline for a site. Everyone else only reads it, so two checks in the same cycle can't disagree.
   You'll know it worked when each site's baseline shows today's date. An interface export can stop at a row cap, so if the query list ends on a round number, it's E03. If the baseline is older than 30 days and no one refreshed it, it's E02.

5. **SG-FU-02-5.** Run the checks in order for each site. Each one reads the baseline, so run them after step 4. In Claude Code, type each request and let it finish before the next.

   - "Run the technical [SEO](../glossary.md#seo) audit on the crawl export in this site's folder."
   - "Run the cannibalization check, then list the pairs that serve the same need."
   - "Run the internal links audit."
   - "Run the speed check on the pages in config.json." Missing [field data](../glossary.md#field-data) is normal on small pages, and it's E18.
   - Run the [Common Crawl](../glossary.md#common-crawl) check from the [terminal](../glossary.md#terminal). Replace example.org with the site's domain:

     ```
     python3 skills/common-crawl-checker/scripts/check_visibility.py example.org --months 12
     ```

   - Quarterly, "Run the backlink gap with the link database." Every report says on its first line which path it used. If it fell back to the free path because the key was missing, it's E05, and if that is expected it's E06.
   - Quarterly, "Run the competitor content review for each competitor in config.json." If a competitor's site blocks the read, the [skill](../glossary.md#skill) skips it and says so, and it's E12.

   You'll know it worked when each run produced a dated report in the site's `reports` folder and you wrote the finish time in the run log. Timeouts from the Common Crawl servers are common, and one failed run says nothing about your site, so retry in an hour (E09). If Claude gives a number with no source, it's E11.

6. **SG-FU-02-6.** Handle a missed or failed slot the same day. This is the rule, and it has no exceptions.

   1. Record it. Set the run log row to "missed" or "failed" with the reason in plain words.
   2. Retry it. Write a retry date in the row, and rerun the same day when the cause is on your side.
   3. Flag it. Tell the slot's owner and the person who reads the summary, and write who you told and when.

   A missed slot is a failure even when older data is still fresh enough to use. Never let a week pass without either the data or a message that you don't have it.
   You'll know it worked when no row stays "planned" past its date. A blank where a run should be is E01.

7. **SG-FU-02-7.** Cross-check direction before anything reaches a leader. For each headline movement (a page gaining or losing, a competitor pulling ahead), look at a second platform, such as [Bing Webmaster Tools](../glossary.md#bing-webmaster-tools) or [GA4](../glossary.md#ga4) for traffic, and a second link source for links. Write one line in the register on whether the directions agree.
   You'll know it worked when each headline has an agreement line, or a note explaining why the sources differ. If they point opposite ways and you can't say why, it's E04, and guide SG-FU-03 shows how to handle that.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like SG-FU-02-5). Run `python3 support/doctor.py search-gaps` and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

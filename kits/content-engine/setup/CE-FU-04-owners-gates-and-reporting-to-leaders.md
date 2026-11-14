# CE-FU-04: Owners, Gates, and Reporting to Leaders

You'll end with a named owner for every stage, gates calibrated on your own pages, a publish approval you can point to, and a monthly note leaders can read. Allow about half a day, spread over a few days because the calibration needs real pages.

1. **CE-FU-04-1.** Fill in the owner table. In `config.json` under `owners`, name one person per role and a backup. A person can hold several roles on a small team, but write each one down. This is what each role answers for.

   | Role | Owns | Signs off |
   |---|---|---|
   | Content lead | The [queue](../glossary.md#queue), priorities, and the Monday routine | Which items move to Planned |
   | SEO owner | topic-screen, content-gap, and brief verdicts | New post, refresh, hold, or skip |
   | Editor | The four gates and evidence-review | A draft is ready for the publisher |
   | Publisher | The publish path for each site | The exact words that approve a post |
   | Analyst | Search data, checkpoints, and the leader note | Numbers and their sources |
   | Ops owner | The schedule, the job log, and the [check-up](../glossary.md#check-up) | That every job ran or was reported |

   You'll know it worked when a stranger could read the table and say who to ask about a missed [feed](../glossary.md#feed). The check-up confirms the `owners` block exists, and the rest is up to you.

2. **CE-FU-04-2.** Calibrate the gates on your own pages. Score five to ten of your best recent pages, then copy `skills/tell-scorer/gate-thresholds.default.json` to `style/gate-thresholds-<site-id>.json` and set each ceiling just above what those pages score. The shipped ceilings are starting points, not a [verdict](../glossary.md#verdict) on your content.

   ```bash
   python3 skills/tell-scorer/scripts/score_batch.py --md-glob 'drafts/*.md' --out measure/baseline-scores.csv
   ```

   You'll know it worked when your best pages pass and a draft full of banned words fails. If the [gate](../glossary.md#gate) fails everything, or passes a draft you know is poor, it's E14. For live pages, check extraction on two or three first; a wrong selector poisons every number (E18). When you ban a phrase, writers reach for the nearest unbanned one, so run the tell-scorer's emerging-phrases script on new content against an older baseline and read the list before banning anything else. Recalibrate each quarter from your own corpus, never from another team's numbers.

3. **CE-FU-04-3.** Make the evidence review a rule. Say: "Run evidence-review on <file>". It grades each claim confirmed, likely, unverified, or hypothesis, requires a dated source for every number, and tests cause-and-effect claims. Require it for any page with original data or a claim about your own results, and for every leader report. A hypothesis goes in an investigation list, not in the page or the plan.
   You'll know it worked when each reviewed file has a pass or fail, with blockers named. A statistic that rests on a weak outside source isn't confirmed by being repeated, so keep the source tier next to the number.

4. **CE-FU-04-4.** Decide your rule for platforms that disagree. [Search Console](../glossary.md#search-console), Bing, [GA4](../glossary.md#ga4), an SEO platform, and an AI-visibility platform will not move together, because their dates, filters, sampling, and sources differ. Write down the rule before the first argument: name every source and date range, don't average, and check the direction in at least two of them before acting. When they conflict, say why before choosing, then grade the finding unverified until the reason is checked. AI answers also change from run to run, so treat a single run of any AI-answer check as a hypothesis, record the date and model, and repeat it before you change a page for it (E08).
   You'll know it worked when a report you can show carries each number's source and date range, and a conflict has a written reason beside it (E07).

5. **CE-FU-04-5.** Pick a voice for each content type and stick to it. Run voice-presets once with your three main formats and choose Quick Take, Analyst Memo, or Straight Talk for each, or make your own from one of them. Set `draft.default_voice_preset` in the config.
   You'll know it worked when two writers drafting the same brief produce pieces that read as one publication, and article-check passes both.

6. **CE-FU-04-6.** Set the publish authority per site. For a git-based site, keep `authority` at `none` in the site's config until the team opens one [pull request](../glossary.md#pull-request) per post and reviews it on a phone. Then switch to `merge_n`: the publisher says the exact words `merge 12` for pull request 12, and nothing else counts. For a [CMS](../glossary.md#cms) site, stay at [dry run](../glossary.md#dry-run) plus manual or draft creation until the earlier level has run cleanly several times. Run the dry run:

   ```
   Run publish in dry-run mode for <title>.
   ```

   You'll know it worked when the summary lists the title, [slug](../glossary.md#slug), links checked, and images, and the live page shows the post's own title afterward. A merge or a saved draft alone isn't publication. If the script reports deploy_unconfirmed, live_check_failed, or merge_uncertain, it's E12. A CMS that rejects the entry is E11.

7. **CE-FU-04-7.** Set the measurement and refresh rhythm. Check each new page at two, six, and 12 weeks and record the numbers in `measure/`. Once a month, say "Run content-refresh part one" for each site, and have the SEO owner choose the top three to five. One refresh keeps what works and fixes what doesn't, and it never counts if only the date changes. Check for [cannibalization](../glossary.md#cannibalization) before expanding a page; the fix may be to merge two.
   You'll know it worked when each checkpoint has a row or file and each month ends with a ranked refresh list that names its data source.

8. **CE-FU-04-8.** Write the leader note, monthly. Ask the analyst to run content-handoff for its plain-language summary, then add one table of what shipped, what was measured at each checkpoint, and what you decided not to claim. Run evidence-review on the file before it goes anywhere. Say "share of the conversations we measured" or "the pages we measured", not market share, and say which sources the numbers came from. Leaders should see one page, plus a link to the table behind it.
   You'll know it worked when the note passes evidence-review and every number in it traces to a file in `measure/`. If a leader asks "how do we know", the answer is the source line, not a defense.

9. **CE-FU-04-9.** Put the check-up and the review on the calendar. Run `python3 support/doctor.py content-engine` monthly, review the owner table each quarter, and rerun the gate calibration when you change a rule. Read the job log's failures at the start of each month and keep a one-line record of each: what failed, when, who fixed it.
   You'll know it worked when the month's note says either that every job ran or exactly which didn't.

If you are stuck, go to the [fixes table](../fixes.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CE-FU-04-6). Run `python3 support/doctor.py content-engine` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

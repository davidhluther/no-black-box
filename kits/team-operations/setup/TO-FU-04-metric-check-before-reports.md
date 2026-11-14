# Put the Metric Check in Front of Every Report

About 60 minutes. You will run the `metric-check` [skill](../glossary.md#skill) on a real recent report, agree which platforms count as independent for your team, and make "checked, and here is what agreed" a condition of sending anything to leaders. The skill's method is in its `SKILL.md`. The prompt-only form for a smaller team is in the [Measure kit](../../measure/choose-your-version.md).

1. **TO-FU-04-1.** Pick a real report from the last month in which a number moved enough that someone asked why. Collect the exports behind it: [Search Console](../glossary.md#search-console), [Bing Webmaster Tools](../glossary.md#bing-webmaster-tools), [GA4](../glossary.md#ga4), your rank tracker, your [AI visibility platform](../glossary.md#ai-visibility-platform) and the [CRM](../glossary.md#crm) lead counts, for the same dates.

   You'll know it worked when each export has its first date of history and a data-through date written beside it. A feed that started late makes the "before" period look shorter than it was, and that is how falling pages once read as growing.

2. **TO-FU-04-2.** Decide, as a team, which sources are independent for each question you report on. Read `skills/metric-check/references/multi-source.md` in the kit. A Search Console export, a Search Console [API](../glossary.md#api) pull and a tool that only shows Search Console data are one source. Search Console, Bing, GA4 organic sessions and a rank tracker are four.

   You'll know it worked when you have a short table with one row per question (search traffic, leads, AI visibility) and the independent sources for each. Record it in the [workstream](../glossary.md#workstream) brief's "Settled, never re-ask" section with today's date.

3. **TO-FU-04-3.** Run the check on the report. Ask [Claude Code](../glossary.md#claude-code):

   ```
   Use the metric-check skill on this report and these exports. For every flagged move: define the measure, check the measurement before the cause, list the candidate causes with a grade and evidence for each, check direction on at least two independent sources, and give one action and one owner. Use its flagged-move template.
   ```

   You'll know it worked when each flagged move comes back as one block: the measure and its definition, the dates and data-through date, the measurement check, the causes with grades, the sources and whether they agree, and what to do, who and by when.

4. **TO-FU-04-4.** Read the grades before the story. A cause is graded holds, weakened or refuted, and must name its evidence. Missing data is "missing" and never zero. A figure confirmed on one platform is "[single-source](../glossary.md#single-source)." Where comparable sources disagree, the figure is "direction disputed" and nobody acts on it yet.

   You'll know it worked when no cause in the report lacks a grade. If two platforms disagree on direction, it's E12, and the fix is to find out why before the report goes anywhere.

5. **TO-FU-04-5.** Run the optional report checker. It reads the file and warns when a causal sentence has no grade, a figure has no source or date, or only one source is named.

   ```bash
   python3 PATH_TO_KIT/skills/metric-check/scripts/check_report.py report.md
   ```

   You'll know it worked when it prints warnings or none. A clean pass is not proof the analysis is right, and a warning is a prompt to look, so fix each one by adding the missing grade, source or date (E17).

6. **TO-FU-04-6.** Add the job record to the report. Use the line from the scheduled jobs guide, filled from the runner's report for the same period.

   ```bash
   python3 PATH_TO_KIT/skills/scheduled-jobs/scripts/job_runner.py report --days 7
   ```

   You'll know it worked when the report states the data-through date and lists every missed or failed [slot](../glossary.md#slot) in the period, even those a [retry](../glossary.md#retry) filled. A figure built on a late or repaired pull should say so next to the figure.

7. **TO-FU-04-7.** Give leaders one view. Per flagged move, show the measure and definition, what the sources say and whether they agree, the grade of the leading cause, and the action with its owner and date. Lead with the answer, then the evidence. Put the full blocks in an appendix.

   You'll know it worked when a leader can answer "how do we know" from the first page. Where leaders disagree with a decision someone else made, state the best case for that decision first, then judge it and name the test that settles it.

8. **TO-FU-04-8.** Make it the gate. Add to the workstream brief's Settled section, with today's date: "No report leaves the team until the metric check has run, direction rests on two independent sources or is labeled single-source, and missed slots are listed." Name the person who runs the check, and who runs it when they are out.

   You'll know it worked when the next report arrives with the check already attached. Follow-up answers from leaders get folded back into the report, and corrections are stated as "earlier this said X, it is Y because Z."

9. **TO-FU-04-9.** (Optional) Apply the predict-then-grade habit to your team's own recurring claims, such as forecasts or "this change will lift leads." Read `skills/scheduled-jobs/references/predict-then-grade.md`. Write the prediction down before the result, store it unedited, capture the actual on its own schedule and grade it against a rubric written first.

   You'll know it worked when the team has a short scoreboard that includes its misses. A forecast nobody grades is an opinion with a chart.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like TO-FU-04-3). Run `python3 support/doctor.py team-operations` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

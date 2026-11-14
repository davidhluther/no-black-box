# Put Every Recurring Job Under the Rule

About 90 minutes, mostly spent listing jobs. You will register your team's recurring pulls and reports with an owner each, run the watcher on a shared machine, send flags to a channel people read, and make the weekly report list every missed [slot](../glossary.md#slot). The rule itself is in the `scheduled-jobs` [skill](../glossary.md#skill). The one-person practice run is [BT-FU-05](../../builders-toolkit/setup/BT-FU-05-scheduled-jobs.md), and this guide does not repeat it.

Work in the first [workstream](../glossary.md#workstream)'s folder from guide 01.

1. **TO-FU-02-1.** List every recurring job the workstream relies on. Ask [Claude Code](../glossary.md#claude-code):

   ```
   List every recurring pull, export, crawl, report build and automation this workstream relies on. Look in the scripts folder, the scheduler's current entries, and any hosted scheduler settings I point you to. For each, give the source it reads, when it runs, what file or report it feeds, and who last changed it. Mark anything you could not find evidence for as "not verified".
   ```

   You'll know it worked when you have a table of jobs with a source, a time and a consumer for each. Add the jobs people run by hand "every Monday" too. If your team's list differs from what Claude Code found, trust neither until you reconcile them, because a job nobody listed is the one nobody is watching.

2. **TO-FU-02-2.** Give every job one named human owner, and one backup. The owner is the person who gets the flag and decides what to do when a fix needs a password, money or a message to someone else. Put both names beside the job.

   You'll know it worked when no row says "the team." If an owner leaves, the row changes the same day, and the ledger's Recurring runs table (step 10) is where you will see it.

3. **TO-FU-02-3.** Give each paid or limited source exactly one pulling script, called a [capture point](../glossary.md#capture-point), and make every report read the saved file. Read `skills/scheduled-jobs/references/one-capture-point.md` in the kit for the method.

   You'll know it worked when each paid source in your table has one script against it and no report calls the vendor directly. A second consumer that calls the source itself doubles the cost and splits the history. If a pull spends [quota](../glossary.md#quota), note the limit in the row now, because step 4 uses it.

4. **TO-FU-02-4.** Write the [registry](../glossary.md#registry). Copy `skills/scheduled-jobs/assets/jobs.example.json` to `jobs.json` in the workstream folder and make one entry per job: its command, a schedule, a grace period, a timeout, [retry](../glossary.md#retry) delays, whether it is safe to repeat and the file it must produce.

   ```bash
   cp PATH_TO_KIT/skills/scheduled-jobs/assets/jobs.example.json jobs.json
   ```

   The runner understands hourly, daily and weekly schedules. A monthly report is therefore built by a weekly or daily job that checks whether its inputs are complete, and the monthly step reads the saved files. Say "safe to repeat" only for a job whose rerun for the same slot gives the same result and spends nothing it should not. A pull that burns quota or appends rows twice is not safe until it writes by date and skips what it already has.

   You'll know it worked when `jobs.json` lists every job from step 1 and each has an `output_file`. If the runner later says it cannot find the registry, it's E06.

5. **TO-FU-02-5.** Make each job end with a line that starts `RESULT:` and says what it found, such as `RESULT: found 12 new rows` or `RESULT: found nothing`. The runner copies it into the [outcome row](../glossary.md#outcome-row).

   You'll know it worked when a run that found nothing is distinguishable from a run that never happened. Keep the capture script's own exit code honest too. An exit code of zero with no output file is cause "output-missing" and is a failure (E09).

6. **TO-FU-02-6.** Run one real job by hand and read the [outcome row](../glossary.md#outcome-row). Use a [slot](../glossary.md#slot) in the form the runner expects.

   ```bash
   python3 PATH_TO_KIT/skills/scheduled-jobs/scripts/job_runner.py run weekly-data-pull --slot 2026-11-13T22:00
   ```

   You'll know it worked when it prints "ok" and `job-outcomes/outcomes.ndjson` has an "attempting" row and an "ok" row. Then break the job on purpose, as in BT-FU-05-3, and confirm the failure leaves a row with the cause and the last lines of the log. A failure with no row is a bug.

7. **TO-FU-02-7.** Start the watcher on a machine that stays on, under a shared account and not a person's laptop. It writes missed-slot rows, retries jobs marked safe to repeat and flags the stuck ones. Put one line in the machine's [scheduler](../glossary.md#scheduler) every 20 minutes, with full paths. On Mac and Linux the scheduler is [cron](../glossary.md#cron): open its list with `crontab -e`.

   ```
   */20 * * * * cd /full/path/to/workstream && python3 /full/path/to/job_runner.py check --retry --notify >> job-outcomes/check.log 2>&1
   ```

   You'll know it worked when `job-outcomes/check.log` grows every 20 minutes. If the watcher reports missed slots for jobs that did run, or its log never grows, it's E07.

8. **TO-FU-02-8.** Route flags to a channel your team reads. Create an incoming-message address ([webhook](../glossary.md#webhook)) in your chat tool, then set it as the [environment variable](../glossary.md#environment-variable) `JOB_ALERT_WEBHOOK` in the same place the scheduler reads. Cron does not read your login settings, so put the variable in the crontab. Name who reads that channel the same day and who covers when they are out.

   You'll know it worked when a deliberately stuck practice slot posts a message. Without the address, flags land only in `job-outcomes/flags.md`, and a flag nobody reads counts as a delivery failure (E08). The runner never prints the address and scrubs secret-looking values from logged evidence.

9. **TO-FU-02-9.** Write down the repair routine, so the first response to a failure is a diagnosis and not an alert. Copy the standing instruction in `skills/scheduled-jobs/references/team-notes.md` into the workstream's brief (guide 03). In short: read the outcome row, classify the cause, fix what is local, rerun the slot, and tell the owner only when the fix needs them.

   You'll know it worked when a teammate can answer, from the brief alone, who is told, when, and what Claude Code is allowed to fix without asking.

10. **TO-FU-02-10.** Register every job in the [capability ledger](../glossary.md#capability-ledger)'s Recurring runs table, with its owner, schedule and outcome log. Then make the weekly report list missed slots. Run this at report time.

    ```bash
    python3 PATH_TO_KIT/skills/scheduled-jobs/scripts/job_runner.py report --days 7
    ```

    You'll know it worked when the ledger table matches `jobs.json` row for row, and the report prints every missed or failed slot in the last seven days with whether each was later resolved. Paste its result into the report even when every slot was later filled, because a leader reading the number should know it was late.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like TO-FU-02-4). Run `python3 support/doctor.py team-operations` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

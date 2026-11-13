# Make Scheduled Jobs Report Honestly

About 25 minutes. You will register a small practice job, break it on purpose, watch the runner record and [retry](../glossary.md#retry) the failure, and schedule it. Each step uses the practice folder.

1. **BT-FU-05-1.** Copy the registry and a practice script. Ask [Claude Code](../glossary.md#claude-code):

   ```
   Use the scheduled-jobs skill. Copy its assets/jobs.example.json to jobs.json here, then reduce it to one daily job named "practice" that runs scripts/practice.py. Create that script so it prints "RESULT: found nothing" and exits 0.
   ```

   You'll know it worked when `jobs.json` lists one job and `scripts/practice.py` exists. If Claude Code cannot find the [skill](../glossary.md#skill), it's E06.

2. **BT-FU-05-2.** Run the job once by hand. Replace `PATH_TO_KIT`. The [slot](../glossary.md#slot) is a date and time in the form shown, so use today's date and the time in your registry.

   ```bash
   python3 PATH_TO_KIT/skills/scheduled-jobs/scripts/job_runner.py run practice --slot 2026-11-13T06:30
   ```

   You'll know it worked when it prints "ok: practice slot ..." and a file `job-outcomes/outcomes.ndjson` now has two lines, one "attempting" and one "ok". If it says the registry is not found, run it from the folder that holds `jobs.json`, or it's E14.

3. **BT-FU-05-3.** Break the job on purpose. Change `scripts/practice.py` so it exits with an error, then run the same line again.

   ```bash
   python3 PATH_TO_KIT/skills/scheduled-jobs/scripts/job_runner.py run practice --slot 2026-11-13T06:30 --attempt 2
   ```

   You'll know it worked when it prints "FAILED" and the outcomes file gains a row with the cause and the last lines of the log. A failure with no row would be a bug. If it hangs, it's E15.

4. **BT-FU-05-4.** Run the watcher with retries. It records any slot that left no row, retries jobs marked safe to repeat, and flags stuck ones.

   ```bash
   python3 PATH_TO_KIT/skills/scheduled-jobs/scripts/job_runner.py check --retry --lookback-days 2
   ```

   You'll know it worked when it lists "unresolved" slots while the script is still broken, then "0 unresolved slot(s)" after you fix the script and run it again. Expect old slots to show as missed the first time, since nothing ran them. If every run says missed even when jobs are running, it's E16.

5. **BT-FU-05-5.** Put the watcher on your computer's [scheduler](../glossary.md#scheduler) (the part that starts jobs at set times). On Mac or Linux, run `crontab -e` and add this line, with your real paths. It runs the watcher every 20 minutes.

   ```
   */20 * * * * cd /full/path/to/practice && python3 /full/path/to/job_runner.py check --retry --notify >> job-outcomes/check.log 2>&1
   ```

   You'll know it worked when `job-outcomes/check.log` grows after 20 minutes. On Windows use Task Scheduler with the same [command](../glossary.md#command). If the log stays empty, it's E16.

6. **BT-FU-05-6.** (Optional) Set an alert address so a stuck job reaches you. Put it in an [environment variable](../glossary.md#environment-variable) named JOB_ALERT_WEBHOOK, never in a file you share.

   You'll know it worked when a deliberately stuck practice slot sends you a message. Without it, flags still land in `job-outcomes/flags.md`. If nothing arrives, it's E17.

7. **BT-FU-05-7.** Register the job in your ledger. Ask Claude Code to add "practice" to the Recurring runs table of `CAPABILITIES.md`, pointing at `job-outcomes/outcomes.ndjson`.

   You'll know it worked when the table has the row and the ledger checker still says "0 problem(s)". A job with no ledger row and no registry entry is the one nobody is watching.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like BT-FU-01-3). Run `python3 support/doctor.py builders-toolkit` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

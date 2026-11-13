---
name: scheduled-jobs
description: Rules and a small runner for scheduled work that must never fail quietly. Every scheduled job records the outcome of every run, a missed slot counts as a failure even when older data still looks fresh, failures are diagnosed and retried the same day, and anything still stuck gets flagged to the owner. Also covers two data habits, predict-then-grade and one capture point per outside source. Use before building, changing or reporting on any check, pull, crawl, export, automation or script that runs on a schedule.
---

# Scheduled jobs that never fail quietly

Works in: Claude Code (full version). The runner needs Python 3 and a way to start it on a schedule (your computer's scheduler: cron on Mac and Linux, Task Scheduler on Windows, or a hosted scheduler).

Settings: if the kit's `config.json` exists, read the `scheduled_jobs` block (registry path, and the name of the environment variable that holds the alert address). Otherwise ask the user.

## The failure that set the rule

On a Sunday night, a weekly data pull crashed because the computer's disk filled. It died before it rewrote its status file. The previous success, from four days earlier, still sat inside the job's allowed age, so the daily check read the job as fresh. Nobody was told. The week's data would have stayed missing until the next Sunday, with no mention anywhere.

The owner's rule afterward was that anything relied on that fails at its scheduled time must be documented and attempted again. Going a week without data and with no mention of it is not an acceptable answer.

## The rule

It covers every check, scrape, crawl, pull, export, automation and script that runs on a schedule.

1. **A missed slot is a failure, and the checker says so on its own.** A slot is one scheduled run time ("Sunday 10 p.m."). Judge each job against its schedule, not against a freshness window. If a job has no outcome row for its latest slot once a short grace period has passed, the checker writes a missed-slot row itself, without relying on the job's own files. This holds even when an older success is still inside the allowed age.
2. **Record before work.** A job writes an "attempting" row when it starts, so a crash or a killed process leaves a trace. A full disk can stop even that row, which is why the checker in rule 1 is the backstop. A stale success left behind must never stand in for a run that did not happen. An attempting row with no outcome after the job's timeout counts as a failure.
3. **Document every failure.** Each failure gets an outcome row naming the job, the slot, the reason and the evidence (the last lines of the log). A failure with no row is a bug. Rows are append-only. A late run or a retry writes its own row for the same slot, and the slot counts as resolved only when a later row for it says it succeeded.
4. **Retry automatically.** A failed or missed slot is retried without waiting for the next scheduled run. Each job's registry entry sets the wait times (the default is 15 minutes, one hour and four hours after the failure) and how to replay that exact slot (for example an `--as-of` date, so the retry fills the gap the failure left). A job is exempt only when it cannot be repeated safely, and its entry says so.
5. **Tell the owner, once, when stuck.** A failure that is still unresolved after the retries becomes one flag, keyed by job and original slot, never by log text or retry time, so the same failure does not alert every hour and filing cannot duplicate. Close the flag with the passing run as evidence. If the flag cannot be delivered, that is a failure too.
6. **Mention it in the next report.** Any weekly or daily report that relies on a job lists every slot the job missed in its period, even if a retry filled it.
7. **Watch the watchers.** Every scheduled job is registered with a checker. A job nobody watches breaks this rule.

## Fix it in the moment, not the morning after

The owner's second instruction: do not just flag that things broke. Troubleshoot in the moment and wait until they can run. A pile of alerts the next morning is useless, and it cascades when reports depend on the failed data.

So the order is repair first, alert last.

1. **Diagnose on failure, right away.** Read the log, classify the cause (full disk, expired login, permission denied, network, the source being down, or a bug) and apply the known fix for that class before the first retry.
2. **Keep trying until it can run.** While the cause is temporary, keep retrying and wait for the condition to clear. Do not stop after a fixed three attempts.
3. **Hold the dependents.** A report that consumes a failed job's output waits for the repaired run. It never publishes a gap silently.
4. **Alert only when stuck.** The owner hears about it only when the fix needs them (their password, their decision, their money) or every repair route is used up. The alert says what was tried and the one thing they must do.

## Sweep and self-heal

- Check every scheduled job daily against its own schedule: last exit status, missed slots, and whether its output actually landed (a fresh file, a new row, a delivery). An exit code of zero alone proves nothing.
- On detection, start a repair. It fixes what is local (scripts, paths, interpreters, configuration) without asking, and leaves anything touching a live site, money, credentials or a message to another person as a proposal for the owner.
- Prove the fix. A job counts as fixed only when it ran after the repair began and the next sweep shows no problem. A change that does not pass is "not fixed", never "fixed".
- Report where the owner reads. A report meant for them that lands only in a log file or a code-hosting page counts as a delivery failure.

## The runner

`scripts/job_runner.py` implements rules 1 to 5 in plain Python with no extra packages.

1. Copy `assets/jobs.example.json` to `jobs.json` in your project and describe each job: its command (a list of words), its schedule, a grace period, a timeout, whether it is safe to repeat, and optionally the output file that must exist and be fresh after a run.
2. Have your scheduler run `python3 scripts/job_runner.py run <job>` at the job's slot.
3. Have your scheduler also run `python3 scripts/job_runner.py check --retry --notify` every 15 to 30 minutes. This is the watcher. It writes missed rows, retries safe jobs when their wait has passed, and flags the stuck ones.
4. A job may print a last line starting `RESULT:` (for example `RESULT: found 12 new rows` or `RESULT: found nothing`). The runner copies it into the outcome row, so a run that found nothing is distinguishable from a run that did not happen.
5. `python3 scripts/job_runner.py report --days 7` lists every missed or failed row in the period and whether each was later resolved. Use it for rule 6.

Outcome rows go to one append-only file (`job-outcomes/outcomes.ndjson`, one JSON record per line). Flags go to `job-outcomes/flags.md`. If the environment variable `JOB_ALERT_WEBHOOK` holds a web address that accepts a JSON POST, flags are sent there as well. Keep that address in your environment, not in files you share. The runner never prints it, and it scrubs the values of any environment variable whose name contains KEY, TOKEN, SECRET or PASSWORD out of logged evidence.

What the runner does not do: diagnose causes, apply fixes, hold dependent reports or decide what is safe to repair. Those are judgment steps. Ask Claude Code to read the evidence in the outcome row, work out the cause and fix what is local, then rerun the slot with `job_runner.py run <job> --slot <slot> --attempt <n>`.

## Two data habits that go with it

Read these before building a job that pulls outside data or makes forecasts.

- `references/one-capture-point.md`: exactly one script pulls each paid or limited source and saves the result; everything else reads the saved file. Cost then follows the data, not the number of pages.
- `references/predict-then-grade.md`: publish a prediction that can be wrong, store it unchanged, capture the actual, grade on a schedule with a rubric written first, and show the misses.

## Register the jobs in your ledger

Add each job to the "Recurring runs" table in your capability ledger (see the `capability-ledger` skill), pointing at its outcome file. A scheduled job with no ledger row and no registry entry is the one nobody is watching.

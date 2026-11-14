# Team notes for scheduled jobs

Use these three pieces when more than one person depends on the jobs. They add to the rule in `SKILL.md`. They change none of it.

## The owner register

Keep this table in the workstream's capability ledger, under Recurring runs. One row per job in `jobs.json`.

| Job | Schedule | Owner | Backup | Feeds | Outcome log | Safe to repeat |
|---|---|---|---|---|---|---|
| Example: weekly organic pull | Sunday 22:00 | Alex Example | Sam Example | Monday report | `job-outcomes/outcomes.ndjson` | Yes |

Rules for the register:

1. Every job has a named person as owner and a named backup. A team name is not an owner.
2. When someone leaves or changes roles, update the register the same day and change the alert contact.
3. A job in `jobs.json` that is not in the register, or the reverse, is a finding in itself. Reconcile the two lists whenever you review the ledger.

## The standing repair instruction

Paste this into the workstream's session brief so every session starts with the same behavior when a job fails.

```
When a scheduled job fails or misses a slot, repair first and alert last.
1. Read the outcome row and the last lines of its log. Classify the cause: full disk, expired login, permission denied, network, source down, quota used up, or a bug.
2. Fix what is local (scripts, paths, interpreters, settings) without asking, then rerun the same slot with the runner's run command and the next attempt number.
3. Hold any report that reads the failed job's output until the repaired run succeeds. Never publish a gap silently.
4. Do not touch a live site, money, credentials or a message to another person. Write those as a proposal for the owner.
5. Tell the owner only when the fix needs them or every repair route is used up. Say what was tried and the one thing needed from them.
6. A fix counts only when the job ran after the repair and the next check shows no problem. Otherwise write "not fixed".
```

## The weekly line in every report

Any report that relies on a scheduled job ends with a line like this, filled from `job_runner.py report --days 7`.

> Data through 11/13/2026. Missed or failed slots this period: weekly organic pull, 11/08 (disk full, rerun and resolved 11/09). All other slots ran on time.

A report with no missed slots says so in the same place, so a reader can tell "none" from "not checked."

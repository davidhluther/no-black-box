# Capabilities: <project name>

Last verified against repo: YYYY-MM-DD by <session or person>

This file answers one question: what can this project do right now, and what proves it. The task list and the status file answer different questions. Update this file in the same change that ships a capability.

## 1. Live capabilities

| Capability | Where it runs | Shipped | Proof |
|---|---|---|---|
| Example: sends a weekly summary email to the team | `scripts/weekly_summary.py`, scheduler entry "weekly-summary" | YYYY-MM-DD | `logs/weekly-summary-YYYY-MM-DD.log`, pull request #12 |

## 2. In progress or staged

Built but not live. Name the gate each one waits on.

| Capability | Where it runs | Gate | Proof |
|---|---|---|---|
| Example: second weekly report for finance | branch `finance-report` | Owner review | pull request #15 |

## 3. Known NOT built, or decided against

Things a reasonable session might assume exist. Give the decision date and the reason.

| Item | Decision | Date | Reason |
|---|---|---|---|
| Example: SMS alerts | Declined | YYYY-MM-DD | Email covers it and SMS adds a monthly cost |

## Recurring runs

One row per scheduled job, pointing at where its outcome rows live.

| Job | Schedule | Outcome log |
|---|---|---|
| Example: weekly summary | Mondays 7:00 | `job-outcomes/outcomes.ndjson` |

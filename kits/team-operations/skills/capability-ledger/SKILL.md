---
name: capability-ledger
description: Sets up and maintains a shipped-capability ledger, one file per project that says what the project can do right now and what proves it. Includes the template, the rules for claiming that something does not exist, how to correct a fact everywhere it appears, and how recurring runs record their outcomes. Use when starting a project, when shipping a capability, before any claim that something is missing, never built or not set up, and when auditing whether a ledger is trustworthy.
---

# Capability ledger

Works in: Claude Code (full version). The template is plain Markdown and the checker needs Python 3. Everything else in this skill is a habit you can follow in any tool.

Settings: if the kit's `config.json` exists, read the `ledger` block (ledger path and maximum age in days). Otherwise ask the user where the ledger lives.

## The problem it solves

AI models are fluent about things they have not checked. Ask whether a project can send email, and a session will search, find nothing and say "no, it can't". Maybe the capability lives in a different folder. Maybe it shipped last week. Maybe it was decided against, on purpose, for a reason nobody wrote down. The wrong "no" then costs real work: a build of something that already exists, or a promise to a client that a feature is missing when it is live.

A ledger is the file a session reads first, so the answer comes from a record kept at the time the thing shipped and not from a search at question time.

## What the ledger is, and is not

It answers one question: **what capabilities exist right now, and what proves it.**

It is not the task list, which answers "what did we decide and finish". It is not the status snapshot, which answers "where are we this week". Keep all three. A ledger is the third thing. Neither of the other two can stand in for it, because a finished task is not a live capability (it may have been merged and never published) and a status line goes stale the week after it is written.

## One ledger per workstream

Every workstream (a project, a client, a site, a data pipeline) has exactly one ledger, kept as a file inside its repository, named `CAPABILITIES.md` at the top of the folder unless the project already has an equivalent file. If the project has none, create one before you ship anything, and say in the project's brief where it lives.

Work done in a worktree (a second working folder for the same project) updates the same ledger.

Do not use your tool's automatic memory as the ledger. Memory is scoped to a working folder and is not dependable shared state. A ledger is a file anyone can open and check.

## The shape

Copy `assets/CAPABILITIES.template.md`. It has a header and three sections.

**Header.** One line: `Last verified against repo: YYYY-MM-DD by <session or person>`. "Verified" means every row was checked against code, build logs or the live system on that date, not summarized from an older file. A reader should tell a verified ledger from a stale one at a glance. Dates inside the ledger are written year-month-day (2026-11-13) so the checker and any sorting tool read them correctly.

**1. Live capabilities.** A table with four columns.

| Column | What goes in it |
|---|---|
| Capability | One thing a user would call a capability ("sends a weekly summary email", "grades yesterday's forecast every morning"), not a code module. |
| Where it runs | Folder and path, web address, or runtime (the scheduler, the hosting service, a local command). |
| Shipped | The date it went live. |
| Proof | The strongest checkable pointer: a pull request number, a commit, a build log file or a live address. |

A row whose proof does not resolve is not a row. Fix the proof or demote the row to "In progress".

**2. In progress or staged.** Same columns. Things built but not live, such as an unmerged branch or a feature waiting on a gate. Name the gate.

**3. Known NOT built, or decided against.** This section ends the other half of wrong "no" answers. List things a reasonable session might assume exist or might waste time building, with the decision date and the reason ("price-tracking integration, declined 2026-07-25 by the owner, cost too high for the benefit").

## Maintenance rules

1. **A row lands in the same change that ships the capability.** This is the binding rule. A ledger updated "later" is a ledger that is wrong.
2. **Re-verify on any audit or backfill pass, and update the header date.** Never edit rows without rechecking their proof.
3. **Know the traps in verification.**
   - Reading environment variables from a hosting service can return empty strings for secret ones. That proves nothing about whether they are set.
   - A green automation run proves the pipeline ran, not that the deploy shipped. An outage once hid exactly there.
   - "Merged" is not "published" wherever a separate publish step exists.
   - Correct mail-routing records do not prove a mailbox exists, and the absence of a bounce does not prove delivery. Some servers accept a message and throw it away, which looks identical to the sender.

## Rules for negative claims

"Not found" is a search result. It is never a fact about what exists.

- Say where you looked. "Not found in the ledger and the build logs" is a report. "It doesn't exist" is a claim you have not earned.
- Before saying something does not exist, never shipped or is not set up, read the ledger and the build logs for the workstream.
- Check behavior, not only configuration. A setting that says a feature is on does not prove the feature works. Call it, or read the log of a real run.
- If you cannot verify, write "not verified" and what you checked.
- When someone pushes back on a negative claim, verify again. Do not defend it.

## Corrections

When a fact changes, correct every place the file states it, including summary headers. After editing, search the whole file for the old claim (`python3 scripts/check_ledger.py CAPABILITIES.md --find "old phrase"` lists every line that still has it). Prefer headers that point to details over headers that repeat factual claims, so there is one place to fix next time.

## Recurring runs write outcome rows

Any run that repeats on a schedule (a daily pull, a weekly report, a nightly check) writes an outcome row every time, even when it finds nothing or fails. Allowed outcomes:

- ran and found X
- ran and found nothing
- failed because Y

Silence must mean the run did not happen. Health checks then compare against the upstream truth of which runs should have happened, never only against downstream stamps, because a stale success left behind looks fine. The `scheduled-jobs` skill covers the mechanics.

Review and completion stamps attach to artifacts that exist whether or not a particular output was created. Stamp the thing under review, or create the missing brief as part of the review.

## Checking a ledger

```bash
python3 scripts/check_ledger.py CAPABILITIES.md
python3 scripts/check_ledger.py CAPABILITIES.md --find "superseded phrase"
```

The checker is read only. It confirms the header date exists and how old it is (a ledger over 30 days old gets a warning, change with `--max-age-days`), that the three sections exist, that each Live row has a shipped date and a proof, and that every proof written as a file path in backticks exists (paths are checked relative to the ledger's folder, or to `--root`). It cannot tell you that a web address is still live or that a pull request is real. That check stays with a person or a session.

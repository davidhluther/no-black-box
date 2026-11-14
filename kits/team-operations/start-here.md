# Start Here with Team Operating Discipline

The Monday report went out on time. The number in it was four days old, because the Thursday pull died on a full disk and an older success still sat inside its allowed age. Nobody was told. Two weeks later a leader asks why organic leads fell, and three people give three causes, each backed by a different platform.

This kit is the set of habits that stop both failures. It is for a marketing-ops lead, an SEO manager or a content-ops owner whose team runs recurring data pulls, reports and AI-assisted work, and who is the person leaders ask "how do we know."

## What your team will have at the end

- A [scheduled job](glossary.md#scheduled-job) rule with a working runner. Every run writes an [outcome row](glossary.md#outcome-row), a missed [slot](glossary.md#slot) counts as a failure, retries happen the same day, and a job that stays stuck becomes one message to a named owner.
- One [capability ledger](glossary.md#capability-ledger) per [workstream](glossary.md#workstream), updated in the same change that ships something, so "can we do that?" is answered from a record and not from memory or a hurried search.
- A [session brief](glossary.md#session-brief) for every piece of AI-assisted work that spans more than one sitting, with a [handoff](glossary.md#handoff) routine that survives [compaction](glossary.md#compaction) and staff changes.
- A routing check across all your workstreams that finds the ones your written notes forgot.
- A metric check that runs on every report before it leaves the team: define the measure, rule out measurement problems, grade each candidate cause, and confirm direction on more than one independent platform.

## The black box, once

Reliability for recurring work usually arrives as a vendor's monitoring product or a consultant's audit, and the method behind both is short. Nothing here needs a platform subscription. The rules are written down, the small programs are included, and you can copy every file.

## The six skills

This is the full team version. Each [skill](glossary.md#skill) is reused unchanged from a smaller kit, so you read each skill's method once and link to it. The guides here cover what changes at team scale: owners, schedules on a shared machine, many workstreams and how results reach leaders.

| Skill | What it does for the team | Needs a paid platform |
|---|---|---|
| `scheduled-jobs` | The rule and the runner: record every run, treat a missed slot as a failure, [retry](glossary.md#retry) the same day, flag once when stuck. Also two data habits, one [capture point](glossary.md#capture-point) per outside source and predict-then-grade | No |
| `capability-ledger` | The file that says what a workstream can do now, what proves it, and what was decided against. Also the rules for claiming something does not exist | No |
| `session-brief` | The brief with an unchanging purpose line, a compaction count and a "settled, never re-ask" list, plus the handoff routine | No |
| `workstream-inventory` | A fresh scan of every project folder, compared with your routing notes | No |
| `design-gate` | A browser check of changed web pages at phone and desktop widths, with a rule that the reviewer is not the builder | No. Needs a site you can run locally |
| `metric-check` | The check before any cause is claimed: measurement first, graded causes, direction on two independent sources | No. It reads whatever exports you give it |

None of the six calls a paid SEO or analytics platform. They govern the work that does. Your pulls from those platforms are the jobs you register.

## What you need

[Claude Code](glossary.md#claude-code) on a paid Claude plan, [Python](glossary.md#python) 3, and one machine that stays on, or a hosted [scheduler](glossary.md#scheduler), for the watcher. The [shopping list](shopping-list.md) names every dependency, links the keys guide for each account, and says what you can skip.

Plan on about three hours across the four guides, plus whatever time it takes to list your real recurring jobs. You can stop after any guide.

## Where to start

Read [choose your version](choose-your-version.md) (this is the full team version, and it points a smaller team elsewhere). Then work through the guides in `setup/` in order.

| Guide | What changes at team scale |
|---|---|
| [TO-FU-01](setup/TO-FU-01-install-and-pick-a-workstream.md) | Install the kit, point it at your workspace, pick the first workstream and give it a ledger |
| [TO-FU-02](setup/TO-FU-02-scheduled-jobs-with-owners.md) | Register every recurring pull with an owner, run the watcher on a shared machine, route flags to a channel people read |
| [TO-FU-03](setup/TO-FU-03-briefs-handoffs-and-inventory.md) | Briefs and handoffs for AI-assisted work, plus the inventory across all workstreams |
| [TO-FU-04](setup/TO-FU-04-metric-check-before-reports.md) | Put the metric check in front of every report, and list missed slots in the report itself |

If something goes wrong, look up the code in [fixes](fixes.md). Every term is in the [glossary](glossary.md). [What David built](what-david-built.md) explains where these rules came from.

> **Want it fitted to your stack?** Pigasus Group sets these up for in-house teams: your platforms, your [CMS](glossary.md#cms), your reporting cadence. Start at https://pigasus.group/contact.

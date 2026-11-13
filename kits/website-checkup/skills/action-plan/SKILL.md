---
name: action-plan
description: Turns findings from the scorecard and the other checks into one prioritized plan. Pulls tasks out of each report, drops guesses, rates each task by impact, urgency, and effort, sorts them into P0 to P3, and groups them by kind of work. Keeps tasks from the last plan visible so nothing disappears quietly. Use when asked what to do first, to prioritize findings, to build an action plan, or to turn an audit into a to-do list a small team can finish.
---

# Action plan

Works in: Claude Code, Claude.ai, ChatGPT.

This skill reads reports that already exist (the site scorecard, local search, speed, metadata, links, and so on) and answers one question: what should the owner do, in what order? It doesn't collect new data.

## Inputs

The reports to merge, pasted in or saved in the output folder. At least one is needed. Missing reports are listed as gaps ("speed hasn't been checked yet"), and the plan covers what exists. Also read `config.json` for the business type and, if known, how many hours a week the owner has for this.

## Steps

### 1. Collect

List each report with its date and how much of it was checked. A report that was mostly "unknown" contributes its gap as a task ("check the Google listing's dashboard") and no findings.

### 2. Keep only findings you can stand behind

- Confirmed and Likely findings become normal tasks.
- Unverified findings may appear with their caveat attached.
- Hypotheses never become numbered tasks. They go into an "investigate" list.
- Check every web address in a task by opening it. A wrong address is worse than no task.

### 3. Write each task as a record

What to do, why, what it changes for the business, effort (S, M, L), urgency (P0 crisis, P1 high, P2 medium, P3 low), what it depends on, confidence, and which report it came from.

Effort is judged against a one-person business. A task that needs money (paid tools, an agency) says so.

### 4. Prioritize

| Impact and urgency | Effort S | Effort M | Effort L |
|---|---|---|---|
| P0 crisis | Do today | Do this week | Make time first |
| P1 high | This week | This month | This quarter |
| P2 medium | This month | This quarter | A project, plan it |
| P3 low | Backlog | Backlog | Skip |

Anything that has AI models, search results, or listings stating something wrong about the business (wrong address, closed when open) is P0 whatever the effort. Customers act on it today.

### 5. Group

Group tasks by kind of work: site content, local presence, technical and markup, links and listings, AI visibility, and housekeeping. Sort by priority inside each group.

### 6. Continuity

If an earlier plan exists, list every task that was on it and isn't now, with a reason (done, replaced, evidence changed). Never drop one silently.

## Output

A plan of up to about 1,200 words. Lead with the P0 items, then each group in priority order, then the investigate list, then gaps ("what a speed check would add"). Attribute every number to its report. Write dates as mm/dd/yyyy.

## Boundaries

- Don't promise rankings or traffic. Say what the fix changes and what it doesn't.
- The plan is advice. Nothing is changed on the site or listing by this skill.

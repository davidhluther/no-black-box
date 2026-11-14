# What David Built: Search and Competitor Gaps

This page is the story behind the kit, written for a hiring manager or a team lead deciding whether to trust it.

## The problem

A B2B marketing team that runs a large site through a [CMS](glossary.md#cms) gets asked the same question every quarter. Why does a competitor beat us on the pages that matter, and which of the fixes we made actually helped? The honest answer usually arrives as a handful of reports from different platforms, pulled on different days by different people. Link data says one thing, Search Console says another, and the technical audit is a score nobody can reproduce. Two of the team's own pages may be competing for the same search, and nobody knows because no one looked at them side by side.

The cost is not a missing tool. The team has the tools. It lacks a method that gives every analyst the same dated numbers, tells them what to look at in what order, and leaves a record a leader can check.

## What David built

David Luther built this as a set of repeatable [skills](glossary.md#skill) for Claude Code while working in-house at Corpay, a B2B payments company, and later generalized them for public use. Each skill does one job and states its rules up front.

- A shared snapshot, the [baseline](glossary.md#baseline), that every check reads, with a date and a rule for how old it may get before the check says so.
- A technical audit that ranks findings by search impact, business impact, and effort, and always lists what it could not see.
- A cannibalization check that first asks whether two pages serve different needs before it recommends a merge, and a merge skill that refuses to run when they do.
- A link-gap skill that tiers outreach targets and labels every number with the platform and the date it came from.
- Competitor content and customer-language skills that keep quotes word for word and label thin evidence as thin.
- A wording pre-screen that says plainly it is a guess and never replaces real customers.

The team-scale layer in this kit adds the pieces a program needs. A schedule with named owners, a [run log](glossary.md#run-log) that records every slot, a [gap register](glossary.md#gap-register) that ties each finding to evidence and to a person, and a rule that a missed or failed run is recorded, retried, and flagged the same day.

## What it changed

Decisions got easier to defend. A recommendation arrived with its source, its date, and a note of what the checks could not see, so a challenge became a conversation about the evidence, not a contest of screenshots. Disagreements between platforms were written down and explained, not settled by picking the number that looked best. Merging pages stopped being a reflex, because the method asks whether the pages serve different needs first. A missed run showed up as a row in a log, not as silence that someone discovered a month later.

## Skills it shows

- **Program design.** Turning a pile of one-off audits into a cadence with owners, inputs, outputs, and a record.
- **Measurement discipline.** Dating every number, naming its source, cross-checking direction against a second platform, and separating "what changed" from "what caused it."
- **Automation.** Writing skills and small scripts that run the same way each time, read-only wherever possible, and fail loudly.
- **AI-search strategy.** Treating crawler access, link profiles, and content gaps as inputs to how AI models find and cite a site, and checking claims about causes before stating them.
- **Working with in-house teams.** Fitting a method to a team's platforms, CMS, and reporting cadence instead of handing over a score.

If you run an in-house team and want this fitted to your own stack, [start here](start-here.md), or contact Pigasus Group at https://pigasus.group/contact.

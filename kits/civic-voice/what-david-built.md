# What David Built: Civic Voice

This page tells the story behind the kit, for readers who want to know who made it and why.

## The problem

Local government decides things that touch a block, a school, a food pantry, or a main street, and the paperwork behind those decisions is hard to read. The [agenda packet](glossary.md#agenda-packet) for one meeting can run to hundreds of pages. The rules for speaking differ from one body to the next.

Records requests are easy to get wrong, and the law behind them changes by state. County statistics come with uncertainty that most people never see. Residents and small organizations without staff end up choosing between showing up unprepared and paying someone to prepare them. David Luther ran into all of this himself, as a volunteer on a local advisory board and as a volunteer helping a small rural housing nonprofit.

## What David made

David turned his own routine for meeting preparation into skills that anyone can use.

- Packet routine. Save the official documents in a dated folder, write a prep memo that ranks the agenda and cites a page for every fact, draft a comment that fits the time limit, and record the outcome afterward. It treats the official packet and the [adopted minutes](glossary.md#adopted-minutes) as the source of truth, and it makes the memo mark every claim as verified or not.
- Records-request routine. It makes the writer look up their own state's law on an official page before anything is drafted, then writes a narrow, neutral request for records instead of questions, and tracks the deadline.
- County-numbers routine. It keeps every [margin of error](glossary.md#margin-of-error) beside its estimate, flags numbers too shaky to use, and checks whether a difference between two places is real before anyone claims one.
- [Transcript](glossary.md#transcript) routine. It turns the [captions](glossary.md#captions) of a public meeting video into text with timestamps and links back to the video, and labels the result machine-made and unofficial.

Every routine comes in a free version (prompts, checklists, and a Google Sheet), a low-cost version (the same inside a paid AI plan), and a full version with short scripts that only read public data. He wrote the scripts with the standard library only, so nothing needs installing beyond [Python](glossary.md#python) and a free caption-fetching program. Secrets stay in the computer's memory for a session and never in a file.

## Lessons built into the method

Several rules exist because something went wrong once. One prep memo proposed conditions the local [ordinance](glossary.md#ordinance) already required, which would have spent the speaker's turn at the microphone on nothing, so the packet routine now checks the governing document first. A planned [public comment](glossary.md#public-comment) never got delivered because the meeting ran long, so the routine now includes a written fallback to the [clerk](glossary.md#clerk).

The Census Bureau's data service, which once answered anonymous requests, began requiring a sign-up code. The county [script](glossary.md#script) therefore reads that code from the computer's memory and explains the failure in plain words. And a summary of a meeting is only as good as its source, so every transcript carries a notice and a link.

## What it is built to change

The aim is to move preparation from reading everything to reading what matters, with the evidence a click away. Comments should come out shorter, more specific, and easier to stand behind. Records requests should go out narrow enough that an office can fill them, and statistics should stop being quoted without their uncertainty. None of it takes a position, so the same kit serves people on every side of an issue.

David has used the routines himself. The kit has not yet been tested by a beginner who followed the free version cold, and that test is planned before release.

## Skills this shows

- Turning a messy, expert-only process into steps a beginner can follow, with a way to check each step.
- Source discipline, where every claim traces to a page or [timestamp](glossary.md#timestamp) and the [AI model](glossary.md#ai-model) must say what it cannot verify.
- Data literacy, including margins of error, comparison tests, and honest limits on what a survey can say.
- Safe automation, with read-only scripts, secrets kept out of files, and a dry run before any request.
- Plain-language writing for readers with no technical background, including a glossary, numbered steps, a fixes table, and a support-code [check-up](glossary.md#check-up).
- Neutral design in a politically charged setting.

Questions about the kit, or a setup to fit your group? Pigasus Group answers setup questions for free at [pigasus.group/contact](https://pigasus.group/contact).

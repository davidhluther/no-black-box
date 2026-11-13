# What David Built: Customer-Language Research

This page tells the story of the kit for recruiters, clients, and anyone curious how it was made.

## The problem

Small organizations write about themselves in their own words. A food bank calls its program "client choice," a salon lists "balayage and dimensional color," and a treasurer writes "restricted fund balance." Their customers, donors, and neighbors use different words, so the person searching for "where can I get groceries this week" never finds the page about "client choice distribution." Market research would fix that, but it is sold in packages built for companies with a research budget, and the part that matters (reading what people actually said) is not complicated.

David Luther ran into the same gap at larger scale. He needed to know how business buyers described their problems before he wrote anything for them. Guessing produced content that spoke in company language, and nobody searched for it.

## What David built

He built a set of repeatable research methods, then rewrote them for small organizations as this kit.

- A review-reading method that pulls the exact words buyers use from public reviews and sorts them into problems, what they look for, what they got, and what they wish had been different.
- A forum-reading method for Reddit-style discussion boards, with rules about rate limits, source quality, and recording what the research could not reach.
- A way to read the questions people type into search boxes, including the suggestion lists and "[People Also Ask](glossary.md#people-also-ask)" boxes.
- A synthesis step that merges all of those sources into one list of customer phrases, tagged by who said them and what stage of deciding they were in.
- A [persona](glossary.md#persona) panel, where [AI models](glossary.md#ai-model) answer as customers built from real quotes, used to catch confusing wording before publishing. David wrote its limits into the method from the start, which is the part most buyers of this idea skip: [simulated respondents](glossary.md#synthetic-respondent) [pre-screen](glossary.md#pre-screen) wording, and they never replace real customers.
- A competitor-content review that shows which topics nearby alternatives cover and which questions nobody answers.

For this kit, the heavy parts (paid tools, scheduled jobs, large crawls) were removed, since a small organization has dozens of relevant comments and reading them yourself is better research. What remained became a Google Sheet, nine paste-in [prompts](glossary.md#prompt), an optional search-suggestion script with a logged monthly schedule, and a [check-up](glossary.md#check-up) button that gives a [support code](glossary.md#support-code) when setup goes wrong.

## What it changed

The work stopped content from being written in internal vocabulary. Teams could point to the quote behind every phrase they chose, and they could say how confident they were, because [sample size](glossary.md#sample-size) was recorded beside each finding. Wording tests found confusing phrases before publication. Because the panel's limits are stated up front, it never became the thing that decided what shipped; real customers still did.

## Skills it shows

- Qualitative research design and honest handling of its limits.
- Turning an expert method into steps a volunteer can follow without a command line.
- Writing for readers with no background, with a glossary and a defined term at first use.
- Building small, safe tools, including a Google [Apps Script](glossary.md#apps-script) that records every run and flags failures the same day.
- Judgment about when not to add technology.
- Applying the same method across a large company's search work (Corpay) and a small nonprofit's signs.

Part of the no-black-box repo by David Luther, which gives away the knowledge that is usually sold back to small organizations.

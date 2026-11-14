# What David Built

This is the story behind the kit, written for anyone deciding whether the work is worth trusting.

## The problem

People now ask AI products who to hire before they ever type a search. Search tools could not see that: [Search Console](glossary.md#search-console) reports only what was typed into Google, and a question put to ChatGPT leaves no trace in it. The tools sold to fill the gap tended to be black boxes. They returned a score, sometimes a share-of-voice percentage, with little to show which questions were asked, what the model said, or whether a "mention" was the company in question or a different business with the same name. When a number from one tool disagreed with another, nobody could say why.

David Luther ran into this at Corpay, a large business payments company where he works on search and AI visibility, and again with his own consultancy's name, which collides with a famous protest pig, a film company, and a planning firm with a similar spelling. A scoring system that cannot tell those apart cannot be trusted.

## What he made

A method, then a set of skills and small tools around it.

- A fixed battery of customer-style questions, written the way people type, asked of several AI products on the same terms every month. The questions are [frozen](glossary.md#frozen), so a change in the answer cannot be blamed on a change in the question.
- A [preflight](glossary.md#preflight) that hunts for [same-name](glossary.md#same-name) entities before the first run, so a look-alike can never be counted as the company.
- A [noise audit](glossary.md#noise-audit) that removes those look-alikes from the numbers, shows raw and clean figures side by side, and checks how much one question's answer varies on its own.
- A rule that two runs from different [question sets](glossary.md#question-set), or from the app and from a developer interface, are never compared.
- Analysis skills that read the answers themselves (what was said, which sites were cited, who won, how products differ, what changed), with every number traceable to a quoted line.
- A free version on Google Sheets with a [check-up](glossary.md#check-up) button, a Google Analytics recipe for spotting visits from AI products, and a classifier for leaked conversational queries in Search Console.
- A runner that asks the AI companies' official developer services with the owner's own keys, keeps its answers separate from hand-run ones, and never prints or stores a key.

## What it changed

For his own consultancy it showed, early and plainly, that the name problem was real and measurable, and that the measure had to be cleaned before anyone trusted it. Across the work, it moved conversations from "what is our score" to "which questions, which answers, and how do we know". It also made disagreement between tools useful. When sources disagreed, the first step became listing the reasons (different questions, products, model versions, or collection methods) instead of picking the more flattering one.

## Skills it shows

- Measurement design. Freezing a test instrument, separating instruments that should not be compared, and writing down what a number cannot tell you.
- Skepticism toward vendor metrics. Cleaning data, naming confounds, and refusing to claim a trend from a single month.
- Search and analytics fluency across Search Console, Google Analytics 4, and AI answer products.
- Practical engineering. Standard-library [Python](glossary.md#python), Google [Apps Script](glossary.md#apps-script), careful handling of [API](glossary.md#api) keys, tests, and a support-code system for non-technical users.
- Plain-language teaching. Explaining a technical method so that a salon owner can run it, which is the point of the whole repository.

## His point of view

Much of how this field works is held in a black box, partly because it is complicated and partly because people profit from selling the answer back to you. David's view is that a small business should be able to see exactly how its numbers were made, and decide for itself whether it needs help. This kit is that view in working form. If someone does want help fitting it to their situation, he and Pigasus Group can do that, and the knowledge in the kit stays free.

## Read the full write-up

David wrote up how this runs in his own work in the case study [Measuring AI Visibility Without Fooling Yourself](https://davidhluther.github.io/case-studies/ai-visibility-measurement/), on his portfolio.

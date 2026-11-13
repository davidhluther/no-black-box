# What David Built

This page is for anyone deciding whether to trust the kit, including a hiring manager skimming it. It says what problem David Luther set out to fix, what he made, and what it shows about how he works.

## The problem

Reports about a website's performance often arrive as numbers with no way to tell whether they are real. [Event](glossary.md#event) counts in analytics tools grow because of automatic measurements that are not visitors. Meanwhile the same form fill gets counted three times under three names. A tracking change in the middle of a month looks like a drop in leads. One tool's figure is treated as fact when a second tool, reading different data, disagrees. AI tools sending visitors to a site hide inside generic "referral" traffic, so nobody can see them. Readers, from a board to a busy leader, then act on a cause nobody tested.

David Luther ran into all of this doing search and AI visibility measurement work at Corpay, where moves in lead and traffic numbers had to be explained to leaders who rightly asked "how do you know?"

## What David made

Six [skills](glossary.md#skill), each a plain-language method with the small tools to support it.

- A way to add tracking events through [Google Tag Manager](glossary.md#google-tag-manager) without changing anything that already worked. Every addition is new and labeled, imported into a draft copy, and tested before publishing, so a mistake can be undone in one step. It includes a builder that writes the setup file, and a custom [channel group](glossary.md#channel-group) that gives AI traffic its own line in Google Analytics 4.
- A number-checking method, the center of the kit. For every number that moves, it defines the measure, confirms the data is real, lists the possible causes, grades each cause as holds, weakened or refuted, and requires the direction to be confirmed on a second independent source. David built it as a standing rule for himself and the tools he uses, so the same questions get asked every time, whoever or whatever is doing the analysis.
- A monthly report method that insists on a source, a definition and a date range for every figure, never presents a tracking change as a loss, and lists what cannot be measured instead of estimating it.
- A dashboard export that keeps a Google Sheet in a shape [Looker Studio](glossary.md#looker-studio) can read, with a checker for headers and formats.
- A read-only [Search Console](glossary.md#search-console) reader that compares two weeks and says plainly what the data cannot show.
- A Microsoft [Clarity](glossary.md#clarity) reader that respects the tool's hard limits, flags AI visits as a floor, and notes what Clarity's own wording does and does not support.

For this public kit David generalized all of it for organizations without technical staff. The free version works from exports and a Kit help menu in a Google Sheet that finds setup mistakes. The low-cost version adds small programs that pull the numbers. The full version is the original set of tools.

## What it changed

Reports that once drew a "why did it drop?" question now answer it before it is asked. A tracking change stops looking like a decline. Duplicated conversion counts get named and reported once. People who read the reports can see which figures were confirmed on more than one source and which were not. A site with a handful of staff can run the same checks a large team would.

## Skills it shows

- Analytics engineering: events, [tags](glossary.md#tag), triggers and channel groups in [GA4](glossary.md#ga4) and Google Tag Manager, with additive, reversible, tested changes.
- Measurement discipline: defining metrics, separating observation from cause, grading evidence, and reconciling independent data sources.
- Reporting for non-technical readers: plain-language explanations, honest labeling of floors and gaps, and recommendations that end in an owner and a date.
- Automation with safe defaults: read-only access, secrets kept in [environment variables](glossary.md#environment-variable), rate limits respected, no silent failures.
- Teaching: turning an expert's method into steps a first-time reader can follow, with a printed ID on every step and a code for every problem.

## The point of view

This is the same idea as the rest of the repository. Analytics gets sold as a black box, with a dashboard nobody can question and an expert who applies the same template everywhere. Knowing how to check a number is not secret knowledge. A small organization can do it, and it is better for everyone when it does.

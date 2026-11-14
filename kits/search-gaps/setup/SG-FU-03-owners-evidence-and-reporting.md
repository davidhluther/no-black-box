# SG-FU-03: Owners, Evidence, and Reporting

You will turn each run's findings into owned work, handle the cases where the evidence is ambiguous, and send leaders a summary they can check. About 90 minutes the first time. Do [SG-FU-02](SG-FU-02-run-it-on-a-schedule.md) first.

The skills suggest changes and never make them. Your editors, developers, and outreach people do the work, and this guide is what keeps their work traceable to evidence.

If you get stuck, the check-up command prints a [support code](../glossary.md#support-code) that tells a helper which step failed. The box at the bottom says where to send it.

1. **SG-FU-03-1.** Load the findings into the [gap register](../glossary.md#gap-register). One row per finding, with the site, the type (technical, links, content, wording, speed, crawler access), a plain description, the page or domain, the source and its date, the proposed fix, and the technical audit's impact and effort scores where it gave them. Ask Claude: "Add this run's findings to gap-register.csv in the template's columns. Do not add a finding that has no source and date."
   You'll know it worked when every row shows where its evidence came from and when it was pulled. A row without a source gets deleted, and if Claude supplied a number you can't trace, it's E11.

2. **SG-FU-03-2.** Name one owner and one due date per row. The owner is whoever can ship the change, not whoever found it, so a title rewrite goes to the content editor and a [robots.txt](../glossary.md#robots-txt) block goes to the web team. Sort by the audit's priority, then by what blocks the most pages.
   You'll know it worked when no row in the top ten has a blank owner or date. A finding no one owns is a finding that will reappear next cycle.

3. **SG-FU-03-3.** Apply the merge test before any merge ticket. The `cannibalization` and `consolidate` skills both ask first whether the two pages serve different needs, because merging a service page and a how-to post removes a page that people use. Only open a merge ticket when both pages are the same kind and meet the same need. For the rest, write a separate-and-strengthen ticket: new title and heading for each, and links between them. For a merge, the [redirect](../glossary.md#redirect) plan the [skill](../glossary.md#skill) writes goes to the person who can publish [redirects](../glossary.md#redirect), and the register row stays open until you have tested the old address.
   You'll know it worked when each flagged pair is marked as merge or separate, with the reason. A pair flagged as hard [cannibalization](../glossary.md#cannibalization) that turns out to serve different needs is E10.

4. **SG-FU-03-4.** When platforms disagree, write that down and explain it. [Search Console](../glossary.md#search-console), [Bing Webmaster Tools](../glossary.md#bing-webmaster-tools), [Ahrefs](../glossary.md#ahrefs), and [GA4](../glossary.md#ga4) measure different things from different samples, so small gaps are normal. When two point in opposite directions, check in this order: the date range, the page or query set, the country and device filter, and how each tool counts. Then add one line to the register row for the difference, such as "Search Console shows clicks down, GA4 shows sessions flat, GA4 counts after consent". Never pick the number you like.
   You'll know it worked when every disputed row says why the numbers differ, or says "unexplained" and who will look into it. An unexplained row can still go to leaders, but it goes labeled. See E04.

5. **SG-FU-03-5.** Test wording before it goes live. Give the draft title, heading, or page to the `persona-jury` skill, which answers as customers built from real quotes. Then show it to real customers or sales staff who talk to them. If you haven't run the customer-language skills yet, [CR-FR-01](../../customer-research/setup/CR-FR-01-make-your-sheet.md) shows the quote, source, and theme layout the `research-synthesis` skill expects.
   You'll know it worked when the register row says which personas read the draft and what a real person said. A jury that likes every draft is a warning, not a pass (E17), and a pass from the jury never excuses a factual error.

6. **SG-FU-03-6.** Write the one-page leader summary. Use four short sections.

   - What changed since last cycle, with the dates of the data on both sides.
   - What the checks found, in order of expected effect, each with its source.
   - What ships next, with owners and due dates from the register.
   - What the checks could not see. The skills write this section for you, and you should keep it.

   Keep numbers to ones you can trace. Say how many of anything it is, never a percentage alone. If the method changed, such as a new competitor set or a different [crawl](../glossary.md#crawl) scope, say so on the first line (E19).
   You'll know it worked when someone who wasn't in the room can follow every claim back to a row in the register. If a claim has no row, take it out.

7. **SG-FU-03-7.** Set a check-back date on every shipped fix. When a row's status becomes "shipped", write the date and a check-back date a few weeks out, long enough for search engines to re-read the page. At the check-back, compare the same measure from the same source, record what you see, and label it. A before-and-after read shows what moved after the change, which is weaker than proof that the change caused it.
   You'll know it worked when shipped rows carry a result note. If a merged page lost traffic and the redirect isn't live, it's E13.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like SG-FU-03-4). Run `python3 support/doctor.py search-gaps` and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

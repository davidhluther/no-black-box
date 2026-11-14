---
name: aeo-citations
description: Find which websites [AI models](../../glossary.md#ai-model) list as sources for your questions, check that the links are real, sort them by type (directories, review sites, local press, competitors, your own site), and show who "owns" each answer and where your business is missing from sources it could realistically enter. Use when asked why we are not cited, who gets cited instead, or what to publish or join.
---

# AEO citations

Works in: [Claude Code](../../glossary.md#claude-code), Claude.ai, ChatGPT (link checking needs web access; without it, mark every link unverified and skip format analysis).

## The idea

Whoever gets cited on a question tends to own that answer. The cited-sources column is the most useful thing in a run, because it turns into a to-do list of places to be. It also has a trap: models sometimes invent plausible web addresses, so a listed link is a claim, not a fact, until you check it.

## What to read

`runs/<run>/scored.csv` (cited_domains), the raw answer files (full web addresses), the [noise audit](../../glossary.md#noise-audit). If you have a list of pages on your own site, use it rather than rediscovering what you already have.

## Step 1: Collect

Gather cited domains and addresses per cell, across all groups. Strip tracking parts and obvious mobile variants. Cells where the model cited nothing count in the denominator ("none given" is an observation); skipped cells leave it.

## Step 2: Check each distinct address

Open it. Label it verified (loads), dead (error), suspected invented (a believable address on a real site that does not exist), or unverifiable (the check itself failed). Count suspected inventions per product. Never treat an unchecked address as a real target.

## Step 3: Sort by type

Your own site, a tracked competitor, an untracked business (a signal that your competitor list is incomplete), a review platform, a directory (chamber, listings, county or city pages), local press, an industry publication, a software or vendor blog (the answer chose a tool over a person), a community forum or social group, a government or school site, other. Report each domain's share of cells with [citations](../../glossary.md#citation), and each type's share.

## Step 4: Who owns each answer, and where you are absent

- Owners: domains cited again and again on the same question, across products.
- Absences: questions where the cited types are ones you could realistically enter (a directory you could join, local press you could earn, a question your site could answer). If you already have a matching page and it is still not cited, that is a reach problem, not a content gap. Say which.
- Thin slots: questions where no source owns the answer. These are the cheapest ground.
- Encroachment: untracked businesses cited repeatedly. Recommend adding them to your competitor list; never edit the list yourself.

## Step 5: Page formats

For checked addresses, note the format (what-is explainer, comparison, best-of list, how-to, review profile, directory listing, price page, service page, other). The dominant formats per group show what kind of page models prefer to cite on this topic.

## Output

`analysis/<run>/citations.md` (300 to 600 words): top owners per question group, type shares, your absence pattern with the three most reachable entry paths, thin slots, and a note on invented links if they matter. Confidence: a checked link is confirmed; ownership seen across two or more products is likely; one-cell observations are unverified.

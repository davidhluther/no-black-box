---
name: brief-layer
description: Add search and AI-answer structure to a content brief, or check a draft's structure against its brief. Use whenever a brief, cluster plan, or content spec is being written, because the brief is where search intent gets decided. Covers the target query, title direction, question-style headings, FAQ direction, tables and lists, internal links, AI-answer habits, refresh cadence for buying-intent pages, and schema discipline.
---

# Brief layer

Works in: Claude Code, Claude.ai, ChatGPT.

## Premise

Search intent is a strategy decision. If the brief does not name it, the writer guesses, and nobody sees the guess until rankings and AI answers show it. This layer applies at brief time, not as a drafting afterthought. Voice and wording rules live in your style guide (`draft.style_guide_file`); this layer decides what a piece targets and how it is shaped for machines. Where they seem to conflict ("prose over bullets" against tables), the rule is structure for enumerable data, prose for argument.

## What every brief carries, per piece

1. **Target query.** The question or phrase the piece answers, written the way a reader would type or say it ("how much food should we order at once", not "inventory optimization"). One main query per piece. Add others only if the piece genuinely answers them.
2. **Title direction.** The main query's natural wording should survive into the title within your length limit. If no title under the limit can hold the query, the query is wrong for the piece.
3. **Question-style heading candidates.** List the real questions the piece will answer; each becomes a heading in question form. A heading with no real question behind it stays plain, because an all-question outline is its own detectable pattern.
4. **Questions-and-answers direction.** Three to five questions a reader has after the main one is answered. The drafter writes them as part of the draft. If your website platform builds structured data (FAQ markup) from a field, fill that field so the visible section and the markup come from one source.
5. **Structured elements.** Name what is genuinely a list, comparison, spec, or step sequence, and specify it as a table or list. Machines lift structure cleanly. Argument stays in prose.
6. **Internal link map.** Which existing pages this piece links to and which should link back, woven into sentences with descriptive anchor text. In a cluster of related posts, links go both ways between the main page and its supporting pages.

## AI-answer habits

- Lead with the answer. The first section should answer the main query in a form that could be quoted, then earn the rest of the read.
- A question heading followed by a direct, self-contained answer is what AI tools lift most cleanly.
- Named specifics (real tools, real places, real numbers with sources) survive into AI answers. Vague allusion does not.
- If you track AI visibility (for example by asking the same set of questions each month and noting who is mentioned), say so in the brief. That is the scoreboard for these choices.

## Pages that people use to buy or choose

Applies to pricing, product, comparison, and "best X" pages. These are brief-time decisions.

- **State the refresh cadence in the brief.** A reasonable default is monthly for pricing and product pages and quarterly for other choosing pages. The page needs a visible date a crawler can read (not only in hidden metadata, not inside an image), and every refresh pairs the date with a real change.
- **A date-only bump on unchanged content is prohibited.** If a cycle has nothing real to change, leave the date as it is.
- **Counted lists.** Public analyses of thousands of search results, such as the Growth Memo listicle study by Kevin Indig (2026), report that numbered lists with an honest count tend to do better than loose roundups, and that more headings do not mean better pages. Treat these as directional findings from one analyst, check the original before quoting a figure, and note that results differ by field. The number in a title must be the true count of developed entries. Brief the entries first, then title the piece; never brief a number and pad to it.
- **Do not use heading count as a quality signal.** Brief the sections the piece needs, and let depth carry it.

## Schema discipline

Structured-data facts expire without warning. A search engine can remove a feature it once recommended, and a handoff built on the old fact will mislead people. Rules.

- Verify any claim about what a structured-data type earns against the search engine's current documentation before building on it. A remembered fact is a hypothesis.
- Markup that mirrors visible content (generated from the same field) is cheap and safe to keep even if its special display is retired. The content keeps its value.
- Never add markup for content that is not visibly on the page.

## Check current intel before deciding

Before writing a brief, read the newest note from `industry-intel` and the baseline note (`industry_intel.baseline_note`) for changed assumptions about AI answers, ranking behavior, or search features. Weekly notes are unverified by default. Adopt direction freely, but verify a number against the original before it reaches a published page, and never use a tier D figure.

---
name: evidence-review
description: Check claims, findings, and statistics before they reach a board, funder, client, or the public. Grades each claim (confirmed, likely, unverified, hypothesis), requires a named dated source for every number, tiers borrowed research statistics A to D, tests cause-and-effect claims, flags tool artifacts and site changes that fake a trend, and writes a pass or fail review with blockers. Use after an audit, analysis, or draft and before the report, grant text, or presentation goes out, or when someone doubts a finding.
---

# Evidence Review

Works in: Claude Code, Claude.ai, ChatGPT

Every claim that will be presented to someone who acts on it needs an evidence chain, a grade, a way for the reader to check it, and the alternative explanations you ruled out. This skill is the gate that makes sure it has one.

A claim, once written down, stops being re-checked. That is the failure this skill exists to interrupt. One unsourced line in an intake note becomes sixteen assertions across nine documents, and nobody ever goes back to the first line.

## When to run

- After an audit, analysis, or research pass, and before the action plan, report, grant text, or presentation.
- When a finding is surprising, high-impact, or will cost money to act on.
- When someone doubts a finding already in a document. Run it again on that finding.

## The grades

Grade each finding. Grade everything or grade nothing, because an ungraded claim in a document that grades others reads as verified.

| Grade | Meaning | May it go in the plan? |
|---|---|---|
| Confirmed | Two or more independent sources agree, and the reader can reproduce it. | Yes, plainly. |
| Likely | One strong source plus supporting signals. | Yes, and name the basis. |
| Unverified | One source, not yet reproduced or checked. | Yes, but labeled Unverified, with the caveat and the next check. |
| Hypothesis | A plausible explanation with no direct evidence. | No. Move it to an "Investigation needed" section, not the action list. |
| Refuted | Evidence contradicts it. | No. Keep the record so nobody reinstates it. |

These grade your finding. They say nothing about the quality of an outside study behind a borrowed statistic. Give that its own tier (below). A Confirmed finding that rests on a Tier D statistic is not confirmed. It is a repeated error.

## The evidence card

Write one per finding.

```markdown
### Finding: [short description]
**Claimed impact:** [what the finding says this causes]
**Primary source:** [tool or document, and the exact data point, with the date observed]
**Corroborating evidence:** [a second, independent source, or "None, single source"]
**Contradicting evidence:** [anything that disagrees, or "None found"]
**How to check it yourself:** [steps the reader can follow]
**Timing:** [does the timing of the cause match the timing of the effect?]
**Other explanations:** [what else could produce the same data]
**Grade:** [Confirmed / Likely / Unverified / Hypothesis / Refuted]
**Recommendation:** [include as is / include with caveats / move to investigation / remove]
```

## Extra checks for cause-and-effect claims

When a finding says one thing caused a change, check all four.

- **Timing.** Did the cause start before or at the same time as the effect? A decline that began months before the problem was found is a weak case.
- **Size.** Is the cause big enough for the effect? A small layout problem does not explain a quarter of lost visitors.
- **Other causes.** Were seasons, outside events, changes in your own campaigns, and competitors ruled out?
- **Mechanism.** Can you say, step by step, how the cause produces the effect? If you cannot, the grade is Likely at best.

A finding supported by only one source cannot be Confirmed.

## Rules for every number and fact

1. **Name the primary source, not the last document that said it.** A claim repeated in six documents is one claim. If every document cites another document, it has no source.
2. **Date every number.** Counts, scores, ratings, and rankings move. Write the date observed next to the figure, and re-check any number a recommendation depends on before it ships.
3. **Look for the newest authority first.** Search for the most recent reliable source before you form a view. If the newest source you can find is more than about two years old, treat that as a question (was it replaced?) and say what you found. Hedge in proportion to age.
4. **Rank sources of similar age.** Law and regulation outrank agency guidance, which outranks advisory letters, which outrank news summaries. Read an opinion's own caveats; some say they are not binding.
5. **A blocked page is not evidence.** A refused connection, an error page, or a paywall tells you nothing about what the source says. Do not substitute a search summary for a page you could not open. Say you could not open it, then try the publisher's own index, an archived copy, or the law the guidance interprets.
6. **Absence is reported as absence.** "No evidence found" is a finding. Do not soften it into "probably" as it moves between documents. Write a named gap, not an estimate. Remember "not found" describes where you searched, not proof that something does not exist.
7. **If your reading says a common practice is illegal, read again.** Widespread open practice is evidence. A hedged statement ("may be outside the scope") is often misread as a ban. Quote the primary text, or say whose paraphrase you are quoting.
8. **Record corrections.** When a claim is refuted, write what was believed, what is true, and when it changed. Retire the old document to a marked place with the reason. Silent correction erases the pattern, and lets the claim come back through a file nobody revisited. Check the intake files that seeded the error too.

## Borrowed statistics: the source tiers

Every figure from outside research (a market share, an adoption rate, a survey result) gets a tier. The tier travels with the figure into the deliverable.

| Tier | Meaning | Use |
|---|---|---|
| A | Original publisher's own report or release, read directly. | Quote with attribution and date. |
| B | Named research firm, figure confirmed in a reputable outlet's own reporting. | Quote, crediting both. |
| C | Real methodology, but published by a firm that sells what the data supports. | Use with a stated caveat, never as the only support. |
| D | Traces only to sites that republish figures without a link to the original. | Do not use. |

- A figure whose tier you cannot establish is Tier D by default. Drop it, or say it in words without the number.
- Assign the tier by reading the primary source, not by inference. "A named research firm" in a summary article is not a Tier A claim until you have followed the link.
- Tier D in a deliverable is a blocker. Tier C as the only support for a recommendation is also a blocker.
- Look at the meaning, not only the number. A search for one figure misses the same claim in different words ("nearly all," "about three-quarters"). Read the sentence and ask what it claims.
- Keep a short list of claims you have already caught and barred (see `assets/known-bad-claims-template.md`). Any document that contains one is blocked until it is fixed.

## Common tool traps

- **Crawler findings.** A crawling tool runs a browser that may act differently from a search engine's. Chat widgets and cookie banners can change a page title in the crawler and nowhere else. Check against the live page and what a search engine actually shows (a search for `site:yourdomain.org/page` shows its view).
- **Lab scores versus real users.** A speed test under simulated slow conditions can look far worse than what visitors experience. Use field data for severity and lab data only to find causes.
- **Estimated versus measured.** Third-party traffic and keyword numbers are modeled estimates. For impact claims, prefer your own measured data (search console, analytics).
- **Correlation.** A decline and a technical issue existing at the same time does not mean one caused the other. Check seasons, outside updates, and competitors.
- **One-time measurements.** Positions in AI answers and similar lists rotate. Present a trend with its dates and cadence, not one reading as a standing fact.
- **Wrong page.** Make sure a number belongs to the exact page named. A product page and a blog post on the same topic have separate counts. Never add them together.

## When the site changed

If anything suggests a redesign, a move to a new domain, a new content system, or a tracking change in the comparison period (a sudden cliff in conversions, a drop in direct visits over about 15 percent, a spike in impressions with jumpy positions), apply these before grading any decline.

1. Ask the owner whether a change happened and when. If no one is sure, look for the signs above.
2. State the change at the top of the review and note the comparison spans two different sites.
3. Mark each decline finding **Migration sensitivity: High** (could settle by itself, so watch for 60 to 90 days), **Low** (has traits of a real problem, such as a confirmed bug on the live page), or **None** (it is about a gap, not a decline).
4. During a change, a decline measured in one source is not enough for Confirmed. You need a measured decline, a specific non-change cause on the live page, a clear mechanism, and timing that matches the cause rather than the change. Default to Likely.

## Output

Write a dated review, for example `evidence-review-2026-11-13.md`, with these parts.

1. A summary counting findings by grade.
2. Confirmed findings, each with its evidence card.
3. Likely findings, each with a note on the basis.
4. Unverified findings, each with the caveat and the check that would settle it.
5. Findings needing investigation.
6. Removed findings, with the reason.
7. A verdict: **pass** if no blockers, otherwise **fail** with a numbered list of blockers. Blockers include any Tier D figure, any Tier C figure standing alone, any known-bad claim, any number with no named source, and any cause-and-effect claim with no mechanism.

If the user wants a data file for another program, also write the same verdict as JSON: `pass`, `findings_reviewed`, `blockers`.

Then update the plan or report. Confirmed and Likely findings go in as normal. Unverified findings go in with a visible caveat. Hypotheses go in a separate section after the action items. Every cause-and-effect claim shows its grade.

## For anything that matters

Findings someone will spend money on get a second pass by a person who did not write them and who has been told to disbelieve. Every significant error in the work this method came from was caught that way, and none by the author.

## Settings

Optional: read `evidence_standard_file` and `known_bad_claims_file` from `config.json` (copied from `config.example.json`). If missing, use this skill's defaults.

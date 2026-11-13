---
name: metric-check
description: Check a number before explaining it. For every metric that moved (traffic, leads, rankings, AI mentions, ad results), confirm the measurement is real, list the likely causes, grade each one holds, weakened or refuted with its evidence, and confirm the direction on more than one independent source before anyone claims a cause. Use when a report shows a rise or drop, when someone asks "why did this go down", before sending any monthly report, or before acting on a single platform's figure.
---

# Metric check

Works in: Claude Code, Claude.ai, ChatGPT (prompt only; the optional `scripts/check_report.py` needs Python 3).

Plain words used below:
- GA4 (Google Analytics 4, Google's free tool that counts visits to a website)
- tag (one tracking instruction, such as "report that a download was clicked")
- Google Tag Manager (a free Google tool for adding and changing tracking on a website without editing the site)
- event (one recorded action, such as a page view, a download click or a form being sent)
- session (one visit to your site)
- impression (one time a page was shown in a search result, clicked or not)
- Search Console (Google's free report of how your site appears in Google search)
- API (a way for two programs to talk, like a waiter carrying orders between you and the kitchen)
- single-source (a figure confirmed on only one platform)
- skill (a folder of written instructions an AI tool follows to do one job the same way each time)




A size and a direction are not analysis. This skill turns "traffic is down 12%" into "here is the most likely cause, here is the evidence for and against, and here is what to do". It also stops the most common mistake in small-organization reporting: believing one platform.

## When to run it

Run it on every flagged move: any number that rose or fell enough that someone would ask why. Also run it on the finished report, before it goes to anyone.

## Step 1: Define the measure

Say in plain words what the number counts. Which forms count as a lead? What is a "session"? Which engine and which tool (Google or Bing; Search Console or GA4)? Which dates, and what is the date the data runs through? A reader should never have to ask whether "leads" included a customer-service request.

## Step 2: Check the measurement before the cause

Before explaining a move, confirm it is real.

- Same time window on both sides, same length, same days of the week?
- Same definition on both sides? A tracking change, a new tag or a new lead definition inside the window is never a drop or a gain. Compare like with like, or leave the number out and say why.
- Known gaps: events not tracked yet, test traffic, spam, a tool that was down, a data feed that started late (a short history makes the "before" period look smaller than it was).
- What the metric misses: return visits, other devices, people who saw the answer but did not click.

## Step 3: List the candidate causes and grade each

Work through every one that could apply. For each, write a one-line claim, the evidence for, the evidence against, and a grade.

1. Our own changes: launches, edits, redesigns, tracking changes, new campaigns. Compare pages or campaigns we changed with comparable ones we did not.
2. Rankings and pages: did one page or a group of queries fall, or did our own pages swap places?
3. Search results pages and AI answers: are AI summaries or AI assistants absorbing clicks? Did mentions and clicks move differently?
4. Other people's changes in the same period: developers, other teams, an agency, a vendor, a campaign start or stop, a site move.
5. Outside forces: a search engine update, a seasonal pattern, a market-wide move, a competitor. Is the move specific to us or everywhere?
6. Measurement itself: the thing in step 2.
7. Chance: small numbers swing. Say how many events sit behind the percentage.

Grades:

- **Holds.** The evidence fits, other causes are weaker, and a check that could have proved it wrong did not.
- **Weakened.** Some evidence fits, some does not, or the data is thin.
- **Refuted.** Something checkable contradicts it.

Never write a cause without a grade. Missing data is "missing", never zero, and a claim with no evidence is "not verified", with what was checked.

## Step 4: Confirm direction on more than one source

Never trust one platform's figure or one platform's direction alone. See `references/multi-source.md`. The short form:

- Check up, down or flat on at least two independent sources for the same window. Sources that read the same upstream data count as one (a Search Console export, a Search Console API pull and a tool that shows Search Console numbers are all Search Console).
- Compare comparable things: organic search sessions in GA4 against clicks in Search Console for the same pages and dates. Different measures moving apart (impressions up, clicks down) is context, not a dispute.
- If comparable sources disagree, mark the figure "direction disputed" and do not act on it. Usually it is a data gap: a feed that starts late, web address variants (www or not, trailing slashes, `#` fragments), or different date cutoffs.
- If no second comparable source exists, label the figure "single-source" and say which one.
- Keyword volume or difficulty from different tools can differ by many times. Use the middle value of the tools you have and report the spread.
- Write down which sources agreed. A reader should see the check was done.

## Step 5: Say what to do

End each finding with one action and one owner, plus the next question a reader would ask. Close the report with the bottom line.

## Format for a flagged move

Use `assets/flagged-move-template.md`. One block per move:

> Move | Measure and definition | Dates and data-through date | Measurement check | Causes, each with grade and evidence | Sources checked and whether they agree | What to do, who, by when

## Habits that keep reports honest

- Keep observation separate from cause.
- State the engine and tool next to every search figure, and the AI engine next to every AI figure.
- Explain every technical term once, in a sentence, the first time it appears.
- Where money moves, give cost per result before and after.
- When someone else's decision drove a change (a budget shift, a new tag), give the best case for it first, then judge it and name the test that settles it.
- Fold follow-up answers into the report itself; state corrections ("earlier this said X; it is Y because Z").
- If a check can be done now, do it now. Do not write "worth a look".

## Optional script

`python3 scripts/check_report.py report.md` reads a report and warns when a causal sentence has no grade, a figure has no source or date, or only one source is named. It reads the file only and prints warnings. A clean pass is not proof the analysis is right.

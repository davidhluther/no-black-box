---
name: industry-intel
description: Turn a week of newsletters, feeds, and pasted items into one dated, source-checked note of post ideas and changes that matter to your organization. Use when asked for a roundup, "what happened in our field this week", topic ideas for the blog, or the weekly idea pass. Method covers gathering, triage, reading the original source, recording where a summary drifted from the source, grading confidence A to D, and listing testable claims.
---

# Industry intel: the weekly idea pass

Works in: Claude Code (full version) with the feed script in `tools/fetch_feeds.py`. Without the script, paste your items into the chat and it works in: Claude Code, Claude.ai, ChatGPT.

## What this is for

It finds what changed in your field and what your readers would want a post about, then writes it down so you can trust it later. Newsletters are the discovery layer. They tell you something happened. They are not the record of what happened. A roundup that only compresses newsletter summaries is a newsletter about newsletters, so the step that matters is opening the original source.

## Read the settings first

Read `config.json` (copied from `config.example.json`). Use `organization`, `industry_intel.feeds`, `industry_intel.window_days`, `industry_intel.notes_folder`, and `industry_intel.baseline_note`. If `config.json` is missing, ask the user for their organization's name, readers, and a few sources to watch. Never invent a feed address.

## Steps

### 1. Gather

If the feed script is available, run it from the kit folder:

```
python3 tools/fetch_feeds.py --config config.json --days 7 --out ideas/pasted/raw-bundle.md
```

It prints each source as `ok`, `empty`, or `failed`. Read the bundle. Otherwise ask the user to paste items (title, link, and a sentence).

If a source produced nothing, say so in the note. A quiet week and a broken feed look identical unless you report the status. A feed that fails two weeks in a row goes in the note's first paragraph.

### 2. Triage, then read the original sources

Sort items into substantive (a rule change, a study, a platform change, a technique, a question your readers keep asking) and noise (ads, webinars, job posts, giveaways). Drop noise without ceremony.

For every substantive item, open the original and read it: the study, the official announcement, the documentation, the practitioner's own write-up. Not the newsletter's sentence about it. If you cannot open it (paywall, login, blocked), say so in the item and mark it UNVERIFIED. Never let a summary stand in for a source you could not read.

Record where the summary drifted from the source. Quote both and say which is right. This is the most valuable output of the step. Summaries misquote statistics and merge two different things into one often enough that a decision built on one can go wrong.

### 3. Check against what you already know

Open the baseline note (`industry_intel.baseline_note`) and the last few dated notes. For each substantive item decide which of three things it is.

- **Conflict.** It contradicts something you banked. Say so in the item, compare the quality of the two sources, and say which should win.
- **Supersession.** It is newer or stronger research on the same question. Update the baseline in place with the old figure struck through, in the same pass.
- **Corroboration.** It agrees. Say so; it raises your confidence in the banked claim.

A conflict left unmentioned is how two people end up citing opposite numbers.

### 4. Grade confidence

Tag every item.

| Tier | Meaning | How to use it |
|---|---|---|
| A | The organization's own publication, read directly | Quote with attribution |
| B | A named organization, confirmed by a reputable outlet's direct reporting | Quote, naming both |
| C | A vendor publishing numbers about the thing it sells; real method, but self-interested | Use with a stated caveat, never as the only support |
| D | Traced only to articles that repeat each other, with no original | Do not use |

Use OPINION as a separate tag for a practitioner's judgment that is not research. A number you cannot trace to A, B, or C does not go in anything you publish, however often it is repeated.

### 5. Write the note

Save to `industry_intel.notes_folder` as `YYYY-MM-DD-weekly-roundup.md`, dated the day you run it. Use this order every time.

1. **Key takeaways.** Three to six bullets. Each is a finding, not a topic label. If a takeaway is a retraction (a number you can no longer cite), say so.
2. **What happened.** One paragraph describing the shape of the window. A quiet week is a legitimate paragraph. Write it plainly.
3. **Recommendations.** What to do differently, stated as recommendations and only where the evidence supports them. It is allowed to disagree with a source.
4. **What to do with it.** A table with action, where it lands (which post, page, or person), effort, and urgency. "No action, deliberately" is a legitimate row.
5. **For our organization.** Written from the organization's own situation in `config.json` and what the user tells you about it. It may say "nothing this week changes what we should do." A section that always finds something stops being read.
6. **Items.** One section per item with its confidence tier, what the source actually says (sample size, dates, scope, stated limits, with the real link), the drift if any, the impact on this organization in concrete terms, and a specific recommendation or an explicit "no action".
7. **Honesty ledger.** Which sources were read and which were not, and why, plus a per-source count table.

Combine duplicates. The same study arrives through three newsletters; write one item and list the sources. Mark ad-hoc items the user pasted as "(from the user)". Never include private information about the organization's clients, donors, or staff.

### 6. Write down the testable claims

Next to the note, save `hypotheses-YYYY-MM-DD.json` with a list. Each entry has these keys and no others.

- `claim`: one sentence, in your own words, of what would change for a site like yours.
- `source`: the source's name as the note names it.
- `date`: the source's publication date, `YYYY-MM-DD`.
- `tier`: `"A"` or `"B"` only. Never write C or D here.
- `measurement`: the number in your own data that would show it, in plain words (for example, "Search Console clicks on how-to searches"), or `"none identified"`.
- `item`: the item's number in the note.

Write an empty list when no A or B item makes a testable claim. Never pad it.

### 7. Hand the ideas on

Add each post-worthy idea to the Ideas sheet or `ideas` list with its source link and tier. Ideas then go to `topic-screen`.

## Monthly baseline refresh

On the first run of each month, check the baseline note for figures that may have gone stale (for example, which AI tools people use and how, or how buyers in your field research). Look for newer editions of the same sources and for new datasets. Update figures in place with the date checked, even when nothing changed ("checked, no new data" is information). Trace every new number to its primary source before it enters the file. Re-grade sources each time. If a refresh changes a recommendation, not just a number, tell the user.

## Rules that keep this honest

- A scheduled run is not a shorter run. If this runs on a schedule, it does the whole sequence and records what happened, including failures, in a log the user will see.
- Never present an unread source as read.
- Never cite a tier D figure.
- If you cannot tell whether something is true, write "not verified" and what you checked.

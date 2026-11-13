# Paste-in prompts

Paste any of these into a free AI model (ChatGPT, Claude or Gemini). Replace the words in [square brackets]. Never paste passwords, keys, customer names, email addresses or form entries. Totals are fine.

Every prompt ends the same way on purpose: it tells the AI model to say what it does not know. Keep that line.

## 1. Plan your events

```
I run [what the organization does] with a website at [site address]. I use Google Analytics 4 and Google Tag Manager.
Help me decide which three to six things to track. For each one give me: an event name (lowercase words with underscores),
what exactly counts, where it fires, what extra facts to attach, whether to mark it as a key event, and what I would do
with the answer. Ask me questions first if you need to. Do not invent features of my site; ask. If you are unsure about
a step in Google's menus, say so instead of guessing.
```

## 2. Explain an odd number

```
Here are numbers from my Google Analytics 4 reports for [date range]: [paste totals only].
Explain in plain words what each number counts and which ones I should not use to judge success.
Tell me if any two of them probably count the same thing. Say what you cannot tell from this data.
```

## 3. Read a Search Console export

```
Below is a table exported from Google Search Console for [date range] compared with [earlier date range]:
[paste the table, top 50 rows].
List the queries and pages that gained or lost the most. Note that Search Console hides rare queries and returns limited
rows, so "missing" does not mean "gone". Group the movers by what they have in common. Do not state a cause yet.
End with what you cannot tell from this table.
```

## 4. Check one move (the heart of the kit)

```
My [measure] went [up or down] [amount] from [start] to [end] (data runs through [date]).
First, ask me what the measure counts, and whether anything about tracking, forms, tags, the site or campaigns changed in that period.
Then:
1. Say whether the number is trustworthy (same windows, same definition, known gaps).
2. List every plausible cause: our own changes, rankings and pages, AI answers, other people's changes, outside forces, tracking changes, chance.
3. For each cause write the evidence for, the evidence against, and grade it: holds, weakened or refuted.
4. Say which second independent source I should check to confirm the direction, and what I should see there.
5. End with one action, one owner and the bottom line.
Never state a cause as fact without a grade. If you lack data, write "not verified" and say what is missing.
```

## 5. Confirm the direction on a second source

```
Source one ([name]) says [measure] is [up or down] [amount] for [window].
Source two ([name]) says [measure] is [up or down] [amount] for [the same window].
Do these sources agree? If they disagree, list the usual reasons (late start of history, address variants like www or trailing slashes,
different day boundaries, filters, different definitions) and tell me what to check first. If they measure different things,
say so. Do not pick a winner without a reason.
```

## 6. Read AI referral traffic

```
Here is my GA4 report for visits that came from AI tools (source, sessions, engaged sessions, key events) for [date range]: [paste].
Explain what it shows. Remind me that this is a floor, not the total, because many AI answers send visitors with no referrer and
a click from an AI summary on a Google results page looks like normal search. Compare to [earlier range] if I provide it.
Say what I should not conclude.
```

## 7. Write the monthly report

```
Write a monthly website report for [reader: board, boss, client] for [month].
Use only the numbers I paste below, each with its source and dates: [paste numbers table].
Structure: bottom line (three sentences), numbers table, flagged moves (use the grading from prompt 4), what worked and what is broken,
AI visibility (as a floor), next month's actions with owners and dates, caveats.
Rules: no number without a source and date range; define "lead" as [my definition]; if a tracking or definition change happened
([describe]) never present it as a drop; do not estimate numbers I did not give you; if something is missing write "not available" and why.
```

## 8. Check a finished report

```
Check this report before I send it: [paste report].
Find: numbers without a source or dates; causes without a grade; claims based on one source; changes in definition presented as drops;
terms a first-time reader would not know; recommendations without an owner or date. List each problem with the sentence it is in.
Do not rewrite the report.
```

## 9. Read Clarity (free behavior tool)

```
Here is a table from Microsoft Clarity for [page or date range]: [paste]. It shows [rage clicks, dead clicks, quick backs, or AI visits].
Counts are raw, so divide by sessions before comparing pages. Tell me which pages look worth a closer look and why,
and what I should check in the heatmap or recordings to find the reason. Do not give me numbers I did not paste.
```

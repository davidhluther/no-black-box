# Predict, then grade

A pattern for any recurring work that makes claims about the future or about its own impact. Publish a prediction that can be proved wrong, store it where it cannot be edited, capture what actually happened, grade the pair on a fixed schedule, and publish the scoreboard with the misses in it.

The claim underneath: credibility is a graded track record and nothing else. A forecast nobody checks is an opinion with a chart.

## Declared priors are the entry fee

The step people skip is publishing numbers before they are any good. A first model can be five coarse multipliers, each written down as a "declared belief, corrected by grading": a prior (a starting guess, held until evidence replaces it). Each one is checkable, because it was stated before the outcome. The alternative, waiting until the model is good before saying anything, never produces a track record. There is nothing to grade and no date to count from.

Every prediction file carries its own audit trail: the baseline, the adjustments applied, and where the baseline came from. A "cold start" field lets a prediction admit how little it knows.

## The mechanism

| Stage | What it is | Example shape |
|---|---|---|
| Predict | A dated file per prediction that is never edited, holding its inputs and reasoning | `forecast/2026-11-13.json` |
| Capture the actual | A separate capture on its own schedule, appending samples | `actuals/2026-11-13.json` |
| Grade | A scoring function with no side effects that joins stored prediction to stored actual | `compare.py` writing one comparison file per day |
| Roll up | A scoreboard rebuilt from all comparison files every run, never appended to | `scores.json` |
| Publish | A page, a file or a report anyone can read | the scoreboard |

## Rules that cost something to learn

1. **Fix the rubric before observations land.** A rubric written after you have seen the results is not a rubric. Build the scorer before the season it will grade.
2. **Grade yesterday before predicting today.** A job that predicts first and grades second will eventually grade against its own updated priors.
3. **Gate on output, not on the clock.** A job that runs only "when the hour equals 12" silently skipped two whole days when the scheduler fired it at odd times. Run if today's prediction file does not exist yet. This is the same rule as treating a missed slot as a failure.
4. **Slice by condition.** Score a holiday weekend against an ordinary Tuesday, not one blended number. Blending hides the only cases anyone cares about.
5. **Require a minimum sample before calling it a record.** One shared constant (nine scored days, in the project this came from) decides whether a source shows as an established record or as "gathering data".
6. **A missing actual is a skip, never a zero.** An empty file creates a ghost row and lets a partial run seed a phantom day. A blank means the question went unanswered, not that it was answered wrongly.
7. **Rebuild rollups, do not append to them.** Appending froze old rows after a rescore and let the per-day numbers drift out of sync with the totals until one page showed two different averages. Keep a test whose only job is to fail if that returns.
8. **Backfill, because a gap is permanent.** Data sources often post one to five days late, and nothing revisits a day on its own. Sweep the last two weeks daily.
9. **Never overwrite an original capture.** Corrections write a sibling file and the grader prefers the sibling. If a backfill's validation fails for a date, log and skip it.
10. **Disclose recalibrations** with a date, a reason and a full rescore of history.

## Publishing the misses is the product

A scoreboard only works if it is allowed to be bad. State plainly when a source you track is graded against its own provider's records, because that cuts both ways. Commit a time to the record before an event so there is no room to nudge it afterward. The cost is that the payoff is deferred: the newest loop has little graded history, and its priors are still first guesses. You adopt this knowing the credibility arrives later, and the discipline is what gets you there.

## Where to use it

- Content work: record a predicted ranking position or traffic band per piece, by a stated date, before publication. The monthly report grades last wave's predictions instead of only reporting what happened.
- Grant pipelines: a stated probability per prospect, graded at each decision date.
- Attendance or demand estimates for a decision, graded against what happened.

In each case the value is less the accuracy than the record. A graded prior is an argument, and an ungraded one is an assertion.

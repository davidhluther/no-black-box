---
name: visibility-diff
description: Compare two scored AI visibility runs cell by cell with a small [script](../../glossary.md#script) that refuses to compare runs from different [question sets](../../glossary.md#question-set) or different collection methods. Produces a plain table of what changed per AI product and question. Use before writing any month-over-month note, so the model reads exact rows instead of eyeballing two long files.
---

# Visibility diff

Works in: Claude Code (full version), because it runs a small [Python](../../glossary.md#python) script. Without Claude Code, filter your Results tab by run and compare by hand, following `aeo-trends`.

## Why a script

Long exports are easy to misread, and a model reading two big files by eye can attribute a count to the wrong cell. The script does the matching exactly. You, or your model, interpret the table afterward.

## Use

Export the Results tab of each run as CSV (File, Download, Comma-separated values), then:

```
python3 scripts/visibility_diff.py older_results.csv newer_results.csv
python3 scripts/visibility_diff.py older_results.csv newer_results.csv -o analysis/diff.md
```

## What it refuses to do

It stops with a plain message when the two files used different question set versions, when either file mixes versions, or when one run is an app run and the other an [API](../../glossary.md#api) run. That refusal is the point: such numbers do not mean the same thing. Fix the cause (usually by comparing the right pair of runs), do not override it.

## What it reports

Per AI product, the number of cells scored in both runs and how many were visible (named, cited, or both) before and now. Then every cell whose outcome changed, with before and after. Brand-check (BV) and control (CT) questions are left out. Cells present in only one run are counted and not compared.

## How to read it

Counts only. With about twenty headline questions per product, a change of one or two cells is within normal answer-to-answer variation. Report changes you can see, hold causes as hypotheses, and note any model version change from the run headers before crediting your work. Paid platform exports can be compared the same way: same question set, same method, same dates, or do not compare.

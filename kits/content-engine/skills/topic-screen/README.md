# topic-screen

A cheap check that runs before you spend time on a brief. It screens a list of candidate topics against your existing content, a minimum search demand, and each other.

```
python3 topic_screen.py --candidates my-topics.csv --config config.json
```

`--config` takes your `config.json` (it reads the `topic_screen` block) or a small file holding only that block.

## What it checks

1. **Existing content.** It folds simple plurals and scores overlap against your sitemap, your queue export, and your saved briefs. This is evidence for you to look at, never a verdict, because similar titles do not prove the same job.
2. **Demand floor.** Anything under the configured monthly searches is flagged unless the candidate carries a written reason. A deliberate bet on a small topic is fine; it should say so.
3. **Duplicates inside the list.** Every candidate is compared with every other candidate.

A source it could not reach is reported as INCOMPLETE and never counted as clean.

## What it does not do

It does not find two topics worded differently that do the same job. A person reads the nearest matches and decides. It also cannot tell that a keyword means something else (an acronym that is also the name of a band, for example), so check what a search for the phrase actually returns.

## Candidates file

CSV or JSON with `title`, `keyword`, and optionally `volume`, `rationale`, and `id`. A Google Sheet exported as CSV works.

## Settings

| Key | Meaning |
|---|---|
| `demand_floor` | Monthly searches below this are flagged (default 100) |
| `existing_threshold` | Overlap score against existing content (default 0.8) |
| `dedupe_threshold` | Overlap score between candidates (default 0.8) |
| `sitemap_url` or `sitemap_file` | Your live content list; the file wins if both are set |
| `path_filter` | Only count sitemap addresses containing this text, for example `/blog/` |
| `board_dump` | Your Queue tab exported as CSV (columns `title`, `keyword`, `stage`), or a JSON list of `{name, kw, stage}` |
| `briefs_dir` | Folder of saved briefs, named like `brief_some-topic.md` |
| `blocking_stages` | Queue stages that count as already claimed. Leave "Idea" out; an idea does not block |

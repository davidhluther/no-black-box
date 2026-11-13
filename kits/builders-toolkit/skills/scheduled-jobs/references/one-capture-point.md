# One capture point

A pattern for any scheduled job that pulls data from outside, especially data that costs money or is capped by a quota (a limit on how many requests you may make).

## The rule

Each external dataset is pulled by exactly one script, on a schedule, and that script saves its result into the project as a file. Nothing else calls the outside source. Every consumer (a web page, a report, a model, a later project) reads the saved file. The repository is the API: it is the one interface everything else uses, and pulls never multiply with the number of consumers.

## Why

Without it, cost scales with consumers and not with data. A second page that wants the same numbers doubles the bill. A preview copy of the site triples it. Each individual call looks reasonable, so the failure is quiet. With one capture point, a handful of feeds can run for a few dollars a month, however many pages read them.

Three side benefits matter as much as the money.

1. **Secrets stay in one place.** Only the scheduled capture authenticates, so keys need not reach a browser, a hosting service or a laptop.
2. **Cadence is one setting.** How often to pull lives in one file per source, so tuning cost is a one-line change.
3. **History accrues for free.** Every pull is saved, so you get a time series nobody designed. Start capturing before the page that will use it exists.

## What a capture script promises

| Habit | Why |
|---|---|
| Fail soft. Always exit 0 on a vendor outage, print a warning, and still write the file with `"fetch_ok": false`. | An outage must not turn the whole daily run red. A red that always appears stops meaning anything. Note the tension with the rule that a failure must be recorded: the capture's own file says it failed, and the outcome row records the same. |
| Stamp every file with `fetched_at`, a human-readable `source`, and `fetch_ok`. | Consumers decide whether to trust a file by its stamp. |
| State the pacing next to the code (a spacing constant with a comment saying why). | Rate limits are facts about the vendor, so keep them with the vendor's code. |
| Use only the standard library. | A capture that breaks on a dependency upgrade breaks silently at 6 a.m. |
| Merge, do not clobber. Read the existing day, append, and start fresh if the old file is corrupt. | Several captures may feed one file. |
| Carry the caveats in the data (a `notes` list saying what the numbers are not). | The consumer three months from now is you, and you will have forgotten. |
| Write to a temporary file, then rename it into place. | A crash mid-write must not truncate saved data. |

## The consumer's side

Consumers have no network access at all. Every input is a path in the project, loaded through one helper that swallows failures and names what was missing. A calculation with no side effects plus a saved sample file is a unit test. A calculation that calls a vendor is an integration test with a monthly bill.

## Where it breaks, and the question that catches it

The violations cluster on request paths and build paths, never in capture scripts: a component that calls a weather service from every visitor's browser, a page that fetches a feed at build time with nothing saved in between. The diagnostic is a question. **Does this call happen once a day, or once per visitor?** Anything in the second group scales with traffic, which is the thing the pattern exists to prevent.

Interactive lookups, where the visitor's input decides the query, are a real exception. Name them as one deliberately and do not force a capture point onto them. If several scripts touch a free, keyless source, that is fine too. Hold the line where it costs money.

A saved pull still needs a freshness gate. A five-day-old inventory had half its rows stale. The answer is to check the stamp, not to replace the file with live calls from every consumer.

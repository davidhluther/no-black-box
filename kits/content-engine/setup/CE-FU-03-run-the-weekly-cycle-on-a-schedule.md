# CE-FU-03: Run the Weekly Cycle on a Schedule

You'll end with the unattended parts of the cycle running on a [scheduler](../glossary.md#scheduler), every run written to a log, retries built in, and a check that flags a missed slot the same day. The parts that need judgment stay with a person. Allow about three hours.

What can run without a person: the [feed](../glossary.md#feed) fetch, the [Search Console](../glossary.md#search-console) export, and the [gate](../glossary.md#gate) audit on recently published pages. They are scripts that read and write files. What can't: briefing, drafting, publishing, and anything that changes the [queue](../glossary.md#queue). The draft-queue [skill](../glossary.md#skill) refuses to run unattended on purpose, and publish never runs from a schedule. Keep that line.

1. **CE-FU-03-1.** Write your job list into `schedule.jobs` in `config.json`. Each job has a `name`, an `every_days` cadence, a `grace_days` allowance, and an `owner` role from your owner table. The starting list is feeds, search-console-export, and tell-audit.
   You'll know it worked when the names match what you'll pass to `--job` in the next steps, spelled the same. A name mismatch is the most common reason a check says MISSED for a job that ran (E06).

2. **CE-FU-03-2.** Test the log wrapper with a harmless command. From the kit folder:

   ```bash
   python3 tools/job_log.py run --job selftest -- python3 --version
   ```

   You'll know it worked when it prints the [Python](../glossary.md#python) version and `ops/job-log.csv` now has one line with status ok. The log records the job name, start time, seconds, attempt number, and exit code. It never records the command, its output, or any key.

3. **CE-FU-03-3.** Wrap the feed fetch and schedule it for Monday morning. The wrapper retries once after a minute, then records a failure. Put this line in your [scheduler](../glossary.md#scheduler) (on a Mac or Linux machine, a [cron](../glossary.md#cron) entry; on Windows, Task Scheduler), replacing the path with the full path to your kit folder.

   ```bash
   0 6 * * 1 cd /path/to/no-black-box-main/kits/content-engine && python3 tools/job_log.py run --job feeds --retries 1 -- python3 skills/industry-intel/tools/fetch_feeds.py --config config.json --days 7 --out ideas/pasted/raw-bundle.md
   ```

   You'll know it worked when, after the first scheduled Monday, the log shows the feeds job and `ideas/pasted/raw-bundle.md` has a new date. A log with no line for Monday is E06. A feed that comes back empty or FAILED inside the bundle is E05; a quiet week and a broken feed look the same unless the bundle says which.

4. **CE-FU-03-4.** Schedule the other two unattended jobs the same way. If a person exports Search Console by hand, skip the first and keep the weekly reminder. The gate audit scores pages published in the last two weeks against your thresholds and writes a [CSV](../glossary.md#csv); it needs two add-ons, installed once with `pip install requests beautifulsoup4`.

   ```bash
   30 6 * * 1 cd /path/to/no-black-box-main/kits/content-engine && python3 tools/job_log.py run --job tell-audit --retries 1 -- python3 skills/tell-scorer/scripts/score_batch.py --sitemap https://www.example.org/sitemap.xml --include /blog/ --selector article --max-age-days 14 --thresholds style/gate-thresholds-example-site.json --out measure/tell-audit.csv
   ```

   You'll know it worked when `measure/tell-audit.csv` updates and the log shows tell-audit. Lines containing EXTRACTION PROBLEM mean the selector is wrong for that site (E18).

5. **CE-FU-03-5.** Schedule the daily check and send its result somewhere a person sees it. The check exits 0 when every job is inside its slot, 1 when any job missed, and 2 when the job list is empty. Wire a nonzero exit to whatever your team already watches (a channel message, an email, a ticket). The kit supplies the check; the alert is your tooling.

   ```bash
   30 7 * * 1-5 cd /path/to/no-black-box-main/kits/content-engine && python3 tools/job_log.py check --config config.json || echo "content engine: a job missed its slot"
   ```

   You'll know it worked when a deliberate miss (next step) produces a message to the job's owner. A missed slot counts as a failure even when older data is still good enough to use, so the owner reruns the job by hand the same day and writes why in the team channel.

6. **CE-FU-03-6.** Run an alarm drill. Add a job named `drill` to `schedule.jobs` with `every_days` 0 and `grace_days` 0, then run:

   ```bash
   python3 tools/job_log.py check --config config.json
   ```

   You'll know it worked when the output shows drill as MISSED, the command exits 1, and your alert fires. Remove the drill job afterward. If nothing alerts, fix that before trusting the schedule (E06).

7. **CE-FU-03-7.** Set up the person-present weekly routine. The order is fixed because each step reads the one before it.
   - Monday: ask [Claude Code](../glossary.md#claude-code) to "Run industry-intel on ideas/pasted/raw-bundle.md", then open the original source for every item you plan to use.
   - Then screen the candidates: `python3 skills/topic-screen/topic_screen.py --candidates ideas.csv --config config.json`, with the queue exported to `queue/queue-export.csv`. A source marked INCOMPLETE is E19.
   - Then "Run content-handoff". Its verdict (CLEAR, DEGRADED, or BLOCKED) decides what happens next. A BLOCKED note lists what to fix first, and if the schedule failed, the note will say the inputs are stale. draft-queue refuses to start on a note that is missing, over three weeks old, or BLOCKED (E13).
   - Then "Run content-brief" for the topics that passed. Check each brief with `python3 skills/draft-queue/scripts/check_brief.py briefs/brief_<keyword-slug>.md`; a BRIEF PARTIAL message lists what is missing (E20). Then "Run draft-queue" for Planned items, one operator at a time.

   You'll know it worked when each Monday leaves a notes file, a screen result, a [handoff note](../glossary.md#handoff-note), and at least one brief or a stated reason there isn't one.

8. **CE-FU-03-8.** Handle several sites and markets. Keep one config per site or market (CE-FU-01-5), one queue per site, one style guide and rules file per language, and one publish site file per site (`skills/publish/sites/<site-id>.json`). Run each unattended job once per config with its own job name, such as `feeds-example-site`, and list each in `schedule.jobs`. Stagger start times by 15 minutes so a slow site doesn't block the next. The shipped word lists in article-check and tell-scorer are English, so for another language use your own rules file or skip those two gates and keep evidence-review. Add `owner`, `site`, `market`, and `content_type` columns to the right of the queue's existing columns, using `new post` or `refresh` as the content type, and give every item a single owner; two people picking the same Planned item is E15. The file `references/team-notes.md` inside the draft-queue skill spells out the claim rule.
   You'll know it worked when the log shows one line per site per job, and each queue row names one owner.

If something fails, go to the [fixes table](../fixes.md).

Next, [CE-FU-04, owners, gates, and reporting to leaders](CE-FU-04-owners-gates-and-reporting-to-leaders.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CE-FU-03-4). Run `python3 support/doctor.py content-engine` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

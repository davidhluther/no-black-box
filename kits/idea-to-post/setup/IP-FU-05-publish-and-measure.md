# IP-FU-05: Publish and Measure

The publish step always starts with a dry run (a practice pass that shows what would happen without doing it) and stops for a person to confirm. It never runs from a schedule. Measurement can run on a schedule, as long as failures are recorded and shown to you. Allow about an hour.

1. **IP-FU-05-1.** Set `publish.adapter` in config.[json](../glossary.md#json). Use `manual-copy-package` to get a ready-to-paste package, or the name of an adapter the publish [skill](../glossary.md#skill) supports for your site's software. Keep `dry_run_first` and `require_human_confirmation` set to true.
   You'll know it worked when config.json saves and the publish skill's practice run reads it. A missing or broken file is E16.

2. **IP-FU-05-2.** Say: "Run publish in dry-run mode for <title>." Read the summary of what would be created.
   You'll know it worked when the summary lists the title, [slug](../glossary.md#slug), links checked, and images. If it refuses because a field is missing, it's E19.

3. **IP-FU-05-3.** If the summary is right, say "confirm". A person (you) confirms every time. Then open the live page on a phone and click every link.
   You'll know it worked when the live page matches the summary. Record the live address and date in the [Queue](../glossary.md#queue) and set the stage to Live.

4. **IP-FU-05-4.** Ask for [indexing](../glossary.md#indexing): in [Search Console](../glossary.md#search-console), request indexing for the new address.
   You'll know it worked when Search Console confirms. If the page is still missing from search after several weeks, it's E21.

5. **IP-FU-05-5.** At two, six, and 12 weeks, say: "Run gsc-read for <page>, then ai-traffic-classifier, then clarity-analytics if connected." Record the numbers on the Measure tab or in the measure folder.
   You'll know it worked when each checkpoint has a file or row. The ai-traffic-classifier skill flags searches that look like long conversational questions, a sign of AI-driven traffic that analytics tools cannot label.

6. **IP-FU-05-6.** Say: "Run content-refresh part one." It ranks old posts worth updating. For one, run part two with its [refresh](../glossary.md#refresh) brief.
   You'll know it worked when a refresh draft with the _refresh suffix appears in the drafts folder.

7. **IP-FU-05-7.** (Optional.) Schedule weekly runs of the idea fetch and the Search Console pull with your computer's own scheduler or [Claude Code](../glossary.md#claude-code)'s scheduling features; check their current documentation for how. Never schedule the publish step. Each scheduled run must write a line to a log file you will see, including when it fails.
   You'll know it worked when each Monday adds a log line. A Monday with no new line means the schedule failed; this is E20.

8. **IP-FU-05-8.** Run `python3 support/doctor.py idea-to-post` once a month.
   You'll know it worked when the code ends in OK.

If you are stuck, go to the [fixes table](../fixes.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

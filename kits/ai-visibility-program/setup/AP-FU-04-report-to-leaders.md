# AP-FU-04: Report to Leaders

Time, about three hours the first month and about 90 minutes a month after that. You clean each site's run, run the analysis chain, set the sources side by side, and write one leader report that answers "how do we know". The rule that comes first is that no number goes into the report until the [noise audit](../glossary.md#noise-audit) has cleaned it.

1. **AP-FU-04-1.** Clean every site's run. In [Claude Code](../glossary.md#claude-code), from the program folder, ask: "Use the answer-noise-audit skill on sites/example-us/runs/<month>-api." Then do the repeat test the skill describes: pick up to five questions per site, ask each three more times in fresh chats on one product, and count how often the same businesses are named. Repeat for each site.
   You'll know it worked when each site has `analysis/<month>-api/noise-audit.md` with raw and clean counts side by side, every removal tied to a quoted line, and a verdict on how much the look-alikes mattered. Write the repeat-test result down as the site's noise level. If a site has no [same-name](../glossary.md#same-name) list, the audit labels its numbers "not preflighted". Go back to guide AP-FU-02, step 3.

2. **AP-FU-04-2.** Run the analysis chain for each site: "Use the aeo-audit skill on sites/example-us/runs/<month>-api." It runs visibility, mentions, [citations](../glossary.md#citation), competitive, platforms and trends in order and writes `analysis/<month>-api/summary.md`.
   You'll know it worked when each summary names the file behind every number and says "[baseline](../glossary.md#baseline)" for a first run. If a skill reports "skipped", the summary carries that forward and you read why.

3. **AP-FU-04-3.** From the second month on, compare each site with its own last month:
   ```
   python3 scripts/visibility_diff.py sites/example-us/runs/2026-11-api/scored.csv sites/example-us/runs/2026-12-api/scored.csv
   ```
   Then ask for the `aeo-trends` skill on the same pair. Compare a site only with itself, and only on the same [question set](../glossary.md#question-set) version.
   You'll know it worked when you get a table of cells that changed. If it says "Not comparable", the version or method differs, and you do not override it (E39 in the [single-site fixes](../../ai-visibility/fixes.md)). A change of a cell or two is inside the noise level you wrote down in step 1. Say so in the report.

4. **AP-FU-04-4.** Set the sources side by side. Export the month's [Search Console](../glossary.md#search-console) and [Bing Webmaster Tools](../glossary.md#bing-webmaster-tools) queries for each site into `imports/`, run `ai-traffic-classifier` on the Search Console file ("Use the ai-traffic-classifier skill on imports/search-console-queries.csv"), and add the [GA4](../glossary.md#ga4) AI-channel count and any paid platform's export. Then ask: "Use the unified-visibility skill on this month's analysis and imports."
   You'll know it worked when `analysis/unified-<month>.md` shows each source's direction and plain count, with no blended score. Where sources disagree, the skill lists the usual reasons first: different questions, competitors, products or model versions, collection methods, dates or locations. Copy each disagreement and its reason into `reports/disagreements.md` with the date. If you cannot name a reason, write "none found" and treat the change as a lead, not a finding (E44).

5. **AP-FU-04-5.** Write the leader report from `full/leader-report-template.md`. Ask Claude Code: "Fill in reports/leader-report.md from the template, using only the analysis files for this month. Show one row per site, never a blended total. Put the noise level and the disagreements section in, and cite the file behind every number."
   You'll know it worked when someone outside the program can follow it, and every number traces to a file under `analysis/`. If the report has a number with no source file, take it out.

6. **AP-FU-04-6.** Turn the findings into fixes with an owner. Ask: "Use the aeo-implement skill on sites/example-us." It puts listings and plain-language pages first, drafts [robots.txt](../glossary.md#robotstxt) and [llms.txt](../glossary.md#llmstxt) changes only if you want them, and writes a handoff. It publishes nothing. File each handoff item as a ticket for the web team, with an owner and a date.
   You'll know it worked when each ticket links the handoff and names who applies it. After the change is live, fetch the page or `robots.txt` yourself and write the date in `reports/fixes-log.md`. A fix that is not verified live is not counted in next month's trend (E47).

7. **AP-FU-04-7.** Hold the monthly review and keep a decisions log in `reports/decisions.md`: what leaders asked, what the report answered, which hypotheses you will test next month, and any question changes. Any retired or added question bumps that site's version in `config.json` and gets a line in its `CHANGES.md`, and starts a new [series](../glossary.md#series).
   You'll know it worked when next month's review can open the log and see what was promised. Hypotheses are things to test, not promises, and the report says once what the data cannot see: conversations that never produce a click or a mention you can find.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AP-FU-04-4). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

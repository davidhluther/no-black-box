# AV-FU-06: Analyze, Compare, and Repeat

Time, about 20 minutes plus reading. You run the analysis skills once, then settle into the monthly loop.

1. **AV-FU-06-1.** Run the whole chain. In [Claude Code](../glossary.md#claude-code) ask: "Use the aeo-audit skill on my latest run." It runs the [noise audit](../glossary.md#noise-audit), then visibility, mentions, [citations](../glossary.md#citation), competitive, platforms, and trends, and writes `analysis/<run>/summary.md`.
   You'll know it worked when the summary names its sources for every number and says "[baseline](../glossary.md#baseline)" if it is your first run. If a skill reports "skipped", the summary carries that forward. Read why.

2. **AV-FU-06-2.** Read the summary. Check that every number can be traced to a file under `analysis/<run>/`. Check that it says whether the run was preflighted.
   You'll know it worked when you can explain each number in a sentence. If a number looks wrong, open the matching skill's file and see which rows it counted.

3. **AV-FU-06-3.** Next month, repeat guide AV-FU-05 with the same [frozen](../glossary.md#frozen) questions. Then compare:
   ```
   python3 scripts/visibility_diff.py runs/2026-11-api/scored.csv runs/2026-12-api/scored.csv
   ```
   You'll know it worked when it prints a table. If it says "Not comparable", the [question set](../glossary.md#question-set) version or method differs. Do not override it. See E39.

4. **AV-FU-06-4.** Put your sources together. Export your [Search Console](../glossary.md#search-console) queries and run `ai-traffic-classifier` on them (ask Claude Code, "Use the ai-traffic-classifier skill on queries.csv"). Combine it with the [GA4](../glossary.md#ga4) count from AV-FR-07 using `unified-visibility`. Do not add them together.
   You'll know it worked when the report shows each source side by side and explains any disagreement before it recommends anything.

5. **AV-FU-06-5.** Optional. Turn the findings into website fixes with the `aeo-implement` skill. It starts with non-technical fixes such as listings and a plain services page, drafts [robots.txt](../glossary.md#robotstxt) and [llms.txt](../glossary.md#llmstxt) only if you want them, and writes a handoff for whoever manages your site. It publishes nothing.
   You'll know it worked when you have a handoff file you could hand to a web person.

6. **AV-FU-06-6.** Paid tracking platforms are optional and the kit never needs one. If you use one (Ahrefs Brand Radar, Peec AI, AirOps, or another), export its results and add them to `unified-visibility`. Ask what question set it tracks and how it guards against [same-name](../glossary.md#same-name) confusion before trusting its numbers.
   You'll know it worked when its numbers sit beside yours with the differences explained.

7. **AV-FU-06-7.** Keep the loop. Put a monthly reminder in your calendar. If you automate any part of it, make sure it tells you when it fails or misses its slot. A silent failure looks exactly like a quiet month. If a month is missed, write down that it was missed and why.
   You'll know it worked when next month's run happens on schedule or the miss is written down.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FU-06-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

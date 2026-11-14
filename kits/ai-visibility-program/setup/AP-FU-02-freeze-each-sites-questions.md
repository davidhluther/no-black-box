# AP-FU-02: Freeze Each Site's Questions

Time, about 45 minutes for the first site and 20 for each one after it. Each site gets its own folder, its own [same-name](../glossary.md#same-name) list and its own [frozen](../glossary.md#frozen) [question set](../glossary.md#question-set). The method is the single-site kit's, so this guide links to those steps and spells out the team changes: one shared B2B template, collisions across sibling brands, and a version label per site.

1. **AP-FU-02-1.** Make a folder for each site and give it a settings file. For each entry in `sites`, run the first line below (change `example-us`), then copy the single-site settings file into it.
   ```
   mkdir -p sites/example-us/runs sites/example-us/analysis
   ```
   Ask [Claude Code](../glossary.md#claude-code): "Copy config.example.json from the ai-visibility kit into sites/example-us/ as config.json." Open that file and fill the `business` block: the brand as people say it, the kind of company, the main service or product, the market in `town` and the wider region in `region`, the owner or lead executive, the domain, and up to three competitors. Leave `question_set.version` as `v1` for now.
   You'll know it worked when each site folder holds its own `config.json` and no value still reads Maple or example. If the file is rejected later as invalid, it's E33 in the [single-site fixes](../../ai-visibility/fixes.md).

2. **AP-FU-02-2.** Write the team's question template once. The shipped template is worded for a local consumer business. A B2B team rewrites the wording and keeps the structure: 28 questions, the same codes (LD, PF, CE, CH, CT, BV groups), the same placeholders. Ask Claude Code: "Copy references/questions-template.md to templates/questions-template.md, then rewrite each question the way a buyer at a company like ours would type it to an [AI model](../glossary.md#ai-model), keeping every code and every placeholder." Buyers type casually, so keep the wording casual. Have someone from sales or support read them.
   You'll know it worked when the file still has 28 lines that start `### ` and a curly-bracket placeholder only where the original had one. Do not name your own brand in any question outside the BV group. If the fill [script](../glossary.md#script) complains about a name, it's E06 in the single-site fixes.

3. **AP-FU-02-3.** Run the [preflight](../glossary.md#preflight) for every site. In Claude Code ask: "Use the battery-preflight skill on sites/example-us/config.json." Read `analysis/preflight.md`, open each colliding entity's real web page, and add what it missed to `same_names` in that site's config. At team scale, look for three extra collisions. A parent brand and a product name that each appear in the other's answers. A sibling market with the same brand name. A competitor that was acquired or renamed this year.
   You'll know it worked when each site has a same-name list you agree with, and the products or markets that share a name carry the same entries in each other's lists. If the preflight says it has no [web search](../glossary.md#web-search), it marks entries "likely". Check them yourself.

4. **AP-FU-02-4.** Fill and read each question set. From the program folder:
   ```
   python3 scripts/fill_questions.py --config sites/example-us/config.json --template templates/questions-template.md
   ```
   Read all 28 aloud for that site. Reword in the shared template if a question is off, then run it again for every site, because a template change affects all of them.
   You'll know it worked when each run prints "Status: DRAFT, not frozen yet." and each site folder has a `questions.md`. If it lists problems, fix the config or template and rerun. Curly brackets or a name in the wrong place are E33 and E06.

5. **AP-FU-02-5.** Freeze each site, and record the version. Run the first line below, then put the date it prints, as mm/dd/yyyy, in that site's `config.json` under `question_set`, `frozen_on`. Change `version` only when a question is retired or added.
   ```
   python3 scripts/fill_questions.py --config sites/example-us/config.json --template templates/questions-template.md --freeze
   ```
   You'll know it worked when each `questions.md` starts with "Status: FROZEN". From now on never edit a question. Retire it, add a new code, and bump the version. A new version starts a new [series](../glossary.md#series) for that site and is never compared with the old one.

6. **AP-FU-02-6.** Keep a one-line change log per site in `sites/<id>/CHANGES.md`: the date, the version, and what changed. Leaders will ask "did the questions change" and the log answers in ten seconds.
   You'll know it worked when each site's log has its first line, such as "11/13/2026 | v1 | first freeze".

7. **AP-FU-02-7.** Do a [dry run](../glossary.md#dry-run) of the whole program, which checks keys, model names and question files and sends nothing.
   ```
   set -a && . ./.env && set +a
   python3 run_program.py run --dry-run
   ```
   You'll know it worked when every site prints "dry-run-ok". Open `logs/` and read one log: each company should say "key: found" and show a model name. If a key is missing, it's E34 in the single-site fixes. If a model is not found, set a current name in that site's `api_models` (E35).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AP-FU-02-4). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

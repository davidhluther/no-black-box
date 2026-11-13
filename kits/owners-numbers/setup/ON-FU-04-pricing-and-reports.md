# ON-FU-04 Pricing and Reports

You will run the pricing [what-if](../glossary.md#what-if) and the three report [scripts](../glossary.md#script).

1. **ON-FU-04-1.** Make lines.[csv](../glossary.md#csv) with one row per service or product, using the columns line, price, variable_cost, units_per_month. [Variable cost](../glossary.md#variable-cost) is what one more sale costs you directly. See `assets/example/lines.csv` in the pricing-whatif folder.
   You'll know it worked when each row has a price and a cost. A missing column is E21.
2. **ON-FU-04-2.** Run the pricing what-if from inside the pricing-whatif folder.

```bash
python3 scripts/pricing_whatif.py lines.csv --moves=-10,-5,5,10 --business "Your business" --out pricing-whatif.md
```

   You'll know it worked when it prints pricing-whatif.md. Each line shows the [break-even](../glossary.md#break-even) volume shift, a [finding](../glossary.md#finding). Add `--volume-change=-0.05` to also see a what-if on a volume change you name.
3. **ON-FU-04-3.** Make the quarterly report from inside the owner-reports folder, once you have scorecard.json files for the months.

```bash
python3 scripts/quarterly_report.py month1/scorecard.json month2/scorecard.json month3/scorecard.json --out quarterly-report.md
```

   You'll know it worked when quarterly-report.md has a table with a direction for each line and a look ahead marked what-if.
4. **ON-FU-04-4.** Draft the advisory letter.

```bash
python3 scripts/advisory_letter.py month3/scorecard.json --from "Your name" --to "Owner" --out advisory-letter.md
```

   You'll know it worked when advisory-letter.md has four short paragraphs. Edit it before you send it. It is a draft.
5. **ON-FU-04-5.** Make targets.csv with the columns [metric](../glossary.md#metric), baseline, target, quarter, why. Leave target blank for anything not chosen. Then run the roadmap.

```bash
python3 scripts/roadmap.py targets.csv --business "Your business" --start-month 2026-10 --out roadmap.md
```

   You'll know it worked when blank targets print as "to set" and no target appears that you did not type.
6. **ON-FU-04-6.** Optional. In Claude Code, install the kit's three skills as the repository's README describes, then ask in plain words, for example Build this month's Owner's Scorecard from the files in my owners-numbers-data folder. The skills use the same scripts.
   You'll know it worked when the answer names the same output files. If the [AI model](../glossary.md#ai-model) offers a number from memory instead of running the script, say run the script.

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

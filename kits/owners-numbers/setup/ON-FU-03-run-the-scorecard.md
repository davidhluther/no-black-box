# ON-FU-03 Run the Scorecard Each Month

You will run one command, read the page, and keep a copy.

1. **ON-FU-03-1.** Open the [command line](../glossary.md#command-line) and move into the owner-scorecard folder as in ON-FU-01-3.
   You'll know it worked when `ls` lists [scripts](../glossary.md#script). If not, repeat [ON-FU-01](ON-FU-01-install-and-test.md).
2. **ON-FU-03-2.** Run the [script](../glossary.md#script) on your folder. Use your own folder path and a name for the output folder.

```bash
python3 scripts/owner_scorecard.py ~/Documents/owners-numbers-data --out-dir ~/Documents/scorecards/2026-09
```

   You'll know it worked when it prints the path of scorecard.md. If it says a file is missing, it's E20. If it says no rows fall inside the month, check the dates in settings.[csv](../glossary.md#csv). That is E24.
3. **ON-FU-03-3.** Open scorecard.md. Read the verdict, the money table, the top items, customers and capacity, and the item named under "This month, look at".
   You'll know it worked when the numbers match what you know about the month. The page also lists data notes, such as bank rows with no category.
4. **ON-FU-03-4.** Find the [What-ifs](../glossary.md#what-if) section at the end. Any measure it lists used an example value because the matching setting in settings.csv is blank.
   You'll know it worked when you can name one setting to fill in. Fill it in and run again to turn that [what-if](../glossary.md#what-if) into a [finding](../glossary.md#finding).
5. **ON-FU-03-5.** Keep scorecard.json beside scorecard.md. It carries every number and its basis, and the report scripts read it next.
   You'll know it worked when both files sit in a folder named for the month.
6. **ON-FU-03-6.** Run the doctor command and keep the code for your records.

```bash
python3 support/doctor.py owners-numbers
```

   You'll know it worked when it prints a [support code](../glossary.md#support-code) beginning ON-FU.

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# AV-FU-04: Preflight and Practice Run

Time, about 40 minutes. You will run the [same-name](../glossary.md#same-name) check with the `battery-preflight` skill, then do a practice run that sends nothing and costs nothing.

1. **AV-FU-04-1.** Start [Claude Code](../glossary.md#claude-code) in your working folder (`claude`). Ask: "Use the battery-preflight skill on my config.json and my questions.md."
   You'll know it worked when it writes `analysis/preflight.md` with a table of names, severity, and scoring rules. If it says it has no [web search](../glossary.md#web-search), it works from its own knowledge and marks everything "likely". That is fine for a first pass, but check the entries yourself.

2. **AV-FU-04-2.** Read the [preflight](../glossary.md#preflight). Open `analysis/preflight.md`. Check each colliding entity it names has a real web page, and add anything it missed. Update `same_names` in `config.json`.
   You'll know it worked when you agree with the list. If the preflight suggests changes to your questions and the set is not yet [frozen](../glossary.md#frozen), make them in the template and redo guide AV-FU-03, step 3 to 5.

3. **AV-FU-04-3.** Do a [dry run](../glossary.md#dry-run) (a practice run that checks everything and sends nothing):
   ```
   python3 scripts/run_api_battery.py --config config.json --dry-run
   ```
   You'll know it worked when it prints the question count, "frozen: yes", and for each company either "key: found" and a model name, or "MISSING". If it says "key: MISSING", it's E34. If it says it found zero questions, it's E36.

4. **AV-FU-04-4.** Set model names. For each company you will use, open its models page and copy a current model name into `config.json` under `api_models`. The names in the example file were taken from the companies' own examples on 11/13/2026 and may already be out of date. Model names change.
   You'll know it worked when the dry run lists each model name next to "will run". If a later run says the model was not found, it's E35.

5. **AV-FU-04-5.** Run the built-in self-test:
   ```
   python3 scripts/run_api_battery.py --self-test
   ```
   You'll know it worked when it prints "self-test passed". This checks only that the [script](../glossary.md#script) can read the response formats in the vendors' documentation. It makes no live calls. The first real run is the real test.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FU-04-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

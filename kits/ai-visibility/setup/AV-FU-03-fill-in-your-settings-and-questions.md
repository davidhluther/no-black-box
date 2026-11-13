# AV-FU-03: Fill In Your Settings and Questions

Time, about 30 minutes. `config.json` is the one file that holds your business details. Then one [script](../glossary.md#script) turns the 28 question templates into your own [frozen](../glossary.md#frozen) [question set](../glossary.md#question-set).

1. **AV-FU-03-1.** Open `config.json` in any text editor (TextEdit on a Mac works if you choose Format, Make Plain Text). Replace every example value with your own: business name, type, service, town, region, owner name, website, and competitors. Keep the quotation marks and commas as they are. Do not change the names on the left.
   You'll know it worked when the file still looks like the example in layout, only with your words. If a later step says "invalid JSON", a quotation mark or comma went missing. That is E33.

2. **AV-FU-03-2.** Add your [same-name](../glossary.md#same-name) entries from guide AV-FR-02 to the `same_names` list, one line each, copying the layout of the examples. If you have not done that guide, do it first; the free version's steps for finding look-alikes still apply.
   You'll know it worked when the list holds your own entries, not the example "Maple Studio".

3. **AV-FU-03-3.** Make the question set. In the [terminal](../glossary.md#terminal), from your working folder:
   ```
   python3 scripts/fill_questions.py --config config.json
   ```
   You'll know it worked when it prints "Status: DRAFT, not frozen yet." and a file called questions.md appears. If it lists problems ("names your business", "still has a curly bracket"), fix them in `config.json` or the template, and run it again. See E33.

4. **AV-FU-03-4.** Read all 28 questions in questions.md aloud. They should sound like a customer. Change the wording now, in `references/questions-template.md`, if something is off, then rerun step 3.
   You'll know it worked when you would be comfortable asking every one of them yourself.

5. **AV-FU-03-5.** Freeze it.
   ```
   python3 scripts/fill_questions.py --config config.json --freeze
   ```
   Then put the date it printed, as mm/dd/yyyy, in `config.json` under `question_set`, `frozen_on`.
   You'll know it worked when questions.md starts with "Status: FROZEN". From now on never edit a question. Retire it and add a new code, with a new version.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FU-03-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

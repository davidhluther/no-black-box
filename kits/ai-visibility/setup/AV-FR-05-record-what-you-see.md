# AV-FR-05: Record What You See

Time, about 90 minutes for the first run. For each question and product, you add one row to the Results tab. It is a bit like marking a test, but there is no right answer, only what the [AI model](../glossary.md#ai-model) said.

Columns A to L are yours to fill in. Columns M (outcome) and N (group) fill themselves in.

1. **AV-FR-05-1.** Add the first row. In column A write the run label. In B the question code, such as LD-01. In C the product name, spelled exactly ChatGPT, Claude, Gemini, or Perplexity, because the Summary tab matches on those words. In K the [question set](../glossary.md#question-set) version.
   You'll know it worked when the outcome column (M) fills in on its own, even if it only says "not scored". If M stays empty after you add values in D to G, it's E21.

2. **AV-FR-05-2.** Fill the coded columns. Use only these values. Anything else makes the [check-up](../glossary.md#check-up) complain with E10.
   - D, answer_status. `ok` if you got an answer, `not_run` if you skipped it, `refused` if the product would not answer, `failed` if there was an error.
   - E, named. `y` if your business name is in the answer. `n` if not. `same-name` if the answer names a look-alike from your SameNames tab instead.
   - F, position. `1` if you were the first business named, `2` for second, `3+` for third or later, `list` if you are in an unranked list, `aside` if you only appear in a caveat or a "you might also check", and `-` if you are not named.
   - G, your_site_cited. `y` if your website is among the sources listed. `n` if sources were listed and yours was not. `none_given` if no sources were shown.
   You'll know it worked when each row with `ok` has values in D, E, F, and G. If a row's question code is not recognized, it's E08.

3. **AV-FR-05-3.** Fill the rest. In H list the websites cited, separated by semicolons. In I list every other business named, separated by semicolons. In J choose what the answer settled on, using one of `person_local`, `person_remote`, `software`, `generic_advice`, or `nobody`. In L add a note if anything was odd.
   You'll know it worked when I is filled in for every answer that names other businesses. This is what the outcome column uses to tell "[crowded out](../glossary.md#crowded-out)" from "absent". If you cannot tell whether an answer means you or a look-alike, it's E18.

4. **AV-FR-05-4.** The [same-name](../glossary.md#same-name) rule. If the answer names a business or word from your SameNames tab and your town or website does not appear with it, E is `same-name`, never `y`. If you are unsure, write `y`, and put "check same-name" in L. You will review those in guide AV-FR-06.
   You'll know it worked when same-name answers are not counted as you. Check the Summary tab's last column.

5. **AV-FR-05-5.** Optional help. If you want a second pair of eyes on an answer, use the coding prompt in Part 4 of `free/prompts.md` with a free AI model. Check what it says against the answer yourself. It sometimes misreads.
   You'll know it worked when you agree with the row it suggested. If you do not, trust your reading.

6. **AV-FR-05-6.** Never leave a gap. If you did not collect an answer, add the row anyway with `not_run`, `refused`, or `failed`. A blank row looks like "not named" and that is a lie.
   You'll know it worked when all 112 cells (28 questions times four products) have a row, with a real status in D.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FR-05-3). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# PW-FU-03: Run the Checkers

You'll end having run all three checkers on the example draft and read what they found. It takes about 20 minutes. Do this from inside the `plain-writing` folder (see `PW-FU-01-6`). On Windows, type `py` where it says `python3`.

1. **PW-FU-03-1.** Put the draft you want to check in a [markdown](../glossary.md#markdown) file (a plain text file whose name ends in `.md`). For practice, use `free/example-draft.md`. For your own writing, in Google Docs choose File, Download, Markdown, then move the file into the folder. If you try a Word or PDF file, it's E20.
   You'll know it worked when the [command line](../glossary.md#command-line)'s `ls` or `dir` shows your file.
2. **PW-FU-03-2.** Run article-check, the validator (a program that checks a document against rules):

   ```
   python3 [skills](../glossary.md#skill)/article-check/[scripts](../glossary.md#script)/validate_article.py free/example-draft.md --prose
   ```

   You'll know it worked when it prints a list of errors and ends with `VALIDATION FAILED`. For the example draft, that's the right answer. It should flag "in today's ever-evolving," "it's important to note," "in conclusion," "moreover," "testament," "seamless," "robust," and the [title-case](../glossary.md#title-case) heading. If it says `FATAL: could not load canonical style rules`, it's E15. If you run it on a short memo without `--prose` and it complains about internal links or a FAQ, it's E17.
3. **PW-FU-03-3.** Run tell-scorer's gate (a gate is a check that must pass before something goes out):

   ```
   python3 skills/tell-scorer/scripts/score_batch.py --md-glob free/example-draft.md --thresholds skills/tell-scorer/gate-thresholds.default.[json](../glossary.md#json) --out scores.[csv](../glossary.md#csv)
   ```

   You'll know it worked when you see `GATE:` followed by a count of breaches and the rules that were passed, such as `composite_hard_per1k`. A clean draft prints `GATE: clean`. Run the same line on `free/example-draft-fixed.md` and compare.
4. **PW-FU-03-4.** Run copy-lint (a [linter](../glossary.md#linter), which is a program that lists places that break your rules):

   ```
   python3 skills/copy-lint/scripts/copy_lint.py free/example-draft.md
   ```

   You'll know it worked when it lists lines with `ERROR` or `warn` and ends with a count. Exit code 2 and no findings means it couldn't run, and that's E21.
5. **PW-FU-03-5.** Read the output top to bottom. Fix each error by rewriting the sentence it names, not by deleting headings or lists. Run the same command again.
   You'll know it worked when article-check prints `VALIDATION PASSED` for the fixed example: `python3 skills/article-check/scripts/validate_article.py free/example-draft-fixed.md --prose`.

A passing check doesn't prove the writing is good. It proves the known tells are gone. Read the piece yourself.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like PW-FU-03-2). Run `python3 support/doctor.py plain-writing` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

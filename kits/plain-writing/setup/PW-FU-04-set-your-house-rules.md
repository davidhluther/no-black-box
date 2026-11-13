# PW-FU-04: Set Your House Rules and Limits

You'll end with the checkers tuned to your organization: your name in the settings file, your own rules file for the blog checks, and score limits calibrated to your own writing. It takes about 30 minutes.

1. **PW-FU-04-1.** Copy the settings file. In the [command line](../glossary.md#command-line), from the `plain-writing` folder, type `cp config.example.json config.json` on a Mac, or `copy config.example.json config.json` on Windows.
   You'll know it worked when a new file called `config.json` appears next to the original.
2. **PW-FU-04-2.** Open `config.json` in a text editor and change the values to yours: your organization name, short name, site address, and the file names for your [house style](../glossary.md#house-style). Leave a value as `""` if you don't have one. Keep the quotes and commas exactly as they are.
   You'll know it worked when the file still looks like the original, with only the words inside the quotes changed. If a checker later says it can't read the file, you probably deleted a quote or comma.
3. **PW-FU-04-3.** Make your own rules file for the blog checks. Copy `skills/article-check/data/brand-rules/example.json` to a new file such as `my-rules.json`. Change `brand`, the internal-link address pattern, and the call-to-action phrases to match your site. Set any list you don't need to `[]`. Run it with `--brand-rules my-rules.json`.
   You'll know it worked when running the [validator](../glossary.md#validator) without `--prose` stops asking for things you don't use. If it prints `FATAL: unknown key(s)`, it's E16. Compare your key names with the example.
4. **PW-FU-04-4.** Tune the score limits from your own writing. Copy `skills/tell-scorer/gate-thresholds.default.json` to `my-gate-thresholds.json`. Score three to five pieces you're proud of with `score_batch.py`, look at each rule's score in `scores.csv`, and set each limit a little above your best pieces. A draft you like that fails the [gate](../glossary.md#gate) is E19.
   You'll know it worked when your best pieces pass and a draft full of banned words fails.
5. **PW-FU-04-5.** Add your own banned words. Open `skills/article-check/data/style_rules.json`. Find the block named `restricted_words`. Add a new entry with the same shape as the others. Do the same copy in `skills/copy-lint/data` and `skills/tell-scorer/data`, so all three read your list.
   You'll know it worked when a draft containing your new word fails article-check.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like PW-FU-03-2). Run `python3 support/doctor.py plain-writing` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

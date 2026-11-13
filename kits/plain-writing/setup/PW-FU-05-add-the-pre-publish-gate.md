# PW-FU-05: Add the Pre-Publish Gate

You'll end with one command that runs all the checks on a file, and optionally a hook (a small program [Git](../glossary.md#git) runs automatically at a set moment) that stops a bad draft from being saved into your [project](../glossary.md#project). It takes about 30 minutes. The hook is optional.

1. **PW-FU-05-1.** Run the [gate](../glossary.md#gate) on the example draft. From the `plain-writing` folder:

   ```
   python3 skills/plain-writing/scripts/prepublish_gate.py free/example-draft.md
   ```

   You'll know it worked when you see three sections called article-check, tell-scorer gate, and copy-lint, then `GATE FAILED` with the checks that failed. That's the right answer for the example. Run it on `free/example-draft-fixed.md` and you should see `GATE PASSED`.
2. **PW-FU-05-2.** Run it on your own file with your own rules and limits:

   ```
   python3 skills/plain-writing/scripts/prepublish_gate.py --rules my-rules.json --thresholds my-gate-thresholds.json my-post.md
   ```

   You'll know it worked when the three sections run and a verdict prints. If it says `Could not find these skills`, it's E18. Keep `article-check`, `tell-scorer`, `copy-lint`, and `plain-writing` side by side in one folder, or add `--skills-dir` with that folder's path.
3. **PW-FU-05-3.** Read the verdict. Exit code 0 means every check passed. Exit code 1 means fix and run again. Exit code 2 means the gate couldn't run, so it never blocks you by accident.
   You'll know it worked when you can tell which of the three checks failed from the last lines.
4. **PW-FU-05-4.** Optional. Add the hook, which only works if your writing folder is tracked by [Git](../glossary.md#git). In the [command line](../glossary.md#command-line), from your writing folder, create the file `.git/hooks/pre-commit` with this content, replacing the path with the full path to your `plain-writing` folder:

   ```
   #!/bin/sh
   files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')
   [ -z "$files" ] && exit 0
   python3 /full/path/to/plain-writing/skills/plain-writing/scripts/prepublish_gate.py $files
   ```

   Then make it runnable: `chmod +x .git/hooks/pre-commit` (Mac). File names with spaces don't work with this version, so use dashes in file names.
   You'll know it worked when `ls -l .git/hooks/pre-commit` shows the file with an `x` in its permissions.
5. **PW-FU-05-5.** Test the hook. Save a change to the example draft with Git (`git add free/example-draft.md`, then `git commit -m "test"`).
   You'll know it worked when the commit is refused and the gate's findings print. That's the hook doing its job (and it's E22 if you didn't expect it). Fix the findings and commit again. If you've read the findings and want to skip once, add `--no-verify` to the commit command.

The gate reads files and prints text. It never changes your writing and never sends anything over the network.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like PW-FU-03-2). Run `python3 support/doctor.py plain-writing` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# PW-FU-02: Install the Skills in Claude Code

You'll end with the plain-writing [skills](../glossary.md#skill) available inside Claude Code (a program from Anthropic that runs an [AI model](../glossary.md#ai-model) with tools on your computer). This is optional. The checker programs run on their own without it, so skip to `PW-FU-03` if you don't use Claude Code. It takes about 15 minutes.

1. **PW-FU-02-1.** Install Claude Code if you don't have it. The shared guide [install Claude](../../../guides/install-claude.md) walks through it.
   You'll know it worked when typing `claude` in the [command line](../glossary.md#command-line) opens a chat inside the window.
2. **PW-FU-02-2.** In Claude Code, add this kit's marketplace (a catalog of [plugins](../glossary.md#plugin)) by typing the line shown on the repository's front page. It has this shape, with the real address in place of the placeholder:

   ```
   /plugin marketplace add davidhluther/no-black-box
   ```

   You'll know it worked when Claude Code says the marketplace was added.
3. **PW-FU-02-3.** Install the kit's plugin (a bundle of skills) by typing:

   ```
   /plugin install plain-writing@no-black-box
   ```

   You'll know it worked when Claude Code says the plugin installed. If the name isn't found, run `/plugin` and pick plain-writing from the list.
4. **PW-FU-02-4.** Check the skills loaded. In Claude Code, type: "Which skills do you have for writing?"
   You'll know it worked when the reply lists plain-writing, article-check, tell-scorer, copy-lint, evidence-review, voice-presets, and presentations.
5. **PW-FU-02-5.** Manual alternative if the marketplace doesn't work. Copy the folders inside `skills` (in your downloaded kit) into a folder called `.claude/skills` in your home folder. A skill is a folder, so copy each folder whole.
   You'll know it worked when you restart Claude Code and step 4 gives the same list.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like PW-FU-03-2). Run `python3 support/doctor.py plain-writing` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

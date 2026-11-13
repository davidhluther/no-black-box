# Install the Skills (Full, Guide 1)

The full version runs the kit's six [skills](../glossary.md#skill) inside Claude Code, a program that runs an AI model on your own computer with tools it can use. It needs a Claude plan that includes Claude Code and some comfort with typing commands into a terminal (a window where you type instructions instead of clicking). If that is new, do the free or low-cost version first; nothing is lost by starting there. About 30 minutes.

1. **MM-FU-01-1.** Install Claude Code by following [Install Claude](../../../guides/install-claude.md). Open a terminal and run the version check from that guide.
   You'll know it worked when the terminal prints a version number. If it says "command not found", it's E22.

2. **MM-FU-01-2.** Add the kit. In Claude Code, add the no-black-box marketplace using the repository address given on the repository's front page, then install the kit named `measure`, as the shared guide shows. The six skills are ga4-events-setup, metric-check, monthly-report, looker-export, gsc-read and clarity-analytics.
   You'll know it worked when typing `/` in Claude Code lists the skills by name. If a skill is missing, it's E22.

3. **MM-FU-01-3.** Make your settings file. Copy `config.example.json` to `config.json` in the folder where you will work, and replace each example value with your own: site address, [Search Console](../glossary.md#search-console) site name, [GA4](../glossary.md#ga4) property and measurement IDs, [Tag](../glossary.md#tag) Manager [container](../glossary.md#container) ID, [Clarity](../glossary.md#clarity) project name, and sheet name. This is the only file with your organization's details. Never put a password, key or [token](../glossary.md#token) in it.
   You'll know it worked when the file opens as valid text with your values and no example.org left in it. Claude Code skills read this file first.

4. **MM-FU-01-4.** Try the planning skill, which needs no keys. Ask Claude Code: "Use ga4-events-setup to make a Tag Manager import file for my site." It runs `build_gtm_import.py`, which writes a file of new, prefixed tracking pieces and never contacts Google. Add `--existing` with a container export if you want a name-collision check.
   You'll know it worked when it prints how many tags, [triggers](../glossary.md#trigger) and [variables](../glossary.md#variable) it wrote. Then follow free guide 3 from step 3 (new [workspace](../glossary.md#workspace)), importing the file with Merge and "Rename conflicting tags, triggers, and variables" (never Overwrite), and test in preview before publishing.

Next: [Give the scripts read-only access](MM-FU-02-give-the-scripts-read-only-access.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

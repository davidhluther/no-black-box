# CE-FU-01: Install and Set Up the Team Config

You'll end with the kit installed, one config file filled in for your first site, a work folder, and a clean [check-up](../glossary.md#check-up). Allow about 90 minutes. Two folders matter. The repo's top folder (named no-black-box-main if you downloaded a ZIP, see [get the kit files](../../../guides/get-the-files.md)) holds `support`. The kit folder, `kits/content-engine` inside it, holds `skills`, `tools`, and your `config.json`. Run the check-up from the top folder and everything else from the kit folder.

1. **CE-FU-01-1.** Install [Claude Code](../glossary.md#claude-code) by following the shared [install guide](../../../guides/install-claude.md), Way two. Come back when its last step passes.
   You'll know it worked when typing `claude --version` in the [command line](../glossary.md#command-line) prints a version number. If it says command not found, it's E01.

2. **CE-FU-01-2.** Check that [Python](../glossary.md#python) is 3.9 or newer.

   ```bash
   python3 --version
   ```

   You'll know it worked when it prints 3.9 or higher. If it's older or missing, install the current version from python.org and open a new window; this is E04.

3. **CE-FU-01-3.** Install the kit's [plugin](../glossary.md#plugin). Inside Claude Code, add the marketplace if you haven't, then install.

   ```
   /plugin marketplace add davidhluther/no-black-box
   /plugin install content-engine@no-black-box
   ```

   You'll know it worked when Claude Code lists 18 skills for the plugin. Ask "Which skills do you have for content briefs and drafts?" and look for content-brief, seo-draft, article-check, and evidence-review. If one is missing, it's E01. You don't need to install idea-to-post or plain-writing separately; this kit carries the skills it uses from both.

4. **CE-FU-01-4.** Copy the settings file and fill it in for your first site. From the kit folder:

   ```bash
   cp config.example.json config.json
   ```

   Open `config.json` in a text editor. Change every example value: the team block, the owners (one role per line, a backup for each), your site's address and sitemap, the [queue](../glossary.md#queue) stages if yours differ, and the schedule's job names. Leave `paid_keyword_tool` as `"none"` until [CE-FU-02](CE-FU-02-connect-data-and-your-cms.md). Never put a key or password in this file.
   You'll know it worked when the file still reads as a list of names and values with only the words inside the quotes changed. A message about a missing or broken file is E02, and it is usually a lost comma or quote.

5. **CE-FU-01-5.** Decide how you'll name config files for more than one site. Make a copy per site, named for the site, and fill each one in.

   ```bash
   cp config.json config.example-site-two.json
   ```

   You'll know it worked when each site has its own file with its own `site.id`, sitemap, queue, and publish settings. Every command in this kit takes `--config <file>`, so you never edit a file back and forth between sites. Markets in other languages get their own file too; see [CE-FU-03](CE-FU-03-run-the-weekly-cycle-on-a-schedule.md) step 8.

6. **CE-FU-01-6.** Make the work folders. From the kit folder:

   ```bash
   mkdir -p ideas/pasted ideas/notes briefs drafts measure queue style ops
   ```

   You'll know it worked when `ls` lists them. A [skill](../glossary.md#skill) that later says a folder is missing is E03.

7. **CE-FU-01-7.** Put your style guide and banned-words list in `style/voice-and-banned-words.md`. If you don't have one, build it with [PW-FU-04, set your house rules](../../plain-writing/setup/PW-FU-04-set-your-house-rules.md) in the Plain writing kit, then copy the result here. Copy `skills/article-check/data/brand-rules/example.json` to `style/brand-rules-<site-id>.json` and edit it for each site.
   You'll know it worked when both files exist. seo-draft stops without the style guide, by design.

8. **CE-FU-01-8.** Run the [check-up](../glossary.md#check-up). From the repo's top folder:

   ```bash
   python3 support/doctor.py content-engine
   ```

   You'll know it worked when it prints a [support code](../glossary.md#support-code) ending in OK. For a second site, add `--config kits/content-engine/config.example-site-two.json`. The check-up reports only filenames and whether settings are filled in, never keys or file contents. If it fails, copy the whole code and see [fixes](../fixes.md).

Next, [CE-FU-02, connect your data and your CMS](CE-FU-02-connect-data-and-your-cms.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CE-FU-01-3). Run `python3 support/doctor.py content-engine` and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

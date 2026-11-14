# AP-FU-01: Set Up the Program Folder

Time, about 90 minutes. You install the tools, add the kit, make one program folder that every site hangs from, and decide who owns what. The install and key steps are the same as the single-site kit, so this guide links to them and covers only what changes with a team.

The check-up for this kit is a command. When a step fails, run it and copy the [support code](../glossary.md#support-code):

```
python3 support/doctor.py ai-visibility-program --config ~/ai-visibility-program/config.json
```

1. **AP-FU-01-1.** Install [Claude Code](../glossary.md#claude-code) and Python 3 on the machine that will run the schedule, following [Install Claude](../../../guides/install-claude.md) and steps 1 and 2 of [AV-FU-01](../../ai-visibility/setup/AV-FU-01-install-claude-code-and-the-kit.md). Use the machine that will stay on, not only your own laptop.
   You'll know it worked when `claude` opens a chat prompt and `python3 --version` prints 3.9 or higher. If the [terminal](../glossary.md#terminal) says "command not found", it's E30 in the [single-site fixes](../../ai-visibility/fixes.md).

2. **AP-FU-01-2.** Add this kit. In Claude Code type the two lines below, one at a time.
   ```
   /plugin marketplace add davidhluther/no-black-box
   /plugin install ai-visibility-program@no-black-box
   ```
   You'll know it worked when Claude Code lists the kit's 14 skills, including `question-battery`, `answer-noise-audit` and `unified-visibility`. If it cannot find the marketplace, it's E31 in the single-site fixes.

3. **AP-FU-01-3.** Make the program folder and give it the runner. In a [terminal](../glossary.md#terminal) (a window where you type instructions instead of clicking):
   ```
   mkdir -p ~/ai-visibility-program/sites ~/ai-visibility-program/templates ~/ai-visibility-program/imports ~/ai-visibility-program/reports
   cd ~/ai-visibility-program
   claude
   ```
   Then ask Claude Code: "Copy the scripts and references folders from the question-battery skill into this folder. Copy full/run_program.py and config.example.json from the ai-visibility-program kit here, and save config.example.json as config.json."
   You'll know it worked when `ls` shows `config.json`, `run_program.py`, `scripts`, `references`, `sites`, `templates`, `imports` and `reports`. If Claude Code cannot find the kit files, it's E31 in the [single-site fixes](../../ai-visibility/fixes.md).

4. **AP-FU-01-4.** Fill in `config.json`. Open it in a plain-text editor. The `program` block names the people and the schedule. The `sites` list has one entry per site, market or product line you will track.

   | Field | What to put |
   |---|---|
   | `owner_name`, `owner_role` | The one person accountable for the program's numbers. One name, not a team. |
   | `backup_owner_name` | Who runs the program when the owner is out. They must be able to log in to the machine and read the [ledger](../glossary.md#ledger). |
   | `reviewer_name` | The person who reads scored drafts and signs off on clean numbers. Not the person who wrote the questions, if you can help it. |
   | `run_day_of_month` | The day the run starts. Pick one that is not a month end or a release day. |
   | `grace_days` | How many days after that day the daily check waits before it calls a site missed. |
   | `review_days` | How many days after a good run the check waits for the scored file before it flags the review. |
   | `max_attempts`, `retry_wait_minutes` | How many times a failed site is tried, and the wait between. Each retry re-asks every question and costs money, so keep it at two. |
   | `sites[].id` | A short lowercase name with hyphens, such as `example-us`. It becomes a folder name. |
   | `sites[].config_file` | Where that site's own `config.json` will live, such as `sites/example-us/config.json`. |
   | `providers` | The AI companies you will run. Leave out any you have no key for. |
   | `sources` | Where your [Search Console](../glossary.md#search-console), Bing, [GA4](../glossary.md#ga4) and platform exports land. Used in guide AP-FU-04. |

   You'll know it worked when the file still has the same layout as the example, only with your words, and the check-up's `config.json is valid JSON` line passes. If a later step says the file is invalid, a quotation mark or comma went missing. That's E41.

5. **AP-FU-01-5.** Store the keys the team way. Follow steps 1 to 4 of [AV-FU-02](../../ai-visibility/setup/AV-FU-02-get-and-store-your-keys.md) for each company, with two changes. Create the keys in a team billing account with a monthly cap, not on a personal card. Then save them in a file named `.env` in the program folder, one line per key, because a scheduled job does not see keys you typed into a terminal.
   ```
   touch .env && chmod 600 .env
   ```
   Open `.env` and add one line per company in the form `ANTHROPIC_API_KEY=your-key`, using the names OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY and PERPLEXITY_API_KEY. See [Keys and accounts](../../../guides/keys-and-accounts.md) for where each key comes from.
   You'll know it worked when `ls -l .env` shows `-rw-------` and `grep -c KEY config.json` prints 0. Never put `.env` in a shared or synced folder. If a key shows up anywhere else, it's E32.

6. **AP-FU-01-6.** Run the check-up from the folder where you unpacked the kit (see [Get the kit files](../../../guides/get-the-files.md)):
   ```
   python3 support/doctor.py ai-visibility-program --config ~/ai-visibility-program/config.json
   ```
   You'll know it worked when it prints "All basics passed" and a support code ending in your kit version. Optional lines for `claude` and `python3` may say "skip". If a line says FAIL, fix the first one, run it again and use the code in [Fixes](../fixes.md) (E90 to E95).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AP-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

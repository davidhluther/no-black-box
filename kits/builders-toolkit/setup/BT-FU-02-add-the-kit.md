# Add the Kit to Claude Code

About 10 minutes. You will install the kit's [plugin](../glossary.md#plugin) (a bundle of [skills](../glossary.md#skill) that installs in one step) and confirm [Claude Code](../glossary.md#claude-code) can see all five.

1. **BT-FU-02-1.** Start Claude Code in your practice folder.

   ```bash
   cd ~/work/practice && claude
   ```

   You'll know it worked when Claude Code's welcome screen and a text box appear. If it asks you to sign in, follow the prompts and use your paid Claude plan. If you see "[command](../glossary.md#command) not found", it's E01.

2. **BT-FU-02-2.** Tell Claude Code where the kit's list of plugins lives. This list is called a [marketplace](../glossary.md#marketplace). Type this inside Claude Code, replacing the part in angle brackets with the address on the [repository](../glossary.md#repository)'s front page.

   ```
   /plugin marketplace add davidhluther/no-black-box
   ```

   You'll know it worked when Claude Code says the marketplace was added. If you see "not found" or "invalid", it's E05.

3. **BT-FU-02-3.** Install the Builder's Toolkit plugin. Type this, then follow any prompt to approve.

   ```
   /plugin install builders-toolkit@no-black-box
   ```

   You'll know it worked when Claude Code says the plugin installed. If the name is not found, type `/plugin` and pick it from the list, then see E05.

4. **BT-FU-02-4.** Confirm the skills are visible. Type this to Claude Code as a normal message.

   ```
   Which skills do you have from the builders-toolkit plugin? Name each one in a line.
   ```

   You'll know it worked when you see capability-ledger, session-brief, scheduled-jobs, design-gate and workstream-inventory. If any is missing, quit with `/exit`, start `claude` again and repeat the question, or see E06.

5. **BT-FU-02-5.** Tell Claude Code to read your settings.

   ```
   Read config.json in this folder and tell me what projects_folder is set to.
   ```

   You'll know it worked when it quotes the `projects_folder` value from the file. Edit that value to the folder that holds your real projects (for example `~/work`) before BT-FU-04. If it says it cannot find the file, it's E04.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like BT-FU-01-3). Run `python3 support/doctor.py builders-toolkit` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# Install the Kit and Pick a Workstream

About 40 minutes. You will install the six [skills](../glossary.md#skill), point them at your team's workspace and give your first [workstream](../glossary.md#workstream) a [capability ledger](../glossary.md#capability-ledger). Do this on the machine your team's recurring jobs will run on, or on your own machine if jobs will move later.

If you have never opened a [terminal](../glossary.md#terminal) or built a practice folder, run [BT-FU-01](../../builders-toolkit/setup/BT-FU-01-get-ready.md) first. It takes 15 minutes and covers the same ground in more detail.

1. **TO-FU-01-1.** Install [Claude Code](../glossary.md#claude-code) with the shared guide [install-claude](../../../guides/install-claude.md), then check it.

   ```bash
   claude --version
   ```

   You'll know it worked when a version number prints. If you see "command not found", it's E01.

2. **TO-FU-01-2.** Check that [Python](../glossary.md#python) 3 is installed.

   ```bash
   python3 --version
   ```

   You'll know it worked when it prints "Python 3" and a version of 3.9 or higher. If you see "command not found", it's E02.

3. **TO-FU-01-3.** Start Claude Code in your team's workspace folder (the folder that holds your workstreams) and add the kit. Type these inside Claude Code, one at a time. The first line adds the [marketplace](../glossary.md#marketplace) (the list the [plugin](../glossary.md#plugin) installs from). The second installs the plugin, which carries all six skills.

   ```
   /plugin marketplace add davidhluther/no-black-box
   ```

   ```
   /plugin install team-operations@no-black-box
   ```

   You'll know it worked when Claude Code says the plugin installed. Then ask "Which skills do you have from the team-operations plugin? Name each one." You should see scheduled-jobs, capability-ledger, session-brief, workstream-inventory, design-gate and metric-check. If the plugin is not found, or a skill is missing, it's E03.

4. **TO-FU-01-4.** Make your settings file. In the kit's folder, copy `config.example.json` to `config.json` and open it in any text editor. The file is [JSON](../glossary.md#json), so keep every quote and comma.

   ```bash
   cp config.example.json config.json
   ```

   Fill in `team_name`, then `workspace.projects_folder` (the folder that holds your workstreams) and `workspace.routing_table` (the notes file that says where each kind of work lives). Fill `scheduled_jobs.owner_name` and `scheduled_jobs.owner_contact` with a role and a shared address, such as "Marketing ops on-call" and name@example.org, so the contact survives a person leaving. List your workstreams under `team.workstreams`, each with a folder and a named owner.

   You'll know it worked when `python3 -c "import json; json.load(open('config.json'))"` prints nothing. If it prints an error, a comma or quote is wrong, and it's E04.

5. **TO-FU-01-5.** Run the [check-up](../glossary.md#check-up) from the folder that holds the kit's `support/` folder.

   ```bash
   python3 support/doctor.py team-operations
   ```

   You'll know it worked when it prints "All basics passed" and a [support code](../glossary.md#support-code) ending in E00. If a line says FAIL, the problem code points to the matching row in [fixes](../fixes.md).

6. **TO-FU-01-6.** Choose the first workstream. Pick one that already has a recurring pull or a recurring report, a named owner and a [repository](../glossary.md#repository) you can save files to. Organic reporting or AI visibility tracking are typical first picks, because leaders read them. Do not start with the messiest one.

   You'll know it worked when you can finish this sentence: "[workstream] is owned by [person], lives in [folder], and runs [number] recurring jobs." Write it in your `config.json` under `team.workstreams`.

7. **TO-FU-01-7.** Create the ledger inside that workstream's folder. Ask Claude Code:

   ```
   Use the capability-ledger skill to create CAPABILITIES.md in this workstream's folder. Then list what this workstream can do today from its scripts, schedules and published outputs, and add one row per capability with its proof. Put today's date and my name in the verified header.
   ```

   You'll know it worked when the file exists and every Live row names a shipped date and a proof you can open. A capability with no proof goes in "In progress" until it has one. If Claude Code does not use the skill, say "use the capability-ledger skill" again, or see E03.

8. **TO-FU-01-8.** Run the ledger checker. Replace `PATH_TO_KIT` with the folder that holds the kit.

   ```bash
   python3 PATH_TO_KIT/skills/capability-ledger/scripts/check_ledger.py CAPABILITIES.md
   ```

   You'll know it worked when it prints "0 problem(s)". A header with no date, or a proof path that does not exist, is E05. A newly copied template reports problems on purpose until its example row is replaced.

9. **TO-FU-01-9.** Fill the ledger's third section, "Known NOT built, or decided against." Add each thing someone might assume exists: a market you stopped tracking, a platform you declined, an export you never automated. Give each a decision date, who decided and why.

   You'll know it worked when the section has at least three dated rows. From now on, a "we can't do that" answer starts here, and an answer that comes only from a search must say "not found in" and name what was searched. For a worked practice run of that rule, see [BT-FU-03](../../builders-toolkit/setup/BT-FU-03-ledger-and-brief.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like TO-FU-01-3). Run `python3 support/doctor.py team-operations` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

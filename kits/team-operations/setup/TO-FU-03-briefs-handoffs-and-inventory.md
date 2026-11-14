# Briefs, Handoffs and the Workstream Inventory

About 60 minutes. You will give AI-assisted work a brief that survives a long conversation and a change of person, rehearse a [handoff](../glossary.md#handoff), and check that no [workstream](../glossary.md#workstream) is missing from your written routing notes. The one-person practice runs are [BT-FU-03](../../builders-toolkit/setup/BT-FU-03-ledger-and-brief.md) and [BT-FU-04](../../builders-toolkit/setup/BT-FU-04-inventory-and-design-gate.md).

1. **TO-FU-03-1.** Set the unit of work. One [session](../glossary.md#session) per task or topic, one brief per session, and each brief saved in its workstream's folder as `BRIEF-<topic>.md` next to the [capability ledger](../glossary.md#capability-ledger). Never reopen a large idle session and keep going. Start a fresh one from its handoff.

   You'll know it worked when your team can say where a given piece of work's brief lives without asking anyone. If two briefs claim one session, or none does, fix that before you rely on either.

2. **TO-FU-03-2.** Create a brief for a real piece of work, not a practice one. Ask [Claude Code](../glossary.md#claude-code):

   ```
   Use the session-brief skill to create BRIEF-weekly-organic-report.md in this workstream's folder. Purpose: "Produce the weekly organic report from the saved pulls and explain any move over the flag threshold". Session: "organic-report-1". Compactions: 0.
   ```

   You'll know it worked when the file opens with the three header lines Purpose, Session and Compactions. The Purpose line is written once and never edited. If the work drifts, that is the signal to hand off, not to rewrite the line. A missing header line is E14.

3. **TO-FU-03-3.** Move the team's standing rules into the brief's "Settled, never re-ask" section, each with a date. Typical ones for a reporting team: how dates and numbers are written, which platforms count as independent sources, who must approve a publish, that a missed [slot](../glossary.md#slot) is listed in every report, and that a cause is never stated without a grade.

   You'll know it worked when a new session reading only the brief stops asking questions you answered last week. A rule that exists only in a chat is lost at the next [compaction](../glossary.md#compaction).

4. **TO-FU-03-4.** Run the brief checker.

   ```bash
   python3 PATH_TO_KIT/skills/session-brief/scripts/check_brief.py BRIEF-weekly-organic-report.md
   ```

   You'll know it worked when it prints "0 problem(s)". It warns when the brief runs past 150 lines. Detail beyond a minute's reading belongs in a separate file the brief points to.

5. **TO-FU-03-5.** Rehearse the compaction routine once. Before a compaction, refresh State, Settled, Open items and Next step, update the ledger for anything shipped and save your work. After it, the first act of the session is to reread the brief and say which one it reread.

   You'll know it worked when the session names the brief and its Compactions count, then continues from Next step without asking again about anything in Settled. Count a compaction only after it finishes. After two completed compactions, the next full-window warning starts a handoff and not more task work.

6. **TO-FU-03-6.** Rehearse the handoff with a person as well as a session. Ask Claude Code to run the handoff protocol in the `session-brief` [skill](../glossary.md#skill). Then give the brief, and nothing else, to a colleague who was not in the work.

   You'll know it worked when that colleague can state the purpose, three settled decisions and the next step in two minutes without opening the chat. If they cannot, the gap is in the brief. Fix the brief, not the colleague.

7. **TO-FU-03-7.** Run the workstream inventory across your whole workspace. Ask Claude Code:

   ```
   Use the workstream-inventory skill with the projects_folder and routing_table from config.json. Tell me how many repositories it found, whether it filtered anything, and which ones the routing table does not mention.
   ```

   You'll know it worked when you get a table of [repositories](../glossary.md#repository) with last-change dates and a count, ending with the list the [routing table](../glossary.md#routing-table) does not mention. Several folders of one repository count once. If it finds none, it's E15.

8. **TO-FU-03-8.** Close the gaps the inventory found. For each repository in the "not in the routing table" list, add one line to your [routing table](../glossary.md#routing-table): when the work is about X, read Y first. Or write down, in the same file, that you left it out on purpose.

   You'll know it worked when a rerun lists nothing unexplained. The tool cannot tell an omission from a judgment call, so the written decision is the evidence that it was a judgment call.

9. **TO-FU-03-9.** Keep the inventory honest over time. Save a baseline now, then register a weekly job in `jobs.json` that runs the inventory with `--diff` against it, so a new or vanished workstream shows up as an [outcome row](../glossary.md#outcome-row).

   ```bash
   python3 PATH_TO_KIT/skills/workstream-inventory/scripts/inventory.py --json > baseline.json
   ```

   You'll know it worked when the weekly row says what changed since the baseline. A written inventory goes stale and a remembered one is worse, so derive the list from the folders each time.

10. **TO-FU-03-10.** If your team ships web pages, put the [design gate](../glossary.md#design-gate) in front of every change that touches pages, components or templates, and require that the reviewer of the screenshots is not the person who built the page. Install and practice it with BT-FU-04 steps 3 to 5.

    You'll know it worked when a pull request for a page change carries the gate's report. A builder who reviews their own page has not run the gate. If the gate exits with code 2, nothing was measured, and it's E16.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like TO-FU-03-4). Run `python3 support/doctor.py team-operations` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

# Start a Ledger and a Session Brief

About 20 minutes. You will create a [capability ledger](../glossary.md#capability-ledger) (one file listing what the project can do and what proves it) and a [session brief](../glossary.md#session-brief) (a short file holding the session's purpose and settled decisions). Work inside [Claude Code](../glossary.md#claude-code) in the practice folder from guide 02.

1. **BT-FU-03-1.** Ask Claude Code to create the ledger.

   ```
   Use the capability-ledger skill to create CAPABILITIES.md in this folder from its template. Put today's date and "Claude Code" in the verified header.
   ```

   You'll know it worked when a file named `CAPABILITIES.md` appears. If Claude Code does not use the [skill](../glossary.md#skill), say "use the capability-ledger skill" again, or see E06.

2. **BT-FU-03-2.** Run the ledger checker. Ask Claude Code to run it, or leave Claude Code with `/exit` and run it yourself, replacing `PATH_TO_KIT`.

   ```bash
   python3 PATH_TO_KIT/skills/capability-ledger/scripts/check_ledger.py CAPABILITIES.md
   ```

   You'll know it worked when it prints "0 problem(s)" after you replace the example row. A newly copied template reports problems on purpose, because its example row has no real date or proof. If it says "missing header", it's E07.

3. **BT-FU-03-3.** Add one real row. Make a small script, then record it. Ask Claude Code:

   ```
   Create scripts/hello.py that prints "hello". Then add a row to the Live capabilities table of CAPABILITIES.md: capability "prints hello", where it runs "scripts/hello.py", shipped today, proof "scripts/hello.py". Run the checker.
   ```

   You'll know it worked when the checker says "0 problem(s)". If it says "proof path not found", the file name in the Proof column does not match a real file, so it's E08.

4. **BT-FU-03-4.** Practice a negative claim. Ask the question below and watch how Claude Code answers.

   ```
   Can this project send email?
   ```

   You'll know it worked when the answer names what it searched (the ledger and the files) and says "not found in" those places. It should not say "it cannot". If it does, remind it: "Follow the negative-claims rules in the capability-ledger skill."

5. **BT-FU-03-5.** Create the brief.

   ```
   Use the session-brief skill to create BRIEF-practice.md from its template. Purpose: "Learn the builder's toolkit in a practice folder". Session: "practice-1". Compactions: 0.
   ```

   You'll know it worked when `BRIEF-practice.md` opens with the three lines Purpose, Session and [Compactions](../glossary.md#compaction). If a line is missing, it's E09.

6. **BT-FU-03-6.** Add a settled decision and check the brief.

   ```
   Add this to the Settled section of BRIEF-practice.md with today's date: "Write dates as month/day". Then run the brief checker.
   ```

   You'll know it worked when the checker prints "0 problem(s)". If it reports a missing section, it's E09.

7. **BT-FU-03-7.** Save your work as a [commit](../glossary.md#commit) (a saved snapshot with a label).

   ```bash
   git add -A && git commit -m "Add ledger and brief"
   ```

   You'll know it worked when [git](../glossary.md#git) prints a line with "2 files changed" or more. If it asks who you are, run the two `git config` lines it shows, then repeat.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like BT-FU-01-3). Run `python3 support/doctor.py builders-toolkit` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

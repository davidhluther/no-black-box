# AV-FU-01: Install Claude Code and the Kit

Time, about 30 minutes. The full version uses [Claude Code](../glossary.md#claude-code), a program that runs on your computer and carries out multi-step tasks with your files, and a few small [scripts](../glossary.md#script). If you have never opened a [terminal](../glossary.md#terminal) (a window where you type instructions to your computer instead of clicking), the shared guide [Install Claude](../../../guides/install-claude.md) walks through it. These steps are written for a Mac.

Support for the full version comes from a [check-up](../glossary.md#check-up) command. When a step fails, run `python3 support/doctor.py ai-visibility` from the kit folder and copy the [support code](../glossary.md#support-code) it prints.

1. **AV-FU-01-1.** Install Claude Code by following [Install Claude](../../../guides/install-claude.md). Sign in with your Claude account.
   You'll know it worked when typing `claude` in the terminal opens a chat prompt. If the terminal says "command not found", it's E30.

2. **AV-FU-01-2.** Check that Python (a common programming language the scripts are written in) is installed. In the terminal type:
   ```
   python3 --version
   ```
   You'll know it worked when it prints a version number such as 3.11 or higher. If it says command not found, it's E30. Ask Claude Code, "Please help me install Python 3", and approve each step it asks about.

3. **AV-FU-01-3.** Add the kit. In Claude Code type the two lines below, one at a time, replacing the address with the one shown on the kit's GitHub page.
   ```
   /plugin marketplace add davidhluther/no-black-box
   /plugin install ai-visibility@no-black-box
   ```
   You'll know it worked when Claude Code lists the kit's 14 skills, including question-battery and battery-preflight. If it says it cannot find the marketplace, check the address, and see E31.

4. **AV-FU-01-4.** Make a working folder for your results. In the terminal type the first line to make it and the second to go into it.
   ```
   mkdir -p ~/ai-visibility-work
   cd ~/ai-visibility-work
   ```
   You'll know it worked when `pwd` prints a path ending in ai-visibility-work. Start Claude Code from inside this folder each time, by typing `claude`.

5. **AV-FU-01-5.** Ask Claude Code to copy the question-battery scripts into your folder. Type this to it:
   "Copy the scripts folder and the references folder from the question-battery skill into this folder, and copy config.example.json from the ai-visibility kit here as config.json."
   You'll know it worked when `ls` lists config.json, scripts, and references. If it cannot find the kit files, it's E31.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

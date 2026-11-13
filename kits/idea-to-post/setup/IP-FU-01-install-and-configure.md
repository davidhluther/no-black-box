# IP-FU-01: Install and Configure

The full version runs on Claude Code (a program from Anthropic that runs on your own computer and can read your files and run tools). It means typing a few lines in the command line (a text window where you type instructions instead of clicking), and each line is given exactly. You do not need to understand them. Allow about an hour. You also need the low-cost Google Sheet from [IP-FR-01](IP-FR-01-make-your-workspace.md), since the [Queue](../glossary.md#queue) still lives there.

1. **IP-FU-01-1.** Install Claude Code by following the shared [install guide](../../../guides/install-claude.md). Come back here when its last step passes.
   You'll know it worked when typing `claude --version` in the command line prints a version number. If it says the command is not found, it's E14.

2. **IP-FU-01-2.** Check that Python (the programming language the kit's small programs use) is installed. In the command line, type this and press Return.

   ```bash
   python3 --version
   ```

   You'll know it worked when it prints a version number beginning with 3. If it says command not found, install Python from python.org and try again; this is E14.

3. **IP-FU-01-3.** Open Claude Code in a new folder for your content work. Type these three lines, one at a time.

   ```bash
   mkdir -p ~/content-work
   cd ~/content-work
   claude
   ```

   You'll know it worked when Claude Code opens and asks what you want to do. If it asks you to sign in, do so with your Claude account.

4. **IP-FU-01-4.** Add the kit. Inside Claude Code, type the following, replacing the address with the repository address shown on the front page of the no-black-box repository.

   ```
   /plugin marketplace add davidhluther/no-black-box
   /plugin install idea-to-post@no-black-box
   ```

   You'll know it worked when Claude Code says the [plugin](../glossary.md#plugin) is installed and lists its [skills](../glossary.md#skill). If a skill is missing or does not respond, it's E15.

5. **IP-FU-01-5.** Copy the settings file. Quit Claude Code, then in the command line type the line below. It copies the example settings to a file you will edit.

   ```bash
   cp config.example.json config.json
   ```

   Open config.[json](../glossary.md#json) in any text editor and replace every example.org value and every example name with your own. Never put a password or key in this file.
   You'll know it worked when the file opens with your organization's name. A message about a missing or broken file is E16.

6. **IP-FU-01-6.** Make the work folders named in the settings file: ideas, briefs, drafts, images, measure, queue, and style.

   ```bash
   mkdir -p ideas/pasted ideas/notes briefs drafts images measure queue style
   ```

   You'll know it worked when `ls` lists those folders.

7. **IP-FU-01-7.** Put your voice and banned-words guide in `style/voice-and-banned-words.md`. If you do not have one, paste in [prompt](../glossary.md#prompt) 0's rules from [prompts.md](../free/prompts.md).
   You'll know it worked when the file exists. The drafting skills stop without it.

8. **IP-FU-01-8.** Run the [check-up](../glossary.md#check-up). In the command line, from your content-work folder, type the line below and press Return. It tests your setup and prints one [support code](../glossary.md#support-code).

   ```bash
   python3 support/doctor.py idea-to-post
   ```

   You'll know it worked when the code ends in OK. Copy the whole code if anything fails. The check-up reports only filenames and whether settings are filled, never your keys or file contents. If the command is not found or the file path is wrong, it's E14 or E16.

Next, [IP-FU-02, connect your data](IP-FU-02-connect-your-data.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

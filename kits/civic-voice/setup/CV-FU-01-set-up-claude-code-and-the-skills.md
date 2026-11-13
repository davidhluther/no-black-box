# CV-FU-01: Set Up Claude Code and the Skills

Full version, guide 1. You will check that your computer has [Python](../glossary.md#python), install [Claude Code](../glossary.md#claude-code) (Anthropic's program that runs on your own computer), add the kit's four [skills](../glossary.md#skill), and fill in your [config file](../glossary.md#config-file). Plan an afternoon the first time. Everything here is typed into the [terminal](../glossary.md#terminal), a window where you type instructions instead of clicking. Copy each command exactly, then press Return. You can finish the free guides first, and your tracker carries over.

1. **CV-FU-01-1.** Open the terminal. On a Mac, press Command and Space, type Terminal, and press Return. On Windows, open the Start menu, type PowerShell, and press Return. Type `python3 --version` (on Windows, try `py --version`) and press Return.
   You'll know it worked when it prints "Python 3.9" or a higher number. If it says "command not found" or shows a number starting with 2, it's E15. The fix is to install Python from python.org/downloads.

2. **CV-FU-01-2.** Install Claude Code. The install command changes from time to time, so open the current instructions at code.claude.com/docs/en/overview, choose the Terminal tab, and run the command it shows for your computer. Then type `claude --version`.
   You'll know it worked when it prints a version number. Most ways of using Claude Code need a Claude subscription or an Anthropic Console account, which you can set up when it first asks you to sign in (see the [shopping list](../shopping-list.md) for prices).

3. **CV-FU-01-3.** Sign in. Type `claude` and press Return from inside the folder you made for your civic work, then follow the on-screen sign-in.
   You'll know it worked when you see a [prompt](../glossary.md#prompt) where you can type a message. Type `/exit` to leave.

4. **CV-FU-01-4.** Get the kit. On the repository's front page, choose Code, then Download ZIP, and unzip it into your Documents folder. Open the kit's folder, `kits/civic-voice`.
   You'll know it worked when you see the files `start-here.md`, `config.example.json`, and a `skills` folder with four folders inside.

5. **CV-FU-01-5.** Add the skills to Claude Code. The repository's front page shows the two exact lines to type inside Claude Code, one to add the marketplace (the list of kits) and one to install the Civic voice kit. Copy them from there.
   You'll know it worked when Claude Code answers each line without an error. If it says it cannot find the marketplace, check the address for a typo, and see E26.

6. **CV-FU-01-6.** Make your own settings file. In the kit's folder, copy `config.example.json` to a new file named `config.json`. Open `config.json` in any text editor and replace the example values with your own: your name or group, your state, the board you follow, its agenda page, and your county names. Keep the quote marks and commas as they are.
   You'll know it worked when the file still opens in a text editor and every value is yours. Never put a password or an [API](../glossary.md#api) key in this file.

7. **CV-FU-01-7.** Test the skills. In Claude Code, started from the kit folder, type: "Which skills do you have from the civic-voice kit?"
   You'll know it worked when it lists public-comment-packet, records-request, census-county-table, and meeting-transcripts. If it lists none, it's E26.

8. **CV-FU-01-8.** Run the [check-up](../glossary.md#check-up). In the terminal, from the repository folder, type `python3 support/doctor.py civic-voice` and press Return. Copy the [support code](../glossary.md#support-code) it prints.
   You'll know it worked when it prints a support code and a short list of what it checked, and it shows exactly what a report would contain before you copy anything. If it prints a problem code, find it in the [fixes table](../fixes.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CV-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

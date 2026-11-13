# Get Ready for the Builder's Toolkit

About 15 minutes. You will open a [terminal](../glossary.md#terminal) (a window where you type [commands](../glossary.md#command)), install nothing new beyond what is listed, and make a practice folder that every later guide uses.

1. **BT-FU-01-1.** Open your terminal. On a Mac, press Command and Space, type Terminal, and press Return. On Windows, open PowerShell from the Start menu. On Linux, open your terminal app.
   You'll know it worked when you see a window with a blinking cursor after a short line of text. If nothing opens, restart your computer and try once more.

2. **BT-FU-01-2.** Install [Claude Code](../glossary.md#claude-code) with the shared guide [install-claude](../../../guides/install-claude.md), then check it. Type this and press Return.

   ```bash
   claude --version
   ```

   You'll know it worked when a version number prints. If you see "command not found", it's E01.

3. **BT-FU-01-3.** Check that [Python](../glossary.md#python) (the language the kit's small programs are written in) is installed.

   ```bash
   python3 --version
   ```

   You'll know it worked when it prints "Python 3" and a number, such as 3.11 or higher. If you see "command not found", it's E02.

4. **BT-FU-01-4.** Make a practice folder and turn on [git](../glossary.md#git) (the free program that tracks a project's history in a [repository](../glossary.md#repository), which is a project folder with that history). Paste all four lines at once.

   ```bash
   mkdir -p ~/work/practice && cd ~/work/practice && git init && git config user.name >/dev/null || echo "Set your name: git config --global user.name \"Your Name\""
   ```

   You'll know it worked when you see "Initialized empty Git repository". If git is not installed, your computer will offer to install it. Say yes, then repeat the line. If it still fails, it's E03.

5. **BT-FU-01-5.** Copy the kit's settings file into the practice folder. In the line below, replace `PATH_TO_KIT` with the folder you downloaded this kit to.

   ```bash
   cp PATH_TO_KIT/config.example.json ~/work/practice/config.json
   ```

   You'll know it worked when `ls ~/work/practice` lists `config.json`. If it says "No such file", you replaced the path wrongly, so it's E04.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like BT-FU-01-3). Run `python3 support/doctor.py builders-toolkit` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

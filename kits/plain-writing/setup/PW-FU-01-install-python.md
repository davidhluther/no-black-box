# PW-FU-01: Install Python

You'll end with Python (a free programming language) installed and ready to run the checkers. It takes about 15 minutes. This is the first time in this kit you'll type instructions to your computer, so each step says exactly what to type.

You'll type into the command line (a window where you type instructions instead of clicking, like texting your computer). On a Mac it's called Terminal. On Windows it's called Command [Prompt](../glossary.md#prompt) or PowerShell.

1. **PW-FU-01-1.** Open the command line. On a Mac, press Command+Space, type `Terminal`, and press Enter. On Windows, press the Windows key, type `PowerShell`, and press Enter.
   You'll know it worked when a window opens with a blinking cursor after some text and a symbol such as `%` or `>`.
2. **PW-FU-01-2.** Check whether Python is already installed. On a Mac, type `python3 --version` and press Enter. On Windows, type `py --version` and press Enter.
   You'll know it worked when you see "Python 3." followed by numbers, such as `Python 3.12.4`. Any version from 3.9 up is fine. If you see that, skip to step 4. If you see "command not found," it's E14.
3. **PW-FU-01-3.** Install Python. Go to python.org/downloads, click the large Download button, and open the file it gives you. Follow the installer's prompts. On Windows, tick the box that says "Add python.exe to PATH" on the first screen before you click Install.
   You'll know it worked when the installer says "Setup was successful" or "Install finished."
4. **PW-FU-01-4.** Close the command line window, open a new one (as in step 1), and run the check from step 2 again.
   You'll know it worked when you see a version number starting with "Python 3." On Windows, remember that you'll type `py` wherever this kit says `python3`.
5. **PW-FU-01-5.** Download the kit. On the repository's front page on GitHub, click the green Code button, then Download ZIP. Open the downloaded [zip file](../glossary.md#zip-file) so it unpacks into a folder. Find the folder `kits/plain-writing` inside it. 
   You'll know it worked when you can see folders named `skills`, `free`, and `setup` inside `plain-writing`.
6. **PW-FU-01-6.** In the command line, move into that folder. Type `cd ` (the letters c and d and a space), then drag the `plain-writing` folder from your file window onto the command line window, and press Enter.
   You'll know it worked when you type `ls` (Mac) or `dir` (Windows) and press Enter, and the list shows `skills`, `free`, and `setup`.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like PW-FU-03-2). Run `python3 support/doctor.py plain-writing` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

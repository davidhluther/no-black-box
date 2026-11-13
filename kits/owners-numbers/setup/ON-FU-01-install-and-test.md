# ON-FU-01 Install and Test the Scripts

You will check that your computer can run the scorecard [scripts](../glossary.md#script), then run them on the invented example business. The scripts only read files and write one new folder. They make no network calls.

1. **ON-FU-01-1.** Open a [command line](../glossary.md#command-line) (a window where you type short instructions instead of clicking). On a Mac, press Command and Space, type Terminal, and press Enter. On Windows, press the Windows key, type Command Prompt, and press Enter.
   You'll know it worked when a window opens with a blinking cursor after a line of text. If it will not open, ask whoever manages the computer.
2. **ON-FU-01-2.** Check for [Python](../glossary.md#python) (a programming language the scripts are written in). Type the next line and press Enter. On Windows, type py instead of python3.

```bash
python3 --version
```

   You'll know it worked when it prints Python 3.9 or higher. If it says command not found, or an older number, install Python from python.org/downloads and run the line again. That is E22.
3. **ON-FU-01-3.** Find the kit's three skill folders, owner-scorecard, pricing-whatif and owner-reports, under `kits/owners-numbers/skills/` in the downloaded repository. Move into the owner-scorecard folder. Replace the path with where you saved it.

```bash
cd path/to/no-black-box/kits/owners-numbers/skills/owner-scorecard
```

   You'll know it worked when typing `ls` (on Windows, `dir`) lists SKILL.md, scripts and assets. If it says no such folder, the path is wrong. Drag the folder into the window to paste its path.
4. **ON-FU-01-4.** Run the scorecard on the invented example business.

```bash
python3 scripts/owner_scorecard.py assets/example --out-dir example-output
```

   You'll know it worked when it prints example-output/scorecard.md. Open that file. It begins with Example Hair Studio (invented). A message starting E20 or E21 means a file or column is missing. See [fixes.md](../fixes.md). If the script cannot write the folder, it's E25.
5. **ON-FU-01-5.** Run the doctor command from the repository's main folder, then copy the [support code](../glossary.md#support-code) it prints.

```bash
python3 support/doctor.py owners-numbers
```

   You'll know it worked when it prints a code that begins with ON-FU. Keep it. If the command is not found, update the repository and try again.

> **How to get help.** Write down the step ID where you got stuck (it looks like ON-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

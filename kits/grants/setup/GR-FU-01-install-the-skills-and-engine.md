# GR-FU-01: Install the Skills and the Engine

**What you'll have.** The four grants skills (folders of written instructions that a chat program can follow) installed in Claude Code, the engine that builds a workbook and a phone page from your tracker's data, and your organization's settings in one place. **Time.** About an hour. **You need.** A computer where you can install programs, a Claude plan that includes Claude Code (see the [shopping list](../shopping-list.md)), and the free version's tracker if you want to carry its data over.

If you get stuck, the check-up (a button or command that tests your setup) prints a support code (a short code that tells a helper which step failed and holds none of your information). The last box on this page says how to use it.

Claude Code is a program that lets an AI model (a program that reads and writes text) work with files on your own computer and run small programs. You type short instructions into the command line (a screen where you type instructions instead of clicking), also called a terminal (the same screen). If you have never done that, the shared [Claude install guide](../../../guides/install-claude.md) walks through it, or ask for help first. The setup questions are free.

1. **GR-FU-01-1.** Install Python (a programming language the engine is written in), version 3, from https://www.python.org/downloads/ and Claude Code by following the [Claude install guide](../../../guides/install-claude.md). Then open a terminal and run the command below.

   ```bash
   python3 --version
   ```

   You'll know it worked when it prints a version such as Python 3.13.5. If it says "command not found", it's E25.

2. **GR-FU-01-2.** Add the kit's marketplace and install the grants plugin (a plugin is a bundle of skills you can install in one step). In Claude Code, type these two lines. The repository (the kit's home on GitHub) is https://github.com/davidhluther/no-black-box, and the first line below is its short form.

   ```
   /plugin marketplace add davidhluther/no-black-box
   /plugin install grants@no-black-box
   ```

   You'll know it worked when Claude Code lists grants-pipeline, funder-research, grant-drafting and giving-channels among its skills. If the install fails, copy the exact message and see E26.

3. **GR-FU-01-3.** Make a private folder for your organization's data, outside any shared or public folder, and copy the engine's example settings into it. Run these lines, replacing the folder name with your own.

   ```bash
   mkdir -p ~/Documents/my-org-grants
   cp kits/grants/config.example.json ~/Documents/my-org-grants/config.json
   cp kits/grants/skills/grants-pipeline/orgs/example.json ~/Documents/my-org-grants/my-org.json
   ```

   You'll know it worked when both files are in the new folder. Run the commands from the folder where you downloaded the kit.

4. **GR-FU-01-4.** Edit the two files in any text editor. A config file (a small settings file) named `config.json` holds your name, tax ID, service area and contacts. The second file, `my-org.json`, is written in [JSON](../glossary.md#json) (a way of writing settings as text with curly braces), and its comments explain each part. Change the names, the "data_dir" path to your folder, the stages of your work and the words under sweep (the weekly search). Remove or replace the example funder names.
   You'll know it worked when this command prints your settings back with no error. Do the same for `config.json`. Do not paste your settings into a website to check them. A missing comma or quotation mark is E27.

   ```bash
   python3 -m json.tool ~/Documents/my-org-grants/my-org.json
   ```

5. **GR-FU-01-5.** Match your tracker's columns to the engine's files. The free tracker's Pipeline tab maps to the engine's pipeline-rows.csv like this. Export the tab (File, Download, Comma-separated values), then rename the columns in the first row.

   | Free tracker column | Engine column | Notes |
   |---|---|---|
   | Funder | funder | |
   | Program or purpose | purpose | |
   | (none) | locality | Type Local, Regional or National |
   | Request ($) | request | Plain number, no dollar sign or comma |
   | Status | status | Same words |
   | Submitted, Decision date | submitted, decision | m/d/yy or m/d/yyyy |
   | Award ($) | award | Plain number |
   | Eligible (Y or N) | elig | |
   | Mission, Geography, Fund-area, Relationship, Reporting ease | mission, geo, fund_area, reln, report_ease | 1 to 5 |
   | Chance of winning (%) | p_win | Whole number such as 40 |
   | Effort (hours) | effort | |
   | Notes and source | notes, source | Split if you like |
   | Funder link | funder_url | |
   | Deadline, Next step | (none) | Put them in notes |

   The other engine files have their own headers in the templates folder: funder-intel.csv, wider-net.csv and dossier-index.csv. The Funders tab fills dossier-index.csv and wider-net.csv.
   You'll know it worked when each CSV has its engine header row and at least one data row. The builders stop on an empty file, which is E28.

6. **GR-FU-01-6.** Run the check. In the same terminal, run the command below and copy the support code it prints.

   ```bash
   python3 support/doctor.py grants
   ```

   You'll know it worked when the last line shows a code containing E00. Any other code is in [fixes](../fixes.md).

Next, build the workbook and page in [GR-FU-02](GR-FU-02-build-the-workbook-and-page.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

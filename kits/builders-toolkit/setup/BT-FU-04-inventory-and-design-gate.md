# Map Your Projects and Check a Page

About 25 minutes. You will list every project folder on your computer, then lay a web page out in a real browser and read the report. If you build no websites, do steps 1 and 2 and skip the rest.

1. **BT-FU-04-1.** Run the inventory. Ask [Claude Code](../glossary.md#claude-code) to run it with your settings.

   ```
   Use the workstream-inventory skill with the projects_folder and routing_table from config.json. Tell me how many repositories it found and whether it filtered anything.
   ```

   You'll know it worked when you get a table of projects with last [commit](../glossary.md#commit) dates, plus a count. If it reports 0 repositories, your `projects_folder` setting points at the wrong place, so it's E10.

2. **BT-FU-04-2.** Read the "NOT in the routing table" list. Each name there is a project your written notes never mention.

   You'll know it worked when you can say, for each name, whether to add a line for it or leave it out on purpose. If the list is empty, nothing was missed. If it says the routing table file does not exist, the check could not run, and the answer is to create a `CLAUDE.md` in your home folder listing your projects.

3. **BT-FU-04-3.** Install what the [design gate](../glossary.md#design-gate) needs: [Playwright](../glossary.md#playwright) and a browser. Run these two lines.

   ```bash
   python3 -m pip install playwright pillow numpy && python3 -m playwright install chromium
   ```

   You'll know it worked when the second line finishes without the word "error". If you see "No module named playwright" later, it's E11.

4. **BT-FU-04-4.** Prove the gate works on its built-in test pages. These deliberately contain a gap, a sideways scroll and an empty section. Ask Claude Code:

   ```
   Use the design-gate skill to run the gate on its own fixtures with config/fixtures.json and --serve fixtures/. Tell me what each fixture page produced.
   ```

   You'll know it worked when void.html, overflow.html and ghost-section.html each report a problem and clean.html reports none. If it exits with code 2, it's E12.

5. **BT-FU-04-5.** Run the gate on your own site. Start your site's [development server](../glossary.md#development-server) on a port you choose (for example 3100), copy the [skill](../glossary.md#skill)'s `config/example-site.example.json` to `.design-gate.json` in your site folder, then ask:

   ```
   Run the design gate on /about and the home page at http://127.0.0.1:3100 with --expect-marker set to the short git hash of this checkout.
   ```

   You'll know it worked when `report.json` lists a `target` block with your port and a verdict of PASS or WARN. If it exits with code 2 and says the marker did not match, it's E13, and that is the gate protecting you from measuring the wrong copy.

6. **BT-FU-04-6.** Run the judgment pass with a reviewer who did not build the page. Ask:

   ```
   Start a subagent. Give it only judgment-packet.md, the screenshots and my DESIGN.md. Do not tell it why I made the change. Ask it for findings on the six judgment checks.
   ```

   You'll know it worked when you get findings or a "no findings" note, each marked severity 1 or 2. If you have no `DESIGN.md`, write a short one first (heading sizes, spacing, a list of devices you never want), and the gate will use it.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like BT-FU-01-3). Run `python3 support/doctor.py builders-toolkit` and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

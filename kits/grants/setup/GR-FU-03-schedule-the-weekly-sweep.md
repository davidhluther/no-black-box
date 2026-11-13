# GR-FU-03: Schedule the Weekly Sweep

**What you'll have.** A weekly search of Grants.gov (the US government's public list of grant opportunities) and local news that runs by itself, writes every attempt and result to a log, and alerts you the same day if it fails or a week is missed. **Time.** About 30 minutes. **You need.** A finished [GR-FU-02](GR-FU-02-build-the-workbook-and-page.md), and a computer that is on at the chosen time.

If you get stuck, the check-up (a button or command that tests your setup) prints a support code (a short code that tells a helper which step failed and holds none of your information). The last box on this page says how to use it.

The sweep (a search that runs by itself every week) only reads public websites. It never contacts a funder.

1. **GR-FU-03-1.** Test the sweep without saving anything.

   ```bash
   cd kits/grants/skills/grants-pipeline
   python3 engine/sweep.py --config ~/Documents/my-org-grants/my-org.json --dry-run
   ```

   You'll know it worked when it prints scored notices and ends with a line such as "12 new, 12 total, failed: none". If a source is listed under failed, it's E30.

2. **GR-FU-03-2.** Run it through the wrapper, which records every attempt and raises an alert on failure.

   ```bash
   python3 ../../full/sweep_wrapper.py --engine engine --config ~/Documents/my-org-grants/my-org.json
   ```

   You'll know it worked when a file named wrapper.jsonl appears in your data folder's sweep folder with an "attempting" line and an "ok" line.

3. **GR-FU-03-3.** Set up the alerts. The wrapper always writes an ALERT file, prints a message and, on a Mac, shows a desktop notice. For email, set these in your computer's environment, not in any file you share: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD and ALERT_TO. The kit never reads or prints them anywhere else. To test, make the sweep fail on purpose by running the wrapper with a wrong config path.
   You'll know it worked when an ALERT file appears and, if you set email, a message arrives. If email never arrives but the ALERT file does, it's E31.

4. **GR-FU-03-4.** Schedule two jobs with your computer's scheduler (the part of the computer that runs programs on a timetable, called cron on a Mac or Linux and Task Scheduler on Windows). On a Mac or Linux, type crontab -e and add these two lines, changing the paths and the time. The first runs every Thursday at 8:25 a.m. The second checks every morning that a recent run succeeded.

   ```
   25 8 * * 4 python3 /path/to/kits/grants/full/sweep_wrapper.py --engine /path/to/kits/grants/skills/grants-pipeline/engine --config /path/to/my-org.json
   40 8 * * * python3 /path/to/kits/grants/full/sweep_wrapper.py --engine /path/to/kits/grants/skills/grants-pipeline/engine --config /path/to/my-org.json --check-fresh 8
   ```

   You'll know it worked when the next Thursday adds an "ok" line to wrapper.jsonl. A missed run raises an alert on the following morning. If nothing runs, it's E32.

5. **GR-FU-03-5.** Read the results each week. Open candidates.csv in your sweep folder, read the highest-scored notices, and add real ones to your tracker.
   You'll know it worked when you have added or dismissed every Tier 2 notice.

> **How to get help.** Write down the step ID where you got stuck (it looks like GR-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

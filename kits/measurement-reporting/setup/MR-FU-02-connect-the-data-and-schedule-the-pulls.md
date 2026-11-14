# Connect the Data and Schedule the Pulls (MR Full, Guide 2)

The pulls are read-only and the same for every site. What changes at team scale is who holds the secrets, how many sites one pull covers, and what happens when a slot is missed. About two hours the first time.

For the account setup itself, follow the existing guide for [read-only access](../../measure/setup/MM-FU-02-give-the-scripts-read-only-access.md) rather than repeating it here. For AI-visibility keys, use [AV-FU-02](../../ai-visibility/setup/AV-FU-02-get-and-store-your-keys.md). Read [Keys and accounts](../../../guides/keys-and-accounts.md) for where each account lives.

1. **MR-FU-02-1.** Create one [service account](../glossary.md#service-account) for the team, not one per person, and grant it "Restricted" (read-only) access on each [Search Console](../glossary.md#search-console) property you report on. Store its key file in a secrets store or a private folder the scheduled job can read, never in a shared drive or a repository. Follow steps 1 and 2 of the [read-only access guide](../../measure/setup/MM-FU-02-give-the-scripts-read-only-access.md).
   You'll know it worked when the service account's email appears with "Restricted" on every property in the list. If Search Console answers 403, it's E19.

2. **MR-FU-02-2.** Tell the pull which sites it may read. Set the sites as a comma-separated list in an [environment variable](../glossary.md#environment-variable), plus the key path:

   ```bash
   export GSC_SA_KEY="/path/to/private/search-console-key.json"
   export GSC_SITES="sc-domain:example.org,https://www.example.net/"
   ```

   The `gsc-read` [skill](../glossary.md#skill) refuses any site not in this list, so a typo cannot reach another property.
   You'll know it worked when `echo "$GSC_SITES"` prints your list. If a pull says the site is "not listed", it's E29.

3. **MR-FU-02-3.** Add the [Clarity](../glossary.md#clarity) [token](../glossary.md#token) for each project, one token per project, held by a project admin. Follow step 4 of the read-only guide. Clarity allows a small number of calls per project per day, so plan which calls the schedule uses and leave the rest for questions.
   You'll know it worked when a pull with `--dry-run` prints the request without sending it. If it says the daily limit is used, it's E26. If it cannot find the token, it's E25.

4. **MR-FU-02-4.** Plan the pulls on a calendar and write them into the owner table from guide 1. A workable default is a weekly Search Console capture, a daily or weekly Clarity pull, and a monthly [GA4](../glossary.md#ga4) totals export that you read from the interface or an export. Keep each pull's output in the site's own folder, named with the date.
   You'll know it worked when the calendar shows each pull's day, owner and output folder.

5. **MR-FU-02-5.** Wrap every scheduled pull so it always leaves a line in a [run log](../glossary.md#run-log), whether it worked or not. Save this as `run-and-log.sh` next to your site folders:

   ```bash
   #!/bin/sh
   # Usage: run-and-log.sh NAME COMMAND [ARGS]
   name="$1"; shift
   day=$(date +%Y-%m-%d)
   if "$@"; then
     echo "$day $name ok" >> "$HOME/measurement/run-log.txt"
   else
     echo "$day $name FAILED" >> "$HOME/measurement/run-log.txt"
   fi
   ```

   Then schedule it with your [scheduler](../glossary.md#scheduler). On a Mac or Linux machine, run `crontab -e` and add a line such as the first one below. The second is the slot check from step 6:

   ```bash
   0 7 * * 1 /path/to/run-and-log.sh gsc python3 /path/to/skills/gsc-read/scripts/gsc_read.py --site sc-domain:example.org --out /path/to/sites/example-org/gsc-latest.json
   30 9 * * 1 grep -q "^$(date +\%Y-\%m-\%d) gsc ok" "$HOME/measurement/run-log.txt" || echo "gsc pull missed or failed" | mail -s "Pull missed" name@example.org
   ```

   Use your own paths and your team's alert channel instead of mail if you have one.
   You'll know it worked when a test run adds a line to the log, and breaking the command on purpose adds a FAILED line and sends the alert. If the job never ran at all, it's E32.

6. **MR-FU-02-6.** Set the rule that a miss is a failure, even when older data is still fresh. A failed or skipped run is recorded, retried by hand the same day and flagged to the report owner. The retry result goes in the run log, and the gap goes in the report's caveats if it reaches the report. Never let a week pass without either the data or a note saying why it is missing.
   You'll know it worked when, for any week you pick, the run log shows either an ok line or a FAILED line with a retry line after it. If the log has no line for a slot, treat that as a miss.

7. **MR-FU-02-7.** Verify each Search Console capture before anyone uses it. Run `python3 scripts/verify_capture.py --site sc-domain:example.org --file <capture>.json` from the `gsc-read` skill folder. It tells you whether the capture is adoptable.
   You'll know it worked when it says "adoptable". If it says "not adoptable", read its one-line reason: usually the capture is a day old or hit the row cap. Take a fresh one before reporting.

Next: [Run the monthly cycle and report to leaders](MR-FU-03-run-the-monthly-cycle-and-report-to-leaders.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MR-FU-02-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

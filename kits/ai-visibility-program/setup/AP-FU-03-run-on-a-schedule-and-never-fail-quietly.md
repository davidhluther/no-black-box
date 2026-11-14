# AP-FU-03: Run on a Schedule and Never Fail Quietly

Time, about two hours plus waiting. You run the first month by hand to check cost and quality, then hand the monthly run to a scheduler and add a daily check. The rule behind this guide is that a missed or failed run counts as a failure even when last month's data is still fresh. Every miss gets recorded, retried and flagged to the team the same day.

Remember that the runner asks each company's developer service, so its answers are not what a customer sees in the apps. The runner tags them "-api". Never compare them with hand-run app answers.

1. **AP-FU-03-1.** Run one site first, to see what a run costs and what it looks like. From the program folder:
   ```
   set -a && . ./.env && set +a
   python3 run_program.py run --site example-us
   ```
   Replace `example-us` with one of your site ids. Then read at least five answers in `sites/example-us/runs/<month>-api/answers/` and the `searches` lines in each `.jsonl` file.
   You'll know it worked when the program prints "ok" for that site and `program-ledger.csv` has a row with status `ok`. Open the company billing pages and write down what the run cost, so you can multiply it by sites. If every question says ERROR, a 401 or 403 is a key problem (E37 in the [single-site fixes](../../ai-visibility/fixes.md)) and a 429 is a limit (E38).

2. **AP-FU-03-2.** Run the rest.
   ```
   python3 run_program.py run
   ```
   Sites that already have a good run for this month are skipped. A site that fails is moved aside to a folder ending `.failed-1`, tried again after the wait you set, and flagged if it still fails.
   You'll know it worked when the [ledger](../glossary.md#ledger) has one `ok` row per site for the month. If one site failed after its retries, the program prints the alert text and you read that site's log in `logs/`. See E42.

3. **AP-FU-03-3.** Have the reviewer correct the drafts. For each site, open `runs/<month>-api/scored-draft.csv` in a spreadsheet. Every row says "DRAFT by [script](../glossary.md#script)", because the runner only matches your name and domain. The reviewer reads each answer and fixes named, position, your_site_cited, others_named and resolved_to, then saves the file as `scored.csv` in the same folder. This is the one step the program cannot do for you.
   You'll know it worked when no row says DRAFT and `scored.csv` exists for every site. The daily check flags a site whose `scored.csv` is still missing `review_days` after its run (E52).

4. **AP-FU-03-4.** Make the two scheduled scripts. The first runs the month. The second checks the ledger every day, which is what catches a machine that was off. Run these in the program folder.
   ```
   printf '#!/bin/sh\ncd "$HOME/ai-visibility-program" || exit 1\nset -a; . ./.env; set +a\npython3 run_program.py run\n' > run-monthly.sh
   printf '#!/bin/sh\ncd "$HOME/ai-visibility-program" || exit 1\nset -a; . ./.env; set +a\npython3 run_program.py check\n' > run-daily-check.sh
   chmod 700 run-monthly.sh run-daily-check.sh
   ```
   Test each one by hand, once, with `./run-daily-check.sh`.
   You'll know it worked when the daily check prints the [slot](../glossary.md#slot), one line per site, and "waiting" or "ok" next to each.

5. **AP-FU-03-5.** Schedule them with [cron](../glossary.md#cron), the scheduler built into Mac and Linux. Type `crontab -e` and add these two lines, changing the day to your `run_day_of_month`. On Windows, ask your IT team for a scheduled job that runs the same two scripts.
   ```
   0 6 3 * * /bin/sh $HOME/ai-visibility-program/run-monthly.sh >> $HOME/ai-visibility-program/logs/cron.log 2>&1
   30 9 * * * /bin/sh $HOME/ai-visibility-program/run-daily-check.sh >> $HOME/ai-visibility-program/logs/cron.log 2>&1
   ```
   You'll know it worked when `crontab -l` lists both lines. On a Mac, cron may need permission to read your folder under System Settings, Privacy and Security, Full Disk Access. A job that never ran looks the same as a quiet month, so confirm the first scheduled run by finding its row in the ledger. If there is none, it's E40.

6. **AP-FU-03-6.** Connect the alerts. Create an incoming [webhook](../glossary.md#webhook) in the team chat channel (your chat tool's admin page says how), add one line to `.env` in the form `PROGRAM_ALERT_WEBHOOK=the-address`, and prove it works:
   ```
   set -a && . ./.env && set +a
   python3 run_program.py check --test-alert
   ```
   You'll know it worked when the test message appears in the channel. If the program prints "No alert sent", the variable is missing, and if it prints "could not be posted", the address is wrong (E48). The webhook address is a secret. Do not paste it into `config.json`, a ticket or a chat.

7. **AP-FU-03-7.** Run a miss drill, so the first real miss is not also the first time anyone sees an alert. This pretends today is the 20th of a month in which nothing ran:
   ```
   mv program-ledger.csv program-ledger.bak
   python3 run_program.py check --today 2026-12-20
   mv program-ledger.bak program-ledger.csv
   ```
   Change the date to the 20th of the current or a future month. You'll know it worked when each site prints MISSED and the alert reaches the channel. Put the daily check on a second machine or a hosted scheduler too if you can, because a dead machine cannot report that it is dead.

8. **AP-FU-03-8.** Agree the same-day rule in writing, in `reports/incidents.md`: who reads the alert, who fixes by when, and what gets written down. For every miss or failure add one row with the date, the site, the cause, the fix and when the rerun finished. A silent failure looks exactly like a quiet month, so an empty incident log should mean nothing happened, not that nobody looked.
   You'll know it worked when `reports/incidents.md` exists and the owner and backup have both read it. To rerun a site after fixing the cause, use `python3 run_program.py run --site example-us --force`.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AP-FU-03-5). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

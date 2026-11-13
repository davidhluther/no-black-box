# Give the Scripts Read-Only Access (Full, Guide 2)

The [Search Console](../glossary.md#search-console) and [Clarity](../glossary.md#clarity) [skills](../glossary.md#skill) need permission to read your data. You will create that permission with the narrowest rights, and keep the secret out of every shared folder. About 40 minutes. For where each account lives and what it costs, see [Keys and accounts](../../../guides/keys-and-accounts.md).

1. **MM-FU-02-1.** Make a [service account](../glossary.md#service-account) (a login that belongs to a program, not a person). In Google Cloud console (console.cloud.google.com) pick or create a project, open "IAM and Admin", then "Service accounts", then "Create service account", and name it "search-console-reader". Skip the optional role steps. Open the account, choose Keys, "Add key", "Create new key", JSON. A file downloads; that file is the secret.
   You'll know it worked when a .json file is in your Downloads folder. Move it to a private folder such as `~/.config/measure/` and never email it, post it or put it in a shared drive. If you cannot create a project, it's E24.

2. **MM-FU-02-2.** Let the account read Search Console. In the Google Cloud console enable the "Google Search Console [API](../glossary.md#api)" for the project. In Search Console, open Settings, "Users and permissions", "Add user", paste the service account's email address (it ends in iam.gserviceaccount.com), and choose "Restricted", which is read-only.
   You'll know it worked when the account appears in the user list with "Restricted".

3. **MM-FU-02-3.** Tell the program where the key is without writing the secret into any file the kit shares. Use an [environment variable](../glossary.md#environment-variable). In a terminal run these two lines, replacing the path and site name:

   ```bash
   export GSC_SA_KEY="$HOME/.config/measure/search-console-key.json"
   export GSC_SITES="sc-domain:example.org"
   ```

   Run `pip install google-api-python-client google-auth` once to add the two libraries the script needs. These settings last only for that terminal window, which is a feature: close the window and the setting is gone.
   You'll know it worked when running `echo "$GSC_SITES"` prints your site name. If `pip` is not found, it's E22.

4. **MM-FU-02-4.** Make the Clarity [token](../glossary.md#token) (a long secret code that proves a program may read your data). Only a Clarity project admin can. At clarity.microsoft.com open the project, Settings, Data Export, "Generate new API token", name it with four to 32 letters, digits, hyphens, underscores or periods, copy it right away because Clarity shows it once, and store it:

   ```bash
   mkdir -p ~/.config/clarity
   printf '%s' 'paste-token-here' > ~/.config/clarity/my-site.token
   chmod 600 ~/.config/clarity/my-site.token
   ```

   You'll know it worked when running `ls -l ~/.config/clarity` shows the file with `-rw-------`. The Clarity script refuses to read a token kept inside a project folder under version control, and never prints it. If a run says the token is missing, it's E25.

5. **MM-FU-02-5.** Test both with no risk. Ask Claude Code to run the Clarity script with `--dry-run`, which prints the exact request without sending it. Then run a Search Console capture for your site (the gsc-read skill shows the command). Both only read.
   You'll know it worked when the Search Console run writes a dated JSON file and prints nothing alarming, and the dry run lists the request. If Search Console answers "403" or "failed", it's E19. If Clarity says you have used the daily limit, it's E26.

Next: [Run the monthly routine](MM-FU-03-run-the-monthly-routine.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

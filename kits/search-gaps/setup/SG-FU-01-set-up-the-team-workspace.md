# SG-FU-01: Set Up the Team Workspace

You will install the kit, list your sites in one [config file](../glossary.md#config-file), make a folder for each site, and run a first read-only check. About an hour. The install and key steps are the same as in the small-business full version, so this guide links to them and spends its time on what changes with several sites.

If you get stuck, the check-up command prints a [support code](../glossary.md#support-code) that tells a helper which step failed. The box at the bottom says where to send it.

1. **SG-FU-01-1.** Install [Claude Code](../glossary.md#claude-code) and check [Python](../glossary.md#python) on the computer that will run the checks. Follow [the install guide](../../../guides/install-claude.md), then in the [terminal](../glossary.md#terminal) type:

   ```
   python3 --version
   ```

   You'll know it worked when typing `claude` opens a chat [prompt](../glossary.md#prompt) and the version command prints a number such as `Python 3.12.1`. If the terminal says "command not found", it's E15.

2. **SG-FU-01-2.** Get and store your keys. The only key the kit can use that you may not have is an [API key](../glossary.md#api-key) for your link database (named `AHREFS_API_KEY` for [Ahrefs](../glossary.md#ahrefs)). A second, optional one named `GOOGLE_API_KEY` lets the speed check run itself. Follow [Keys and accounts](../../../guides/keys-and-accounts.md), and use [AV-FU-02](../../ai-visibility/setup/AV-FU-02-get-and-store-your-keys.md) for the exact way to store a key without writing it in a file. Give each analyst their own key if your platform allows it.
   You'll know it worked when `echo ${#AHREFS_API_KEY}` prints a number above zero. That prints the key's length, not the key. If you have no link database, skip this step and the report will use the free path. A rejected key is E05.

3. **SG-FU-01-3.** Install the kit's [plugin](../glossary.md#plugin). Inside Claude Code, type these two lines, one at a time:

   ```
   /plugin marketplace add davidhluther/no-black-box
   /plugin install search-gaps@no-black-box
   ```

   A [plugin](../glossary.md#plugin) bundles the 17 skills. If you already installed the small-business plugins, remove them first, so the same [skill](../glossary.md#skill) name doesn't load twice (E20).
   You'll know it worked when Claude Code says the plugin was installed. If it can't find the marketplace, check the address and see E15.

4. **SG-FU-01-4.** Make your settings file. In the terminal, go to the kit's folder and copy the example:

   ```
   cp config.example.json config.json
   ```

   Open `config.json` in a text editor. Keep one block per site or market inside `sites`, and delete the second example block if you only have one site. Fill in each site's address, owner, [Search Console](../glossary.md#search-console) property, and up to six competitors. Leave `customer_research` for later if you aren't running those skills yet.
   You'll know it worked when no example.org address is left in a block you plan to use. If a later step says the file won't load, you removed a quote or a comma, and it's E16.

5. **SG-FU-01-5.** Make a folder for each site and copy the two templates. A site folder holds that site's [crawl](../glossary.md#crawl) export, its [baseline](../glossary.md#baseline), and its reports, so two sites never share a file.

   ```
   mkdir -p gap-review-output/example-us/baseline gap-review-output/example-us/reports
   cp templates/run-log.csv gap-review-output/run-log.csv
   cp templates/gap-register.csv gap-review-output/gap-register.csv
   ```

   Replace `example-us` with each site's name from your config. Keep the [run log](../glossary.md#run-log) and the [gap register](../glossary.md#gap-register) at the top, one file each for the whole team, so a leader can see everything in one place. If you prefer a shared Google Sheet, import the two [CSV](../glossary.md#csv) files into it and keep that sheet as the single copy.
   You'll know it worked when each site has its own folder and there is one run log and one register. If two people each keep their own copy, that is E14.

6. **SG-FU-01-6.** Run the check-up. It tests that Python is new enough, that the kit is in place, and that `config.json` loads and has your team name and sites. It never prints key values.

   ```
   python3 support/doctor.py search-gaps
   ```

   You'll know it worked when it reports every item as passing and prints a support code. If it lists a problem, look the code up in [fixes](../fixes.md).

7. **SG-FU-01-7.** Run a first read-only check on one site. In Claude Code, type: "Read config.json and build the baseline for the site named Example US. Use only my Search Console export and the crawl file I give you. Do not change any file except the baseline folder." Export the last 90 days of queries and pages from [Search Console](../glossary.md#search-console) first, and save them in that site's `baseline` folder.
   You'll know it worked when the [baseline](../glossary.md#baseline) has four tables and a date, and a short note says which sources were missing. If Claude asks for a number it can't verify and invents one, discard that answer, and see E11.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like SG-FU-01-3). Run `python3 support/doctor.py search-gaps` and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

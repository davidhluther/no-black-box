# WC-FU-01: Install in Claude Code

You will install the kit in [Claude Code](../glossary.md#claude-code), tell it about your business, and run the first [scorecard](../glossary.md#scorecard). About 45 minutes. This is the only guide that uses a [command line](../glossary.md#command-line), and every line to type is shown. You need the free version finished first, and a Claude plan that includes Claude Code.

If you get stuck, the doctor command prints a [support code](../glossary.md#support-code), a short code that tells a helper which step failed. The box at the bottom says where to send it.

1. **WC-FU-01-1.** Install Claude Code by following [the install guide](../../../guides/install-claude.md). See [Keys and accounts](../../../guides/keys-and-accounts.md) for the plan and sign-in.
   You'll know it worked when typing `claude` in the [terminal](../glossary.md#terminal) opens a chat [prompt](../glossary.md#prompt). If the terminal says "command not found", it's E16.

2. **WC-FU-01-2.** Check that [Python](../glossary.md#python) is installed. In the terminal, type:

   ```
   python3 --version
   ```

   You'll know it worked when it prints a version number, such as `Python 3.12.1`. If it says "command not found", install Python from python.org and try again, and see E16.

3. **WC-FU-01-3.** Add the kit's marketplace and install the [plugin](../glossary.md#plugin). Inside Claude Code, type these two lines, one at a time. Replace the address with the one shown at the top of the kit's GitHub page.

   ```
   /plugin marketplace add davidhluther/no-black-box
   /plugin install website-checkup
   ```

   You'll know it worked when Claude Code says the plugin was installed. If it can't find the marketplace, check the address, and see E17.

4. **WC-FU-01-4.** Make your settings file. In the terminal, go to the kit's folder and copy the example. A [config file](../glossary.md#config-file) holds the details that belong to your business.

   ```
   cp config.example.json config.json
   ```

   Open `config.json` in any text editor and replace each example value with your own. Copy the values from your Config tab. Never put a key in this file. Keep keys in environment settings, as [Keys and accounts](../../../guides/keys-and-accounts.md) explains.
   You'll know it worked when `config.json` has your business name and site address instead of the example.org ones. If the file refuses to load later, you probably deleted a quote or comma, and it's E17.

5. **WC-FU-01-5.** Run the doctor command, which tests your setup and prints a support code.

   ```
   python3 support/doctor.py website-checkup
   ```

   You'll know it worked when it reports every item as passing. If it lists a problem, look up its E code in the fixes table.

6. **WC-FU-01-6.** Ask for your first scorecard. In Claude Code, type: "Run the site scorecard for my business, using config.json."
   You'll know it worked when it asks only for what the config lacks, opens your pages, and writes a scorecard with five headlines and a list titled "What this check could not see". If it can't reach a page, it marks the check unknown, and that's correct. If it reports a number with no source, it's E12.

> **How to get help.** Write down the step ID where you got stuck (it looks like WC-FU-01-3). Run `python3 support/doctor.py website-checkup` and copy the support code it prints. Then send both to Pigasus Group at [https](../glossary.md#https)://pigasus.group/contact. Setup questions are free.

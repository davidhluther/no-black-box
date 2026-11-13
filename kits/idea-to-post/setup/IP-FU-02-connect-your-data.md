# IP-FU-02: Connect Your Data

The full version reads your [Search Console](../glossary.md#search-console) numbers and, if you choose, a paid [keyword](../glossary.md#keyword) tool. Each connection needs an [API](../glossary.md#api) key (a long secret password that proves a program may use a service) or a sign-in. Every key goes in an environment variable (a setting stored outside your files) and never in config.[json](../glossary.md#json). Allow about 45 minutes.

1. **IP-FU-02-1.** Read the [keys and accounts guide](../../../guides/keys-and-accounts.md) section on keeping keys out of shared files and screenshots before you create anything.
   You'll know it worked when you can say where each key will live.

2. **IP-FU-02-2.** Make sure Search Console is verified for your site (see IP-FR-03) and that `measurement.search_console_property` in config.json holds the property name.
   You'll know it worked when Search Console shows the property as verified. If not, it's E10.

3. **IP-FU-02-3.** Give the gsc-read [skill](../glossary.md#skill) access using the method its own page describes (a sign-in, or an export file placed in your measure folder). Ask [Claude Code](../glossary.md#claude-code): "Pull the last 28 days of Search Console data for my site with gsc-read."
   You'll know it worked when a file appears in your measure folder and Claude Code summarizes it. A permission or "not found" error is E10 or E11.

4. **IP-FU-02-4.** (Optional.) If you chose a paid keyword tool, create its key as the keys guide shows, and set it as an environment variable in your [command line](../glossary.md#command-line) profile. Do not paste it into a chat.
   You'll know it worked when Claude Code can read a keyword overview without asking you to type the key. If it asks for the key, it's E16.

5. **IP-FU-02-5.** (Optional.) Connect [Microsoft Clarity](../glossary.md#microsoft-clarity) and Google Analytics 4 only if you already use them. The clarity-analytics skill describes the export it needs.
   You'll know it worked when each skill reports a first export without errors.

6. **IP-FU-02-6.** Re-run `python3 support/doctor.py idea-to-post`.
   You'll know it worked when the code still ends in OK.

Next, [IP-FU-03, ideas to brief](IP-FU-03-ideas-to-brief.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

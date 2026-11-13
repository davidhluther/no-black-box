# Getting Help

Stuck is normal, and it is almost never your fault. This page shows the fastest route to unstuck, and what to send so nobody has to guess.

Terms are in the [glossary](glossary.md). If your trouble is finding or opening a [kit's](glossary.md#kit) files, read [get the kit files](get-the-files.md) first.

## Three steps, in this order

1. **NB-FR-06-1.** Write down the [step ID](glossary.md#step-id) where you stopped. Every numbered step in every guide starts with one, like GR-FR-01-3 (Grants kit, free version, guide one, step three).
   You'll know it worked when you have something like "BP-FR-02-4" on a note. If a step has no ID, copy its first few words.
2. **NB-FR-06-2.** Look for the matching problem code. If the guide said "it's E14," open the kit's fixes page and find E14. It lists what you see, why it happens, and the fix. For the shared guides, use the table below.
   You'll know it worked when you find a row that matches what is on your screen. If nothing matches, go on to step 3.
3. **NB-FR-06-3.** Run the [check-up](glossary.md#check-up) if your kit has one. In a Google Sheet, open the Kit help menu and choose Run check-up. In the full version, type `python3 support/doctor.py <kit-id>` into your terminal (the window where you type commands). Either way you get one [support code](glossary.md#support-code) and, if you choose, a plain-text report.
   You'll know it worked when a code like `GR-FR-03-2-E14-v0.1.0-7KQ` appears.

The report never contains passwords, keys, donor or client data, or the contents of your files. It shows you exactly what it will share before you copy anything. The code format is explained in [support-code-format](../support/support-code-format.md).

## Ask for help

Send the step ID and the support code (and the report, if you made one) to Pigasus Group at https://pigasus.group/contact. Setup questions are free. If you are asking an [AI model](glossary.md#ai-model) instead, paste the same two items and add which device you use and what you see on screen, then leave out anything private.

## Shared fixes

These codes belong to the shared guides, whose step IDs begin NB.

| Code | What you see | Why | Fix | Step |
|---|---|---|---|---|
| E01 | Claude.ai sends you back to sign in over and over | A browser extension or old saved data is blocking the sign-in | Try a private window or another browser | NB-FR-01-1 |
| E02 | You can't find the [code execution](glossary.md#code-execution) switch | Your account or organization hides it | Ask the account owner to turn it on under Settings, Capabilities | NB-FR-01-2 |
| E03 | The Releases page has no zip files | The kit isn't released yet | Use the free version's prompts instead | NB-FR-01-3 |
| E04 | Claude says the uploaded file is invalid | The zip contains an extra folder or was renamed | Download the zip again and upload it without opening it | NB-FR-01-4 |
| E05 | The terminal says "command not found: claude" | [Claude Code](glossary.md#claude-code) isn't installed, or the terminal was open before you installed it | Close the terminal, open a new one, and try again | NB-FU-01-1 |
| E06 | The [marketplace](glossary.md#marketplace) can't be found | A typo in the owner name or address | Copy the address from the GitHub page and retry | NB-FU-01-2 |
| E07 | A check says config.json is invalid | A missing quote or comma | Paste the file into a JSON checker and fix the line it names | NB-FU-01-4 |
| E08 | ChatGPT says the instructions are too long | More than one file was pasted | Paste only `chatgpt/instructions.md` | NB-FR-02-6 |
| E09 | A key appears in a shared file or screenshot | It was pasted somewhere public | Delete it there and make a new key on the service's website | NB-FR-03-1 |
| E10 | The [VPN](glossary.md#vpn) app shows an error and won't connect | Wrong sign-in, or the administrator hasn't added the device | Ask the administrator to confirm your account and device | NB-FR-04-3 |
| E11 | The [router](glossary.md#router) label is missing | It wore off or was removed | Find the model on the maker's support page | NB-FR-05-1 |
| E12 | You can't find the downloaded kit files, or the folder looks empty | The ZIP was not unzipped, or it is in a different folder than you expected | Follow [get the kit files](get-the-files.md) from the step that finds the Downloads folder | NB-FR-07-3 |
| E90 | The check-up says your [Python](glossary.md#python) is too old | The program that runs the kit's scripts is out of date | Install the current Python from python.org | any |
| E91 | The check-up can't find the kit folder | You ran it from the wrong place | Open the terminal in the folder that contains `kits` | any |
| E92 | The check-up can't find config.json | You haven't copied config.example.json yet | Copy it to config.json and fill it in. If you keep it in another folder, add `--config` and the file's location to the check-up command | any |
| E93 | The check-up says config.json isn't valid | A missing quote or comma | Same fix as E07 | any |
| E94 | The check-up says a key name isn't set | The line is missing from your `.env` file | Add the line, see [keys and accounts](keys-and-accounts.md) | any |
| E95 | The check-up says an optional tool isn't installed | The kit works without it, but one feature won't | Install it, or skip that feature | any |

> **How to get help.** Write down the step ID where you got stuck (it looks like NB-FR-06-2). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

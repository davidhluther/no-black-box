# Install a Kit in Claude

This guide gets a [kit](glossary.md#kit) into Claude two ways. The first uses Claude.ai, the website, and needs no [command line](glossary.md#command-line). The second uses [Claude Code](glossary.md#claude-code), a program you type instructions into, and gives the full version. Step IDs start with NB (for "no black box"), then FR for free or FU for full.

Words in this guide are defined in the [glossary](glossary.md). A kit is a folder of instructions and tools for one job. A [skill](glossary.md#skill) is one instruction file inside a kit (the official term is "skill"). Claude loads a skill only when your request matches it, the way a cook pulls one recipe card out of a box.

## Way one: Claude.ai (free and low cost)

You need a Claude account. The Free plan is enough, and Pro is $20 a month billed monthly (checked 11/13/2026).

1. **NB-FR-01-1.** Go to claude.ai and sign in or create an account.
   You'll know it worked when you see the chat box. If you loop back to the sign-in page, try another browser and see E01 in the [shared fixes](getting-help.md#shared-fixes).
2. **NB-FR-01-2.** Open Settings, then Capabilities, and turn on code execution (a feature that lets Claude run small programs to make files for you).
   You'll know it worked when the switch is on. If you can't find it, see E02.
3. **NB-FR-01-3.** Download the kit's zip files from the kit's Releases page on GitHub. Each skill is one zip, and the zip's folder name matches the skill name.
   You'll know it worked when your Downloads folder holds one or more files ending in .zip. If the page has no files, the kit may not be released yet (E03).
4. **NB-FR-01-4.** In Claude.ai choose Customize, then Skills, then the plus sign, then Upload a skill. Pick one zip.
   You'll know it worked when the skill appears in your list with its switch on. If Claude says the file is invalid, the zip may have been unpacked and rezipped with an extra folder (E04).
5. **NB-FR-01-5.** Repeat step 4 for each zip in the kit.
   You'll know it worked when every skill in the kit's shopping list shows in your list.
6. **NB-FR-01-6.** Start a new chat and describe the job in your own words, for example "Help me track grant deadlines."
   You'll know it worked when Claude says it is using the skill. If it doesn't, name the skill in your request.

Anthropic describes the upload steps at support.claude.com/en/articles/12512180.

## Way two: Claude Code (full version)

Claude Code is Anthropic's program for working with files on your computer. Setup is in the Claude Code docs at docs.claude.com. It runs in a terminal (a window where you type commands instead of clicking). A plugin marketplace is a catalog Claude Code can install add-ons from, like an app store for one publisher.

1. **NB-FU-01-1.** Install Claude Code by following the current instructions on the Claude Code docs page, and sign in.
   You'll know it worked when typing `claude` in your terminal opens a chat [prompt](glossary.md#prompt). If the word is not recognized, see E05.
2. **NB-FU-01-2.** Add this repo's marketplace by typing the following, with the real owner name from the GitHub address in place of `<owner>`.
   ```
   /plugin marketplace add davidhluther/no-black-box
   ```
   You'll know it worked when Claude Code says the marketplace was added. If it can't find it, check the spelling of the address (E06).
3. **NB-FU-01-3.** Install the kit you want. Each kit is its own plugin (a bundle of skills).
   ```
   /plugin install grants@no-black-box
   ```
   Other kit names are `board-packet`, `books`, and `plain-writing`. The full list is in the [README](../README.md).
   You'll know it worked when the plugin shows in `/plugin` as installed.
4. **NB-FU-01-4.** Copy the kit's `config.example.json` to `config.json` and fill in your organization's details. Put names, folders, and your site address there and nowhere else.
   You'll know it worked when the file opens as valid text. If a check later says the file is invalid, see E07.
5. **NB-FU-01-5.** Run the kit's [check-up](glossary.md#check-up) command, `python3 support/doctor.py <kit-id>`, and read what it reports. The format of its code is in [support-code-format](../support/support-code-format.md).
   You'll know it worked when it prints "all basics passed" or a short list of what is missing.

Keys and sign-ups for paid or limited services are in [Keys and accounts](keys-and-accounts.md). Never paste a key into a chat or a shared file.

> **How to get help.** Write down the [step ID](glossary.md#step-id) where you got stuck (it looks like NB-FR-01-3). If your kit has a check-up button or command, run it and copy the [support code](glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

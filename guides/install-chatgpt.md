# Use a Kit in ChatGPT

ChatGPT reads the same [skill](glossary.md#skill) format as Claude, and OpenAI describes it in its own docs (learn.chatgpt.com/docs/build-skills). A skill is a folder with an instruction file named SKILL.md, and sometimes helper files. Which ChatGPT plans can upload one is not confirmed here, so this guide gives two routes and tells you how to pick.

Terms are defined in the [glossary](glossary.md).

## Route one: upload a skill

1. **NB-FR-02-1.** Go to chatgpt.com and sign in. A free account is fine for the free version of every [kit](glossary.md#kit).
   You'll know it worked when you see the message box. If you loop on sign-in, try another browser.
2. **NB-FR-02-2.** Look in the sidebar and in your profile menu for an item named Skills or Plugins.
   You'll know it worked when you find it. If you don't see either, your plan may not offer uploads yet, so use route two.
3. **NB-FR-02-3.** Download the skill's zip from the kit's Releases page on GitHub and upload it in that screen.
   You'll know it worked when the skill appears in your list. If ChatGPT rejects the file, use route two.
4. **NB-FR-02-4.** Start a new chat, turn the skill on if it asks, and describe your job in plain words.
   You'll know it worked when ChatGPT follows the kit's steps instead of improvising.

Whether ChatGPT can run a skill's bundled scripts is also not confirmed. Skills labeled "Claude Code (full version)" depend on scripts, so treat them as Claude-only for now.

## Route two: a Custom GPT or a Project

A [Custom GPT](glossary.md#custom-gpt) is your own saved version of ChatGPT with fixed instructions. A Project is a folder in ChatGPT that keeps instructions and files together for one job. Every kit has a chatgpt folder that serves both.

1. **NB-FR-02-5.** Open the kit's `chatgpt/instructions.md` on GitHub and copy all of it.
   You'll know it worked when you have the text on your clipboard (the place your computer holds what you copied).
2. **NB-FR-02-6.** In ChatGPT, create a Custom GPT (under Explore GPTs, then Create) or a new Project. Paste the text into the instructions box.
   You'll know it worked when the text fits. If the box says it is too long, check you copied only the one file (E08).
3. **NB-FR-02-7.** Open `chatgpt/knowledge-files.md`. It lists which kit files to upload as knowledge (reference files the AI model reads before answering). Upload exactly those.
   You'll know it worked when each file shows in the list without an error. A Custom GPT accepts up to 20 files, according to OpenAI.
4. **NB-FR-02-8.** Test it with the first [prompt](glossary.md#prompt) in the kit's `free/prompts.md`.
   You'll know it worked when the answer uses the kit's wording and structure.

Never put keys, passwords, donor lists, or client records into instructions or knowledge files. Anyone you share the GPT with can read them.

> **How to get help.** Write down the [step ID](glossary.md#step-id) where you got stuck (it looks like NB-FR-02-3). If your kit has a [check-up](glossary.md#check-up) button or command, run it and copy the [support code](glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

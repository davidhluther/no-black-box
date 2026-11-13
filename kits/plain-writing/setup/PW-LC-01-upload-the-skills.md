# PW-LC-01: Upload the Skills to Claude.ai or ChatGPT

You'll end with the plain-writing [skills](../glossary.md#skill) loaded into your paid AI plan, so the rules are there in every chat without pasting. It takes about 20 minutes.

A skill (a folder of instructions an [AI model](../glossary.md#ai-model) reads when a task matches, like a recipe card it pulls out) is uploaded as a zip file (one file that holds a whole folder). You need a paid plan with skills turned on. See the [shopping list](../shopping-list.md) for where to check the current plans.

1. **PW-LC-01-1.** On this kit's Releases page on GitHub, download the zip files for the skills you want. Start with `plain-writing.zip`. Add `evidence-review.zip`, `voice-presets.zip`, and `presentations.zip` later if you want them. Don't open or rename them.
   You'll know it worked when the files sit in your Downloads folder, each ending in `.zip`.
2. **PW-LC-01-2.** In Claude (claude.ai), click your name or the settings icon, then Settings. Look for a section called Skills, which may sit under Capabilities or Customize. Code execution must be on for skills to work.
   You'll know it worked when you see a list of skills with an [upload](../glossary.md#upload) button. If you can't find it, it's E01. Skip to guide `PW-LC-02` and use a [Project](../glossary.md#project).
3. **PW-LC-01-3.** Click the upload button and choose `plain-writing.zip`.
   You'll know it worked when "plain-writing" appears in the list. If it's rejected or has no name, it's E02.
4. **PW-LC-01-4.** Switch the skill on, then open a new chat and type: "Use the plain-writing skill. Review the draft below and list the rule each problem breaks." Paste [example-draft.md](../free/example-draft.md) under it.
   You'll know it worked when the reply cites rules by name (a banned word, a hollow opener, a recap ending) and doesn't just say the draft is fine.
5. **PW-LC-01-5.** Repeat steps 3 and 4 for any other zip you downloaded. For evidence-review, ask: "Use the evidence-review skill on this draft." For voice-presets, ask: "Write a 150-word post about volunteer reminders in the Quick Take voice."
   You'll know it worked when each skill appears in your list and the reply follows its method.
6. **PW-LC-01-6.** If you use ChatGPT, open Settings and look for Skills or a similar section. If your plan offers it, upload the same zip files the same way. This kit hasn't confirmed which ChatGPT plans accept skills or run the programs inside them. If you don't see it, use guide `PW-LC-02`.
   You'll know it worked when you either see your skills listed or know to use a Project instead. Either result is fine.

Programs bundled inside a skill (the [Python](../glossary.md#python) checkers) need a place to run. Claude with code execution on can run them. If yours can't, the skill still gives you the rules and the method, and the Google Docs word check in guide `PW-LC-03` covers the banned words.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like PW-LC-03-5). If you set up the Google Docs word check, run Help, then Run check-up, and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

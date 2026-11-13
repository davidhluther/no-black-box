# Glossary

Every technical term used in this kit, in plain words.

**Claude Code.** A program from Anthropic that you type to in a terminal. It reads your project's files, runs commands and edits things for you, and it is the tool this kit is built for.

**Skill.** A folder of instructions (and sometimes small programs) that teaches Claude Code one job, like a recipe card it pulls out when the job comes up.

**Plugin.** A bundle of skills that you install in one step, like an app that arrives with several tools inside.

**Marketplace.** A list of plugins that Claude Code can install from, like an app store with a single shelf.

**Terminal.** A window where you type commands instead of clicking. On a Mac it is the Terminal app, and on Windows it is PowerShell or a Linux window.

**Command.** One line you type in the terminal that tells the computer to do something.

**Repository.** A project folder whose history of changes is tracked, so you can see what changed and go back. People often say "repo" for short.

**Git.** The free program that tracks a repository's history. You do not need to learn it in depth to use this kit.

**Commit.** One saved snapshot of a repository, with a short note on what changed. Like pressing save and writing a label on the copy.

**Worktree.** A second working folder for the same repository, so two jobs can be open at once without stepping on each other.

**Pull request.** A proposed change that other people review before it joins the project, like handing in a draft before it goes in the book.

**Compaction.** What Claude Code does when a conversation gets too long. It replaces the earlier conversation with a shorter summary so the work can continue. Details can be lost in the summary.

**Context window.** The amount of text an AI model can hold in mind at one time, like the size of a desk. When the desk is full, something has to go.

**Capability ledger.** One file per project that lists what the project can do right now and what proves it, like an inventory sheet for abilities.

**Session brief.** A short file that holds a session's purpose, its settled decisions and its next step, so none of it depends on the chat.

**Handoff.** Passing unfinished work to a fresh session, with a brief that tells it everything it needs.

**Subagent.** A second Claude instance that Claude Code starts for a side job, with its own fresh view of the work.

**Scheduled job.** A script that runs by itself at set times, such as every Sunday at 10 p.m.

**Slot.** One scheduled run time of a scheduled job. "Sunday at 10 p.m." is a slot, and a job that skips it has missed the slot.

**Scheduler.** The part of your computer that starts scheduled jobs at their times. On Mac and Linux it is called cron.

**Outcome row.** One line in a log that says how a scheduled run ended (it worked, it found nothing, or it failed and why).

**Retry.** Running a failed job again.

**Design gate.** A check you run before proposing a change to a website. It looks at the finished page in a real browser and reports gaps, sideways scrolling and empty sections.

**Python.** A programming language. This kit includes a few small programs written in it, and you only need Python installed so they can run.

**Playwright.** A free program that opens a web browser and controls it, so a script can take screenshots of a page.

**Config file.** A small text file of settings, like the address of your site, so the programs do not need those details written into them.

**JSON.** A plain text format for settings and records, written as names and values inside braces.

**Step ID.** The code at the start of each numbered step, such as BT-FU-02-3. Give it to anyone helping you so they know exactly where you are.

**Support code.** A short code that the check-up command prints. It tells a helper which step failed and what the problem was.

**Environment variable.** A private setting stored on your computer outside your project files, so a secret like an address or a key never sits in a file you might share.

**Development server.** A copy of your website running on your own computer, so you can test changes before anyone else sees them.

**Chromium.** The free browser that Google Chrome is built on. Playwright uses it to load pages for the design gate.

**Webhook.** A web address that accepts a message from a program and posts it somewhere, such as a chat channel. Think of a mail slot for automatic messages.

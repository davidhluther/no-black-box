# Start Here with the Builder's Toolkit

This kit gives you five habits for working with AI, each packaged as a [skill](glossary.md#skill) that [Claude Code](glossary.md#claude-code) can run. They keep long projects honest. Claude Code checks a website's design before you ship it, keeps a list of what a project can really do, keeps a session's decisions from vanishing, and refuses to let a [scheduled job](glossary.md#scheduled-job) fail without someone hearing about it.

By the end you will have a project folder with a working capability file, a [session brief](glossary.md#session-brief) that survives long conversations, a design check that runs in a real browser, a map of every project on your computer, and a small runner that records every scheduled run and flags the ones that go missing. You can read the whole method here for free, and you can copy every file.

## The black box this opens

So much of how technology gets run is held in a black box. Part of that is real complexity. Part of it is that people benefit from selling the knowledge back to you. A hair salon or a small food bank should not have to pay someone to answer "how do I stop my AI from forgetting what I told it?" or "how do I know the nightly report actually ran?" These are the same questions a software team has. The answers are short, and they are in this kit.

## Who it is for

This kit is for people building with Claude Code: someone who runs a small website, a data job, or an automation and uses Claude Code to do the work. You will type a few [commands](glossary.md#command) in a [terminal](glossary.md#terminal). Each guide shows the exact line and what you should see.

It is Claude Code only, and only the full version exists. If you do not build with Claude Code, the other kits in this [repository](glossary.md#repository) are the better start. They have free versions that run on paste-in prompts and Google Sheets, and they need no terminal at all. [Choose your version](choose-your-version.md) explains why this kit has no free or low-cost edition.

## The five skills

| Skill | What it does for you |
|---|---|
| `capability-ledger` | A file that says what a project can do right now and what proves it, plus the rules for saying "that does not exist" without being wrong. |
| `session-brief` | A short file that holds a session's purpose and settled decisions, and the routine for [compaction](glossary.md#compaction) and [handoff](glossary.md#handoff), so long work does not lose its thread. |
| `scheduled-jobs` | The rule that every scheduled run writes down how it ended and a missed run counts as a failure, plus a small runner that retries and flags. |
| `design-gate` | A browser check that lays your changed pages out at phone and desktop widths and reports what a visitor would see. |
| `workstream-inventory` | A scan of every project folder on your computer, compared with your written routing notes, so nothing is forgotten. |

The [glossary](glossary.md) defines every term used in this kit.

## What you need

A computer with Claude Code installed, a paid Claude plan, and [Python](glossary.md#python). The [shopping list](shopping-list.md) has each item, its cost and what you can skip. Plan on about an hour for all five guides. You can stop after any guide, because each skill stands alone.

## Where to start

1. Read [choose your version](choose-your-version.md) (two minutes).
2. Gather what you need from the [shopping list](shopping-list.md).
3. Follow the guides in `setup/` in order, starting with `BT-FU-01`.
4. If something goes wrong, look up the code in [fixes](fixes.md).

## Want this set up for you?

Setup questions are free. Write down the [step ID](glossary.md#step-id) where you got stuck, such as BT-FU-02-3, and send it to Pigasus Group at https://pigasus.group/contact. If you would like David Luther to fit these habits to your own projects, that is a paid engagement that covers his time. It never buys information the kit withholds, because the kit withholds nothing. [What David built](what-david-built.md) explains where these skills came from.

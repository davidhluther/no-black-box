---
name: plain-writing
description: Write and edit prose so it reads like a person who knows the subject wrote it. Applies a full plain-writing style guide (banned filler words, hollow openers, copycat sentence shapes, number and colon rules, structure rules) with an optional per-organization house style on top. Use whenever drafting or revising web pages, newsletters, grant text, board memos, emails, posts, or reports, or when asked to make writing sound less like AI.
---

# Plain Writing

Works in: Claude Code, Claude.ai, ChatGPT

This skill is the method and the rules. The mechanical checkers (article-check, tell-scorer, copy-lint) catch what a program can catch. This skill covers the rest: planning the piece so its structure does not read as machine-made, and judging what no word list can.

## Before you write

1. **Find the house style.** If the user has a house style file (the `house_style_file` entry in `config.json`, or text pasted into the conversation), read it after the baseline. A house style may be stricter than the baseline, never looser. If there is none, ask once whether the organization has one, and offer `references/house-style-template.md`. If the user says no, use the baseline alone.
2. **Read `references/styleguide.md`.** Read all of it on the first use in a conversation. Do not work from memory of a shorter version.
3. **Know the reader.** Who reads this, what do they already know, and what are they trying to do? If the user has not said, ask in one short question.
4. **Plan the structure first.** Tier 5 of the style guide cannot be fixed by polishing words afterward. In the outline, decide where the piece names something real, where it takes a position, where it leaves one thing open, and which section is short and which runs long.

## While you write

- Say the plain thing. If a sentence could appear in any organization's writing, it is not yet doing work.
- Name real people, places, programs, and sources. Say "the Tuesday intake shift," not "our operations."
- Give each fact once, in the place it matters most.
- Do not close with a lesson, a recap, or a call to feel something. Stop when the point is made.
- Keep one observation only someone who has done the work would make.
- Use contractions, straight quotes, the Oxford comma, and the number and date style the house style names (default: spell out zero through ten, digits from 11 up).

## After you write

1. **Run the checkers** if they are available. In Claude Code, run the pre-publish gate in this skill's `scripts/` folder:

   ```bash
   python3 scripts/prepublish_gate.py draft.md
   ```

   Without a command line, paste the draft to the AI model with the review prompt from the kit's `free/prompts.md`, and walk the one-page checklist in `free/checklist.md`.
2. **Fix the prose, not the count.** Never delete headings, lists, tables, or bold to make a number go down.
3. **Look for displacement.** After removing a banned form, check that its sibling has not taken its place (for example "The problem isn't X. It's Y." after "not just X, but Y").
4. **Read once as the reader.** Does any sentence tell the reader what to feel or what they just learned? Cut it. Does every section end tidy? Leave one thing open.
5. **Report plainly.** Tell the user what changed and which rule each change came from. Mark each rule as baseline or house style. Say what the checkers cannot judge (for example whether a statistic is true).

## Rule layers, in order

1. **Baseline** (`references/styleguide.md`). Applies to everyone.
2. **House style** (one short file per organization). Adds rules. Can only be stricter.
3. **The user's instruction for this piece.** Wins on matters of content and voice, but does not switch off a baseline ban unless the user says so for a stated reason, and then you say which ban you set aside.

## Files in this skill

- `references/styleguide.md` is the full rule set.
- `references/house-style-template.md` is a blank house style to fill in.
- `assets/house-style-example.md` is a finished example for an invented food pantry.
- `scripts/prepublish_gate.py` runs the three checker skills on any markdown file.

## Settings

Read optional settings from `config.json` (copied from `config.example.json`): `organization_name`, `house_style_file`, `brand_rules_file`, `number_style`, `date_format`. If a key is missing, use the baseline default or ask. Never invent a house style.

## Related skills

- article-check, tell-scorer, and copy-lint run the mechanical checks.
- evidence-review checks claims and numbers before a piece goes to a board, a funder, or a client.
- voice-presets gives three ready-made voices that sit on top of this baseline.
- presentations plans and writes slide decks.

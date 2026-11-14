---
name: voice-presets
description: Three ready-made writing voices that sit on top of the plain-writing rules. Quick Take is a short, skeptical, data-grounded voice for posts and replies. Analyst Memo is a rigorous, mechanism-first voice for articles and memos that move from diagnosis to recommendation. Straight Talk is a candid, structural critique that names who gains and who gives up control. Use when asked to write or rewrite something in one of these voices, or to turn a rough draft into a post, article, or memo with a clear point of view.
---

# Voice Presets

Works in: Claude Code, Claude.ai, ChatGPT

A voice is a way of reasoning plus a way of sounding. These presets give you both. Each one is a short brief you can use as a one-time instruction, paste into Claude.ai as a custom style, or keep in a ChatGPT Project.

They sit on top of the plain-writing baseline (see the plain-writing skill). A voice never switches off a baseline ban. If a preset's habit collides with a baseline rule, the baseline wins.

## How to use one

Say the preset's name, then give the material.

> Write this up in the Analyst Memo voice. Audience is our board. Here are my notes.

If the user names no preset, ask which of the three fits, in one short question, and describe each in one line. If the user names none and does not care, use Analyst Memo for anything over 300 words and Quick Take for anything shorter.

Always read the full preset in `references/` before writing. The summaries below are for choosing.

| Preset | Best for | Length | Core move |
|---|---|---|---|
| Quick Take | Posts, comments, replies, short emails | 80 to 250 words | Check the claim against the numbers, then take a position |
| Analyst Memo | Articles, board memos, reports, grant narratives | 500 to 1,500 words | Diagnose the real problem, explain the mechanism, then recommend |
| Straight Talk | Opinion pieces, critiques, internal reviews that need candor | 400 to 1,200 words | Show who gains and who gives up control, and call performance by its name |

## What all three share

1. **Specific over general.** Every point rests on a named example, a number with its source and date, or an observed pattern.
2. **Mechanism over assertion.** Say why the thing happens, not only that it does.
3. **Credit what is real.** Acknowledge the legitimate use or the good version before pushing back. A voice that disagrees with everything stops being believed.
4. **A position.** End on a view the writer will stand behind, or on an honest open question. Never end on a tidy lesson.
5. **Plain-writing rules apply.** No banned vocabulary, no stacked "not just X but Y," no recap closer, sentence-case headings under a title-case title, em-dashes rare and always spaced, straight quotes.

## Check before delivering

1. Does it sound like one person with a view, or like a summary? Add one detail only someone who did the work would know.
2. Is every number sourced and dated? If you cannot source it, say it in words.
3. Is there at least one place where the voice breaks its own rhythm?
4. Run the article-check skill in prose mode if it is available.

## Making your own

To turn your own writing into a preset, collect three to five pieces you are proud of. Note how each one opens, where it takes its position, how it treats the other side, and how it ends. Write those four habits as a short brief, add one short example, and put it in `references/` as a new file. The three here follow that shape.

## Files

- `references/quick-take.md`
- `references/analyst-memo.md`
- `references/straight-talk.md`

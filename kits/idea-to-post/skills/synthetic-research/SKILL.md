---
name: synthetic-research
description: Pre-test post angles, messages, or concepts with AI-simulated readers before spending on real research, using a method that asks for a free-text reaction and maps it to a rating scale instead of asking a model for a number. Use when someone asks about synthetic respondents, simulated surveys, AI personas, concept or message testing, or wants to calibrate an AI judge onto a rating scale. Includes the validation gate that decides whether any result can be trusted.
---

# Synthetic research

Works in: Claude Code, Claude.ai, ChatGPT for the brainstorming use. The full scoring method needs a script and an embeddings service, so it is Claude Code (full version) only.

## What it is, in plain words

A way to simulate survey respondents with AI models so you get a realistic spread of answers rather than the clumped, skewed output you get when you ask a model "rate this from one to five." The idea comes from a published study (Maier and colleagues at PyMC Labs and Colgate-Palmolive, arXiv 2510.08338, 2025). Read [references/method.md](references/method.md) before quoting any figure from it.

## The core move

Never ask the model for a number. Ask a model playing a described reader for a free-text reaction. Convert that text into a position on the scale by comparing it with anchor statements written for each point on the scale ("I would definitely not do this" through "I would definitely do this"). Normalize the result into a probability spread across the scale.

The same pattern fixes any place a pipeline asks an AI model for a single score (relevance, intent, quality). Elicit text, then project it onto a calibrated scale.

## The hard gate

**No validation data, no claims.** The published accuracy exists because the authors had thousands of real survey responses to check against. A simulated panel with nothing real to compare to is an opinion generator that cannot be proven wrong. Before treating results as research, confirm you have, or can get, at least one past study with respondent-level human data (each person's rating and comment). If you cannot, there are two honest options: run a small real study first and use it to calibrate, or call the exercise brainstorming and say so everywhere the results appear.

For a small organization the usual answer is the second one. Use pretend readers to generate objections and angles, then check the top two or three with five real people.

## Workflow

| Phase | What happens |
|---|---|
| 1. Intake | Gather past survey rows, scale wording, and comments. See [references/data-request.md](references/data-request.md). |
| 2. Calibrate | Write anchor statements to match your real question wording. Tune them; wording moves results. |
| 3. Replicate | Rebuild one past study with simulated readers. Compare ranking order and the spread of answers. Check both, always. |
| 4. Report | State how close you got, or state that no benchmark exists. |
| 5. Use | Only after phase 3, and only as a pre-screen. |

### Why both checks matter

Direct rating can get the order of concepts roughly right while producing a spread nothing like human answers. If you only report that the order matched, you have repeated the failure the method exists to avoid.

### Reporting honestly

Agreement means little without a ceiling, meaning how closely real people agree with themselves when asked twice. If you have no repeat-measure data, say so and report the raw match with that caveat. Never invent the denominator.

## Brainstorming mode (free versions)

1. Describe five to eight readers in a line or two each, based on real people you serve (role, situation, what they worry about, what they have tried).
2. Show each the post idea, message, or title. Ask for a two or three sentence reaction in their own words and what they would still want to know.
3. Collect objections that came up more than once.
4. Label the output "brainstorm, not research" and list it in the brief that way.

## Where it is useful and where it is not

Good for ranking many candidates quickly (twenty titles down to three) and mining reactions for objections. Poor for forecasting. The published validation was in consumer products, where AI models have read endless discussion. Thin categories, local and specialized topics, and decisions made by committees are untested. Say that to anyone who wants more from it.

## Writing outputs

Follow your style guide (`draft.style_guide_file`) for anything a reader sees.

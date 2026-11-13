---
name: synthetic-research
description: Use AI models as simulated survey respondents to pre-screen wording, concepts, or messages before spending on real research, and state honestly how far the results can be trusted. Simulated respondents catch confusing or off-target wording, and they never replace real customers. Use when someone proposes AI personas, a "synthetic panel," concept or message testing with AI, or when judging whether an AI-generated "survey result" can be believed. Covers a simple free method, a more rigorous method, and the validation needed before any numbers are claimed.
---

# Synthetic Research

Works in: Claude Code, Claude.ai, ChatGPT

## What this is, and what it is not

Synthetic research means asking AI models to answer as if they were customers or survey respondents. It is useful for one job. It narrows a long list of wordings, names, or ideas down to a few worth showing real people. It is not a survey. It cannot tell you how many people will respond, what they will pay, or whether a message will work.

Say this plainly to anyone who will use the results. The people in the simulated panel do not exist. Their answers are guesses assembled from text on the internet, so they reflect the most common ways people write about a topic, and they can sound sure and be wrong.

## Validity limits (state these whenever results are shown)

1. No ground truth. A simulated panel with nothing real to check against is an opinion generator that cannot be proven wrong. Published accuracy figures exist only because the authors had thousands of real answers to compare with.
2. Tested only on consumer products. The best-known study covered personal-care product concepts, a topic AI models have read a huge amount about. It has not been shown for small local nonprofits, local services, or business-to-business decisions, which involve committees, budgets, and existing contracts that a simulated respondent does not model.
3. Demographic fidelity is uneven. In that study, age and income were reproduced better than gender and region. Persona details matter, and invented details mislead.
4. Missing context. Budget limits, competing choices, advertising, and trust built over years are absent.
5. Agreeableness. Simulated respondents lean positive and agree with one another. Unanimous approval is a warning sign.
6. Hallucination. In unfamiliar areas the model fills gaps with plausible fiction. Mark every unsupported detail as a GUESS.
7. People who rarely post online are underrepresented in the text these models learned from, and in your own sources too.

Never write "customers prefer," "will convert," or "tested well." Write "a simulated panel found version A clearer, to be checked with real customers."

## The simple method (use this by default)

1. **Start from real quotes.** Build persona cards from collected customer quotes (see persona-jury's `reference/persona-cards.md`). Without evidence, stop and collect first.
2. **Ask for reactions, not numbers.** For each persona and each version, ask for a two-to-three sentence reaction in the persona's voice: what they understand, what they would do next, and what confuses or bothers them. Do not ask for a score. Models asked for a number give narrow, clustered answers that look nothing like real people's.
3. **Make it skeptical.** Tell the persona they are busy, a little tired, and not looking to be sold. This counters agreeableness.
4. **Collect the useful parts.** Which version each persona understands fastest, the exact words that caused confusion, every guess marked GUESS, whether the personas agree, and three questions for real customers.
5. **Take the finalists to real people.** Show two versions to at least five real customers or neighbors, in random order, and ask the questions from step 4. If real answers disagree with the panel, the real answers win.
6. **Record the result** with the date, the cards used, and what real customers said.

## The rigorous method (only with real data to check against)

For people who need numbers on a scale, such as purchase intent. This is the "semantic similarity rating" method (see `references/method-notes.md` for the source and details). Do not use it without the gate below.

1. Elicit free text from a persona-conditioned model, never a number.
2. Convert each reply into an embedding (a list of numbers that captures meaning, so similar sentences get similar lists).
3. Compare each embedding with hand-written anchor statements, one for each point on the scale, such as "I would definitely not do this" through "I would definitely do this."
4. Turn the similarity into a probability for each scale point and average across several sets of anchors.

**The hard gate: no validation data, no claims.** Before using this method for anything beyond idea generation, the organization must have at least one real study with respondent-level answers (each person's rating and written comment, not a summary slide). Rebuild that study with the simulated panel, then compare both rank order (do the same ideas come out on top?) and the shape of the distribution (do the spread of answers look human?). Report both. A method that gets the order right but a distribution wrong is exactly the trap the method exists to avoid. If the organization has no real data, either run a small real study first to serve as the check, or stay with the simple method above and present results as qualitative.

## Writing results for others

State the date, the number of personas, which evidence the cards came from, the limits above, and the real-customer follow-up. Use plain language. A funder, board, or coworker reading your result must be able to tell at a glance that it is a pre-screen.

---
name: aeo-audit
description: Run the whole AI visibility review for one business in order ([noise audit](../../glossary.md#noise-audit), then visibility, mentions, [citations](../../glossary.md#citation), competitive, platforms, trends) and write one short summary. Use for a monthly review or when someone asks for the full picture of how [AI models](../../glossary.md#ai-model) treat the business. Chains the other skills in this kit; it does no counting itself.
---

# AEO audit (the full chain)

Works in: Claude Code (full version) for chaining the skills. In Claude.ai or ChatGPT, run each skill yourself in the order below and paste the outputs together. AEO means answer engine optimization, the habit of making your business easy for AI answers to find and describe.

## What this does

It answers one question: where does this business stand in AI answers right now? It chains the other skills, checks that each one ran, and writes a one-page summary. It does not read answer files and compute numbers itself. If you catch yourself counting mentions in this skill, stop and run `aeo-visibility`.

## Before starting

1. Find the latest run folder under `runs/` and confirm it has a scored file and answer files. If there is no corpus, write a short note saying how to get one (run `battery-preflight`, freeze the questions, collect a run, then return) and stop. Never collect answers on someone's behalf from their personal accounts.
2. Check for a [preflight](../../glossary.md#preflight) sign-off from `battery-preflight`. If missing, say so at the top: every number is "not preflighted".
3. Hand-run (app) runs and [API](../../glossary.md#api) runs are separate instruments. Audit one at a time. Never merge them.

## The chain

Run each skill fully, one after another, saving each result under `analysis/<run>/`:

1. `answer-noise-audit` (everything after it uses its clean numbers)
2. `aeo-visibility`
3. `aeo-mentions`
4. `aeo-citations`
5. `aeo-competitive`
6. `aeo-platforms`
7. `aeo-trends`

If a skill reports "skipped" or "degraded", carry that status into the summary. It does not stop the chain. If one fails outright, stop, name which results exist, and write the summary as incomplete.

## Check before summarizing

- Every result exists and says which run and which [question set](../../glossary.md#question-set) version it covers. The versions must match.
- Every number in the summary can be traced to a named result file.
- Raw figures never appear as headlines. If the noise audit is missing, say "unverified" next to every number.

## Output

`analysis/<run>/summary.md` (300 to 600 words): one paragraph on where the business stands, up to five issues in order of seriousness (each with confidence and the result file behind it), a short "what to try next" paragraph written as hypotheses to test rather than promises, and one line on what the data cannot tell you. State plainly if this is the first run: a first run is a [baseline](../../glossary.md#baseline), and a baseline has no trend.

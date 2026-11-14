---
name: question-battery
description: Build, freeze, and run a fixed set of 28 customer-style questions against AI models (ChatGPT, Claude, Gemini, Perplexity), then log whether your business is named, cited as a source, or [crowded out](../../glossary.md#crowded-out). Covers the hand-run method (free) and an automated runner that uses your own [API](../../glossary.md#api) keys. Use when starting AI visibility tracking, running the monthly check, adding a new business to track, or when someone asks "do AI models recommend us?"
---

# Question battery

Works in: Claude Code (full version) for the automated runner. The hand-run method and the question template work in Claude Code, Claude.ai, and ChatGPT.

## The idea

Customers now ask AI models "who should I go to for X near me?" before they search. A question battery (a fixed list of those questions, asked the same way every month) tells you whether a model names you, links to your website, or names someone else instead. It is a thermometer, not a ranking: it only works if the questions never change.

## Three rules that make the numbers honest

1. **Freeze the questions.** Once a run happens, never edit a question, not even to fix a typo. If one is broken, retire it (strike it out, write the date and reason) and add a new one with a new code. Compare only runs that used the same [question set](../../glossary.md#question-set) version.
2. **Never hand over the answer.** No question outside the brand-check group (BV) may contain your business name or your name. A name you hand over voids that cell.
3. **Hand-run and API runs are different instruments.** Questions typed into the apps (ChatGPT, Claude, Gemini, Perplexity) show what a customer sees. Questions sent through a developer API (a way for one program to ask another for an answer) skip the apps' own instructions, memory, and location handling. File them separately, tag them "-api", and never compare one with the other.

## Before you run anything

Run the `battery-preflight` skill first. It finds other businesses and words that share your name, so the scoring can tell them apart from you.

## Step 1: Build the question set

Copy `references/questions-template.md` (28 questions in six groups, with placeholders). Fill your details into `config.json` (copy `config.example.json` from the kit) and run:

```
python3 scripts/fill_questions.py --config config.json
```

It fills the placeholders, then checks that no non-brand question names you and that nothing is left in curly brackets. Read all 28 aloud. If one does not sound like something a customer would type or say, reword it now, before freezing. Then freeze:

```
python3 scripts/fill_questions.py --config config.json --freeze
```

Without Claude Code, fill the template by hand in the Google Sheet from the free version.

## Step 2: Run it by hand (the instrument of record)

- Use the free consumer apps, a fresh chat for every question, one question per chat, no follow-ups.
- Stay signed out where the product allows it. Where an account is needed, use a clean browser profile with memory and custom instructions turned off.
- Run from your real location on your normal connection, without a VPN (a service that hides where you connect from). Many models guess your location from your connection, and local questions depend on it.
- Paste each question exactly as written. Copy the whole answer and paste it unedited under the question code in `runs/<run>/answers/<product>.md`.
- Never argue with the model and never name your business in the thread.
- Write the run header first: date, who ran it, the model name each app shows, signed in or out, location, questions skipped and why.

## Step 3 (optional): Run it through the APIs

Needs your own keys, set as environment variables (settings stored outside any file, so they never end up in a shared folder): OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, PERPLEXITY_API_KEY. Put model names in `config.json` under `api_models`.

```
python3 scripts/run_api_battery.py --config config.json --dry-run
python3 scripts/run_api_battery.py --config config.json --providers anthropic --yes
```

The [dry run](../../glossary.md#dry-run) checks keys, model names, and the question count, and sends nothing. A real run asks every question once per provider with [web search](../../glossary.md#web-search) on, pauses between calls, and writes `runs/<run>-api/answers/<provider>-api.md`, a `.jsonl` file with the sources and searches each model reported, and `scored-draft.csv`. Every number in that draft is a guess by a simple [script](../../glossary.md#script). Read each answer and correct the row.

`python3 scripts/run_api_battery.py --self-test` checks the answer parsers against the response shapes in the vendors' documentation. It makes no live calls. The first real run per provider is the real test; if a provider errors, check its current documentation, because request shapes and model names change.

## Step 4: Score

Score every cell with these columns (they match the Results tab in the Google Sheet): answer_status (ok, not_run, refused, failed), named (y, n, [same-name](../../glossary.md#same-name)), position (1, 2, 3+, list, aside, or -), your_site_cited (y, n, none_given), cited_domains, others_named, resolved_to (person_local, person_remote, software, generic_advice, nobody).

- A failed or skipped cell is a gap in coverage. Never score it as "not named".
- A same-name business or a word sense that is not you is `same-name`, never `y`.
- Quote the answer line that justifies any `y`.

## Reading the results

Report counts with their denominators ("named in 6 of 80 cells"), not percentages of small numbers. Brand-check and [control questions](../../glossary.md#control-question) stay out of the headline. A zero is a result, and for a small or new business it is the normal first month. Hand the scored file to `answer-noise-audit`, then `aeo-audit`.

## Limits worth stating

- Small numbers. Twenty headline questions across four products is eighty cells. One month's movement of a cell or two is within normal answer-to-answer variation.
- Models change under you. A quiet model swap can move scores without your business changing, so record the model name every run.
- This tool does not drive the consumer apps by browser automation, because that breaks their terms of service and puts accounts at risk. The method here is hand collection, or official APIs on your own accounts.

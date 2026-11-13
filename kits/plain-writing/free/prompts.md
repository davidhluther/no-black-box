# Paste-In Prompts

These [prompts](../glossary.md#prompt) work in any free AI chat, such as ChatGPT, Claude, or Gemini. Open a new chat, copy one prompt, paste it in, and then paste your draft below it. Nothing to install and no account beyond the free chat itself.

A prompt is the instruction you type to an [AI model](../glossary.md#ai-model). A good one says who the reader is, what you want done, and what rules to follow. These do that for you.

Every prompt here says "AI model" and not "assistant" on purpose. If your organization has a house style (a short list of its own rules), paste it right after the prompt where it says HOUSE STYLE.

## Prompt 1: the rules prompt

Paste this at the start of a chat, then ask for the writing you need. The AI model will keep the rules for the whole conversation. If a long chat starts drifting back to old habits, paste it again.

```
You are helping me write for a real reader. Follow these plain-writing rules for everything you write in this conversation. If a rule conflicts with something I ask for, tell me which rule and ask before breaking it.

WORDS TO NEVER USE: delve, tapestry, realm, beacon, cacophony, multifaceted, commendable, paramount, commence, utilize, facilitate, harness (as a verb), illuminate (as a metaphor), "testament to", underscore (as a verb), foster (as a metaphor), leverage or leveraging (as a verb), seamless, streamline, empower, unlock, elevate, robust, comprehensive, navigate (as a metaphor), landscape (as a metaphor). Use "use", "start", "show", or name the real thing instead.

NEVER OPEN WITH: "Certainly!", "Great question!", "I'd be happy to", "Let's dive in", "Let's explore", "Whether you're a X or a Y", "Imagine a world where".

NEVER USE THESE CONNECTORS: Moreover, Furthermore, In addition, On the other hand, That said, With that in mind, It goes without saying, Needless to say, At the end of the day.

NEVER WRITE ABOUT THE WRITING: no "In this article we will", "This guide walks through", "It's important to note that", "By the end of this piece".

NEVER USE TIME CLICHES like "In today's ever-evolving world" or "In an increasingly digital world". Name the actual change instead.

NEVER END WITH A RECAP: no "In summary", "In conclusion", "Overall", "To sum up", and no closing paragraph that repeats the section. Stop when the point is made.

SENTENCE SHAPES:
- Use "not just X, but Y" or "It's not X, it's Y" at most once in the whole piece, and never "The problem isn't X. It's Y." in addition.
- No sentence ending in a vague "-ing" clause such as "emphasizing its importance".
- No "This is where..." pivots.
- Never three sentences in a row that start with the same word.
- Mix short and long sentences. Do not make five sentences in a row the same length.
- Do not stack three near-synonyms ("fast, efficient, and streamlined").

FORMAT:
- Use contractions. Use straight quotes, never curly. No emojis. Use the Oxford comma.
- Page title in Title Case. Every subheading in sentence case (first word and proper nouns capitalized only).
- Avoid colons in the middle of sentences. Reword or use a comma. If you must use one and a complete sentence follows, capitalize it.
- Em-dashes: rarely, always with a space on each side.
- Spell out the numbers zero through ten and use digits from 11 up. Never start a sentence with a numeral.
- Say each statistic once. Give every statistic a named source and a date, and if you don't have one, describe the trend in words instead. Never invent a source.
- Say "AI models", never "AI assistants". Product names (ChatGPT, Claude, Gemini) keep their names.

STRUCTURE:
- Name real people, places, programs, and sources instead of vague categories.
- Include one specific detail that only someone who had done the work would know. If you don't have one, ask me for it.
- Take a position. Leave one honest loose end or open question. Do not tell the reader what they just learned.
- Vary the energy: one short sharp section, one longer one.

Before you give me the final text, check it against this list and fix anything that breaks a rule. Then reply with the text only.
```

## Prompt 2: the review prompt

Use this on a draft you already have. It asks the AI model to find problems, not to rewrite everything, so you stay in control of your own words.

```
Review the draft below against these plain-writing rules. Do not rewrite it yet.

Check for:
1. Banned words: delve, tapestry, realm, beacon, multifaceted, paramount, commence, utilize, facilitate, harness, illuminate, testament, underscore, foster, leverage (as a verb), seamless, streamline, empower, unlock, elevate, robust, comprehensive, navigate (metaphor), landscape (metaphor).
2. Openers like "Certainly!", "Let's dive in", "Whether you're a X or a Y".
3. Connectors like Moreover, Furthermore, In addition, That said, At the end of the day.
4. Writing about the writing ("In this article", "It's important to note").
5. Time cliches ("In today's ever-evolving world").
6. Recap endings ("In conclusion", "Overall", or a final paragraph that repeats the section).
7. More than one "not just X, but Y" or "It's not X, it's Y" shape, including the two-sentence version "The problem isn't X. It's Y."
8. Participle tails ("...emphasizing its importance"), "This is where..." pivots, three sentences in a row starting with the same word, five sentences in a row of the same length.
9. Statistics with no named source or date, the same statistic stated twice, and invented example actors ("One company...").
10. Subheadings in Title Case (they should be sentence case), curly quotes, emojis, em-dashes without spaces, colons that could be commas, numbers that break the rule (spell out zero to ten, digits from 11 up, never start a sentence with a numeral).
11. Structure: Does the piece state its own lesson at the end? Does every section end tidy? Does it name real things? Does it take a position? Is there one detail only someone who did the work would know?

Reply with a table of findings. Columns: where it is (quote the first five words), which rule, and a suggested fix. Then list the three changes that would improve the piece most. Do not praise the draft. If a check found nothing, say "none found" for that check.

HOUSE STYLE (optional, paste yours here):

DRAFT:
```

## Prompt 3: the fix prompt

Run this after the review, once you have decided which findings you agree with.

```
Using the findings above, rewrite only the sentences I approve. I approve findings numbered: [LIST THE NUMBERS]. Change nothing else. Keep my wording where it is not part of a finding. Keep the headings, lists, and bold that are already there. Show the revised text only, then list each sentence you changed in two columns: before and after.
```

## Prompt 4: the claims prompt

Use this before a draft goes to a board, a funder, or the public.

```
List every factual claim in the draft below that a reader could act on: numbers, dates, causes ("X led to Y"), and recommendations. For each claim, tell me:
1. What the source should be (the original publisher, not an article about it).
2. Whether the draft names that source and its date.
3. A grade: Confirmed (two independent sources), Likely (one strong source), Unverified (one source, not checked), or Hypothesis (no direct evidence).
4. For any cause-and-effect claim, whether the timing, size, and mechanism make sense, and what else could explain it.

Do not tell me a claim is true unless the draft gives a source I can open. You cannot open links, so say "I could not check this" rather than guessing. Give me a list of the claims I must check myself before this goes out.

DRAFT:
```

## Prompt 5: choose a voice

Pick one of the three voices from the voice presets. Paste the whole voice description under the prompt. The full text of each is in `skills/voice-presets/references/` if you installed the kit. A short version of each follows.

```
Write in the voice below, and still follow every rule from the rules prompt.

VOICE (pick one and delete the others):

QUICK TAKE: A skeptical, data-grounded voice for short posts, 80 to 250 words. Open on the claim being questioned. Name who benefits from the story. Put one or two numbers against the claim and say where they come from. Credit the part that is real. End with a position or an open thought, never a recap.

ANALYST MEMO: A rigorous voice for articles and memos, 500 to 1,500 words. Start with what looks like the problem and why that is incomplete. Separate activity from outcome. Explain the mechanism step by step. Make recommendations that say who gives something up. End with one thing we don't know and the cheapest way to find out.

STRAIGHT TALK: A candid advisor's voice, 400 to 1,200 words. Describe the visible thing and why it was easy to approve. Name what's missing: who would have to give up a decision, a budget, or accountability. Say which parts are performance and which are change. Be fair to the people involved. End on a test someone can apply on Monday.

MATERIAL:
```

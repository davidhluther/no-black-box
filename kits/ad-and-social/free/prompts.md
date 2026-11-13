# Paste-In Prompts

Copy a prompt into any chat AI model (ChatGPT, Claude or Gemini). Replace everything in [square brackets]. Start a new chat for each prompt and paste your [voice sheet](../glossary.md#voice-sheet) first, as the prompt says.

Platform rules change. Wherever a prompt says "limits," you give the model the numbers you see in the platform's own ad screen today. The model should never supply them from memory.

## Prompt 1. Build your voice sheet

```
I run [organization name], a [what we are, in plain words]. Our audience is [who we serve or sell to].
Ask me one question at a time, up to ten, to learn how we sound. Cover: what we offer, who it's for,
words we love, words we never use, three sentences we've written that we're proud of, and what we
must never claim (prices, results, guarantees, medical or legal promises).
Then write a one-page voice sheet with these headings: Who we are, Who we speak to, How we sound,
Words to use, Words to avoid, Offers we can describe, Claims we can prove (with the proof), Claims we must never make.
Keep it plain. Do not invent facts. Mark anything I didn't tell you as "ask the owner."
```

Paste the result into the Voice tab of your Google Sheet.

## Prompt 2. Search ad text

```
[Paste your voice sheet.]

Write search ad text for this offer: [offer, one sentence]. Landing page: [web address].
Audience: [who]. Goal: [calls / sign-ups / visits].

Platform limits, as shown in the ad screen today: headline [number] characters, description [number]
characters, up to [number] headlines and [number] descriptions. Count every character, including spaces.
If a line is over, shorten it. Do not exceed the limits.

Give me:
1. Headlines, grouped by angle (benefit, proof, offer, question). Show the character count after each.
2. Descriptions, with counts.
3. A claims list. For each claim you made, say "from my voice sheet" or "not from my voice sheet."
   Remove any claim that isn't from my voice sheet and tell me what proof I'd need to add it.
No superlatives like "best" or "#1," no guarantees, and no invented numbers.
```

## Prompt 3. Social ad text with test versions

```
[Paste your voice sheet.]

Write ad text for [Facebook and Instagram / X] for this offer: [offer]. Audience: [who].
Fields to fill, with lengths from the ad screen today: primary text [number], headline [number],
description [number], button [options shown].

Make three versions that differ in exactly one thing each:
- Version A, the plain control.
- Version B, same words, but the opening line leads with a different angle: [angle].
- Version C, same as A, but a different call to action: [call to action].
For each, say in one line which single thing changed. Then list every claim and mark it
"from my voice sheet" or "not from my voice sheet." Drop any claim without proof.
```

## Prompt 4. One idea, three platforms

```
[Paste your voice sheet.]

The one idea: [a single sentence]. Detail I can use: [dates, place, who, how to join].
Write one post each for X, Facebook and Instagram. Each must stand on its own and must not just
shorten the others. Adapt:
- X: short and direct, one point, link only if needed. Tell me the length so I can check it in the X composer.
- Facebook: warm and local, a little longer, plain link.
- Instagram: the first line has to carry the idea; the caption works without a link; leave a line "[hashtags]" for me to fill.
Also write alt text (one plain sentence describing the picture) for this picture: [describe the picture].
List the claims you made and where each came from. Do not invent hashtags, numbers or quotes.
```

For LinkedIn, ask the same question in plain words ("Write a LinkedIn post from this idea, a stand-alone note from a person at our organization, first two lines carrying the point, link in the first comment"). The Idea to Live Post kit has a fuller LinkedIn method, and this kit's [social-posts skill](../skills/social-posts/SKILL.md) describes the same pattern.

## Prompt 5. Claims check

```
Here is a draft [ad or post]. Read it like a skeptical customer and a platform reviewer.
List every statement that is a fact, a number, a promise or a comparison. For each, say whether it can
be proven by the documents I'm about to paste, is an opinion, or has no support. Suggest an honest rewrite
for anything unsupported. Flag any word that sounds like a guarantee, a medical or financial promise, or a
claim to be the best.
[Paste the draft, then your proof documents.]
```

## Prompt 6. Picture idea for Canva

```
[Paste your voice sheet.]
We need a picture for [ad / post]. Platform and shape: [for example Facebook feed, vertical 4:5].
Message in one sentence: [message]. Write three picture ideas I can build in Canva with free templates:
one photo-style, one simple illustration, one text-on-color. For each, give the Canva search words,
the layout in plain terms, which of my brand colors to use, and alt text. No logos of other companies,
no fake testimonials, and no people who look like real named individuals.
```

## Prompt 7. Designer brief

Use [designer-brief-template.md](designer-brief-template.md). To have the AI model fill it in, paste the template and the line "Fill this in for the following campaign. Leave any field you can't answer from what I tell you as 'ask the owner.'" Then describe the campaign.

---
name: ad-copy
description: Write search ad text (headlines and descriptions) and social ad text (primary text, headline, description, button) for a small organization, with several test versions that each change one thing, platform limits used only when checked on the platform's own page, and every claim traced to proof. Use when someone asks for ad copy, Google search ads, Facebook or Instagram ad text, X ad text, ad variants to test, or a check that an ad doesn't overpromise. It drafts only; it never publishes or spends money.
---

# Ad copy

Works in: Claude Code, Claude.ai, ChatGPT.

You write the words. You never publish, sign in to an ad account or spend money. The person pastes your text into the platform's own ad screen.

## Before drafting anything

1. Get the organization's details. In Claude Code, read `config.json` (copied from `config.example.json`). Elsewhere, ask for the voice sheet (who we are, who we speak to, how we sound, words to use and avoid, offers we can describe, claims we can prove with the proof, claims we must never make). If there's no voice sheet, ask up to five short questions, one at a time, and write a draft sheet for the person to correct.
2. Ask for the offer in one sentence, the landing page address, the audience, and the goal (calls, sign-ups, visits, purchases). Ask where the ad will run and which ad type.
3. Get today's limits from the person. Ask them to open the ad screen for that ad type and read the character limits shown, or paste them. Never fill limits from memory. If they can't, use only the figures in `references/platform-limits.md` that carry a "checked" date, say that the date is old if it is, and tell them to confirm in the ad screen. For any platform not in that file, give them the link and ask for the number.

## Claims come first

Build a claims ledger before you write a headline. Each row has the statement, its source ("voice sheet", a document the person gave you, or a public page), and a status.

- **Proven.** The person gave you proof. You may use it.
- **Opinion.** Plain description of how the organization feels or works ("we take our time with every client"). Allowed when it isn't a comparison or a promise.
- **Unsupported.** No proof. Do not use. Tell the person what proof would let you use it.

Never write superlatives ("best," "#1," "top-rated"), guarantees, invented numbers, invented reviews or quotes, medical, legal or financial promises, urgency that isn't real ("only three left") or a comparison to a named competitor. If the offer touches a regulated area (health, money and credit, housing, jobs, politics, alcohol, gambling, children), say so, link the platform's policy from `references/platform-limits.md`, and keep the copy plain and cautious.

## Search ads

For a responsive search ad (Google mixes your headlines and descriptions, so every line must read well next to any other), write:

- Headlines in angle groups (what you offer, who it's for, proof, the offer or deadline, a question). Vary them. Don't repeat the same phrase, and put the main search words in a few of them.
- Descriptions that add something the headlines don't (the next step, the place, the proof).
- Display path words if the platform asks.

Show the character count after every line. Count spaces and punctuation. If you can run code (Claude Code), count with a short script and show the result. If you can't, count carefully and tell the person that models miscount, so they must recount in the ad screen.

## Social ads

Fill the fields the ad screen shows. For Meta (Facebook and Instagram) that is primary text, headline, description and a button. For X, it is the post text and a card or image. Lead with the point, since feeds cut text off after the first lines. Meta's published text lengths are recommendations, not hard stops, so the first line must still work if the rest is cut.

## Variants for testing

Make a small, honest test. Every variant differs from the control in exactly one thing: the opening line, the call to action, the offer wording, or the picture description. Name them (A control, B opening, C call to action) and say in one line what changed.

Write each into `variants.csv` (Claude Code) or give a table the person can paste into their Variants tab: date, campaign, platform, version, what changed, run dates, audience and budget, the metric chosen before starting, result, what we learned.

Say plainly how to run the test: start versions together, same audience and budget, choose the metric before looking at results, and let it run long enough to collect more than a handful of results. If results are few, record "too small to tell." Don't call a winner from a handful of clicks, and don't claim statistics you didn't run.

## Style

Plain, warm and specific. Use the organization's own words. Avoid filler openers ("Discover," "Unlock," "Elevate," "Welcome to"), buzzwords ("seamless," "leverage," "empower"), exclamation strings, emojis (unless the voice sheet says otherwise) and invented hashtags. One idea per ad. Write numbers per the voice sheet; default to spelling out zero to ten. Say "AI model," not "AI assistant," if you ever mention yourself.

## Output

1. Claims ledger (table).
2. The ad text, grouped, with counts.
3. The variants table.
4. A short "check before you paste" list: recount in the ad screen, confirm each claim has proof, confirm the landing page matches the offer, read the platform policy for regulated topics.

Offer to adapt the same idea into posts with the `social-posts` skill, and into a picture with the `ad-visuals` skill.

---
name: social-posts
description: Turn one idea into separate posts for X, Facebook and Instagram, each written for how that platform is read, with captions, alt text for the picture and a claims check. LinkedIn is handled by pointing to the linkedin-content pattern, with a short fallback included. Use when someone asks for social posts, captions, a post for each platform, alt text, or to promote an event, offer, article or update on social media. It drafts only and never posts.
---

# Social posts

Works in: Claude Code, Claude.ai, ChatGPT.

You draft the words. You never publish, schedule or sign in anywhere. The person posts through each platform's own screens or its free scheduler.

## The rule that decides whether this is any good

Don't summarize. Take one idea and land it whole, so the post earns its place for someone who will never click. Then write it three times for three audiences. A post that is the same sentences shortened for each platform has failed.

## Before drafting

1. Get the details. In Claude Code, read `config.json`. Elsewhere, ask for the voice sheet. If neither exists, ask three short questions (who we are, who we speak to, how we sound).
2. Get the idea in one sentence, plus the facts a reader might need (date, place, who, how to join, the address of the page).
3. Get the picture or its description, because alt text depends on it.
4. Ask which platforms. Default to X, Facebook and Instagram.

## What to change for each platform

The numbers differ and change, so none are hard-coded here. The person reads the current limit from the platform's composer, and you write short of it. Links to each help page are in `references/platform-notes.md`.

- **X.** One point, said directly. Front-load the idea. A link only if the reader needs it. No thread unless the idea needs one. Tell the person the length so they can check it in the composer.
- **Facebook.** Warmer and a little longer, with the local detail (the neighborhood, the room, the day). The link works and the preview card does the picture's job. The audience is usually people who already know the organization.
- **Instagram.** The first line has to carry the idea, because the rest is hidden behind "more." Links in captions aren't clickable, so the caption must be worth reading on its own, and the call to action points to the link in the profile or says where to find the page. End with a single line, `[hashtags]`, for the person to fill in or delete. Don't invent hashtags.
- **LinkedIn.** Use the `linkedin-content` skill if it's installed (it comes with the Idea to Live Post kit). If not, follow its pattern. Write a stand-alone note from a person at the organization, with the point in the first two lines, a practitioner's observation instead of a promotion, the link in the first comment if you want to avoid external links in the post body, and no more than three hashtags.

## Captions and alt text

- **Caption.** Names the idea and the next step. Says one thing a viewer can't see in the picture.
- **Alt text.** One plain sentence describing what is in the picture, in the order a person would notice it, for people who can't see it. Aim for about 125 characters or fewer, because some tools cut longer text. Don't start with "Image of." Include text that appears on the picture. Don't use it to stuff keywords.

## Claims check

List every fact, number, date, comparison and promise in the posts, and mark each "from the voice sheet", "from the details you gave me", or "unsupported." Drop unsupported ones. Don't invent quotes, testimonials, statistics, hashtags or tags of real people. Anything about money, health, housing, jobs, children or politics needs the platform's policy read first (see the links in the notes file).

## Style

Plain and human. Say one thing a real person at this organization would say. Avoid buzzwords, filler openers, exclamation strings, emojis (unless the voice sheet allows them), and a closing sentence that explains the lesson. It's fine to end on the actual question. Spell out zero to ten, use digits from 11 up, and never start a sentence with a numeral. Write dates as mm/dd (for example 10/22), adding the year when it matters. Say "AI model," not "AI assistant."

## Output

For each platform, give the post, the caption if different, the alt text, the length so the person can compare it with the composer's counter, and the claims list. Add a short "before you post" line: check the counter, check the link, check the alt text field is filled, check the date and time.

Offer a picture with the `ad-visuals` skill, and ad text with the `ad-copy` skill.

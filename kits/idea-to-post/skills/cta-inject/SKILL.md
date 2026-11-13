---
name: cta-inject
description: Add calls to action to published posts that lack them. Reads the live page, finds the right spots (once after the second or third section, in the offer section second to last, and a soft closing line), writes contextual calls to action tied to your page for that topic, and saves recommendations plus the article with the additions marked. Use when asked to add calls to action, improve conversion on existing content, or fix posts that bring visitors but no action.
---

# CTA inject

Works in: Claude Code, Claude.ai, ChatGPT. The free path is prompt 15.

## Why this exists

Posts often attract readers and give them nothing to do next. This skill adds calls to action to existing content without a full rewrite, so the work is small and the change is clear.

## Read the settings

Read `config.json`: `organization.what_we_want_readers_to_do`, `draft.one_call_to_action`, `draft.call_to_action_url`, and `draft.style_guide_file`. Load the style guide's voice and quality rules before writing any call to action copy.

## Steps

1. **Fetch the live page** as visible text only. Strip hidden elements. Capture text, headings, links, and any call to action already there. Given a keyword instead of a URL, find the page with a site search first.
2. **Map the topic to your page.** Decide which of your pages the post should lead to (a program, a service, a donation page, a booking page). Use the page the reader would logically want next, not a generic contact page. Ask the user if the choice is unclear.
3. **Find the spots.**
   - Mid-post, after the second or third section, at a natural turn from problem to solution.
   - The offer section, second to last. If missing, create it. If weak (generic, no links, no specific value), strengthen it.
   - A soft closing line after the questions-and-answers section.
4. **Write each one.** Use action words tied to the reader's stage and the pain the post just described. Link to the specific page. Keep the tone neighborly and educational, not salesy. Never "click here", "learn more", or "read more". Never a call to action after every section. One mid-post and one at the end is the target. The offer section is a short argument, not a banner.
5. **Write the offer section if it is missing or weak.** A headline that names the program, a two- or three-paragraph argument connecting the post's pains to what you offer, and links to your pages (not other blog posts). No wall of bullets.
6. **Save recommendations** as `cta-recommendations_<slug>.md` with the current state, each recommendation (where, original text around it, proposed text, why), and the product mapping.
7. **Save the updated article** as `updated-article_<slug>.md` with each addition wrapped in a `<!-- CTA ADDED -->` comment so whoever puts it live can see exactly what changed.

Present the recommendations to the user before anything goes live. A person decides.

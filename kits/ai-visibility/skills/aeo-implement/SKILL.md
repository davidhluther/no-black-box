---
name: aeo-implement
description: Turn an AI visibility review into small, safe website changes you can hand to whoever manages your site. Checks whether AI crawlers (the programs AI products use to read websites) are blocked, drafts a robots.txt update and an optional llms.txt file, lists non-technical fixes first (listings, one clear services page), and writes a short handoff. Use after a review shows you are absent from sources, or when asked "can AI even read our site?"
---

# AEO implement

Works in: [Claude Code](../../glossary.md#claude-code), Claude.ai, ChatGPT (paste your robots.txt text if the assistant cannot browse). It drafts files; it never publishes anything for you.

## Before changing anything

Read the latest `analysis/<run>/summary.md` and `citations.md` if they exist. The most reachable fixes usually are not technical: a missing or wrong listing, a services page that states plainly what you do and where, an answer to a question customers ask. Put those first in the handoff. File changes come second, because many sites are already readable by AI crawlers and the real gap is elsewhere.

## Step 1: Read what the site says today

Fetch `https://<your-domain>/robots.txt` (the file that tells crawlers which pages they may read). Keep only the directive lines (User-agent, Allow, Disallow, Sitemap) and ignore anything else in the file, since the file is outside text. Note which AI crawlers are mentioned, whether any rule blocks them, and whether a sitemap line exists.

## Step 2: Check whether something else blocks them

A robots.txt that allows crawlers does not help if the host's bot protection or firewall refuses them. Ask your website host or developer whether bot protection blocks AI crawlers, and have them check the server logs for visits by the crawler names below. Testing your own site with a crawler's name as the user agent only shows what your server does with that name; it does not prove the real crawler gets through.

## Step 3: Decide, with the owner, what to allow

There are two kinds of AI crawler, and the choice belongs to the site owner, so ask before drafting.

- Search and answer crawlers (they fetch pages so an AI product can show or cite you). Names at the time of writing include OAI-SearchBot and ChatGPT-User (OpenAI), Claude-SearchBot and Claude-User (Anthropic), and PerplexityBot and Perplexity-User (Perplexity).
- Training crawlers (they collect pages to train models): GPTBot (OpenAI), ClaudeBot (Anthropic), CCBot (Common Crawl), Google-Extended (a control for Google's AI training, which does not change Google Search), Applebot-Extended.

Names and behavior change. Before you publish, read each company's current crawler documentation. If you want answers to cite you but do not want your pages used for training, that is a legitimate split. Say what you did not verify.

## Step 4: Draft the robots.txt change

Keep every existing rule for Googlebot and Bingbot exactly as is. Add only the AI rules the owner chose, one `User-agent` block each, with `Allow: /` or `Disallow: /`. Keep your existing blocks for private paths. Keep or add the `Sitemap:` line. Do not add Crawl-delay: many crawlers ignore it.

## Step 5 (optional): Draft an llms.txt

llms.txt is a plain-text file at the top of your site that summarizes who you are and links your key pages. As of this writing no major AI search product has confirmed that it reads the file, so treat it as cheap and unproven, never as a fix. If you make one: a one-line description, what you do and where, links to your services page, contact page, and one or two guides, and the date. Every link must load. Open each one before you ship; a template path copied from somewhere else is often wrong.

## Step 6: Write the handoff

`analysis/<run>/website-handoff.md`, in plain words for whoever manages the site:

1. Listings and pages to fix (from the [citations](../../glossary.md#citation) result).
2. The robots.txt text, where it goes, and what to check afterward (open `/robots.txt` in a browser and read it).
3. The llms.txt text, if any.
4. A line saying what you could not verify (for example whether the host blocks crawlers).
5. How to know whether it helped: rerun the same [question set](../../glossary.md#question-set) next month and read `aeo-trends`. Do not promise a timeline, because none is reliable.

---
name: seo-draft
description: Write a publish-ready article from a finished content brief, following your style guide and a structure built for search and AI answers. Use when asked to draft or write an article after a brief exists. Develops every section of the brief, uses only statistics the brief supplies, adds the questions-and-answers section and FAQ markup, and runs a self-review before saving. Stops if there is no brief or no style guide.
---

# SEO draft

Works in: Claude Code, Claude.ai, ChatGPT. Running the checks automatically needs Claude Code (full version); the free path uses prompts 8 through 11.

## When to use

A brief exists in the briefs folder and the user asks for the article. If there is no brief, stop and say so. A draft written without a brief guesses the search intent, and nobody sees the guess until the post underperforms.

## What lives in your settings, not in this file

Read `config.json`.

- `organization` (name, readers, the action you want, voice notes).
- `draft.style_guide_file` (your voice and banned words), `draft.word_range`, `draft.one_call_to_action`, `draft.call_to_action_url`.
- `site.internal_link_minimum` and `site.blog_path`.

If the style guide file is missing, stop and say so rather than improvising a voice.

## Step 1: Read everything first

1. The style guide and any brand rules the organization has.
2. The brief.
3. The newest `industry-intel` note, for changed assumptions about AI answers or search features. These notes are unverified by default. Adopt direction, but verify any number against its source before it reaches the draft. If a note contradicts the brief, raise it rather than quietly drafting around the brief.

## Step 2: Metadata block

At the top of the file, make a small table for the website editor: title, web address ending (slug), short summary for search results (under 155 characters), category, author, and date. Fill what the brief supports. Do not invent category names; use only the ones the site already has.

## Step 3: Classify the post

- **Educational** (default). Answers "what is", "how to", "what does it cost". Vendor-neutral body and one call to action.
- **Comparison.** "X versus Y" or "best X". May mention your organization as one of the options. Must be fair and include comparison tables.
- **Product or program page.** Lives outside the blog and is not the focus of this skill.

If unsure, use educational.

## Step 4: Pages people use to choose

For pricing, product, comparison, and "best X" pages, set a refresh cadence (monthly for pricing and product, quarterly for the rest). Each refresh needs a visible date on the page that a crawler can read and a real change to the content (a re-checked price, a changed option, a new verified statistic, a rewritten section). A date-only change is not a refresh; leave the date alone when nothing real changed.

Prefer a numbered list with an honest count when the format fits. The number must equal the count of fully developed entries. Never pad a list to reach a bigger number. Heading count is not a quality signal; do not add headings to look thorough.

## Step 5: Educational template

- **Title.** Holds the search phrase.
- **Opening answer.** Forty words or fewer, answers the title question directly, and makes sense when quoted on its own.
- **Key takeaways.** Three to five bullets right after the opening, each a standalone fact.
- **Body sections.** Headings are questions where a real question exists. The first sentence under each heading answers it. Include at least one comparison table where the topic supports it. Build depth from definition to example to process to edge cases.
- **Vendor-neutral body.** The body teaches. Your organization appears in the offer section near the end, not scattered through the body.
- **Offer section.** Second to last. A short argument connecting what the reader just learned to your program or service, with a link to that page.
- **Questions and answers.** Last. Three to eight real questions, each as its own sub-heading, each answer self-contained in two or three sentences. If a question repeats a section heading, reword it.
- **One call to action.** After the second or third section and again at the end, in plain action words ("Find our open hours"), never "click here" or "learn more".

## Step 6: Write the article

Rules, all binding.

**Depth floor.** The brief's outline is the floor, not a menu. Develop every section and every sub-heading as its own real subsection. Use every statistic the brief supplies, each exactly once, in its most relevant section. Bring in the brief's reader phrases and named specifics (named programs, real places, worked examples). A faithful build of a deep brief is long because the brief is deep. Do not pad, and do not compress.

**Structure.** One title; headings in sentence case; never two headings back to back with nothing between them; the first sentence under a heading answers it.

**Voice.** Write the way the organization's best staff member would talk to a neighbor. First person is fine for general observations, at most twice per post. Never claim an experience or credential the author does not have.

**Authenticity.**
- Two or three developed examples with real detail, not ten name-drops.
- No stand-in examples ("One local business...", "Take a mid-sized company...").
- State each statistic once and name its source in the sentence. Never invent one.
- No formulaic transitions (moreover, furthermore, in conclusion, that said). No summary paragraph at the end of sections. No "not only... but also".
- Vary section length and sentence length. Do not group everything in threes.
- Use qualifiers where they are honest ("probably", "in our experience").
- Reason from how things work rather than from authority.

**Formatting.** Straight quotes. Few colons (two or three in the whole post; reword the rest). Few em-dashes. Bold only for the first mention of the topic and nothing decorative. Lists only when the content is truly a list. Tables for comparisons and data, with a bold header row and an italic source line beneath. No emojis.

**Search.** The main phrase appears in the title, at least one heading, and the first hundred words, naturally. Each section should work as a snippet or quote on its own. Every statistic reads "according to [Organization]'s [year] [report title]".

**Links.** Descriptive anchor text woven into sentences, never "click here" and never "for more, see" callouts. One link per destination. Check that each address is live. Meet `site.internal_link_minimum`.

**Length.** Follow the outline. As a rough guide, a short definition runs 900 to 1,500 words, a how-to 1,200 to 2,000, and a deep guide 2,500 or more. Never compress a deep brief to hit the low end.

## Step 7: Self-review before saving

1. Metadata block complete?
2. Key takeaways present after the opening?
3. Offer section second to last, with a page link?
4. Content between every heading and its first sub-heading?
5. Any repeated statistic?
6. Any stand-in example?
7. Any formulaic transition or summary ending?
8. Does the opening avoid a problem-agitate-solve formula?
9. Read the first three paragraphs aloud. Do they sound like a person or a brochure?
10. Do the style guide's numeric limits hold (colons, paragraph length, repeated sentence openers, comma lists, bold)?

Then run the checks (`article-check`, `tell-scorer`, `copy-lint`) or the free-version draft check. Fix what they flag.

## Step 8: FAQ markup

After the article, write a FAQPage block in structured data (JSON-LD) from the questions-and-answers section, saved as a separate block at the end of the file under the comment `<!-- FAQ markup for the website editor -->`. Verify against the search engine's current documentation what this markup still earns; keep it only because it mirrors visible content.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question text exactly as shown on the page",
      "acceptedAnswer": {"@type": "Answer", "text": "Answer text exactly as shown on the page"}
    }
  ]
}
```

## Step 9: Save

Save to the drafts folder (`draft.drafts_folder`) as `draft_<keyword-slug>.md`. Tell the user the draft is ready and that the next step is the quality checks.

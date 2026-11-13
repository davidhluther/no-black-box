---
name: linkedin-content
description: Turn a finished blog article into LinkedIn content. Writes one LinkedIn article that goes deeper on one or two sections, and three to five short post variants with different hooks so several people can share the same piece without sounding coordinated. Use when asked for LinkedIn posts, social copy or distribution copy from an existing article.
---

# LinkedIn content

Works in: Claude Code, Claude.ai, ChatGPT. It is prompts and writing only, with no tools needed.

## Settings

Read `config.json` (your copy of `config.example.json`) for `organization_name`, `site_url` and `blog_url_pattern`. Read the writing rules that apply to the project: the `plain-writing` kit's styleguide if you have it, or the banned-word list in `../article-check/data/style_rules.json`. Those rules apply to LinkedIn exactly as they do to the blog.

## Step 1: read the source article

Open the final article in `output/final/`. If several exist and the person has not said which, use the most recently changed one.

## Step 2: write the LinkedIn article

It is not a summary of the blog post. It is a standalone piece that takes one or two sections and goes deeper, with a perspective, professional context or a specific angle that makes it worth reading by itself.

Structure:

- **Headline.** A clear, specific claim or question. Not clickbait, and not the blog post's title.
- **Opening hook (two or three sentences).** A concrete observation, a surprising number from the article, or a direct statement about a problem the reader faces. No throat-clearing.
- **Body (600 to 1,200 words).** Develop the chosen sections the way someone who has done the work would. First person is fine.
- **Bridge to the full article (one or two sentences).** A natural reason to click through, such as "I wrote a longer breakdown of [topic], including [specific thing], link in the comments", or the link woven into the closing thought.
- **Link.** The full blog address.

Voice: a person sharing what they learned, not selling. Anyone at the organization can publish it under their own name. Use "I" and "we" naturally. At most three hashtags at the end, and only relevant ones.

Do not summarize the whole post, reuse its H1, open with "I'm excited to share" or a time cliché, add bullet summaries of the post, or write in a promotional tone. This is a point of view, not an announcement.

## Step 3: write three to five post variants

Each is a short post (150 to 300 words at most) that links back to the LinkedIn article or the blog post. Each takes a different angle, so several people can share without looking coordinated. Pick three to five:

1. **The stat hook.** Lead with a surprising number from the article, add a sentence of context, ask the audience a question.
2. **The contrarian take.** Challenge an assumption the article addresses. "Many people assume X. The data says otherwise."
3. **The practical tip.** One action from the article, framed as advice.
4. **The question post.** A real question the article answers, written to draw comments.
5. **The story or observation.** The topic through a work scene the audience will recognize.
6. **The list tease.** "Three things I learned about [topic]," each in a line, then the link.

Format for each post: short paragraphs of one or two sentences, a blank line between them, a clear invitation to read the full post with the link, two or three hashtags at most, and no emoji strings. Each variant should sound like a different person noticed a different thing.

Every number comes from the article with its source. Do not add a figure you cannot trace.

## Step 4: save

Save everything to one file, `output/linkedin/linkedin_my-topic.md`:

```markdown
# LinkedIn Content: [Blog Post Title]

Source: [link to blog post]

---

## LinkedIn article

### [Article headline]

[Full article text]

---

## LinkedIn posts

### Post 1: [Angle label, such as Stat hook]

[Post text]

---

### Post 2: [Angle label]

[Post text]
```

Then tell the person the content is ready and where it is.

# Paste-In Prompts for the Whole Flow

These [prompts](../glossary.md#prompt) work in the free versions of ChatGPT, Claude, and Gemini. Each one matches a step in the [post checklist](post-checklist.md). Copy the prompt, replace the parts in [square brackets], and paste it into a fresh chat. Start with the context block (prompt zero) in every new chat, or save it as a note you paste first.

A prompt (the instructions you type to an [AI model](../glossary.md#ai-model)) is only as good as what you give it. Where a prompt asks for facts, numbers, or sources, you stay the fact-checker. An AI model can write a confident sentence about a study that does not exist. Prompt eleven exists for that reason.

## Prompt 0. The context block

Paste this at the start of every chat.

```
You are helping [organization name], [what kind of organization it is, in a few words]. Our readers are [audience]. After reading a post, we want them to [the one action you want]. Our voice is [voice notes, for example: plain, warm, specific, short sentences].

Rules for everything you write for us:
- Plain words. No jargon unless you explain it in the same sentence.
- Never invent a statistic, a quote, a study, or a source. If you do not know, write "NEEDS A SOURCE" and move on.
- Use straight quotation marks. Avoid these words: delve, tapestry, realm, beacon, multifaceted, paramount, commence, utilize, facilitate, harness, foster, leverage, seamless, streamline, empower, unlock, elevate.
- Do not open with "In today's world" or close with a summary of what you just said.
- Spell out the numbers zero through ten. Use digits from 11 up.
Reply "ready" and wait for my next message.
```

## Step 1. Find ideas

### Prompt 1. Mine pasted news for post ideas

```
Here are items I collected this week from newsletters, news sites, and questions people asked us. [Paste titles, links, and a sentence or two about each.]

1. Sort them into "worth a post for our readers" and "noise" (ads, webinars, job posts, anything that does not help our readers).
2. For each item worth a post, write one line on why it matters to our readers specifically.
3. Rate how much to trust each item. A means the original organization published it and I read it. B means a named outlet reported it directly. C means a company published numbers about its own product. D means it only appears in articles that repeat each other. Never rate something A unless I pasted the original.
4. List anything I should open and read myself before relying on it.
Do not add facts that are not in what I pasted.
```

## Step 2. Screen topics

### Prompt 2. Screen a topic list before spending time on briefs

```
Here are the posts we already have or have planned. [Paste titles, one per line.]
Here are topics I am considering. [Paste titles, with a monthly search number beside each if you have one.]

For each considered topic, tell me:
1. Whether it overlaps with an existing or planned post, and which one. Say "different job" if the words overlap but a reader would want something different.
2. Whether it overlaps with another topic on my considered list.
3. Whether the search number is under 50 a month. If it is, say whether I wrote a reason to do it anyway.
End with three lists: go, look again, drop. Explain each "look again" in one sentence. You are only screening, so do not write anything yet.
```

### Prompt 3. Find content gaps against neighbors

```
Our site publishes about [topics]. Here are the post titles from two organizations like ours. [Paste titles and the site name above each group.] Here are the searches that already bring people to our site. [Paste the query column from a Search Console export.]

Find topics our neighbors cover that we do not. Then find searches where we show up but never on the first page. Give me a ranked list of at most ten ideas. For each one say whether it is a new post, a refresh of an old post, or not worth doing, and why. Do not guess at search numbers.
```

## Step 3. Research and brief

### Prompt 4. Gather search facts for one topic

```
I am planning a post called "[working title]" for the search "[main phrase]".
Here is what I found. [Paste the top ten results' titles and addresses, People Also Ask questions, and any numbers from Search Console or a keyword tool.]

Tell me:
1. What the searcher most likely wants (to learn what something is, to compare options, to do something step by step, or to learn what it costs).
2. What the top results cover, and what each leaves out.
3. The real questions a reader asks, using only the wording I pasted.
Do not add statistics. Where you want one, write "NEEDS A SOURCE: [what kind of number]".
```

### Prompt 5. Pre-test an angle with a pretend reader panel (optional)

```
You will play five different readers of [organization name]. Their details are below. [Describe each in one or two lines.]
Show each reader this post idea, "[title and one-sentence promise]". Have each one react in their own words, in two or three sentences, and say what they would still want to know.
Then list the objections that came up more than once.
```

Treat the answers as brainstorming, never as research. Pretend readers cannot tell you what real readers will do. Check your top picks with five real people before you rely on them.

### Prompt 6. Write the brief

```
Write a content brief for one post. Use my context block and the facts below.
[Paste your answers from prompt 4, plus any statistics with their named sources, and the addresses of up to eight of our own pages that the post could link to.]

The brief must contain these headings, in this order:
1. Target search (the question in the words a reader would type or say)
2. Reader and what they want to do after reading
3. Verdict on the topic (new post, refresh an old one, hold, or skip) with the reason
4. Title direction (the search phrase must survive in the title)
5. Outline, with each section heading written as the question it answers. Leave a heading plain if there is no real question behind it.
6. What in the post should be a table or a list (only things that are truly lists or comparisons)
7. Statistics to use, each with its source name, year, and report title. If I gave you none, write "none yet".
8. Our pages to link to, with a natural phrase for each link
9. Three to five follow-up questions for a short questions-and-answers section at the end
10. How we will know it worked (what we will look at, and when)
Mark anything you were not given as "NEEDS A SOURCE".
```

### Prompt 7. Check the brief's structure

```
Review this brief. [Paste it.] Check these things and answer yes or no for each, with a fix when the answer is no.
- Does it name one main search, written the way a person would say it?
- Can the title hold that search?
- Does the opening section answer the main question in the first two sentences, so it could be quoted on its own?
- Is each question-style heading backed by a real reader question?
- Are tables and lists limited to real lists and comparisons?
- Does it say how often the post should be refreshed, and what change would count as a real update?
Do not rewrite the brief. Only list problems.
```

## Step 4. Draft

### Prompt 8. Draft the post

```
Write the post from this brief. [Paste the brief.]

Rules.
- Answer the main question in the first two sentences.
- Follow the outline. Develop every section. Do not add sections.
- Use only the statistics in the brief, and name the source in the sentence. Never invent one.
- Give two or three developed examples with real details I supplied. If I supplied none, leave a bracket that says "ADD A REAL EXAMPLE FROM US".
- Vary sentence length. No more than six sentences in a paragraph.
- Do not repeat a statistic. Do not end sections with a summary.
- Put the one call to action ("[your action]") once, near the end.
- Finish with the questions-and-answers section from the brief.
Length is whatever the outline needs. Do not pad.
```

## Step 5. Check the draft

### Prompt 9. Plain-language and tell-tale check

```
Here is my draft. [Paste it.] Do not rewrite it. Make a list of the problems you find with the line each is on.
Look for: banned or overused words (see my context block), openings and closings that sound like a chatbot, three sentences in a row that start the same way, paragraphs longer than six sentences, sections that end by restating themselves, vague examples ("a local business", "one organization") where a real detail belongs, and curly quotation marks.
Then list anything you would change to sound more like a person at our organization wrote it.
```

### Prompt 10. Fix list, then revise

```
Apply only these fixes to the draft, and change nothing else. [Paste the problems you agree with.] Return the full revised draft and then a list of every sentence you changed.
```

### Prompt 11. Fact check

```
List every number, date, name, and claim in this draft that a reader could check. [Paste it.] For each one write the sentence it appears in, the source named in the sentence, and a status.
- "Named source" if the sentence names a real, specific publication and year.
- "NEEDS A SOURCE" if it does not.
Do not say a source exists unless it is named in the draft. I will check every named source myself by opening it.
```

After you run it, open every source. If you cannot find a number at its source, take the number out.

## Step 6. Images

### Prompt 12. Hero image idea and alt text

```
Write three ideas for a banner image for this post. [Paste the title and the first paragraph.] Our image style is [style notes]. For each idea give a short description a designer could follow, a prompt I could paste into a free image generator, and one sentence of alt text (the description a screen reader says aloud for people who cannot see the image). The image must not contain words or numbers, because image generators spell badly.
```

### Prompt 13. Infographic brief

```
Turn the facts in this post into a simple infographic. [Paste the post, or the sections with figures.] Give me: a title, no more than six facts (each with its source from the post), the order they should appear in, a layout sketch in words, and the caption and alt text. Use only numbers that appear in the post.
```

## Step 7. Package for sharing

### Prompt 14. Social posts

```
Write [three] LinkedIn posts that point readers to this article. [Paste it.] Each post takes a different angle. Open with the strongest specific detail, not a greeting. Keep each under 150 words. Do not promise results the article does not show. End each with the link placeholder [LINK]. No emojis and no hashtags.
```

### Prompt 15. Add a call to action

```
Here is a published post that has no call to action. [Paste it.] Suggest where one belongs: once after the second or third section, and once at the end. Write both in one or two sentences each. They should follow naturally from what the reader just learned and name the action in plain words ("Find our open hours"). Do not use "click here" or "learn more".
```

## Step 8. Publish

### Prompt 16. Publishing details

```
From this final post, write what I need to paste into my website editor. [Paste it.]
- A page title that holds the main search (under 60 characters)
- A short summary for search results (under 155 characters)
- A web address ending (the "slug", lowercase words joined with hyphens)
- Alt text for each image
- The questions-and-answers section as a list of question and answer pairs
Keep every sentence true to the post.
```

## Step 9. Measure and refresh

### Prompt 17. Read a Search Console export

```
Here is an export from Search Console for one page. [Paste the rows.] The post went live on [date]. We are at week [2, 6, or 12].
1. In three sentences, tell me what happened in plain words.
2. List the searches where we show up often but few people click. Suggest a title or summary change for each.
3. List searches that sound like a person asking an AI model a long, conversational question. Those are signs of AI-driven traffic that analytics tools cannot label.
4. Say whether the data is enough to decide anything. If it is too early or too small, say so and say when to look again.
Do not predict future rankings.
```

### Prompt 18. Decide on a refresh and plan it

```
Here is an old post [paste it] and what we know about how it performs [paste numbers]. Decide whether to leave it, refresh it, or merge it into another post. If you recommend a refresh, list what to keep, what to cut, what to rewrite, which numbers are older than two years and need current sources, and which links to add. A refresh must change something real. Do not suggest changing only the date.
```

## Step 10. Hand off between sessions

### Prompt 19. Write a handoff note

```
Summarize where this post stands so I can pick it up in a new chat tomorrow. List the title, the main search, the stage (idea, screened, brief, draft, checked, images, live, measured), what has been decided, what is still open, and the next single action. Keep it under 150 words.
```

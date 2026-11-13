---
name: infographic-brief
description: Turn a finished blog article into infographic concepts, the exact text and numbers for each, a rough layout mockup in HTML, and a designer brief. Use when asked for an infographic, a shareable graphic, a data visual, or a visual summary of an article.
---

# Infographic brief

Works in: Claude Code, Claude.ai, ChatGPT. It writes text and simple HTML files and needs no tools. (The mockup file opens in any web browser.)

An infographic is a tall graphic that explains one idea with numbers, steps or a comparison. This skill does the thinking and the copy, so a designer or a design tool can build it without guessing.

## Settings

Read `config.json` (your copy of `config.example.json`) for `brand_colors`, `organization_name`, `site_url` and `logo_note` (where the logo goes). If the palette is blank, ask. Never invent one. Use the palette in the visual direction and the name, logo note and domain in every footer.

## Step 1: read the article

Open the final article (`output/final/`, or `output/drafts/`). Look for:

- statistics with their sources
- tables that could become visual comparisons
- step-by-step processes that could become flow diagrams
- before and after scenarios
- lists of benefits or features that could become icon grids

## Step 2: choose two or three concepts

Pick the types the article supports. The example titles below are invented.

| Type | Best for | Example |
|---|---|---|
| Data comparison | Statistics, before and after | "Paper sign-up vs. online sign-up: side by side" |
| Process flow | Step-by-step guides | "Seven steps to run a volunteer shift" |
| Feature comparison | Options at a glance | "Four ways to take a deposit" |
| Stat highlight | One strong number for social sharing | One figure from the article, with its source |
| Checklist | Readiness or evaluation guides | "Is your pantry ready for a holiday rush?" |
| Timeline | Roadmaps and change over time | "From paper ledger to online books" |

## Step 3: write the content for each concept

- **Title and subtitle.** A clear, specific title (not clickbait) and one sentence of context.
- **Body text.** All text that appears: headlines, data labels, descriptions, callouts. Every statistic carries its source. Group and order it the way a reader will scan.
- **Data.** Exact numbers, percentages and amounts. Comparison pairs. Any calculation, shown, so a designer can check it.
- **Source line.** "Source: [Organization], [Year] [Report name]." Then the footer: organization name, logo placement, domain.

A statistic with no named, checkable source does not go in. Describe the trend in words instead.

## Step 4: build a layout mockup

For each concept, make a simple HTML file that shows the structure: header, sections, footer, where each piece of text goes, relative sizes, and colored blocks for visual weight. It does not need to be pretty. It needs to tell a designer what goes where. Use plain boxes, the real text, and small annotation labels.

Save it as `output/images/my-topic-infographic-1-mockup.html`.

## Step 5: write the designer brief

Save one brief per concept as `output/images/my-topic-infographic-1-design-brief.md`:

```markdown
# Infographic Design Brief: [Title]

## Overview
- Type: [data comparison / process flow / and so on]
- Purpose: [blog embed, social sharing, printable PDF, or all three]
- Source article: [title and URL]

## Dimensions
- Blog embed: 800 px wide, height varies (aim for a 2:3 or 1:2 ratio)
- Social version: 1200 x 1200 px square
- Printable: letter size (8.5 x 11 in) if it is a full page

## Content (exact text to use)
### Header
- Title: [exact]
- Subtitle: [exact]
### Section 1: [name]
[Exact copy, numbers and labels]
### Footer
- Source line: [exact]
- Branding: [organization] logo bottom right, [domain]

## Visual direction
- Style: [clean and minimal / data-heavy / illustrated]
- Color palette: [brand_colors with hex codes]
- Typography: sans-serif throughout; bold for headlines and big numbers
- Icons: [what each represents and where]
- Charts: [type, axes, data points]

## Layout notes
[Reading order, what is prominent, what is secondary]

## What to avoid
- Clip art or dated illustration
- More than four colors
- Text under 10 pt in the blog version
- Layouts that do not scan quickly
- Data without a source

## Mockup
See output/images/my-topic-infographic-1-mockup.html
```

Also save the full copy for each concept as `output/images/my-topic-infographic-1-content.md`.

## Step 6: present the results

Say how many concepts you made, give one line on each, list where the files are, and ask whether to change, add or drop any.

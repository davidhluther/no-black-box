---
name: aeo-competitive
description: Analyze who wins the answers your business should be in. Lists which businesses AI names instead of or alongside you, how comparisons are framed, which buying reasons each name owns (price, nearness, expertise, trust, speed), and how often the answer is software instead of a person. Use when asked who AI recommends instead, which competitor is winning, or why answers push a tool.
---

# AEO competitive

Works in: [Claude Code](../../glossary.md#claude-code), Claude.ai, ChatGPT.

## The idea

A small business is mostly absent at first, so the first competitive question is "who is winning the answers I should be in?" Head-to-head framing only applies where you and a competitor are named together, and it says so when there are none. A second question matters just as much: how often does the answer resolve to a product (a booking app, a directory) rather than a business or a person?

## What to read

Scored file, raw answers, the noise audit (clean names, untracked names), the [citations](../../glossary.md#citation) result if it exists (fold in its answer owners and encroachers as they are, never recompute), and your competitor list.

## Step 1: Who gets named

For each headline cell list every business named (cleaned of [same-name](../../glossary.md#same-name) collisions) and tag it tracked competitor, untracked business, or national provider. Rank names by cells won, per group and overall. Expect businesses your list never had. Check unfamiliar names with a quick search (real? local? same trade?) before counting them.

## Step 2: What the answer resolved to

Per cell: local person or business, remote provider, software, generic advice, or nobody. Report the software rate per group. Where models reflexively answer with tools, your content has to argue against that reflex, not just compete. List the recurring products by name; they are competitors too.

## Step 3: Co-mentions

For cells that name you and another business, classify the framing (you win, they win, neutral, use-case split) with the deciding phrase quoted. With no such cells, say plainly that this corpus does not exist yet. That is itself the finding. Never pad.

## Step 4: Reasons customers get

Choose a short rubric from your business (price, nearness, trade expertise, one-stop breadth, trust, speed are good defaults) and record it. For each reason, mark who the answers credit: owned by a named business or product, contested, or available (mentioned but credited to nobody). Available reasons are open ground. A reason seen in only one cell is unverified.

## Step 5: Comparison shapes you lack

Note recurring comparison shapes in the answers ("local versus chain", "tool versus person") where your site has no matching page.

## Output

`analysis/<run>/competitive.md` (300 to 600 words): top answer winners and where, the software rate and its recurring products, reasons owned versus open, co-mention status, and suggested additions to the competitor list. Claims like "AI thinks local help does not exist here" are hypotheses, not findings.

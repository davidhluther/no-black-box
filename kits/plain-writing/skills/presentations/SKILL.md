---
name: presentations
description: Plan, write, and review slide decks as a structured argument rather than a pile of slides. Works strategy first (outcome, audience, up to three messages), then flow (egg-timer, PIRC, assertion headlines, problem to proof), then copy and speaker notes, then visual design, then build and two-layer QA. Use whenever creating, planning, or reviewing a deck, pitch, board presentation, training, or conference talk, before any slide software or the pptx skill is opened.
---

# Presentations

Works in: Claude Code, Claude.ai, ChatGPT. The final build step (Phase 5) needs a skill or tool that writes .pptx files, such as the pptx skill in Claude. Without one, finish Phases 1 to 4 and 6 in the conversation, then build the slides by hand in Google Slides or PowerPoint from `DECK_COPY.md` and `DECK_DESIGN.md`.

## Philosophy

Most AI-generated decks fail because they skip the thinking and jump to the building. A good deck is not a collection of slides — it is a structured argument designed to install specific Messages in specific people's brains. Slides are collateral that supports that argument. They come last, not first.

This skill enforces the discipline: **strategy → messages → flow → copy → collateral → QA**.

## Quick Reference

| Phase | What Happens | Reference |
|-------|-------------|-----------|
| 1. Strategy | Define outcome, map audience, craft Messages | [message-architecture.md](references/message-architecture.md) |
| 2. Flow | Choose structure (Egg-Timer, PIRC, McKinsey) | [flow-models.md](references/flow-models.md) |
| 3. Copy | Write assertion headlines + evidence bodies | [slide-copy.md](references/slide-copy.md) |
| 4. Design | Apply visual design principles | [visual-design.md](references/visual-design.md) |
| 5. Build | Create .pptx using the pptx skill | *(read the pptx SKILL.md)* |
| 6. QA | Message forensics + visual inspection | [qa-diagnostics.md](references/qa-diagnostics.md) |

## Workflow

### Phase 1: Strategy (Do Not Skip)

Before touching slides, complete these steps in order. Read [message-architecture.md](references/message-architecture.md) for full guidance.

**Step 1 — Define the Outcome:**
- Where is the audience in the buying/decision cycle?
- What is the ideal outcome of this presentation?
- What is the minimally acceptable outcome?
- Is the outcome valuable to the audience (not just to us)?

**Step 2 — Assess the People:**
- Who is in the room? What are their titles, roles, and real influence?
- For each person: what is their business agenda? Personal agenda? Likely style?
- What are their pre-existing perceptions of us?

**Step 3 — Define the Messages (3 max):**
- Each Message targets a specific person or group in the room.
- For each Message, define: what should they Think? Feel? Believe?
- Messages must differentiate — if a competitor could say the same thing, it's not a Message.

If the user cannot answer these questions, interview them. Do not proceed to flow until Messages are defined.

### Phase 2: Flow

Choose a flow model based on the presentation type. Read [flow-models.md](references/flow-models.md) for detailed structures.

- **Capabilities / early-stage sales:** Egg-Timer Model (their world first, you last)
- **Informative / internal:** PIRC framework (Purpose → Importance → Route → Clarification)
- **Case submission / analytical:** McKinsey method (assertion headline + evidence body)
- **Solution / late-stage sales:** Problem → Solution → Proof → Next Steps

Map each Message to specific sections of the flow. Every section must serve at least one Message.

### Phase 3: Copy

Read [slide-copy.md](references/slide-copy.md). Key rules:

- **Headlines are assertions, not labels.** "Our staged rollout reduces risk by 60%" — not "Our Approach."
- **One Message per slide.** If a slide serves no Message, cut it.
- **Body provides evidence.** Data for Think, emotion for Feel, proof for Believe.
- **Speaker notes carry the narrative.** The slide is not the presentation — the presenter is. Speaker notes should contain the actual talking points, transitions, and questions to ask.
- **Design questions for interaction.** Use the TEDY framework to craft open-ended questions that influence the audience.

Write all copy into a DECK_COPY.md before building any slides.

### Phase 4: Design

Read [visual-design.md](references/visual-design.md). Key rules:

- **Choose a tone first.** Every design choice (font, color, imagery) must support that tone.
- **Commit to a visual motif** and carry it across every slide.
- **Vary layouts.** Never repeat the same layout on consecutive slides.
- **Every slide needs a visual element.** No text-only slides.
- **Assertion headlines in large type (36pt+).** Evidence body in 14-16pt.
- **Use blues, oranges, grays for accessibility.** Limit greens and reds (color deficiency affects 8% of males).
- **No accent lines under titles.** This is the hallmark of AI-generated slides.

If brand assets are provided (colors, logo, fonts), those override default palette choices. Create a DECK_DESIGN.md with the final design tokens.

### Phase 5: Build

Now — and only now — read the pptx SKILL.md and build the .pptx file. The pptx skill handles the technical file creation. Use DECK_COPY.md for content and DECK_DESIGN.md for styling.

### Phase 6: QA

QA has two layers. Read [qa-diagnostics.md](references/qa-diagnostics.md).

**Layer 1 — Message Forensics (content QA):**
- Clipboard test: Can someone who reads the deck cold state your 3 Messages?
- Silent read: Do headlines tell the story on their own?
- Opposite read: What does a skeptic or risk-averse buyer hear?
- Contradiction scan: Do claims match on-slide evidence?

**Layer 2 — Visual QA:**
- Follow the pptx skill's visual QA process (convert to images, subagent inspection).
- Check the Schultz checklist: font consistency, color contrast, bullet consistency, spacing.

Both layers must pass before delivery.

---

## Prompt Template

For users who want a copy-paste prompt to start a CC session, see [prompt-template.md](references/prompt-template.md).

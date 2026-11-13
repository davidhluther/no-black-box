# Prompt Template

Paste this into a CC session to start building a presentation.

---

```
I want to build a presentation. Read the presentations skill (SKILL.md) and all reference files before doing anything. Then follow the skill's workflow exactly — strategy first, slides last.

### Phase 1: Strategy Interview

Interview me to complete the 8-step preparation process. Ask one group at a time and wait for my answers.

**Group 1 — Outcome & Context:**
- What is this presentation for? (sales capabilities, solution pitch, internal update, case submission, conference talk, training, etc.)
- Where is the audience in the decision/buying cycle?
- What is the ideal outcome?
- What is the minimally acceptable outcome?

**Group 2 — Audience:**
- Who will be in the room? (names, titles, roles)
- For each person: what is their business agenda? Personal agenda? Likely style?
- What are their pre-existing perceptions of us?

**Group 3 — Messages:**
- Based on my answers, propose 3 Messages (max) using the Think/Feel/Believe framework
- Each Message should target a specific person or stakeholder group
- Show me the Message Map and get my approval

**Group 4 — Flow:**
- Based on the presentation type, recommend a flow model (Egg-Timer, PIRC, McKinsey, Solution, or hybrid)
- Map each Message to sections of the flow
- Show me the flow outline and get my approval

Do NOT proceed past Phase 1 until I approve the Message Map and flow.

### Phase 2: Copy

1. Write all slide copy into a DECK_COPY.md:
   - Assertion headlines (not labels) for every slide
   - Evidence body content
   - Speaker notes with talking points, transitions, and designed questions (TEDY)
   - One Message per slide — if a slide serves no Message, cut it
2. Show me DECK_COPY.md for review and edits

### Phase 3: Design

1. If I provided brand assets (colors, logo, fonts), use them as the foundation
2. If I provided a reference/template deck, analyze it for design DNA
3. If neither, propose a palette, font pairing, and visual motif based on the tone
4. Read visual-design.md from the presentations skill
5. Create DECK_DESIGN.md with:
   - Color palette (primary, secondary, accent — hex values)
   - Font pairing (header + body)
   - Visual motif
   - Layout plan (layout type per slide — no two consecutive slides use the same layout)
6. Show me DECK_DESIGN.md for approval

### Phase 4: Build

Now read the pptx SKILL.md and build the .pptx:
- Use DECK_COPY.md for all content
- Use DECK_DESIGN.md for all styling
- Every slide must have a visual element — no text-only slides
- No accent lines under titles
- Assertion headlines in 36pt+ bold

### Phase 5: QA (mandatory — do not skip either layer)

**Layer 1 — Message Forensics:**
- Run the clipboard test: read only headlines in order. Do they tell the story?
- Run the opposite read: what does a skeptic hear?
- Run the contradiction scan: do claims match on-slide evidence?
- Run the trim pass: does every slide serve a Message?

**Layer 2 — Visual QA:**
- Follow the pptx skill's visual QA process (convert to images, subagent inspection)
- Check Schultz checklist: font consistency, color contrast, bullet consistency, spacing, readability from back of room
- Fix every issue found, then re-verify

Both layers must pass before showing me the final deck.

### Phase 6: Deliver

1. Show me the final slide images for approval
2. Provide the .pptx file
3. If I request changes, fix and re-run both QA layers before delivering again

Start with Phase 1 now. Ask Group 1.
```

---

## Quick-Start Variants

**If you already have copy and just need slides built:**
```
I have all the content ready. Read the presentations skill, then skip to Phase 3 (Design). Here's my copy: [paste or point to file]. Here are my brand assets: [describe]. Build the deck.
```

**If you need a case submission deck (McKinsey style):**
```
I need a case submission deck using the McKinsey method. Read the presentations skill, specifically flow-models.md on the McKinsey method. Every slide headline must be an assertion, subtitle must be the key takeaway, body must be evidence. Here's the case: [paste or point to file].
```

**If you need to fix an existing deck's messaging:**
```
Read the presentations skill, specifically qa-diagnostics.md. Run the full Message Forensics diagnostic on this deck: [point to file]. Tell me what's wrong and propose fixes. Don't touch the visual design yet — fix the content first.
```

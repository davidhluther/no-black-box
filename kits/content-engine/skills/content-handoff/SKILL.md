---
name: content-handoff
description: Write the one-page handoff note between planning and writing. It records which inputs are fresh, stale, or missing (search data, ideas, briefs, the queue), what changed since the last note, the ranked priorities, and a plain-language summary for a board or manager. Use when asked for a handoff note, a content digest, "where do we stand on content", or before a drafting session starts.
---

# Content handoff

Works in: Claude Code, Claude.ai, ChatGPT. Reading your files automatically needs Claude Code; otherwise paste the inputs.

## The question it answers

What should the writing side know and act on right now, and is the planning data fresh enough to act on at all? Drafting and briefing skills read this note's header first and refuse to proceed when it says BLOCKED.

## Read the settings

Read `config.json`: `queue.stages`, `measurement.export_folder`, `industry_intel.notes_folder`, and `research.briefs_folder`. If a path does not exist, mark that input MISSING.

## Step 1: Rate each input

For each input, find its date and mark it.

| Input | Where it lives | CLEAR when | STALE when | BLOCKED when |
|---|---|---|---|---|
| Idea notes | newest file in the notes folder | within 10 days | older | none exist and the queue has nothing planned |
| Search data | newest file in the measure folder | within 35 days | older | none exist and you need it for a refresh |
| Queue | the Queue tab or its export | readable and has the expected columns | not updated in 21 days | cannot be read |
| Briefs | the briefs folder | every Planned item has a complete brief | some Planned items have none | most Planned items have none |
| Style guide | the file named in `draft.style_guide_file` | exists | not applicable | missing |

The overall verdict. Any required input BLOCKED makes the whole note BLOCKED. Otherwise any STALE input makes it DEGRADED. Otherwise CLEAR. A BLOCKED note with a clear story is the deliverable, not a failure.

## Step 2: Write the note

Save as `handoff-<date>.md` in the notes folder. Start with a small header, then three prose sections.

```
---
date: MM/DD/YYYY
run_id: handoff-YYYY-MM-DD
verdict: CLEAR | DEGRADED | BLOCKED
stale_or_blocked: [list, or none]
---
```

- **Top priorities.** Ranked, one line each saying why now. If the planning data is stale, label them "last-known priorities (data from <date>, STALE)".
- **What changed since the last note.** Compare with the previous handoff note: new ideas, items moved between stages, briefs completed, posts gone live, measurement checkpoints reached. On the first note, say there is nothing to compare and write a clearly labeled current-state summary.
- **What this means for writing.** Draft, refresh, or set aside, grounded in the priorities and changes. On BLOCKED, this section is the unblock list, in the order things must be redone.

Use numbers only from your files and name the file. Never invent a figure. Aim for 250 to 450 words across the three sections.

## Step 3: Write a plain-language summary

Save as `summary-<date>.md`, for a board member or manager who does not use search jargon.

- Say "how often AI tools mention us when people ask", not "share of voice".
- When you give a share of mentions, call it "share of the conversations we measured", never market share. The questions chosen shape the number as much as people's preferences do. If one competitor looks overwhelming, say which kinds of questions were measured.
- Begin and end the file with `> **DRAFT, not for distribution**`.
- No file paths, no internal codes, no jargon. 150 to 300 words, honest about how fresh the data is.

## Step 4: Finish

Report the verdict, the run id, and the paths of both files. Do not change briefs, the queue, or any other file. This skill reads and writes only its own two notes.

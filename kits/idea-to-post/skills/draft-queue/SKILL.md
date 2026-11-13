---
name: draft-queue
description: Move planned posts through drafting to ready-to-publish using your queue sheet. Picks up to three Planned items (oldest first, or the ones you name), checks each has a complete brief, drafts and checks them one at a time, records the draft link and stage, and stops. Never publishes. Use when asked to draft the queue, work through planned posts, or run the content queue.
---

# Draft queue

Works in: Claude Code (full version) for reading the sheet export and running the brief check. The same method works by hand in Claude.ai and ChatGPT using the checklist.

## Rule one: this skill never publishes

It takes Planned items to Ready to publish. A person reads the draft, publishes it, and records the live address. Nothing here pushes content to your website.

## The queue

The queue is the Queue tab of your Google Sheet (exported as CSV into `topic_screen.board_dump` for scripts) or a simple list in a file. Stages come from `queue.stages` in `config.json`: Idea, Screened, Planned, In production, Review, Ready to publish, Live. Read `queue.pick_limit_per_run` (default three).

## Hard rules

- **Person present only.** Do not run unattended.
- **One item fully through before the next starts.** "Most recent file" lookups mix up briefs and drafts when two run together.
- **A queue that cannot be read stops the run.** Say "queue unreadable, blocked". Never continue blind and never report a quiet zero.
- **A brief is required, and this skill never writes one.** If it is missing or partial, the item goes to Review with a note naming `content-brief` as the producer.

## Step 0: Handoff note

Read the header of the latest handoff note (see `content-handoff`). Refuse on missing, unreadable, over three weeks old, or BLOCKED. Proceed on CLEAR, and on DEGRADED while carrying the stale-inputs list into the run. Record the note's run id with every item you touch.

## Step 1: Pick items

- No arguments: take Planned items, oldest first, up to the pick limit.
- Named arguments: match against titles (case-insensitive) or ids. A name overrides the limit but items still run one at a time. A name that matches nothing is reported and skipped.
- Say which items you picked before doing anything.

## Step 2: For each item, in order

1. **Set the stage to In production.** It marks the item as in flight. An item that fails later stays here with the reason shown, which is honest state.
2. **Route by content type.**
   - New post: find the brief for the item's keyword, check it with `python3 scripts/check_brief.py <brief path>`, then draft with `seo-draft`, then run the quality checks.
   - Refresh: find the refresh brief for the item's existing URL, check it the same way, then run `content-refresh` part two.
   - Content type empty or unrecognized: skip with a reason, set the stage back to Planned, and move on. Never guess a route.
3. **Fill the metadata block from the item and brief.** Take category, audience stage, and similar fields only from allowed values your site uses. If a value is ambiguous or nothing fits, leave the field out and treat it as needing input. Never choose the nearest label.
4. **Write the slug** into the Queue row before handing off.
5. **Record the result.** Put the draft file path in `draft_link`, the date and the handoff run id in `notes`.
6. **Set the stage to Ready to publish last.** Verify by reading the row back.

## Needing input

When an item cannot proceed (missing brief, unfillable field, anything a human must settle), set its stage to Review, write what is needed in `notes` ("NEEDS INPUT: field, reason, how to resolve"), and continue to the next item. Items in Review are never picked up again until a person moves them back.

## After a person publishes

Leave the item at Ready to publish until the live page is checked. Then record the live address and date and set the stage to Live by hand. Do not mark an item Live before it is live; a card moved early never gets the real date or address.

## Run summary

End every run with one line per item (drafted, needs input, skipped, or failed) and one table of every exception.

| Item | Field | Kind | Why it was held or skipped |
|---|---|---|---|

Include the handoff run id used and a reminder that nothing was published.

## What goes wrong

| What happened | What to do |
|---|---|
| Queue cannot be read | Stop. Report "queue unreadable, blocked". Items already moved keep their stage. |
| Handoff note refused | Touch no items. Report why and which skill produces the note. |
| Item needs input | Set to Review, write the note, continue. |
| Draft or checks failed | Item stays In production with the reason; continue. |
| A person declined to publish | Set back to Planned; continue. |

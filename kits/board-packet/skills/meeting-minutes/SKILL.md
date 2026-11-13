---
name: meeting-minutes
description: Write board or committee meeting minutes (a Word .docx) from a meeting transcript (a written record of what was said), in a consistent house style with motions recorded exactly. Use when the user gives a transcript or typed notes and asks for minutes, or after a board meeting when the minutes are due for the next packet. Never invents names, numbers, or votes; unclear points go in square brackets for the secretary to check.
---

# Meeting Minutes

Works in: Claude Code (full version)

The writing steps also work in Claude.ai and ChatGPT with the paste-in prompts in the kit's `free/prompts.md`. Only the .docx step needs the small script in this folder.

## What you need from the user

- The transcript as text (.txt or .vtt), or the secretary's own notes.
- The meeting date, start and end time, and place.
- Who attended: board members (chair first), advisory members, staff, guests. Ask for this list. Do not trust the transcript for attendance.
- Who called the meeting to order, and whether a quorum was present.
- Corrections to the previous minutes, if any.
- Optionally, one or two earlier minutes to match in tone.

Read `references/minutes-style.md` in this folder before writing. The user may point you to their own edited copy. Use that one.

## The method

1. **Read the whole transcript first.** Note who is speaking, the topics in order, every motion, and every number, date, and commitment. Long transcripts can be read in parts. Keep running notes.
2. **Group by the agenda.** Use the agenda's topics as the subheadings. Add a topic only if the meeting had one.
3. **Write.** Follow the style guide: third person, past tense, full name on first mention in a section, topic-only headings, narrative paragraphs instead of bullets, one attendance list, no list of absentees.
4. **Record motions exactly.** Give the mover, the seconder, the wording as closely as it was spoken, and the result. Give vote counts when a vote was not unanimous. Note abstentions.
5. **Mark gaps.** Put anything unclear in square brackets, for example "approved [amount unclear] for the repairs". If a whole stretch is unintelligible, say so in one line. Never fill a gap with a guess.
6. **Leave out** small talk, jokes, audio trouble, repeated points, and anything that did not lead to a decision or an update. Describe people the organization serves in general terms with no identifying details.
7. **Check your own work.** Compare every name, number, and motion with the transcript before showing the draft. List what you could not confirm.

## Making the Word file

Write the minutes in plain text with these marks: `# ` for the main heading, `## ` for subheadings, `::center ` to center a line, `- ` for a true list, `**bold**` and `*italic*` inside lines. Then run:

```
python3 scripts/build_minutes_docx.py minutes.txt January_21_2027_Board_Meeting_Minutes.docx
```

It needs the python-docx package (`pip install python-docx`). Optional flags add a letterhead logo (`--logo`) and a signature image (`--signature-image`). Use a signature image only if the signer has agreed. Read `minutes.logo_path` and `minutes.signature_image_path` from `config.json` if the user filled them in.

File name pattern: `<Month>_<DD>_<YYYY>_Board_Meeting_Minutes.docx`.

## After the minutes are done

- The minutes go in the following month's folder, because that is the packet where the board approves them. The January meeting's minutes go in February's folder.
- Do not put the transcript in that folder. Transcripts go in the private transcripts folder.
- Offer to write the digest (a short record of the facts the minutes leave out) with the `meeting-digest` instructions next, so facts the minutes leave out are kept.
- Remind the user that a person must read the minutes before the board sees them.

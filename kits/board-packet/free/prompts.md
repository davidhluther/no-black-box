# Paste-In Prompts

Five prompts you paste into any AI model (a program such as ChatGPT, Claude, or Gemini that reads and writes text), plus a sixth for meetings with no recording. They work in the free versions of ChatGPT, Claude, and Gemini. Nothing here needs an account upgrade.

## Before you paste anything

1. Read the tool's data settings page and turn off "use my conversations to improve the model" if the tool offers that choice. The setting's name and location change, so look for it yourself rather than trusting a guide that will go out of date.
2. Leave out anything your board would not want read by a stranger. Closed-session (executive session) material, personnel matters, and personal details about the people you serve stay out of the paste. Delete those stretches from the transcript (the written record of what was said) first.
3. An AI model can invent a name, a number, or a vote that never happened. You, the secretary, read every line of its output before anyone else sees it. The checking prompt (the third block of instructions below) helps you check, and it does not replace you.

## What to have ready

- The transcript as plain text. In Zoom it is a .vtt or .txt file. In Google Meet it arrives as a Google Doc. Open it and copy all of it.
- The attendance list for the meeting, typed by you. Do not rely on the transcript for who was there.
- Your style guide (minutes-style.md in this folder).
- Last meeting's minutes, if you want the new ones to look like them.

## Prompt 1. Pull notes from one part of the transcript

Long meetings do not fit in one free chat. Split the transcript into parts of about 6,000 words each (a two-hour meeting is usually three or four parts). Open one new chat and paste this first, then the first part. Repeat in the same chat for each part.

```text
You are helping the secretary of a nonprofit board write minutes. I will paste a meeting transcript in parts. For each part, pull out notes only. Do not write minutes yet.

For each part, list under these headings and leave a heading out if it has nothing.
- Topics discussed, in order, each with two or three plain sentences about what was said and by whom (use the speaker's full name the first time).
- Motions. For each, who moved, who seconded, the exact wording as spoken, and the result (carried, failed, unanimous, or a count). If any of that was not clear, write [unclear] instead of guessing.
- Numbers and dates said out loud, exactly as spoken, each with a few words of context.
- Commitments. Who said they would do what, and by when.
- Unclear or garbled passages I should check, with the first few words so I can find them.

Rules. Never invent a name, number, date, or vote. Skip small talk, jokes, and technical trouble with the video call. Describe people the organization serves in general terms only, with no names or identifying details.

Reply "Ready" and wait for the first part.
```

## Prompt 2. Write the minutes from the notes

Use this in the same chat after the last part, so the model still has the notes. If the chat has become very long, start a new one and paste the notes it gave you first.

```text
Now write the minutes for the meeting using all the notes above.

Meeting details.
- Organization and board name: [org name and board name]
- Date: [meeting date]
- Start and end time: [times]
- Place: [place]
- Board members present: [names, chair first, marked (Chair)]
- Advisory members present: [names, or none]
- Staff present: [names]
- Guests: [names, or none]
- Who called the meeting to order, and was a quorum present: [answer]
- Corrections to the previous minutes, if any: [list, or none]

Follow this style guide exactly:
[paste the whole of minutes-style.md here]

Output format. Plain text with headings written as lines starting with # and ## so I can paste them into Google Docs. Put anything you are unsure about in square brackets. Do not add any content that is not in the notes. Do not add a list of people who were absent.
```

## Prompt 3. Check the minutes against the transcript

Run this in a new chat. Paste the finished minutes, then the whole transcript in parts as before, then the instruction.

```text
Below are draft minutes and the transcript they came from. Check the minutes against the transcript and report problems. Do not rewrite the minutes.

Report these four things as separate lists, and say "none found" when a list is empty.
1. Every name in the minutes. For each one that does not appear in the transcript, or that appears spelled differently, show both spellings.
2. Every number, amount, and date in the minutes. For each one that does not match the transcript, show what the minutes say and what the transcript says.
3. Every motion. Compare mover, seconder, wording, and result. Flag any that differ.
4. Anything important said in the transcript, such as a decision, a commitment, a deadline, or a number, that the minutes leave out. Minutes are allowed to be shorter than the transcript, so list only what a board member would want to find later.

Quote the few words from the transcript that prove each point so I can search for them.
```

## Prompt 4. The digest

Minutes are shorter than the meeting by design. The digest (a short, structured record of one meeting) keeps the facts the minutes leave out so they can be found later. Run it in the chat that holds the transcript and the finished minutes.

```text
Write a digest of this meeting from the transcript, comparing it with the final minutes above. It is a navigation aid for the secretary, not a source. Where the digest and the transcript disagree, the transcript wins.

Use exactly these headings.
## Decisions and motions
Each decision with who moved and seconded and the result.
## Numbers, money, and outside parties
Every dollar amount, count, percentage, funder, partner, and vendor named, quoted as spoken with a few words of context. Note when a figure sat in a garbled part of the recording.
## Commitments, deadlines, and follow-ups
Who, what, and by when.
## In the transcript but not in the minutes
A numbered list of every fact above that the final minutes leave out.
## Coverage notes
How the meeting ran in one line, where the transcript quality was poor (with the first few words so I can find the spot), and any place the minutes and transcript seem to disagree.

Rules. Do not invent anything. Leave out names and details that could identify a person the organization serves. Do not tidy up numbers, quote them as heard.
```

Save the digest as a Google Doc in the private transcripts folder, next to the transcript, named with the meeting date.

## Prompt 5. Fill in the email

Paste the email template (email-template.md), then the values.

```text
Fill in this board email template. Keep the structure and the warm, brief tone. Do not add anything I did not give you. Where I left a value blank, delete that line instead of guessing.

Values.
- Organization: [name]
- Meeting date and time: [date, start to end]
- Place: [place]
- Special notes: [anything, or none]
- Reports that did not arrive: [paste the "missing_reports_auto" cell from the Month tab, or none]
- Items for approval: [list, or none]
- Standing link names, in order: [Combined packet, Files folder, and so on]
- Video details: [paste]
- My name: [name]

Write the email as plain text. I will paste the links in myself.
```

## Prompt 6. No recording? Use your own notes

```text
I am the secretary of a nonprofit board and I took typed notes at the meeting. Turn them into minutes. Do not add anything that is not in my notes. Wherever my notes are thin or unclear, put a question in square brackets instead of filling the gap.

Meeting details.
[same list as Prompt 2]

Style guide.
[paste minutes-style.md]

My notes.
[paste]
```

## Adapting these

Change the headings in Prompt 4 to match what your board cares about. A food bank might want "Pounds distributed". A school board might want "Enrollment figures". The prompts are a starting shape, so edit them freely.

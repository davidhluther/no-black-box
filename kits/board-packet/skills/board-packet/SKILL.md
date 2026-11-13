---
name: board-packet
description: Run a nonprofit board's monthly packet from start to finish. Gathers the reports named on the agenda, flags any that did not arrive, writes the prior meeting's minutes from its transcript (a written record of what was said), combines the packet PDF, places files in the right Drive folders, and writes the board email as a Gmail draft that is never sent. Use when the user says "run the [month] board packet", "get the board packet out", or asks what is missing for the next board meeting.
---

# Board Packet (the monthly run)

Works in: Claude Code (full version)

This skill (a folder of written instructions an AI tool follows) runs the whole monthly cycle in order. It hands the specialist jobs to four sibling skills: `transcribe`, `meeting-minutes`, `meeting-digest`, and `packet-pdf`. The free and low-cost versions of this kit do the same cycle by hand or with a Google Sheet. If the user has not set those up, they do not need to. This skill works alone.

## Before you start

1. Read `config.json` in the kit folder (the user's copy of `config.example.json`). If it is missing, ask the user to copy `config.example.json` to `config.json` and fill it in, or ask the questions one at a time and write the file for them. It holds the organization's name, the reports list, the recipients, the folder names, and the email settings. Never put a password or key in it.
2. Read `references/monthly-checklist.md` and `references/email-template.md` in this skill's folder. The user may have edited their own copies. Use theirs if they exist, because standing rules (expected reports, recipients, dates) change in those files, not here.
3. Ask which month to run, unless the user said. The meeting date, the month folder name (built from `folders.month_folder_pattern`), and the prior meeting's date follow from it.

## Standing rules (do not bend)

- The agenda is the master list of what is expected. Flag any active standard report that did not arrive. Never leave one out silently. Reports marked inactive in config are never flagged.
- Minutes written after a meeting go in the following month's folder, locally and in Drive, because that is the packet where the board approves them.
- Reports with `in_combined_packet` set to false (financials, a budget, and so on) are not merged into the combined PDF. Each gets its own named link in the email.
- The email is always created as a draft and never sent. If the only email tool available can send mail and cannot make a draft, do not use it. Write the email to `email-draft.html` and `email-draft.txt` in the month folder and tell the user to paste it into Gmail.
- Everything in the email is a Drive link, never an attachment.
- Transcripts never go in a month folder. Month folders are usually link-shared, so anyone with the link can read them. Transcripts go in the private transcripts folder.
- Before putting any file in a shared folder, tell the user what you are about to put there and get a yes. Files in a link-shared folder are visible to everyone with the link.
- Never invent a report, a name, a number, or a vote.

## How to reach the user's files

Use whichever of these the user has, in this order.

1. A local folder that mirrors Drive, made by Drive for desktop (Google's free app that keeps a normal folder on the computer in step with Drive). Work there. Every file you save syncs by itself.
2. Connectors (tools that let Claude Code read and write one outside service) for Google Drive and Gmail, if the user has added them. Use them to read the month folder, upload files, and create the draft.
3. Neither. Ask the user to drop the files into a local working folder (`folders.local_workspace`). Do the work there, then tell the user exactly which files to upload and where.

Say which route you are using at the start of the run.

## The run

### Step 1. Resolve the month

Set the local working folder to `<local_workspace>/<YYYY-MM>/` (create it if needed). The Drive month folder is `<drive_root_name>/<year>/<month folder name>`. Month folders are normally made ahead of time inside the link-shared year folder, so uploads inherit sharing. Use the existing one. Do not create a second one beside it.

### Step 2. Gather the inputs

Pull each expected report (see `reports` in config) from the month folder, from email, or from the user's drop folder into the working folder. Record which expected reports are missing. That list feeds the email's missing-reports note.

### Step 3. Prior meeting's minutes

- Find the prior meeting's transcript (.txt or .vtt) in the private transcripts folder. If only audio or video exists, run the `transcribe` skill first.
- Run the `meeting-minutes` skill to write the minutes.
- Place the finished minutes in this month's folder.
- Run the `meeting-digest` skill and save the digest (a short record of the facts the minutes leave out) in the private transcripts folder next to the transcript.

### Step 4. Combine the packet

Run the `packet-pdf` skill on the working folder. Order follows `reports` in config, agenda first and the prior meeting's minutes last. Excluded reports are converted to PDF and kept in the folder but left out of the combined file.

### Step 5. Put the files in Drive

After the user says yes, upload the combined packet, the minutes, and any converted PDFs to the month folder. Then check that each file opens by link without signing in. If a link asks for a sign-in, tell the user to fix the sharing, and do not change sharing yourself.

### Step 6. Draft the email

Follow `references/email-template.md` and config: subject pattern, recipients (To the chair, Cc the staff who wrote reports, Bcc (blind carbon copy, so addresses stay hidden) the full board), standing links, the missing-reports note from Step 2, and the recurring ask. Create the Gmail draft. When revising, update the same draft instead of making a second.

### Step 7. Hand off for review

Tell the user what was gathered, what is missing or flagged, where the packet and minutes live, and that the draft is ready for the reviewer named in config. Do not send.

### Step 8. After the user sends it (optional)

If the board keeps a copy of each sent email, save it as a PDF in the month folder without the Bcc list, because the folder is shared.

## If something goes wrong

- A document will not convert to PDF. Close LibreOffice (the free office program used for conversion) if it is open and run again, or ask the user to export the file to PDF themselves.
- A Drive link asks for a sign-in. The month folder is probably outside the link-shared year folder. Move it inside, then test the link again.
- The transcript is missing. Ask the user to put the transcript file in the private transcripts folder. Some video services only produce transcripts on certain plans. A recording plus the `transcribe` skill is the fallback.
- A connector (a permission that lets the tool reach Drive or Gmail) says it needs permission. Ask the user to approve it in the Claude Code settings. Do not try to get around it.
- Run `python3 support/doctor.py board-packet` and ask the user for the support code (a short code naming the step and the problem) it prints if the setup looks broken.

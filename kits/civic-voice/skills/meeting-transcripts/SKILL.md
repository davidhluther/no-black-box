---
name: meeting-transcripts
description: Turn a public meeting video's captions (the words shown on screen, with times) into a clean, timestamped written record of what was said, with links back to the video, a short agenda-time index, and a clear label that it is machine-made and unofficial. Free route copies the video site's own text panel and cleans it with a chat program such as ChatGPT or Claude. Full route documents a free, open-source caption fetcher plus a short program in Python (a programming language) that converts the files. Use when a resident, civic group, or small nonprofit wants to search, quote, or summarize what was said at a council, board, or commission meeting. Neutral and read-only.
---

# Meeting transcripts

Works in: Claude Code (full version) for the script (a small program in a text file that does one job). The free route below works in any web browser plus a free AI model (a program like ChatGPT or Claude that writes in ordinary language).

Many town and county meetings are posted as video, and most video sites make captions (the words shown on a video, with the time each was spoken) automatically. Those captions are text with a time beside each line. This skill (a folder of written instructions an AI program can load for a job) turns them into something you can search, skim, and quote with a link to the exact moment.

## Ground rules

1. **Machine-made, unofficial.** Every transcript (the words of a meeting written out in order) opens with a notice saying so. The adopted minutes (the official written record of a meeting, approved by a later vote) are the record. Where a transcript and the adopted minutes disagree, say so and follow the minutes.
2. **Check before you quote.** Before repeating anyone's words in public, play the video at the timestamp (the hours, minutes, and seconds mark showing when something was said) and confirm. Auto-captions mishear names, numbers, and motions.
3. **Do not guess speakers.** Captions rarely say who is talking. Mark a speaker only when the agenda, the video's on-screen label, or the user tells you. Otherwise write "speaker not identified."
4. **Do not fix words by guessing.** Mark unclear passages "[unclear]." Correct proper names only to the spelling in the agenda or packet, and say you did.
5. **Summaries are not quotes.** Keep summaries in plain words, tied to timestamps, and never put summary words in quotation marks.
6. **Keep the source.** Save the video link, the meeting date, the body, and the date you made the transcript.
7. **Stay neutral.** Summarize what was said, in the order said. No commentary about who is right.

## Read the settings

Read `config.json` for the body names, their video channel or page if the user listed one, and the transcript folder. If missing, ask for the video link, the body, and the meeting date.

## Step 1: Find the video and the agenda

Get the video link from the body's own page or channel. Download the agenda too, since it gives item numbers and the correct spellings of names. If no video is posted, ask the clerk (the staff member who keeps a body's official records) whether recordings are kept and how to request one (see the records-request skill).

## Step 2a: Free route (the platform's own transcript)

1. On a YouTube video, open the description below the video, find "Show transcript" (the wording and place can change), and open it. Turn timestamps on if there is a toggle. Not every video has one; if not, see E13 in the kit's fixes table.
2. Select all of the transcript text, copy it, and paste it into a Google Doc or a text file.
3. Give an AI model the prompt (the message you give an AI model) in `free/prompts.md` ("Clean a pasted transcript"). It keeps the timestamps, joins broken lines into short paragraphs, marks unclear words, and builds the agenda-time index. Paste the agenda in too.
4. Save as `<transcripts folder>/yyyy-mm-dd-<body>-transcript.md` with the notice, the video link, and your name and date as the person who prepared it.

Other sites (Vimeo, Facebook, a town's own video page) may have captions under a similar "transcript" or "CC" menu. If a site has none, the full route may still work (Step 2b), or the clerk may have a recording you can request.

## Step 2b: Full route (yt-dlp and the converter)

yt-dlp (a free, open-source program that fetches caption files from video sites) is a free, open-source program run from a terminal (a window where you type instructions instead of clicking) that can fetch captions (and, if you ask, video) from many sites. Use it only for the text here.

1. Install it. See `references/fetching-captions.md` for the install commands, and run `yt-dlp --version` to check.
2. Fetch captions only, with no video download:
   `yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "en.*" --sub-format vtt -o "%(upload_date)s-%(id)s" "<video link>"`
   This saves one or more `.vtt` caption files in the current folder. Human-made captions, if the uploader provided them, are better than auto-made ones; use them first when both exist.
3. Convert: `python3 -I scripts/captions_to_transcript.py <file>.vtt --title "<Body>, mm/dd/yyyy" --source-url "<video link>" --out transcript.md`.
4. Open the result and check the first and last minutes against the video.
5. Then do Step 3.

## Step 3: Add the index and a summary (optional)

Using the agenda and the transcript, list each agenda item with the timestamp where it starts, and write a short summary of each item (who asked for what, what was decided, as said in the meeting), each point tied to a timestamp. Ask the user which items matter and keep the rest to one line.

## Step 4: Cross-check

Compare any decisions in the transcript with the adopted minutes when they are posted. Record differences in the outcome record (see the public-comment-packet skill).

## What to hand back

The file path, the source video link, which route you used, anything marked unclear, and which passages the user must check before quoting.

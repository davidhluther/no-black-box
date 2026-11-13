---
name: transcribe
description: Turn a meeting recording (audio or video) into a text transcript (a written record of what was said) on the user's own computer using Whisper (a free speech-to-text program), so the recording never leaves their machine. Use when the user has a recording but no transcript and wants minutes. Hands the finished transcript to the meeting-minutes instructions.
---

# Transcribe

Works in: Claude Code (full version)

## Why on your own computer

Board recordings hold unfiltered talk about people and money. Whisper runs locally, so the recording is never uploaded anywhere. It is free and open source.

## What you need

- The recording (.mp3, .m4a, .wav, .ogg, .flac, .aac, .wma, .mp4, .mkv, .webm, .mov, or .avi) and the meeting date.
- Whisper (`pip install openai-whisper`) and ffmpeg, a free audio and video converter. The setup guide BP-FU-01 shows how.

## How to run it

1. Ask for the path to the recording and the meeting date. Read `transcription.whisper_model` and `transcription.language` from `config.json` if it exists. Defaults are `small` and `en`.
2. Choose the folder for the result. Use the month folder for the meeting's month in the local working folder.
3. Show the command first with a dry run, then run it.

```
python3 scripts/transcribe.py --audio <recording> --date YYYY-MM-DD --out-dir <folder> --dry-run
python3 scripts/transcribe.py --audio <recording> --date YYYY-MM-DD --out-dir <folder>
```

The result is `YYYY-MM-DD_board_meeting_transcript.txt`. The script refuses to overwrite an existing transcript of the same name.

4. Copy the transcript into the private transcripts folder (`folders.transcripts_folder_name`). The working copy in the month folder is for the minutes run only. Move it out of any shared folder when the minutes are done.
5. Tell the user where both copies are, about how many words it has, and any quality worries. Offer to run the `meeting-minutes` skill (a folder of written instructions an AI tool follows) next.

## Model choice

- `small` is fast and reliable on an ordinary computer and good enough for meetings. It is the default.
- `medium` is more accurate and three to four times slower. Use it for short recordings, or when `small` gave poor text.
- `large` is the most accurate and usually too slow for a two-hour meeting without a powerful computer.

A two-hour meeting can take from a few minutes to well over an hour, depending on the computer and the model. The script prints a reminder.

## What to know about the result

- The transcript has no speaker names. The `meeting-minutes` skill works out who said what from context and the attendance list, and flags guesses.
- A recording with a long silence at the start can make Whisper repeat itself. The script sets a flag that prevents that.
- Audio-only recordings usually transcribe better than video files.
- If the text is poor, run again with a larger model, or fix the worst passages by hand before writing minutes.

## Safety

The script reads your recording and writes one new text file. It never deletes or changes the recording and never uploads anything.

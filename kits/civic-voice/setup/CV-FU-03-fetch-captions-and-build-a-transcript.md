# CV-FU-03: Fetch Captions and Build a Transcript

Full version, guide 3. You will use [yt-dlp](../glossary.md#yt-dlp) (a free, open-source program you run in the [terminal](../glossary.md#terminal)) to fetch the [captions](../glossary.md#captions) of a public meeting video, then run the kit's [script](../glossary.md#script) to turn them into a timestamped [transcript](../glossary.md#transcript) with links back to the video. Plan 20 minutes. You need [Python](../glossary.md#python) (see [CV-FU-01](CV-FU-01-set-up-claude-code-and-the-skills.md)). The commands fetch text only. They do not download the video. A transcript made this way is machine-made and unofficial. The [adopted minutes](../glossary.md#adopted-minutes) are the record.

1. **CV-FU-03-1.** Install yt-dlp. On a Mac with Homebrew, type `brew install yt-dlp`. Otherwise type `python3 -m pip install -U yt-dlp`. Then type `yt-dlp --version`.
   You'll know it worked when a version number prints. If the terminal says "command not found," it's E18.

2. **CV-FU-03-2.** Make a folder for this meeting and move into it. Type `mkdir meeting-2027-03-09` and press Return, then `cd meeting-2027-03-09`.
   You'll know it worked when your terminal [prompt](../glossary.md#prompt) shows the new folder name.

3. **CV-FU-03-3.** Fetch the captions. Copy the video's address from your browser and replace VIDEO-LINK in this command:
   `yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "en.*" --sub-format vtt -o "%(upload_date)s-%(id)s" "VIDEO-LINK"`
   You'll know it worked when one or more files ending in `.vtt` appear in the folder (type `ls` on a Mac, or `dir` on Windows, to list them). If it says there are no subtitles, it's E19. If it says to sign in to confirm you are not a bot, or shows HTTP 429, it's E20. Do not try to get around it. Use the free route in [CV-FR-05](CV-FR-05-get-a-meeting-transcript.md) instead.

4. **CV-FU-03-4.** Convert a caption file. If there are several, start with the plain `en` one. Type (all on one line; adjust the names):
   `python3 -I /path/to/kit/skills/meeting-transcripts/scripts/captions_to_transcript.py FILE.en.vtt --title "Example Town Planning Board, 03/09/2027" --source-url "VIDEO-LINK" --out transcript.md`
   Replace `/path/to/kit` by dragging the kit folder into the terminal window.
   You'll know it worked when it prints "Wrote transcript.md" and a number of blocks.

5. **CV-FU-03-5.** Open `transcript.md` in any text editor or in Google Docs. It starts with a notice that it is machine-made and unofficial, then shows blocks like "[00:12:30] words..." about every 30 seconds. If you gave a YouTube address, each time is a link to that moment.
   You'll know it worked when the first and last minutes read sensibly. Play the video at three timestamps and compare. If names or numbers are wrong, it's E14.

6. **CV-FU-03-6.** Save it into your "Civic voice/Transcripts" folder as "yyyy-mm-dd-body-transcript," and add a row to your tracker's Transcripts tab. To add an agenda index or a summary, ask [Claude Code](../glossary.md#claude-code), started from the kit folder: "Use the meeting-transcripts [skill](../glossary.md#skill) to add an agenda index and a summary of item 4 to this transcript, with timestamps, using this agenda."
   You'll know it worked when the file is saved and each summary point has a [timestamp](../glossary.md#timestamp). Before you quote anyone, play the video at that moment and confirm the words.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CV-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

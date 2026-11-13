# Fetching captions with yt-dlp

yt-dlp (a free, open-source program that fetches caption files from video sites) is an open-source program you run by typing a command into a terminal (a window where you type instructions instead of clicking). It talks to video sites and can save a video's caption files. This page covers captions (the words shown on a video, with the time each was spoken) only.

## Install

Pick one. Each is a command you type into the terminal and then press Return.

- With Homebrew on a Mac (Homebrew is a free installer for Mac programs): `brew install yt-dlp`
- With Python (a programming language)'s installer: `python3 -m pip install -U yt-dlp`
- On Windows with the package manager built into recent versions: `winget install yt-dlp`

Check it worked by typing `yt-dlp --version`. It prints a version number. If the terminal says "command not found," it's E18 in the fixes table. Sites change often, so update it first when something that worked stops working: `python3 -m pip install -U yt-dlp` (or `brew upgrade yt-dlp`).

## The command

```
yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "en.*" --sub-format vtt -o "%(upload_date)s-%(id)s" "VIDEO-LINK"
```

What each piece does:

- `--skip-download` fetches no video, only what the other options ask for.
- `--write-auto-subs` saves the site's machine-made captions.
- `--write-subs` saves captions a person uploaded, if any.
- `--sub-langs "en.*"` asks for English caption tracks (the pattern also catches variants such as en-US).
- `--sub-format vtt` asks for the common WebVTT caption format.
- `-o "%(upload_date)s-%(id)s"` names the files with the upload date and the video's ID.

If the video has both human-made and machine-made English captions, use the human-made file.

## If it does not work

- "There are no subtitles": the video has no captions. Ask the clerk (the staff member who keeps a body's official records) for the recording or the adopted minutes (E19).
- "Sign in to confirm you're not a bot," or an HTTP 429 error: the site is limiting automated requests. Wait and try later, or use the free route (copy the transcript (the words of a meeting written out in order) from the video page in your browser). Do not try to work around a site's blocks (E20).
- Several files appear: that is normal. Open each one, start with the file whose name ends in ".en.vtt," and check the first minute against the video.

## Manners

Fetch only the meetings you need, one at a time. Keep the video link with every transcript so readers can go back to the source.

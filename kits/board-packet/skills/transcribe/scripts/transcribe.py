#!/usr/bin/env python3
"""Turn a meeting recording into a text transcript on your own computer.

It runs Whisper (a free, open-source speech-to-text program) so the recording
never leaves your machine. This script only builds and runs the Whisper command
for you and gives the result a clear file name.

Needs
  Python 3.9 or newer, the "whisper" command (pip install openai-whisper),
  and ffmpeg (a free audio and video converter).

Usage
  python3 transcribe.py --audio recording.m4a --date 2027-01-21 --out-dir month-folder
  python3 transcribe.py --audio recording.m4a --date 2027-01-21 --out-dir month-folder --dry-run

Result
  <out-dir>/2027-01-21_board_meeting_transcript.txt

The script never deletes or changes your recording and never uploads anything.
"""
import argparse
import datetime
import os
import shutil
import subprocess
import sys
import tempfile

AUDIO_VIDEO = {
    ".mp3", ".m4a", ".wav", ".ogg", ".flac", ".aac", ".wma",
    ".mp4", ".mkv", ".webm", ".mov", ".avi",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audio", required=True, help="path to the recording")
    ap.add_argument("--date", required=True, help="meeting date, YYYY-MM-DD")
    ap.add_argument("--out-dir", required=True, help="folder for the transcript")
    ap.add_argument("--model", default="small", help="small (default), medium, or large")
    ap.add_argument("--language", default="en")
    ap.add_argument("--dry-run", action="store_true", help="show the command, run nothing")
    args = ap.parse_args()

    try:
        datetime.date.fromisoformat(args.date)
    except ValueError:
        print("E35: --date must look like 2027-01-21.")
        return 2
    audio = os.path.abspath(args.audio)
    if not os.path.isfile(audio):
        print("E36: the recording was not found at that path.")
        return 2
    if os.path.splitext(audio)[1].lower() not in AUDIO_VIDEO:
        print("E36: that file type is not an audio or video recording Whisper can read.")
        return 2
    out_dir = os.path.abspath(args.out_dir)
    final = os.path.join(out_dir, f"{args.date}_board_meeting_transcript.txt")

    def whisper_cmd(work_dir):
        return [
            "whisper", audio,
            "--model", args.model,
            "--language", args.language,
            "--output_format", "txt",
            "--output_dir", work_dir,
            # Stops Whisper getting stuck repeating itself after long silences.
            "--condition_on_previous_text", "False",
        ]

    # Whisper writes into a fresh, empty working folder so it can never
    # overwrite a file that already sits in the month folder.
    print("Command:", " ".join(whisper_cmd(os.path.join(out_dir, "<new working folder>"))))
    if args.dry_run:
        print("Dry run only. Nothing was run.")
        return 0

    if not shutil.which("whisper"):
        print("E37: the 'whisper' command is not installed. See the setup guide BP-FU-01.")
        return 1
    if not shutil.which("ffmpeg"):
        print("E38: ffmpeg is not installed. Whisper needs it to read recordings.")
        return 1
    if os.path.exists(final):
        print("E39: a transcript with that name already exists. Move it first so nothing is overwritten.")
        return 1

    os.makedirs(out_dir, exist_ok=True)
    work_dir = tempfile.mkdtemp(prefix=".transcribe-", dir=out_dir)
    print("Working. A two-hour meeting can take 5 to 15 minutes or longer, depending on your computer.")
    subprocess.run(whisper_cmd(work_dir), check=True)
    produced = os.path.join(work_dir, os.path.splitext(os.path.basename(audio))[0] + ".txt")
    if not os.path.exists(produced):
        print(f"E40: Whisper finished but no transcript file appeared. Check {work_dir}.")
        return 1
    try:  # "x" creates the file only if it does not exist, so nothing is ever replaced
        with open(produced, "rb") as src, open(final, "xb") as dst:
            shutil.copyfileobj(src, dst)
    except FileExistsError:
        print(f"E39: a transcript named {os.path.basename(final)} appeared while Whisper ran. "
              f"Nothing was overwritten; the new transcript is in {work_dir}.")
        return 1
    shutil.rmtree(work_dir, ignore_errors=True)
    words = len(open(final, encoding="utf-8", errors="replace").read().split())
    print(f"Saved {final} (about {words} words).")
    print("Next: copy it to your private transcripts folder, never a shared month folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

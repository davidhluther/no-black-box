#!/usr/bin/env python3
"""Turn a caption file (.vtt or .srt) from a public meeting video into a timestamped transcript.

Works in: Claude Code (full version), or any computer with Python 3.9 or newer.
Standard library only. Read-only on your caption file; it writes one Markdown file.

Video sites often make "rolling" captions, where each line shows up two or three times as the
words build up on screen. This script drops those repeats, joins the lines into blocks of
about 30 seconds, and puts a timestamp at the start of each block. If you give it a YouTube
link, each timestamp becomes a link that jumps to that moment, so anyone can check a quote
against the video.

Example
  python3 captions_to_transcript.py meeting.en.vtt --title "Planning board, 03/09/2027" \\
      --source-url "https://www.youtube.com/watch?v=VIDEOID" --out meeting-transcript.md
"""
import argparse
import html
import re
import sys

TS = re.compile(r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})")
ARROW = re.compile(r"^\s*(\S+)\s+-->\s+(\S+)")
TAGS = re.compile(r"<[^>]+>")


def to_seconds(stamp):
    m = TS.fullmatch(stamp.strip())
    if not m:
        return None
    h, mi, s, ms = m.groups()
    return int(h or 0) * 3600 + int(mi) * 60 + int(s) + int(ms) / 1000.0


def parse_cues(text):
    """Return a list of (start_seconds, [lines]) from VTT or SRT text."""
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("﻿")
    cues = []
    for block in re.split(r"\n\s*\n", text):
        lines = block.split("\n")
        for i, line in enumerate(lines):
            m = ARROW.match(line)
            if m:
                start = to_seconds(m.group(1))
                if start is None:
                    break
                body = []
                for raw in lines[i + 1:]:
                    clean = html.unescape(TAGS.sub("", raw)).strip()
                    if clean:
                        body.append(clean)
                cues.append((start, body))
                break
    return cues


def dedupe(cues):
    """Drop repeated lines that rolling captions create. Returns [(start, line)]."""
    out, last = [], None
    for start, body in cues:
        for line in body:
            if line == last:
                continue
            # A line that only extends the previous one ("the budget" then "the budget was") replaces it.
            if out and last and line.startswith(last) and start - out[-1][0] < 8:
                out[-1] = (out[-1][0], line)
            else:
                out.append((start, line))
            last = line
    return out


def clock(seconds):
    s = int(seconds)
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def youtube_id(url):
    if not url:
        return None
    m = re.search(r"(?:v=|youtu\.be/|/live/|/embed/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None


def build_blocks(lines, block_seconds):
    blocks, cur_start, cur = [], None, []
    for start, line in lines:
        change = line.startswith(">>")
        line = line.lstrip(">").strip() if change else line
        if cur_start is None:
            cur_start = start
        elif change or start - cur_start >= block_seconds:
            if cur:
                blocks.append((cur_start, " ".join(cur)))
            cur_start, cur = start, []
        if line:
            cur.append(line)
    if cur:
        blocks.append((cur_start, " ".join(cur)))
    return blocks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("captions", help="a .vtt or .srt caption file")
    ap.add_argument("--title", default="Public meeting")
    ap.add_argument("--source-url", default="", help="link to the video, so readers can check the source")
    ap.add_argument("--block-seconds", type=int, default=30, help="length of each timestamped block")
    ap.add_argument("--out", default=None, help="output file (default: print to the screen)")
    a = ap.parse_args()

    try:
        with open(a.captions, encoding="utf-8", errors="replace") as f:
            raw = f.read()
    except OSError as e:
        sys.exit("Could not read %s: %s" % (a.captions, e))
    cues = parse_cues(raw)
    if not cues:
        sys.exit("No captions found in that file. Is it a .vtt or .srt file? (fix E19)")
    blocks = build_blocks(dedupe(cues), a.block_seconds)
    vid = youtube_id(a.source_url)

    out = ["# %s" % a.title, ""]
    if a.source_url:
        out.append("Video: %s" % a.source_url)
    out += ["",
            "> Machine-made captions turned into text. This is not an official record or minutes. "
            "Names, numbers, and motions can be wrong. Check any quote against the video at the "
            "timestamp before you repeat it.", ""]
    for start, text in blocks:
        stamp = "[%s]" % clock(start)
        if vid:
            stamp = "[%s](https://www.youtube.com/watch?v=%s&t=%ds)" % (clock(start), vid, int(start))
        out.append("%s %s" % (stamp, text))
        out.append("")
    result = "\n".join(out)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(result)
        print("Wrote %s (%d blocks)." % (a.out, len(blocks)))
    else:
        print(result)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Turn finished minutes written in simple text into a Word (.docx) file.

Write the minutes in a plain text file using these few marks.
  # Heading            big heading (bold, 14 point)
  ## Heading           smaller heading (bold, 12 point)
  ::center Some text   a centered line
  - Item               a bullet (use only for true lists)
  **bold**  *italic*   inside any line
  (blank line)         starts a new paragraph

Usage
  python3 build_minutes_docx.py minutes.txt January_21_2027_Board_Meeting_Minutes.docx
  python3 build_minutes_docx.py minutes.txt out.docx --logo logo.png --signature-image sig.png

Needs the python-docx package (pip install python-docx). It reads your text
file and writes one new .docx. It changes nothing else.

Add --signature-image only with the signer's own permission. The image goes on
the line right after a line that starts "Respectfully submitted".
"""
import argparse
import re
import sys

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt
except ImportError:
    print("E41: the python-docx package is not installed. Run: pip install python-docx")
    sys.exit(1)

SPAN = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")


def add_runs(par, text, font):
    for piece in SPAN.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**"):
            run = par.add_run(piece[2:-2]); run.bold = True
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            run = par.add_run(piece[1:-1]); run.italic = True
        else:
            run = par.add_run(piece)
        run.font.name = font
        run.font.size = Pt(12)


def style_heading(par, size, font):
    for run in par.runs:
        run.bold = True
        run.font.name = font
        run.font.size = Pt(size)
        run.font.color.rgb = None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("output")
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--logo", help="optional letterhead image, placed first and centered")
    ap.add_argument("--signature-image", help="optional signature image (get the signer's okay first)")
    args = ap.parse_args()

    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1)
    normal = doc.styles["Normal"]
    normal.font.name = args.font
    normal.font.size = Pt(12)

    if args.logo:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(args.logo, width=Inches(1.4))

    lines = open(args.source, encoding="utf-8").read().splitlines()
    for i, raw in enumerate(lines):
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("## "):
            p = doc.add_paragraph(style="Heading 2"); p.add_run(line[3:])
            style_heading(p, 12, args.font)
        elif line.startswith("# "):
            p = doc.add_paragraph(style="Heading 1"); p.add_run(line[2:])
            style_heading(p, 14, args.font)
        elif line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet"); add_runs(p, line[2:], args.font)
        elif line.startswith("::center "):
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs(p, line[len("::center "):], args.font)
        else:
            p = doc.add_paragraph(); add_runs(p, line, args.font)
        if args.signature_image and line.lower().startswith("respectfully submitted"):
            sp = doc.add_paragraph(); sp.add_run().add_picture(args.signature_image, width=Inches(2.2))

    doc.save(args.output)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()

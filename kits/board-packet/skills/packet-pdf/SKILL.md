---
name: packet-pdf
description: Convert every report in a monthly board packet folder to PDF, put them in the board's standard order, remove blank pages, and merge them into one combined packet PDF. Lists any expected report with no file. Use when the user says to combine, merge, or assemble the board packet, or has dropped reports into a month folder and wants a single printable PDF.
---

# Packet PDF

Works in: Claude Code (full version)

The free and low-cost versions of the kit cannot merge PDFs automatically. Google's Apps Script (a free tool for small programs inside Sheets and Drive) has no built-in way to do it, so those versions use a simple manual merge. The bundled script does it in one step.

## What it does

1. Looks at every file in the month folder. Word, Excel, PowerPoint, image, text, and OpenDocument files are converted to PDF with LibreOffice (a free office program), one at a time (running two conversions at once makes LibreOffice stumble). PDFs are used as they are.
2. Orders the PDFs from the `reports` list in `config.json`, matching each file to a report by the keyword in its filename. Files that match nothing go just before the minutes. The prior meeting's minutes always go last.
3. Leaves out reports whose `in_combined_packet` is false (financials, a budget). They are still converted and kept, so the email can link them.
4. Removes blank pages, because the packet is often printed. A page is blank if it has no text (a bare page number does not count) and no large image. Scanned reports, where each page is one large image, are never stripped.
5. Merges the rest into the file named in `folders.combined_packet_filename`.
6. Lists every active report with no file found, so the email can say so.

## How to run it

Ask which month, or work it out from context. Then:

```
python3 scripts/combine_packet.py --folder <month-folder> --config config.json --dry-run
```

Show the user the planned order and the missing-report list. If they agree, run it again without `--dry-run`. Report the number of files converted, the page order used, where the combined file is, any file that failed (with the reason), and the number of blank pages removed.

## What you need installed

- LibreOffice (free) for non-PDF files. The command is `soffice`.
- pypdf (a free add-on that joins PDFs; install it with `pip install pypdf`) to merge and remove blank pages. Without it the script falls back to the `pdfunite` program if present, and skips blank-page removal.

## If something goes wrong

- LibreOffice is already open and conversion fails. Close it and run again.
- A file is not a supported type. The script skips it and says so. Do not stop the whole batch.
- The folder holds no processable files. Tell the user.
- If a file lands in the wrong place in the order, rename it so its filename holds the right keyword, or fix the keyword in the reports list. Do not hand-edit the combined PDF.

## Safety

The script writes only new PDF files into the month folder. It never edits or deletes the originals and never uploads anything.

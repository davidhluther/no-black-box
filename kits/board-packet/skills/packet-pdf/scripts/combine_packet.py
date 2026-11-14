#!/usr/bin/env python3
"""Turn a month folder of reports into one combined board packet PDF.

What it does
  1. Finds the reports in a month folder.
  2. Converts Word, Excel, PowerPoint, image and similar files to PDF with
     LibreOffice (one at a time).
  3. Puts the PDFs in packet order using the reports list in config.json.
     Unmatched files go just before the minutes. Minutes always go last.
  4. Drops truly blank pages (no text, no image and no drawing on the page)
     and lists every page it removed.
  5. Merges everything into one PDF.
  6. Prints which active reports were not found.

What it never does
  It never edits or deletes your original files. It writes only new PDF files
  into the month folder. It never uploads anything.

Needs
  Python 3.9 or newer, LibreOffice (the command "soffice") for non-PDF files,
  and the pypdf package (pip install pypdf) for merging and blank-page removal.
  If pypdf is missing it falls back to the "pdfunite" program and skips
  blank-page removal.

Usage
  python3 combine_packet.py --folder /path/to/month-folder --config config.json
  python3 combine_packet.py --folder /path/to/month-folder --config config.json --dry-run
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

CONVERTIBLE = {
    ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".rtf",
    ".odt", ".ods", ".odp", ".png", ".jpg", ".jpeg", ".gif", ".tiff", ".bmp",
}


def load_reports(config_path):
    with open(config_path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    reports = cfg.get("reports", [])
    folders = cfg.get("folders", {})
    return reports, folders.get("combined_packet_filename", "board-packet-combined.pdf")


def convert(path, outdir, dry_run):
    """Convert one file to PDF with LibreOffice. Returns the PDF path or None."""
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(path))[0] + ".pdf")
    if os.path.exists(pdf) and os.path.getmtime(pdf) >= os.path.getmtime(path):
        return pdf
    if dry_run:
        print(f"  would convert {os.path.basename(path)}")
        return pdf
    if not shutil.which("soffice"):
        print("  E30: LibreOffice ('soffice') is not installed, so non-PDF files cannot be converted.")
        return None
    try:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", outdir, path],
            check=True, capture_output=True, timeout=300,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"  E31: could not convert {os.path.basename(path)} ({type(exc).__name__}). "
              "Close LibreOffice if it is open and run again.")
        return None
    return pdf if os.path.exists(pdf) else None


def match_report(filename, reports):
    low = filename.lower()
    for rep in sorted(reports, key=lambda r: r.get("order", 0)):
        kw = str(rep.get("filename_keyword", "")).lower()
        if kw and kw in low:
            return rep
    return None


# Content-stream operators that put something visible on the page.
PAINT_OPS = {b"S", b"s", b"f", b"F", b"f*", b"B", b"B*", b"b", b"b*", b"sh", b"Do", b"BI",
             b"INLINE IMAGE"}


def is_blank_page(page):
    """Verified empty: no text (a bare page number does not count), no image of
    any size (a scan or a signature is an image), and no drawing. Anything we
    cannot check counts as not blank, so the page is kept."""
    text = (page.extract_text() or "").strip()
    if text and not (text.isdigit() and len(text) <= 3):
        return False
    try:
        resources = page["/Resources"].get_object() if "/Resources" in page else {}
        xobjects = resources.get("/XObject")
        if xobjects and len(xobjects.get_object()) > 0:
            return False
        contents = page.get_contents()
        if contents is not None:
            for _operands, op in contents.operations:
                if op in PAINT_OPS:
                    return False
    except Exception:
        return False
    return True


def merge_with_pypdf(pdfs, out_path, strip_blank):
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    dropped = []
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for num, page in enumerate(reader.pages, 1):
            if strip_blank and is_blank_page(page):
                dropped.append(f"{os.path.basename(pdf)} page {num}")
                continue
            writer.add_page(page)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return dropped


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--folder", required=True, help="the month folder holding the reports")
    ap.add_argument("--config", required=True, help="your config.json")
    ap.add_argument("--dry-run", action="store_true", help="show the plan, change nothing")
    ap.add_argument("--keep-blank-pages", action="store_true", help="do not remove blank pages")
    args = ap.parse_args()

    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        print(f"E32: folder not found: {folder}")
        return 2
    reports, combined_name = load_reports(args.config)
    combined_path = os.path.join(folder, combined_name)

    print(f"Looking in {folder}")
    names = sorted(
        n for n in os.listdir(folder)
        if not n.startswith(".") and not n.startswith("~$") and n != combined_name
        and os.path.isfile(os.path.join(folder, n))
    )
    pdfs = {}   # path -> True
    for n in names:
        ext = os.path.splitext(n)[1].lower()
        full = os.path.join(folder, n)
        if ext == ".pdf":
            pdfs[full] = True
        elif ext in CONVERTIBLE:
            out = convert(full, folder, args.dry_run)
            if out:
                pdfs[out] = True
        else:
            print(f"  skipped (not a supported type): {n}")

    if not pdfs:
        print("E33: no files to combine were found.")
        return 1

    minutes_orders = [r.get("order", 99) for r in reports if r.get("role") == "minutes"]
    unmatched_order = (min(minutes_orders) - 0.5) if minutes_orders else 98
    in_packet, separate, found_names = [], [], set()
    for path in sorted(pdfs):
        rep = match_report(os.path.basename(path), reports)
        if rep:
            found_names.add(rep["name"])
            (in_packet if rep.get("in_combined_packet", True) else separate).append((rep.get("order", 0), path, rep["name"]))
        else:
            in_packet.append((unmatched_order, path, "(no matching report row)"))
    in_packet.sort(key=lambda t: (t[0], t[1]))

    print("\nPacket order")
    for i, (_, path, label) in enumerate(in_packet, 1):
        print(f"  {i:>2}. {os.path.basename(path)}   [{label}]")
    if separate:
        print("\nKept out of the packet (share each by its own link)")
        for _, path, label in separate:
            print(f"  - {os.path.basename(path)}   [{label}]")

    missing = [r["name"] for r in reports
               if r.get("active", True) and r["name"] not in found_names]
    if missing:
        print("\nActive reports with no file found. Mention them in the email, do not hide them.")
        for m in missing:
            print(f"  - {m}")

    if args.dry_run:
        print("\nDry run only. Nothing was written.")
        return 0

    ordered = [p for _, p, _ in in_packet]
    try:
        import pypdf  # noqa: F401
        dropped = merge_with_pypdf(ordered, combined_path, not args.keep_blank_pages)
        print(f"\nWrote {combined_path}")
        print(f"Blank pages removed: {len(dropped)}")
        for d in dropped:
            print(f"  - {d}  (check it; rerun with --keep-blank-pages to keep every page)")
    except ImportError:
        if shutil.which("pdfunite"):
            subprocess.run(["pdfunite", *ordered, combined_path], check=True)
            print(f"\nWrote {combined_path} (blank pages were not removed because pypdf is not installed)")
        else:
            print("E34: install pypdf (pip install pypdf) or pdfunite to merge PDFs.")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

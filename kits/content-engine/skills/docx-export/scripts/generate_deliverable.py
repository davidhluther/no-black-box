#!/usr/bin/env python3
"""
Deliverable generator
Combines all article outputs into a single Word document.

Reads from the working folder (or the folder you pass as the second argument):
  output/final/final_<slug>.md        the finished article (required)
  output/briefs/brief_<slug>.md       the research brief
  output/linkedin/linkedin_<slug>.md  the LinkedIn drafts
  output/images/<slug>-image-brief.md the hero image brief

Optional settings live in <project-root>/guidelines/DOCX_EXPORT_PARAMS.json:

    {"cover_label": "Example Org content pipeline",
     "mirror_dir": "/absolute/path/to/a/shared/folder"}

No config file (or "mirror_dir": null) means no mirror copy.

Usage: python3 generate_deliverable.py <keyword-slug> [project-root]
Example: python3 generate_deliverable.py best-trail-shoes
"""

import json
import sys
import re
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.section import WD_ORIENT
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("python-docx is not installed. Install it once with:  pip install python-docx")

# Word hyperlink helper. python-docx has no public hyperlink call (python-docx
# issue 74), so build the w:hyperlink node directly. The XML shape comes from the
# OOXML spec and has not changed across python-docx versions.
from docx.oxml import OxmlElement  # noqa: E402


def add_hyperlink(paragraph, url, text=None):
    """Append a clickable link (Word's default blue, single underline) to a paragraph."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rPr.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rPr.append(underline)
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text if text is not None else url
    t.set(qn("xml:space"), "preserve")  # keep spaces in multi-word link text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


# Colors
NAVY = RGBColor(0x1A, 0x2B, 0x4A)
MAROON = RGBColor(0x7B, 0x2D, 0x3F)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_cell_shading(cell, color_hex):
    """Set cell background color."""
    shading = cell._element.get_or_add_tcPr()
    shading_elem = shading.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): color_hex,
    })
    shading.append(shading_elem)


def add_section_header(doc, text, level=0):
    """Add a styled section header."""
    p = doc.add_heading(text, level=level + 1)
    for run in p.runs:
        run.font.color.rgb = NAVY
    return p


def add_divider(doc):
    """Add a thin horizontal rule."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._element.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single',
        qn('w:sz'): '6',
        qn('w:space'): '1',
        qn('w:color'): 'CCCCCC',
    })
    pBdr.append(bottom)
    pPr.append(pBdr)


_INLINE_RE = re.compile(
    r'\[(?P<anchor>[^\]]+)\]\((?P<url>[^)]+)\)'   # [anchor](url)
    r'|\*\*(?P<bold>.+?)\*\*'                       # **bold**
    r'|\*(?P<italic>[^*]+?)\*'                      # *italic*
)


def _render_inline(p, text):
    """Render inline markdown (links, bold, italic) into paragraph p.

    Single-pass finditer. This deliberately replaces an earlier re.split-based
    walker whose multi-group pattern double-emitted the inner capture group as
    plain text (e.g. '**bold**bold'). finditer never sees the subgroups as
    separate tokens, so each span is emitted exactly once.
    """
    pos = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            plain = text[pos:m.start()]
            if plain:
                run = p.add_run(plain)
                run.font.size = Pt(10)
                run.font.color.rgb = DARK_GRAY
        if m.group('anchor') is not None:
            add_hyperlink(p, m.group('url'), text=m.group('anchor'))
        elif m.group('bold') is not None:
            run = p.add_run(m.group('bold'))
            run.font.size = Pt(10)
            run.bold = True
            run.font.color.rgb = DARK_GRAY
        elif m.group('italic') is not None:
            run = p.add_run(m.group('italic'))
            run.font.size = Pt(10)
            run.italic = True
            run.font.color.rgb = DARK_GRAY
        pos = m.end()
    if pos < len(text):
        plain = text[pos:]
        if plain:
            run = p.add_run(plain)
            run.font.size = Pt(10)
            run.font.color.rgb = DARK_GRAY


def markdown_to_docx(doc, markdown_text):
    """Convert markdown text to Word document elements."""
    lines = markdown_text.split('\n')
    in_table = False
    table_rows = []
    in_code_block = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            i += 1
            continue
        if in_code_block:
            p = doc.add_paragraph(line)
            p.style = 'No Spacing'
            for run in p.runs:
                run.font.name = 'Courier New'
                run.font.size = Pt(9)
            i += 1
            continue

        # Tables
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # Skip separator rows
            if cells and all(set(c.strip()) <= set('-: ') for c in cells):
                i += 1
                continue
            table_rows.append(cells)
            # Check if next line is still table
            if i + 1 >= len(lines) or '|' not in lines[i + 1] or not lines[i + 1].strip().startswith('|'):
                # End of table - render it
                if table_rows:
                    num_cols = max(len(r) for r in table_rows)
                    table = doc.add_table(rows=len(table_rows), cols=num_cols)
                    table.style = 'Light Grid Accent 1'
                    for row_idx, row_data in enumerate(table_rows):
                        for col_idx, cell_text in enumerate(row_data):
                            if col_idx < num_cols:
                                cell = table.cell(row_idx, col_idx)
                                cell.text = cell_text.replace('**', '')
                                for paragraph in cell.paragraphs:
                                    paragraph.paragraph_format.space_after = Pt(2)
                                    for run in paragraph.runs:
                                        run.font.size = Pt(9)
                                        if row_idx == 0:
                                            run.bold = True
                    doc.add_paragraph()  # spacing after table
                in_table = False
                table_rows = []
            i += 1
            continue

        stripped = line.strip()

        # Empty lines
        if not stripped:
            i += 1
            continue

        # Headings
        if stripped.startswith('# ') and not stripped.startswith('## '):
            add_section_header(doc, stripped[2:], level=0)
            i += 1
            continue
        if stripped.startswith('## '):
            add_section_header(doc, stripped[3:], level=1)
            i += 1
            continue
        if stripped.startswith('### '):
            add_section_header(doc, stripped[4:], level=2)
            i += 1
            continue
        if stripped.startswith('#### '):
            p = doc.add_paragraph(stripped[5:])
            p.style = 'Heading 4'
            i += 1
            continue

        # Bullet points — render inline bold/links instead of stripping them
        if stripped.startswith('- ') or stripped.startswith('* '):
            text = stripped[2:]
            p = doc.add_paragraph(style='List Bullet')
            _render_inline(p, text)
            i += 1
            continue

        # Numbered items — render inline bold/links instead of stripping them
        if re.match(r'^\d+[\.\)]\s', stripped):
            text = re.sub(r'^\d+[\.\)]\s', '', stripped)
            p = doc.add_paragraph(style='List Number')
            _render_inline(p, text)
            i += 1
            continue

        # Key Takeaways box detection
        if 'key takeaway' in stripped.lower():
            # Semantic Heading 3 style so Contentful imports this as a proper
            # heading rather than body text (manual bold + font size landed as
            # body text in the CMS importer).
            p = doc.add_paragraph('Key Takeaways', style='Heading 3')
            for run in p.runs:
                run.font.color.rgb = NAVY
            # Collect following bullets
            i += 1
            while i < len(lines):
                bline = lines[i].strip()
                if bline.startswith('- ') or bline.startswith('* ') or bline.startswith('• '):
                    text = re.sub(r'^[-*•]\s*', '', bline)
                    bp = doc.add_paragraph(style='List Bullet')
                    _render_inline(bp, text)
                elif bline == '':
                    i += 1
                    break
                else:
                    break
                i += 1
            add_divider(doc)
            continue

        # Regular paragraph — inline links, bold, and italic via the single-pass
        # renderer (see _render_inline). The previous re.split walker is gone;
        # it double-emitted bold text as plain text.
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        _render_inline(p, stripped)

        i += 1


def read_file_safe(path):
    """Read a file, return content or None if not found."""
    p = Path(path)
    if p.exists():
        return p.read_text(encoding='utf-8')
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_deliverable.py <keyword-slug> [project-root]")
        print("Example: python3 generate_deliverable.py best-commercial-card")
        sys.exit(1)

    slug = sys.argv[1]
    root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('.')

    # Load per-repo brand params (cover label, mirror folder) from
    # <project-root>/guidelines/DOCX_EXPORT_PARAMS.json. Loaded once, early,
    # so both the cover page and the end-of-run mirror step can read it.
    # No config file = default cover label, no mirror.
    brand_params = {}
    params_path = root / "guidelines" / "DOCX_EXPORT_PARAMS.json"
    if params_path.is_file():
        try:
            with open(params_path, encoding="utf-8") as f:
                brand_params = json.load(f)
        except (OSError, ValueError) as exc:
            print(f"WARN: could not read {params_path} ({exc}); using defaults.")

    # Find source files
    brief = read_file_safe(root / f'output/briefs/brief_{slug}.md')
    final = read_file_safe(root / f'output/final/final_{slug}.md')
    linkedin = read_file_safe(root / f'output/linkedin/linkedin_{slug}.md')
    image_brief = read_file_safe(root / f'output/images/{slug}-image-brief.md')

    if not final:
        print(f"ERROR: No final article found at output/final/final_{slug}.md")
        sys.exit(1)

    # Create document
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(10)
    font.color.rgb = DARK_GRAY

    # Set narrow margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # --- COVER PAGE ---
    doc.add_paragraph()  # spacing
    doc.add_paragraph()
    doc.add_paragraph()
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_p.add_run(slug.replace('-', ' ').title())
    run.font.size = Pt(28)
    run.bold = True
    run.font.color.rgb = NAVY

    subtitle_p = doc.add_paragraph()
    subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle_p.add_run('Content Deliverable Package')
    run.font.size = Pt(14)
    run.font.color.rgb = MAROON

    brand_p = doc.add_paragraph()
    brand_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = brand_p.add_run(brand_params.get('cover_label', 'Content pipeline'))
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY

    doc.add_page_break()

    # --- SECTION 1: FINAL ARTICLE ---
    add_section_header(doc, 'Section 1: Final Article', level=0)
    add_divider(doc)
    if final:
        markdown_to_docx(doc, final)
    else:
        doc.add_paragraph('Final article not available.')
    doc.add_page_break()

    # --- SECTION 2: LINKEDIN CONTENT ---
    add_section_header(doc, 'Section 2: LinkedIn Content', level=0)
    add_divider(doc)
    if linkedin:
        markdown_to_docx(doc, linkedin)
    else:
        doc.add_paragraph('LinkedIn content not yet generated.')
    doc.add_page_break()

    # --- SECTION 3: IMAGE & DESIGN BRIEF ---
    add_section_header(doc, 'Section 3: Image & Design Brief', level=0)
    add_divider(doc)
    if image_brief:
        markdown_to_docx(doc, image_brief)
    else:
        doc.add_paragraph('Image brief not yet generated.')

    # Also look for infographic briefs
    infographic_files = sorted((root / 'output/images').glob(f'{slug}-infographic-*-design-brief.md'))
    if infographic_files:
        doc.add_page_break()
        add_section_header(doc, 'Infographic Design Briefs', level=1)
        for inf_file in infographic_files:
            content = inf_file.read_text(encoding='utf-8')
            markdown_to_docx(doc, content)
            add_divider(doc)

    doc.add_page_break()

    # --- SECTION 4: CONTENT BRIEF ---
    add_section_header(doc, 'Section 4: Research Brief', level=0)
    add_divider(doc)
    if brief:
        markdown_to_docx(doc, brief)
    else:
        doc.add_paragraph('Research brief not available.')

    # Save to project output directory
    output_path = root / f'output/docs/{slug}-deliverable.docx'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f"Deliverable saved: {output_path}")

    # Optional mirror to a shared library folder (for example a synced cloud
    # folder), configured in
    # <project-root>/guidelines/DOCX_EXPORT_PARAMS.json -> "mirror_dir".
    # The destination may be offline (for example a cloud folder that is signed out); a
    # failed copy logs a warning and does not fail the script — the local copy
    # is the source of truth. No config file = no mirror.
    # (brand_params was loaded earlier, alongside cover_label.)
    mirror_dir = brand_params.get("mirror_dir")
    if mirror_dir:
        import shutil
        mirror_dest_dir = Path(mirror_dir)
        try:
            if mirror_dest_dir.exists():
                mirror_path = mirror_dest_dir / output_path.name
                shutil.copy2(str(output_path), str(mirror_path))
                print(f"Mirror copy saved: {mirror_path}")
            else:
                print(
                    f"WARN: mirror destination not found ({mirror_dest_dir}). "
                    "Local copy was saved; mirror copy was skipped. "
                    "Sign in to the shared library or verify the path, then re-run if needed."
                )
        except (OSError, PermissionError) as exc:
            print(f"WARN: mirror copy failed ({type(exc).__name__}: {exc}). Local copy is unaffected.")

    # Report what was included
    sections = []
    if final: sections.append("Final Article")
    if linkedin: sections.append("LinkedIn Content")
    if image_brief: sections.append("Image Brief")
    if infographic_files: sections.append(f"{len(infographic_files)} Infographic Brief(s)")
    if brief: sections.append("Research Brief")
    print(f"Sections included: {', '.join(sections)}")

    missing = []
    if not final: missing.append("Final Article")
    if not linkedin: missing.append("LinkedIn Content")
    if not image_brief: missing.append("Image Brief")
    if not brief: missing.append("Research Brief")
    if missing:
        print(f"Sections missing: {', '.join(missing)}")


if __name__ == '__main__':
    main()

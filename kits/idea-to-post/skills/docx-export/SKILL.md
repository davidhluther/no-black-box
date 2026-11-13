---
name: docx-export
description: Package everything made for one article (the final text, the LinkedIn drafts, the image briefs and the research brief) into one styled Word document. Use when asked to export, create a Word doc, make a deliverable, or package article outputs for someone who reviews in Word.
---

# Word export

Works in: Claude Code (full version). It runs a Python script; install its one add-on once with `pip install python-docx`.

Many reviewers want one file they can open in Word, comment on and forward. This skill makes it from the folders the other skills already filled.

## Step 1: pick the article

The article is named by its slug, the short web name used in every output file (for example `best-trail-shoes` or `what-is-a-board-packet`).

## Step 2: run the script

```bash
python3 scripts/generate_deliverable.py my-topic
```

Pass a second argument to run it from another folder: `python3 scripts/generate_deliverable.py my-topic path/to/project`.

The script reads:

- `output/final/final_my-topic.md` (required)
- `output/linkedin/linkedin_my-topic.md`
- `output/images/my-topic-image-brief.md` and the infographic briefs in the same folder
- `output/briefs/brief_my-topic.md`

It combines them into one styled document, saves `output/docs/my-topic-deliverable.docx`, and reports which sections it included and which were missing. Bold text and links inside bullets and numbered lists carry over.

## Optional settings

Create `guidelines/DOCX_EXPORT_PARAMS.json` in the project folder:

```json
{"cover_label": "Example Org content pipeline", "mirror_dir": "/path/to/a/shared/folder"}
```

`cover_label` is the line on the cover page. `mirror_dir` is a second place to copy the finished file, for example a synced cloud folder your reviewers open. If that folder is offline or signed out, the script warns and carries on: the copy in `output/docs/` is the one to trust. With no file, the cover reads "Content pipeline" and no copy is made.

## Step 3: report

Say where the file landed, which sections it holds, and which were missing. If a mirror copy was skipped, say so. For missing sections, name which skill makes them.

## Notes

- Use the script as it is. It makes one consolidated document on purpose, so do not split sections into separate files.
- If the script says `python-docx is not installed`, run `pip install python-docx` and try again.

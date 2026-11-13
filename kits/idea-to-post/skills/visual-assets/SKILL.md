---
name: visual-assets
description: Produce the pictures for a batch of articles (a hero image, a data chart, a step diagram) with alt text, a caption, a source line and a placement, tracked in one spreadsheet-style file per batch. Charts and diagrams are drawn from code so every printed number matches the article word for word. Use when several posts need images before they go to your website system.
---

# Visual assets for a batch of articles

Works in: Claude Code (full version). It runs Python scripts that draw charts and diagrams; install the drawing library once with `pip install matplotlib`.

Brand values (colors, fonts, the list of things that get an image held back) come from a JSON file you keep, passed with `--params`. Never write brand values into this skill's files. A starter file:

```json
{
  "palette": {"emph": "#1F5FAD", "base": "#8A8A8A", "text": "#1A1A1A", "muted": "#666666", "bg": "#FFFFFF"},
  "font_preference": ["Helvetica Neue", "Arial"],
  "domain_mark": "example.org",
  "hero_holds": ["baked-in headlines", "made-up company names", "ranking labels", "another organization's logo"],
  "hero_reviewer_notes_not_holds": []
}
```

## The contract

One tracking file per batch (`assets.csv`), one row per asset, keyed by each article's `slug` (its short web name). The columns and the life cycle of a row (`briefed`, `generated`, `qa-pass` or `qa-hold`, `approved`, `uploaded`, `published`, and `stale`) are in `contract.md` beside this file. The person producing images moves rows from `briefed` to `approved`. The person publishing owns `uploaded` and `published`.

## Rules that came from real failures

1. **Generate from stable finals only.** A final exists, the article checker reports zero errors, and the file has not changed for five minutes (`scripts/check_stable.py <slug>`). Record the first 16 characters of the final's SHA-256 fingerprint on the row. If the fingerprint later changes, the asset is `stale`. Writers keep polishing after a check passes, so re-check before approval: a hero stays valid while the H1 and H2s are unchanged, and a chart stays valid while every figure it prints still appears word for word in the final.
2. **Never let an image model print data.** One emphasized bar in the accent color with the rest neutral is the default for a single series. Draw charts from code (`scripts/render_chart.py spec.json --params your-params.json`) using only figures from the brief's fact list, and give each figure as a display string so the check is a text match against the final. Draw diagrams (`scripts/render_diagram.py`) with step text copied word for word from the final. Generated images garble numbers, invent company names and bake in slogans, and in a large first run a meaningful share were held for exactly those defects.
3. **Add an inline visual only when it shows something the prose and tables do not.** A picture of a table the article already has is less accessible and less searchable than the table. Zero inline visuals is a normal outcome, and planned diagrams get dropped when the final already lists the same steps.
4. **Heroes come from your hero generator** (see the `hero-image` skill). Keep the untouched output as the master and deliver the crop.
5. **Check every hero against your hold list** before approval. Reviewer-note classes you have accepted ship with a note instead of a hold.
6. **Alt text** is 125 characters or fewer and says what is shown; for a chart, the takeaway and the extremes. **Captions** are one plain sentence. **Source lines** follow `Source: <org>, <year> <title> (<data year> data).` and are printed in the image and repeated in your website system.
7. **Placement** is `after_section:<exact heading text>`. Check that your website system supports embedded images before promising inline placement; heroes must never wait on it.
8. **Review on a phone.** Deliver each batch as one page with the images embedded, plus slug, alt text, caption and state.

## Steps

1. Read the batch's article list and each article's brief. Write an asset brief for each: the hero style to expect, its hold risks, and any inline visual with its anchor, facts and draft alt text and caption.
2. Create `assets.csv` with every row at `briefed`.
3. When `check_stable.py` passes for a slug, make the hero, render any inline visuals, fill in alt text, caption and source line from the final, and set the row to `generated`.
4. Review each row, then mark it `qa-pass` or `qa-hold` with the reason. Approved rows go to whoever publishes.
5. Publish the review page again to the same address after each batch, so people keep one link.

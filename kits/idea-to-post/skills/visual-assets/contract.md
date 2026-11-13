# Asset contract schema

One sidecar CSV per batch (`assets.csv`), one row per asset, keyed by the batch manifest's `slug`. Brand-specific values (generator names, delivery sizes, CMS fields) come from your own `guidelines/VISUAL_ASSETS_PARAMS.json`; the values in the table below are sensible defaults.

## Columns

| Column | Meaning |
|---|---|
| `slug` | Manifest slug |
| `asset_id` | `<slug>-hero` or `<slug>-fig1` |
| `asset_type` | `hero`, `data-chart` or `diagram` |
| `required` | `yes` for the hero; `no` for inline visuals (the article ships without them) |
| `generator` | The tool that made it: your hero generator's name, `render_chart.py` (data chart from checked figures) or `render_diagram.py` (diagram from the final's own steps) |
| `source_final_sha256_16` | First 16 hex of SHA-256 of `output/final/final_<slug>.md` at generation time. Blank until generated |
| `master_path` | Untouched generator output (hero 1200x630 PNG; inline 1600 px wide PNG) |
| `file_path` | Delivery file. Hero: `hero_<slug>.jpg`, 1200x600 sRGB JPEG under 800 KB. Inline: `fig_<slug>-1.png`, 1600 px wide, under 500 KB, rendered at 2x for an 800 px column |
| `alt` | 125 characters or fewer. Says what the image shows; for a chart, the takeaway and the extremes. Never "image of" |
| `caption` | Inline only, one plain sentence in sentence case, no "Label:" opener. Heroes carry no caption |
| `source_line` | Inline data charts only, printed in the image and repeated in the CMS: `Source: <org>, <year> <title> (<data year> data).` |
| `credit` | Who made it, for your records. Internal only, never rendered |
| `cms_target` | Where it goes in your CMS: the thumbnail field for heroes, an embedded-image block for inline visuals |
| `placement_anchor` | Hero: `thumbnail`. Inline: `after_section:<exact heading text>`, meaning the last block before the next H2 or H3 |
| `claims_used` | Fact-list item numbers from the brief that the visual prints, such as `AFP-2` |
| `state` | See lifecycle |
| `qa_notes` | Why a row is held, or reviewer notes that ship with it |
| `updated` | Last state change, with your time zone |

## Lifecycle

`briefed` -> `generated` -> `qa-pass` or `qa-hold` -> `approved` -> `uploaded` -> `published`. `stale` replaces any state before `uploaded` when the final's hash no longer matches `source_final_sha256_16`; the asset is regenerated or re-checked.

Approval is the producer's QA pass against the hold list in your params file (`hero_holds`); notes in `hero_reviewer_notes_not_holds` ship with a note instead of a hold. Inline visuals also need every printed number to match the final word for word.

# org.example.json: key reference

Copy `org.example.json` to `orgs/<slug>.json` and edit. JSON has no comments, so every key is documented here. Top-level keys that start with an underscore are ignored. Paths expand `~`. Everything under `paths` is relative to `paths.data_dir` unless noted. Prose strings are inserted as plain text (the page escapes `&`, `<` and `>`).

## Required

| Key | Meaning |
|---|---|
| `org.name` | Short name used in headers and column titles ("ECT relationship", "ECT angle"). |
| `org.full_name` | Full legal or display name, used in the default workbook title. |
| `paths.data_dir` | Folder holding the CSVs, START-HERE.md and dossiers (the organization's own repo, not shared-skills). |

## Identity and guards

| Key | Meaning |
|---|---|
| `exclude_names` | Names that must never appear in output (another organization, say). The workbook and page builders refuse to write if any appears, the link resolver drops matching links and the sweep drops matching titles. Case-insensitive. |
| `plugin` | Optional path to a Python file (relative to the config) defining `extra_links(row, key, links, ctx)`, called per row after the data-driven rules. Return the link list. Use only for rules that data cannot express. |

## Paths

| Key | Default | Meaning |
|---|---|---|
| `paths.xlsx_out` | none | Workbook file name (builder requires it). |
| `paths.html_out` | none | Page file name (builder requires it). |
| `paths.pipeline_csv` | `pipeline-rows.csv` | One row per ask. |
| `paths.intel_csv` | `funder-intel.csv` | One row per funding stream. |
| `paths.wider_net_csv` | `wider-net.csv` | One row per non-local source. |
| `paths.dossier_index_csv` | `dossier-index.csv` | One row per prospect. |
| `paths.start_here` | `START-HERE.md` | Page intro and sections (first line is the title, text before the first `## ` is the intro). |
| `paths.links_json` | `links.json` | Optional Drive links for the page header (`sheet`, `doc`, `note`, `folder`). |
| `paths.research_urls` | `research-urls.json` | Research slug to Doc URL. Optional. |
| `paths.dossier_urls` | `dossier-urls.json` | Dossier slug to Doc URL. Optional. |
| `paths.dossiers_dir` | `funder-dossiers` | Markdown dossiers with front matter (`funder`, `priority_tier`, `status`, `city_state`). |
| `paths.research_dir` | `research` | Research Markdown; headings plus `Source:` lines feed wider-net URL matching. |
| `paths.sweep_dir` | `sweep` | Sweep outputs (`candidates.csv`, `runs.jsonl`, `grantsgov-cache.json`). |
| `paths.drive_map_glob` | none | Absolute glob for the Drive map, a JSON list of `[path, id, mime, url]`. The newest by name wins. Omit for no Drive. Keep it gitignored when it lists applicant names. |
| `paths.url_overrides` | none | JSON file (relative to the config) with `funder_urls` and `wide_urls` maps of funder name to official URL. An empty string means "no URL". |

## Statuses and stages

| Key | Meaning |
|---|---|
| `statuses` | Ordered list of `{name, role, class}`. `role` drives the Dashboard formulas and page counts: `prospect`, `loi`, `submitted`, `pending`, `awarded`, `awarded_reduced`, `declined`, `not_pursued`, `unknown`, `closed`. `class` (`open`, `won`, `lost`, `unknown`) sets the page color and filter. Omit to use the ten defaults. |
| `stages` | Wider-net stage labels in button order. Stages found in the CSV but not listed are appended. |
| `dossier_tiers` | `order` (tier letters, sort order) and `default` (tier selected on load, or `all`). |
| `tiers` | `t1_min` and `t2_min` request-size cutoffs and the three tier `names` used on the Dashboard. |

## Theme

| Key | Meaning |
|---|---|
| `theme.xlsx` | ARGB colors: `head` (header fill), `title`, `sub`, `link`, `blue` (assumption text), `calc` (formula fill), `input` (score-input fill), `confirm` (unconfirmed fill). |
| `theme.page.light`, `theme.page.dark` | Page color tokens: `bg`, `panel`, `fg`, `muted`, `rule`, `accent`, `won`, `lost`, `unknown`, `open`. |
| `theme.page.display`, `theme.page.body` | CSS font stacks. |
| `theme.page.fonts_url` | Google Fonts stylesheet URL, or empty for none. |

## Prose

| Key | Meaning |
|---|---|
| `text.xlsx.pipeline_title`, `pipeline_sub` | Pipeline tab title and subtitle. |
| `text.xlsx.confirm_marker` | Notes text that turns the Status cell yellow (default `CONFIRM`). |
| `text.xlsx.rubric` | Scoring & Rubric rows. `null` is a blank row, `{"title": ...}`, `{"h": ...}` and `{"sub": ...}` are headings, a list is a table row (one-item lists merge across). Placeholders `{t1}`, `{t2}`, `{t1m1}` expand to the formatted tier cutoffs. |
| `text.xlsx.dashboard` | `title`, `subtitle`, `notes` (`asks`, `declined`, `unknown`, `win_rate`, `prospects`) and `plan` (`heading`, `planned_label`, `planned_amount`, `planned_note`, `since_label`, `since_date` as `[y, m, d]`, `since_note`). Set `plan` to null to drop that section. |
| `text.xlsx.intel_title`, `intel_sub`, `wider_title`, `wider_sub`, `dossier_title`, `dossier_sub`, `dossier_evidence_header` | Titles and subtitles for the other tabs. |
| `text.page.title`, `h1` | Page title and heading. |
| `text.page.css_comment` | Comment line at the top of the stylesheet. |
| `text.page.stat_labels` | Six labels under the stat figures, in order: asks, awarded, awarded total, no outcome, prospects, prospect dollars. |
| `text.page.wider_intro`, `pipeline_intro`, `foot` | Section intro paragraphs and footer. |
| `text.page.link_labels` | `[key, label]` pairs matched to `links.json` keys. |
| `text.page.status_filters` | `[class, label]` pairs for the pipeline filter buttons; first must be `["all", ...]`. |

## Link resolver (`links`)

| Key | Meaning |
|---|---|
| `links.skip_hosts` | URL substrings never linked (aggregators, spam). |
| `links.minutes` | `name_template` (Drive file name ending, with `{m}`, `{d}`, `{y}`) and `label_template` for board minutes lookups by date or by month. |
| `links.rules` | Ordered list applied to each row's `source` text. Types: `urls` (links in the text), `research_slug` (regex with one group, label template), `research_all` (token that pulls every research Doc), `dossier_slug`, `minutes_phrase` (regex whose group holds dates), `drive_path` (regex whose group is a Drive path fragment), `text_match` (regex plus one action: `url`, `drive_find` with optional `folder_ok`, `funder_url` as a key into `funder_urls`, or `minutes` as a date token). |
| `links.row_rules` | Rules on the row itself: `source_contains`, `name_contains`, `name_contains_any`, then `add_dossier` (`label`, `slug`), `research` (slugs) and `research_all_if_name_contains`. |
| `links.fallback_search_url` | Used when a row has no funder page (default ProPublica nonprofit search). |

## Sweep (`sweep`)

| Key | Meaning |
|---|---|
| `sweep.keywords` | Roadmap stage to Grants.gov search terms. |
| `sweep.good_agencies`, `bad_agencies` | Agency-code prefixes that raise or lower the score. |
| `sweep.positive`, `negative` | Title words (lowercase) that raise or lower the score. |
| `sweep.strong`, `off` | Synopsis phrases (lowercase) that raise or lower the score. |
| `sweep.user_agent` | Sent to Grants.gov; include a contact address. |
| `sweep.grants_gov` | `eligibilities`, `opp_statuses`, `rows`. |
| `sweep.news` | `feeds` (search base URLs, BLOX style), `terms`, `local_paths` (link must contain one), `skip_paths`, `hit_regex` (title filter), `max_age_days`, `query` (RSS query string before the term). |
| `sweep.scoring` | Weights and cutoffs; see the example for every default. |

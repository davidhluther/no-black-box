---
name: design-gate
description: Pre-pull-request design check for any website project. Lays every changed page out in a real browser at phone and desktop widths, in light and dark themes, with collapsed sections opened, and reports big empty gaps, sideways scrolling and sections that render nothing. Then hands the screenshots to a second reviewer who did not build the page, to judge them against the site's own design rules. Use before opening any pull request that touches pages, components, layout or design tokens.
---

# The design gate

Works in: Claude Code (full version). It needs Python, a browser and a local copy of your site running.

Settings: if the kit's `config.json` exists, read the `design_gate` block (site name, local address, reference page, path of the `.design-gate.json` file). Otherwise ask the user for those values.

A page can pass every automated check you own and still look wrong. A spellchecker, a link checker and a build that finishes cleanly all read the page's source. None of them see the page as a visitor does. This skill lays the page out in a real browser, measures what it can measure without taste, and then asks a fresh reviewer to judge the rest.

The rule it protects: **new work must fit the site's design, or change the design on purpose. It never drifts away silently.** A pull request (a proposed change other people can review before it joins the project) either conforms to the design standard or updates the standard in the same change, with the reasoning written down.

## Why a gate, and why two layers

The case that started this: a new page shipped with every mechanical check green. The owner then read it and found nine visual defects. One was a 177 pixel void, a screen and a half of nothing between two blocks. Three competing label styles sat on one page. A figure contradicted its own legend. No linter can search for those. They are facts about a laid-out page.

So the gate has two layers.

- **Layer A, mechanical.** A script that reads pixels. It has no intent to defend, so it is impartial.
- **Layer B, judgment.** A reviewer reads the screenshots against the site's design rules. This reviewer must not be the one who built the page. A builder who has just made a hundred layout choices has tuned their eye to the page they made. The third label style looks fine because they chose it, and the void looks like breathing room because they put it there. That is the ordinary result of having formed the intent, not carelessness. Spawn a subagent (a second Claude instance with its own fresh context) for this pass, or hand the packet to a different session. Give it the screenshots and the design reference, and keep the reasoning behind the change away from it.

A builder who runs the judgment pass on their own page has not run the gate. They have spellchecked their own handwriting.

## When to run it

Before opening any pull request that touches pages, components, layout, design tokens or content templates. A green build is not a substitute.

Scope is the changed routes (page addresses), not the whole site. Work them out from the change:

- A changed page file means that route.
- A changed shared component means every route that uses it, capped at a representative set if that is the whole site.
- A changed token, global stylesheet or layout means the reference page plus every route the rest of the change touches.

## Layer A, mechanical

Run `scripts/design_gate.py`. It takes full-page screenshots of every changed route at every configured width (390 and 1440 pixels by default) in every configured theme (light and dark by default). On any route with collapsible sections it takes a second pass with them open, because a closed section hides exactly the content most likely to be off-style. Before each capture it freezes animation and scrolls the full page so content that appears on scroll has actually appeared. Without that, such content shows up as a gap that no visitor would ever see, and false alarms teach people to ignore the gate.

| Check | Severity | What it means |
|---|---|---|
| `void` | 1 | A band of empty page taller than the ceiling (120 pixels by default) with content above and below. |
| `overflow` | 1 | The page scrolls sideways at that width. Reports the outermost offending elements. |
| `zero-ink-section` | 1 | A section with real area that draws nothing. The finding says whether its text is in the page, because "missing" and "present but invisible" are different bugs. |
| `capture-failed` | 1 | The page could not be laid out at all in that theme and width. |
| `void-near` | 2 | A gap within 90 percent of the ceiling. Worth watching. |
| `void-edge` | 2 | Empty page at the very top or bottom. Off by default, since that is usually breathing room. |
| `page-too-tall` | 2 | Above the height cap, so capture was skipped. |

"Empty" means every pixel in a row is the same color, whatever the color is. Two hundred pixels of solid dark green with nothing in it is as empty as two hundred pixels of white, so the check works unchanged in dark mode. One refinement matters: a thin full-width rule line counts as ink, so a gap, a rule and another gap read as two small gaps and not one big one.

### Exit codes

A skip is never a pass.

| Code | Meaning |
|---|---|
| 0 | Ran and found no severity 1 problem. PASS, or WARN if only severity 2. |
| 1 | Ran and found at least one severity 1 problem. FAIL. |
| 2 | Could not run: no browser, an unreachable address, a bad config, or a target whose fingerprint does not match what you expected. Nothing was measured, or what was measured was not the thing under test. |

Read the exit code, never the last line of the log. A failure branch once nearly got recorded as a green because its message was worded like an opt-out.

### Target fingerprinting

After one real incident, the gate asserts what it connected to. A re-run reported ten severity 1 findings, including the exact gaps a branch had just repaired. The cause was a configured address (127.0.0.1:3000) that another session's development server, running a different copy of the code, happened to own. The fixed copy sat unserved on another port and was never measured. Nothing errored. Most developer machines run several local servers at once, so this is the normal state. The mirror case is worse: a stale server still showing the old, passing build hands a broken change a green.

So before any capture the gate fetches one page and records what answered (address, status, size, a content hash and any build stamp) in `report.json` under `target`. To assert it, set `expect_marker` to a string that must appear in that page's HTML, or pass `--expect-marker`. Prefix the string with `!` to require its absence. A mismatch exits 2 and captures nothing.

The convention: stamp the build's short git hash into a meta tag named `x-build-id` in the page head, so one string is true of exactly one copy of the code. A site with no stamp can point the marker at any text the change makes true (a new heading) or false (a renamed label, using `!`).

Start your own server on your own port, and give the gate the same port. Many dev servers quietly move to the next free port when theirs is taken.

## Layer B, judgment

A reviewer who did not build the page reads every screenshot in `judgment-packet.md` against the site's design reference (its `DESIGN.md` or equivalent) and the configured reference page, the canonical example of a conforming page. Six checks:

1. **Single label grammar.** Every label uses one construction. If some read "Source: X", some "X (source)" and some stand alone, that is three grammars and a finding.
2. **Heading scale.** Every heading is a step on the site's named scale, in order, with none skipped or invented, and no visual heading faked out of a styled paragraph.
3. **Spacing rhythm.** Gaps between blocks come from the site's spacing scale and repeat. Three different section gaps on one page is drift even when each is under the ceiling.
4. **Banned devices.** Read the site's ban list (config key `banlist`) and check the page against it. Any hit is severity 1. The list is append-only: a device the owner has rejected once never comes back.
5. **Theme parity.** Light and dark show the same design, not two visual languages. Compare the two captures of one route side by side.
6. **Self-consistency.** The page must not contradict itself: a legend that disagrees with its figure, a heading that promises a section that is not there, a count in the text that the table below disproves. Mechanical checking cannot reach this class at all, which is the reason this layer exists.

Record findings in `report.json` under `judgment`, in the same shape as mechanical ones. A ban-list hit, a broken theme or a self-contradicting page is severity 1. Drift in grammar, scale or rhythm is severity 2 unless it makes the page unreadable.

## The verdict

- Any severity 1 from either layer: the gate fails and the pull request does not open.
- Severity 2 only: WARN. The request may open, with the warnings in its description so a reviewer sees what was accepted.
- Nothing from either layer: PASS.
- A mechanical pass alone is half a gate. `report.json` ships with `judgment.status` set to `"pending"` so nobody can quote a green that only one layer produced.

If the gate fails because the feature really needs a new pattern, that is not an exemption and not a reason to raise the ceiling. Update the site's design system in the same change, with the reasoning. Changing the standard is allowed. Diverging from it silently is the thing this gate exists to stop.

## Running it

First copy `config/example-site.example.json` to `.design-gate.json` at the root of your site project and edit it (the table below lists every key). Install the requirements once: Python 3, the `playwright`, `pillow` and `numpy` packages, and a Chromium browser (`python3 -m pip install playwright pillow numpy`, then `python3 -m playwright install chromium`).

```bash
# the routes this change touched, on a server you started, proving it is your copy
python3 scripts/design_gate.py \
  --config .design-gate.json \
  --base-url http://127.0.0.1:3100 \
  --routes /pricing,/about \
  --expect-marker "$(git rev-parse --short HEAD)"

# every route in the config, against the config's own address
python3 scripts/design_gate.py --config .design-gate.json

# a static build folder (it picks its own free port, so no collision is possible)
python3 scripts/design_gate.py --config .design-gate.json --serve out/
```

Other flags: `--out DIR`, `--ceiling N`, `--quiet`. The browser is found in this order: the path in `CHROME_PATH` or `PUPPETEER_EXECUTABLE_PATH` if set, then Playwright's own Chromium, then the system Chrome.

### Config keys

| Key | Default | Notes |
|---|---|---|
| `repo` | none | Name, for the report. |
| `base_url` | `http://127.0.0.1:3000` | Dev server, static server or live site. |
| `routes` | `["/"]` | Overridden per change by `--routes`. |
| `reference_page` | none | The canonical conforming page. The fingerprint is taken from it, falling back to the first route. |
| `expect_marker` | `null` | String that must appear in the fingerprint page's HTML. Prefix `!` to require absence. Mismatch exits 2. |
| `design_system` | `[]` | Paths to your design reference files. |
| `banlist` | none | Path (or `file#anchor`) to your banned-devices list. |
| `void_ceiling_px` | `120` | The severity 1 line for gaps. |
| `near_ratio` | `0.9` | Fraction of the ceiling that earns a severity 2 warning. |
| `report_edge_voids` | `false` | Empty page at top or bottom. Noise for most sites. |
| `rule_max_px` | `4` | A uniform band this thin that differs from both neighbors counts as a rule, so as ink. |
| `ink_threshold` | `8` | Per-channel tolerance for "same color". |
| `viewports` | 390 and 1440 | Names, widths and heights. |
| `themes`, `dark_mode` | light and dark, `{"strategy":"media"}` | Use `{"strategy":"localstorage","key":"theme","value":"dark","class":"dark"}` when your site's theme is a stored choice and not the visitor's system setting. |
| `disclosure_selectors` | `["details:not([open])"]` | Collapsed sections to open for the second pass. |
| `expand_aria_toggles` | `false` | Also click `[aria-expanded="false"]` controls. Off by default, since clicking arbitrary toggles can take the browser to another page. |
| `section_selector` | `main section, main > article, main > div[id]` | What counts as a section for the empty-section test. |
| `ignore_selectors` | `[]` | Usually `["nav","header","footer"]`, site furniture with its own style. |
| `force_visible_selectors` | `[]` | Escape hatch for reveal animations the scroll walk misses. |
| `min_section_area_px` | `4000` | Below this a box is too small to accuse. |
| `max_page_height_px` | `30000` | Capture ceiling. |

## Keeping the gate honest

The folder `fixtures/` holds four synthetic pages. `void.html` rebuilds the 177 pixel hole. `overflow.html` has a 900 pixel table with no scroller (it only breaks on a narrow screen, which is why the gate captures more than one width). `ghost-section.html` has a section that is in the page, carries its text and draws nothing. `clean.html` is the control and must produce zero findings. Run the gate against them with `--config config/fixtures.json --serve fixtures/` after any change to the detector, and confirm each page produces exactly the findings its name promises, in both themes at both widths.

The fixtures exist because a gate must never depend on a live site staying broken. The page that motivated this was fixed the same night, so it could only ever prove the pass direction. The fail direction has to be proved against a page broken on purpose.

## What the gate does not do

- It does not read prose. Copy quality belongs to a writing check one layer down.
- It does not check accessibility, tap targets or speed. Use dedicated tools for those. This gate adds to them and replaces none.
- It does not keep a page inventory or sweep the whole site. That is a slower, separate ritual.
- It does not judge whether the design is good. It judges whether this page is the same design as the rest of the site.

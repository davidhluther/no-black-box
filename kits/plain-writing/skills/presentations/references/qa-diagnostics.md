# QA Diagnostics

QA has two layers. Both must pass before delivery.

---

## Layer 1: Message Forensics (Content QA)

Run these diagnostics on the completed deck. These test whether the CONTENT works, independent of visual quality.

| Diagnostic | What You Do |
|------------|------------|
| **Clipboard test** | Have a neutral third party do a silent read. Can they state the 3 Messages you intended? If not, the deck fails. |
| **Silent read** | Read only the headlines in order. Do they tell a coherent story? Do visuals prove the headline claims? Minimal words? |
| **Opposite read** | Read the deck as a skeptic — small company, regulated industry, risk-averse buyer. What do they hear? Fix anything that backfires. |
| **Contradiction scan** | Do claims match the evidence shown on the same slide? Check for typos, geographic errors, data inaccuracies, proper noun spelling. |
| **Logo wall test** | If any slide is a wall of logos, replace with outcome tiles (client, problem, action, result with metric). If logos must stay, segment by relevance. |
| **Industry focus** | Does the deck show depth in 3-5 relevant areas? Breadth without depth signals "we do everything" which installs no Message. |
| **Proof strength** | Rank your proof: Value-based pricing > Pilot offer > Named reference > Plan artifact > Guarantee (weakest). If you're relying on guarantees, find stronger proof. |
| **Tone audit** | Remove filler pride (flags, slogans, growth brags) unless directly functional. Replace with capacity, reliability, and NPS data. |
| **Trim pass** | One Message per slide. Kill anything not in the Message Map. |

### Pre-Flight Checks

- **Squint test (10 seconds):** Look at each slide for 10 seconds. Do the headlines stand alone as your Message?
- **Red team:** Have someone play a skeptical buyer (small account CFO, analytical procurement lead). Ask what they think/feel/believe after reading.
- **Number discipline:** All numbers have units, baselines, ranges, and caveats visible.
- **Geography & names:** Every proper noun verified.

---

## Layer 2: Visual QA

Follow the pptx skill's visual QA process exactly:

### Step 1: Content extraction
```bash
python -m markitdown output.pptx
```
Check for: missing content, wrong slide order, typos, leftover placeholder text.

### Step 2: Visual inspection
```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

### Step 3: Subagent review

Use a subagent (fresh eyes) to inspect every slide image. Look for:

- Overlapping elements (text through shapes, stacked elements)
- Text overflow or cut off at edges
- Elements too close (< 0.3" gaps) or sections nearly touching
- Uneven gaps (large empty area + cramped area on same slide)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned
- Low-contrast text or icons
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content
- Font inconsistency across slides
- Visual motif not carried through consistently

### Step 4: Fix and re-verify

One fix often creates another problem. After fixing:
1. Regenerate PDF and images
2. Re-inspect affected slides
3. Repeat until a full pass finds zero issues

**Do not declare done until both Layer 1 and Layer 2 pass with zero issues.**

---

## Converting Risky Slides

If any of these slide types appear, convert them:

| Risky Slide | Convert To |
|-------------|-----------|
| Logo farm | 4-6 outcome tiles: Client, Problem, Action, Result (metric) |
| "All industries" list | Pattern slide: "In [your industry] we see 3 recurring issues..." + implications |
| Quality claim | QA proof: Show gates, defect trends, customer health metrics |
| Growth brag | Capacity + NPS: "Added 3 pods; maintained NPS 65; on-time 98%" |
| Feature parade | Decision criteria map: each feature tied to a buyer's stated need |
| "No risk" assertion | Risk handling proof: show the process, not the claim |

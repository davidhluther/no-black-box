---
name: funder-research
description: Research grant funders for a small nonprofit and write one sourced dossier per funder. Checks whether the funder is already a past or current funder first, reads the funder's tax filings and its own guidelines, tiers it by fit, and suggests an ask sized from what it really grants. Use when someone asks who might fund their work, to research a named funder, or to build or refresh a funder list.
---

# Funder research

Works in: Claude Code, Claude.ai, ChatGPT for the method and dossiers. The scripts in `scripts/` need Claude Code (or any computer with Python 3) and are optional.

This skill turns "who might fund us?" into a short, sourced file per funder that a person can act on. The method comes from a real search for a small rural nonprofit. Its central idea is to rank funders by what they did fund (their own tax filings) rather than by what their websites say.

Read the organization's name, EIN, service area, programs and known funders from the kit's `config.json` or the tracker's Settings tab. If you don't have them, ask once.

## Standing rules

1. Wide net, human priority. Never drop a funder that could fund the work unless there is a very good reason: dissolved, legally barred, or published guidelines that explicitly exclude this work. Weak evidence means a lower dossier tier and a note for a person to review, never deletion. "No unsolicited proposals," "by invitation only," a religious affiliation or a thin grant history is not a reason to park a funder.
2. Everything learned goes in the dossier with a source URL and the date checked.
3. Existing-funder check first. Before treating anyone as a prospect, search the organization's tracker, past grant reports, board minutes, shared-drive documents and bank or accounting records for the funder's name. Account names often use odd spellings or abbreviations, so try variants. A current or past funder is never a "prospect." Mark it correctly and cite where you found it. Two supposed prospects in the original search turned out to be past funders recorded in only one monthly update.
4. Sources beat research. Where this skill's output disagrees with a grant letter, the books or the minutes, the source document wins.
5. Mark every claim `verified` (seen at the source, with the URL and the date), `secondary` (a directory such as Candid or Instrumentl, labelled as secondary) or `unverified`. Open every funder URL yourself before it goes in. Never guess a web address.

## The dossier

For each funder write `<slug>.md` using `references/dossier-template.md`. Fill the front matter exactly. Sections with nothing found say "Not researched in this pass" instead of disappearing.

Steps per funder:

1. Existing-funder check (rule 3). Record where you looked.
2. Tax-filing data. ProPublica Nonprofit Explorer shows assets, giving and officers for any EIN without a login. For line-level detail, `scripts/fetch_990.py <EIN> --summary` pulls the IRS's own filing. Its web download links sit behind a security check that scripts cannot pass, which is why the script reads the IRS index directly.
3. Guidelines and how to apply, from the funder's own website first. Candid, Instrumentl or GrantStation summaries are a fallback and are labelled secondary. Record the date checked on every source.
4. Fit. Match the funder's stated priorities to one of the organization's programs, using facts from the organization's claims register (see the `grant-drafting` skill). Never invent the organization's numbers.
5. Tier.
   - A: one human-services-type grant of at least a stated floor (for example $5,000) inside the organization's service area, or a current or past funder, or a live application.
   - B: local or relationship funders, or smaller gifts inside the area.
   - C: regional capacity, or giving only to institutions so far. Flag for human review.
   State the geographic condition in tier A in every instruction you write. Earlier agents misread it as "a grant anywhere."
6. Suggested ask: about the 60th percentile of what the funder granted organizations like yours nearby, inside the funder's published range. Say which evidence you used.
7. Public-record names only in the People section. Do not guess at relationships.

## Passes

- Full pass: all steps, for tier A and B funders.
- Light pass, for the long tail of foundations from the tax-filing search: steps 1 and 2, one web search for a website and guidelines, and the grants-in-area evidence copied from the search output and attributed to it. Default tier C, status `prospect`, and a log line "light pass; deepen before any ask". Keep each dossier to about 35 to 50 lines.
- Cold pass, for foundations that fund your cause elsewhere in the state with no known tie to your area: the light pass plus a record of the geography rule (do the published guidelines or grant history limit giving to certain counties?). A funder whose guidelines exclude your area stays in the list with status `parked` and the rule quoted. Dossier tier C by default; dossier tier B if there is any tie to your area (a trustee, an office, a gift under the floor).
- Work in batches of 20 to 30 funders per helper, and run the existing-funder check centrally first. A gift to a regional organization that serves your area counts as a tier B tie.

## Finding funders in bulk

`scripts/mine_990pf.py` builds a candidate list from IRS data for one state: every private grantmaking foundation, then those whose grant lists show money going into your footprint or to your cause elsewhere in the state. Copy `references/footprint.example.json`, fill in your state, towns, ZIP codes and known funders, and run it in a scratch folder (it downloads several gigabytes). Treat the result as leads. The matching is by text, one filing year only, and every candidate needs a human read of its 990-PF.

## Other lanes to research

Seven passes that find money the tax filings miss are in the `grants-pipeline` skill (federal and state programs, national intermediaries, corporate and employer giving, population and heritage lenses, peers' funders, local news, congregations and civic clubs). Use the same verified, secondary, unverified marks.

## Guardrails

- Read-only. Never contact a funder, create an account, or fill a portal form.
- Never try to get past a CAPTCHA. Search slowly: a burst of about 20 searches in a row once tripped one.
- Public data only. Keep donor and applicant names out of anything shared.

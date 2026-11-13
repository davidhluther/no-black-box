---
name: grant-drafting
description: Draft a grant application, letter of inquiry or funder letter in which every fact about the organization traces to a claims register, then check the draft for numbers the register does not support. Use when someone asks to write or tailor a grant draft for a named funder, to build a claims register, or to check a draft before it goes to the board.
---

# Grant drafting

Works in: Claude Code, Claude.ai, ChatGPT for drafting with a claims register pasted in. `scripts/check_draft.py` needs Python 3 (Claude Code or any computer with it); the free kit has a spreadsheet-and-script version of the same check.

A funder's dossier plus a claims register should give a first draft tailored to that funder, with every factual claim traceable to a source. Drafts are drafts. A person edits and submits them. This skill never sends anything to a funder.

## The claims register

The register is the only place a draft may take facts about the organization from. It is a table with these columns: `id`, `claim`, `value`, `as_of`, `source`, `status`. A starting example is in `assets/claims.example.csv`, and `references/claims-register.md` explains how to build one.

Statuses:

| Status | Meaning | May a draft use it? |
|---|---|---|
| source-verified | Read in the organization's own document (cite the page) | Yes |
| external-verified | Read on a named web page on a stated date | Yes, but recheck ratings and staff counts before each submission |
| unverified | The only evidence is a spoken remark, a summary or inference | No |
| conflict | Sources disagree; the claim says which figure to use | Only as the claim directs |
| do-not-use | Known to be wrong or retired | No |

Keep the period with every number ("in fiscal year 2025"). One number per row, so the checker can match it. Where the register and a source document disagree, the source document wins and the register is corrected.

## Rules every draft follows

1. Only claims from the register. If the draft needs a fact the register lacks, add a row with its source first, or leave `[CONFIRM: what is needed, who knows it]`.
2. Claims marked unverified or do-not-use stay out until someone confirms them.
3. Describe the organization's identity (religious, political or otherwise) only in the words its own documents use, and never let the draft affirm a statement the board has not approved. If a funder requires a doctrinal or political statement, stop and flag it for the board.
4. Privacy. No client names, dates of birth, case notes or database records in any draft or in any AI tool. Aggregate numbers only.
5. Plain, warm, specific writing. Name real things. Use each number once, in its most relevant place.
6. Do not claim service in places the organization does not serve.

## Procedure

Follow `references/procedure.md` in order. In short:

1. Read the funder's dossier (see `funder-research`), the claims register, the program descriptions and any boilerplate.
2. Gate. Stop and report, without drafting, if the funder is a current funder and the ask is not a renewal staff asked for, the funder requires something the organization cannot honestly give, the deadline has passed or the channel is invitation-only with no introduction, or staff are already drafting this application.
3. Get the funder's own words fresh from its site the day you draft. Quote its guidelines and form questions. A dossier summary is not a substitute.
4. Compare with the organization's past applications to this funder and recent winning ones to similar funders. Reuse what won; fix what a decline letter said went wrong. If none exist, say so plainly.
5. Choose one program and the ask, bounded by the funder's published range and the size of grants it makes nearby.
6. Outline from the funder's questions, in their order and wording. Note the claim IDs that answer each one.
7. Write. Open with the funder's priority language where it honestly fits. Keep to length limits (with none, a letter of inquiry is one page and a letter application two).
8. Build an alignment table: one row per thing the funder asks for or values (form field, attachment, priority, eligibility rule, length or format rule), with the funder's words, where the draft answers it, and the status.
9. Make the package self-contained: links to the funder's site, guidelines, form and tax filing, the submission address and deadline, every attachment, and the claims appendix.
10. Have a separate reviewer, with no stake in the draft, check it against the funder's documents and the register. It looks for a missed requirement, an unsupported claim, a tone mismatch and anything a program officer would reject on sight.
11. Check mechanically: `python3 scripts/check_draft.py <draft.md> --claims <claims.csv>`. Resolve every flag.
12. Record the draft in the funder's dossier log.

## Draft file layout

Put a cover note for staff at the top (funder, program, ask and its basis, deadline and channel, required attachments, every `[CONFIRM]`). Wrap the text that goes to the funder between `<!-- draft -->` and `<!-- end draft -->`. End with the claim IDs used. Add an `allow:` line for numbers that are not claims (the ask amount, deadlines, the funder's own figures).

# Drafting procedure: dossier to draft

A session that skips step 2 or step 11 is producing guesses, not a draft. The numbering matches `SKILL.md`; this page adds detail.

## 1. Read the inputs

- The funder's dossier: giving priorities in their words, how to apply, required attachments, grants in your area, the tailored angle and open questions.
- The claims register, the program descriptions and the boilerplate (see `claims-register.md`).
- The funder's application form or guidelines, if the dossier links one. The form's questions set the draft's structure, not your boilerplate.

## 2. Gate before writing

Stop and tell the person, without drafting, if any of these hold.

- The dossier status is `awarded`, or the funder is a current funder and the ask is not a renewal staff asked for. A thank-you or stewardship letter is fine.
- The funder requires a statement or eligibility the organization does not have (a county restriction, a tax-status type, a budget cap, a doctrinal statement).
- The deadline has passed, or the channel is invitation-only and no introduction exists.
- Staff are already drafting this application. Offer your draft as support, not as a parallel version.

## 3. Get the funder's own words, fresh

Download the current guidelines, form and FAQ from the funder's site on the day you draft, and quote them. If the funder publishes nothing, say so at the top of the package, list what secondary sources claim, and make "call to confirm" the first step for staff. Read the funder's most recent 990-PF grant list for typical size, purpose wording and whether it funds operating costs or projects. Record the three grants most like your request.

## 4. Compare with what you submitted before

Look for the organization's past applications to this funder (declined ones too) and its recent winning applications to similar funders. Check board notes for what was said about a decline. If nothing is available, the package says so and asks staff for one before submission. Never imply a comparison that did not happen.

## 5. Choose the program and the ask

Match the funder's stated priorities to one program. One program per request unless the funder gives general operating support. Take the ask from the dossier's suggested ask, bounded by the funder's published range and the size of grants it makes nearby, and say which in the cover note.

## 6. Outline from the funder's questions

List the funder's sections or questions in their order and wording. Beside each, note the claim IDs and boilerplate that answer it. If a question needs a fact the register lacks, write `[CONFIRM: what is needed, who knows it]`.

## 7. Write

- Open with the funder's priority language where it fits honestly. Don't paraphrase their mission back at them at length.
- Use each number once, with its period.
- Name the counties or towns the funder cares about, and only those you serve.
- Keep to the funder's length limits.

## 8. Alignment table

| The funder's words (verbatim, with link) | Where the draft answers it | Status (answered, attached, missing, and who supplies it) |
|---|---|---|

A requirement with no row is a requirement you missed.

## 9. Self-contained package

One document a staff member can act on without opening anything else: links to the funder's site, guidelines, form, portal or email and tax filing; the submission address and deadline; every attachment as a link or marked "staff to supply"; the claims appendix with each claim's source; and the alignment table. No local file paths.

## 10. Independent review

A reviewer who did not write the draft checks it against the funder's documents and the register, and tries to find what a program officer would reject. Fix what it finds. List anything unfixed in the cover note.

## 11. Check

1. Run `check_draft.py` and resolve every flag.
2. Reread against the dossier. Does every paragraph answer something this funder asked for?

## 12. Record

Add a log line to the dossier (date, draft location, program, ask). If the draft changes the funder's status, update the dossier front matter and the index in the same edit.

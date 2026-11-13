---
name: records-request
description: Draft a public-records request (sometimes called an open-records, right-to-know, or freedom-of-information request) under the reader's own state law. First walks a state-law lookup so nothing is assumed from memory, then drafts a plain, narrow request for the records, adds a send-and-track log with the response deadline, and drafts follow-ups for no reply, a fee estimate, partial release, or denial. Use when a resident, group, or small nonprofit wants copies of local or state government records. Never sends anything and never gives legal advice.
---

# Records request

Works in: Claude Code (Anthropic's program that runs on your own computer and uses skills), Claude.ai, ChatGPT.

A public-records request (a written ask for copies of records an office already holds) is a written ask for copies of records a government office already holds. This skill (a folder of written instructions an AI program can load for a job) drafts one under your state's law. It does not assume which state you are in, and it never fills in a legal citation or deadline from memory. It makes you look the law up, and it records where you looked.

## Ground rules

1. **Ask for records, not answers.** A request names documents that exist (reports, emails, contracts, maps, meeting recordings, permits). Offices generally are not required to answer questions, explain, or create new documents, though rules differ. Turn questions into "records sufficient to show" requests.
2. **State law first.** Local and state agencies usually answer to the state's own law. The federal Freedom of Information Act covers federal agencies. Do not cite the federal law to a town or county.
3. **No guessing at law.** Citations, deadlines, fee rules, and exemptions come from the lookup step below, from an official source the user can open. If the model is not sure, it says "not verified" and shows what to check.
4. **Neutral and courteous.** No accusations, no arguments, no opinions about the office. A request is a request.
5. **Nothing is sent by the model.** The user reviews, sends, and logs it.
6. **No private data demanded.** Do not ask for personal information about private people (account holder names, health data, children's records, Social Security numbers). If the user needs aggregate or de-identified records, say so in the request.
7. **Not legal advice.** For a denial, an appeal, or a request tied to a lawsuit, point the user to their state's open-government help line, a legal aid group, or a lawyer.

## Read the settings

Read `config.json` for the requester's name, group, state, and records offices. If missing, ask for the state and the agency first.

## Step 1: Who is asking, and what for

Ask:
- Writing as yourself or for a group? The choice changes the signature and tone. Decide before drafting and keep to it.
- Which agency holds the records? (Town clerk (the staff member who keeps a body's official records), county manager, school board, police department, planning office, health department, state agency.) If unsure, draft to the clerk or the agency's records officer and say the agency may route it.
- What do you want to learn, in one sentence? What documents would show that?

## Step 2: State-law lookup (do this before drafting)

Follow `references/state-law-lookup.md`. In short, fill in this table from official sources with a link and date checked for every row:

| Field | What to find |
|---|---|
| Name and citation of the law | |
| Who counts as a public body | |
| Must the request be in writing? Must it cite the law? | |
| Who may ask (residents only, or anyone)? | |
| Response deadline, and what kind of days (business or calendar) | |
| Fee rules (copy costs, staff time, estimates, waivers) | |
| What the office must do if it denies (cite the exemption (a reason in the law that lets an office keep a record back), release the rest) | |
| Appeal or review route | |
| Records with special rules (personnel, investigations, attorney advice, personal data) | |

If any row stays blank, say so in the draft's cover note and tell the user whom to ask (the agency's records officer, the state open-government coalition, or the attorney general's office, as your state has them).

## Step 3: Draft the request

Use `references/request-template.md`. Build it so a busy clerk can fill it without a phone call:

1. Cite the law by its official name and section from the lookup.
2. Number each item. Name the record type, the subject, the office or people it involves by role, and a date range.
3. Prefer electronic copies, and say which formats are fine.
4. Ask for a fee estimate before any charge above an amount the user chooses, and ask whether a waiver is possible if the state's law allows one.
5. Ask for the exemption cited in writing if anything is withheld, and for the rest to be released.
6. Offer to narrow the request, and give a contact for questions.
7. Close with thanks. No threats, no deadlines you invented.

Keep it to one page when you can. Broad requests ("all emails about X") draw delay and cost. Narrow by date range, sender or office, and record type.

## Step 4: Review before sending

Run the checklist in the template: scope is narrow, every item is a record, no private data is requested, tone is neutral, the legal citation matches the lookup, and the requester's contact details are right. List anything the user must decide, such as whether to send as a person or a group.

## Step 5: Send and log

The user sends by a method that leaves a dated record (the agency's online form, email, or certified mail). Log: date sent, method, agency, who received it, the response deadline computed from the lookup (show the count), and a follow-up date. Add the row to the tracker. Calendar the deadline.

## Step 6: Follow-ups

Draft from `references/request-template.md`: acknowledgment check-in, no response by the deadline, fee estimate reply, partial release, and denial (ask for the cited exemption and the appeal steps). Keep each short and courteous.

## Step 7: When records arrive

Save the records unchanged in a dated source folder. Log what was provided and what was not. Record what the office said about anything withheld. Compare to the request item by item. Note that an absence in what you received describes what the office sent, and says nothing about whether other records exist.

## What to hand back

The draft, the filled lookup table with its links and dates, the open decisions, and the dated deadline.

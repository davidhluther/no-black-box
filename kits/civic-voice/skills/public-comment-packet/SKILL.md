---
name: public-comment-packet
description: Get ready for a public meeting and speak at it with facts you can stand behind. Saves the official meeting documents in a dated folder, writes a dated prep memo that ranks items and cites pages, drafts a spoken or written comment with a claims check, lists delivery steps, and records the outcome afterward. Use when a resident, civic group, or small nonprofit wants to prepare for a council, board, commission, or committee meeting. Neutral by design. It never chooses a position for you and never speaks or files anything for you.
---

# Public comment packet

Works in: Claude Code (Anthropic's program that runs on your own computer and uses skills), Claude.ai, ChatGPT.

A five-step routine for showing up prepared at a public meeting: bank the packet, write a dated prep memo, write the comment, deliver it, and record what happened. You choose your position. This skill (a folder of written instructions an AI program can load for a job) helps you read the documents, check your facts, and say what you came to say in the time you get.

## Ground rules (read these first)

1. **Neutral.** Never recommend how to vote, support or oppose, or argue a side unless the user states the position first. Then help them say it clearly and truthfully. Present facts from both the packet and the user's notes without spin.
2. **Source wins.** The official packet, the agenda, and adopted minutes (the official written record of a meeting, approved by a later vote) beat any memo, summary, or memory, including this skill's own output. When a memo and a source disagree, say so and follow the source.
3. **Cite or mark.** Every fact in a memo or comment carries a packet page ("page 12 of 88") or another named source. Anything else is marked "unverified" and kept out of the spoken comment.
4. **Nothing leaves without the user.** Never file, send, post, or sign up on the user's behalf. Drafts are labeled "draft, not filed."
5. **No invented quotes, no guessing at motives.** Describe what documents say and what people did on the record. Do not attribute intent to named people.
6. **Not legal advice.** If an item turns on the law (a rezoning standard, a permit rule, a conflict-of-interest question), name the document that governs and tell the user to confirm with the clerk (the staff member who keeps a body's official records), the attorney for the body, or their own counsel.
7. **Privacy.** Keep personal details of private people (home addresses, phone numbers, health, children) out of memos and comments unless they are already in the public packet and the user needs them.

## Read the settings

Read `config.json` (the user's copy of `config.example.json`) for the speaker's name and group, state, the meeting body and where its agenda and comment rules are posted, and the folder names. If `config.json` is missing, ask the user for those five things and carry on.

## Step 1: Bank the packet

1. Ask which body and which meeting date. Find the official agenda page (from `config.json`, or ask the user for the link). Do not rely on a news story or social post for the agenda.
2. Make a dated folder: `<meetings folder>/yyyy-mm-dd-<body>/source/`. Save the agenda and the full agenda packet (the bundle of reports and drafts a public body posts before a meeting) there unchanged. Add a one-line `source-note.md`: where it came from, the date and time you retrieved it, page count, and whether the text is searchable.
3. If a PDF is a scan (no selectable text), say so. Offer to work from the pages the user pastes in, and mark anything you could not read as "not read."
4. Packets are sometimes updated. Before the meeting, ask the user to check for a newer version, and record the retrieval date each time.
5. Find the comment rules: sign-up deadline, time limit per speaker, whether comment is allowed on agenda items, general comment, or both, and whether written comments are accepted. Record each rule with its source link. If you cannot find a rule, write "not found" and tell the user to ask the clerk. "Not found" describes where you looked and proves nothing.

## Step 2: Write the dated prep memo

Save as `prep-memo-yyyy-mm-dd.md` in the meeting folder. Use `references/prep-memo-template.md`. The shape:

- Header with the body, meeting date, time, place, packet source and retrieval date, memo date, and the sentence "Prep only. Nothing here has been filed, sent, or said on anyone's behalf."
- **What needs attention first.** A ranked table: item, why it is ranked there, and what is the user's call (judgment only they can make) versus background reading.
- **Per item.** What it is in two sentences. The facts that matter, each with a packet page. What staff or the applicant asked for, and whether staff gave a recommendation (say "none given" when none appears). What the governing document sets as the baseline. Questions a listener might ask. What cannot be checked from the packet.
- **The baseline check.** Before suggesting that anyone ask for a condition, a change, or a standard, find out whether the governing ordinance (a local law passed by a governing board), policy, or law already requires it. A request that repeats an existing requirement wastes the user's time at the microphone. If the governing document is not in the folder, say the check is not done.
- **Kind of decision.** Say whether the body is advisory or decides, and whether the item is a general policy decision (usually called legislative (a decision that sets a general rule or policy)) or a decision about one specific property or person that applies set standards to sworn evidence (usually called quasi-judicial (a decision about one property or person that applies set standards to evidence)). The rules about talking to members outside the hearing, and about what counts as evidence, can differ between the two. Tell the user to confirm which applies with the clerk.
- A short "check before you speak" list of figures to re-verify against the packet.

Keep it short enough to read in one sitting. Plain words, no jargon the user has not seen.

## Step 3: Write the comment

Save as `comment-yyyy-mm-dd.md`. Use `references/comment-templates.md`.

1. Ask: speaking as a resident or for a group? Which agenda item, or general comment? What is the time limit? What do you want the body to do or know? Take the user's answer as given.
2. Spoken pace is about 130 words a minute at a calm speed. Write to the time limit minus a margin. Three minutes is about 350 words. Have the user read it aloud with a timer.
3. Structure: name and group, the item, the request in the first or second sentence, two or three facts with sources, one sentence from the user's own experience, the specific ask, thanks. Put the ask first so it lands even if the chair cuts the time.
4. Build a claims table under the draft: claim, source and page, status (verified in packet / verified elsewhere / unverified). Keep only verified claims in the spoken version. Unverified claims go to "ask staff" questions instead.
5. Write a written version for the clerk (if written comments are accepted) and a 30-second version for the case where the time is cut.
6. Check tone: no insults, no claims about private motives, no reading of other people's names with accusations. Stick to the item before the body.

## Step 4: Deliver

Walk the user through this list: sign up by the deadline; arrive early; bring printed copies of the comment and any one-page handout; state name and address only if the rules require it; speak to the chair; stay inside the time. Agree in advance what to do if the meeting runs long or the item moves: send the written version to the clerk the same day and ask how to have it added to the record, since rules differ.

## Step 5: Record the outcome

Within a day, save `outcome-yyyy-mm-dd.md` using `references/outcome-record-template.md`: what happened on each item (motion, vote, conditions, next step and date), whether the comment was delivered or filed, what you would do differently, and whether this record comes from the official minutes or from someone's recollection. Mark recollections "working record, minutes win once adopted." When the minutes are posted, compare and correct. Update the tracker sheet row.

## What to hand back

Say which files you wrote and where, which claims are still unverified, and what only the user can decide. End with the one next action and its date.

# Paste-in prompts for the free version

Use these with any free [AI model](../glossary.md#ai-model) (ChatGPT, Claude, or Gemini). Paste the [prompt](../glossary.md#prompt), then paste your material below it. Replace the brackets first. Everything here is neutral by design: the AI model helps you read, check, and say what you came to say. You choose your position.

Every prompt starts with the same rules block. Keep it.

## Rules block (paste at the top of every prompt)

```
Rules for this task.
1. Stay neutral. Do not recommend how anyone should vote or what position to take. If I state a position, help me state it clearly and truthfully.
2. Use only the material I paste. When you state a fact, give the page or timestamp it came from. If something is not in my material, say "not in the material" and do not fill it in from memory.
3. Never invent a quote, a number, a law citation, or a deadline. If I need a legal citation or deadline, tell me where to look it up instead.
4. Do not guess why any named person acted as they did.
5. Mark anything uncertain as "unverified."
6. You are not giving legal advice.
```

## 1. Prep memo from a meeting packet

```
[Paste the rules block.]

I will paste the text of a public meeting packet. It is [number] pages. Page markers look like [describe, for example "Page 12 of 88"].

Write a prep memo for [me / our group] with these parts.
A. A ranked table of agenda items: rank, item, why it ranks there, and whether the call is mine or just background reading.
B. For each of the top [three] items: what it is in two sentences; a table of facts with the packet page for each; what staff or the applicant asked for, or "none given"; questions to ask that the packet does not answer; things that cannot be checked from the packet.
C. A "check before you speak" list of the figures I should re-verify against the pages.

Do not suggest what I should ask the body to do. Meeting date: [mm/dd/yyyy]. Body: [name].

PACKET TEXT:
[paste]
```

Tip. Packets can be long. Paste one agenda item at a time, with its page numbers, if the chat stops accepting text.

## 2. Check my ask against the governing document

```
[Paste the rules block.]

Below is what I plan to ask for at the meeting, followed by the text of the rule or ordinance that governs this kind of item. For each thing I plan to ask for, tell me whether the document already requires it (give the section), whether it conflicts with something in the document, or whether the document does not cover it. Do not tell me whether I should ask.

MY PLANNED ASKS:
[paste]

GOVERNING DOCUMENT (sections that apply):
[paste]
```

## 3. Write a public comment

```
[Paste the rules block.]

Help me write a public comment. Facts:
- I am speaking as [a resident / a member of group name].
- Agenda item: [number and title]. Time limit: [minutes].
- What I want the body to do or know: [one sentence in my words].
- Facts from the packet I want to use, with pages: [list].
- One sentence from my own experience, in my words: [sentence].

Write (1) a spoken version that fits the time limit at about 130 words a minute, with my ask in the first two sentences; (2) a 30-second version; (3) a written version for the clerk. Then give a claims table with columns: claim, source and page, status (verified in packet / unverified). Move every unverified claim out of the spoken version.
```

## 4. Record the outcome

```
[Paste the rules block.]

Turn my notes into an outcome record. Label the source as "my notes" and say it is a working record until adopted minutes are posted. Sections: item results (item, what happened, vote if reported, conditions or next step, next date); my comment (delivered, written only, or not delivered, and why); what I learned; follow-up checklist.

MY NOTES:
[paste]
```

## 5. Public-records request

Step A is a lookup you do first. The AI model must not fill in the law from memory.

```
[Paste the rules block.]

I live in [state]. I want to request records from [agency]. First, do not draft anything. Tell me which kind of law governs requests to a [town / county / school board / state agency] there (for example, a state public-records law, not the federal one), and give me the exact search words and the kinds of official websites to use to find the law's own text, the response deadline, the fee rules, and the appeal route. Say plainly that you cannot be sure of these from memory and that I must confirm each one on an official page and write down the link and date.
```

Step B, after you have filled in the lookup table from `checklists/records-request-checklist.md`:

```
[Paste the rules block.]

Draft a public-records request using these facts, which I verified at official sources (links and dates in brackets):
- Law and section: [name, section] [link, date].
- Response deadline: [rule] [link, date].
- Fee rules: [summary] [link, date].
- I am writing as [name, group or resident]. Agency: [name]. Date range: [dates].
- What I want to understand, in one sentence: [sentence].
- Records I think would show it: [list].

Rules for the draft: every item must be a record, not a question; each item names a record type, a subject, a role or office, and a date range; ask for electronic copies; ask for a fee estimate before costs above $[amount]; ask for any exemption to be cited in writing and for the rest to be released; offer to narrow it; no private personal data; neutral tone; one page. Then give me the review checklist and flag anything I must decide.
```

## 6. County numbers write-up

```
[Paste the rules block.]

Below is a table of American Community Survey estimates with margins of error. Write one plain sentence per measure that gives the estimate, the margin of error, and the period. Say "an estimated," not "X percent of residents." For each comparison between two places, say they are clearly different only if the gap between the estimates is larger than the square root of the sum of the two squared margins of error. Otherwise say "not clearly different." Flag any number whose margin of error is more than 30 percent of the estimate. End with the source line: U.S. Census Bureau, American Community Survey, [period] 5-year estimates, retrieved [mm/dd/yyyy].

TABLE:
[paste]
```

## 7. Clean a pasted transcript

```
[Paste the rules block.]

Below is a transcript copied from a video site, with timestamps. Also below is the meeting agenda.

Do these things.
1. Keep every timestamp at the start of its paragraph. Join broken lines into short paragraphs of about 30 seconds each.
2. Do not change any word unless it is a clear typing split. Mark unclear words "[unclear]." Fix the spelling of proper names only to match the agenda, and list each fix at the end.
3. Do not label who is speaking unless the transcript or agenda says so. Otherwise write "speaker not identified."
4. Put this notice at the top: "Machine-made captions turned into text. Not an official record or minutes. Check any quote against the video at the timestamp."
5. After the transcript, add an index of agenda items with the timestamp where each starts.

AGENDA:
[paste]

TRANSCRIPT:
[paste]
```

## 8. Summarize one item from a transcript

```
[Paste the rules block.]

Summarize what was said about agenda item [number] in the transcript below, in the order it was said. Tie each point to a timestamp. Do not use quotation marks around your summary words. Do not say who was right. List any decisions announced, with the timestamp, and say they must be checked against adopted minutes.

TRANSCRIPT:
[paste]
```

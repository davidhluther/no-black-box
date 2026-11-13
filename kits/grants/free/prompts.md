# Paste-in Prompts for Grants Research and Drafting

A prompt (the message you type or paste into a chat) works with an AI model (a program that reads and writes text, such as ChatGPT, Claude or Gemini). These ones are written to work in the free versions of ChatGPT, Claude and Gemini. Open a new chat, paste the prompt, then paste your own material where the square brackets say to.

## Four rules that apply to every prompt

1. AI models make things up, and they do it fluently. Funder names, deadlines, award sizes and "facts" about your own organization are the things most often invented. Use the AI model to read, sort and write what you paste in. Do not use it as a source of facts about funders or about you.
2. Check every funder yourself. Open the funder's own website and write down the web address and the date next to each fact. Mark each fact verified (you saw it), secondary (a directory said so) or unverified (you have not seen it).
3. Keep private details out. Never paste donor names, client names, case notes, passwords or bank numbers. Aggregate numbers only ("1,200 households," not a list of households).
4. Nothing leaves your hands. These prompts produce drafts for a person to review. A person sends them.

## Prompt 1, where to look

Use this when you have no funder list yet. It asks for search ideas, not names, so it can't invent a funder.

```
I work with a small nonprofit. Here are the facts you may rely on:
- What we do: [one or two sentences]
- Where we work: [towns or counties]
- Who we serve: [people]
- Typical budget size: [rough range]

Do not name any specific funders, because I will check names myself. Instead give me:
1. Ten kinds of funders that often give to organizations like ours (for example, community foundations, local banks' giving programs, civic clubs, congregations' mission funds), with one sentence on why each fits.
2. For each kind, three phrases I can type into a web search to find real ones near us.
3. Five questions I should ask our own board and past records before I search, to find funders we may already know.
```

## Prompt 2, turn a funder's own page into a dossier

Open the funder's website. Copy the text of its guidelines or "apply" page and paste it where shown. If you have the funder's tax filing numbers from ProPublica Nonprofit Explorer (a free site that shows nonprofit tax filings, at projects.propublica.org/nonprofits), paste those too.

```
You are helping me write a funder dossier. Use ONLY the text I paste below. If something is not in the text, write "Not found in pasted text" and do not guess.

Fill in this template exactly:
Funder name:
City and state:
Type (private foundation, community foundation, corporate, government, public charity):
Giving priorities, quoted in their words:
How to apply (open application, letter of inquiry, invitation only, no unsolicited proposals):
Deadlines or cycles:
Award range or typical size:
Geography rules (where they will and won't give):
Required attachments:
Eligibility rules that might exclude us:
Questions a person must confirm by phone or email:

Our organization, for the fit note only: [what we do, where, who we serve].
Last, give a two-sentence fit note saying whether we seem to fit and the single next step.

PASTED TEXT:
[paste the guidelines text here]
[paste tax filing numbers here, if any]
```

Then put each answer into a row of your Funders tab, with the web address and today's date in the "Date checked" and "Funder website" columns.

## Prompt 3, are they already a funder of ours?

Before you call anyone a prospect, check whether they have already given to you. Copy the names from your bank deposits report, old grant reports and board minutes and paste them below. Spellings vary, so the AI model helps you match them.

```
Below is a list of names of funders we have received money from or applied to in the past, copied from our own records. Below that is a list of funders I am researching. Tell me which names in the second list might be the same as a name in the first list, even with different spelling, abbreviations or word order (for example "Smith Fndtn" and "The Smith Family Foundation"). Show each possible match side by side. Do not guess beyond the spelling; I will check each one.

OUR RECORDS:
[paste names]

RESEARCHING:
[paste names]
```

## Prompt 4, build your claims register from your own documents

A claims register (a table of every fact you may state about your organization) also records each fact's source. Paste text from your annual report or audit, one document at a time.

```
Read the text below, which comes from our [annual report / audit / determination letter]. Turn every checkable fact and number in it into rows of a table with these columns: ID, Claim, Value, As of, Source, Status.
- ID: a short code such as PRG-01 for programs, FIN-01 for money, ID-01 for identity.
- Claim: the fact as one plain sentence.
- Value: the one number in the claim, written as it appears (1200, or 35 for 35 percent). One number per row. Leave blank if there is no number.
- As of: the period the number covers.
- Source: the document name and page. The document is: [document name].
- Status: write "source-verified" for everything, because it comes straight from our own document.
Do not add any fact that is not in the text. Do not round. Give the table as plain text separated by tabs so I can paste it into a spreadsheet.

TEXT:
[paste the text here]
```

## Prompt 5, draft a letter of inquiry or application

```
Write a first draft of a [letter of inquiry / application answer] to the funder described below. Rules:
- Use ONLY facts from my CLAIMS table. After each fact, put its ID in square brackets, like [PRG-01]. If you need a fact that is not in the table, write [CONFIRM: what is needed] instead of inventing it.
- Use only the program I name. Do not claim service outside these places: [towns or counties we serve].
- Open with the funder's own priority language where it honestly fits. Do not repeat their mission back at length.
- Use each number once, with the period it covers.
- Plain, warm, specific. No hype words. Keep to [length limit].
- The ask is $[amount] for [purpose]. Say how I arrived at it only if the funder's guidelines give a range.

PROGRAM TO PITCH: [name and two sentences]

FUNDER DOSSIER:
[paste the dossier you made in Prompt 2]

CLAIMS TABLE:
[paste the rows from your Claims tab, including ID, Claim, Value, As of, Status. Leave out rows marked unverified or do-not-use.]
```

Paste the result into the DraftCheck tab (see GR-FR-04) and run the check before anyone reads it.

## Prompt 6, a second look from a fresh chat

Start a brand new chat so the AI model has not seen the draft being written. This takes the role of a reviewer with no stake in it.

```
You are a skeptical program officer. Below are the funder's own guidelines and a draft that was written for them. Find: (1) anything the guidelines require that the draft does not answer, (2) any claim in the draft that looks unsupported or exaggerated, (3) wording that does not match the funder's tone, and (4) anything you would reject on sight. List each problem with the exact words from the draft. Do not rewrite the draft.

GUIDELINES:
[paste]

DRAFT:
[paste]
```

## Prompt 7, a board update

```
Below are figures from our grants tracker. Write a one-page summary for our board in plain language. Say what is working, what is stuck, and the three things that most need a decision this month. Use only these figures and say "not known" for anything missing. Do not predict.

FIGURES:
[paste the Dashboard tab's Measure and Value columns]

OPEN ASKS AND DEADLINES THIS MONTH:
[paste the Funder, Request, Status and Deadline columns for rows that are open or due soon]
```

## Prompt 8, page copy for a way of giving

For gifts from a donor-advised fund (a charitable account a donor holds at a sponsor), and for stock, monthly and will pages, start from the templates in the giving-channels folder, then use this prompt to fit them to your voice.

```
Here is template text for a donor letter or web page about [a gift through a donor-advised fund / a monthly gift / a gift of stock / an IRA gift / a gift in a will]. Rewrite it in our voice, which is [warm and plain / formal / short]. Keep every bracketed blank as it is, because a person will fill those in. Keep the tax disclaimer unchanged. Do not add any dollar amounts, tax rules, limits, deadlines or legal claims that are not in the template.

TEMPLATE:
[paste the template]
```

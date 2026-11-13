# Paste-In Prompts for the Owner's Numbers Kit

These work in any free [AI model](../glossary.md#ai-model), including free ChatGPT, Claude and Gemini. Copy a prompt, replace the bracketed parts, and paste it into a new chat. An [AI model](../glossary.md#ai-model) only sees what you paste, so copy numbers and layouts, never account numbers, passwords or a customer's name.

Each prompt carries the same rule. A number built on a guess is a [what-if](../glossary.md#what-if), and the AI model must say so.

## 1. Tag my bank rows

Use this before the Bank [tab](../glossary.md#tab) if you have not categorized yet. Paste only the description and amount columns, with account numbers removed.

```
You are helping a small business owner tag bank rows. Use only these categories:
sales_deposit, other_income, cogs, supplies, payroll, rent, utilities, software,
insurance, marketing, loan_payment, tax, other_fixed, other_variable, owner_draw, transfer.
For each row below, return one line: the row number, the category, and a confidence
of high or low. If you are not sure, say low and do not guess. Rows:
[paste description and amount, one row per line]
```

Check every "low" row yourself. Then type the categories into the Bank tab.

## 2. Read my scorecard back

```
Below are the values from the Scorecard tab of my monthly sheet, with a basis
column that says "actual" or "what-if". Explain the month in plain words in under
200 words. Say first whether the month paid for itself. Then name the two numbers
that matter most. Any line marked what-if must be called a what-if, and you must
not draw a conclusion about my business from it. Finish with the one thing I
flagged for myself, and stop. Do not tell me what to decide.
[paste the Scorecard tab: label, value, basis]
```

## 3. Explain one metric to me

```
Explain [metric name, for example break-even] to a small business owner with no
finance training. Use a hair salon or a food bank as the example, with made-up
numbers marked as an example. Give the formula in one line, then say which of
my inputs would have to be real before the result stops being a what-if.
```

## 4. Pricing question

```
My price is [price] and one more sale costs me [variable cost] directly
(supplies, card fees, commission). I am thinking about changing the price by
[percent]. Work out the break-even volume shift: how much volume I can lose, or
must win, before the change stops paying. Show the arithmetic. This is a finding
because it uses only my own numbers. If you also estimate how many customers I
will lose, label that a what-if built on my assumption and name the assumption.
Do not predict demand.
```

## 5. Quarterly report

```
Here are my monthly Scorecard values for three months, each with a basis column.
Write a quarterly report with these headings: What happened, One naive look ahead,
Where the money sits, Decisions for next quarter. The look ahead must be labeled
what-if, continue a straight line, and name the season next to it. Where my
basis column says what-if, label the result what-if. Leave the decisions table
blank for me to fill in.
[paste the three months]
```

## 6. Advisory letter

```
Draft a letter of about 200 words from [sender] to [recipient] about [month].
Four short paragraphs. One, the verdict in a sentence. Two, the numbers that moved,
with direction. Three, the one thing to look at, stated as an observation. Four,
one question to think about before next month. Use only the numbers below.
Do not include any what-if as if it were a fact. Dates in mm/dd/yyyy.
[paste the Scorecard values]
```

## 7. Twelve-month roadmap

```
Build a 12-month roadmap in four quarters. For each quarter give a table of two
or three metrics with a baseline, a target and why it matters, plus one first action.
Use only the baselines I give you. For any target I have not given, write "to set".
Do not invent a target number. My baselines and priorities are:
[paste baselines and what you want to improve]
```

## 8. Check my data

```
I will paste the first ten rows of my [sales/bank/bookings] export. Tell me
whether the columns match this layout: [paste the header row from the template].
List any column that is missing, out of order or named differently. Do not
repeat any names or amounts back to me.
```

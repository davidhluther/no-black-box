# Paste-in prompts for the free version

Everything here works in the free versions of ChatGPT, Claude, Gemini, and Perplexity. Replace anything in curly brackets with your own details. Keep your replacements short and in the words a customer would use.

## Part 1: Find names that look like yours (preflight)

Ask this in a fresh chat on any free [AI model](../glossary.md#ai-model). Fill in your business name and town. Do not add anything else.

```
What businesses, people, places, or everyday words are called or sound like "{business_name}"? List each one with what it is and where it is. Do not assume I mean any one of them.
```

Ask the same thing once with your owner's name:

```
Who or what is called "{owner_name}"? List the different people or businesses with that name, with what each does and where. Do not assume I mean any one of them.
```

Write what comes back on the SameNames tab. Then search the name yourself, because AI models can invent businesses that do not exist. Guide AV-FR-02 walks through it.

## Part 2: The 28 questions

These are templates. The Questions tab in your sheet fills in your details automatically. If you work without the sheet, replace each placeholder yourself. The wording is casual on purpose, with the missing apostrophes and lowercase letters. Customers type this way, and tidying the wording can change what a model returns. Once you have asked a question for the first time, never edit it. If one turns out to be broken, strike it out, write the date and reason, and add a new one with a new code.

Placeholders are {business_type}, {service}, {town}, {region}, {business_name}, {owner_name}, and {competitor_1}.

### Local discovery

**LD-01**

```
is there a good {business_type} in {town} that does {service}? i dont want to drive to the city
```

**LD-02**

```
anyone in {town} or {region} who actually does {service} well? looking for someone local, not a chain
```

**LD-03**

```
whats the best {business_type} near {town} for {service}
```

**LD-04**

```
i just moved to {town}. who should i go to for {service}? i dont know anybody here yet
```

**LD-05**

```
{business_type} in {town} that takes walk ins or books same week for {service}
```

**LD-06**

```
Looking for a {business_type} in {region} that is good for {service} and not crazy expensive. Who do locals actually use?
```

**LD-07**

```
my sister is visiting {town} next month and wants {service}. where should she go
```


### Problem first

**PF-01**

```
i keep paying for {service} and hating how it turns out. how do i find a {business_type} that actually gets it right
```

**PF-02**

```
how do i know if a {business_type} is any good at {service} before i book
```

**PF-03**

```
i got a bad {service} somewhere in {region} last month. what should i look for next time
```

**PF-04**

```
my {service} appointment got cancelled at the last minute. is there a {business_type} around {town} that can fit me in this week
```

**PF-05**

```
is {service} worth it or should i just do it myself at home
```


### Cost and education

**CE-01**

```
how much does {service} usually cost at a {business_type} in a small town like {town}
```

**CE-02**

```
what should i expect at my first visit to a {business_type} for {service}
```

**CE-03**

```
how often do people get {service} and how long does it take
```

**CE-04**

```
what is the difference between a cheap and an expensive {business_type} for {service}
```


### Choosing between options

**CH-01**

```
is it better to go to a small local {business_type} or a chain for {service}
```

**CH-02**

```
{business_type} near {town}: how do i pick between the ones with good reviews
```

**CH-03**

```
should i trust the top rated {business_type} in {town} or ask a friend
```

**CH-04**

```
what questions should i ask a {business_type} in {region} before booking {service}
```


### Controls (no town named)

**CT-01** (control)

```
what makes a good {business_type}
```

**CT-02** (control)

```
how do i find a trustworthy local business for {service}
```

**CT-03** (control)

```
what should i know before booking {service}
```


### Brand check (may name your business)

**BV-01**

```
is {business_name} in {town} legit?
```

**BV-02**

```
what does {business_name} in {town} offer and who runs it? i think {owner_name} is the owner
```

**BV-03**

```
{business_name} {town} reviews, what do people say
```

**BV-04**

```
{business_name} vs {competitor_1} in {town}, which is better for {service}
```

**BV-05**

```
where is {business_name} and what are their hours
```


## Part 3: Asking, one question at a time

1. Open a fresh chat. One question per chat, and no follow-up questions.
2. Paste the question exactly. Press enter.
3. Wait for the whole answer. Copy all of it.
4. Paste it under the question code in your answer document (template in `answer-log-template.md`).
5. Log one row on the Results tab. Close the chat.

Never argue with the model, and never name your business in a chat that did not start with a brand-check question. Doing so hands the model the answer and spoils that cell.

## Part 4: Optional help with coding an answer

Coding means filling in a Results row from an answer. You can do it yourself with the guide in AV-FR-05. If you want a second pair of eyes, paste this into a fresh chat, then paste one answer after it. Check what it says against the answer yourself. A free AI model sometimes misreads.

```
I run {business_name}, a {business_type} in {town}. Website: {website_domain}.
Below is an answer an AI model gave to a customer question. Do four things.
1. Say whether {business_name} is named. If so, quote the exact sentence and say whether it is first, second, third or later, in a list, or an aside.
2. List the web addresses or website names listed as sources, and say whether {website_domain} is one of them.
3. List every other business named.
4. Say whether any name in the answer could be a different business with a similar name to mine, and explain why.
Quote the answer for every claim. If something is not in the answer, say "not in the answer".

ANSWER:
{paste the answer here}
```

## Part 5: The repeat test (how noisy is this?)

Pick three questions. Ask each one three more times, each in a fresh chat on the same product, and record whether you are named each time. If you are named once in four tries, a single "named" in your main run is weak evidence. This is the cheapest honest measure of how much an AI model's answer varies from one ask to the next.

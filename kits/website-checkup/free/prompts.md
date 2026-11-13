# Paste-in prompts for the website check-up

Each [prompt](../glossary.md#prompt) below works in a free ChatGPT, Claude, or Gemini chat. Copy the text in the box, replace anything in [SQUARE BRACKETS] with your own details, and paste it into a new chat.

Two habits make every prompt work better.

- Start a fresh chat for each prompt. Long chats drift.
- If the [AI model](../glossary.md#ai-model) says it can't open web pages, don't argue. Open the page yourself, copy the text (or the page source where a prompt asks), and paste it under the prompt.

Every prompt ends with the same safety line. It tells the model to mark anything it couldn't check as unknown, so a missing number never turns into an invented one.

## 1. Quick scorecard (start here)

```
You are checking a small business the way a stranger would, using only public information. Do not guess. If you cannot check something, write "unknown" and say what would be needed.

Business: [NAME EXACTLY AS ON GOOGLE]
Website: [https://www.example.org]
Type of business: [for example restaurant, dentist, plumber, shop]
Town or area: [CITY]
Competitors: [UP TO FIVE NAMES OR WEBSITES, OR "none known"]

Check these sections and give each check one result: Pass (2 points), Partial (1), Fail (0), or Unknown (left out of the score).
1. Google listing: claimed, exact name, specific main category, extra categories, address or service area, honest hours, clean website link, description, services listed, real photos, recent activity.
2. Reviews: rating, count against competitors, a review in the last 90 days, owner replies, a second review platform, an easy way to ask.
3. Speed: tell me to run pagespeed.web.dev on the mobile tab for the home page and paste the result. Do not invent scores.
4. Structured data: tell me to paste the home page source so you can look for JSON-LD blocks.
5. Local search: name, address, and phone identical everywhere; Apple and Bing listings; a directory for this business type; city named on key pages; a page per service; map or directions.
6. Positioning: who the business says it serves, what only it can claim, and whether the Google description, home page, and social bio make the same promise. Quote the words you read.
7. Search visibility: ask me whether Search Console and Bing Webmaster Tools are set up.

Then give me: (a) a table with section, points, possible, percent, and how many checks were answered; (b) the five most important findings, most important first, each with its evidence and a label of Confirmed, Likely, or Unverified; (c) a list titled "What this check could not see."
Anything you could not open or verify is "unknown", never "fail". Never invent a number.
```

## 2. Read my Google listing

```
Below is the text I copied from my business's Google Maps listing. Review it as a stranger would. Do not guess at anything that is not in the text.

[PASTE THE LISTING TEXT, INCLUDING CATEGORIES, HOURS, DESCRIPTION, AND SERVICES]

Check: is the name exact with no extra keywords; is the main category specific to our core service and not a catch-all; do the extra categories cover our other services; is the address or service area right for how we work; are the hours honest; is the description clear and free of links, prices, and promotions; are services listed. Also tell me what a competitor with a more specific category might be doing better. For anything you can't tell from the text, write "unknown". Give me the three changes that matter most.
```

## 3. Compare reviews with competitors

```
Here are the Google ratings and review counts for my business and its local competitors, which I copied from their listings today ([DATE]).

[PASTE A SIMPLE LIST: NAME, RATING, REVIEW COUNT, MAIN CATEGORY]

Place each rating in a bucket (4.8 and up top, 4.5 to 4.79 strong, 4.0 to 4.49 average, 3.0 to 3.99 mixed, below 3.0 poor) and each count in a bucket (1,000 and up very high, 500 to 999 high, 100 to 499 moderate, 25 to 99 thin, under 25 very thin). Work out the median review count of the competitors. Tell me whether my count is below 20% of that median, between 20% and 49%, or at least half. Do not guess at how fast anyone is gaining reviews, because a total count cannot show that. End with two plain-words suggestions for asking happy customers for reviews.
```

## 4. Read my speed results

```
Below are the results I copied from pagespeed.web.dev (mobile tab) for [PAGE ADDRESS] on [DATE]. Treat the "real-world" (field) numbers as more important than the lab numbers. If field data is missing, say so.

[PASTE THE SCORES AND THE FIELD OR LAB NUMBERS]

Explain in plain words: is the page good, in need of improvement, or poor; which of loading (LCP, good is 2.5 seconds or less), responsiveness (INP, good is 200 milliseconds or less), and layout shift (CLS, good is 0.1 or less) is the problem; and what are the three most likely causes and fixes, written so I can hand them to the person who manages my website. Do not invent numbers that I did not paste.
```

## 5. Check my structured data

```
Below is the source of my home page (or the JSON-LD blocks from it). Look for blocks that begin with <script type="application/ld+json">.

[PASTE THE SOURCE OR THE BLOCKS]

My business: [NAME], [ADDRESS], [PHONE], type: [TYPE OF BUSINESS].

Tell me: is any structured data present; does it parse as valid JSON; is the business type specific and right; are name, address, and phone present and identical to what I gave you; does it describe anything a visitor can't see on the page; and does it copy review stars from another site (that is a risk, so flag it). Then write a corrected LocalBusiness block using only the details I gave you. Put TODO_ in capitals wherever you don't know a value, such as TODO_HOURS. Never guess a phone number, hours, or map coordinates.
```

## 6. Check name, address, and phone everywhere

```
I will paste how my business appears in several places. Compare them character by character.

Official version (from my website): [NAME | ADDRESS | PHONE]
Google: [PASTE]
Apple Maps: [PASTE]
Bing Places: [PASTE]
Yelp: [PASTE]
Other directory: [PASTE]

List every difference, even small ones such as "Street" against "St." or a different phone format. Mark each place exact, variant, or mismatch. Then tell me which places to fix first, with Google and my own website first. If I left a place blank, write "not checked".
```

## 7. Read my positioning

```
Here are three pieces of text from my business: the opening of my home page, my Google description, and my newest social media bio.

[PASTE ALL THREE, LABELED]

Score three things from 0 to 3 and quote the words you based each on. (1) Segment clarity: does it name who it serves, narrowly enough to act on? (2) Distinctiveness: is there a claim a competitor could not copy word for word? "Quality service at fair prices" scores low. (3) Consistency: do the three places make the same promise to the same person? Then suggest one sentence that could appear in all three places. Don't add facts I haven't given you.
```

## 8. Technical basics (the free substitute for a crawl)

```
Here is what I collected for my site [SITE ADDRESS].

Search Console, Pages report (indexed and not indexed, with reasons): [PASTE]
Search Console, Sitemaps report: [PASTE]
Pages that return errors or redirects: [PASTE OR "none known"]
My robots.txt (the text at my-site/robots.txt): [PASTE]
PageSpeed Insights results for the home page: [PASTE]

Find problems in this order: pages Google can't reach, pages that can be reached but aren't kept (and the stated reason), pages that look blocked by robots.txt, security (any pages served as http:// instead of https://), speed. For each, give a severity (Critical, High, Medium, Low) based on how many pages are affected and how likely it is to lose customers, and the effort (small, medium, large). Then say what you could not check without a full crawl. Don't invent counts.
```

## 9. Rewrite titles and descriptions

```
For each page below, write two or three title options (about 50 to 60 characters) and two or three meta description options (about 150 to 160 characters). The title should hold the main phrase near the front and give a reason to click. The description should say what the visitor gets and invite the click. Use plain words, no keyword stuffing, no claims the page can't back up, and my business name at the end of the title if it fits. Give each option's character count, say which one you recommend and why, and suggest one main heading (H1) per page.

Business: [NAME] in [CITY]
Page 1: address [URL], current title [TITLE], current description [DESCRIPTION], main phrase [PHRASE], what the page offers [ONE LINE]
Page 2: [SAME DETAILS]
```

## 10. Read my Search Console numbers

```
Below is an export from Google Search Console for my site, the last three months of queries with clicks, impressions, click-through rate, and average position.

[PASTE THE TABLE OR ITS TOP 50 ROWS]

Tell me: which searches bring clicks; which searches show my site often but rarely get clicked (many impressions, low click-through, which suggests the title or description needs work); which searches sit at positions 8 to 20 where a better page might reach page one; and any search that looks like my business name versus a general search. Give me five actions. Use only the numbers I pasted.
```

## 11. Find pages that compete with each other

```
Below is a Search Console export showing, for each search, the pages of my site that were shown for it.

[PASTE QUERY, PAGE, CLICKS, IMPRESSIONS ROWS]

Find searches where two or more of my pages appear. For each, decide whether the pages serve different needs (for example a service page for people ready to hire and a guide for people learning), in which case I should keep both and make each page's title and heading aim at its own need, or the same need, in which case I should merge them or point one at the other. Say which page should be the main one and why, using clicks. Don't recommend merging a service page into a guide or the reverse.
```

## 12. Find questions to answer on my site

```
My business: [TYPE OF BUSINESS] in [CITY]. Services: [LIST]. The searches I already get clicks for: [PASTE A FEW].

List 30 questions a real customer might type before choosing a business like mine. Group them by service, and mark each as a question to answer on a service page, a question for a short guide, or a local question that includes our town. Mark questions of five words or more that describe a specific problem as "strong." I will check them against real autocomplete suggestions, so don't pretend they came from search data.
```

## 13. Turn findings into a plan

```
Below are findings from my website check-up. Turn them into an action plan. Rules: only Confirmed and Likely findings become numbered tasks. Unverified findings go in with their caveat. Hypotheses go in a separate "investigate" list. Rate each task on impact, urgency (P0 crisis, P1 high, P2 medium, P3 low), and effort (small, medium, large) for a one-person business with about [HOURS] hours a week. Anything that shows wrong facts about my business to customers (wrong address, wrong hours) is P0. Group tasks by site content, local presence, technical, listings and links, and AI visibility. Each task needs what to do, why, and what it will change. Don't promise rankings.

[PASTE YOUR FINDINGS]
```

## 14. Ask an AI model about my business

Run each question in a separate fresh chat, in each of ChatGPT, Claude, and Gemini, and note the answers in the Baseline16 tab, item 13.

```
What does [BUSINESS NAME] in [CITY] do? What are its hours and phone number? Would you recommend it? Say where you got each fact, and tell me what you are not sure about.
```

```
Who are the best [TYPE OF BUSINESS] in [CITY], and why?
```

```
I need [SERVICE] in [CITY]. What should I look for, and which local businesses would you suggest?
```

Read the answers the way a stranger would. Write down anything wrong, missing, or about a different business with a similar name. Wrong facts are the first thing to fix.

## 15. The monthly 15-minute reading

```
Here are this month's numbers from my Monthly tab and last month's. Answer three questions in plain words, using only these numbers. (1) Did anything break? (2) What did search send? (3) Where did people struggle? Then name the one thing I should do before next month.

[PASTE THE LAST TWO ROWS OF THE MONTHLY TAB, PLUS ANY NOTES]
```

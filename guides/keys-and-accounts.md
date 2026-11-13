# Keys and Accounts

Some kits need an account on another service, and a few need a key. This guide covers every one, in the order a beginner will meet them. A key (also called an API key) is a long password that lets a program use a service for you, the way a hotel key card opens your room and nobody else's. An API (a way for two programs to talk, like a waiter carrying orders between you and the kitchen) is what the key opens.

Prices change. A price below has a date next to it, which means it was read on the vendor's own page that day. Anything else says where to look. Terms are in the [glossary](glossary.md).

## Rules for every key

These apply to all the services below.

1. **NB-FR-03-1.** Treat a key like a bank password. Never type it into a chat with an [AI model](glossary.md#ai-model), a Google Sheet, a Doc, an email, or a [kit](glossary.md#kit)'s `config.json`.
   You'll know you did it right when a search of your shared files for the first few characters of the key finds nothing. If a key landed in a shared file, delete it from the file and go to step 2 (E09).
2. **NB-FR-03-2.** If a key ever lands somewhere it shouldn't, make a new one on the service's website and delete the old one. This is called rotating a key.
   You'll know it worked when the old key stops working. Old keys in file history still count as leaked, so always rotate.
3. **NB-FR-03-3.** Keep keys in one private place. For the full version, that is a plain text file named `.env` inside your kit folder, with one line per key in the form `NAME=value`. For tools that have a settings screen, use the screen.
   You'll know it worked when the kit's check-up (`python3 support/doctor.py <kit-id>`) says the name is set. It reports names only and never prints the value.
4. **NB-FR-03-4.** Before sharing a screenshot or screen, close the `.env` file and any settings screen that shows a key. Many services show only the last four characters, and that is safe to show.
   You'll know it worked when no screenshot shows a full key. If one does, rotate it (step 2).
5. **NB-FR-03-5.** Never save the `.env` file in a folder you sync to a shared drive, and never upload it to GitHub. Kits that use one ship a `.gitignore` line that blocks it, but check.
   You'll know it worked when `.env` does not appear in the list of files you share.
6. **NB-FR-03-6.** Set a spending limit wherever the service allows one, before your first paid request.
   You'll know it worked when the billing page shows a monthly cap.

## Accounts every kit uses

### Google account and Google Workspace for Nonprofits

Needed by every free and low-cost kit, because the trackers, checklists, and forms live in Google Sheets, Docs, and Forms.

- **Sign up.** A personal Google account works today. If your organization is a registered nonprofit, apply for Google Workspace for Nonprofits at google.com/nonprofits, which verifies eligibility first.
- **Free tier.** The base edition of Workspace for Nonprofits is $0 per user per month once you are verified (checked 11/13/2026). Eligibility rules are on Google's page.
- **Past free.** Higher editions are discounted for nonprofits. See current prices at google.com/nonprofits.
- **Where the key goes.** There is no key. You sign in.

### Claude (free and low cost)

Needed by the kits' Claude versions. Sign up at claude.ai.

- **Free tier.** The Free plan is $0 per month (checked 11/13/2026). Skills can be uploaded on every plan once [code execution](glossary.md#code-execution) is on.
- **Past free.** Pro is $20 per month billed monthly (checked 11/13/2026). Higher plans are on claude.com/pricing.
- **Where the key goes.** There is no key for chat. You sign in.

### Anthropic API (full version only, optional)

Used by scripts that call Claude directly, billed by use instead of a flat plan. Sign up at console.anthropic.com.

- **Free tier and cost.** See current prices and credits at claude.com/pricing.
- **Where the key goes.** In `.env` as `ANTHROPIC_API_KEY`.

### ChatGPT and the OpenAI API

ChatGPT is for kits' ChatGPT versions. Sign up at chatgpt.com. See current plan prices at chatgpt.com/pricing, because the page didn't show them on 11/13/2026. The free version of ChatGPT is available to everyone, according to OpenAI's pricing page (checked 11/13/2026).

The OpenAI API is separate, billed by use, and only used by the picture-making steps in Idea to live post and Ad and social. Sign up at platform.openai.com. Costs are on openai.com/api/pricing. The key goes in `.env` as `OPENAI_API_KEY`.

### Gemini

A free alternative for the paste-in prompts. Sign up at gemini.google.com with your Google account. See current limits at gemini.google.com. Google AI Studio (aistudio.google.com) issues API keys. The key goes in `.env` as `GOOGLE_API_KEY`. Gemini features in the Nonprofits edition are not verified here.

## Accounts by kit

### Grants and giving, and Board packet and minutes

- **Grants.gov and the IRS tax-filing search.** Public data sites, so you read them without signing up. Check each site for its current terms.
- **ProPublica Nonprofit Explorer.** A search of nonprofit tax filings at projects.propublica.org/nonprofits. Check the site for whether its data service needs a key.
- **Transcription.** The board packet kit turns a meeting recording into text with [Whisper](glossary.md#whisper), a speech-to-text program that runs on your own computer (full version). It needs no account.

### Treasurer and books

- **QuickBooks Online.** Your organization's own subscription. Prices are on quickbooks.intuit.com.
- **Intuit developer account (full version only).** A free sign-in at developer.intuit.com where you create an app, which gives you a client ID and a client secret. See Intuit's page for current terms. Choose read-only (accounting reports) when it asks for scope.
- **Where they go.** `QBO_CLIENT_ID` and `QBO_CLIENT_SECRET` in `.env`. Intuit also gives the script a [token](glossary.md#token) after you approve it in your browser, and the script stores that token in a private folder it names when it runs.
- **Safety.** The script only reads. It never changes your books.

### Plain writing

No accounts. It runs on text you paste.

### Idea to live post, Website check-up, AI visibility, and Measure what matters

- **Google Search Console.** A free Google service that shows how your site appears in Google search (checked 11/13/2026). Sign in at search.google.com/search-console and verify your site. No key.
- **Bing Webmaster Tools.** Bing's version. Sign up at bing.com/webmasters. See the page for terms. No key for the free version.
- **Google Analytics 4 (GA4).** Free website visit counts. Sign up at analytics.google.com.
- **Microsoft Clarity.** Free recordings and heat maps of how people use your pages. "Free forever," per its homepage (checked 11/13/2026). Sign up at clarity.microsoft.com. The [project](glossary.md#project) ID goes in `config.json`, because it isn't secret.
- **Google PageSpeed Insights.** A free speed check at pagespeed.web.dev. A key is optional. A key from Google Cloud Console goes in `.env` as `GOOGLE_API_KEY`. See Google's page for limits.
- **Ahrefs (full version, paid).** A search data service. See ahrefs.com for current plans. The key goes in `.env` as `AHREFS_API_KEY`. The free and low-cost versions skip it.
- **Your site's publishing system.** The Idea to live post kit can publish for you if you give it a token (a key that only lets it add posts). Create it inside your own site's admin settings and keep it in `.env`.

### Customer-language research

- **Reddit and Yelp.** Reading public pages needs no key. Yelp's data service issues a key at yelp.com/developers, which goes in `.env` as `YELP_API_KEY`. See Yelp's page for limits and cost.

### Civic voice

- **Census Bureau data key.** A key request form is at api.census.gov/data/key_signup.html. The page doesn't state cost or limits, so read its terms. The key goes in `.env` as `CENSUS_API_KEY`.

### Owner's numbers, Continuity kit, and Builder's toolkit

No accounts beyond Google and one AI model. They work from files you export from your own tools.

### Ad and social

- **Canva.** Design tool for ad pictures. See canva.com/pricing for free and nonprofit offers, because the page refused automated reading on 11/13/2026.
- **Image makers.** The OpenAI API and Gemini above can generate images when a key is present. Without a key the kit writes a designer brief instead.

If a service won't let you sign up or a key doesn't work, write down the [step ID](glossary.md#step-id) and see [getting help](getting-help.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like NB-FR-03-3). If your kit has a check-up button or command, run it and copy the [support code](glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

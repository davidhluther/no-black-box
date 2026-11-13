# Shopping List

Every item below says what it is, why the kit uses it, what it costs, what to use instead, whether you can skip it, and where you have room to choose. For each account or key, the shared guide [Keys and accounts](../../guides/keys-and-accounts.md) shows where to sign up, what the free tier covers, and where a key goes. Prices change often, so this page states none. Look at the vendor's own pricing page before you buy.

## Free version

These items cover everything in the free guides, AV-FR-01 to AV-FR-07.

### A Google account and Google Sheets

- What it is. Google Sheets is Google's free spreadsheet app. You sign in with a Google account.
- Why. The tracking sheet lives here, and so does the [check-up](glossary.md#check-up) button (built with [Apps Script](glossary.md#apps-script), a Google tool that runs small programs inside a sheet).
- Cost. Free for a personal account. Nonprofits can often use a free Google Workspace for Nonprofits account, if they are eligible. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Instead. Excel works for the tracking tabs, but the check-up button and logging [script](glossary.md#script) need Google Sheets.
- Skip it? No, for the free and low-cost versions.
- Room to choose. A work account or a personal one. Use a shared nonprofit account if several people will run the questions.

### Free access to four AI products

- What it is. ChatGPT, Claude, Gemini, and Perplexity, each in its free tier.
- Why. These are the products customers use, so the answers you collect are what customers see.
- Cost. Free tiers. Their limits and sign-in rules change, so check each one. In 2026 some allowed use without signing in and some did not.
- Instead. Use fewer products. Three products gives a smaller but still honest picture. Write down which ones you used and keep the same set every month.
- Skip it? Skip any one, but keep the same set every month.
- Room to choose. Add Microsoft Copilot or others if your customers use them. Add them as a new series, not into the old one.

### Google Analytics 4 access

- What it is. [GA4](glossary.md#ga4) counts visits to your website. You need edit access to the property to create a [channel group](glossary.md#channel-group).
- Why. It lets you see visits that arrive from AI products.
- Cost. Free. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Instead. Your host's own visitor statistics may show referrers (the site a visitor came from).
- Skip it? Yes. The question battery works without it.
- Room to choose. GA4 only, or GA4 plus Google Search Console (also free), which shows searches that led to your site.

### Time

- About two hours the first month and less after. The 28 questions across four products are 112 asks.

## Low-cost version (adds)

The low-cost version keeps everything above and adds the two items below.

### One paid AI plan

- What it is. A monthly plan for ChatGPT, Claude, or Gemini that lets you set up a Project (a saved workspace with your own instructions and files that the [AI model](glossary.md#ai-model) uses in every chat).
- Why. It reads your pasted answers, suggests the row to log, and helps with the [same-name](glossary.md#same-name) check, saving most of the typing.
- Cost. A monthly fee. See the vendor's pricing page.
- Instead. Keep using the free version. Its prompts do the same job one answer at a time.
- Skip it? Yes. Pick it up only if the typing wears you down.
- Room to choose. Any one of the three. You do not need all of them.

### The logging script

- What it is. `low-cost/log-answers.gs`, a free Apps Script from this kit.
- Why. It adds a menu to the sheet that saves the answer and guesses the row for you.
- Cost. Free.
- Skip it? Yes, but it is the main thing the low-cost version adds.

## Full version (adds)

The full version keeps the free items and adds the following. None of it is needed for the first two versions.

### A computer that can run Python and Claude Code

- What it is. [Python](glossary.md#python) is a common programming language. [Claude Code](glossary.md#claude-code) is a program from Anthropic that runs on your computer and carries out multi-step tasks.
- Why. It runs the runner script and the analysis skills.
- Cost. Python is free. Claude Code needs a Claude plan or [API](glossary.md#api) usage. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Instead. The free and low-cost versions need neither.
- Skip it? Yes, unless you want the full version.

### Developer keys for the AI companies you want to run

- What it is. An API key (a long secret password a program uses to call an AI company's service and be billed) from OpenAI, Anthropic, Google, and Perplexity.
- Why. The runner asks each company's service your 28 questions.
- Cost. Pay as you go on each account. [Web search](glossary.md#web-search) is billed on top of the text cost at some companies. Set a spending limit in each account first. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Instead. Run only the companies you care about, or stay with the hand-run version.
- Skip it? Yes.
- Room to choose. One, two, three, or four companies.
- Safety. A key goes in an environment variable (a setting stored on your computer outside any file), never in `config.json`, a chat, a screenshot, or a shared folder.

### Paid tracking platforms (optional, never required)

- What it is. Services such as Ahrefs Brand Radar, Peec AI, and AirOps track a set of questions on a schedule and report mentions and [citations](glossary.md#citation).
- Why. They can run many more questions than you can by hand and keep history.
- Cost. Subscriptions. See each vendor's page.
- Instead. This kit. Compare any platform's numbers with your own using `unified-visibility`, and ask what questions it tracks and how it avoids same-name confusion.
- Skip it? Yes. Nothing in this kit needs one.

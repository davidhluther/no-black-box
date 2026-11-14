# Shopping List

Every dependency below says what it is, why the program uses it, what it costs, what you can use instead, whether you can skip it, and where you have room to choose. For each account or key, the shared guide [Keys and accounts](../../guides/keys-and-accounts.md) shows where to sign up, what the free tier covers and where a key goes. This page states no prices. Prices change, so read each vendor's own page before you buy or renew.

## What works without a paid platform

All 14 skills. None needs an SEO suite or an AI-visibility platform. The only things that cost money are the AI companies' developer services (the questions) and Claude Code (the analysis).

| Skill | Needs Claude Code | Needs a developer key | Needs a paid platform |
|---|---|---|---|
| `question-battery` (running it) | Yes | Yes, one per company you run | No |
| `battery-preflight` | Helpful | No | No |
| `answer-noise-audit` | Helpful | No | No |
| `aeo-audit`, `aeo-visibility`, `aeo-mentions`, `aeo-citations`, `aeo-competitive`, `aeo-platforms`, `aeo-trends` | Helpful | No | No |
| `visibility-diff` | Yes | No | No |
| `ai-traffic-classifier` | Yes | No | No |
| `unified-visibility` | Helpful | No | No, but better with a [Search Console](glossary.md#search-console) export and any platform exports you own |
| `aeo-implement` | Helpful | No | No, and it needs a person with [CMS](glossary.md#cms) access to apply the handoff |

"Helpful" means the skill is written to also work when you paste files into Claude.ai or ChatGPT, but a team running many sites will want Claude Code so each skill reads the site folders directly.

## Required

### Claude Code

- What it is. [Claude Code](glossary.md#claude-code) is a program from Anthropic that runs on your computer and carries out multi-step tasks with your files.
- Why. It runs the skills against the site folders.
- Cost. Needs a Claude plan or [API](glossary.md#api) usage. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Instead. Claude.ai or ChatGPT can run most analysis skills on pasted files, one site at a time. That works for a pilot and gets tedious across many sites.
- Skip it? Only for a pilot.
- Room to choose. Individual seats for the people who review, or one shared seat on the machine that runs the schedule, depending on your company's policy.

### Developer keys for the AI companies you track

- What it is. An [API key](glossary.md#api-key) from OpenAI, Anthropic, Google (Gemini) or Perplexity, so the runner can ask each company's developer service your questions and be billed to your account.
- Why. The scheduled run asks every question once per company per site.
- Cost. Pay as you go. [Web search](glossary.md#web-search) is billed on top of the text at some companies. A run is sites times questions times companies, so multiply before you schedule it. Check each company's pricing page. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Instead. Run fewer companies. Three is a smaller but honest picture. Keep the same set every month and say which.
- Skip it? You need at least one.
- Room to choose. Which companies, and one key per company shared by the program or one per site if your finance team wants cost by site. Use a team billing account with a monthly cap, never a personal card.
- Safety. Keys live in [environment variables](glossary.md#environment-variable) or a `.env` file outside any shared folder, never in `config.json`, a chat or a ticket.

### A computer that can run a scheduled job

- What it is. A Mac, Linux machine or server that is on at the scheduled time, with Python 3 and a scheduler ([cron](glossary.md#cron) on Mac and Linux, Task Scheduler on Windows).
- Why. `run_program.py` has to start itself on the run day.
- Cost. A machine you already own, or a small cloud machine. See your cloud provider's pricing page.
- Instead. A laptop works if someone's calendar reminder and the daily check cover the days it is closed.
- Skip it? Only if you accept running by hand, which brings the missed-month risk back.
- Room to choose. Where the machine lives and who can log in to it. Put the daily check on a second machine or a hosted scheduler so a dead machine is noticed.

### Search Console and Bing Webmaster Tools

- What it is. [Search Console](glossary.md#search-console) is Google's free report on how each site appears in Google search. [Bing Webmaster Tools](glossary.md#bing-webmaster-tools) is Bing's version. Several AI products draw on Bing's index.
- Why. `unified-visibility` and `ai-traffic-classifier` read query exports from both.
- Cost. Free. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Instead. Any rank tracker that exports queries and clicks can stand in for Bing.
- Skip it? Skip Bing if you must, but say so in the leader report.
- Room to choose. Domain properties or URL-prefix properties. Use one choice per site and note it.

### GA4

- What it is. [GA4](glossary.md#ga4) is Google's analytics. The AI traffic [channel group](glossary.md#channel-group) from the single-site kit sorts visits from AI products into one bucket. Setup is in [AV-FR-07](../ai-visibility/setup/AV-FR-07-add-the-ga4-ai-traffic-channel.md).
- Why. It is the traffic-side check on the question battery.
- Cost. Free tier. See [Keys and accounts](../../guides/keys-and-accounts.md). Teams already on Adobe Analytics can export the equivalent and feed it to `unified-visibility` as a file.
- Skip it? Yes, but you lose one of the sources that can contradict the battery.

## Optional

### An SEO platform

- What it is. A suite such as Ahrefs or Semrush for rankings, backlinks and keyword research.
- Why. The program does not need one. Teams that own one can feed its query exports to `unified-visibility`.
- Cost. Subscription. See [Ahrefs plans](https://ahrefs.com/pricing) or [Semrush plans](https://www.semrush.com/prices/) for the current price.
- Instead. Search Console and Bing Webmaster Tools cover the queries.
- Skip it? Yes.

### An AI-visibility platform

- What it is. A service that tracks a set of prompts on a schedule and reports mentions and citations, such as Ahrefs Brand Radar, Peec AI or AirOps.
- Why. It can ask many more prompts than your 28, and it keeps its own history. `unified-visibility` and `visibility-diff` can sit your battery beside its export.
- Cost. Subscription. See each vendor's own pricing page.
- Instead. This program. Whatever you buy, ask which prompts it tracks, how often, which model versions, and how it avoids [same-name](glossary.md#same-name) confusion.
- Skip it? Yes. Nothing here needs one.
- Room to choose. If you own two platforms that disagree, that is useful input for the agreement check, not a reason to pick one.

### Microsoft Clarity

- What it is. Free recordings and heat maps of how visitors use pages. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Why. It shows what AI-referred visitors do after they land. The skills do not read it.
- Skip it? Yes.

### Looker Studio

- What it is. Google's free dashboard tool. See [Keys and accounts](../../guides/keys-and-accounts.md).
- Why. Some teams show GA4 and Search Console panels beside the monthly leader report. The kit's report is a document and does not need it.
- Skip it? Yes.

### A CMS and a ticket queue

- What it is. The system that publishes your pages, and wherever your web team takes requests.
- Why. `aeo-implement` drafts a handoff and publishes nothing. Someone with CMS access applies it, and the program checks afterward that it went live.
- Cost. Whatever you already pay. A CMS API key is needed only if your team chooses to automate the publish step, which this kit does not do.
- Skip it? No, you need a person who can make the changes.

### A CRM

- What it is. The system where leads and pipeline live, such as Salesforce.
- Why. A leader's real question is pipeline, and AI traffic often shows up as "direct" in a CRM. A CRM is outside this kit, and the report says what it cannot see.
- Skip it? Yes.

### A team chat channel for alerts

- What it is. A channel in the chat tool your team uses, with an incoming [webhook](glossary.md#webhook) address that lets a [script](glossary.md#script) post a message.
- Why. `run_program.py check` posts missed and failed slots there the same day.
- Cost. Usually included in the chat tool. See its admin page.
- Instead. A shared mailbox that someone watches, with the same daily check.
- Skip it? Not if you want same-day flags. The webhook address is a secret: keep it in an [environment variable](glossary.md#environment-variable), not in `config.json`.

## Time

- Setup. About a day for the first site, then an hour per added site once the template is clear.
- Each month. About 20 minutes of machine time per site, plus an hour per site to review the scored draft and read the summary, plus the leader report.

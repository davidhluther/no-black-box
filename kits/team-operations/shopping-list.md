# Shopping List

Everything this kit depends on, split into what the six skills need and what your own recurring jobs will need. Prices change, so every cost points to the seller's own page. Nothing here was verified as of 11/13/2026 except where a line says "checked 11/13/2026," and no price is quoted from memory.

Every account or key is explained in the shared guide [Keys and accounts](../../guides/keys-and-accounts.md). The six skills need no outside keys. The paid platforms below are what your team's own pulls use, and you register those pulls as jobs in [TO-FU-02](setup/TO-FU-02-scheduled-jobs-with-owners.md).

## What the six skills need

| Item | What it is | Why you need it | Cost | Free or cheaper option | Can you skip it | Room to choose |
|---|---|---|---|---|---|---|
| A paid Claude plan | The account that lets you use [Claude Code](glossary.md#claude-code) | Claude Code is how the [skills](glossary.md#skill) run. See [Keys and accounts](../../guides/keys-and-accounts.md) | See the current plans at https://claude.com/pricing | Paying by use through the [API](glossary.md#api) is possible, but a plan is simpler for a team | No | One plan per person who runs sessions. Start with the smallest that includes Claude Code |
| Claude Code | The program you type to | It runs the skills | Included with the plan | None | No | Install it with the shared guide [install-claude](../../guides/install-claude.md) |
| [Python](glossary.md#python) 3 | The language the kit's small programs are written in | The runner and checkers are Python files | Free, from python.org | None needed | No | Any recent version |
| [Git](glossary.md#git) | Tracks a project's history | Ledgers and briefs are meant to be saved with the work they describe | Free | None | You can skip it and lose history | A shared remote [repository](glossary.md#repository) is your team's choice |
| A machine that stays on, or a hosted [scheduler](glossary.md#scheduler) | The place the watcher runs every 15 to 30 minutes | A watcher that sleeps with a laptop cannot catch a missed [slot](glossary.md#slot) | Whatever you already own, or see your hosting provider's own page | A small always-on computer, or your company's job server | Only if you run no [scheduled jobs](glossary.md#scheduled-job) | Mac and Linux use [cron](glossary.md#cron). Windows uses Task Scheduler |
| An alert address (optional) | A [webhook](glossary.md#webhook) from the chat tool your team reads | So a stuck job reaches a person the same day | Many chat tools include it. See your tool's own page | Read the flags file by hand | Not recommended. A flag nobody reads is a delivery failure | Keep it in an [environment variable](glossary.md#environment-variable), never in a shared file |
| A browser the [design gate](glossary.md#design-gate) can drive | A Playwright-controlled Chromium browser | The `design-gate` skill lays pages out in a real browser | Free. Playwright downloads one | An installed Chrome | Yes, if your team ships no web pages | Skip the gate and keep the other five skills |

## What your own recurring jobs will use

These are not part of the kit. They are the sources your registered jobs pull from and the places your reports read. Skip any you do not use.

| Item | What it is | Why you need it | Cost | Free or cheaper option | Can you skip it | Room to choose |
|---|---|---|---|---|---|---|
| Paid SEO platform (Ahrefs, Semrush or similar) | Rankings, backlinks and keyword data, usually through an [API key](glossary.md#api-key) | Source for pulls you register as jobs. See [Keys and accounts](../../guides/keys-and-accounts.md) | See current pricing at https://ahrefs.com/pricing or https://www.semrush.com/prices/ | [Search Console](glossary.md#search-console) and [Bing Webmaster Tools](glossary.md#bing-webmaster-tools) are free | Yes | Check the plan's [quota](glossary.md#quota) before scheduling a pull. A pull that exhausts it is failure E10 |
| [AI visibility platform](glossary.md#ai-visibility-platform) | A service that tracks mentions and citations across AI models | Source for AI visibility pulls. See [Keys and accounts](../../guides/keys-and-accounts.md) | See the vendor's current pricing page | A hand-run set of fixed questions, as in the [AI visibility check kit](../ai-visibility/start-here.md) | Yes | Use at least two sources for any direction claim, so a second one is worth having |
| [GA4](glossary.md#ga4) | Google's analytics for visits, events and conversions | Source for traffic and lead pulls. Free. See [Keys and accounts](../../guides/keys-and-accounts.md) | Free for standard properties. See Google's page for limits | None needed | Yes, if you use another analytics tool | Pull through the reporting [API](glossary.md#api) or a scheduled export |
| [Search Console](glossary.md#search-console) | Google's report of how your site appears in search | Source for search direction. Free. See [Keys and accounts](../../guides/keys-and-accounts.md) | Free (checked 11/13/2026 in the shared guide) | None needed | No, for an SEO team | Needs site verification and a service account for scripted pulls |
| [Bing Webmaster Tools](glossary.md#bing-webmaster-tools) | Bing's report | The second independent source for search direction. Free. See [Keys and accounts](../../guides/keys-and-accounts.md) | Free. See Bing's page for terms | None needed | Yes, but then search direction is often [single-source](glossary.md#single-source) | |
| [Clarity](glossary.md#clarity) | Free visitor-behavior tool | An AI-referral view that does not depend on GA4. Free. See [Keys and accounts](../../guides/keys-and-accounts.md) | Free (checked 11/13/2026 in the shared guide) | None needed | Yes | |
| [Looker Studio](glossary.md#looker-studio) | Google's dashboard tool | Where leaders may read your numbers. Free. See [Keys and accounts](../../guides/keys-and-accounts.md) | Free. See Google's page | Any dashboard tool you already use | Yes | Confirm the dashboard cites its sources and data-through date |
| A [CMS](glossary.md#cms) with an [API](glossary.md#api) | Where pages are published | Needed only for jobs that publish or read pages. See [Keys and accounts](../../guides/keys-and-accounts.md) | Whatever your CMS costs | A manual publish step | Yes | Use a token that can only add or edit posts. A failed publish is E11 |
| A [CRM](glossary.md#crm) | Where leads and opportunities live | The place a lead claim is checked against, as a second source. See [Keys and accounts](../../guides/keys-and-accounts.md) | Whatever your CRM costs | Exports on a schedule | Yes | A read-only report token is enough |
| A model [API key](glossary.md#api-key) | A key that lets a script call Claude directly | Only for jobs that call a model from a script. See [Keys and accounts](../../guides/keys-and-accounts.md) | See current prices at https://claude.com/pricing | Run the step inside a Claude Code [session](glossary.md#session) | Yes | Set a spending limit before the first scheduled run |

## Which skills work without a paid platform

All six. The ledger, the brief, the inventory, the job runner and the metric check read files and folders on your machine. `metric-check` reads the exports you give it, so a team with only Search Console, Bing Webmaster Tools and GA4 can still run it, with fewer independent sources and more figures labeled [single-source](glossary.md#single-source).

## Total cost

The required payments are the Claude plan, plus whatever you already pay for the platforms above. This kit adds no subscription of its own. Paid help (see the help box in [start here](start-here.md)) buys time to fit the habits to your stack, and it never buys a withheld step.

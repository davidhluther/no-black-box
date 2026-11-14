# Shopping List

Every dependency the team kit touches. For each: what it is, why it is there, what to expect on cost, a cheaper or free route, whether you can skip it, and where you have room to choose. No vendor price appears here, because none was checked on the vendor's own page for this release. Each cost cell points to the page that holds the current terms. Accounts and keys are explained in [Keys and accounts](../../guides/keys-and-accounts.md).

| Item | What it is | Why it is here | Cost | Free or cheaper route | Skip it? | Room to choose |
|---|---|---|---|---|---|---|
| [GA4](glossary.md#ga4) | Google's visit and [event](glossary.md#event) counter | Visits, events, key events, the AI referral channel | See current terms at https://marketingplatform.google.com/about/analytics/ | None; the kit assumes it | No | Add a second analytics tool if you have one |
| [Google Tag Manager](glossary.md#google-tag-manager) | Where tracking pieces are added without editing the site | `ga4-events-setup` | See current terms at https://marketingplatform.google.com/about/tag-manager/ | Ask your developers to add each event by hand | Yes, if developers own tracking | [Tag](glossary.md#tag) Manager or developers |
| [Search Console](glossary.md#search-console) | Google's report of search visibility | `gsc-read`, `ai-traffic-classifier`, direction checks | Free; see https://search.google.com/search-console/about | None needed | No | None |
| [Bing Webmaster Tools](glossary.md#bing-webmaster-tools) | Microsoft's version of Search Console | An independent second source for search direction | See current terms at https://www.bing.com/webmasters | None needed | Yes, but the direction check gets weaker | Add whenever |
| A paid SEO platform | Ahrefs, Semrush or similar | Rank and backlink context, a third source for search direction | See current pricing at https://ahrefs.com/pricing or https://www.semrush.com/pricing/ | Search Console plus Bing covers direction | Yes | Any platform; the skills do not call one |
| An AI-visibility platform | A service that tracks how often AI answers mention or cite you | A second source for AI direction beside GA4 referrals and your own question battery | See the vendor's current pricing page | The question battery from the [AI search kit](../ai-visibility/start-here.md) | Yes | Two platforms is better than one |
| [Clarity](glossary.md#clarity) | Microsoft's behavior analytics | `clarity-analytics`; a view of AI crawlers and AI visits | Free, per its home page, "free forever" (checked 11/13/2026); https://clarity.microsoft.com | None needed | Yes | Add when you want it |
| [Looker Studio](glossary.md#looker-studio) | Google's dashboard tool | The dashboard leaders open | See current terms at https://lookerstudio.google.com | Charts inside the sheet | Yes | Looker Studio or your BI tool |
| A [CRM](glossary.md#crm) and [marketing automation](glossary.md#marketing-automation) platform | Where leads and pipeline live | The independent source for "did leads move" | Whatever you already pay for | None needed | No, if you report leads | Your existing stack |
| A [CMS](glossary.md#cms) with an [API](glossary.md#api) | Your publishing system | Only for change-log automation; reading publish dates saves a manual log | Whatever you already pay for | Keep the [change log](glossary.md#change-log) by hand | Yes | Optional |
| A Google Cloud project and [service account](glossary.md#service-account) | A login that belongs to a program | The read-only Search Console reader | See https://cloud.google.com/pricing; reading Search Console this way uses no paid service | Use the Search Console web export | Yes, if you export by hand | Per team, not per person |
| Claude Code | A program that runs Claude on your computer, with tools | Runs every script-backed [skill](glossary.md#skill) | See current plans at https://claude.com/pricing | The prompt-only skills run in Claude.ai or ChatGPT | No, for the full cycle | A shared machine or each person |
| Model API keys | Keys to an AI company's developer service | Only if you add the question battery from the AI search kit | See each company's pricing page; set a monthly cap before first use | Skip the battery and use platform data | Yes | One company is enough |
| [Python](glossary.md#python) 3 | A programming language the helper scripts use | Scripts for capture, checks and export | Free; https://www.python.org/downloads/ | None | No | None |
| A [scheduler](glossary.md#scheduler) | Your computer's or server's built-in way to run a command at a set time | Scheduled pulls | Built in to most systems | Run by hand on the calendar | Yes, if you accept manual runs | Your platform's scheduler |
| A password manager or secrets store | A locked place for tokens and keys | Keeps secrets out of files and screenshots | See the vendor's page | A locked, access-controlled shared vault | Advised | Whatever your security team approves |

## Which skills work without a paid platform

All eight. Nothing in the kit calls a paid SEO or AI-visibility platform. `metric-check`, `monthly-report` and `evidence-review` take whatever numbers you give them, so a platform export, a screenshot transcribed into a table or an API pull all work. Paid platforms add independent sources. They never replace the second-source rule, they feed it.

## Keys and where they live

- Search Console reader and Clarity [token](glossary.md#token). Created and stored in [MM-FU-02](../measure/setup/MM-FU-02-give-the-scripts-read-only-access.md). Read access only.
- Model API keys, if you use the question battery. See [AV-FU-02](../ai-visibility/setup/AV-FU-02-get-and-store-your-keys.md).
- No key ever goes in `config.json`, a report, a ticket or a chat.

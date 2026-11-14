# Microsoft Clarity: what's API-accessible vs. dashboard-only

Verified against Microsoft Learn and the Clarity blog on **2026-08-26**. Every
row cites the page it came from. Doc `ms.date` / `updated_at` values are noted
because Clarity ships fast and this table will rot — re-check before trusting a
row that matters.

## The whole API surface is one endpoint

```
GET https://www.clarity.ms/export-data/api/v1/project-live-insights
Authorization: Bearer <JWT>
Content-Type: application/json
```

Source: [Clarity Data Export API](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api)
(`ms.date` 2024-11-26, `updated_at` 2025-12-05).

That is the entire documented REST surface. There is no recordings endpoint, no
heatmap endpoint, no bot-analytics endpoint, no citations endpoint, no
project-list endpoint, and no pagination.

**There is no project-id parameter.** The token *is* the project scope — one
token per Clarity project, minted by that project's admin. Anything that talks
about "the Clarity project ID" in an API context is talking about which token
you present. (The project ID does appear in dashboard URLs, which is why the
script still tracks it as a label.)

### Parameters

| Param | Values | Notes |
|---|---|---|
| `numOfDays` | `1`, `2`, `3` | Last 24/48/72 hours **from the moment of the call**. Not a date range. |
| `dimension1` | see list | Optional |
| `dimension2` | see list | Optional |
| `dimension3` | see list | Optional |

Documented dimensions: `Browser`, `Device`, `Country/Region`, `OS`, `Source`,
`Medium`, `Campaign`, `Channel`, `URL`.

Documented metrics returned: Scroll Depth, Engagement Time, Traffic, Popular
Pages, Browser, Device, OS, Country/Region, Page Title, Referrer URL, Dead Click
Count, Excessive Scroll, Rage Click Count, Quickback Click, Script Error Count,
Error Click Count. The docs add that "additional metrics and dimensions may be
included in the full API response" — i.e. the list is not closed, so never parse
by fixed schema.

### Hard limits (all quoted from the API doc)

- **10 requests per project per day.** Exceeding returns `429 TooManyRequests`.
- **1–3 days of data only.** No historical backfill of any kind.
- **3 dimensions max per request.**
- **1,000 rows per response, no pagination.** Rows beyond that are simply gone.
- Response is in **UTC**.

Error codes: `401` (missing/invalid/expired token), `403` (token not authorized),
`400` (bad params), `429` (daily limit).

Two consequences worth stating plainly, because they drive the whole workflow
design: (a) the 3-day window means **history only exists if we keep it** — the
API cannot answer "what happened last month," so a scheduled pull that appends
to a local time series is the only way to get one; (b) 10 requests/day means a
pull plan, not ad-hoc querying.

### Known reliability wart

[microsoft/clarity#1085](https://github.com/microsoft/clarity/issues/1085)
(filed 2026-05-15, since closed): the endpoint returned `500` with
`Content-Length: 0` and an empty body for every request against a healthy
project with a valid token, reproducible across parameter combinations. A
similar earlier report (#812) was closed without resolution. The takeaway for
tooling: surface the raw status code and body rather than swallowing an empty
response as "no data."

## Dashboard-only (no API)

| Surface | What it gives | Setup | Export path |
|---|---|---|---|
| **Session recordings** | Individual replays, Highlights clips, Copilot summaries over up to 250 recordings | Tracking code | UI; bulk export of replay **URLs** after filtering; the MCP server can *list* recordings |
| **Heatmaps** | Click / scroll / area / attention / conversion maps | Tracking code | Share link, image export |
| **AI Visibility → Citation** | Page citations, **Share of authority**, AI referral traffic %, **Grounding queries**, My cited pages | Domain verification only (tracking code **or** GSC **or** Bing Webmaster Tools) | Dashboard CSV/PNG/PDF download |
| **AI Visibility → Bot Activity** | Bot operator, AI request share, bot activity by category, path requests, request-status breakdown, content-type card, robots.txt **violations** card | **Requires connecting a CDN/edge provider** — see below | Dashboard CSV per widget |
| **AI Scrape-to-Referral Ratio** | Scrape volume vs. referral traffic per AI operator; click through to recordings filtered to that AI source | Bot Activity setup **plus** referral data | Widget CSV |
| **Copilot / Chat** | Natural-language Q&A over dashboard data, heatmap insights, recording summaries | Built in | — |
| **Smart events, funnels, segments, dashboard cards generally** | — | Tracking code | Dashboard CSV / PNG / PDF, whole-dashboard or per widget ([download doc](https://learn.microsoft.com/en-us/clarity/insights/download-dashboard)) |

### The Bot Activity prerequisite is the big one

From the [FAQ](https://learn.microsoft.com/en-us/clarity/faq) (`updated_at`
2026-08-24): *"Is Bot Activity tracking available by default? **No.** Bot
Activity becomes available after you connect a supported CDN or edge provider,
including Fastly, Cloudflare, or Amazon CloudFront."* The FAQ elsewhere also
names Azure Front Door; WordPress sites get it automatically via the current
Clarity plugin.

It reads **server-side logs**, not the JS tag — which is exactly why it can see
crawlers at all, and exactly why a site whose CDN isn't on that list gets
nothing. Microsoft also warns the integration **may cost money on the provider
side** (log access, egress, processing), billed by the provider, not Microsoft
([cost considerations](https://learn.microsoft.com/en-us/clarity/ai-visibility/cost-considerations-bot-activity-integrations)).

**Vercel is not on the documented supported list** as of the pages read on
2026-08-26. That is a documentation observation, not a claim that it will never
work — the onboarding flow in Clarity lists supported providers *and upcoming
integrations*, so check the live list in Settings → AI Visibility before
concluding anything for a Vercel-hosted property.

### Citations needs no CDN

Worth separating from Bot Activity because it changes who can use it: the
Citation dashboard needs only **domain verification**, and GSC or Bing Webmaster
Tools counts. Grounding queries — "the queries that AI systems used to retrieve
your content before generating an answer" — are the single most interesting
free AEO artifact in the product, and they are dashboard-only.

Caveat carried in Microsoft's own Share-of-authority definition: it is computed
**daily, over queries where your domain was cited at all** — days with no
citation for a query are excluded, which Microsoft says "may lead to higher
Share of authority values compared to broader calculations." It is not a share
of all AI answers. Don't put it in a deck as one.

## Retention and sampling (from the FAQ)

- **Recordings: 30 days.** Favorites and a random sample are kept up to 9 months.
- Labels: up to 9 months.
- Collection is **not sampled** — Clarity states no traffic limits and no
  partial-traffic tracking, on a free-forever product.
- **Heatmaps are sampled for display**: capped at 100,000 page views per heatmap,
  and "the displayed data is dependent on the sample impression on which the heat
  map is created."

The 30-day recording window plus the 3-day API window is the reason this skill
insists on scheduled capture into project-local storage. Anything not captured
is unrecoverable.

## The Clarity MCP server

[`@microsoft/clarity-mcp-server`](https://learn.microsoft.com/en-us/clarity/third-party-integrations/clarity-mcp-server)
(`updated_at` 2026-06-29), run as
`npx @microsoft/clarity-mcp-server --clarity_api_token=...`. Three tools per the
[repo README](https://github.com/microsoft/clarity-mcp-server):
`query-analytics-dashboard`, `list-session-recordings`,
`query-documentation-resources`.

It uses the same Data Export token and, per the Learn page, the same limits — 10
requests/day, 3 days, 3 dimensions. `list-session-recordings` is the one
capability with no documented REST equivalent. Microsoft's stated roadmap for it
includes raising the API request limit, predictive heatmaps, and multi-project
support.

**Not adopted by this skill.** Two reasons: it puts a live project token
into an MCP client config where another person or program on the machine could reach it, which
the one-token-per-project rule in SKILL.md forbids; and natural-language querying against a
10-call/day budget burns the budget on retries. Reconsider if the multi-project
and higher-limit roadmap items ship with per-project scoping.

## Page-level export test (large site, 10/29/2026)

One live call with `dimension1=URL` (numOfDays=1) on a large site hit the 1,000-row cap on every metric. The rows returned were not the busiest pages; they were an arbitrary subset. They covered about half of that day's sessions, included localhost, and 744 rows had query strings. Some important pages were missing entirely. Adding `Device` as a second dimension only makes the cap worse.

So the export API cannot give reliable page-level frustration metrics for a large site. For page-level dead clicks, rage clicks, quick backs, script errors and layout shift on named pages, read the Clarity dashboard filtered by "Visited URL contains" instead. That view keeps 30 days.

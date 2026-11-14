# Check direction on more than one source

Never trust one platform's figure, or one platform's direction of change, alone.

## Which sources are independent

| Question | Independent sources (use at least two) | Counts as one source |
|---|---|---|
| Did search traffic move? | Google Search Console, Bing Webmaster Tools, GA4 organic search sessions, a rank tracker | Search Console in the browser, its export, its API, and any tool that only shows Search Console data |
| Did visits and leads move? | GA4, your email or form tool, your customer list or CRM, ad platform reports | Two dashboards that read the same GA4 property |
| Did AI visibility move? | An AI-answer tracker, a manual set of questions you ask yourself each month, GA4 AI referral traffic, Clarity AI channel | Two views of the same tracker |

## Rules

1. Direction (up, down or flat) needs two independent sources for the same window.
2. The windows must match exactly. Check each source's first date of history before trusting a "before" period.
3. Compare comparable measures over the same pages, channel and dates.
4. Different measures moving apart is context, not a conflict.
5. Comparable sources that disagree mean "direction disputed". Do not act on the figure until you know why. Usual reasons: history that starts late, address variants, different time zones for day boundaries, filters.
6. No second source available means "single-source". Say so in the report.
7. Volume or difficulty figures from different tools: report the middle value and the spread. If the highest is more than one and a half times the lowest, mark the figure uncertain and do not let it decide a ranking on its own.
8. Record which sources agreed.

## Why

A late-starting data feed once made the "before" period look short, so falling pages read as growing. Two tools that both read the same upstream data agreed with each other and disagreed with the third source, which was right. Agreement among tools that share a source is a consistency check, not corroboration.

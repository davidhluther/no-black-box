# Impact scoring

## The formula

```
priority_score = (SEO Impact × 0.4) + (Business Impact × 0.4) + ((10 − Fix Effort) × 0.2)
```

All three inputs are 0-10. Higher score = fix first. The 0.4/0.4/0.2
weighting means SEO impact and business impact matter equally, and fix
effort matters half as much as either — a hard-but-important fix still
outranks an easy-but-trivial one, which is deliberate: an audit that always
surfaces the cheap wins first trains the reader to ignore the expensive,
important ones.

## Category defaults (`DEFAULT_SCORES` in `analyse_crawl.py`)

| Category | SEO impact | Business impact | Fix effort | Why |
|---|---|---|---|---|
| Crawlability | 9 | 7 | 3 | A page search engines can't fetch doesn't rank, full stop. Usually a quick fix (a bad redirect, a broken link). |
| Indexability | 8 | 7 | 4 | Similar severity to crawlability, slightly more effort to diagnose (noindex could be intentional). |
| On-page | 5 | 5 | 2 | Real but incremental; title/meta/H1 fixes are typically the cheapest category to execute. |
| Architecture | 6 | 5 | 5 | Depth and orphan issues usually need an internal-linking change, not a one-line fix. |
| Performance | 6 | 6 | 6 | Genuinely valuable but often requires engineering time, not just content ops. |
| Security | 7 | 6 | 3 | HTTPS migration is disruptive to plan but mechanically simple once decided. |
| AI readiness | 6 | 7 | 4 | Business impact skews slightly higher than SEO impact here on purpose — this is the newest, least-established category, and its value is more strategic bet than proven ranking factor yet. |

**These are priors, not facts about any specific site.** A site whose entire
value proposition depends on page speed should weight performance's business
impact higher. A brand-new site with no backlink profile yet should probably
weight crawlability/indexability even higher, since nothing else matters
until search engines can reliably reach the content. Override per engagement
— that's Step 2 in `SKILL.md`, not an afterthought.

## Severity bands

| Score | Severity |
|---|---|
| ≥ 8 | Critical |
| ≥ 6.5 | High |
| ≥ 5 | Medium |
| ≥ 3 | Low |
| < 3 | Informational |

## Category health scoring

Each category starts at 100 and takes a penalty per finding: 15 points for
Critical, 8 for High, 3 for everything else. Overall health is the simple
average across all seven categories — deliberately not weighted, so a
site can't hide a badly broken category behind several healthy ones in the
headline number. Read the category breakdown, not just the overall score.

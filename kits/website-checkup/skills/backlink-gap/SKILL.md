---
name: backlink-gap
description: Looks at who links to a business's website and finds sites that link to its competitors but not to it. Free path covers your own links with Search Console and Bing Webmaster Tools. The competitor comparison, with tiered outreach targets, link quality, anchor text, and unusual links, needs a paid link database (Ahrefs) and is full version only. Use when asked about backlinks, link building, who links to us, outreach targets, referring domains, or why a competitor is cited more often by search and AI.
---

# Backlink gap

Works in: Claude Code, Claude.ai, ChatGPT for the free path. The competitor comparison is full version only: Claude Code with an Ahrefs account.

A backlink is a link from another website to yours. Search engines read links as votes. A "referring domain" is one website that links to you (ten links from one site count as one referring domain). "Anchor text" is the clickable words of a link. Domain Rating (DR) is Ahrefs' own zero to 100 score for a site's link strength. It isn't a Google number.

## Ground rules

- Every number names the tool and date it came from. Without a paid tool, don't show competitor link counts at all. Nobody can see them for free.
- A business with a short list of local links is normal. An empty top tier is a finding, not a failure of the method.
- Internal and test addresses (staging, preview sites) found in link lists are for the owner's web person, and stay out of anything shown to outsiders.

## Free path: your own links

1. Search Console, Links report. Read top linking sites, top linked pages, and top linking text. The report shows a sample, not everything, and says so.
2. Bing Webmaster Tools, inbound links, for a second view. Sites that appear in one and not the other are normal.
3. Ahrefs Webmaster Tools lets a site owner see their own link profile for a verified site. Check Ahrefs' site for the current terms before you rely on it.
4. Sort what you see. Count how many links use only the business name, how many use a service phrase, and how many use an old business name. Look for linking sites you don't recognize in bulk, since spam arrives on new sites quickly and a formal disavow (a file telling Google to ignore links) is for real infestations only.
5. Free substitute for a gap list. Find the nearby sites that matter for a local business, such as the chamber of commerce, the local newspaper, the community calendar, trade associations, suppliers, and schools. Search for each competitor's name to see who mentions them, and list the local organizations they appear on that the business doesn't. This finds the best local targets, but it can't count links.

## Full path: competitor gap with Ahrefs

1. Settle the competitor set. Use at most six. Add the business's other domains (old names, sister sites) to an exclusion list.
2. For the business and each competitor, pull current referring domains, Domain Rating, and 12 months of referring-domain and DR history.
3. Pull referring domains (follow links only, seen within the last 90 days, one row per domain). Drop links last seen over 90 days ago and nofollow-only links.
4. Find the intersect. A site that links to at least three competitors (at least two when you compare fewer than five) and doesn't link to the business is a gap target. Remove sites that already link to the business, the business's own domains, and sites flagged as spam.
5. Add each target's rating, traffic, how many competitors it links to, and the page it linked to. Label it as matching the business's field, regional, general business directory, or unrelated. Drop unrelated ones.
6. Tier:
   - Tier 1: DR 60 or higher, links to four or more competitors (all of them in a small set), relevant. High-touch outreach.
   - Tier 2: DR 40 to 59, links to two or three competitors, relevant. Medium-touch.
   - Tier 3: DR 20 to 39. Batch outreach candidates.
   - Local relevance list: relevant local sites below DR 20. For a local business, relevance beats rating. Exclude paid-listing directories.
7. Read the anchor profile. A profile that is almost all brand-name anchors with no service phrases is a plausible reason a business is rarely cited in AI answers. State it as a likely cause, not a proven one.
8. Scan the top 30 linking domains for stale high-authority links (candidates to ask for a fix) and old-brand domains that could redirect.

## Output

A note of 300 to 600 words and a spreadsheet of targets with columns: domain, tier, rating, competitors linking, top competitor page, angle for the outreach, and source. List the top ten with a suggested angle each. When the paid tool wasn't available, say so on the first line and give only the free path.

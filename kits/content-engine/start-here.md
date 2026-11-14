# Content Engine: Start Here

Fifty pages a quarter, and nobody can say which ones worked. Briefs get written for topics a colleague already covered. A draft goes live with a statistic nobody can source. Leaders ask what the content program is producing, and the answer depends on which tool you open. Most of that comes from stages that live in different places and gates that exist only in one editor's head.

The content engine puts the whole path in one set of small, separate [skills](glossary.md#skill), each doing one job and handing a file to the next, with a named person making every call that matters. It is the full team version of the method in [Idea to live post](../idea-to-post/start-here.md), plus the evidence and voice gates from [Plain writing](../plain-writing/start-here.md), reorganized for a team that runs many pages, more than one site, and a reporting line.

## What your team will have at the end

- A weekly idea pass that reads original sources, grades how far each item can be trusted, and logs every failed [feed](glossary.md#feed) instead of calling a broken week quiet.
- A topic screen that stops duplicates, planned overlaps, and no-demand topics before anyone spends a day on a [brief](glossary.md#content-brief).
- One brief producer with a required [verdict](glossary.md#verdict) (new post, refresh, hold, or skip) and statistics that name a source.
- A draft [queue](glossary.md#queue) that works items one at a time, refuses to start on a stale or blocked [handoff note](glossary.md#handoff-note), and never publishes.
- Four [gates](glossary.md#gate) before a page leaves the building: the article check, the AI-tell score, the copy lint, and an evidence review.
- A publish step with a named approver, a [dry run](glossary.md#dry-run), and proof the live page shows its own title. A [CMS](glossary.md#cms) path covers sites that don't publish through git.
- Refresh candidates ranked from your own search data, and a measurement rhythm at two, six, and 12 weeks.
- A [scheduled job](glossary.md#scheduled-job) log and a check that flags a missed slot the same day, so a quiet failure doesn't pass for a quiet week.
- A one-page summary leaders can read, built from numbers that name their source and survive an evidence review.

## The skills and who they serve

| Stage | [Skill](glossary.md#skill) | What it does |
|---|---|---|
| Ideas | industry-intel | Weekly pass over feeds and pasted items. Opens the original source, records where a summary drifted, grades confidence A to D, and lists testable claims. |
| Ideas | topic-screen | Checks candidates against existing posts, the queue, each other, and a demand floor. Sorts into go, look again, and drop. |
| Ideas | content-gap | Finds what competitors cover that you don't, and where you appear but rank poorly. Ranks as new post, refresh, or skip. |
| Brief | seo-research | Researches one target search before the brief: demand, who ranks, [search intent](glossary.md#search-intent), real questions, traceable statistics. |
| Brief | content-brief | The only brief producer. Redundancy check, verdict, outline, verified statistics, internal links. A refresh mode covers existing pages. |
| Brief | brief-layer | Adds search and AI-answer structure to a brief, or checks a draft against it. |
| Draft | seo-draft | Writes the article from a finished brief and your style guide. Stops with no brief or no style guide. |
| Draft | draft-queue | Moves up to three Planned items through drafting to Ready to publish. Person present, one item at a time, never publishes. |
| Draft | voice-presets | Three ready-made voices (Quick Take, Analyst Memo, Straight Talk) on top of your style rules. |
| Gates | article-check | Script that flags banned words, formulaic transitions, weak headings, missing links, and uncited statistics. |
| Gates | tell-scorer | Scores AI-sounding habits per rule, compares before and after a rule change, and can gate recently published pages. |
| Gates | copy-lint | Checks the words a site actually shows: menus, buttons, captions, titles. |
| Gates | evidence-review | Grades claims, requires a dated source for every number, and tests cause-and-effect claims before they reach leaders. |
| Package | cta-inject | Adds calls to action to published posts that lack them. |
| Package | docx-export | Bundles the final text, shares, and brief into one Word file for reviewers who work in Word. |
| Publish | content-handoff | One-page note on which inputs are fresh, stale, or missing, with a plain-language summary for a manager. |
| Publish | publish | One repeatable path to live. Approval by exact words, a dry run, and a live-page check. A CMS adapter pattern covers non-git sites. |
| Measure | content-refresh | Ranks old posts worth updating, then carries one through to an updated draft. |

The skills are the same ones the two small-business kits ship, so the method is already tested. This kit adds what a team needs around them, covered in the four [setup guides](setup/CE-FU-01-install-and-set-up-the-team-config.md): scheduling with a log that catches missed runs, many sites and markets, who owns what, and how results reach leaders.

## What it needs

- [Claude Code](glossary.md#claude-code) and a Claude plan or [API](glossary.md#api) access your team can pay for.
- [Python](glossary.md#python) 3.9 or newer.
- Read access to [Search Console](glossary.md#search-console) for each site. [Bing Webmaster Tools](glossary.md#bing-webmaster-tools) and [GA4](glossary.md#ga4) help.
- **A way to publish.** A git repository you can merge to, or a CMS key that can create drafts.
- **Optional.** An SEO platform, an AI-visibility platform, a [CRM](glossary.md#crm) export, and a reporting surface such as [Looker Studio](glossary.md#looker-studio).

The [shopping list](shopping-list.md) names each one, says what it costs or where to check, and says which skills still work without it.

## What it does not do

It doesn't promise rankings, and it doesn't decide for you. The screens and gates say look, not kill. A passing check proves the known problems are gone, not that the page is good, so a person reads every draft. It never publishes from a schedule. It doesn't connect to your platforms for you beyond the reads described in the guides, and where two platforms disagree it asks you to say why instead of averaging them. See [what-david-built](what-david-built.md) for the reasoning.

## Where to start

Start with [CE-FU-01](setup/CE-FU-01-install-and-set-up-the-team-config.md). A smaller team, or one person on a thin budget, can run the same method for free or low cost; see [choose your version](choose-your-version.md).

> **Want it fitted to your stack?** Pigasus Group sets these up for in-house teams: your platforms, your CMS, your reporting cadence. Start at https://pigasus.group/contact.

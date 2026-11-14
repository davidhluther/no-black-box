# AI Visibility Program

Leaders ask whether AI search is costing you demand, and three tools hand you three different answers. Nobody can say which questions were asked, whether the "mention" was your brand or a look-alike, or whether last month's change is real or just the model answering differently today. This kit turns that into a program your team can run, defend and hand to the next person.

## What the team has at the end

- A fixed [question set](glossary.md#question-set) per site or market, [frozen](glossary.md#frozen) so a change in the answers can never be blamed on a change in the questions.
- A [same-name](glossary.md#same-name) check for every brand, product line and competitor you track, so a look-alike does not inflate anyone's numbers.
- A scheduled monthly run across every site, with a [ledger](glossary.md#ledger) that records each attempt, a retry when one fails, and a same-day alert when a [slot](glossary.md#slot) is missed.
- A named owner, backup and reviewer for every site, and a rule that no number goes to leaders before the [noise audit](glossary.md#noise-audit) has cleaned it.
- A monthly leader report that puts the question battery beside [Search Console](glossary.md#search-console), [Bing Webmaster Tools](glossary.md#bing-webmaster-tools), [GA4](glossary.md#ga4) and any paid AI-visibility platform you already own, and says why they disagree before it says what to do.
- A short list of website and listing fixes with an owner, and a check afterward that each one went live.

## The black box

AI-visibility platforms return a score or a share-of-voice percentage. Most of them show little of the method: which prompts, how often, which model version, how a brand was matched. When two platforms disagree, nobody can tell why. Everything here is visible. The questions are plain text, the answers are saved verbatim, every removal from a count is tied to a quoted line, and the refusal to compare unlike runs is built into the scripts.

## This is the team version

The single-site kit, [AI visibility check](../ai-visibility/start-here.md), teaches the method with a Google Sheet and free AI apps. This kit reuses its 14 skills unchanged and adds what changes at team scale: many sites and markets, who owns what, a schedule that cannot fail quietly, and a path from the numbers to a leadership meeting. Setup is four short guides. [Choose your version](choose-your-version.md) says when a smaller kit is the better fit.

## The skills

Each skill is a folder of written instructions that [Claude Code](glossary.md#claude-code) follows. They are the same ones the single-site kit ships, with the same behavior.

| Skill | What it does for the program |
|---|---|
| `question-battery` | Builds the frozen question set per site and runs it through each AI company's developer service with your own keys. |
| `battery-preflight` | Finds names that collide with your brand, product or competitors, before the first run and whenever a name is added. |
| `answer-noise-audit` | Cleans a scored run, shows raw and clean counts side by side, and measures how much one question varies on its own. |
| `aeo-audit` | Chains the analysis skills for one site and writes a one-page summary. |
| `aeo-visibility` | Counts how often each brand is named and cited, with denominators. |
| `aeo-mentions` | Reads what the answers say about you and checks claims against your site. |
| `aeo-citations` | Lists the sources the answers cite, checks the links are real, and shows who owns each answer. |
| `aeo-competitive` | Shows who wins the answers you should be in, and how often the answer is a product instead of a company. |
| `aeo-platforms` | Compares ChatGPT, Claude, Gemini and Perplexity without blending them. |
| `aeo-trends` | Reports what changed between runs, and refuses to call one month a trend. |
| `visibility-diff` | Compares two scored runs cell by cell and refuses mismatched runs. |
| `unified-visibility` | Sets every source side by side and explains disagreements. |
| `ai-traffic-classifier` | Flags Search Console queries that look like leaked AI conversation turns, as a floor, not a total. |
| `aeo-implement` | Turns findings into a handoff of site and listing fixes. It publishes nothing. |

## What it needs

- [Claude Code](glossary.md#claude-code) and Python 3 on a computer that can stay on or be scheduled, plus a developer key for each AI company you want to run. The [shopping list](shopping-list.md) names every dependency and which skills work without a paid platform.
- Read access to Search Console, Bing Webmaster Tools and GA4 for each site, as exports or a connector. Skills take exports, so no connector is required.
- A named owner per site, and an hour a month to review scored drafts. The runner scores with a simple match; a person reads each answer.

## Honest limits

Twenty headline questions across four products make 80 answers per site. That is a thermometer, not a ranking, and one cell moving is inside normal answer-to-answer variation. Developer-service answers differ from what customers see in the apps, and the kit keeps the two apart. The program reports direction with its noise level, and it says "[baseline](glossary.md#baseline)" for the first run.

## Where to begin

1. Read [Choose your version](choose-your-version.md) (two minutes).
2. Check the [shopping list](shopping-list.md) for keys and access you still need.
3. Follow `setup/AP-FU-01-set-up-the-program-folder.md`, then guides 02 to 04.

Stuck? Each step has an ID like AP-FU-03-2. The check-up command prints a [support code](glossary.md#support-code) you can send with it. [Fixes](fixes.md) lists the failures a team meets at scale.

**Want it fitted to your stack?** Pigasus Group sets these up for in-house teams: your platforms, your [CMS](glossary.md#cms), your reporting cadence. Start at https://pigasus.group/contact.

## Who made it

David Luther built this method while running AI-visibility measurement inside a large B2B payments company, then generalized it. [What David built](what-david-built.md) tells the story for a hiring manager.

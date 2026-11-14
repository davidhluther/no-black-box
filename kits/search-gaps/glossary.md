# Glossary

Every technical term used in this kit, in plain words. Each page links a term to this page the first time it appears on that page.

<a id="ahrefs"></a>
**Ahrefs.** A paid SEO platform with a large database of who links to whom. It is the source the `backlink-gap` skill is written around.

<a id="ai-model"></a>
**AI model.** The program behind a chat tool such as ChatGPT, Claude, or Gemini. You send a request and it writes a reply.

<a id="anchor-text"></a>
**Anchor text.** The clickable words of a link. A profile made almost entirely of brand-name anchors, with no service or topic phrases, is one plausible reason a company is rarely named in AI answers.

<a id="api-key"></a>
**API key.** A long secret code that proves to a service that a request comes from your paid account. Treat it like a password. It lives in an environment variable (a named setting your computer keeps in memory), never in a file you share.

<a id="backlink"></a>
**Backlink.** A link from another website to yours. Search engines read links as votes.

<a id="baseline"></a>
**Baseline.** The shared snapshot of queries, pages, keywords, and competitors, with a date on it, that every check reads so that no two checks disagree about the same page.

<a id="bing-webmaster-tools"></a>
**Bing Webmaster Tools.** Microsoft's free report for site owners, the Bing counterpart of Search Console. It gives a second view of queries and inbound links.

<a id="cannibalization"></a>
**Cannibalization.** Two or more pages on the same site competing for the same search, so neither wins cleanly. The `cannibalization` skill finds it and the `consolidate` skill plans the fix when merging is right.

<a id="canonical"></a>
**Canonical.** The address a page names as its "real" version when several addresses show the same content.

<a id="claude-code"></a>
**Claude Code.** Anthropic's tool that runs Claude on your own computer, where it can read and write files and run small programs. It runs in the terminal, in a desktop app, and in some code editors.

<a id="cms"></a>
**CMS.** Content management system, the software your site's pages are written and published in. WordPress and Contentful are examples.

<a id="common-crawl"></a>
**Common Crawl.** A nonprofit that archives much of the public web and publishes the archive for anyone. Many AI models draw training data from archives like it. Its crawler is named CCBot.

<a id="config-file"></a>
**Config file.** A plain text file named `config.json` that holds the details specific to your team, such as site addresses and competitors. It never holds keys.

<a id="core-web-vitals"></a>
**Core Web Vitals.** Google's three page-experience measures: how fast the main content appears (LCP), how fast the page responds to a tap or click (INP), and how much the layout jumps (CLS).

<a id="crawl"></a>
**Crawl.** A robot visiting every page of a site and writing down what it finds, the way a search engine does. A crawl export is the spreadsheet of results.

<a id="csv"></a>
**CSV.** A plain table saved as text, one row per line, with commas between columns. Every spreadsheet program opens it.

<a id="domain-rating"></a>
**Domain Rating.** Ahrefs' own zero to 100 score for the strength of a site's links. It is one platform's estimate, so label it that way whenever you report it.

<a id="field-data"></a>
**Field data.** Speed measurements taken from real Chrome visitors. Google uses it. Lab data is a simulated test, useful for finding causes and not for judging severity.

<a id="ga4"></a>
**GA4.** Google Analytics 4, Google's traffic and conversion reporting tool.

<a id="gap-register"></a>
**Gap register.** The kit's single list of findings, one row per gap, each with its evidence, owner, due date, and a check-back date. The template is `templates/gap-register.csv`.

<a id="json-ld"></a>
**JSON-LD.** The format used to put structured data in a page, as a small block of labeled facts that machines read and visitors never see.

<a id="lab-data"></a>
**Lab data.** A simulated speed test on a deliberately slow phone and network. Good for finding causes, unreliable for judging how bad a problem is.

<a id="looker-studio"></a>
**Looker Studio.** Google's free tool for building dashboards from Sheets, Search Console, GA4, and other sources.

<a id="orphan-page"></a>
**Orphan page.** A page that no other page on the site links to, so visitors and crawlers struggle to find it.

<a id="pagespeed-insights"></a>
**PageSpeed Insights.** Google's free speed test at pagespeed.web.dev. It shows field data and lab data side by side.

<a id="persona"></a>
**Persona.** A short written profile of one kind of customer, built from real quotes and used by the `persona-jury` skill.

<a id="plugin"></a>
**Plugin.** A bundle of skills you install into Claude Code in one step.

<a id="prompt"></a>
**Prompt.** The message you send an AI model.

<a id="python"></a>
**Python.** A programming language. Several skills in this kit include small Python scripts, and the check-up tool is one.

<a id="redirect"></a>
**Redirect.** An instruction that sends anyone who asks for an old address to a new one. A permanent redirect (a 301) also passes most of the old page's search standing to the new page.

<a id="referring-domain"></a>
**Referring domain.** One website that links to you. Ten links from one site count as one referring domain.

<a id="robots-txt"></a>
**Robots.txt.** A plain file at the root of a site that tells crawlers where they may go.

<a id="run-log"></a>
**Run log.** The kit's record of every scheduled slot, who owned it, whether it ran, and, when it did not, why and when it was retried. The template is `templates/run-log.csv`.

<a id="screaming-frog"></a>
**Screaming Frog.** A desktop crawler (the SEO Spider) that exports a site's pages as a spreadsheet. The `technical-seo-audit` skill reads its export.

<a id="search-console"></a>
**Search Console.** Google's free report for site owners. It shows real searches, clicks, impressions, and positions for your own site, and a sample of who links to you.

<a id="semrush"></a>
**Semrush.** A paid SEO platform that overlaps with Ahrefs. The backlink skill is written around Ahrefs, so using Semrush data means exporting it and handing the files to Claude.

<a id="seo"></a>
**SEO.** Search engine optimization, the work of making a site easier to find in search.

<a id="skill"></a>
**Skill.** A saved set of instructions that Claude Code loads when a task matches, so the same method runs the same way each time.

<a id="step-id"></a>
**Step ID.** The code at the start of each numbered setup step, such as SG-FU-01-3: kit, version, guide number, step number. Quote it when you ask for help.

<a id="structured-data"></a>
**Structured data.** Labeled facts hidden in a page for computers to read. The `schema-gen` skill writes it as JSON-LD.

<a id="subreddit"></a>
**Subreddit.** One topic community on Reddit.

<a id="support-code"></a>
**Support code.** A short code printed by the check-up command that tells a helper which step failed and which version of the kit you have. It never contains keys or file contents.

<a id="terminal"></a>
**Terminal.** The text window where you type commands. On a Mac it is the Terminal app, and on Windows it is PowerShell.

<a id="verbatim"></a>
**Verbatim.** Word for word. The review and forum skills keep customer quotes verbatim, never paraphrased.

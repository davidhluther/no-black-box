# Shopping List

Every item says what it is, why the kit needs it, what it costs or where to check, a cheaper option, whether you can skip it, and where you get to choose. Prices change and differ by plan, so where this page hasn't verified one today it points to the vendor's page instead. Every account or key is explained in [keys and accounts](../../guides/keys-and-accounts.md). Never paste a key into a chat, a config file, or a shared document.

## Needed to run the kit

### Claude Code and a model plan

**What it is.** The program that runs the skills on your computer ([install guide](../../guides/install-claude.md)), and the paid plan or [API key](glossary.md#api-key) that powers it.

**Why you need it.** Every [skill](glossary.md#skill) here runs inside it. The scripts also run without it, but the briefing, drafting, and review steps are done by the AI model.

**Cost.** See current pricing on Anthropic's pricing page, claude.com/pricing. Team plans and [API](glossary.md#api) billing price differently, and heavy drafting uses more than occasional use.

**Cheaper option.** One shared seat for the person who runs the [queue](glossary.md#queue), while others review in Word or Google Docs.

**Skip it?** No.

**Room to choose.** Plan or API billing, one seat or several. Decide who pays before the first scheduled run, because a billing lapse looks like a failed job.

### Python 3.9 or newer

**What it is.** The programming language the [gate](glossary.md#gate) scripts use.

**Why you need it.** article-check (a [validator](glossary.md#validator)), tell-scorer, copy-lint, topic-screen, the [feed](glossary.md#feed) fetch, and the job log are [Python](glossary.md#python) programs.

**Cost.** Free. Install from python.org.

**Skip it?** No. Without it the skills still draft, but the gates and the schedule don't run.

### A shared work folder

**What it is.** The kit folder with its `ideas`, `briefs`, `drafts`, `queue`, `measure`, `style`, and `ops` folders.

**Why you need it.** It holds briefs, notes, and logs. Briefs and notes name competitors and plans, so keep the folder in a private repository or a shared drive your team already controls, never a public one.

**Cost.** Whatever you already pay for storage.

**Room to choose.** A private git repository gives you history and review. A shared drive is easier to start with.

### A queue

**What it is.** The list of every page in flight and its stage (the [queue](glossary.md#queue)), with owner, site, market, and content type columns.

**Why you need it.** draft-queue and topic-screen read it. Export it to [CSV](glossary.md#csv) so scripts can.

**Cost.** Free in a spreadsheet. Use your project tool if it exports CSV.

**Skip it?** No.

## Data your team probably already has

### Search Console

**What it is.** Google's free tool showing which searches bring people to each site. [Keys and accounts](../../guides/keys-and-accounts.md) shows how to add a user.

**Why you need it.** It is the only source of your own search numbers. content-gap, content-refresh, and the measurement checkpoints read it.

**Cost.** See Google's current terms on the [Search Console](glossary.md#search-console) page; this page didn't verify them today.

**Skip it?** You can start without it and you will be guessing at refreshes. Add read-only access for each site early, because data only starts from verification.

### Bing and GA4

**What they are.** [Bing Webmaster Tools](glossary.md#bing-webmaster-tools) is Bing's version of Search Console. [GA4](glossary.md#ga4) counts visits and conversions. Both are free to sign up for; see [keys and accounts](../../guides/keys-and-accounts.md).

**Why you need them.** A second search source and a traffic source let you test whether a trend is real. Say which source every number came from.

**Skip them?** Bing yes, if your readers rarely use it. GA4, only if your analytics tool already gives you per-page visits and conversions.

### Microsoft Clarity

**What it is.** A free tool recording how visitors use pages. Terms are on [keys and accounts](../../guides/keys-and-accounts.md).

**Why you need it.** It helps explain a refresh candidate with strong traffic and weak engagement.

**Skip it?** Yes. Nothing in this kit needs it.

### A paid SEO platform

**What it is.** A service such as Ahrefs or Semrush that sells keyword volumes, backlinks, and competitor data.

**Why you need it.** It gives volume and difficulty numbers for topic-screen and content-brief, and competitor coverage for content-gap.

**Cost.** See current pricing at ahrefs.com/pricing or semrush.com/prices. API access is priced separately on some plans, so confirm that your plan includes it before building on it.

**Cheaper option.** Search Console impressions, Bing data, and reading results by hand. The skills fall back to these when no platform is configured, and the brief says which source it used.

**Skip it?** Yes. Every skill in this kit runs without one. Volumes are less precise and content-gap leans on your own data.

**Room to choose.** Use the platform you already have. Don't buy a second one to run this kit.

### An AI-visibility platform

**What it is.** A service that tracks whether AI answers mention or cite your pages. See the AI visibility program kit for running that as its own program.

**Why you might want it.** It can change which refreshes you prioritize. The skills here don't connect to it, so bring its numbers in as an export and name the platform and date.

**Skip it?** Yes.

### A CRM export

**What it is.** A report from your customer system showing leads or pipeline by landing page or campaign.

**Why you might want it.** It lets a leader report show outcomes beyond visits. This kit reads exports only and never writes to a [CRM](glossary.md#crm).

**Skip it?** Yes, until someone asks you for it.

### Looker Studio or another reporting surface

**What it is.** [Looker Studio](glossary.md#looker-studio) is Google's free reporting tool. Use whatever your leaders already open.

**Why you might want it.** The kit writes a one-page note and CSV tables. Point a dashboard at the CSVs if leaders want a live view.

**Skip it?** Yes.

## Needed to publish

### A git repository you can merge to, or a CMS key

**What it is.** For a git-based site, an account that can open and merge a [pull request](glossary.md#pull-request), and the GitHub command-line tool `gh`. For a [CMS](glossary.md#cms) site, a key that can create drafts.

**Why you need it.** publish drives either path, a [pull request](glossary.md#pull-request) for git sites or a draft entry for a CMS. Create the CMS key with the least access that works, drafts only and no delete.

**Cost.** Whatever your site already costs.

**Skip it?** Yes, if a person pastes the post into the CMS. Start there and move to draft creation later.

## Which skills work without a paid platform

All eighteen. The ones that read data (topic-screen, seo-research, content-gap, content-refresh) get sharper with a platform, and each says in its output which sources it did and didn't read. A source that could not run is marked incomplete, never clean.

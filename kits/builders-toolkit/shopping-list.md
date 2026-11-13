# Shopping List

Everything you need for the full version, and what you can skip. Prices change, so every cost points to the seller's own page. Nothing was verified for this list as of 11/13/2026, and the one price that matters (the Claude plan) is not quoted here.

Anything that needs an account or a key is explained in the shared guide [Keys and accounts](../../guides/keys-and-accounts.md). This kit needs no outside keys, apart from one optional alert address.

| Item | What it is | Why you need it | Cost | Free or cheaper option | Can you skip it | Room to choose |
|---|---|---|---|---|---|---|
| A paid Claude plan | The account that lets you use [Claude Code](glossary.md#claude-code) | Claude Code is how the [skills](glossary.md#skill) run | See the current plans at https://claude.com/pricing (not verified for this list) | Paying by use instead of by plan is possible, but the plan is simpler for most people | No | Pick the plan that matches how much you use it. Start with the smallest that includes Claude Code |
| Claude Code | The program you type to | It runs the skills | Included with the plan | None | No | Install it with the guide [install-claude](../../guides/install-claude.md) |
| A computer you can leave on | A Mac, Linux or Windows machine | [Scheduled jobs](glossary.md#scheduled-job) only run while the machine is awake | Whatever you already own | A small always-on computer or a hosted [scheduler](glossary.md#scheduler) | Yes, if you will not run scheduled jobs | A cheap always-on machine suits `scheduled-jobs`, and nothing else in the kit |
| [Python](glossary.md#python) 3 | The language the kit's small programs are written in | The checkers and runner are Python files | Free, from python.org | None needed | No | Any recent version works. Newer Macs may already have it |
| [Git](glossary.md#git) | Tracks your project's history | The ledger and briefs are meant to be committed | Free | None | You can skip it, but then you lose history | None |
| A web browser for the [design gate](glossary.md#design-gate) | A [Playwright](glossary.md#playwright)-controlled [Chromium](glossary.md#chromium) browser | The design gate needs a real browser to lay pages out | Free. Playwright downloads one for you | An installed Chrome also works | Yes, if you build no websites | Skip the gate and keep the other four skills |
| A place to run your site locally | Your own site's [development server](glossary.md#development-server) | The gate needs your site running on your computer | Free | A built copy of the site served from a folder (`--serve`) | Yes, if you build no websites | Depends on how your site is built |
| An alert address (optional) | A web address that accepts a message, such as a chat channel's incoming-message address (a [webhook](glossary.md#webhook)) | Lets `scheduled-jobs` tell you when a job is stuck | Many chat tools offer this free. See your tool's own page | Read the flags file by hand | Yes | Keep the address in an [environment variable](glossary.md#environment-variable), not in files you share |

## Total cost

The only required payment is the Claude plan. Everything else is free. Because this kit needs no extra paid tools, there is no paid upgrade path. Paid help (see "Want this set up for you?" in [start here](start-here.md)) buys David's time to fit the skills to your own projects, and it never buys a withheld step.

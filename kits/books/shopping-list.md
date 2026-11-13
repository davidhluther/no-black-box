# Shopping List

This kit only looks at your books. It never changes them.

Everything this kit might use, with what it costs and whether you can skip it. All prices were read from the vendor's own page on 11/13/2026. They change, so check before buying. Every account below is explained in the shared guide [Keys and accounts](../../guides/keys-and-accounts.md).

| Item | What it is | Why you need it | Cost | Free or cheaper option | Can you skip it? |
|---|---|---|---|---|---|
| QuickBooks Online | The accounting program your organization already uses | It holds the books this kit reads | Plans from $38 a month at the regular price for Simple Start (checked 11/13/2026); Intuit often discounts the first months. See the current price at https://quickbooks.intuit.com/pricing/ | Your organization already has it | No, this is what the kit reads |
| A QuickBooks login you can export from | A user on the company with reports access | Needed to export reports or approve the [connector](glossary.md#connector) | Included | Ask the administrator to add you with report-only rights | No |
| Google account | A free account with Google Sheets and Drive. Setup help: [Keys and accounts](../../guides/keys-and-accounts.md). | Holds the cash sheet and [check-up](glossary.md#check-up) button | Free | Google Workspace for Nonprofits may be free for eligible organizations; check eligibility at https://www.google.com/nonprofits/ | No for free and low cost; yes for full if you prefer spreadsheet files on your computer |
| A free AI model | ChatGPT, Claude, or Gemini on a free plan. Setup help: [Keys and accounts](../../guides/keys-and-accounts.md). | Reads pasted reports and answers questions | Free | Pick any one | Only if you do the checks by hand |
| One paid AI plan | Claude Pro or ChatGPT paid plan. Setup help: [Keys and accounts](../../guides/keys-and-accounts.md). | Needed to use the QuickBooks connector comfortably and to upload skills | Claude Pro is $20 a month with monthly billing (checked 11/13/2026); for ChatGPT see the current price at https://chatgpt.com/pricing | Use the free plan with the free version | Yes, unless you want the live connector |
| Intuit's QuickBooks connector or [plugin](glossary.md#plugin) | Intuit's official add-on for Claude and ChatGPT. Setup help: [Keys and accounts](../../guides/keys-and-accounts.md). | Lets the AI model look at live books | No separate price is stated in Intuit's announcement; a QuickBooks Online subscription is required (checked 11/13/2026) | Free version's exports | Yes |
| Intuit developer account | A free sign-up at developer.intuit.com. Setup help: [Keys and accounts](../../guides/keys-and-accounts.md). | Needed only for the full version's [script](glossary.md#script) | Free to sign up (see the current terms at https://developer.intuit.com) | None needed | Yes, unless you want the full version |
| A computer with [Python](glossary.md#python) | A common programming language, already on many Macs | Runs the script | Free; install from https://www.python.org/downloads/ if missing | None | Yes, unless you want the full version |
| Claude Code | A program that runs Claude on your own computer | Runs the full version's skills | See the current price at https://claude.com/pricing | You can run the script by hand without it | Yes |
| A bank statement each month | The paper or PDF from your bank | The only proof of what the real balance is | Free | None | No. Nothing here replaces it |
| A bookkeeper or CPA | A person who knows your organization | Final say on corrections and taxes | Varies | This kit cuts the hours you pay for | Yes, but do not skip tax advice |

## Room to choose

The AI model is your call. The [prompts](glossary.md#prompt) in `free/prompts.md` work in ChatGPT, Claude, and Gemini alike. If you already pay for one, use it. Privacy-minded organizations can remove names from exports before pasting them; guide BK-FR-01 shows how.

If your organization does not use QuickBooks Online, the free version's questions still work on any report you can export, but the connector and the script are QuickBooks Online only. QuickBooks Desktop is a different product and is not covered.

## Where the keys go

You will see three kinds of secret in the full version: a [client ID](glossary.md#client-id), a [client secret](glossary.md#client-secret), and a [refresh token](glossary.md#refresh-token). They never go in a shared file, a chat, an email, or a screenshot. The shared guide [Keys and accounts](../../guides/keys-and-accounts.md) shows where they are kept and how to keep them out of sight.

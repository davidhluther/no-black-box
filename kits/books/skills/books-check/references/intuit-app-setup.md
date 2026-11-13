# Intuit Developer App Setup

The hard part of the full version. The user-facing walkthrough is guides BK-FU-01 to BK-FU-03 in the kit. This page is the short version for an agent helping someone, with what was and was not verified.

Checked 11/13/2026. Intuit's developer documentation pages are rendered by script (a small program saved as a text file), so their text could not be read directly today. Details marked "reported" come from third-party guides and a web search that quoted Intuit's own authorization FAQ. Verify them on https://developer.intuit.com before depending on them.

## The shape of it

1. Create a free developer account at developer.intuit.com.
2. Create an app on the platform "QuickBooks Online and Payments". Select only the accounting scope (the kind of access a sign-in asks for), `com.intuit.quickbooks.accounting`.
3. Development keys and production keys (keys that work on your real company file) are separate. Development keys work with a sandbox (a practice company with invented data). Production keys work with a real company file. Reported: production keys require Intuit to review an app assessment questionnaire, and reviews may take one to two weeks.
4. Redirect addresses. Reported from Intuit's authorization FAQ: Intuit's sign-in server only redirects to addresses that begin with https, and does not accept IP addresses. A plain local address works only with development keys. That is why this kit signs in through Intuit's own OAuth Playground (Intuit's own page for signing in once and getting the keys), whose redirect address you add to your app's list.
5. In the Playground: choose the app, pick the accounting scope, approve in QuickBooks, pick the company, then ask for tokens. Copy the refresh token (a longer-lived pass that gets new short-lived ones) and the company ID (the company's number, which Intuit labels `Realm ID`).
6. Access tokens (a short-lived pass for reading your books) last about an hour. Refresh tokens last about 100 days on a rolling basis, and Intuit can return a new refresh token every time one is used (reported). Always keep the newest. The script saves it in a private file. Two third-party blogs report a newer hard cap of five years on refresh tokens. That was not confirmed on Intuit's pages.
7. Keys live only in environment variables (named settings stored on your computer outside any shared file): `QBO_CLIENT_ID`, `QBO_CLIENT_SECRET`, `QBO_REFRESH_TOKEN`, `QBO_REALM_ID`, `QBO_ENV`. Never in a config file, a chat, or a screenshot.

## API addresses used by the script

- Reports and queries: `https://quickbooks.api.intuit.com/v3/company/<company ID>/reports/<ReportName>` and `/query`. Sandbox uses `https://sandbox-quickbooks.api.intuit.com`.
- Token exchange: `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer`. This is the only POST the script ever sends, and it goes to Intuit's sign-in service, not to the books.

## Costs

The developer account is free to create (see current terms at developer.intuit.com). Reported: since July 2025 Intuit meters data reads for apps through its App Partner Program, with a free tier large enough for hundreds of thousands of reads a month. The script makes a few dozen requests at most per session. Confirm on Intuit's current page.

## Common failures

- `invalid_grant` or HTTP 401 on refresh: the refresh token is old or was pasted wrong. Get a fresh one from the Playground.
- Redirect mismatch in the Playground: the address on the app's list differs from the Playground's. Copy it exactly, for the same set of keys, Development or Production.
- HTTP 403: the authorizing login cannot see the company, or sandbox and production were mixed.
- Production keys locked: Intuit's review is not finished or a questionnaire field is missing.

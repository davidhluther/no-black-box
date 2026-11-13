# Setting up a Clarity token

You do this once per Clarity project. It takes about five minutes. Only a Clarity project admin can make a token, and it needs a sign-in, so an AI model cannot do it for you.

## What a token is

Microsoft Clarity (a free tool that records how visitors use your site) has a data export that needs a token, a long password-like string that proves you may read one project's data. The token is the project's scope: the export has no "project" setting, so whichever project the token belongs to is the data you get. Keep one token per project.

## Steps

1. Sign in at clarity.microsoft.com and open the project.
2. Open Settings, then Data Export, then Generate new API token.
3. Name it. The name must be 4 to 32 characters, using letters, digits, hyphens, the _ character and periods, with no spaces, and unique within the project. A good name is `clarity-export-my-site`.
4. Copy the token. Clarity shows it only once.
5. Give the token to your computer through an environment variable (a setting your computer remembers for a program). The variable is named after your project label: uppercase it and turn anything that is not a letter or digit into the _ character. For a project you call `my-site`:

   ```bash
   export CLARITY_TOKEN_MY_SITE='paste-the-token-here'
   ```

   Put that line in the file your terminal reads at start (usually `~/.zshrc`), then close and reopen the terminal. If you only ever use one Clarity project, the single variable `CLARITY_API_TOKEN` works as a fallback.
6. Test the request without using the token or the network: `python3 scripts/fetch_clarity.py --project my-site --dimensions Source --dry-run`. You will know it worked when it prints the exact address, settings and an equivalent `curl` command.
7. Do a real pull: `python3 scripts/fetch_clarity.py --project my-site --days 1 --dimensions Channel --out ./measurement/clarity`. You will know it worked when a file named `my-site-<date>.json` appears in that folder.

## If something goes wrong

| What you see | What it means |
|---|---|
| "No Clarity API token found" | The variable name does not match the project label, or the terminal was not reopened. Check the name in step 5. |
| `HTTP 401` | The token is missing, wrong or expired. Make a new one in Settings, Data Export. |
| `HTTP 403` | The token is not allowed for this action. A project admin must make it. |
| `HTTP 429` | You used the 10 requests a day Microsoft allows for this project. Wait for the next UTC day. |
| Empty-bodied `HTTP 500` | A known intermittent Clarity problem. Try again later. It does not mean "no data". |

## Keeping the token safe

- Never paste a token into a chat, a file inside a project folder, or a screenshot. The script refuses to read a token file from inside a git folder.
- Replace a token whenever someone with project access leaves. The replace control is on the same Settings page.
- Do not move a token between organizations. Each organization's data stays in its own folder.

## Two AI-visibility settings worth doing at the same time

1. Verify your domain for the Citation dashboard (the fast path is a connected Search Console or Bing Webmaster Tools account). It is free and needs no other setup.
2. Decide whether the Bot Activity feature is worth connecting to your site's content delivery network (CDN, the service that serves your pages from servers near your visitors). Bot Activity, and the scrape-to-referral ratio inside it, only appear after you connect a supported CDN, and the CDN provider may charge for log access. Check the provider list in Clarity's Settings, then AI Visibility, before you decide.

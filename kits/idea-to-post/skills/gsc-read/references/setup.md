# Setting up Search Console access

You do this once. It takes about 20 minutes. You need a Google account that is an owner of your Search Console property.

## What you are building

A service account is a robot login that belongs to a Google Cloud project instead of a person. You give the robot permission to read your Search Console, and you give this tool the robot's key file. Because the robot can only read, the worst a leaked key can do is expose your search numbers.

## Steps

1. Open console.cloud.google.com and sign in. Choose an existing project or make a new one. Google may ask for billing details when you make a new project. Check Google's current terms for the Search Console API to see whether any charge applies.
2. Open APIs and Services, then Library. Search for "Google Search Console API" and click Enable.
3. Open IAM and Admin, then Service Accounts. Click Create service account. Name it something like `search-console-reader`. Skip the optional role steps; it needs no Cloud role.
4. Open the new service account, choose Keys, then Add key, then Create new key, and pick JSON. A file downloads. This is the key.
5. Move the file somewhere outside your project folders, for example a folder named `keys` in your home folder. Do not put it in a folder that is shared, synced to a public place, or tracked by git.
6. Copy the service account's email address (it ends in `iam.gserviceaccount.com`).
7. Open search.google.com/search-console, pick your property, and go to Settings, then Users and permissions. Click Add user, paste the robot's email, and choose Restricted (view-only) permission. If the first run says permission denied, change that user to Full. The tool itself still asks Google for read-only access.
8. Tell your computer where the key is and which properties are allowed. On a Mac or Linux, add these two lines to the file your terminal reads at start (usually `~/.zshrc`), with your real path and property:

   ```bash
   export GSC_SA_KEY="$HOME/keys/search-console-reader.json"
   export GSC_APPROVED_SITES="sc-domain:example.org"
   ```

   Close and reopen the terminal. A domain property is written `sc-domain:example.org`. A URL-prefix property is written as its full address, such as `https://www.example.org/`.
9. Install the Python add-ons: `pip install google-api-python-client google-auth`.
10. Test with `python3 gsc_read.py --site sc-domain:example.org --out /tmp/gsc-test.json`. You will know it worked when the command prints nothing and the file exists. If it prints `site_not_approved`, the property is missing from `GSC_APPROVED_SITES`. If it prints `auth: failed`, the robot's email is not yet a user on that property, or the API is not enabled.

## Keeping the key safe

- Never paste the key file's contents into a chat window, an email or a screenshot.
- If a key leaks, go back to the service account's Keys tab, delete that key, and make a new one.
- Rotate the key once a year.

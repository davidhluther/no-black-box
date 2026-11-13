# CV-FU-02: Pull a County Table With the Census API

Full version, guide 2. You will get a Census key, store it so it is never written in a file, and run the kit's [script](../glossary.md#script) to build a county table with every [margin of error](../glossary.md#margin-of-error) attached. Plan 30 minutes. You need guide [CV-FU-01](CV-FU-01-set-up-claude-code-and-the-skills.md) done, or at least [Python](../glossary.md#python) 3.9 and the kit folder. The script is read-only. It asks the Census Bureau's [API](../glossary.md#api) for public numbers and writes two [CSV](../glossary.md#csv) files on your computer.

1. **CV-FU-02-1.** Request a key. Open api.census.gov/data/key_signup.html and fill in the form (it asks for an organization name and an email address, and for you to agree to the terms). The Census Bureau emails you the key, which is a long string of letters and numbers. This is your [API key](../glossary.md#api-key).
   You'll know it worked when an email arrives with the key. Do not paste the key into a chat, a document, or a screenshot. The shared [keys and accounts guide](../../../guides/keys-and-accounts.md) explains how to keep it safe.

2. **CV-FU-02-2.** Put the key in an [environment variable](../glossary.md#environment-variable) (a named setting that lives in your [terminal](../glossary.md#terminal) window only for this session). In the terminal on a Mac or Linux, type `read -s CENSUS_API_KEY` and press Return, paste your key (nothing will show on screen), press Return, then type `export CENSUS_API_KEY` and press Return. On Windows PowerShell, type `$env:CENSUS_API_KEY = Read-Host "Paste your key"` and press Return, then paste the key (it will show on screen, so do not screenshot).
   You'll know it worked when the next step prints "key is set."

3. **CV-FU-02-3.** Check it without showing it. On Mac or Linux, type `echo "${CENSUS_API_KEY:+key is set}"`. On Windows, type `if ($env:CENSUS_API_KEY) { "key is set" }`.
   You'll know it worked when it prints "key is set." If it prints nothing, repeat step 2 in the same terminal window.

4. **CV-FU-02-4.** Move to the script's folder. Type `cd ` (with a space), drag the kit's `skills/census-county-table/scripts` folder from your file browser into the terminal window, and press Return. Then do a dry run, which shows what the script would ask for and sends nothing. Type (replace the example state and counties with yours):
   `python3 -I acs_table.py --state "Example State" --counties "Alpha,Beta,Gamma" --include-state --dry-run`
   You'll know it worked when it lists the counties, says how many variables it needs, prints web addresses with "<your-key>" in place of your key, and says whether a key is present.

5. **CV-FU-02-5.** Run it for real, with the same counties, the year you want, and an output name:
   `python3 -I acs_table.py --state "Example State" --counties "Alpha,Beta,Gamma" --include-state --year 2024 --out county-table`
   You'll know it worked when it prints "Wrote county-table-long.csv and county-table-table.csv" and the number of rows. If it says the Census API "did not return data," it's E16. If it names a variable it cannot find, it's E17.

6. **CV-FU-02-6.** Open `county-table-table.csv` in Google Sheets (File, Import). You get one row per measure, one column per county, with "plus or minus" margins and a note "(large margin of error)" where a margin is more than 30 percent of the estimate. Open `county-table-long.csv` for the full detail, including whether each place is clearly different from the reference place.
   You'll know it worked when the table shows numbers like "$52,000 +/- $3,000." The cutoff for the note is the kit's rule of thumb, not a Census Bureau standard, and you can change it with `--moe-threshold 0.25`.

7. **CV-FU-02-7.** Check two numbers by hand against Census Reporter or data.census.gov. Add the source line: "U.S. Census Bureau, [American Community Survey](../glossary.md#american-community-survey), 2020-2024 5-year estimates, retrieved [mm/dd/yyyy]."
   You'll know it worked when both numbers match.

8. **CV-FU-02-8.** Close the terminal window when you are done. Because the key lived only in that window, nothing is saved on your computer.
   You'll know it worked when a new terminal window prints nothing for the "key is set" check.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CV-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

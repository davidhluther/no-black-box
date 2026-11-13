# CV-FR-04: Get County Numbers

Free version, guide 4. You will collect numbers from the [American Community Survey](../glossary.md#american-community-survey) (the Census Bureau's yearly sample survey of income, rent, age, and housing) for the counties you choose, keep each number's [margin of error](../glossary.md#margin-of-error) beside it, and write them up honestly. Plan about 45 minutes. You need your tracker from [CV-FR-01](CV-FR-01-make-your-tracker.md). No account or key is needed.

1. **CV-FR-04-1.** Choose your places and measures. Pick the counties you care about, and add your state as a yardstick. Pick at most a dozen measures, such as median household income, poverty rate, median rent, and the share of renters who pay 30 percent or more of income on rent. Use the five-year numbers, which are steadier for small counties (see [five-year estimate](../glossary.md#five-year-estimate)). A list of ready measures with their Census table numbers is in `skills/census-county-table/references/measures.md`.
   You'll know it worked when you have a short list of places and measures and have written down the period you will use, such as 2020 to 2024.

2. **CV-FR-04-2.** Try Census Reporter first. Go to censusreporter.org, type a county's name in the search box, and open its profile page. Look for the option to compare with another place (the exact label can change). Add your other counties and the state.
   You'll know it worked when you see a page of numbers for your counties side by side, each with a small plus-or-minus figure. If the site cannot find your county, it's E25.

3. **CV-FR-04-3.** If Census Reporter lacks a measure, use data.census.gov, the Census Bureau's own site. Type a table number from the measures list (for example B19013) in the search box, open the table, pick the geographies (your counties) and the 5-year survey, and download the table as a [CSV](../glossary.md#csv). Each estimate sits beside its margin of error.
   You'll know it worked when you have a file with an estimate column and a margin-of-error column per place. The menu labels on the site change from time to time. If you get stuck, it's E25.

4. **CV-FR-04-4.** Copy the numbers into your tracker's County numbers tab, one row per place and measure: place, measure, estimate, margin of error, unit, period, source link, and the date you retrieved it.
   You'll know it worked when every row has an estimate, a margin, a period, and a source link. If a cell has a dash, "(X)," or asterisks, or Census Reporter shows no number, write "no usable number" and see E23.

5. **CV-FR-04-5.** Flag shaky numbers. In the "Large margin of error" column of the first data row (cell F2), type this formula, then copy it down the column:
   `=IF(AND(ISNUMBER(C2),ISNUMBER(D2),D2>0.3*ABS(C2)),"yes","no")`
   It says "yes" when the margin is bigger than 30 percent of the estimate. That cutoff is this kit's rule of thumb, not a Census Bureau standard.
   You'll know it worked when each row shows yes or no. If many rows say "yes," it's E24, and the fix is to use a bigger area or fewer categories.

6. **CV-FR-04-6.** Check comparisons. For each measure, put the place you compare against (usually the state) in the first row of a block. In the "Differs from reference" column of the next row, type this formula and copy it down the block:
   `=IF(ABS(C3-C$2)>SQRT(D3^2+D$2^2),"yes","no")`
   Two numbers are clearly different only when the gap is bigger than the combined margins of error. Where it says "no," write "not clearly different" in your notes.
   You'll know it worked when each compared row says yes or no.

7. **CV-FR-04-7.** Ask an [AI model](../glossary.md#ai-model) for plain sentences. Copy the "Rules block" and [prompt](../glossary.md#prompt) 6 from `free/prompts.md`, paste in your table, and send. Read the answer against your table.
   You'll know it worked when each sentence reads like "an estimated 14.2 percent, plus or minus 2.1 points," and no sentence says "X percent of residents" or ranks places that are not clearly different. If the model adds numbers that are not in your table, it's E08.

8. **CV-FR-04-8.** Check two numbers by hand against the source. Add the source line to the sheet: "U.S. Census Bureau, American Community Survey, [period] 5-year estimates, retrieved [mm/dd/yyyy]."
   You'll know it worked when your two spot-checks match and the source line is on the sheet.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CV-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

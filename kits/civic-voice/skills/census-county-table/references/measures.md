# Default measures

Each measure comes from one or more tables of the American Community Survey (the Census Bureau's yearly sample survey of income, rent, age, and housing) 5-year estimates. A variable is the table number, the character _, and a row number. Add E for the estimate or M for the margin of error (the plus-or-minus amount that goes with an estimate) when using the Census API (for example B19013_001E and B19013_001M).

| Measure | Census table and rows | How it is built |
|---|---|---|
| Total population | B01003, row 001 | One cell |
| Median household income | B19013, row 001 | One cell, in inflation-adjusted dollars |
| Poverty rate | B17001, rows 002 over 001 | Share of people whose poverty status is known |
| Median gross rent | B25064, row 001 | One cell, dollars per month |
| Renter-occupied share | B25003, rows 003 over 001 | Share of occupied homes |
| Renters paying 30% or more of income on rent | B25070, rows 007 to 010 over (001 minus 011) | Excludes renters whose ratio is not computed |
| Median home value | B25077, row 001 | One cell, dollars |
| Vacancy rate | B25002, rows 003 over 001 | Share of all housing units |
| No-vehicle households | B25044, rows 003 and 010 over 001 | Owner and renter homes with no vehicle |
| Households receiving SNAP | B22010, rows 002 over 001 | Past 12 months |
| Age 65 and over | B01001, rows 020 to 025 and 044 to 049 over 001 | Men and women combined |

To add or change measures, copy the shape of an entry in `DEFAULT_MEASURES` in `scripts/acs_table.py` into a JSON file and pass it with `--measures-file`. Look up variable names on the Census Bureau's variable list for your year (api.census.gov/data/2024/acs/acs5/variables.html, checked 11/13/2026 to exist).

## When a table shows odd symbols

On data.census.gov, a dash, "(X)," or asterisks in place of a number or margin mean the estimate could not be given (too few sample cases, or a margin that does not apply). Treat them as "no usable number" and say so. The Census API uses large negative codes (such as -666666666) for the same reason. The script (a small program in a text file that does one job) turns those into "n/a."

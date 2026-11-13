# Margin of error in plain words

The American Community Survey (the Census Bureau's yearly sample survey of income, rent, age, and housing) asks a sample of households, not everyone. Each result is an estimate. The margin of error (the plus-or-minus amount that goes with an estimate) says how far the true figure could plausibly be from the estimate. The Census Bureau publishes margins at the 90 percent confidence level, which means that in about nine of ten repeats of the survey, the true figure would fall inside the estimate plus or minus the margin.

## Reading one number

Median household income of $52,000 plus or minus $3,000 means the true figure is probably between $49,000 and $55,000. A smaller margin means a firmer number.

## Comparing two numbers

Two estimates are clearly different only if the gap between them is larger than the square root of the sum of their squared margins of error. In words, combine the two margins, and ask whether the gap beats the combined margin.

Example. County A is 20% plus or minus three points. County B is 17% plus or minus two points. The gap is three points. The combined margin is the square root of (9 + 4), about 3.6 points. The gap is smaller, so the data does not show a clear difference. Write "not clearly different."

The script (a small program in a text file that does one job)'s `differs_from_reference` column does this check for you against the state row, or against whichever place you name with `--reference`.

## Shares and their margins

When a number is a share (for example renters paying 30% or more), the margin is computed from the margins of the pieces. The script uses the formula in the Census Bureau's ACS handbook for combining margins, and it falls back to the ratio formula when the first formula gives a negative number under the square root.

## When the margin is big

If the margin is more than 30% of the estimate, the script marks the number "large margin of error." This cutoff is the kit's rule of thumb, adjustable with `--moe-threshold`. A flagged number can still be reported if you show the margin and say it is uncertain. For small groups, consider a bigger area, combining categories, or leaving the measure out.

## Things the survey cannot do

It cannot give exact counts, and it cannot say why a number is what it is. Year-to-year changes in five-year estimates overlap in time, so compare periods that do not overlap (for example 2015 to 2019 against 2020 to 2024) rather than adjacent years.

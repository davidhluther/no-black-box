# Scoring rules

## Points

- Pass is two points. Partial is one. Fail is zero.
- Unknown is left out of both the points earned and the points possible. Never count an unknown as a fail.

## Section score

Section percent = points earned divided by (two times the number of checks you could answer).

Coverage = checks answered divided by checks in the section.

- Coverage under 60%: write "not enough checked to grade" and show the coverage instead of a percent.
- 80% or higher: strong. 50% to 79%: mixed. Under 50%: weak.

There is no single grand score by default. If the owner asks for one, average the graded sections, show the coverage next to it, and say the headlines matter more than the number.

## Buckets for ratings and review counts

| Rating | Bucket |
|---|---|
| 4.8 and up | top |
| 4.5 to 4.79 | strong |
| 4.0 to 4.49 | average |
| 3.0 to 3.99 | mixed |
| below 3.0 | poor |

| Review count | Bucket |
|---|---|
| 1,000 and up | very high |
| 500 to 999 | high |
| 100 to 499 | moderate |
| 25 to 99 | thin |
| under 25 | very thin |

Counts only mean something against the local competitors. A florist with 60 reviews in a town where the next-best has 70 is in a different position from one where the next-best has 700. Always report the competitor median next to the count.

## Speed bands

- Performance score: 90 and up is good, 50 to 89 needs improvement, below 50 is poor.
- Field data beats lab data. When the two disagree, report both and lead with the field numbers.
- A score taken while the testing computer was busy is noisy. Rerun once before calling something a finding.

## Headline rules

Apply each rule. Keep at most five headlines, lowest severity number first. Each headline is one sentence with its evidence.

| Severity | Rule | Example sentence |
|---|---|---|
| 1 | Review count is below 20% of the competitor median | "Forty-one Google reviews, against competitors at 310, 220, and 180." |
| 1 | A form or booking path on the site doesn't deliver (a test message never arrived) | "The contact form accepted a test message and it never arrived." |
| 2 | Mobile score is more than 15 points below the competitor median, or field data fails any of the three vitals | "Mobile speed score 38, against a competitor median of 71." |
| 2 | The home page has no structured data and at least one competitor does | "No structured data on the home page. A competitor uses LocalBusiness." |
| 2 | Name, address, or phone differ in two or more places | "The phone number is written three different ways." |
| 3 | The Google description is missing and a competitor has one | "No business description on the Google listing." |
| 3 | The primary category is a catch-all and a competitor's is more specific | "Primary category is 'Spa'. The closest competitor uses 'Day spa'." |
| 4 | More than half the checks are unknown | "Eleven of 20 checks need the owner's logins to complete." |

## Confidence on each headline

Every headline carries Confirmed, Likely, or Unverified. Hypotheses go in the investigate list, not in the headlines.

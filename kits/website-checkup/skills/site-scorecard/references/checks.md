# Scorecard checks

Each check gets one result. Pass is two points, partial is one, fail is zero, and unknown is left out of the math. The IDs match the Scorecard tab in the free Google Sheet template.

## Google Business Profile (G)

| ID | Check | Pass looks like |
|---|---|---|
| G1 | Profile found and claimed | A listing shows as verified (no "Claim this business" link) |
| G2 | Name is exact | The listing name matches the sign and the website, with no city or service words added |
| G3 | Primary category is specific | The primary category names the core service, not a catch-all such as "Spa" or "Clinic" |
| G4 | Extra categories cover the other services | Adjacent services have their own category, and nothing is listed that the business doesn't sell |
| G5 | Address or service area is right | Storefronts show the address. Businesses without a public door show service areas (counties beat towns) |
| G6 | Hours are honest | Hours match reality, or hours are blank and an appointment attribute is set |
| G7 | Website link is clean | It points to the one canonical address, with no tracking tags attached |
| G8 | Description is present and follows the rules | It says what the business does, who it serves, and where, with no links, prices, or promotions |
| G9 | Services or products are listed | The services section is filled in, with short descriptions |
| G10 | Photos are real and recent | The business, the people, and the work. No stock images |
| G11 | Recent activity | A post, answered question, or new photo within 90 days. Unknown if not visible |

## Reviews (R)

| ID | Check | Pass looks like |
|---|---|---|
| R1 | Rating | 4.5 or higher is pass, 4.0 to 4.4 is partial, below 4.0 is fail |
| R2 | Volume against competitors | At least half the competitor median is pass, 20% to 49% is partial, below 20% is fail |
| R3 | Recent reviews | At least one review in the last 90 days |
| R4 | Owner replies | Most of the newest ten reviews have an owner reply |
| R5 | Second platform | A presence on the platform that matters for the business type |
| R6 | Easy way to ask | A short review link exists and is used (ask the owner if not visible, mark unverified) |

## Speed (S)

| ID | Check | Pass looks like |
|---|---|---|
| S1 | Mobile performance score, home page | 90 or higher is pass, 50 to 89 is partial, below 50 is fail |
| S2 | Field loading (LCP) | 2.5 seconds or less is pass, up to 4 seconds is partial, above is fail |
| S3 | Field responsiveness (INP) | 200 milliseconds or less is pass, up to 500 is partial, above is fail |
| S4 | Field layout shift (CLS) | 0.1 or less is pass, up to 0.25 is partial, above is fail |
| S5 | Mobile score, a second key page | Same bands as S1 |

If a page has no field data, S2 to S4 are unknown.

## Structured data (D)

| ID | Check | Pass looks like |
|---|---|---|
| D1 | Markup present on the home page | At least one JSON-LD block |
| D2 | Type fits the business | A specific LocalBusiness type, or Organization for a business with no storefront |
| D3 | Valid and complete | The validator shows no errors, and name and address are present |
| D4 | Details match the listing | Name, address, and phone are identical to the Google listing |
| D5 | Honest markup | No copied third-party review stars, no markup for content a visitor can't see |

## Local search (L)

| ID | Check | Pass looks like |
|---|---|---|
| L1 | Name, address, and phone match everywhere | Identical on the site, Google, Apple, Bing, and one or two directories |
| L2 | Apple and Bing listings claimed | Both exist and are claimed |
| L3 | A directory for the business type | Present, with matching details |
| L4 | City or area named on key pages | In title, main heading, and body |
| L5 | A page per major service | Separate pages, with their own copy |
| L6 | Map, directions, or service-area statement | Present on the site |
| L7 | Spot searches | The business appears for its own name, and ideally for one service search |

## Positioning (P)

| ID | Check | Pass looks like |
|---|---|---|
| P1 | Says who it serves | A named customer or job to be done, narrow enough to act on |
| P2 | Says what only this business can claim | A line a competitor couldn't copy word for word |
| P3 | Same promise in every place | Google description, home page, and newest social bio agree |

## Search visibility (V)

| ID | Check | Pass looks like |
|---|---|---|
| V1 | Search Console set up and readable | The owner can see data for the site |
| V2 | Bing Webmaster Tools set up | Same |
| V3 | Home page is in Google | The home page appears in a `site:` search or the URL Inspection tool says it is indexed |
| V4 | Name search finds the site first | The site, not a directory, ranks first for the business name |

## The marketing baseline

The 16 baseline items are tracked in their own tab and described in `baseline-16.md`. They feed the headlines but not the section scores.

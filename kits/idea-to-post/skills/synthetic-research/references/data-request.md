# Data Request Template

Hand this to a client or an internal stakeholder at intake. Written for someone who hasn't read the paper and doesn't care about the method, only about what to go find.

**How to adapt it:** replace `[CLIENT]` and `[CATEGORY]`. Use the consumer or the B2B persona section, not both. Cut any group the client doesn't have (most don't have all six). Keep the "if you can only find one thing" section and the "what good looks like" section no matter how much you cut, because those two do most of the work.

The tone is deliberate. It asks for raw material, admits what we don't know, and names the risk. Requests that oversell get sent the polished deck instead of the messy CSV, which is the opposite of what we need.

---

# Data Request: Synthetic Respondent Pilot

## Why I'm asking

We're evaluating a published method for simulating survey respondents with AI. PyMC Labs and Colgate-Palmolive validated it across 57 real concept tests covering 9,300 human respondents, and it reproduced roughly 90% of human test-retest reliability on concept rankings while producing realistic response distributions. If it holds up in [CATEGORY], we could pre-screen messaging and product concepts synthetically before spending on real panels, then send only the top candidates to human validation.

The method only earns trust if we check it against real human responses first. Most of what's below is calibration and validation material, not a request for new research.

## If you can only find one thing, find this

Respondent-level data from any quantitative study [CLIENT] has already run. A concept test, a message test, or a purchase-intent survey all work. Not the topline deck: the individual rows, meaning each respondent's rating, the scale wording, what they were shown, their attributes, and their open-end comments. One study is enough to start.

## From market research and consumer insights

The highest-value group. Everything here maps onto how the original method was validated.

- Respondent-level exports from past concept tests, message tests, or purchase-intent surveys. One row per respondent per concept, ideally as CSV.
- Exact question wording and scale point labels. The method calibrates against real scale language, so a paraphrase won't do.
- Open-end verbatims tied to those same respondents. This is the closest analog to what the AI generates and the thing we calibrate against.
- The stimulus material respondents actually saw. Concept boards, images, copy blocks, or whatever was in front of them. Visuals reportedly work better than text alone.
- Screener and quota definitions, which tell us the real population composition so synthetic panels can be weighted to match.
- Any study fielded more than once against the same population, or any explicit test-retest work. Without it we have no reliability ceiling and can't state how close to human we landed.
- Tracker waves, if any items repeat across waves.
- Panel vendor names and contract terms, so we know whether respondent-level data can be reused this way at all.

## Persona attributes: consumer version

*(Use this section for B2C. Delete the B2B version below.)*

Respondent personas carry the method. In the source study, stripping demographics cut accuracy nearly in half.

- Which respondent attributes are captured in the data: age, gender, income, region, ethnicity, household composition, and category usage.
- The real distribution of those attributes across the customer base or target market, so synthetic panels aren't uniformly weighted.
- Any segmentation [CLIENT] already uses. Named segments, personas, or usage-occasion frameworks.

## Persona attributes: B2B version

*(Use this section for B2B. Delete the consumer version above. Note the domain risk below.)*

Respondent personas carry the method. In the source study, stripping demographics cut accuracy nearly in half. The B2B analog of demographics is firmographics plus buyer role.

- Which account firmographic fields are actually populated, specifically company size, industry vertical, revenue, employee count, and geography.
- Whatever category-specific volume measure exists, banded is fine.
- Incumbent provider or current solution on the account, wherever it's captured.
- Buyer role and title on opportunity contacts. The economic buyer, the user, and the procurement gatekeeper are different respondents.
- Closed-won and closed-lost records for the last 12 to 24 months, with loss reasons attached.
- However the market gets cut internally. ICP documentation, segment definitions, and any named personas already in use.

## From marketing operations

- Any A/B or multivariate tests on copy, including the losing variants and their results.
- Landing page variants with conversion rates.
- Ad copy with click-through and conversion by variant.
- Email subject lines with open and click rates.
- Any prior message or copy testing, formal or informal.

## From support and customer success

- Ticket exports with whatever category labels exist.
- Churn and cancellation reasons.
- NPS or CSAT scores with the verbatim comments still attached to them.

## From product

- Concept briefs for anything worth putting through a test.
- Feature descriptions and pricing structures written the way a customer would hear them.

## System access

- Call recording (Gong, Chorus, or equivalent). Transcripts are the best record of real buyer objections in buyers' own words.
- CRM. Firmographics and win/loss both live there.
- Support platform, email platform, and any warehouse that already joins this material together.

## Legal and privacy

- Whether respondent-level survey data can be used for model calibration under existing panel vendor agreements.
- PII handling rules for anything carrying customer names or contact details.
- Whether call transcripts can be used this way, and under what constraints.

## What good looks like

Raw and granular beats clean and summarized. A messy CSV of 300 respondent rows is worth more than a polished 40-slide readout of the same study, because the method needs the distribution of individual answers rather than the average. If you're choosing between the two, send the messy one.

## The open question

The published validation ran on personal care products, a category where AI models have absorbed enormous volumes of consumer discussion. Whether the method holds in a category with a thinner footprint is the thing this pilot exists to find out, which is why the validation data matters more for us than it did for the original authors.

*(For B2B engagements, extend the paragraph above: B2B purchases also involve committees, procurement, and incumbent contracts rather than one person deciding, and the method models none of that.)*

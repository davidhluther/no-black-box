# The method in brief

Source: Maier, Aslak, Fiaschi, Rismal, Fletcher, Luhmann, Dow, Pappas, and Wiecki, "LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings," PyMC Labs and Colgate-Palmolive, arXiv 2510.08338 (2025). Read the paper for numbers and limits before quoting any of them. Figures are not repeated here so they cannot drift.

## The problem it addresses

Ask an AI model to rate purchase intent from one to five and you get answers that are too narrow and bunched on one or two points. The order of ideas may be roughly right while the spread is wrong enough that the output cannot stand in for survey data.

## The method

1. **Elicit text.** The model plays a respondent with stated attributes (age, income, situation) and writes a free-text reaction to the concept.
2. **Embed the text.** Convert it to numbers that capture meaning (an embedding model does this).
3. **Compare to anchors.** Write a small set of anchor statements, one per scale point. Measure how close the reaction is to each (cosine similarity).
4. **Normalize.** Turn the similarities into a spread across the scale points. Average across several independently written anchor sets.

The output is a spread, not a single number, so ambiguity in the text survives into the rating.

## What the authors say matters

- Describing the respondents matters a great deal. Without attributes the match dropped sharply.
- Anchor wording was written and tuned by hand, and results depend on it.
- Pictures helped a little compared with text-only descriptions.

## Limits they name

- Anchors were hand-tuned; other domains are untested.
- Some respondent attributes were reproduced better than others.
- It assumes the AI model has read plenty about the category.
- It lacks real-world constraints (budget, competition, marketing exposure).
- It does not stop invented detail in unfamiliar areas.

## How this kit uses it

As a pre-screen and a brainstorming aid. Never as a substitute for asking real people, and never with claims of accuracy unless you replicated a real study of your own first.

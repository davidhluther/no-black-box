# Method Notes: Semantic Similarity Rating

These notes summarize one published study so you can judge claims about simulated respondents. Read them before quoting any figure.

## Source

Maier, Aslak, Fiaschi, Rismal, Fletcher, Luhmann, Dow, Pappas, and Wiecki. "LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings." arXiv 2510.08338, 2025. Authors from PyMC Labs and a consumer-products company. The authors released a Python implementation.

## The problem it addresses

Asking an AI model to rate purchase intent from 1 to 5 gives distributions that are too narrow and clustered. The ranking may be roughly right, but the answers cannot stand in for real survey data.

## What the study did

The authors compared 57 real consumer surveys on personal-care product concepts (about 9,300 human respondents, 150 to 400 per survey, five-point purchase intent scale) with simulated replications using two AI models. They tested three ways of getting a rating:

1. Direct rating: ask the model for the number.
2. Follow-up rating: the model writes a reaction, then a second pass turns it into a number.
3. Semantic similarity rating: the model writes a reaction, the reaction is turned into an embedding (a list of numbers capturing meaning), and the embedding is compared with hand-written anchor statements for each scale point, giving a probability for each point. This is averaged over six sets of five anchors.

## Reported results

| Method | Agreement with human concept ranking (as a share of human self-agreement) | Similarity of answer distribution to humans (1 is identical) |
|---|---|---|
| Direct rating | about 80% | 0.26 |
| Follow-up rating | about 85% | 0.72 |
| Semantic similarity rating | about 90% | 0.88 |

- Agreement was measured as rank correlation against human rankings, divided by how well humans agree with themselves when retested.
- Without demographic details in the personas, agreement dropped to about 50%.
- Visual stimuli did modestly better than text-only.
- Simulated respondents wrote longer, more reasoned comments than real panelists, who tended to write short affirmations.

## Limits the authors name

- Anchor wording was hand-tuned. Other topics are untested.
- Age and income replicated well. Gender and region did not.
- The method assumes the model has read a lot about the category. Personal care qualifies. Other categories may not.
- Results depend on the embedding model and similarity measure used.
- No real-world context such as budget, competing choices, or advertising.
- Hallucination in unfamiliar topics is not solved.

## What to take from it

1. Never ask for a number directly. Ask for text first.
2. Report two measures, ranking and distribution shape.
3. It needs real data to check against. The 57 real studies are why the result is believable.
4. It is a pre-screen. The authors frame it as narrowing many candidates to a few for real testing.
5. Business-to-business and small local organizations are untested.

## What to ask a real-data collaborator for

If you want to try the rigorous method, ask for any past survey with one row per respondent, including the exact question wording and scale labels, each respondent's written comments, the material they were shown, and who they were (age, region, role). A summary slide cannot serve as a check, because the method is judged on the spread of answers, and an average removes the spread. Keep personal details out of any file you share. Confirm you are allowed to reuse the data before using it.

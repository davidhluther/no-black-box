# GA4 recipe: an "AI models" traffic channel

GA4 (Google Analytics 4, Google's free tool that counts visits to your website) sorts visits into channels such as Organic Search, Direct, and Referral. A visit from ChatGPT or Perplexity usually lands in Referral, mixed with every other website that links to you. This recipe adds a custom channel group (your own rule for sorting visits) so those visits show up on their own line.

## What it can and cannot see

It sees visits where the AI product passed along a source name that matches the list below. It cannot see visits where the source was stripped (these show up as Direct), visits from a mobile app that sends nothing, or conversations that mention you but never produce a click. Read every count as "at least this many".

GA4 may also have a built-in AI channel by the time you read this. Two low-authority web sources said so, and I could not confirm it in Google's own documentation (checked 11/13/2026). Open Reports, Acquisition, Traffic acquisition, and look at the channel names before deciding you need this recipe.

## Steps

1. In GA4, click the gear icon (Admin) at the bottom left.
2. Under Data display (some accounts show it as Data settings), click Channel groups.
3. Click Create new channel group. Name it "Default plus [AI models](../glossary.md#ai-model)". GA4 copies the default rules as your starting point.
4. Click Add new channel. Name it "AI models".
5. Add a condition. Choose the dimension Source, the operator "matches [regex](../glossary.md#regex)" (a pattern, written in a small text language, that matches many names at once), and paste the pattern below.
6. Click Apply, then drag the "AI models" channel above Referral in the list. GA4 gives each visit to the first channel that fits, from the top down, so it must sit above Referral or Referral will claim these visits first.
7. Click Save group.
8. Open Reports, Acquisition, Traffic acquisition. Above the table, change the dropdown "Session primary channel group (Default)" to your new group. Choose a date range that includes some past months.

## The pattern

```
.*(chatgpt\.com|chat\.openai\.com|openai\.com|perplexity|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|copilot\.com|deepseek|grok\.com|meta\.ai|poe\.com|phind\.com|mistral\.ai).*
```

Source names change. Every few months, open Traffic acquisition, switch the table to Session source, filter to the Referral channel, and look for AI product names the pattern misses. Add them to the pattern and save the group again.

## Check that it worked

- You should see a line named AI models in the table. If your site gets few AI visits, the line may show a small number or be missing for some dates. A small number is a result.
- Custom channel groups usually apply to past data in the reports that support them. Look at a past month to see whether it did for your account.
- If AI models shows nothing, filter the table to Session source and search for "chatgpt" or "perplexity" to see whether any visits arrived under those names at all.

## Compare it with something else

Do not add this count to the [Search Console](../glossary.md#search-console) classifier count (`ai-traffic-classifier` in the full version). They measure different slices of AI-driven traffic. Put them side by side.

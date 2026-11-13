---
name: hero-image
description: Make the header (hero or thumbnail) image for a blog post. Reads the finished article, writes three image concepts, creates banner images in Canva first, falls back to the OpenAI or Gemini image API if your own key is set, and always writes a designer brief so a person can make the image if no tool does. Use when asked for a hero image, header image, thumbnail or featured image for an article.
---

# Hero image

Works in: Claude Code (full version). The Canva step needs the Canva connector turned on in your AI tool, and the API step runs a small script on your computer. In Claude.ai or ChatGPT, use Step 2's prompts and Step 4's brief by hand.

A hero image is the banner at the top of a post and the picture shown when someone shares the link. This skill makes up to five options and one brief, then asks you to choose.

## Settings

Read `config.json` (your copy of `config.example.json`) for:

- `brand_colors`: the palette as hex codes (for example `#1F5FAD`). If it is blank, ask the person. Never invent a palette.
- `blog_url_pattern`: for example `https://example.org/blog/{slug}`. Used in the brief's publish line.
- `organization_name`: used in the brief only, never printed on the image.

## Step 1: read the article

Open the final article (`output/final/`, or `output/drafts/` if there is no final yet). Note:

- the core topic and what readers do with it
- the audience (for example owners, treasurers, volunteers, program staff)
- the tone: educational, urgent, hopeful or practical
- two or three visual ideas that carry the theme
- whether the topic is abstract (a process or a policy) or concrete (a thing you can photograph)

## Step 2: choose the route for the images

Work down this list and use the first route that is available. Say which route you used.

1. **Canva (first choice).** If the Canva connector is available, ask it to generate three banner designs, 1200 by 630 pixels, no text on the image (your site shows the title separately, and baked-in text clashes), clean and professional. Use these three prompts and fill the brackets:
   - Editorial: "Create a professional banner image, 1200x630 pixels, showing [a concrete scene for the topic]. Clean aesthetic, no text overlay, no logos."
   - Illustrated: "Create an illustrated banner image, 1200x630 pixels, flat design with clean geometric shapes representing [the main idea]. Color palette: [brand_colors]. No text, no logos."
   - Conceptual: "Create a conceptual banner image, 1200x630 pixels, using a visual metaphor for [the core idea]: [describe it]. Professional quality, no text, no logos, clean composition."
2. **An image API with your own key.** Check which key is set without printing it:

   ```bash
   python3 -c "import os; print({k: bool(os.environ.get(k)) for k in ('OPENAI_API_KEY','GEMINI_API_KEY')})"
   ```

   If one is `True`, make one more option with the helper script. Add `--crop 1200x630` to trim the result to banner size (needs `pip install pillow`).

   ```bash
   python3 scripts/generate_image.py --provider openai --prompt "[scene description]" \
       --out output/images/my-topic-option-4.png --crop 1200x630
   ```

   Use `--provider gemini` for a Gemini key. Each call can cost money on your provider account, so check the provider's current price page first. Image model names change often; if the call says the model was not found, look up the current name and set `OPENAI_IMAGE_MODEL` or `GEMINI_IMAGE_MODEL`. Add `--dry-run` to see the request without sending it. If a call fails for any reason (no key, rate limit, billing), skip it and go on.
3. **Designer brief only.** If neither route works, the brief in Step 3 is the deliverable. A person can make the image from it, or you can paste the prompts into any image tool.

Keys come from environment variables only. Never paste a key into a chat, a file in your project, or a screenshot. The shared "Keys and accounts" guide shows how to set one safely.

## Step 3: write the designer brief (always)

Save it as `output/images/my-topic-image-brief.md`, even when images were generated.

```markdown
# Hero Image Brief: [Article Title]

## Article context
- Topic: [core topic]
- Audience: [readers]
- Tone: [educational / urgent / hopeful / practical]
- Publish URL: [blog_url_pattern with the slug filled in]

## Image requirements
- Dimensions: 1200 x 630 px (blog header and social sharing)
- Format: JPG or PNG, under 500 KB
- Text on the image: none (the page shows the title)
- Alt text suggestion: [what the image shows, 125 characters or fewer]

## Visual direction
### Option 1: photograph
[Scene, subjects, setting, lighting, mood.]
Stock photo search terms: [five to eight specific terms]

### Option 2: illustration
[Style, key shapes, palette, composition.]
Style references: [two or three comparable looks]

### Option 3: visual metaphor
[The metaphor and how it connects to the article.]

## Color guidance
- Primary: [brand_colors, with hex codes]
- Avoid: neon, heavy saturation, anything that clashes with the palette

## What to avoid
- Stock-photo clichés (handshakes, people pointing at charts)
- Text baked into the image
- Complex compositions that fail at thumbnail size
- Images that could belong to any organization
```

## Step 4: present the results

Tell the person how many Canva designs were made (with links), whether an API image was made and which provider, where the brief is saved, and which option you recommend and why. Ask which they prefer, or whether to try different prompts.

## Checks before approving any image

Look at every generated image for printed words, made-up company or product names, garbled numbers, slogans, and logos that are not yours. Generated images often get these wrong. Hold any image with one of them and regenerate with a stricter prompt. Keep the untouched original and deliver the cropped copy.

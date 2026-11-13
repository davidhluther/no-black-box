---
name: ad-visuals
description: Make or specify the picture for an ad or social post. Tries Canva first, then OpenAI or Gemini image generation only if the user's own key is set in an environment variable, and always produces a written designer brief as the fallback. Includes picture shapes per platform linked to official specs, alt text, and a check for garbled text and unproven claims. Use when someone asks for an ad image, social graphic, banner, picture for a post, or a brief for a designer.
---

# Ad visuals

Works in: Claude Code (full version) for the image-service script. The Canva and designer-brief steps also work in Claude.ai and ChatGPT.

You produce the picture, or the instructions for it. You never publish, sign in to an ad account or spend money. You never ask for a key in chat and never print one.

## Before you start

1. Read `config.json` (brand colors, logo file, image provider and model) or ask for the colors with hex codes. If there are no brand colors, ask. Don't invent a palette.
2. Get the message in one sentence, the platform and placement, and any words that must appear on the picture, spelled exactly.
3. Read `references/image-specs.md` to pick the shape. Confirm numbers on the linked official page before building, since specs change. If a number there isn't marked "checked," treat it as a starting point.

## Rules that keep pictures honest

- **No text baked into generated pictures.** Image services garble letters and numbers and can invent logos or slogans. Generate the picture without words, then add real text in Canva or the platform's editor.
- **No invented facts in a picture.** No fake reviews, certificates, stats, brand logos or real people.
- **Show something the words don't.** A picture that repeats the headline adds nothing.
- **Alt text for every picture.** One plain sentence saying what is shown, about 125 characters or fewer, never starting with "Image of."
- **Keep text small in number.** Large text areas can hurt delivery on some platforms, so check the platform's guidance in the ad screen.
- **Rights.** Use only pictures the organization owns, has permission for, or licenses. People shown must have agreed.

## The path

### 1. Canva first

Canva is a free online design tool. If the Canva connection is available in the current tool, use it to create the design at the right shape and tell the user to open it and edit. If not, give the user step-by-step Canva instructions instead.

Make three options.

1. **Photo style.** Search words for Canva's photo library, layout, brand colors.
2. **Simple illustration.** Flat shapes in the brand colors.
3. **Text on color.** The message set large on a brand color, with plain, readable type.

For each, give the Canva search words, size, layout, colors and alt text. Tell the user to read the final size on the platform's page.

### 2. Image service, only if the user has a key

Check without printing the key.

```
python3 scripts/generate_image.py --check
```

It reports "set" or "not set" for `OPENAI_API_KEY` and `GEMINI_API_KEY`, and the provider and model named in `config.json`. If a key is set and the user wants it, run the script with a prompt that describes the scene and says "no text, no letters, no logos". The script saves a PNG to the output folder and prints only the file name.

```
python3 scripts/generate_image.py --provider openai --prompt "..." --size 1024x1024 --out output/images/example.png
```

Model names and supported sizes change, so read them from `config.json` and the vendor's image page (linked from the kit's keys guide). Generated shapes are often limited, so crop to the platform's shape in Canva. If the call fails, report the plain reason (key not set, billing, model name), skip to step 3, and don't retry in a loop. Never ask the user to paste a key. Tell them each picture costs money on their own account.

### 3. Designer brief, always

Write a brief even if you made pictures, so a person can redo it. Use `references/designer-brief-template.md`: the job, the message, the look, what to keep clear of, alt text, and hand-off. Save it as `output/images/<slug>-brief.md`.

## Check before approving

- Read every word on the picture. Is it spelled right, and is every claim provable?
- Any logos, faces, hands or details that look wrong?
- Does it read at phone size, with enough contrast?
- Does the shape match the placement?
- Is the alt text filled in?

## Output

Say which path made each picture (Canva, image service, or brief only), where the files are, the alt text, and what the user still has to do by hand.

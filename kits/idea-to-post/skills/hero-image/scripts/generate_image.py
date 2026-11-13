#!/usr/bin/env python3
"""Make one blog hero image with the OpenAI or Gemini image API, using YOUR key from an environment variable.

Keys are read from the environment only and are never printed:
  OPENAI_API_KEY   and optionally OPENAI_IMAGE_MODEL  (default gpt-image-1)
  GEMINI_API_KEY   and optionally GEMINI_IMAGE_MODEL  (default gemini-2.5-flash-image)
Providers rename image models often. If a call fails with "model not found", look up the current image
model name on the provider's own page and put it in the matching *_IMAGE_MODEL variable.

Usage:
  python3 generate_image.py --provider openai --prompt "..." --out output/images/my-topic-option-4.png
  python3 generate_image.py --provider gemini --prompt "..." --out output/images/my-topic-option-5.png --crop 1200x630
  python3 generate_image.py --provider openai --prompt "..." --out x.png --dry-run     (shows the request, sends nothing)

--crop WxH centers and crops the result to that size. It needs Pillow (pip install pillow); without it the
original image is saved and a note says so.
Each call can cost money on your provider account. Check your provider's current price page first.
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

NO_TEXT = (" Landscape banner composition, no text, no words, no letters, no logos, "
           "professional quality, clean composition.")


def build_request(provider, prompt, size):
    full = prompt.strip() + NO_TEXT
    if provider == "openai":
        model = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
        return ("https://api.openai.com/v1/images/generations",
                {"Content-Type": "application/json"},
                {"model": model, "prompt": full, "size": size, "n": 1}, "OPENAI_API_KEY", model)
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    return (f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            {"Content-Type": "application/json"},
            {"contents": [{"parts": [{"text": full}]}],
             "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}, "GEMINI_API_KEY", model)


def call(url, headers, body, provider, key):
    headers = dict(headers)
    if provider == "openai":
        headers["Authorization"] = "Bearer " + key
    else:
        headers["x-goog-api-key"] = key
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        sys.exit(f"The {provider} API answered {exc.code}. {detail}")
    except (urllib.error.URLError, TimeoutError) as exc:
        sys.exit(f"Could not reach the {provider} API: {exc}")


def image_bytes(provider, data):
    if provider == "openai":
        item = (data.get("data") or [{}])[0]
        if item.get("b64_json"):
            return base64.b64decode(item["b64_json"])
        if item.get("url"):
            with urllib.request.urlopen(item["url"], timeout=120) as resp:
                return resp.read()
    else:
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    return base64.b64decode(inline["data"])
    sys.exit("The response held no image. The model name may be wrong or the prompt may have been declined.")


def crop(path, size):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed, so the image was not cropped. Install it with: pip install pillow")
        return
    w, h = (int(n) for n in size.lower().split("x"))
    img = Image.open(path).convert("RGB")
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)))
    left, top = (img.width - w) // 2, (img.height - h) // 2
    img.crop((left, top, left + w, top + h)).save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--provider", choices=["openai", "gemini"], required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1536x1024", help="OpenAI size; Gemini picks its own")
    ap.add_argument("--crop", help="center-crop to WxH after saving, for example 1200x630")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    url, headers, body, env_name, model = build_request(a.provider, a.prompt, a.size)
    if a.dry_run:
        print(json.dumps({"url": url, "model": model, "key_variable": env_name,
                          "key_present": bool(os.environ.get(env_name)), "body": body}, indent=2))
        return 0
    key = os.environ.get(env_name)
    if not key:
        sys.exit(f"{env_name} is not set, so no image was made. Use Canva or the designer brief instead.")
    raw = image_bytes(a.provider, call(url, headers, body, a.provider, key))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "wb") as fh:
        fh.write(raw)
    if a.crop:
        crop(a.out, a.crop)
    print(f"Saved {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

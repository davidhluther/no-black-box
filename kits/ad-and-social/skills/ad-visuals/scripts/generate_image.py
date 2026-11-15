#!/usr/bin/env python3
"""Generate one picture with OpenAI or Gemini, using a key from the environment.

Safe by design.
- Reads keys only from the environment variables OPENAI_API_KEY and GEMINI_API_KEY.
- Never prints, logs or writes a key.
- Uses only the Python standard library.
- Makes one request per run. It does not retry in a loop.

Model names and sizes change, so they are never hard-coded here. Give them with
--model and --size, or in config.json (image_model). Check the vendor's image page.

Examples
  python3 generate_image.py --check
  python3 generate_image.py --provider openai --model MODEL --prompt "A bowl of soup, no text" --size 1024x1024 --out output/images/soup.png
  python3 generate_image.py --provider gemini --model MODEL --prompt "A bowl of soup, no text" --out output/images/soup.png
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ENV_VARS = {"openai": "OPENAI_API_KEY", "gemini": "GEMINI_API_KEY"}
NO_TEXT = " No text, no letters, no numbers, no logos."


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never follow a redirect: it would carry the API key header to whatever host the reply names."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "redirect refused", headers, fp)


OPENER = urllib.request.build_opener(_NoRedirect)
# OpenAI's own picture storage only; a bare ".blob.core.windows.net" would admit any Azure customer's account.
IMAGE_HOST = re.compile(r"^(?:oaidalleapiprodscus\.blob\.core\.windows\.net|(?:[a-z0-9-]+\.)*(?:openai\.com|oaiusercontent\.com))$")
MAX_IMAGE_BYTES = 50 * 1024 * 1024


def fetch_image_url(url):
    """Download a returned picture only from the provider's own https hosts, with a size cap, no key sent."""
    try:
        parts = urllib.parse.urlsplit(url or "")
        host = (parts.hostname or "").lower()
    except ValueError:
        return None
    if parts.scheme != "https" or not IMAGE_HOST.match(host):
        return None
    try:
        with OPENER.open(url, timeout=120) as resp:
            data = resp.read(MAX_IMAGE_BYTES + 1)
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    return data if len(data) <= MAX_IMAGE_BYTES else None


def load_config(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError):
        print("config.json could not be read. See fix E19.", file=sys.stderr)
        sys.exit(2)


def check(config):
    for name, var in ENV_VARS.items():
        print(f"{name}: {var} is {'set' if os.environ.get(var) else 'not set'}")
    print(f"config image_provider: {config.get('image_provider', '(none)') or '(none)'}")
    print(f"config image_model: {config.get('image_model', '') or '(not set)'}")


def post_json(url, body, headers):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
    try:
        with OPENER.open(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except ValueError:
        print("The image service sent a reply that could not be read. See fix E07.", file=sys.stderr)
        sys.exit(3)
    except urllib.error.HTTPError as err:
        # Print the status only. The body can echo request details, so it is not shown.
        print(f"The image service refused the request (HTTP {err.code}). See fix E07.", file=sys.stderr)
        sys.exit(3)
    except (urllib.error.URLError, TimeoutError):
        print("Could not reach the image service. Check your connection and try again.", file=sys.stderr)
        sys.exit(3)


def fetch_bytes(url):
    data = fetch_image_url(url)
    if data is None:
        print("The picture link the service returned could not be downloaded safely. See fix E07.", file=sys.stderr)
        sys.exit(3)
    return data


def openai_image(key, model, prompt, size):
    body = {"model": model, "prompt": prompt, "n": 1}
    if size:
        body["size"] = size
    result = post_json("https://api.openai.com/v1/images/generations", body,
                       {"Authorization": f"Bearer {key}"})
    item = (result.get("data") or [{}])[0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        return fetch_bytes(item["url"])
    print("The service answered but returned no picture.", file=sys.stderr)
    sys.exit(3)


def gemini_image(key, model, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model, safe='')}:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
    result = post_json(url, body, {"x-goog-api-key": key})
    for candidate in result.get("candidates", []):
        for part in (candidate.get("content") or {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    print("The service answered but returned no picture.", file=sys.stderr)
    sys.exit(3)


def main():
    parser = argparse.ArgumentParser(description="Make one picture. Keys come from environment variables only.")
    parser.add_argument("--check", action="store_true", help="Say which keys are set (never shows them) and exit")
    parser.add_argument("--provider", choices=sorted(ENV_VARS))
    parser.add_argument("--model")
    parser.add_argument("--prompt")
    parser.add_argument("--size", help="For example 1024x1024. Check the vendor's page for sizes it accepts")
    parser.add_argument("--out", help="File to save, for example output/images/example.png")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--allow-text", action="store_true", help="Do not append the no-text instruction")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.check:
        check(config)
        return

    provider = args.provider or config.get("image_provider")
    model = args.model or config.get("image_model")
    if provider not in ENV_VARS:
        print("Choose --provider openai or gemini (or set image_provider in config.json).", file=sys.stderr)
        sys.exit(2)
    if not model:
        print("Give --model or set image_model in config.json. Model names change, so none is built in.", file=sys.stderr)
        sys.exit(2)
    if not args.prompt or not args.out:
        print("Both --prompt and --out are required.", file=sys.stderr)
        sys.exit(2)

    key = os.environ.get(ENV_VARS[provider])
    if not key:
        print(f"{ENV_VARS[provider]} is not set. See fix E06.", file=sys.stderr)
        sys.exit(4)

    prompt = args.prompt if args.allow_text else args.prompt.rstrip() + NO_TEXT
    image = openai_image(key, model, prompt, args.size) if provider == "openai" else gemini_image(key, model, prompt)

    folder = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(folder, exist_ok=True)
    with open(args.out, "wb") as handle:
        handle.write(image)
    print(f"Saved {os.path.basename(args.out)}")


if __name__ == "__main__":
    main()

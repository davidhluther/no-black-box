# AS-FU-02: Add an Image Service Key (Optional)

Time about 20 minutes. Skip this guide if [Canva](../glossary.md#canva) or a designer covers your pictures. Nothing else in the kit needs a key.

An [image service](../glossary.md#image-service) is a company's computers that draw a picture from your written description. A key is a long secret code that proves to the service that requests come from your account. Anyone holding it can spend your money, so treat it like a bank card.

1. **AS-FU-02-1.** Read the shared [keys and accounts guide](../../../guides/keys-and-accounts.md) for how to sign up and where the cost and free limits are listed.
   You'll know it worked when you have chosen OpenAI, Google (Gemini), or neither.
2. **AS-FU-02-2.** Create the key on the vendor's own site and set a monthly spending limit in the same place if it offers one.
   You'll know it worked when the vendor shows a key beginning with letters and numbers once. Copy it to a safe place right away.
3. **AS-FU-02-3.** Store the key as an environment variable (a named setting your computer keeps outside your files). The names this kit looks for are `OPENAI_API_KEY` and `GEMINI_API_KEY`. The keys guide shows how for your computer.
   You'll know it worked when a new [terminal](../glossary.md#terminal) window shows the variable is set. Don't print the key itself. Run `python3 scripts/generate_image.py --check` from the kit's ad-visuals folder, and it only says "set" or "not set" (E06).
4. **AS-FU-02-4.** Set `image_provider` and `image_model` in `config.json`. Look up the current model name on the vendor's image page, linked from the keys guide. Model names change, so this kit doesn't hard-code one.
   You'll know it worked when `--check` reports the provider and model name with no error.
5. **AS-FU-02-5.** Never paste the key into chats, spreadsheets, screenshots, or `config.json`.
   You'll know it worked when a search of your folder for the first few characters of your key finds nothing.

> **How to get help.** Write down the step ID where you got stuck (it looks like AS-FU-02-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

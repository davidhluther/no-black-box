# AV-FU-02: Get and Store Your Keys

Time, about 30 minutes. The runner asks each AI company's own developer service your questions, using your account. That needs an [API key](../glossary.md#api-key) from each company you want to run. You do not need all four. One is enough to start.

Read [Keys and accounts](../../../guides/keys-and-accounts.md) first. It shows where to sign up, what the free tier covers, and how to keep a key private.

1. **AV-FU-02-1.** Pick the companies. The runner supports OpenAI (ChatGPT), Anthropic (Claude), Google (Gemini), and Perplexity. For each one, create a developer account, add a payment method if it asks, and create a key. Name the key "ai-visibility".
   You'll know it worked when you have a key for at least one company, shown once on screen. Copy it to a password manager now. Most pages never show it again.

2. **AV-FU-02-2.** Set a spending limit in each account before you use the key. Look for Billing, then Limits (or Budget), and set a monthly cap you are comfortable losing. One run costs money on your own account, and [web search](../glossary.md#web-search) is billed in addition to the text on some of them. Check each company's pricing page. Prices are not stated here because they change.
   You'll know it worked when each billing page shows your cap. If you cannot find a limit setting, ask yourself if that company is worth the risk, and skip it.

3. **AV-FU-02-3.** Give the runner the key without writing it in any file. In the [terminal](../glossary.md#terminal), type the first line below, press Return, then type or paste your key. Nothing appears while you type, and that is on purpose. Press Return again. Repeat with the matching name for each company (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, PERPLEXITY_API_KEY).
   ```
   read -s ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY
   ```
   You'll know it worked when typing `echo ${#ANTHROPIC_API_KEY}` prints a number above zero. That prints the key's length, not the key. If it prints 0, try again. If the terminal window closes, you must do this again; that is the cost of keeping keys off your disk.

4. **AV-FU-02-4.** Never put a key in `config.json`, in a chat, in a screenshot, or in a shared folder. If one leaks, delete the key in that company's account and make a new one. The runner never prints keys, and it hides them if one appears in an error message.
   You'll know it worked when `grep -c KEY config.json` prints 0. If a key is anywhere it should not be, it's E32.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FU-02-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

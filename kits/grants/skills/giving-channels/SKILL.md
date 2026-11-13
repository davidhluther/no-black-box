---
name: giving-channels
description: Open the ways of giving that most small nonprofits lack, beyond grants. Covers donor-advised fund gifts, employer matching gifts, monthly giving, gifts of stock and IRA distributions, gifts in a will, and round-up programs, with page copy, donor letters, a setup checklist for each channel and a way to record each gift. Use when someone asks how to get more donations, make giving easier, or set up a donate page for stock, IRA or fund gifts.
---

# Giving channels

Works in: Claude Code, Claude.ai, ChatGPT. Everything here is text, checklists and templates. Nothing needs a script.

Most small nonprofits already accept gifts from donor-advised funds, IRAs, brokerage accounts and estates. What they often lack is an easy path: a donate page covers all four in one paragraph, so donors have to call a broker, read out account numbers or email staff. These gifts mostly arrive in November and December, so the work is best done by early fall.

None of these channels replaces a major grant. Their value is that they are cheap to open, they compound, and most take days, not months. The pages and letters here remove the "we should set that up sometime" excuse. A person still has to open the doors.

Read the organization's name, EIN, mailing address, development contact and website from the kit's `config.json` or the tracker's Settings tab. Ask for anything missing. Never invent an account number, a DTC number or a tax statement.

## What a person must do

No AI model or script should do these. List them for the person in plain steps.

- Create accounts and accept terms for any donation tool.
- Connect or change the donation platform and publish to the live site.
- Open a brokerage account that can receive securities, and supply its details.
- Confirm tax and legal wording with the organization's accountant or attorney. All donor-facing tax text in this skill is general information, not tax advice, and carries a disclaimer.

## Channels

Details, steps, owners and time estimates for each channel are in `references/channels.md`. In order of effort:

1. Donor-advised funds. A donor-advised fund (DAF) is a charitable account a donor holds at a sponsor such as a community foundation or a brokerage's charity arm. The donor recommends grants from it. A free widget or a plain page with the EIN and mailing address is enough to start.
2. Employer matching gifts. Many employers match employees' donations, and most donors never claim it. Start with plain text on the donation form and confirmation page. Add a search tool later if gifts justify it.
3. Monthly giving. Recurring gifts smooth cash flow. This is usually a setting in the donation platform already in use.
4. Stock and IRA gifts. A gift of stock needs a brokerage account that can receive it. A qualified charitable distribution (QCD) is a gift sent straight from an IRA to a charity by a donor aged 70½ or older, and it is not counted as taxable income for the donor. Check the current annual limit at irs.gov.
5. Gifts in a will. The cheapest channel and the slowest payoff. A page with sample language, plus personal conversations with the most loyal donors.
6. Round-up and rewards programs. Grocery-card rewards and utility or retail round-up programs are enrollments, not builds.

## Templates

In `templates/`: a year-end DAF reminder, a monthly-giving appeal, an IRA and QCD donor letter, a gift-in-a-will soft ask, and matching-gift copy for the form, the confirmation page and a follow-up email. Fill the bracketed parts. Keep the tax disclaimer.

## Recording gifts

`references/gift-records.md` explains how to keep four kinds of record apart (confirmed payment, pending transfer, bequest intention, estate gift received), how to tag each channel in a donor database or sheet, how to thank donors for each kind of gift, how to handle gifts that arrive with no name, and a one-table quarterly report for the board.

## Suggested order

1. Weeks one and two. Donor-advised fund page, gift-in-a-will page and monthly-giving form live.
2. Weeks three and four. Matching-gift text on the donation flow. Stock and IRA page once the brokerage account is confirmed.
3. Ongoing. Round-up enrollments, and personal will conversations with loyal donors.

## Costs

Do not quote a tool's price from memory. Tools in this space change prices often and some charge a share of each gift. Before recommending a paid tool, read its own pricing page, write down the date, and work out the cost on a sample gift. Compare it with the free path. Subscription tools only make sense once you know you are losing gifts the free path cannot catch.

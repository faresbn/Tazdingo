# Settled decisions

Each line is something Fares decided, or approved, with the reason and the date. Flag it before proposing to change one. Newest first within each group.

## What the site is

- **A nest in the corner, not a competitor** (26 Oct). ForeverDB, Wowhead and others do databases and guides at scale; Forever Ledger records our own prices and findings and curates the best of everyone else, credited. ForeverDB's Auction House is a second opinion, not a rival.
- **Everything is the journal** (26 Oct). There are no "journal entries": the site is made of living pages (one per spec, class, profession, world topic and More list) that grow over time. Updates come from conversations in the shared ChatGPT project.
- **Who it's for** (26 Oct). It's public and impersonal: it never names Fares or Mike and never mentions ChatGPT. ChatGPT reads the plain-text files; people read the pages.
- **The front page is a dashboard** (27 Oct): countdown, launch checklist, market pulse, Blizzard's latest posts, class picker, latest changes. Fares found the earlier front page "a bit meaningless" and asked for a blue tracker.

## Name and brand

- **Forever Ledger, "Ledger" for short** (26 Oct), with the sub-header "An unofficial journal for World of Warcraft: Forever" (game name spelt out, for legal clarity). Trail & Tally ("T&T") is the alternative Fares liked. The name lives in one constant (`SITE_NAME` in scripts/pages.py).
- **Domain: not yet chosen** (26 Oct). Blizzard's Legal FAQ says no to domains containing "some portion of your product names", so "forever" in a domain carries some risk; Fares decides when he buys one.
- **Inspired by WoW Forever, never its marks** (26 Oct): no logos, key art, screenshots we didn't take, game typefaces or lookalikes, official frames or copied layouts. Footer: not affiliated, plus Blizzard's trademark notice.
- **Images must look like they're from inside the game** (27 Oct): in-game scenes and item-like objects, high-definition and hand-painted in feel, never abstract art. Generated through Codex until launch; Fares's own screenshots after.
- **The design is a quartermaster's field ledger** (27 Oct, after a design consultation): a canvas work surface, a paper sheet, spruce-ink links, an oxblood accent; gold, silver and copper only for money; class colours only for classes. Literata for headings, Source Sans 3 for text. Light and dark follow the device, with a toggle.

## Content

- **Summaries, never copies** (26 Oct): every page summarises guides in our own words, cites them, and links them. Diversify: Wowhead, Icy Veins, ForeverDB, WoWSims, Method, Warcraft Tavern and others, not ForeverDB alone.
- **Pre-launch data is labelled and replaceable** (26 Oct). Pages are Pre-launch by default and become Live only when checked in the live game (27 Oct, after the senior review).
- **Four sections per page** (27 Oct): At a glance, What the guides say, Ledger findings, Read more. Findings are dated entries with a confidence (idea, testing, tested, outdated), never deleted, only marked outdated.
- **Per-spec pages with hover menus** (27 Oct). Specs include hybrid builds; placeholder pages are acceptable but link to the best guides.
- **Scope of tracking** (26 Oct): prices and volatility, classes and specs, professions, camping, Legacy, Merchant's Favor, rares, zones, dungeons and raids, collections, addons, macros, known issues (including macOS).

## Prices

- **Typical price is the median of daily lows over the last seven days** (26 Oct), after real Beta data showed troll listings and one-day spikes.
- **Volatility matters as much as the price** (26 Oct): every item shows steadiness, and the gold-making tables skip volatile or thinly traded items.
- **Beta data is a reference sample** (26 Oct): only the items the tables need, labelled Beta; the full Beta catalogue isn't published. The launch level cap is 60 (the Beta's was 30).

## How updates arrive

- **ChatGPT commits directly; the site is built assuming it can** (26 Oct). OpenAI documents the GitHub connector as read-only, so this is untested. The fallbacks: a custom MCP connector in the Business workspace (plan v2, section 3), or pasting the file ChatGPT writes into GitHub's web editor.
- **When to write is ChatGPT's call** (26 Oct), guided by UPDATING.md.
- **A record and a backup of every change** (27 Oct): kept automatically by the archive Action in `archive/`, so the record doesn't depend on ChatGPT.

## Working practice

- **Checkpoints to GitHub every 25–40 minutes on long runs, with updates in chat** (26 Oct).
- **Update the packages the repo's work needs** (27 Oct): for this repo, keep tools current (Node, Codex, Python) when they're outdated or vulnerable.
- **Leave a running record** (27 Oct): docs/HANDOVER.md, kept current, so another thread, LLM or machine can carry on.

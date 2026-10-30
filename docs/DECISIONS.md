# Settled decisions

Each line is something Fares decided, or approved, with the reason and the date. Flag it before proposing to change one. Newest first within each group.

## A public repository, a feed and an inbox (30 October)

Decided by Fares on 30 October; the plan, research and review are in `docs/sessions/2026-10-30-public-inbox/`.
- **The repository is public** (was: private, only `dist/` published): "there's no actual added value in keeping the repo private". The site stays impersonal; the repository isn't. Commits from 30 October use the GitHub private address (`195290664+faresbn@users.noreply.github.com`); older commits keep the work address.
- **Original Lua files are committed** (was: never commit SavedVariables): "lua files are not secrets ... They're just game data". Any addon's file, kept unchanged at `data/captures/<environment>/<addon>/`.
- **ChatGPT reads the repository, visitors read the website.** `feed/index.md` is a map only ("a guide that sends ChatGPT into each file as needed"); prices are small committed markdown files in `feed/`; guide pages are read straight from `content/`. "I still want the website to be the main place that faresbn.github.io/Tazdingo/ takes visitors."
- **ChatGPT writes through the inbox** (was: ChatGPT commits directly). Codex and Claude still commit to `main`; Fares can override either on request.
- **A route for anyone without GitHub exists** (was: parked), for Fares and any co-player: a hidden form at `inbox/` on the site, a personal key each, and the instructions in `docs/chatgpt/TAZDINGO_INBOX.md`.
- **The receiver is a second ChatGPT Site** (`inbox-site/`), so the system gains no new service: "the more third-party services we throw in, the harder it is to keep track of an otherwise very simple system". A Cloudflare Worker is the fallback; Vercel and Google Apps Script were rejected. The news relay keeps its rule of never holding GitHub credentials; the inbox Site holds a token limited to this repository.
- **Truth is checked by provenance, attribution and review, not by code.** Enforced rules: findings need a confidence, a date and how they're known, and are never deleted; source summaries link their sources; costs name their source; links are plain and real. Personal keys make every submission attributable. Fares approves, as pull requests: a page set Live, a changed recommendation, a finding marked outdated, a site no page has cited before. A free GitHub Models comment was left out for now.
- **"Co-player", not a name,** in the docs: "not for anonymity but for inclusivity (it can be anyone)".

## The Auction House (27 October, evening)

- **The Auction House is the priority** (Fares): "push the envelope on AH tracking" while still improving the rest.
- **Every scan is kept** (Fares): per-scan tracking "up to and including the past 30 scans or 30 days (whichever is further back in time)"; older scans fold into a permanent daily archive. Three or four scans a day are planned after launch.
- **Alerts and investments** (Fares): unusually low prices on the homepage; track what's worth investing in; study patterns by time of day, weekday and raid season, and how well things sell. The data holds no sales, so "how well it sells" is shown as listing activity and every alert says which scan recorded it (`scripts/market.py`).
- **The investment watch skips volatile, too-new and thinly listed items**, following the gold-making rule below.
- **PvP lives with classes and specs** (Fares): a dedicated PvP section per class and spec; no general PvP section yet, as no full dungeon and raid section is needed yet. Writing it belongs to the next content phase.
- **Taken autonomously on Fares's instruction, reversible:** the menu says "Auction House" (addresses stay `prices/`); the strapline is "An unofficial field guide and market tracker for World of Warcraft: Forever" (Fares disliked "A Horde-side field guide"; the game name stays spelled out); More has an overview page; search sits on every page; ForeverDB API data is fetched from the Mac (an Actions secret would be a repository settings change). See `docs/sessions/2026-10-27-site-plan/plan.md`.

## What the site is

- **No homepage repository changelog** (27 Oct): Fares removed “Latest in Tazdingo” from the front page. The class picker takes the full row. Individual pages retain their source/update history.

- **A nest in the corner, not a competitor** (26 Oct). ForeverDB, Wowhead and others do databases and guides at scale; Tazdingo records our own prices and findings and curates the best of everyone else, credited. ForeverDB's Auction House is a second opinion, not a rival.
- **Everything is the journal** (26 Oct). There are no "journal entries": the site is made of living pages (one per spec, class, profession, world topic and More list) that grow over time. Updates come from conversations in the shared ChatGPT project.
- **Who it's for** (26 Oct). It's public and impersonal: it never names Fares or any co-player and never mentions ChatGPT. ChatGPT reads the plain-text files; people read the pages.
- **The front page is a dashboard** (27 Oct): countdown with a Pre-launch checklist tag, the Auction House card, Blizzard's latest posts, class picker (the changelog was removed, below). Fares found the earlier front page "a bit meaningless" and asked for a blue tracker.

## Name and brand

- **Authentic imagery first** (27 Oct): Fares authorised official/publicly reusable Warcraft scenes, creatures, weapons and objects, with sources and credits. This supersedes the earlier generated-only/own-screenshots-only restriction. Use documented reuse terms; distinguish Classic art from Forever screenshots; keep original compositions and separate site branding.

- **Tazdingo** (27 Oct): selected by Fares; rename the site and repository, keep GitHub Pages. Horde identity comes through races, landmarks and perspective rather than red faction colour. Alliance content remains welcome. "Loktar Ogar" can be used playfully in wider Horde/Orc contexts.
- **News classification** (27 Oct): read full Blizzard posts and linked articles, classify dedicated Forever news versus mixed roundups, and hold ambiguous/unreadable articles back. Mixed roundups get a tag on the inner page and never appear on the homepage.
- **Visitor refresh** (27 Oct): a small read-only relay is authorised, with cache/load controls. It is separate from Pages hosting; GitHub Actions continues to collect directly from Blizzard. No private publishing credentials enter browser code.


- **Historical name: Forever Ledger, "Ledger" for short** (26 Oct, superseded by Tazdingo on 27 Oct), with the sub-header "An unofficial journal for World of Warcraft: Forever" (game name spelt out, for legal clarity). Trail & Tally ("T&T") is the alternative Fares liked. The name lives in one constant (`SITE_NAME` in scripts/pages.py).
- **Domain: not yet chosen** (26 Oct). Blizzard's Legal FAQ says no to domains containing "some portion of your product names", so "forever" in a domain carries some risk; Fares decides when he buys one.
- **Earlier generated-only direction, superseded above** (26 Oct): no logos, key art, screenshots we didn't take, game typefaces or lookalikes, official frames or copied layouts. Footer: not affiliated, plus Blizzard's trademark notice.
- **Images must look like they're from inside the game** (27 Oct): in-game scenes and item-like objects, high-definition and hand-painted in feel, never abstract art. Originally generated through Codex until launch; superseded by authentic sourced imagery above.
- **The design is a quartermaster's field ledger** (27 Oct, after a design consultation): a canvas work surface, a paper sheet, spruce-ink links, an oxblood accent; gold, silver and copper only for money; class colours only for classes. Literata for headings, Source Sans 3 for text. Light and dark follow the device, with a toggle.

## Content

- **Summaries, never copies** (26 Oct): every page summarises guides in our own words, cites them, and links them. Diversify: Wowhead, Icy Veins, ForeverDB, WoWSims, Method, Warcraft Tavern and others, not ForeverDB alone.
- **Pre-launch data is labelled and replaceable** (26 Oct). Pages are Pre-launch by default and become Live only when checked in the live game (27 Oct, after the senior review).
- **Four sections per page** (27 Oct): At a glance, What the guides say, Field findings, Read more. Findings are dated entries with a confidence (idea, testing, tested, outdated), never deleted, only marked outdated.
- **Per-spec pages with hover menus** (27 Oct). Specs include hybrid builds; placeholder pages are acceptable but link to the best guides.
- **Scope of tracking** (26 Oct): prices and volatility, classes and specs, professions, camping, Legacy, Merchant's Favor, rares, zones, dungeons and raids, collections, addons, macros, known issues (including macOS).

## Prices

- **Typical price is the median of daily lows over the last seven days** (26 Oct), after real Beta data showed troll listings and one-day spikes.
- **Volatility matters as much as the price** (26 Oct): every item shows steadiness, and the gold-making tables skip volatile or thinly traded items.
- **Beta data is a reference sample** (26 Oct): only the items the tables need, labelled Beta; the full Beta catalogue isn't published. The launch level cap is 60 (the Beta's was 30).

## How updates arrive

- **ChatGPT commits directly** (26 Oct; superseded on 30 Oct by the inbox, above). A route for someone without a GitHub account was parked on 27 Oct and built on 30 Oct.
- **When to write is ChatGPT's call** (26 Oct), guided by UPDATING.md.
- **A record and a backup of every change** (27 Oct): kept automatically by the archive Action in `archive/`, so the record doesn't depend on ChatGPT.

## Working practice

- **Checkpoints to GitHub every 25–40 minutes on long runs, with updates in chat** (26 Oct).
- **Update the packages the repo's work needs** (27 Oct): for this repo, keep tools current (Node, Codex, Python) when they're outdated or vulnerable.
- **Leave a running record** (27 Oct): docs/HANDOVER.md, kept current, so another thread, LLM or machine can carry on.


## Recommendation evidence (27 October 2026)

Each guide now distinguishes a short **Tazdingo recommendation** from attributed source detail and Field findings. It should resolve obsolete factual conflicts against later official changes, and explain real trade-offs by role, level, equipment and encounter rather than vote between websites. Source dates and model snapshots do not establish in-game verification. Market tables describe estimated listing margins and priced fill bundles; they cannot establish sales, demand, total crate cost or guaranteed profit. See `docs/sessions/2026-10-27-content-review/review.md` for the initial sweep's scope and remaining uncertainty.

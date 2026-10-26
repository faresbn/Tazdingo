# FvrJournal redesign: plan v2, for approval

26 October 2026. Replaces v1 after Fares's seven points and four research sweeps (sources and checks in research.md). Note 4 from the first round (no names or ChatGPT on the public site) is already live.

## In short

- **What it is:** a small nest in the corner. It records what we learn and what our scans show, and leans on other sites (credited, never copied) for everything else. It doesn't compete with ForeverDB or Wowhead.
- **Front page journey:** launch countdown, then search, then a dated log of what changed, then five doors: Prices, Classes, Professions, World, and More (a dropdown with addons, macros and known issues).
- **Pre-launch data is marked "Pre-launch"** everywhere it appears, and is replaced when live data arrives.
- **ChatGPT updates the site through our own small connector** in the Business workspace. It can read the journal and submit updates to an inbox; a GitHub Action checks each update, files it in the right place and publishes it. A five-minute test in the shared project comes first.
- **Design:** follows the system's light or dark setting, with a toggle. It feels like the game through your own screenshots, item icons and the game's quality and class colours, with no Blizzard logos, art, lettering or frames.

## 1. Who comes, and the journey

Research shows what Forever players come to sites for, by what those sites put first: launch timing, calculators and class changes, spec guides, and price lookups. Our nest adds what only it has: our own prices and their volatility, our own notes, and one curated, credited place to start for everything else.

**Intents, most frequent first:**
1. "What's X worth, and how sure is that?" (price plus volatility)
2. "How do I make gold?" (what to craft, what to gather, cheapest Merchant's Favor)
3. "How should I play my spec?" (9 classes × 3 specs, plus hybrid builds)
4. "How does this new system work?" (camping, Legacy, Favor, professions, rares, zones)
5. "What changed?" (our log, and launch versus pre-launch data)
6. "Fix my setup" (addons, macros, known issues such as the macOS GPU hang)

**Front page, top to bottom:**
1. A countdown: "Forever opens in 9 days", which becomes "Day 3 of Forever" after launch. The log uses the same day count, which suits a journal.
2. One search box covering items, classes, specs and topics.
3. **Latest:** each change, newest first, built automatically from the site's history.
4. Five doors, always in this order and also in the navigation: **Prices · Classes · Professions · World · More ▾**.

**Rule we stick to:** every page opens with what it is and how current it is (last updated, Pre-launch or Live), then gives the answer, then the next step. Its change log sits at the bottom.

## 2. Sections and their data

| Section | What it shows | Where the data comes from |
|---|---|---|
| **Prices** | Market pages as now, plus **volatility** (steady / moving / volatile, from how far each item's daily lows swing over 14 days) and a market-wide volatility trend. Each item links to ForeverDB, TheWoWDB and auctionhouse.fyi for comparison | Our scans (primary); others as links |
| Prices → **What to craft** | Recipes ranked by margin: product price minus reagents. Only items with enough volume, and not flagged volatile, count | ForeverDB recipes (GPL data) × our prices; vendor reagent prices need the ForeverDB API key |
| Prices → **Merchant's Favor** | Each Waylaid Crate's material cost per point of Favor, cheapest first | ForeverDB Favor data × our prices |
| Prices → **Gathering** | What each herb, ore and leather is worth now, by skill tier | ForeverDB gathering data × our prices |
| **Classes** | 9 classes → 3 spec pages each plus a hybrid-builds page. Each holds our notes (status idea / testing / tested), talents, macros and addons for that class, and **"Elsewhere"**: cited links to Wowhead, Icy Veins, Method, ForeverDB and other guides. Empty specs say "No notes yet" and still show the links | Our notes; ForeverDB talent data; cited links |
| **Professions** | One page per profession: recipe counts (and how many are new in Forever), top margins, its camp feature, levelling-guide links | ForeverDB data; our prices; links |
| **World** | Camping (the campfire system), Legacy, Merchant's Favor and reputation, Rares, new zones, collections | ForeverDB data; our notes; links |
| **More ▾** | Quick lists: **Addons** (Forever status per addon, where to get it), **Macros** (per class, ours plus linked collections), **Known issues** (official items plus player-reported ones, each with status and date), **Sources and credits** | CurseForge, Kami Labs, Blizzard forums and blue tracker, our notes |

**Pre-launch tagging.** Every fact derived from data carries its source and the game build. Anything from before launch, or not yet seen in play, shows a **Pre-launch** label and can be replaced. When ForeverDB's data moves to a post-launch build, the refresh replaces those values and the labels clear by themselves. Our own notes carry their own status.

**Diversified sources.** ForeverDB is the main data source only because its addon data is licensed for reuse. Prices are ours; guides, calculators, macros, addons and known issues point to several sites. Wowhead's terms forbid copying and scraping, so Wowhead content appears as links and tooltips only.

## 3. How ChatGPT reads and updates the site

What the research established: ChatGPT's GitHub connector is **read-only**. ChatGPT Business can use a **custom connector (MCP server) with write actions**, which only a workspace admin or owner can add, and which works on the web but not the phone app. Whether these connectors work inside shared projects isn't documented.

**Design: one small "FvrJournal" connector,** hosted on Vercel's free tier, with its code in this repo:
- **Read tools** (search, fetch a page, get an item's prices) read the published site directly. Both you and Mike can then ask about the journal in any chat, with no GitHub account and no pasted links. This also fixes "ChatGPT can't open the site".
- **One write tool, `submit_update`,** accepts one structured update: what it is (a spec note, a known issue, a macro…), where it belongs, the text, its status and its sources. It does only one thing: it opens a GitHub issue labelled `inbox`. Its GitHub token can only write issues on this repo.
- **The router (a GitHub Action)** picks up each inbox issue. It checks the format, refuses names or mentions of ChatGPT, and checks the links. It writes the update into the right page, commits with a one-line summary, publishes, comments with the link and closes the issue. A rejected update gets a comment saying why and stays open. No AI runs in the Action, so what gets published is predictable.
- **When ChatGPT submits** is decided in the project's instructions, which tell ChatGPT how to recognise something settled and worth recording. That's ChatGPT's workflow to own, as you asked.
- **Safeguards:** ChatGPT confirms before each write. The connector's address contains a secret known only to the workspace admin. Every update stays visible as an issue, so it can be reverted.
- **First, a five-minute test:** you add a bare connector in the workspace and try it from the shared project. **If shared projects can't use it,** the fallback keeps everything else: ChatGPT writes the same update block in chat, and you paste it into a GitHub issue form from your phone. The router is identical.

## 4. Design

- **Theme:** follows the device's light or dark setting, with a toggle in the masthead (system, light, dark) that's remembered per browser.
- **In-game feel, within Blizzard's limits:** your own screenshots after launch (Blizzard's FAQ allows player screenshots for non-commercial use); item and spell icons through tooltips; the game's item-quality and class colours, which every database site uses; coin colours for prices.
- **Never:** Blizzard logos, key art, Friz Quadrata or Morpheus lettering, official frames or copied layouts. Our own mood palette (dusk teal, cream, parchment, a gold accent, all our own values), our own type pairing and our own surveyor's-map ornaments. Until launch, the hero uses original painterly art (generated, for your approval); your screenshots take over afterwards.
- **Footer:** "Not affiliated with or endorsed by Blizzard Entertainment", plus Blizzard's standard trademark notice. No ads.

## 5. Name

- **For now:** **FvrJournal**, with the sub-header **"An Unofficial WoW Forever Journal"**, as you chose.
- **One trade-off to know:** "WOW" is a registered trademark, and having it in the sub-header puts it inside the name's lockup. "An unofficial journal for World of Warcraft: Forever" reads more like a reference to the game than part of our brand. Your call; I'll use yours unless you change it.
- **For the domain:** Blizzard's FAQ says no to domains containing any part of its product names, so the final name shouldn't contain "Fvr" either.

**Final-name shortlist** (availability checked 26 October; nothing reserved):

| Name | .com | .gg | Why it fits |
|---|---|---|---|
| **Campfire Ledger** (recommended) | ✅ | ✅ | Forever's campfire system, a small nest in the corner, and a ledger of prices and notes. Warm, ownable and specific to Forever without naming it |
| Wayfarer's Ledger | ✅ | ✅ | An adventurer's notebook |
| Trail & Tally | ✅ | ✅ | The journey plus the counting |
| Long Road Journal | ✅ | ✅ | The 1–60 road |
| Copper Ledger | ✗ | ✅ (.net too) | Auction House first |
| Everlog | ✗ | ✅ | "Forever" by synonym, the shortest of the set |

## 6. Build order (9 days to launch)

- [ ] **By 29 Oct:** structure, front-page journey, theme toggle and design; class and spec pages; More lists seeded from sources; Pre-launch labels; volatility; interim name. Checkpoints every 25–40 minutes.
- [ ] **By 2 Nov:** connector and router (after your test); ChatGPT project instructions and source files; What to craft, Merchant's Favor and Gathering from ForeverDB data.
- [ ] **Launch week:** first live scans; data refreshed to the live build so labels clear; review loop on phone and desktop.

## Decisions needed

1. **The journey and the five doors** (Prices · Classes · Professions · World · More ▾): approve or adjust.
2. **The connector:** build the FvrJournal connector (read plus inbox) on Vercel, and you run the five-minute shared-project test when I hand you the bare version. Yes or no?
3. **ForeverDB API key** (optional): needed for vendor reagent prices, disenchanting and beta-versus-live changes. Only you can request it (Battle.net login on foreverdb.net/developers).
4. **Final name:** pick from the shortlist, or ask for another round. FvrJournal is used until then.
5. **Hero art:** generated original art until launch, then your own screenshots: yes or no?

# Research: hosting limits, site structure, page templates, ForeverDB API and copy

27 October 2026, eight days before launch. This feeds `plan.md` in this folder. Everything here was read from the repository, the built site (`dist/`), the live site or the cited sources; one agent explored the ForeverDB API with the key (raw notes in `sources/foreverdb-api.md`), and I re-checked its main claims. Nothing is decided here; the questions at the end are what the plan needs from Fares.

**Update, evening of 27 October.** Fares made the Auction House module the priority ("push the envelope on AH tracking"), asked for per-scan tracking over the last 30 scans or 30 days (whichever reaches further back), alerts for unusually low prices, investment tracking, and the study of price patterns by time of day, weekday and raid season, plus volumes sold. He asked me to plan and build autonomously, consulting Sol as needed. Section 6 covers what that needs; the questions at the end now note which ones the plan answers itself.

## In short

1. **GitHub Pages only serves files.** Nothing runs when someone opens a page. All "server" work happens in GitHub Actions *before* publishing (on a push, on a timer, or on a button press), in the visitor's browser, or on the separate news relay. That covers everything Tazdingo does now, including a ForeverDB refresh that wouldn't need the Mac.
2. **The menu works, but its labels and links are inconsistent.** Four of the five top items open an overview page; "More" jumps to the launch checklist. "Prices" holds two different things (market price lists and gold-making). World mixes game systems with places. The lower half of the homepage repeats the menu, and search exists only on the homepage.
3. **The four-section page template (a settled decision) fits specs and professions, and is forced onto everything else.** The launch checklist's steps sit under "What the guides say"; each class page stitches three files and three spec summaries into one (about 3,700 words, three "At a glance", three empty "Field findings"). Within one page type the sub-headings drift (five wordings of "where the guides disagree").
4. **Field findings are empty in all 77 content files** (77 empty sections across 59 published pages). The site's own voice is so far only the "Tazdingo recommendation", which reads as a list of cautions (88 "does not / is not / do not / are not" constructions in 77 short sections).
5. **ForeverDB's API gives us the "where and how" our pages lack:** where to learn and buy every recipe (with Merchant's Favor costs), where to gather, what each class learns at each level, disenchanting, vendor stock. Not prices, talents, Legacy, rares or camping. Everything is still the last Beta build, so it needs a re-fetch at launch.
6. **The Auction House can do much more with the same uploads.** Each Auctionator upload carries the latest price of every item seen; keeping each upload as a compact scan record (about 27 bytes per item, against 440 today) makes per-scan history, intraday and weekday patterns, deal alerts and investment estimates practical. What it can't give is sales: Auctionator records prices and the most units listed each day, never what sold (section 6).
7. **Copy:** "Horde-side" appears three times on the homepage's first screen, market names are raw realm strings ("ClassicBetaPvP"), several labels describe the mechanism instead of the benefit, and some fixed text promises findings that don't exist yet.

---

## 1. What GitHub Pages can and can't do

**What it means for us:** the site can update itself on a schedule or on a trigger, fetch data with secret keys, and be as interactive as JavaScript in the browser allows. It cannot react to a visitor on the server: no logins, no saved forms, no live per-request data, no secrets in pages, no redirects, no visitor statistics. For those, we'd need a separate small service, as we already have for news.

**How it works.** Pages is a file host with a CDN in front. A *build* is a GitHub Actions job (`.github/workflows/pages.yml`) that runs our Python scripts on a fresh Linux machine, produces `dist/`, checks it and hands the folder to Pages. After that, visitors only ever download files. So "server-side scripts" means scripts that run at build time, not at view time. If any test or check fails, nothing is published and the previous site stays online.

### The three places code can run

| Where | When it runs | What it can do | What it can't do |
|---|---|---|---|
| **GitHub Actions** (build time) | On a push to `main`; on a timer; on a manual button (github.com or the GitHub phone app); on an external call (`repository_dispatch`, needs a token); after another workflow | Run any script, call APIs with secret keys stored as repository secrets, commit back to the repo, build and publish | React to a visitor; run exactly on time (see timers below) |
| **The visitor's browser** | Every page view | Search, filters, countdown, theme, fetching public APIs that allow it (the Refresh news button) | Hold secrets (anything in a page is public); save anything other visitors or the repo can see (it can remember a visitor's own settings, as the theme toggle does) |
| **The news relay** (a small Worker on chatgpt.site, separate from GitHub) | Every request to `/news` | Read Blizzard's posts live, cache them five minutes | By decision, it never holds GitHub credentials and never publishes |

Fares's Mac is a fourth, manual place: scan files exist only there, so `ingest.py` must run there.

### Triggers and timing, as observed

- **Push to `main`:** observed publish runs took 31–70 seconds, and the live site sends `cache-control: max-age=600`, so a returning visitor's browser may keep the previous version for up to **10 minutes**. These are observations, not guarantees: GitHub notes that publishing can take longer, and runs can queue.
- **Timer (`schedule`):** best-effort. GitHub's docs say scheduled runs can be delayed at busy times and dropped under heavy load. Observed: the two-hourly job was added on the evening of 26 October and, by 17:15 UTC on 27 October, had fired three times (01:32, 08:03 and 14:41 UTC), where ten were due (the job runs at 23 minutes past every second hour). Good for "roughly a few times a day"; wrong for anything that must happen at a given minute. That's why the countdown now runs in the browser.
- **Manual button (`workflow_dispatch`):** starts a run on request (subject to queueing) from github.com or the GitHub phone app. Already enabled on `pages.yml`.
- **External trigger (`repository_dispatch`):** any service holding a token can ask for a run. This is how a future ChatGPT connector (parked) could request a rebuild. The news relay could too, technically, but that would change the settled boundary that it never triggers publishing, so it would be a reconsideration.
- **A gotcha:** a commit made by a workflow with its default token does not start other workflows (the archive Action relies on this to avoid loops). A future "fetch ForeverDB data and commit it" job must therefore build and publish in the same run, or start the publish workflow explicitly.

### Limits

- Published site: 1 GB maximum (we're at 6.6 MB). Bandwidth: 100 GB a month, soft. Deploys time out after 10 minutes. The "10 builds an hour" limit doesn't apply to Actions-built sites like ours. ([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits))
- The repository is private and the site public. Publishing Pages from a private repository needs a paid plan (Pro, Team or Enterprise), so the account is on one of those.
- **Whether publishing uses Actions minutes is unclear.** GitHub's docs conflict. The Actions billing page lists standard runners as free "For GitHub Pages" ([Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)); the Pages setup page says private repositories pay for usage beyond the monthly allowance ([creating a Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)). GitHub's run-timing API reports zero billable time for every one of our runs, which fits the free reading. If minutes do count: Pro and Team include 3,000 a month, shared across the account's private repositories (Brew also publishes through Actions), each job is rounded up to a whole minute ([job execution time](https://docs.github.com/en/actions/how-tos/monitor-workflows/view-job-execution-time)), a publish run is two jobs, and the two-hourly timer alone would come to about 720 minutes a month if every run fired. The archive workflow isn't a Pages workflow, so it would count either way. Measured: 38 runs (73 jobs) between the repository's first run on 26 October and 17:15 UTC on 27 October. Only github.com's billing page settles it (the `gh` login lacks the scope).
- **No visitor statistics.** Pages records nothing we can read about traffic. Counting visits needs something outside Pages to receive the counts: a third-party analytics service, or a small collector of our own (like the relay) fed by our own script. Either way it's a privacy and outward-facing choice, with separate questions of provider, what's recorded and how long it's kept. A third-party script on every page already has a precedent: ForeverDB's tooltip script (section 2).

### What this means per kind of update

| Update | Today | Could be |
|---|---|---|
| Prices | Mac: scan → `ingest.py --push` | Same; the scan file only exists on the Mac |
| Guide pages | ChatGPT commits → publish; archive backs up. Fares confirmed on 27 October that ChatGPT made the edits since the FvrRepo days; its commits carry his GitHub identity. HANDOVER and STATUS still call this untested and are due for the end-of-session docs update | Same; a route for someone without a GitHub account was parked by Fares on 27 October |
| ForeverDB data | Mac, by hand or through `ingest.py` (`foreverdb_data.py`, `item_names.py`); both read public files and need no key | These two could move to an Action today with no secret. The new API fetch needs the key as a repository secret |
| Blizzard posts | Scheduled Action, and the relay for visitors | Same |
| Countdown | Browser (since today) | Same |
| Rebuild on demand | Push something | The existing manual button on `pages.yml` |
| Moved pages | n/a | No server redirects: an old address can only forward through a small HTML page left in its place |

---

## 2. Site structure: the menu, section pages and the homepage

**What it means:** a visitor can't tell which top item leads to an overview and which jumps to a page; two section names don't describe their contents; the homepage spends half its length repeating the menu; and once off the homepage, there's no search.

### The menu today

| Top item | Label goes to | Panel contains | Overview page? |
|---|---|---|---|
| Prices | `prices/` | "Making gold" (What to craft, Waylaid Crates, Materials worth gathering) + "Markets" (each realm) + All prices | Yes (162 words): making-gold links, a markets table, a steadiness summary |
| Classes | `classes/` | 9 classes × 3 specs | Yes (401): class cards with portraits, summaries and specs; a short essay on hybrids; links elsewhere |
| Professions | `professions/` | Gathering / Crafting / Secondary | Yes (449): cards with recipe counts |
| World | `world/` | 7 topics with one-line summaries | Yes (201): the same 7 with icons and summaries |
| More | `more/launch/` | Launch checklist, Blizzard posts, Addons, Macros, Known issues, Sources and credits | **No.** The label opens the launch checklist |

How a visitor finds out whether a label has an overview: they can't, except by clicking. Each top item is a link (the label) plus a separate arrow button that opens the panel. On a wide screen with a mouse, hovering opens the panel, so clicking the label feels like "go to the section"; four labels do that, More doesn't. On phones (860 px and narrower) the panels stack inside the opened menu, and the label and arrow are separate tap targets.

### What's weak about the names

- **Prices** covers two jobs: *what does X cost* (market pages, the item browser) and *how do I make gold* (craft margins, crates, materials). Until launch, every number in it is Beta data. Names that cover both: *Auction House*, *Market*, *Gold*, *Economy*. "Auction House" is the in-game term players search for; "Gold" names the goal, not the data.
- **Market names** are the Beta's raw realm strings: "PvP" (975 items, three scans, newest 17 October) and "ClassicBetaPvP" (6 items, newest 26 September), each tagged "Forever Beta". Fares confirmed (27 October) that "ClassicBetaPvP" is a Beta name that won't be used later, and that its six items are an incomplete set, not a sign of a small market. How many live markets there will be, and how they'll be split and named, isn't known yet: the launch checklist says Forever has "rulesets, not realms", which suggests a ruleset plus a faction, but that's unconfirmed. Either way the names need a display rule rather than a one-off fix. Every item search result points to the PvP market, and the homepage's market block stays frozen at "Most listed on 17 Oct" until a live scan arrives.
- **World** holds two kinds of thing: *systems* (Camping, Legacy, Merchant's Favor) and *places and content* (New zones, Dungeons and raids, Rare spawns, Collections). Camping is as much a profession topic, and Merchant's Favor is as much gold-making (its crates already have a page under Prices).
- **PvP lives with classes and specs (decided).** Fares decided on 27 October that each class and spec gets a dedicated PvP section, and that a general PvP section isn't needed yet, just as a full dungeon and raid section isn't. Today PvP comes up in passing in 29 content files (22 of them class and spec files), only the Warlock's hybrid page has its own "PvP hybrids" section, the launch checklist has a "Pick a ruleset" step, and each class page links to ForeverDB's PvP guide.
- **More** mixes three things: *getting set up* (Launch checklist, Addons, Macros, Known issues), *news* (Blizzard posts) and *about the site* (Sources and credits). After launch the checklist matters less and known issues more.

### Overlaps (the same subject in two places)

- Waylaid Crates: `prices/crates/` and `world/merchants-favor/`.
- Camp items: `world/camping/` (full table) and each profession page (its own rows).
- Macros: `more/macros/` (how macros work) and each class page (`#macros`).
- Launch checklist: `more/launch/` and the hero tag.
- Blizzard's posts: the homepage and `more/blizzard/`.
- The class picker: the Classes menu, `classes/` and the homepage.

Overlaps aren't wrong (a crate is both a gold topic and a Favor topic), but each subject needs one home, with the other places linking to it.

### Search and items

- **Search** (items and pages, 1,038 entries) is only on the homepage. Inner pages have no search box; the price pages have their own item filter.
- **Items have no pages of ours.** Every item name links to its ForeverDB page, and hover tooltips come from ForeverDB's embed script, loaded on every page. Our own data about an item (typical price, steadiness, latest price, trend) lives only in its row of the market table; searching for an item opens that table filtered to it.

### The homepage today, top to bottom

1. Greeting ("Loktar Ogar · A Horde-side field guide"), countdown + Pre-launch checklist tag, title, one-line description, search, Darkspear scene.
2. **Market pulse** (Beta): a steadiness bar (7% steady, 33% moving, 58% volatile), the five most-listed items (all worth copper: four kinds of ammunition and Linen Cloth), three listing margins.
3. **Blizzard says:** five posts, with Refresh.
4. **Choose your class:** the same 9 × 3 as the menu.
5. **Professions:** the same 12 as the menu.
6. **The world:** the same 7 as the menu.

What other Forever sites lead with (from the 26 October research): a launch countdown, calculators and class changes, a class/spec picker, and item price search. We have the countdown, the picker and search; calculators are linked out, not ours. We have no traffic data of our own (section 1), so homepage choices rest on that comparison and on judgement.

Observations:
- Rows 4–6 repeat the menu. A class or spec picker is a standard entry point on comparable sites, so it earns a place; the profession and world rows less so.
- Row 2 shows Beta data front and centre. HANDOVER notes Beta content is temporary and its prominence isn't a permanent hierarchy problem, so the lasting issue is the metric: "most listed" measures volume, not interest, so it surfaces the cheapest goods.
- Nothing on the homepage is ours yet except prices: there are no findings to show.
- The homepage has three lives. **Before launch:** countdown, checklist, news, choosing a class. **Launch week:** known issues, Blizzard's notices, the first live prices. **After:** what moved in the market, new findings, news. A layout that serves all three by swapping one or two blocks would avoid a redesign at launch.
- Settled (not to reopen): no repository changelog on the homepage; the homepage is a dashboard.

### Blocks available for the homepage

| Block | Source | Useful when |
|---|---|---|
| Countdown, then "Day N" | Browser | Always (wording changes at launch) |
| Launch checklist link | `content/more/launch.md` | Before launch |
| Known issues (count or top items) | `content/more/known-issues.md` | Launch week onwards |
| Search | `search.json` | Always |
| Class picker | `data/game.json` | Always |
| Blizzard's posts | Scheduled collector + relay | Always |
| Steadiness (the pulse bar) | Our scans | Needs three days with records in the last two weeks (`scripts/build.py`): from about day three |
| Market movers list (rising, falling) | Our scans | Under today's rule, from about day 10 at the earliest, depending on coverage: see "Price movement in the first days" below |
| Crafts worth a look | ForeverDB recipes + our prices | After live prices |
| Latest findings | Field findings across pages | Once findings exist |

### Price movement in the first days

**What it means:** Fares plans three or four scans a day in the first days after launch, to track prices moving from the start. Each item's own trend line already works from the second day of records. What doesn't exist early is a ranked *movers list* (biggest rises and falls) for the homepage and market pages: under today's rule it appears from about day 10. Showing movers earlier needs a new rule, and how the scans are imported decides which rules are possible. Both are plan decisions.

**How it works.**
- **One record per item per day.** Auctionator's file keeps that day's lowest price, highest price and quantity listed, plus the item's latest price at the moment the file was written. Several scans on one day all land in the same daily record, and the build combines records for the same day: lowest low, highest high, largest quantity (`scripts/build.py`, `build_markets`).
- **What already shows movement:** each item's sparkline on the market page (`summarise` builds it from daily lows; `scripts/pages.py` draws it once two days have records).
- **The movers list:** a weekly move compares the median daily low of the last seven days with the seven days before, and only counts an item with at least three days of records in each of those weeks, at least 50 copper and some volume (`summarise`, `highlights`). With a record every day from launch day, the earlier week reaches three days on about day 10.
- **Scans are kept only if each one is imported.** `ingest.py` saves one snapshot per import (a second import on the same day gets its own file) and skips a market whose data hasn't changed. Three scans followed by one import keep only the last state. A newer file can also carry an older sighting of an item.

**Two possible early rules, with their catches:**
- **Scan to scan:** the latest price now against the latest price a few hours ago, from consecutive snapshots. Needs an import after every scan (WoW writes the file on logout or `/reload`), and it's noisy: one cheap listing moves it.
- **Day to day:** today's low against yesterday's. Simpler, but biased: today's low is the minimum of an unfinished day, compared with yesterday's minimum over a whole day. With fewer listings seen, today's minimum tends to sit higher, so early in the day it can exaggerate a rise (yesterday 100 copper, today's first scan 150: "up 50%" until a cheaper listing turns up). During the day the signal can only move downwards, and a recovery after an early cheap listing doesn't show until the next day.

Either needs thresholds of its own (volume and price, as the weekly rule has) and a hand-over to the weekly rule once enough days exist. Steadiness already works from about day three.

---

## 3. Inner page templates

**What it means:** pages of the same type should answer the same questions in the same order, so a reader who has used one spec page can use any spec page, and ChatGPT can update them predictably. Today the outer frame is consistent; the inside isn't, and some page types don't fit the frame at all.

**How it works.** Every content file has the same four `##` sections (At a glance · What the guides say · Field findings · Read more). The build places them and adds data blocks and a sidebar (Guides and tools, On this page). The `###` headings inside "What the guides say" are free text, written per page by the research agents.

### By page type

| Type | Pages | Words on the page (median, range) | Consistent? | What's off |
|---|---|---|---|---|
| **Spec** | 27 | 1,510 (1,350–2,290) | At a glance: yes (Role, How it plays, Strengths, Weaknesses, New in Forever; "Stats" on 12 vs "Stats that matter" on 15). Sub-headings: partly | Every spec has a "where the guides disagree" section, in five wordings. "Talents" (9) vs "Talents by level" (18); "Rotation" (6) vs "Rotation and priorities" (9). No data block: talents and abilities are linked out |
| **Class page** | 9 | 3,670 (3,400–4,380) | No | One page built from three class files (overview, hybrid, macros) plus each spec's summary. Three "At a glance", three "Field findings", three "Read more". Overview glance labels vary (Races / Roles / Resource / Hybrid status…) |
| **Profession** | 12 | 1,360 (1,300–1,490) | The most consistent: glance fields Suits, Pairs with, New in Forever, Camp feature on all 12; sub-headings What changed in Forever and Levelling, in brief on all 12, Open questions on 8 | "From the data" sits between the guides and findings; it shows recipe counts, margins and camp items, but not trainers, recipe sources or skill-ups |
| **World topic** | 7 | 1,390 (1,160–2,610) | No, and partly by nature (camping ≠ rares) | Glance bullets are free-form; data blocks exist for 4 of 7 topics. Only Camping's is a table; Rares, Collections and Merchant's Favor get one or two sentences ("354 rare creatures are known…"). Their headings vary: "Every camp item", "Waylaid Crates", "In the data" |
| **More list** | 4 + news + credits | 1,490 (1,440–1,970) for the four lists | No | The guide frame doesn't fit: the launch checklist's 15 steps sit under "What the guides say"; addons, macros and known issues are lists, not guide summaries. Blizzard posts and Sources and credits have their own layouts |
| **Prices** | overview, 2 markets, 3 tables | n/a | Own templates | Fine structurally; naming and Beta labelling are the issues |
| **Section overviews** | 4 (no More) | 160–450 (range) | Similar | Classes has a hybrids essay; Professions has counts; World has icons; Prices has a markets table |

### Things every type shares that aren't pulling their weight

- **Field findings, "Nothing recorded yet."** in all 77 sections: once on each spec, profession, world and More page, three times on each class page. Until the first finding arrives, an empty section on every page signals an unfinished site.
- **Two outbound link lists.** "Read more" (the sources this page cites) and the sidebar's "Guides and tools" (standard links for the page type). On Frost Mage they share no links, so the split is real, but nothing tells the reader why there are two.
- **"Changes to this page"** at the foot of each page, built from git history.
- **Length** is acknowledged as the next phase (writing and automatic updates of inner pages), so the template should be set first and trimming follow it.

### What each type could contain

| Type | Guide prose | Our data | ForeverDB (addon files, today) | ForeverDB API (new) | Links |
|---|---|---|---|---|---|
| Spec | Summary, recommendation, talents, rotation, gear, PvP (decided, not yet written), disagreements | Findings (none yet) | — | Abilities learned by level for its tree | Wowhead, Icy Veins, WoWSims, ForeverDB calculators |
| Class | Changes, choosing a spec, hybrids, macros, PvP (decided, not yet written) | Findings | — | All abilities by level and tree | ForeverDB class pages |
| Profession | Changes, levelling, what's worth making | Margins from our prices | Recipes, camp items | Trainers and locations, recipe sources and costs, skill-up colours, Classic changes; gathering zones; disenchanting | ForeverDB, Wowhead levelling |
| World topic | How the system works | Findings | Camp items, crates, rare and collection counts | Favor vendor stock, dungeon list | Per topic |
| More list | Lists and steps | Findings | — | Player-seen differences (known issues) | Per list |
| Prices | Short notes | Prices, steadiness, history | Other players' prices, vendor prices | Vendor names and locations, sell-to-vendor prices | ForeverDB item pages |

### A settled decision in play

"Four sections per page" (At a glance, What the guides say, Field findings, Read more; findings dated, never deleted) was decided on 27 October. Giving More lists a different frame, or hiding empty Field findings, changes that decision, so either is a **reconsideration request**, not a tidy-up. Fixing the drift *inside* the frame (sub-headings, glance fields) doesn't touch it.

### What a type template would fix, and what changing one touches

A template here means: fixed glance fields, a fixed set of `###` sections in a fixed order (optional ones allowed but named from a list), and a fixed place for data blocks. The build could warn when a page drifts. That makes pages comparable, makes ChatGPT's updates predictable, and lets the next phase's trimming follow a known shape.

Changing templates or moving pages ripples into: `docs/chatgpt/UPDATING.md` (its "Where things go" table and section rules, which ChatGPT follows); the build's list of allowed content files (it rejects unknown files); the archive, which keys its history by file path; `llms-full.txt`, which mirrors the pages; and old addresses (for example `classes/mage/#hybrid`), which can only be forwarded by leaving small HTML pages in place. That last cost is small right now: the site isn't submitted to search engines and has no custom domain yet, so few outside links point at today's addresses. It grows after launch.

---

## 4. Copy

**What it means:** a few phrases set the site's voice, and some say the wrong thing or say it three times. Most fixes are single strings in `scripts/pages.py`, `scripts/sections.py` and `data/game.json`; the guide prose is the next phase.

### The strapline and homepage

| Where | Now | Issue |
|---|---|---|
| Homepage title (browser tab, search results, link previews) | "Tazdingo: A Horde-side field guide to World of Warcraft: Forever" | Two colons; inner pages use "Frost Mage \| Tazdingo" |
| Masthead strapline (every page) | "A Horde-side field guide to World of Warcraft: Forever" | The site's subtitle on every page |
| Hero greeting | "Loktar Ogar · A Horde-side field guide" | The second "Horde-side" on the first screen |
| Hero description | "Auction House prices, Horde-side class and profession guides, and discoveries from our travels in World of Warcraft: Forever." | The third. The guide summaries are faction-neutral; the Sources and credits page says only "field notes and personally collected market data mainly follow Horde characters". "Discoveries from our travels" promises findings that don't exist yet |
| Footer (every page) | "Built 2026-10-27 14:18 UTC, revision f398c5a284dd." | Internal detail |

Background: "Horde-side field guide" arrived with the Tazdingo rebrand commit (`c096b4a`) and isn't a recorded decision, so changing it reopens nothing. Two recorded decisions bear on a replacement: the sub-header spells out "World of Warcraft: Forever" for legal clarity (26 October, recorded under the earlier name; the reason still holds), and the Horde identity comes "through races, landmarks and perspective rather than red faction colour", with "Loktar Ogar" usable playfully (27 October).

### Labels that describe the mechanism, not the benefit

- "Market pulse" with "7% steady · 33% moving · 58% volatile": meaningful only after reading the price page.
- "Listing margins" (renamed on purpose to avoid implying profit; keep the precision, but it needs a plain lead such as "Crafts worth a look").
- "Recipes ranked by estimated listing margin: output asking value minus reagent cost" (Prices overview and What to craft).
- "From the data" (profession pages) and "In the data" (world pages).
- "Last verified check: 2026-10-27 07:38 UTC" (news widget): a machine timestamp where "Checked 2 hours ago" would do.
- "Blizzard says" on the homepage and "Blizzard posts" in the menu, for the same thing.
- "Rare spawns" in the menu; "New zones" for a page that also covers changed zones.
- "All classes, and choosing one" (Classes panel footer).

### Promises and defensive notes in fixed text

- Classes overview: "For every spec: what the best guides say, the links to read them, and what we've found ourselves." Nothing is found yet.
- Field findings placeholder, 77 times across 59 pages: "Nothing recorded yet. Findings from our own play go here, marked with how well they're tested."
- Materials worth gathering: "This does not measure sales or gold per hour." Waylaid Crates: "the crate itself costs extra." Accurate, but they lead with what the page doesn't do.
- 404: "It may have moved when the site was reorganised."

### The guide prose (next phase, noted for context)

- The 77 "Tazdingo recommendation" sections average 95 words. They lead with the right idea in bold, then spend most of their length on what the evidence doesn't prove ("A Forever-tagged download is evidence of intended support, not a successful test on this character"). Accurate, but they read as a reviewer's caveats rather than a guide's advice. A shorter "do this, unless…" shape with one caveat would carry the same care.
- Every guide page carries a Pre-launch badge, correctly, which makes the badge noise before launch. While every page is unchecked, one site-wide notice would say the same once. After launch it stops working: pages become Live one at a time when checked in the live game (a settled decision), so each page's status has to show again. Beta data labels are a separate thing (where a number came from), and would stay either way.

---

## 5. The ForeverDB API

**What it means:** the key unlocks the "where and how" layer our pages lack: where to learn each recipe and what it costs (including Merchant's Favor), where to gather, what each class learns at each level, what vendors sell and what disenchanting gives. That fills the data slots on profession, class and spec pages with facts instead of more prose. It does **not** add prices, talents, Legacy, rares, camping or mounts; those stay on the addon files and our scans. And today every answer is the **last Beta build** (1.60.1.70532, level cap 30), so it all needs re-fetching once ForeverDB extracts the live client.

**How it works.** A read-only web API at `https://foreverdb.net/api/v1/`, authorised by sending the key in a header. Each answer states the game build it came from and labels anything that comes from Classic data or players' sightings rather than the Forever client. Because the key must never appear on the public site, the pattern is the one we already use: a script fetches with the key (on the Mac or in an Action, with the key as a secret), writes a slimmed JSON file into `data/`, and the build turns that file into tables.

Checked by the agent (73 calls, no rate-limit or server errors) and spot-checked by me (the `/meta` call and the `/developers` page). Full notes and 35 trimmed samples: `sources/foreverdb-api.md`, `sources/foreverdb-api/`. The key appears in no file.

### Terms

- **Credit:** "a visible link to https://foreverdb.net, wherever you show the data." Today every page's footer carries a linked "Data from ForeverDB.net", and the data tables' notes name ForeverDB without a link. A linked credit beside each table built from API data is the safe reading.
- **Allowed:** use on our own site. **Not allowed:** reselling, or presenting the data as ours. No formal licence is named; if we ever want certainty about derived tables, ForeverDB has a data contact (messaging them is Fares's call).
- **Limits:** 60 requests a minute and 10,000 a day. The bulk tables below (professions, gathering, disenchant bands, class abilities, poisons, dungeons list, battlegrounds, player-seen differences) take about 60 calls, plus ~340 for the Merchant's Favor vendor sweep. Per-item and per-quest detail is extra and grows with how many items or quests are wanted.

### What we'd gain, by page type

| Page type | From the API | Effort |
|---|---|---|
| **Professions (12)** | Where to learn each rank (trainer, zone, coordinates, seen in Forever or Classic data); recipes you buy (vendor, faction, gold or Favor cost, limited stock); skill-up colours for levelling; what Forever changed from Classic, with the old values | ~35 calls; the raw data is ~9 MB, so the script must slim it. The biggest gain |
| **Gathering (Herbalism, Mining, Skinning, Fishing)** | Best zones per skill range, node tables, beasts per zone, fishing catch rates | 4 calls, plus one per zone for skinning beasts. Spawn data is mostly Classic; only ~190 spots seen in Forever so far, so it needs a "Classic data" label |
| **Enchanting** | Disenchant results by item-level band; optionally each item's own disenchant result and vendor price | 1 call for the bands (all Classic data until launch); per-item results and vendor prices need one call per item |
| **Classes and specs (36)** | Every ability with the level each rank is learned, by tree, flagged new in Forever or rune-style | 9 calls for names and levels; tooltips cost one call per rank. Not talent trees |
| **Merchant's Favor** | The spending side: what Favor buys, from which vendor, at what cost | No "by currency" filter, so ~340 calls to walk the vendors seen in Forever (one day's quota fits) |
| **Dungeons and raids** | 47 instances with level ranges and new-in-Forever flags; boss lists | 1–47 calls. Onyxia's Lair is listed; Barrow Deeps and Hyjal Summit (also 9 December) aren't yet; loot came back empty |
| **Rogue** | Every poison, its reagents, trainers and suppliers | 1 call |
| **Class quests and levelling** | 6,614 quests with givers, turn-ins, locations and chains (class pages already have "Class quests" sections in prose) | ~67 paged calls for the list; locations and chains need one call per quest |
| **PvP** | 7 battlegrounds and arenas with level brackets, team sizes, objectives and where the rules come from. Context for the per-class and per-spec PvP sections; no general PvP page is planned | 1 call |
| **Known issues** | 400 player-seen differences from the game files (189 verified vendor price changes) | Paged, ~4 calls |
| **Not in the API** | Auction House prices, talents, Legacy, rares, camping, mounts, reputation | Stay on addon data, our scans and links |

### A possible order (a proposal, for the plan to confirm)

1. **Now:** a fetch script for professions, gathering, disenchanting, class abilities and poisons, with the key kept out of the repo, writing a slim `data/` file; tables on those pages marked Pre-launch like today's data. About 50 calls, plus one per zone if skinning beasts are included.
2. **Launch week:** re-run when ForeverDB's build changes and the level cap reads 60; the Beta-versus-live fields should then fill in.
3. **Later, more work:** the Merchant's Favor vendor sweep, dungeon loot once it exists, spell tooltips.

Where it runs is a choice: on the Mac, like today's ForeverDB scripts, or as a scheduled or button-run Action with the key stored as a repository secret (no Mac needed, see section 1).

---

## 6. The Auction House module: what the data can support

**What it means:** every upload can become a timestamped price observation for every item it saw, and the site can keep those for the last 30 scans or 30 days, as Fares asked. That's enough for per-item price charts across a day, alerts when something is listed far below its usual price, investment estimates, movers from the first days, and time-of-day and weekday patterns once a few weeks of scans exist. Two things the data can't support directly: **units sold**, and **quantity at each scan**. Both need saying plainly on the site, with the proxies we do have.

### What one upload contains (checked in Auctionator's source)

Auctionator's price database (`Source/Database/Mixin.lua`, read from a public mirror of the addon) stores, per item and per market:
- `m`: "Last seen minimum price", overwritten every time a scan sees the item.
- `l` and `h`: the lowest and highest *minimum* price seen on each day. `l` is only written when it differs from `h`.
- `a`: the "Highest quantity seen on a given day" (`math.max` of the day's scans), not the quantity at each scan.
- Days are counted from Auctionator's own day zero, in whole 24-hour blocks; history beyond 21 days is pruned by default (`PRICE_HISTORY_DAYS = 21`).
- Nothing about individual auctions, sellers or sales.

So a single upload is a 21-day daily summary plus one latest price per item. Several uploads in a day add one latest-price observation each, with the upload's scan time (`TimeOfLastBrowseScan` / `TimeOfLastReplicateScan`).

### Where it breaks today

- **Storage.** Each upload is kept whole (`data/captures/…market.json`): every item's full 21-day history again. The Beta sample is 440 bytes per item; a full market of ~4,200 items (the Beta's PvP market size) would be ~1.9 MB per upload, so four a day would add over 200 MB a month to the repository. A compact scan record (the latest price plus that day's low, high and quantity, for the items seen that day) measured 27 bytes per item on the 17 October Beta file: ~115 KB per upload for a full market, ~14 MB for a 120-scan window.
- **Per-scan detail is thrown away.** The build merges every upload into one record per day (`build_markets`), keeping only the newest `m`.
- **Retention.** Nothing ages out: old uploads stay forever, and the daily history beyond Auctionator's 21 days survives only inside old uploads.

### Fares's retention rule, made concrete

"The past 30 scans or 30 days, whichever is further back": keep every scan record whose time is within 30 days of the newest scan, and also the 30 most recent scans if those reach further back (a quiet month). Older scan records fold into a permanent daily archive (low, high, most listed, and the day's scan statistics), so long-run history such as raid-season comparisons survives.

### What can be computed, and how honest each is

| Feature | From | Strength |
|---|---|---|
| **Per-scan price chart** for each item, with the daily low–high band and event markers (launch, raid openings) | Scan records + daily archive | Direct observation |
| **Unusually low now** (alert) | Latest scan price against the item's own recent reference (median of its scan prices in the window), with guards for thin history, stale sightings and troll listings | Strong when guarded; a listing may be gone minutes later, so alerts carry their scan time |
| **Below vendor price** | Latest price below what a vendor pays for the item (ForeverDB API `sellPrice`) | Certain arbitrage, if still listed |
| **Investment watch** | Buy at today's price, resell near the item's usual level minus the 5% Auction House cut, weighted by how reliably it's listed and how steady it is | Estimate only; resale isn't guaranteed and sales aren't observed |
| **Movers from day one** | Latest scan against the median of the item's scans over the previous 24 hours (three or more), handing over to the weekly rule once enough days exist | Avoids the single-scan noise and the unfinished-day bias in section 2 |
| **Time-of-day and weekday patterns** | Each scan price divided by the item's own median, averaged per hour band and weekday, per item and across the market | Needs a few weeks of scans spread across times of day; shown as "collecting" until then |
| **Event effects** (raid openings, reset day) | Price index before and after dated events, by item category | Needs the event to have happened; categories from the ForeverDB API (`/items` class and subclass) |
| **How well something sells** | Not in the data. Proxies: how often the item is listed across scans, how quickly its minimum price changes between scans, and the most units listed each day | Weak proxies, labelled as such; never called sales |

Volumes sold would need auction-level scan data (individual auctions disappearing before they expire), which Auctionator doesn't record. A small companion addon could, later; it's outside this plan.

### Ingest routes

- **Mac (today):** `ingest.py --push` reads the WoW folder, imports, tests, builds, commits and pushes. Running it after each scan gives the per-scan record.
- **ChatGPT upload (what Fares described):** the original file must never be committed (it holds settings, posting history and searches). A route that fits: a single standard-library script that turns the uploaded `Auctionator.lua` into the compact market-only scan record; ChatGPT runs it in its own sandbox and commits only that record; a GitHub Action validates it, folds it in, applies retention, builds and publishes. Fares confirmed ChatGPT commits to the repo; running a repo script in ChatGPT's sandbox and committing a ~100 KB file are untested.
- **Integrity:** today each upload's fingerprint is checked against its receipt on every build. Compact records keep that (each record has a receipt); records retired by retention are recorded as folded into the archive rather than silently deleted.

### What other Auction House tools do

**What it means:** the serious tools agree on most of what we can build, and they confirm the limits: nobody computes sales or sale rates without sales records, and TradeSkillMaster itself declined to publish a realm-level sale rate "for lack of data". Our differences: one scanner, one realm and faction, uploads hours apart (so alerts read "seen cheap at 14:05", never "buy now"), and no view of the full order book. Full survey with sources: `sources/ah-tools.md`.

What we adopt, and from where:
- **Usual price from daily lows**, as the Classic addon aux does (median of daily lowest buyouts), with our scan prices on top when there are enough.
- **Deal flags with guards**: a discount threshold (tools use 30–60% of value), a robust z-score from the median absolute deviation (3.5, the published convention), minimum history, and a cap so one mispriced unit can't pose as a huge deal.
- **Confidence tiers** (goldcap.gg's High, Medium and Low, with Low hidden) and "not enough data yet" gates (The Undermine Journal needs more than 8 entries for a median and 14 for a heat map).
- **A market index** (auctionhouse.fyi's 100-based index; Saddlebag's price-group deltas) for showing what a raid opening did to prices.
- **Supply signals from the daily quantity**: Saddlebag's shortage rule (price at least 120% of usual, quantity at most 50% of usual).
- **A good-buy price**: The Undermine Journal's mean minus half a standard deviation, in a robust form.
- **Weekday × time-of-day grids** normalised per item (The Undermine Journal, Undermine Exchange), with a caveat the survey stresses: our time-of-day reading is shaped by when scans happen.

What's out: TradeSkillMaster's market value (it trims individual auctions we can't see), sale rate and sold per day, volume from vanished listings, real-time sniping, cross-realm comparison. Two peers already track Forever prices from player scans (auctionhouse.fyi and ForeverDB's Auction House); our edge is per-scan depth on one market and the analysis on top. The evidence on weekday, reset-day and raid-release price patterns is anecdotal and contradictory, which is a reason to measure it rather than repeat it.

Found while building: Auctionator's daily quantity only reflects what was scanned, so a day of a few item searches looks like a market-wide shortage. The analytics leave out partial-scan days (under half the usual item count) and the unfinished newest day from stock and index comparisons.

---

## Questions for Fares before the plan

**Structure (section 2)**

1. **Menu names.** Which direction for "Prices": *Auction House*, *Market*, *Gold*? And should Merchant's Favor and Camping stay under World or move to where their money or profession side lives?
2. **More.** Give it an overview page like the others, or split it: *Launch* (checklist, known issues, addons, macros) and news under its own name?
3. **Markets.** Once live markets appear and we know how they're split, how should they be named on the site?
4. **Homepage after launch.** Is the target "what changed" (news and known issues in launch week, then market movement as it becomes available) with the class picker kept, and the profession and world rows dropped?
5. **Early price movement.** *Answered by Fares on 27 October: track per scan from the first days (section 6).* Is a ranked movers list wanted before about day 10? If so, scan to scan (needs an import after every scan, noisy) or day to day (simpler, but can exaggerate rises early in the day and hides same-day recoveries)?
6. **Search.** Put the search box on every page (in the masthead), not just the homepage?

**Templates (section 3)**

7. **Fixed templates per type.** Adopt fixed glance fields and a fixed list of sub-headings for each page type, with the build warning on drift?
8. **Class page.** Split hybrid builds and macros into their own pages under each class, so the class page becomes a short "choose a spec" page?
9. **Reconsideration: the four-section frame.** Give More lists (checklist, addons, macros, known issues) a list frame of their own, and hide Field findings until a page has its first? Both change the 27 October "four sections per page" decision.
10. **Two link lists.** Keep "Read more" and "Guides and tools" separate (and say why), or merge them?

**Copy (section 4)**

11. **Strapline.** Drop "Horde-side" from the title and strapline, and keep the Horde voice in the greeting and imagery? A replacement needs to keep "World of Warcraft: Forever" spelled out.
12. **Pre-launch labelling.** Until launch, replace per-page Pre-launch badges with one site-wide notice (Beta data labels unchanged), and bring per-page status back as pages are checked live?

**Data and running costs (sections 1 and 5)**

13. **ForeverDB API scope.** Which datasets and pages first? Section 5 proposes professions, gathering, disenchanting, class abilities and poisons now; the Favor sweep, dungeon loot and tooltips later.
14. **ForeverDB API fetch.** Run it from the Mac, or as a GitHub Action with the key stored as a repository secret? Adding the secret is a repository settings change, so it's yours to approve. The existing ForeverDB scripts need no key and could move either way.
15. **Actions minutes.** Could you check the account's Actions usage on github.com's billing page before more scheduled jobs are added? GitHub's docs conflict on whether Pages runs count; if they do, the allowance is shared with Brew and your other private repos.
16. **Analytics.** Stay without visitor statistics, or add counting, either through a third-party service or a small collector of our own? It's an outward-facing choice, and nothing here assumes one.

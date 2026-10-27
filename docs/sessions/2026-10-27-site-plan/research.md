# Research: hosting limits, site structure, page templates, ForeverDB API and copy

27 October 2026, eight days before launch. This feeds `plan.md` in this folder. Everything here was read from the repository, the built site (`dist/`), the live site or the cited sources; one agent explored the ForeverDB API with the key (raw notes in `sources/foreverdb-api.md`). Nothing is decided here; the questions at the end are what the plan needs from Fares.

## In short

1. **GitHub Pages only serves files.** Nothing runs when someone opens a page. All "server" work happens in GitHub Actions *before* publishing (on a push, on a timer, or on a button press), or in the visitor's browser, or on the separate news relay. That is enough for everything Tazdingo does now, including a ForeverDB refresh that no longer needs the Mac.
2. **The menu works, but its labels and links are inconsistent.** Four of the five top items open an overview page; "More" jumps to the launch checklist. "Prices" holds two different things (market price lists and gold-making). World mixes game systems with places. The lower half of the homepage repeats the menu.
3. **The four-section page template fits specs and professions, and is forced onto everything else.** The launch checklist's steps sit under "What the guides say"; the class page stacks three pages into one (3,700 words, three "At a glance", three empty "Field findings"). Within one page type the sub-headings drift (six wordings of "where the guides disagree").
4. **Field findings are empty on all 77 pages.** The site's own voice is so far only the "Tazdingo recommendation", which reads as a list of cautions (88 "does not / is not / do not" constructions in 77 short sections).
5. **ForeverDB's API gives us the "where and how" our pages lack:** where to learn and buy every recipe (with Merchant's Favor costs), where to gather, what each class learns at each level, disenchanting, vendor stock. Not prices, talents, Legacy, rares or camping. Everything is still the last Beta build, so it needs a re-fetch at launch.
6. **Copy:** "Horde-side" appears three times above the fold, market names are raw realm strings ("ClassicBetaPvP"), and several labels describe the mechanism instead of the benefit.

---

## 1. What GitHub Pages can and can't do

**What it means for us:** the site can update itself on a schedule or on a trigger, fetch data with secret keys, and be as interactive as JavaScript in the browser allows. It cannot react to a visitor on the server: no logins, no saved forms, no live per-request data, no secrets in pages. For those, we'd need a separate small service, as we already have for news.

**How it works.** Pages is a file host with a CDN in front. A *build* is a GitHub Actions job (`.github/workflows/pages.yml`) that runs our Python scripts on a fresh Linux machine, produces `dist/`, checks it and hands the folder to Pages. After that, visitors only ever download files. So "server-side scripts" means scripts that run at build time, not at view time.

### The three places code can run

| Where | When it runs | What it can do | What it can't do |
|---|---|---|---|
| **GitHub Actions** (build time) | On a push to `main`; on a timer; on a manual button (GitHub web or phone app); on an external call (`repository_dispatch`, needs a token); after another workflow | Run any script, call APIs with secret keys stored as repository secrets, commit back to the repo, build and publish | React to a visitor; run exactly on time (see timers below) |
| **The visitor's browser** | Every page view | Search, filters, countdown, theme, fetching public APIs that allow it (the Refresh news button) | Hold secrets (anything in a page is public); write anywhere permanent |
| **The news relay** (a small Worker on chatgpt.site, separate from GitHub) | Every request to `/news` | Read Blizzard's posts live, cache them five minutes | By decision, it never holds GitHub credentials and never publishes |

Fares's Mac is a fourth, manual place: scan files exist only there, so `ingest.py` must run there.

### Triggers and timing, as observed

- **Push to `main`:** publish takes about 35 seconds of build plus deploy; recent runs were 31–70 seconds. Then the CDN may serve the previous version for up to **10 minutes** (`cache-control: max-age=600`, checked on the live site). So "live within a minute" is true for a fresh visitor and up to ten minutes for a returning one.
- **Timer (`schedule`):** best-effort. GitHub's docs say scheduled runs can be delayed at busy times and dropped under heavy load. Observed: the two-hourly job has run only twice since it was added (01:32 and 08:03 UTC on 27 October), with a five-hour gap since. Good for "roughly every few hours"; wrong for anything that must happen at a given minute. That's why the countdown now runs in the browser.
- **Manual button (`workflow_dispatch`):** reliable and immediate, from github.com or the GitHub phone app.
- **External trigger (`repository_dispatch`):** any service holding a token can ask for a run. This is how a future ChatGPT connector (parked) or the relay could request a rebuild.
- **A gotcha:** a commit made by a workflow with its default token does not start other workflows. The archive Action relies on this to avoid loops. A future "fetch ForeverDB data and commit it" job must therefore build and publish in the same run, or explicitly start the publish workflow.

### Limits

- Published site: 1 GB maximum (we're at 6.6 MB). Bandwidth: 100 GB a month, soft. Deploys time out after 10 minutes. The "10 builds an hour" limit doesn't apply to Actions-built sites like ours. ([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits))
- The repository is private and the site public; Pages from a private repository requires a paid plan, which the account has.
- **Actions minutes are metered for private repositories.** Each publish run is two short jobs, billed at a rounded-up minute each, so about 2–3 minutes. Twelve scheduled runs a day plus pushes would come to roughly 1,000–1,500 minutes a month, against a plan allowance of 2,000–3,000. I couldn't read actual usage: the `gh` login lacks the `user` scope. Worth checking before adding more scheduled jobs.

### What this means per kind of update

| Update | Today | Could be |
|---|---|---|
| Prices | Mac: scan → `ingest.py --push` | Same; the scan file only exists on the Mac |
| Guide pages | ChatGPT commits → publish; archive backs up | Same; a no-GitHub route is parked |
| ForeverDB data | Mac, by hand (`foreverdb_data.py`, `item_names.py`) | A scheduled or button-run Action with the API key as a secret: no Mac needed |
| Blizzard posts | Scheduled Action, and the relay for visitors | Same |
| Countdown | Browser (since today) | Same |
| Rebuild on demand | Push something | Add a "Publish now" button (`workflow_dispatch` is already enabled on `pages.yml`) |

---

## 2. Site structure: the menu, section pages and the homepage

**What it means:** a visitor can't tell which top item leads to an overview and which jumps to a page; two section names don't describe their contents; and the homepage spends half its length repeating the menu.

### The menu today

| Top item | Label goes to | Panel contains | Overview page? |
|---|---|---|---|
| Prices | `prices/` | "Making gold" (What to craft, Waylaid Crates, Materials worth gathering) + "Markets" (each realm) + All prices | Yes: making-gold links, a markets table, a steadiness summary |
| Classes | `classes/` | 9 classes × 3 specs | Yes: class cards with portraits, summaries, specs |
| Professions | `professions/` | Gathering / Crafting / Secondary | Yes: cards with recipe counts |
| World | `world/` | 7 topics with one-line summaries | Yes: the same 7 with icons and summaries |
| More | `more/launch/` | Launch checklist, Blizzard posts, Addons, Macros, Known issues, Sources and credits | **No.** The label opens the launch checklist |

How a visitor finds out whether a label has an overview: they can't, except by clicking. Each top item is a link (the label) plus a separate button (the arrow) that opens the panel. On a desktop, hovering opens the panel, so clicking the label feels like "go to the section". Four labels do that; More doesn't.

### What's weak about the names

- **Prices** covers two jobs: *what does X cost* (market pages, the item browser) and *how do I make gold* (craft margins, crates, materials). Until launch, every number in it is Beta data. Names that cover both: *Auction House*, *Market*, *Gold*, *Economy*. "Auction House" is the in-game term players search for; "Gold" names the goal, not the data.
- **Market names** are raw realm strings: "PvP" and "ClassicBetaPvP", each tagged "Forever Beta". At launch these become real realm or ruleset names, so this needs a display-name rule rather than a one-off fix.
- **World** holds two kinds of thing: *systems* (Camping, Legacy, Merchant's Favor) and *places and content* (New zones, Dungeons and raids, Rare spawns, Collections). Camping is as much a profession topic, and Merchant's Favor is as much gold-making (its crates already have a page under Prices).
- **More** mixes three things: *getting set up* (Launch checklist, Addons, Macros, Known issues), *news* (Blizzard posts) and *about the site* (Sources and credits). After launch the checklist matters less and known issues more.

### Overlaps (the same subject in two places)

- Waylaid Crates: `prices/crates/` and `world/merchants-favor/`.
- Camp items: `world/camping/` (full table) and each profession page (its own rows).
- Macros: `more/macros/` (how macros work) and each class page (`#macros`).
- Launch checklist: `more/launch/` and the new hero tag.
- The class picker: the Classes menu, `classes/` and the homepage.

Overlaps aren't wrong (a crate is both a gold topic and a Favor topic), but each subject needs one home, with the other places linking to it.

### The homepage today, top to bottom

1. Greeting ("Loktar Ogar · A Horde-side field guide"), countdown + Pre-launch checklist tag, title, one-line description, search, Darkspear scene.
2. **Market pulse** (Beta): a steadiness bar (7% steady, 33% moving, 58% volatile), the five most-listed items (four of them ammunition and cloth worth copper), three listing margins.
3. **Blizzard says:** five posts, with Refresh.
4. **Choose your class:** the same 9 × 3 as the menu.
5. **Professions:** the same 12 as the menu.
6. **The world:** the same 7 as the menu.

What other Forever sites lead with (from the 26 October research): a launch countdown, calculators and class changes, a class/spec picker, and item price search. We have the countdown, the picker and search; calculators are linked out, not ours.

Observations:
- Rows 4–6 repeat the menu. The class picker is the most-used entry point on comparable sites, so it earns a place; the profession and world rows less so.
- Row 2 shows Beta data front and centre. Its most-listed items are the least interesting (copper ammunition), because "most listed" measures volume, not interest.
- Nothing on the homepage is ours yet except prices: there are no findings to show.
- The homepage has three lives. **Before launch:** countdown, checklist, news, choosing a class. **Launch week:** server status, known issues, the first live prices. **After:** what moved in the market, new findings, news. A layout that serves all three by swapping one or two blocks would avoid a redesign at launch.
- Settled (not to reopen): no repository changelog on the homepage; the homepage is a dashboard.

---

## 3. Inner page templates

**What it means:** pages of the same type should answer the same questions in the same order, so a reader who has used one spec page can use any spec page, and ChatGPT can update them predictably. Today the outer frame is consistent; the inside isn't, and some page types don't fit the frame at all.

**How it works.** Every content file has the same four `##` sections (At a glance · What the guides say · Field findings · Read more). The build places them and adds data blocks and a sidebar (Guides and tools, On this page). The `###` headings inside "What the guides say" are free text, written per page by the research agents.

### By page type

| Type | Pages | Words (median) | Consistent? | What's off |
|---|---|---|---|---|
| **Spec** | 27 | 1,300 (page ~1,600 with sidebar) | At a glance: yes (Role, How it plays, Strengths, Weaknesses, New in Forever; "Stats" vs "Stats that matter"). Sub-headings: partly | Six wordings of "where the guides disagree"; "Talents" vs "Talents by level"; "Rotation" vs "Rotation and priorities". No data block: talents and abilities are linked out |
| **Class hub** | 9 | ~3,700 rendered | No | One page built from four files (overview + spec cards + hybrid + macros). Three "At a glance", three "Field findings", three "Read more". Overview glance labels vary (Races / Roles / Resource / Hybrid status…) |
| **Profession** | 12 | 1,040 (page ~1,400) | Yes, the most consistent: Suits, Pairs with, New in Forever, Camp feature; then What changed, Levelling in brief, Open questions | "From the data" sits between the guides and findings; it shows margins and camp items but not trainers, recipe sources or skill-ups |
| **World topic** | 7 | 1,230 | No, and partly by nature (camping ≠ rares) | Glance bullets are free-form; data blocks exist for 4 of 7 topics, and two are a single sentence ("354 rare creatures are known…") |
| **More list** | 4 | 1,540 | No | The guide frame doesn't fit: the launch checklist's 15 steps sit under "What the guides say"; addons, macros and known issues are lists, not guide summaries |
| **Prices** | index, 2 markets, 3 tables | n/a | Own templates | Fine structurally; naming and Beta labelling are the issues |
| **Section overviews** | 4 (no More) | 400–450 | Similar | Classes has a "Specs and hybrids" essay; Professions has counts; World has icons |

### Things every type shares that aren't pulling their weight

- **Field findings, "Nothing recorded yet."** 77 times. Until the first finding arrives, an empty section on every page signals an unfinished site.
- **"Changes to this page"** at the foot of each page (from git history), and "Read more" lists that partly repeat the sidebar's "Guides and tools".
- **Length** is acknowledged as the next phase (writing and automatic updates of inner pages), so the template should be set first and trimming follow it.

### What a type template would fix

A template here means: fixed glance fields, a fixed set of `###` sections in a fixed order (optional ones allowed but named from a list), and a fixed place for data blocks. The build could warn when a page drifts. That makes pages comparable, makes ChatGPT's updates predictable (UPDATING.md would list the headings), and lets the next phase's trimming follow a known shape.

---

## 4. Copy

**What it means:** a few phrases set the site's voice, and some say the wrong thing or say it three times. Most fixes are single strings in `scripts/pages.py`, `scripts/sections.py` and `data/game.json`; the guide prose is the next phase.

### Above the fold and site-wide

| Where | Now | Issue |
|---|---|---|
| Page title (every page) | "Tazdingo: A Horde-side field guide to World of Warcraft: Forever" | Two colons; "Horde-side" is a positioning claim the content doesn't carry (pages are faction-neutral; only our scans are Horde) |
| Masthead strapline | "A Horde-side field guide to World of Warcraft: Forever" | Same; it is the site's subtitle on every page |
| Hero greeting | "Loktar Ogar · A Horde-side field guide" | Third "Horde-side" within one screen |
| Hero description | "Auction House prices, Horde-side class and profession guides, and discoveries from our travels in World of Warcraft: Forever." | "Horde-side guides" isn't accurate; "discoveries from our travels" promises findings that don't exist yet |
| Settled context | The decision says the sub-header should spell out the game name for legal clarity, and the Horde identity should come "through races, landmarks and perspective rather than red faction colour" | So the strapline must keep "World of Warcraft: Forever"; the Horde note can live in imagery and the greeting |
| Footer | "Built 2026-10-27 14:18 UTC, revision f398c5a284dd." | Internal detail on every page |

### Labels that describe the mechanism, not the benefit

- "Market pulse" with "7% steady · 33% moving · 58% volatile": meaningful only after reading the price page.
- "Listing margins" (renamed on purpose to avoid implying profit; keep the precision, but it needs a plain lead such as "Crafts worth a look").
- "Recipes ranked by estimated listing margin: output asking value minus reagent cost" (Prices overview, What to craft).
- "From the data" (profession and world pages).
- "Blizzard says" on the homepage and "Blizzard posts" in the menu, for the same thing.
- "Rare spawns" in the menu; "New zones" in the menu for a page that also covers changed zones.
- "All classes, and choosing one", "Show Prices menu" (screen-reader only; fine).

### The guide prose (next phase, noted for context)

- The 77 "Tazdingo recommendation" sections average 95 words and lead with the right idea in bold, then spend most of their length on what the evidence doesn't prove ("A Forever-tagged download is evidence of intended support, not a successful test on this character"). Accurate, but they read as a reviewer's caveats rather than a guide's advice. A shorter "do this, unless…" shape with one caveat would carry the same care.
- "Pre-launch" badges appear on nearly everything, correctly, which makes them noise; a single site-wide pre-launch notice plus badges only where data is Beta would say the same once.

---

## 5. The ForeverDB API

**What it means:** the key unlocks the "where and how" layer our pages lack: where to learn each recipe and what it costs (including Merchant's Favor), where to gather, what each class learns at each level, what vendors sell and what disenchanting gives. That fills the empty data slots on profession, class and spec pages with facts instead of more prose. It does **not** add prices, talents, Legacy, rares, camping or mounts; those stay on the addon files and our scans. And today every answer is the **last Beta build** (1.60.1.70532, level cap 30), so it all needs re-fetching once ForeverDB extracts the live client.

**How it works.** A read-only web API at `https://foreverdb.net/api/v1/`, authorised by sending the key in a header. Each answer states the game build it came from and labels anything that comes from Classic data or players' sightings rather than the Forever client. Because the key must never appear on the public site, the pattern is the one we already use: a script fetches with the key (on the Mac or in an Action, with the key as a secret), writes a slimmed JSON file into `data/`, and the build turns that file into tables.

Checked by the agent and spot-checked by me (the `/meta` call and the `/developers` page). Full notes and 35 trimmed samples: `sources/foreverdb-api.md`, `sources/foreverdb-api/`.

### Terms

- **Credit:** "a visible link to https://foreverdb.net, wherever you show the data". Our footer credit exists, but each table built from API data needs its own linked credit line.
- **Allowed:** use on our own site. **Not allowed:** reselling, or presenting the data as ours. No formal licence is named; if we ever want certainty about derived tables, ForeverDB has a data contact (messaging them is Fares's call).
- **Limits:** 60 requests a minute and 10,000 a day. A full refresh of everything below needs a few hundred calls, so a daily or on-launch refresh fits easily.

### What we'd gain, by page type

| Page type | From the API | Effort |
|---|---|---|
| **Professions (12)** | Where to learn each rank (trainer, zone, coordinates, seen in Forever or Classic data); recipes you buy (vendor, faction, gold or Favor cost, limited stock); skill-up colours for levelling; what Forever changed from Classic, with the old values | ~35 calls; the raw data is ~9 MB, so the script must slim it. The biggest gain |
| **Gathering (Herbalism, Mining, Skinning, Fishing)** | Best zones per skill range, node tables, beasts per zone, fishing catch rates | 4 calls. Spawn data is mostly Classic; only ~190 spots seen in Forever so far, so it needs a "Classic data" label |
| **Enchanting** | Disenchant results by item-level band; each item's disenchant result and vendor price | 1 call. All Classic data until launch |
| **Classes and specs (36)** | Every ability with the level each rank is learned, by tree, flagged new in Forever or rune-style | 9 calls for names and levels; tooltips cost one call per rank. Not talent trees |
| **Merchant's Favor** | The spending side: what Favor buys, from which vendor, at what cost | No "by currency" filter, so ~340 calls to walk the vendors seen in Forever (one day's quota fits) |
| **Dungeons and raids** | 47 instances with level ranges and new-in-Forever flags; boss lists | 1–47 calls. Missing the 9 December raids; loot came back empty |
| **Rogue** | Every poison, its reagents, trainers and suppliers | 1 call |
| **Known issues** | 400 player-seen differences from the game files (189 verified vendor price changes) | Paged, ~4 calls |
| **Not in the API** | Auction House prices, talents, Legacy, rares, camping, mounts, reputation | Stay on addon data, our scans and links |

### The order that makes sense

1. **Now:** a fetch script for professions, gathering, disenchanting, class abilities and poisons, with the key kept out of the repo, writing a slim `data/` file; tables on those pages marked Pre-launch like today's data. About 50 calls.
2. **Launch week:** re-run when ForeverDB's build changes and the level cap reads 60; the Beta-versus-live fields should then fill in.
3. **Later, more work:** the Merchant's Favor vendor sweep, dungeon loot once it exists, spell tooltips.

Where it runs is a choice: on the Mac, like today's ForeverDB scripts, or as a scheduled or button-run Action with the key stored as a repository secret (no Mac needed, see section 1).

---

## Questions for Fares before the plan

1. **Menu names.** Which direction for "Prices": *Auction House*, *Market*, *Gold*? And should Merchant's Favor and Camping stay under World or move to where their money/profession side lives?
2. **More.** Give it an overview page like the others, or split it: *Launch* (checklist, known issues, addons, macros) and news under its own name?
3. **Homepage after launch.** Is the target "what changed today" (market movers, news, known issues) with the class picker kept, and the profession/world rows dropped?
4. **Class hub.** Split hybrid builds and macros into their own pages under each class, so the hub becomes a short "choose a spec" page?
5. **Strapline.** Drop "Horde-side" from the title and strapline, keep the Horde voice in the greeting and imagery? A replacement needs to keep "World of Warcraft: Forever" spelled out.
6. **Empty Field findings.** Hide the section until a page has its first finding?
7. **ForeverDB fetch.** Run it from the Mac like today, or as a GitHub Action with the key stored as a repository secret (adding the secret is a repository settings change, so it's yours to approve)?

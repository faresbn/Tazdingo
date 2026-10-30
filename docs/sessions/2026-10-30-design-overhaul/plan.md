# Design overhaul: plan

Fares asked on 30 October for the per-page content and the menus to be rethought, and for the site's cosmetics to look intentional. He's away, and asked for the work to be done and reviewed with Codex until it's right. Branch: `design-overhaul`.

## What's wrong now (audit, 30 October)

- **Pages are one long scroll.** The Warrior page is about 17,600 px tall: the overview, the specs, hybrid builds, macros, 60+ ability rows, findings and sources are stacked. The specs, which are what most visitors want, sit below the whole overview.
- **"At a glance" restates basics.** Armour types, the resource, and which races can play a class are things anyone choosing a spec page already knows. Nothing in the first screen gives a build, a priority or a stat order.
- **Summaries describe the page, not the game.** Cards say "What Herbalism gathers in Forever, how guides level it and where they say the money is". That repeats on every card and tells a player nothing.
- **Professions overview hides the gold-making pages.** What to craft, Materials and Camping are one line of small links at the bottom.
- **The menus.** The Auction House panel opens at the right edge rather than under its word, and four of its links go to the same page. Classes uses large icons and padding. More gives a summary for every entry and carries "Sources and credits".
- **The Auction House lists are too strict and too stacked.** In the current data 89 items were recorded at least 30% under their usual price with enough history, but the extra spread test leaves 2 on "Unusually low". "Below vendor price" shows feathers worth 3 copper. Eight blocks stack on one page, then repeat on the market page.
- **The stylesheet grew in patches.** About a third of `style.css` is override layers added after the first design, which is why spacing, rules and card styles differ from page to page.

## What changes

### 1. One page template with tabs (classes, specs, professions, world)

**For the visitor:** the first screen of every guide page is the useful part: a cheatsheet and our recommendation. The rest is one click away in tabs, not 15,000 px down.

**How it works:** the build still writes every section into the page, in order, with its anchors. `app.js` turns the sections into tabs (`role="tablist"`), opening the tab that holds the address's `#anchor`, so old links (`classes/druid/#hybrid`, search results) still land in the right place. Without JavaScript the page reads top to bottom as now. The right-hand aside goes: its links move into a Sources tab, and the "On this page" list becomes a row of jump links at the top of the In depth tab. Sibling specs move into the page head as a switcher.

| Page | Tabs |
|---|---|
| Spec | Cheatsheet (cheatsheet + Tazdingo recommendation) · In depth · Field findings · Sources |
| Class | Overview (cheatsheet, spec cards, recommendation) · In depth · Hybrid builds · Macros · Abilities · Field findings · Sources |
| Profession | Cheatsheet (cheatsheet, recommendation, best margins) · In depth · Recipes and trainers · Zones or Disenchanting (where they exist) · Field findings · Sources |
| World | Overview · In depth · Game data (where it exists) · Field findings · Sources |

More pages (addons, macros, known issues, launch) keep a single column without tabs: they're lists, not guides.

### 2. "At a glance" becomes "Cheatsheet" (reconsideration of a settled decision, asked for by Fares)

**For the visitor:** the cheatsheet assumes the basics are known and gives what a returning player looks up: the build, the priority, the stats, the levels where things change, and the traps.

**How it works:** the section is renamed `## Cheatsheet` (the build also accepts the old `## At a glance`, so a submission written to the old instructions still passes). The Markdown stays a list of `- **Label:** value` lines, rendered as a compact grid. Standard labels, so the site can lift lines elsewhere:

- **Spec:** Pick it for · Levelling build · Build at 60 · Priority · Stats · Key levels · Gear and consumables · Watch out
- **Class overview:** Pick a spec · Key levels · New in Forever · Professions · Race · Watch out
- **Profession:** Pick it for · Pairs with · Levelling route · Money makers · Camp items · Trainers and ranks · Watch out

"Pick it for" replaces the meta summaries on cards (classes index, class page spec cards, professions index). The content is rewritten from each page's own cited material: no new claims, the same links, in our own words. 48 pages (36 class and spec pages, 12 professions); world, hybrid and macros pages only get the heading renamed. `docs/chatgpt/UPDATING.md`, the tests and DECISIONS.md change with it.

### 3. Menus

- Panels open under their own menu word, kept inside the window.
- **Auction House:** Overview (the board) · All prices · What to craft · Materials worth gathering · Waylaid Crates. One link per page.
- **Classes:** a compact 3 × 3 grid: class name, then its specs with small icons.
- **Professions:** the three groups, plus the gold-making links at the foot.
- **World:** names only, two columns.
- **More:** names only. "Sources and credits" leaves the menu and the More overview for the footer.

### 4. The Auction House

- **The overview (`prices/`)** becomes the board for the main market: a strip of figures (newest scan, items tracked, items under usual, market index), then tabs: Deals · Investments · Short supply · Movers · Always listed · Patterns. Gold-making tools appear as three prominent cards. The markets table and the "what these measures can tell you" text move into a closing details box.
- **Market pages (`prices/<market>/`)** become the searchable price list only, with view chips (All · Under usual · Investments · Rising · Falling) that filter the list already loaded in the browser. The duplicated board goes.
- **Deals** replaces "Unusually low": every item recorded at least 20% under its usual price, with enough history, ranked by the saving. Items that also pass the spread test are marked **Exceptional**. The first 25 show; the rest open with one click (all rows are in the HTML).
- **Below vendor price** is no longer a list: it shows only for Rare or better items and recipes worth at least 1 silver profit, as a tag on the deal row and on the item page.
- The homepage card follows: Deals, Investments, Movers.

### 5. Index pages

- **Professions:** the gold-making pages lead as large cards (What to craft, Materials worth gathering, Camping, Waylaid Crates); the twelve professions follow as a compact grid with their "Pick it for" line and recipe counts.
- **Classes:** a compact grid: class, specs with roles, and each spec's "Pick it for".
- **World, More:** compact lists.

### 6. Cosmetics and the footer

- `style.css` rewritten as one system: a spacing and type scale, one card style, one section-label style, one tab and chip style; the override layers folded in. The settled look stays: canvas, paper sheet, spruce ink, Literata and Source Sans 3, money colours only for money, class colours only for classes, light and dark.
- The masthead strapline stops wrapping to three lines.
- The footer holds the notice, the credits and "Sources and credits".

## What doesn't change

Addresses, the feed for ChatGPT (except the section name), the data rules, the Auction House measures other than Deals and vendor, the impersonal site, the inbox.

## Order of work

1. Cheatsheet rename in the build, tests and UPDATING.md; content rewrites delegated by class and profession group, checked by me.
2. Tabs, page head switcher, new class/spec/profession/world templates.
3. Menus and footer.
4. Auction House board, market list, Deals and vendor rule.
5. Index pages, homepage card.
6. Stylesheet rewrite; phone and dark checks.
7. Checks, Codex end review, HANDOVER, DECISIONS, merge.

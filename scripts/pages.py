"""HTML and text templates for the site. Every value from data goes through esc()."""
from __future__ import annotations

import html
from dataclasses import dataclass
from datetime import date

SITE_NAME = "WoW Forever Journal"
SHORT_NAME = "Forever Journal"
LAUNCH = "4 November 2026"
FOREVERDB = "https://foreverdb.net"
SERVER_ROWS = 1000  # rows rendered into the HTML for readers without JavaScript


@dataclass
class Site:
    base: str
    url: str
    revision: str
    built: str
    credit: bool
    assets: dict  # file name -> short content fingerprint, so browsers never mix old and new files

    def asset(self, name: str) -> str:
        return f"{self.base}assets/{name}?v={self.assets.get(name, self.revision)}"


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def nice_date(iso: str | None) -> str:
    if not iso:
        return "never"
    d = date.fromisoformat(iso)
    return f"{d.day} {d:%b %Y}"


def when(iso: str | None) -> str:
    return f'<time datetime="{esc(iso)}">{nice_date(iso)}</time>' if iso else "not seen"


def money(copper: int | None) -> str:
    """Coins in their own colours; the text still reads "12g 34s 56c"."""
    if copper is None:
        return ""
    gold, rest = divmod(copper, 10000)
    silver, copper = divmod(rest, 100)
    parts = []
    if gold:
        parts.append(f'<span class="g">{gold:,}g</span>')
    if gold or silver:
        parts.append(f'<span class="s">{silver}s</span>')
    parts.append(f'<span class="c">{copper}c</span>')
    return '<span class="money">' + " ".join(parts) + "</span>"


def signed(pct: int | None) -> str:
    """+12%, -40%, or a multiple for big rises: +7,417% reads better as ×75."""
    if pct is None:
        return ""
    return f"×{round((pct + 100) / 100)}" if pct >= 200 else f"{pct:+d}%"


def plain_money(copper: int | None) -> str:
    if copper is None:
        return "unknown"
    gold, rest = divmod(copper, 10000)
    silver, copper = divmod(rest, 100)
    return " ".join(p for p in (f"{gold:,}g" if gold else "", f"{silver}s" if gold or silver else "", f"{copper}c") if p)


def count(n: int | None) -> str:
    return "" if n is None else f"{n:,}"


def change(pct: int | None) -> str:
    if pct is None:
        return ""
    word = "up" if pct > 0 else "down" if pct < 0 else "flat"
    return f'<span class="change {word}">{signed(pct)}</span>'


def spark(values: list) -> str:
    """A small line of the daily lowest price; gaps where the item wasn't seen."""
    points = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(points) < 2:
        return '<span class="spark-none">one day</span>' if points else ""
    ceiling = 4 * sorted(v for _, v in points)[len(points) // 2]  # clip troll listings so the shape stays readable
    points = [(i, min(v, ceiling)) for i, v in points]
    low, high = min(v for _, v in points), max(v for _, v in points)
    span, width, height = (high - low) or 1, 84, 22
    coords = [(round(i * width / (len(values) - 1), 1), round(height - 2 - (v - low) / span * (height - 4), 1)) for i, v in points]
    path = " ".join(("M" if n == 0 else "L") + f"{x},{y}" for n, (x, y) in enumerate(coords))
    x, y = coords[-1]
    return (f'<svg class="spark" viewBox="0 0 {width} {height}" width="{width}" height="{height}" aria-hidden="true">'
            f'<path d="{path}"/><circle cx="{x}" cy="{y}" r="2"/></svg>')


def item_link(item: dict) -> str:
    return (f'<a href="{FOREVERDB}/item/{item["id"]}" data-foreverdb="item:{item["id"]}" target="_blank" rel="noopener">'
            f'{esc(item["name"])}</a>')


# --- Layout -------------------------------------------------------------------

def layout(site: Site, title: str, body: str, active: str = "", description: str = "", path: str = "") -> str:
    def nav(label, href, key):
        current = ' aria-current="page"' if active == key else ""
        return f'<a href="{site.base}{href}"{current}>{label}</a>'
    full_title = SITE_NAME if title == SITE_NAME else f"{title} | {SITE_NAME}"
    description = description or "Auction House prices from our own WoW Forever scans, and the guides, builds and discoveries worth keeping."
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(site.url + path)}">
<link rel="alternate" type="text/plain" title="Everything in one file, for ChatGPT" href="{site.base}llms-full.txt">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{site.asset("icon.svg")}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya+Sans:ital,wght@0,400;0,500;0,700;1,400&family=IM+Fell+English:ital@0;1&display=swap">
<link rel="stylesheet" href="{site.asset("style.css")}">
<script src="{site.asset("app.js")}" defer></script>
<script src="{FOREVERDB}/embed/tooltips.js" data-icons="true" data-color-links="true" async></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <a class="wordmark" href="{site.base}">{SITE_NAME}</a>
  <nav aria-label="Main">{nav("Prices", "prices/", "prices")}{nav("Journal", "journal/", "journal")}{nav("About", "about/", "about")}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="colophon">
  <p>{SITE_NAME}: an independent fan project by Fares and Mike. World of Warcraft belongs to Blizzard Entertainment.</p>
  <p>{'Item names and tooltips: <a href="' + FOREVERDB + '">Data from ForeverDB.net</a>. ' if site.credit else ''}Prices from our own Auctionator scans.</p>
  <p>Built {esc(site.built)}, revision {esc(site.revision)}. <a href="{site.base}llms-full.txt">Everything in one file</a> for ChatGPT.</p>
</footer>
</body>
</html>
'''


def sample_note(market: dict) -> str:
    if not market["sample"]:
        return ""
    whole = f" of {market['original_count']:,}" if market.get("original_count") else ""
    return (f'<p class="note">Beta sample: {len(market["items"])}{whole} items from the Forever Beta, kept to show how '
            f'prices work. Launch prices start with the first scan after {LAUNCH}.</p>')


def price_rows(items: list[dict], limit: int) -> str:
    rows = []
    for item in items[:limit]:
        rows.append(f'<tr><th scope="row">{esc(item["name"])} <span class="id">{item["id"]}</span></th>'
                    f'<td class="num">{money(item["typical"])}</td><td class="num latest">{money(item["price"])}</td><td class="date">{when(item["last_seen"])}</td>'
                    f'<td class="num listed">{count(item["listed"])}</td>'
                    f'<td class="trend">{spark(item["spark"])} {change(item["change"])}</td></tr>')
    return "".join(rows)


# --- Pages --------------------------------------------------------------------

def home(site: Site, markets: list[dict], journal: list[dict]) -> str:
    primary = markets[0] if markets else None
    search = ""
    if primary:
        search = f'''<form class="lookup" action="{esc(primary["url"])}#prices" method="get" role="search">
  <label for="lookup">Look up a price</label>
  <div class="lookup-row"><input id="lookup" name="q" type="search" placeholder="Linen Cloth, or an item ID" autocomplete="off"><button type="submit">Search</button></div>
  <p>Searches {esc(primary["name"])} ({esc(primary["environment_label"])}), last scanned {nice_date(primary["last_date"])}.</p>
</form>'''
    latest = ""
    if primary:
        top = primary["highlights"]["most_listed"][:6] or primary["current"][:6]
        rows = "".join(f'<tr><th scope="row">{item_link(i)}</th><td class="num">{money(i["typical"])}</td>'
                       f'<td class="num">{count(i["listed"])}</td></tr>' for i in top)
        latest = f'''<section class="panel scan" aria-labelledby="scan-title">
  <h2 id="scan-title">Latest scan</h2>
  <p class="lede"><a href="{esc(primary["url"])}">{esc(primary["name"])}</a>, {esc(primary["environment_label"])}: {len(primary["items"]):,} items, newest data from {when(primary["last_date"])}.</p>
  {sample_note(primary)}
  <div class="table-wrap"><table class="compact"><caption>Most listed on {nice_date(primary["last_date"])}</caption>
  <thead><tr><th scope="col">Item</th><th scope="col" class="num">Typical price</th><th scope="col" class="num">Listed</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
  <p><a class="more" href="{esc(primary["url"])}">All {len(primary["items"]):,} prices</a></p>
</section>'''
    return layout(site, SITE_NAME, f'''<section class="hero">
  <picture class="hero-art">
    <source media="(prefers-color-scheme: dark) and (max-width: 700px)" srcset="{site.base}assets/hero-night-800.webp">
    <source media="(prefers-color-scheme: dark)" srcset="{site.base}assets/hero-night.webp">
    <source media="(max-width: 700px)" srcset="{site.base}assets/hero-day-800.webp">
    <img src="{site.base}assets/hero-day.webp" alt="" width="1536" height="1024" fetchpriority="high">
  </picture>
  <div class="hero-text">
    <h1>{SITE_NAME}</h1>
    <p class="intro">Auction House prices from our own scans, and the guides, builds and discoveries worth keeping while we explore WoW Forever.</p>
    {search}
  </div>
</section>
<div class="home-grid">
{latest}
{journal_panel(site, journal)}
<section class="panel chatgpt" aria-labelledby="chatgpt-title">
  <h2 id="chatgpt-title">Reading this from ChatGPT</h2>
  <p>Everything here is also in one plain-text file that ChatGPT can read in a single pass: <a href="{site.base}llms-full.txt">llms-full.txt</a>. Full price lists are in each market's <a href="{site.base}prices/">price files</a>.</p>
</section>
</div>''', active="home")


def journal_panel(site: Site, journal: list[dict]) -> str:
    if not journal:
        body = '''<p class="empty">No entries yet. When a build, guide or discovery is worth keeping, write it up (ChatGPT can draft it) and save it as a journal entry.</p>'''
    else:
        body = "<ul class='entries'>" + "".join(entry_item(e) for e in journal[:6]) + "</ul>"
    return f'''<section class="panel journal-panel" aria-labelledby="journal-title">
  <h2 id="journal-title">Journal</h2>
  {body}
  <p><a class="more" href="{site.base}journal/">The whole journal</a></p>
</section>'''


def entry_item(entry: dict) -> str:
    details = ", ".join(esc(v) for v in (entry.get("class"), entry["status_label"]) if v)
    summary = f'<p>{esc(entry["summary"])}</p>' if entry.get("summary") else ""
    return (f'<li class="entry" data-type="{esc(entry["type"])}"><span class="kind {esc(entry["type"])}">{esc(entry["type_label"])}</span>'
            f'<a href="{esc(entry["url"])}">{esc(entry["title"])}</a>{summary}'
            f'<p class="meta">{details + ". " if details else ""}{when(entry.get("updated") or entry["date"])}</p></li>')


def markets_index(site: Site, markets: list[dict]) -> str:
    rows = "".join(f'''<tr><th scope="row"><a href="{esc(m["url"])}">{esc(m["name"])}</a></th><td>{esc(m["environment_label"])}{" (sample)" if m["sample"] else ""}</td>
<td class="num">{len(m["items"]):,}</td><td>{when(m["last_date"])}</td><td class="num">{len(m["scans"])}</td></tr>''' for m in markets)
    return layout(site, "Prices", f'''<header class="page-head">
  <h1>Prices</h1>
  <p class="lede">One Auction House per realm and faction, each built from our Auctionator scans.</p>
</header>
<section class="page-body">
  <div class="table-wrap"><table>
  <thead><tr><th scope="col">Market</th><th scope="col">Game</th><th scope="col" class="num">Items</th><th scope="col">Newest data</th><th scope="col" class="num">Scans</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
  <p class="note">Launch prices start with the first scan after {LAUNCH}. Until then, the Beta sample shows how a market page works.</p>
</section>''', active="prices", path="prices/", description="Auction House price lists from our WoW Forever scans.")


def market_page(site: Site, market: dict) -> str:
    h = market["highlights"]
    files = market["files"]

    def mini(title, items, extra):
        if not items:
            return ""
        rows = "".join(f'<li>{item_link(i)} <span class="value">{money(i["typical"])}</span> {extra(i)}</li>' for i in items)
        return f'<section class="highlight"><h3>{title}</h3><ul>{rows}</ul></section>'
    listed = lambda i: f'<span class="aside">{i["listed"]:,} listed</span>'
    highlights = (mini(f"Most listed on {nice_date(market['last_date'])}", h["most_listed"][:8], listed)
                  + mini("Rising this week", h["rising"], lambda i: change(i["change"]))
                  + mini("Falling this week", h["falling"], lambda i: change(i["change"])))
    scans = "".join(f'<li>{when(s["date"])}: {s["items"]:,} items{" (no change since the previous scan)" if s["unchanged"] else ""}</li>'
                    for s in reversed(market["scans"]))
    shown = market["current"] if market["current"] else market["items"]
    more = (f'<p class="note">This list shows the first {SERVER_ROWS:,} of {len(shown):,}. Search, or download the full list below.</p>'
            if len(shown) > SERVER_ROWS else "")
    config = esc(f'{{"prices":"{files["prices_json"]}","history":"{files["history_json"]}"}}')
    return layout(site, f'{market["name"]} prices', f'''<header class="page-head">
  <p class="crumbs"><a href="{site.base}prices/">Prices</a></p>
  <h1>{esc(market["name"])}</h1>
  <p class="lede">{esc(market["environment_label"])} Auction House: {len(market["items"]):,} items, newest data from {when(market["last_date"])}.</p>
  {sample_note(market)}
</header>
<section class="page-body">
  {f'<div class="highlights">{highlights}</div>' if highlights else ""}
  <section id="prices" class="browser" data-config="{config}">
    <h2>All prices</h2>
    <form class="filters" role="search">
      <label class="grow">Find an item<input id="filter" name="q" type="search" placeholder="Name or item ID" autocomplete="off"></label>
      <label>Show<select id="scope"><option value="current">Seen in the last two weeks</option><option value="all">Every item ever seen</option></select></label>
      <label>Order<select id="order"><option value="name">Name</option><option value="listed">Most listed</option><option value="price-high">Highest price</option><option value="price-low">Lowest price</option><option value="change">Biggest change</option></select></label>
    </form>
    <p id="status" class="status" aria-live="polite">{len(shown):,} items.</p>
    <div class="table-wrap"><table class="prices">
    <thead><tr><th scope="col">Item</th><th scope="col" class="num">Typical price</th><th scope="col" class="num latest">Latest</th><th scope="col">Last seen</th><th scope="col" class="num listed">Listed that day</th><th scope="col">Trend</th></tr></thead>
    <tbody id="rows">{price_rows(shown, SERVER_ROWS)}</tbody></table></div>
    {more}
    <nav id="pager" class="pager" aria-label="Pages" hidden></nav>
  </section>
  <section class="reading">
    <h2>Reading these prices</h2>
    <p><strong>Typical price</strong> is the middle value of each day's cheapest listing over the item's last seven days of records, so a single odd listing doesn't move it. <strong>Latest</strong> is the cheapest listing the most recent scan saw. When the two differ a lot, someone has just listed unusually high or low.</p>
    <p><strong>Last seen</strong> is the most recent day a scan saw the item; an old date means the price may have moved since. <strong>Listed that day</strong> is the most units on sale at once that day, not how many sold. The two-week line follows each day's cheapest listing, and the percentage compares this week's typical price with the week before's.</p>
    <p>Downloads: <a href="{files["prices_tsv"]}">all prices (TSV)</a>, <a href="{files["history_tsv"]}">daily history (TSV)</a>, <a href="{files["prices_json"]}">JSON</a>.</p>
    <h3>Scans</h3>
    <ul class="scans">{scans}</ul>
  </section>
</section>''', active="prices", path=f'prices/{market["slug"]}/',
                  description=f'{market["name"]} Auction House prices in {market["environment_label"]}: {len(market["items"]):,} items with daily history.')


def journal_index(site: Site, journal: list[dict]) -> str:
    kinds = sorted({e["type"] for e in journal})
    filters = ""
    if len(kinds) > 1:
        buttons = "".join(f'<button type="button" data-filter="{k}">{esc(e)}</button>' for k, e in
                          (("all", "Everything"),) + tuple((k, next(x["type_label"] for x in journal if x["type"] == k) + "s") for k in kinds))
        filters = f'<div class="kind-filter" role="group" aria-label="Show">{buttons}</div>'
    body = (f'{filters}<ul class="entries large">{"".join(entry_item(e) for e in journal)}</ul>' if journal else
            '''<div class="empty-state">
  <h2>Nothing written yet</h2>
  <p>The journal keeps what we learn as we play: class guides, builds we've tested, and discoveries about the new world.</p>
  <p>To add an entry, ask ChatGPT to write it up in the journal format, then save it as a new file in the <code>journal</code> folder. Entries are only added when Fares asks.</p>
</div>''')
    return layout(site, "Journal", f'''<header class="page-head">
  <h1>Journal</h1>
  <p class="lede">Guides, builds and discoveries from our time in WoW Forever, each dated and marked with how well it's tested.</p>
</header>
<section class="page-body">{body}</section>''', active="journal", path="journal/",
                  description="Guides, builds and discoveries from our time in WoW Forever.")


def journal_entry(site: Site, entry: dict) -> str:
    facts = [("Type", esc(entry["type_label"]))]
    for key, label in (("class", "Class"), ("status_label", "Status"), ("author", "Written by")):
        if entry.get(key):
            facts.append((label, esc(entry[key])))
    facts.append(("Written", when(entry["date"])))
    if entry.get("updated"):
        facts.append(("Updated", when(entry["updated"])))
    if entry.get("sources"):
        facts.append(("Sources", esc(entry["sources"])))
    dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    return layout(site, entry["title"], f'''<article class="entry-page">
<header class="page-head">
  <p class="crumbs"><a href="{site.base}journal/">Journal</a></p>
  <h1>{esc(entry["title"])}</h1>
  {f'<p class="lede">{esc(entry["summary"])}</p>' if entry.get("summary") else ""}
  <dl class="facts">{dl}</dl>
</header>
<div class="prose">{entry["html"]}</div>
</article>''', active="journal", path=f'journal/{entry["slug"]}/', description=entry.get("summary", ""))


def about(site: Site, markets: list[dict], captures: list[dict], names: dict | None) -> str:
    scans = "".join(f'<li>{when(c["capture_date"])}, {esc(c["environment"])}: received {nice_date(c["received_on"])}, '
                    f'{c["source_bytes"]:,} bytes, fingerprint <code>{esc(c["source_sha256"][:16])}</code></li>' for c in reversed(captures))
    name_note = (f'Item names come from ForeverDB\'s companion addon data (client build {esc(names.get("client_build"))}, fetched {nice_date(names["fetched_on"])}). '
                 if names else "")
    return layout(site, "About", f'''<header class="page-head">
  <h1>About the journal</h1>
  <p class="lede">A shared notebook for two players exploring WoW Forever, written so that both of us, and ChatGPT, can look things up.</p>
</header>
<section class="page-body prose">
  <h2>What's here</h2>
  <p><a href="{site.base}prices/">Prices</a> come from Auctionator scans made in game. After a scan, one command on Fares's Mac picks up the addon's file, keeps only the price records and publishes them here. Settings, posting history, searches and shopping lists never leave the Mac.</p>
  <p>The <a href="{site.base}journal/">journal</a> holds guides, builds and discoveries. Each entry says what kind it is, which class it's for, how well it's tested and when it was written. Entries are added only when Fares asks.</p>
  <h2>How prices are worked out</h2>
  <p>Auctionator records the lowest buyout per item whenever a scan sees it, along with each day's lowest and highest price and the most units listed. A price here is the most recent of those, with the day it was seen. It is what someone was asking, not what anything sold for, and an item that wasn't seen for a while may cost something different now.</p>
  <p>Dates come from Auctionator's day counter, which starts at midnight on 1 January 2020 in the scanning player's time zone.</p>
  <h2>Reading from ChatGPT</h2>
  <p>ChatGPT finds pages through web search, so the site is open to search engines. For a complete read, point it at <a href="{site.base}llms-full.txt">llms-full.txt</a>, which holds every journal entry and each market's summary. Full price lists are in each market's TSV file. Both files also work as files uploaded to a ChatGPT project.</p>
  <h2>Sources and credits</h2>
  <p>{name_note}Tooltips and item links use <a href="{FOREVERDB}/embed">ForeverDB's embed</a>; they show today's item details, not how an item looked on the day of a scan. <a href="{FOREVERDB}">Data from ForeverDB.net</a>.</p>
  <p>The hero map is an original illustration. World of Warcraft and its artwork belong to Blizzard Entertainment.</p>
  <h3>Scans in the journal</h3>
  <ul class="scans">{scans}</ul>
  <p>The Forever Beta closed on 23 October 2026. Its scans stay here as a small sample: a few dozen items rather than the full catalogue.</p>
</section>''', active="about", path="about/", description="What the WoW Forever Journal holds and where its data comes from.")


# --- Plain text for ChatGPT ---------------------------------------------------

def llms_index(site: Site, markets: list[dict], journal: list[dict]) -> str:
    lines = [f"# {SITE_NAME}", "",
             "> Fares and Mike's shared notebook for World of Warcraft: Forever. Auction House prices from our own Auctionator scans, and the guides, builds and discoveries we chose to keep.",
             "", f"Read everything in one file: {site.url}llms-full.txt", "", "## Prices"]
    for m in markets:
        lines.append(f"- [{m['name']} ({m['environment_label']}{', Beta sample' if m['sample'] else ''})]({site.url}{m['url'][len(site.base):]}): "
                     f"{len(m['items']):,} items, newest data {m['last_date']}. Full list: {site.url}{m['files']['prices_tsv'][len(site.base):]}")
    lines += ["", "## Journal"]
    lines += [f"- [{e['title']}]({site.url}{e['url'][len(site.base):]}): {e['type_label']}" + (f", {e['class']}" if e.get("class") else "")
              for e in journal] or ["- No entries yet."]
    return "\n".join(lines) + "\n"


def llms_full(site: Site, markets: list[dict], journal: list[dict], names: dict | None) -> str:
    out = [f"# {SITE_NAME}", "",
           f"Fares and Mike's shared notebook for World of Warcraft: Forever (launch: {LAUNCH}). "
           "Auction House prices come from Fares's Auctionator scans; journal entries are guides, builds and discoveries saved on Fares's request.",
           f"Site: {site.url}  Built: {site.built}  Revision: {site.revision}", "",
           "## How to read prices", "",
           "- Prices are per single item, in gold (g), silver (s) and copper (c): 1g = 100s = 10,000c.",
           "- \"Typical price\" is the median of each day's cheapest listing over the item's last seven days of records. Use it for questions about what something costs: it ignores one-off spikes and troll listings.",
           "- \"Latest\" is the cheapest listing the most recent scan saw. Both are asking prices, not sale prices.",
           "- \"Last seen\" is the day of that observation. Treat prices last seen more than a few days before the newest scan as possibly stale.",
           "- \"Listed\" is the most units on sale at once that day, not units sold.",
           "- \"Change\" compares this week's typical price with the week before's.",
           "- Each market is one realm and faction. Do not mix markets.", ""]
    for m in markets:
        h = m["highlights"]
        out += [f"## Market: {m['name']} ({m['environment_label']})", "",
                f"Items: {len(m['items']):,} ({len(m['current']):,} seen in the two weeks up to {m['last_date']}). Newest data: {m['last_date']}.",
                f"Scans: {', '.join(s['date'] for s in m['scans'])}.",
                f"Full price list (TSV): {site.url}{m['files']['prices_tsv'][len(site.base):]}",
                f"Daily history (TSV): {site.url}{m['files']['history_tsv'][len(site.base):]}"]
        if m["sample"]:
            out.append(f"This is a Beta sample of {len(m['items'])} items, kept for reference. The Beta closed on 23 October 2026; it is not the live game.")
        out.append("")
        if h["most_listed"]:
            out += [f"### Most listed on {m['last_date']}", "", "| Item | ID | Typical price | Listed |", "|---|---|---|---|"]
            out += [f"| {i['name']} | {i['id']} | {plain_money(i['typical'])} | {i['listed']:,} |" for i in h["most_listed"]]
            out.append("")
        for title, key in (("Rising this week", "rising"), ("Falling this week", "falling")):
            if h[key]:
                out += [f"### {title}", ""] + [f"- {i['name']} ({i['id']}): typical {plain_money(i['typical'])}, {signed(i['change'])} on the week before" for i in h[key]] + [""]
        rows = m["current"] if len(m["current"]) <= 2500 else sorted(m["current"], key=lambda i: -(i["listed"] or 0))[:500]
        label = "All items seen in the last two weeks" if rows is m["current"] else "The 500 most-listed items of the last two weeks (the rest are in the TSV)"
        out += [f"### {label}", "", "| Item | ID | Typical price | Latest | Last seen | Listed | Change |", "|---|---|---|---|---|---|---|"]
        out += [f"| {i['name']} | {i['id']} | {plain_money(i['typical'])} | {plain_money(i['price'])} | {i['last_seen'] or ''} | {count(i['listed'])} | {signed(i['change'])} |"
                for i in rows]
        out.append("")
    out += ["## Journal", ""]
    if not journal:
        out += ["No entries yet.", ""]
    for e in journal:
        facts = [e["type_label"]] + [v for v in (e.get("class"), e["status_label"]) if v]
        out += [f"### {e['title']}", "", f"{', '.join(facts)}. Written {e['date']}" + (f", updated {e['updated']}" if e.get("updated") else "") + ".",
                f"Page: {site.url}{e['url'][len(site.base):]}"]
        if e.get("sources"):
            out.append(f"Sources: {e['sources']}")
        out += ["", e["body"], ""]
    out += ["## Sources", "",
            "- Prices: Fares's Auctionator SavedVariables, market records only.",
            ("- Item names: Data from ForeverDB.net (https://foreverdb.net), client build " + str(names.get("client_build")) + "." if names else "- Item names: unavailable."),
            ""]
    return "\n".join(out)

"""Page templates: layout, front page, prices and the plain-text files. Section pages
(classes, professions, world, more) are in sections.py. Every value from data goes through esc()."""
from __future__ import annotations

import html
from dataclasses import dataclass, field
from datetime import date

SITE_NAME = "Forever Ledger"
SHORT_NAME = "Ledger"
SUBTITLE = "An unofficial journal for World of Warcraft: Forever"
FOREVERDB = "https://foreverdb.net"
SERVER_ROWS = 1000  # price rows rendered into the HTML for readers without JavaScript
NOTICE = ("World of Warcraft, Warcraft and Blizzard Entertainment are trademarks or registered trademarks of "
          "Blizzard Entertainment, Inc. in the U.S. and/or other countries.")


@dataclass
class Site:
    base: str
    url: str
    revision: str
    built: str
    credit: bool
    assets: dict = field(default_factory=dict)  # file name -> content fingerprint
    launch: date = date(2026, 11, 4)

    def asset(self, name: str) -> str:
        return f"{self.base}assets/{name}?v={self.assets.get(name, self.revision)}"


# --- Small pieces ---------------------------------------------------------------

def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def nice_date(iso: str | None) -> str:
    if not iso:
        return "never"
    d = date.fromisoformat(iso)
    return f"{d.day} {d:%b %Y}"


def when(iso: str | None) -> str:
    return f'<time datetime="{esc(iso)}">{nice_date(iso)}</time>' if iso else "not seen"


def game_day(site: Site, iso: str) -> str:
    """Journal dating: "Day 3" after launch, "5 days before launch" before it."""
    days = (date.fromisoformat(iso) - site.launch).days
    if days >= 0:
        return f"Day {days + 1}"
    return "Launch eve" if days == -1 else f"{-days} days before launch"


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


def plain_money(copper: int | None) -> str:
    if copper is None:
        return "unknown"
    gold, rest = divmod(copper, 10000)
    silver, copper = divmod(rest, 100)
    return " ".join(p for p in (f"{gold:,}g" if gold else "", f"{silver}s" if gold or silver else "", f"{copper}c") if p)


def count(n: int | None) -> str:
    return "" if n is None else f"{n:,}"


def signed(pct: int | None) -> str:
    """+12%, -40%, or a multiple for big rises: +7,417% reads better as ×75."""
    if pct is None:
        return ""
    return f"×{round((pct + 100) / 100)}" if pct >= 200 else f"{pct:+d}%"


def change(pct: int | None) -> str:
    if pct is None:
        return ""
    word = "up" if pct > 0 else "down" if pct < 0 else "flat"
    return f'<span class="change {word}">{signed(pct)}</span>'


def badge(kind: str, label: str | None = None) -> str:
    labels = {"prelaunch": "Pre-launch", "beta": "Beta", "live": "Live", "steady": "Steady", "moving": "Moving",
              "volatile": "Volatile"}
    return f'<span class="badge {esc(kind)}">{esc(label or labels.get(kind, kind))}</span>'


def steadiness(v: str | None) -> str:
    return badge(v) if v else '<span class="badge unknown" title="Fewer than three days of prices">Too new</span>'


def spark(values: list) -> str:
    """A small line of the daily cheapest listing; gaps where the item wasn't seen."""
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


def item_link(item_id: int, name: str) -> str:
    return (f'<a href="{FOREVERDB}/item/{item_id}" data-foreverdb="item:{item_id}" target="_blank" rel="noopener">'
            f'{esc(name)}</a>')


def links(pairs: list) -> str:
    out = []
    for label, url in pairs:
        external = url.startswith("http")
        out.append(f'<li><a href="{esc(url)}"{" target=_blank rel=noopener" if external else ""}>{esc(label)}</a></li>')
    return '<ul class="elsewhere">' + "".join(out) + "</ul>"


def changelog(site: Site, entries: list, title: str = "Changes") -> str:
    if not entries:
        return ""
    rows = "".join(f'<li><span class="when">{when(e["date"])} <span class="day">{game_day(site, e["date"])}</span></span> {esc(e["subject"])}</li>'
                   for e in entries[:12])
    return f'<section class="changes"><h2>{esc(title)}</h2><ol class="log">{rows}</ol></section>'


def note_block(page: dict | None, empty: str) -> str:
    if not page:
        return f'<p class="empty">{esc(empty)}</p>'
    facts = [badge("prelaunch") if page["status"] == "pre-launch" else badge("live")]
    if page["confidence_label"]:
        facts.append(badge(page["confidence"], page["confidence_label"]))
    facts.append(f'<span class="updated">Updated {when(page["updated"])}</span>')
    sources = f'<p class="sources">Sources: {esc(page["sources"])}</p>' if page.get("sources") else ""
    return f'<div class="note-meta">{" ".join(facts)}</div><div class="prose">{page["html"]}</div>{sources}'


# --- Layout -------------------------------------------------------------------

def layout(site: Site, title: str, body: str, active: str = "", description: str = "", path: str = "") -> str:
    def nav(label, href, key):
        current = ' aria-current="page"' if active == key else ""
        return f'<a href="{site.base}{href}"{current}>{label}</a>'
    full_title = f"{SITE_NAME}: {SUBTITLE}" if title == SITE_NAME else f"{title} | {SITE_NAME}"
    description = description or "Auction House prices, class notes and discoveries from World of Warcraft: Forever, kept as the game unfolds."
    more_current = ' class="current"' if active == "more" else ""
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(site.url + path)}">
<link rel="alternate" type="text/plain" title="The whole ledger as plain text" href="{site.base}llms-full.txt">
<meta name="color-scheme" content="light dark">
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="icon" href="{site.asset("icon.svg")}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya+Sans:ital,wght@0,400;0,500;0,700;1,400&family=IM+Fell+English:ital@0;1&display=swap">
<link rel="stylesheet" href="{site.asset("style.css")}">
<script src="{site.asset("app.js")}" defer></script>
<script src="{FOREVERDB}/embed/tooltips.js" data-icons="true" data-color-links="true" async></script>
</head>
<body data-base="{site.base}" data-launch="{site.launch.isoformat()}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <a class="wordmark" href="{site.base}"><span class="name">{SITE_NAME}</span><span class="sub">{SUBTITLE}</span></a>
  <nav aria-label="Main">
    {nav("Prices", "prices/", "prices")}{nav("Classes", "classes/", "classes")}{nav("Professions", "professions/", "professions")}{nav("World", "world/", "world")}
    <details class="more-menu"><summary{more_current}>More</summary>
      <ul>
        <li><a href="{site.base}more/addons/">Addons</a></li>
        <li><a href="{site.base}more/macros/">Macros</a></li>
        <li><a href="{site.base}more/known-issues/">Known issues</a></li>
        <li><a href="{site.base}more/about/">Sources and credits</a></li>
      </ul>
    </details>
  </nav>
  <button class="theme-toggle" type="button" data-theme-toggle aria-label="Colour theme: follows your device">
    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 3.75a8.25 8.25 0 0 0 0 16.5z" fill="currentColor"/><circle cx="12" cy="12" r="8.25" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>
    <span class="theme-label">Auto</span>
  </button>
</header>
<main id="main">
{body}
</main>
<footer class="colophon">
  <p><strong>{SITE_NAME}</strong> is an unofficial fan project, not affiliated with or endorsed by Blizzard Entertainment. {NOTICE}</p>
  <p>{'Item names, recipes, tooltips and second-opinion prices: <a href="' + FOREVERDB + '">Data from ForeverDB.net</a>. ' if site.credit else ''}Our prices come from our own Auctionator scans.</p>
  <p>Built {esc(site.built)}, revision {esc(site.revision)}. <a href="{site.base}llms-full.txt">Plain-text version</a>. <a href="{site.base}more/about/">Sources and credits</a>.</p>
</footer>
</body>
</html>
'''


def page_head(title: str, lede: str = "", crumbs: tuple = (), extra: str = "") -> str:
    crumb = "".join(f'<a href="{esc(url)}">{esc(label)}</a>' for label, url in crumbs)
    return (f'<header class="page-head">{f"<p class=crumbs>{crumb}</p>" if crumb else ""}<h1>{esc(title)}</h1>'
            f'{f"<p class=lede>{lede}</p>" if lede else ""}{extra}</header>')


# --- Front page -------------------------------------------------------------------

def home(site: Site, ctx: dict) -> str:
    primary, content = ctx["primary"], ctx["content"]
    days_to_go = (site.launch - date.fromisoformat(site.built[:10])).days
    countdown = (f"Forever opens in {days_to_go} day{'s' if days_to_go != 1 else ''}" if days_to_go > 0
                 else f"Day {1 - days_to_go} of Forever")
    search_action = f'{primary["url"]}#prices' if primary else f"{site.base}prices/"
    latest = "".join(
        f'<li><span class="when">{when(e["date"])} <span class="day">{game_day(site, e["date"])}</span></span> '
        + (f'<a href="{site.base}{esc(e["urls"][0])}">{esc(e["subject"])}</a>' if e["urls"] else esc(e["subject"])) + "</li>"
        for e in ctx["log"][:8])
    recipes = ctx["fdb"].get("recipes", {})
    total = sum(len(r) for r in recipes.values())
    new = sum(r["new"] for rs in recipes.values() for r in rs)
    noted = {k.split("/")[1] for k in content if k.startswith("classes/")}
    beta = badge("beta") if primary and primary["environment"] == "forever-beta" else ""
    doors = [
        ("Prices", "prices/", f'{len(primary["items"]):,} items {beta}, with what to craft, crate costs and materials worth gathering.' if primary else "Prices start with the first scan."),
        ("Classes", "classes/", f"Nine classes and 27 specs, with notes on {len(noted)} so far and the best guides elsewhere."),
        ("Professions", "professions/", f"Twelve professions. {new:,} of {total:,} recipes are new in Forever." if total else "Twelve professions."),
        ("World", "world/", "Camping, Legacy, Merchant's Favor, rares, new zones, raids and collections."),
        ("More", "more/addons/", "Addons that work in Forever, macros, and known issues with workarounds."),
    ]
    door_list = "".join(f'<li><a href="{site.base}{href}" class="door-name">{name}</a><p>{text}</p></li>' for name, href, text in doors)
    return layout(site, SITE_NAME, f'''<section class="hero">
  <div class="hero-art" aria-hidden="true"></div>
  <div class="hero-text">
    <p class="countdown" data-countdown>{countdown}</p>
    <h1>{SITE_NAME}</h1>
    <p class="intro">Prices, class notes and discoveries from World of Warcraft: Forever, kept as the game unfolds.</p>
    <form class="lookup" action="{esc(search_action)}" method="get" role="search">
      <label for="lookup">Search the ledger</label>
      <div class="lookup-row"><input id="lookup" name="q" type="search" placeholder="Linen Cloth, Frost Mage, camping" autocomplete="off" aria-controls="lookup-results"><button type="submit">Search</button></div>
      <ul id="lookup-results" class="lookup-results" hidden></ul>
    </form>
  </div>
</section>
<div class="home-grid">
  <section class="panel doors" aria-labelledby="doors-title">
    <h2 id="doors-title">In the ledger</h2>
    <ul class="door-list">{door_list}</ul>
  </section>
  <section class="panel latest" aria-labelledby="latest-title">
    <h2 id="latest-title">Latest</h2>
    <ol class="log">{latest or "<li>Nothing recorded yet.</li>"}</ol>
  </section>
</div>''', active="home")


# --- Prices -----------------------------------------------------------------------

def sample_note(market: dict) -> str:
    if market["environment"] != "forever-beta":
        return ""
    return (f'<p class="note">{badge("beta")} From three scans of the Forever Beta (6, 10 and 17 October 2026): the items the '
            'crafting, crate and material tables need. The Beta economy was a test, so treat these prices as a rough guide '
            'until launch scans replace them.</p>')


def price_rows(items: list[dict], limit: int) -> str:
    rows = []
    for item in items[:limit]:
        rows.append(f'<tr><th scope="row">{esc(item["name"])} <span class="id">{item["id"]}</span></th>'
                    f'<td class="num">{money(item["typical"])}</td><td class="vol">{steadiness(item["volatility"])}</td>'
                    f'<td class="num latest">{money(item["price"])}</td><td class="date">{when(item["last_seen"])}</td>'
                    f'<td class="num listed">{count(item["listed"])}</td>'
                    f'<td class="trend">{spark(item["spark"])} {change(item["change"])}</td></tr>')
    return "".join(rows)


def summary_volatility(market: dict | None) -> str:
    if not market:
        return ""
    current = [i for i in market["current"] if i["volatility"]]
    if not current:
        return ""
    share = {v: sum(1 for i in current if i["volatility"] == v) for v in ("steady", "moving", "volatile")}
    parts = ", ".join(f"{share[v] * 100 // len(current)}% {v}" for v in ("steady", "moving", "volatile"))
    return (f'<p class="note">How settled is the market? Of {len(current):,} items with enough days of prices in {esc(market["name"])}: {parts}. '
            'Steady items swing by less than a quarter of their price over two weeks; volatile ones by more than three quarters.</p>')


def prices_index(site: Site, ctx: dict) -> str:
    rows = "".join(f'''<tr><th scope="row"><a href="{esc(m["url"])}">{esc(m["name"])}</a></th><td>{esc(m["environment_label"])} {badge("beta") if m["environment"] == "forever-beta" else ""}</td>
<td class="num">{len(m["items"]):,}</td><td>{when(m["last_date"])}</td><td class="num">{len(m["scans"])}</td></tr>''' for m in ctx["markets"])
    tools = f'''<ul class="door-list compact">
  <li><a href="{site.base}prices/craft/" class="door-name">What to craft</a><p>Recipes ranked by margin: what the product sells for, minus its reagents.</p></li>
  <li><a href="{site.base}prices/crates/" class="door-name">Waylaid Crates</a><p>The cheapest bundle to fill each crate for Merchant's Favor.</p></li>
  <li><a href="{site.base}prices/materials/" class="door-name">Materials worth gathering</a><p>Herbs, ores, leather and cloth that no recipe makes and no vendor sells, by value.</p></li>
</ul>'''
    return layout(site, "Prices", page_head("Prices", "Auction House prices from our own scans: what things cost, how steady that price is, and what to do with it.")
                  + f'''<section class="page-body">
  <h2>Making gold</h2>
  {tools}
  <h2>Markets</h2>
  <div class="table-wrap"><table><thead><tr><th scope="col">Market</th><th scope="col">Game</th><th scope="col" class="num">Items</th><th scope="col">Newest data</th><th scope="col" class="num">Scans</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
  {summary_volatility(ctx["primary"])}
  <p class="note">Launch prices start with the first scan after launch on {nice_date(site.launch.isoformat())}. Until then, the Beta reference prices stand in, labelled as such.</p>
</section>''', active="prices", path="prices/", description="Auction House prices from World of Warcraft: Forever scans, with steadiness and gold-making tables.")


def market_page(site: Site, market: dict, ctx: dict) -> str:
    h = market["highlights"]
    files = market["files"]

    def mini(title, items, extra):
        if not items:
            return ""
        rows = "".join(f'<li>{item_link(i["id"], i["name"])} <span class="value">{money(i["typical"])}</span> {extra(i)}</li>' for i in items)
        return f'<section class="highlight"><h3>{title}</h3><ul>{rows}</ul></section>'
    listed = lambda i: f'<span class="aside">{i["listed"]:,} listed</span>'
    highlights = (mini(f"Most listed on {nice_date(market['last_date'])}", h["most_listed"][:8], listed)
                  + mini("Rising this week", h["rising"], lambda i: change(i["change"]))
                  + mini("Falling this week", h["falling"], lambda i: change(i["change"])))
    scans = "".join(f'<li>{when(s["date"])}: {s["items"]:,} items{" (no change since the previous scan)" if s["unchanged"] else ""}</li>'
                    for s in reversed(market["scans"]))
    shown = market["current"] if market["current"] else market["items"]
    more = (f'<p class="note" id="partial-note">This list shows the first {SERVER_ROWS:,} of {len(shown):,}. Download the full list below.</p>'
            if len(shown) > SERVER_ROWS else "")
    config = esc(f'{{"prices":"{files["prices_json"]}","history":"{files["history_json"]}"}}')
    return layout(site, f'{market["name"]} prices', page_head(market["name"], f'{esc(market["environment_label"])} Auction House: {len(market["items"]):,} items, newest data from {when(market["last_date"])}.',
                                                             (("Prices", f"{site.base}prices/"),), sample_note(market)) + f'''
<section class="page-body">
  {f'<div class="highlights">{highlights}</div>' if highlights else ""}
  <section id="prices" class="browser" data-config="{config}">
    <h2>All prices</h2>
    <form class="filters" role="search">
      <label class="grow">Find an item<input id="filter" name="q" type="search" placeholder="Name or item ID" autocomplete="off"></label>
      <label>Show<select id="scope"><option value="current">Seen in the last two weeks</option><option value="all">Every item ever seen</option></select></label>
      <label>Order<select id="order"><option value="name">Name</option><option value="listed">Most listed</option><option value="price-high">Highest price</option><option value="price-low">Lowest price</option><option value="change">Biggest change</option><option value="steadiest">Steadiest first</option></select></label>
    </form>
    <p id="status" class="status" aria-live="polite">{len(shown):,} items.</p>
    <div class="table-wrap"><table class="prices">
    <thead><tr><th scope="col">Item</th><th scope="col" class="num">Typical price</th><th scope="col" class="vol">Steadiness</th><th scope="col" class="num latest">Latest</th><th scope="col">Last seen</th><th scope="col" class="num listed">Listed that day</th><th scope="col">Trend</th></tr></thead>
    <tbody id="rows">{price_rows(shown, SERVER_ROWS)}</tbody></table></div>
    {more}
    <nav id="pager" class="pager" aria-label="Pages" hidden></nav>
  </section>
  <section class="reading">
    <h2>Reading these prices</h2>
    <p><strong>Typical price</strong> is the middle value of each day's cheapest listing over the item's last seven days of records, so a single odd listing doesn't move it. <strong>Latest</strong> is the cheapest listing the most recent scan saw. <strong>Steadiness</strong> says how far the daily price swung over two weeks: early in a new game, prices swing a lot while players find their level.</p>
    <p><strong>Last seen</strong> is the most recent day a scan saw the item. <strong>Listed that day</strong> is the most units on sale at once, not how many sold. Select a row for its daily prices and a comparison with ForeverDB's players' scans.</p>
    <p>Downloads: <a href="{files["prices_tsv"]}">all prices (TSV)</a>, <a href="{files["history_tsv"]}">daily history (TSV)</a>, <a href="{files["prices_json"]}">JSON</a>.</p>
    <h3>Scans</h3>
    <ul class="scans">{scans}</ul>
  </section>
</section>''', active="prices", path=f'prices/{market["slug"]}/',
                  description=f'{market["name"]} Auction House prices in {market["environment_label"]}: {len(market["items"]):,} items with daily history.')


def data_note(ctx: dict, what: str) -> str:
    src = ctx["fdb_source"]
    label = badge("prelaunch") if ctx["data_prelaunch"] else badge("live")
    beta = f' {badge("beta")}' if ctx["primary"] and ctx["primary"]["environment"] == "forever-beta" else ""
    return (f'<p class="note">{label} {what} from ForeverDB\'s data for game build {esc(src.get("client_build"))} '
            f'(fetched {nice_date(src.get("fetched_on"))}), priced with our scans{beta} where they hold the item and ForeverDB '
            'players\' scans where they don\'t. Pre-launch data is replaced when the live game\'s data arrives.</p>')


def source_tag(source: str) -> str:
    return f'<span class="src">{esc(source)}</span>'


def slug_of(text: str) -> str:
    return text.lower().replace(" ", "-")


def craft_page(site: Site, ctx: dict) -> str:
    rows = ctx["craft"]

    def table(items):
        body = "".join(
            f'<tr><th scope="row">{item_link(r["item"], r["name"])}{" ×" + esc(r["count"]) if r["count"] > 1 else ""} {badge("new", "New in Forever") if r["new"] else ""}</th>'
            f'<td>{esc(r["profession"])}</td><td class="num">{esc(r["skill"])}</td>'
            f'<td class="num">{money(r["sells"])} {source_tag(r["value_source"])}</td><td class="num">{money(r["cost"])}</td>'
            f'<td class="num margin">{money(r["margin"])}</td></tr>' for r in items)
        return (f'<div class="table-wrap"><table><thead><tr><th scope="col">Recipe</th><th scope="col">Profession</th><th scope="col" class="num">Skill</th>'
                f'<th scope="col" class="num">Sells for</th><th scope="col" class="num">Reagents cost</th><th scope="col" class="num">Margin</th></tr></thead><tbody>{body}</tbody></table></div>')
    by_prof = {}
    for r in rows:
        by_prof.setdefault(r["profession"], []).append(r)
    groups = "".join(f'<section id="{esc(slug_of(p))}"><h2>{esc(p)}</h2>{table(rs[:10])}</section>' for p, rs in sorted(by_prof.items()))
    jump = " ".join(f'<a href="#{esc(slug_of(p))}">{esc(p)}</a>' for p in sorted(by_prof))
    return layout(site, "What to craft", page_head("What to craft", "Recipes ranked by margin: what the product sells for, minus what its reagents cost.",
                                                    (("Prices", f"{site.base}prices/"),), data_note(ctx, "Recipes")) + f'''
<section class="page-body">
  {f'<p class="jump">Jump to: {jump}</p>' if jump else ""}
  <h2>Best margins overall</h2>
  {table(rows[:25]) if rows else '<p class="empty">No recipe can be priced yet.</p>'}
  {groups}
  <section class="reading"><h2>How this is worked out</h2>
  <p>A recipe is listed only when the product and every reagent have a price. Reagents a vendor sells are costed at the vendor's price; everything else at its typical Auction House price. A product only counts when it actually trades: seen in the last two weeks on at least three days, at least five listed and not volatile, or listed widely on other realms. Margins are before the Auction House's cut and deposit. Skill is the level at which the recipe becomes available.</p>
  <p><a href="{site.base}prices/craft.tsv">Every priced recipe (TSV)</a></p></section>
</section>''', active="prices", path="prices/craft/", description="World of Warcraft: Forever recipes ranked by crafting margin.")


def crates_page(site: Site, ctx: dict) -> str:
    rows = []
    for c in ctx["crates"]:
        cheap = c["cheapest"]
        others = ", ".join(f'{b["count"]} {esc(b["name"])} ({money(b["cost"]) if b["cost"] is not None else "no price"})' for b in c["bundles"] if b is not cheap)
        rows.append(f'<tr><th scope="row">{item_link(c["item"], c["name"])}</th><td class="num">{esc(c["level"])}</td>'
                    + (f'<td>{cheap["count"]} {esc(cheap["name"])} {source_tag(cheap["source"])}</td><td class="num">{money(cheap["cost"])}</td>' if cheap
                       else '<td colspan="2">No bundle priced yet</td>')
                    + f'<td class="others">{others}</td></tr>')
    return layout(site, "Waylaid Crates", page_head("Waylaid Crates", "The cheapest way to fill each crate. A crate takes any one bundle from its list; filled crates earn Merchant's Favor.",
                                                     (("Prices", f"{site.base}prices/"),), data_note(ctx, "Crates and their bundles")) + f'''
<section class="page-body">
  <div class="table-wrap"><table><thead><tr><th scope="col">Crate</th><th scope="col" class="num">Level</th><th scope="col">Cheapest bundle</th><th scope="col" class="num">Cost</th><th scope="col">Other bundles</th></tr></thead>
  <tbody>{"".join(rows)}</tbody></table></div>
  <p class="note">How much Favor each crate earns isn't in the data yet, so this compares the cost of filling crates, not the cost per point of Favor. <a href="{site.base}world/merchants-favor/">About Merchant's Favor</a>.</p>
</section>''', active="prices", path="prices/crates/", description="The cheapest bundle to fill each Waylaid Crate in World of Warcraft: Forever.")


def materials_page(site: Site, ctx: dict) -> str:
    rows = "".join(f'<tr><th scope="row">{item_link(r["item"], r["name"])}</th><td class="num">{money(r["value"])} {source_tag(r["source"])}</td>'
                   f'<td>{steadiness(r["volatility"]) if r["source"] == "our scan" else ""}</td><td class="num">{count(r["listed"])}</td><td class="num">{esc(r["used_in"])}</td></tr>'
                   for r in ctx["materials"][:80])
    return layout(site, "Materials worth gathering", page_head("Materials worth gathering", "Herbs, ores, leather, cloth and drops that no recipe makes and no vendor sells, by what they fetch.",
                                                                (("Prices", f"{site.base}prices/"),), data_note(ctx, "Reagents")) + f'''
<section class="page-body">
  <div class="table-wrap"><table><thead><tr><th scope="col">Material</th><th scope="col" class="num">Worth</th><th scope="col">Steadiness</th><th scope="col" class="num">Listed</th><th scope="col" class="num">Used in recipes</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
</section>''', active="prices", path="prices/materials/", description="World of Warcraft: Forever crafting materials by value.")


# --- Plain text for assistants and scripts --------------------------------------

def md(text) -> str:
    """Names in the plain-text file can't break its tables, links or headings."""
    return " ".join(str(text).split()).replace("|", "\\|").replace("[", "(").replace("]", ")")


def llms_index(site: Site, ctx: dict) -> str:
    lines = [f"# {SITE_NAME}", "", f"> {SUBTITLE}: Auction House prices from our own scans, class notes, professions, world systems, addons, macros and known issues.",
             "", f"Everything in one file: {site.url}llms-full.txt", "", "## Prices"]
    for m in ctx["markets"]:
        lines.append(f"- {md(m['name'])} ({m['environment_label']}): {len(m['items']):,} items, newest data {m['last_date']}. "
                     f"Full list: {site.url}{m['files']['prices_tsv'][len(site.base):]}")
    lines += [f"- What to craft: {site.url}prices/craft/ (all rows: {site.url}prices/craft.tsv)",
              f"- Waylaid Crates: {site.url}prices/crates/", f"- Materials: {site.url}prices/materials/", "",
              "## Sections", f"- Classes: {site.url}classes/", f"- Professions: {site.url}professions/", f"- World: {site.url}world/",
              f"- Addons: {site.url}more/addons/", f"- Macros: {site.url}more/macros/", f"- Known issues: {site.url}more/known-issues/"]
    return "\n".join(lines) + "\n"


def llms_full(site: Site, ctx: dict) -> str:
    game, content = ctx["game"], ctx["content"]
    out = [f"# {SITE_NAME}", "", f"{SUBTITLE} (launch: {nice_date(site.launch.isoformat())}). Prices come from our own Auctionator scans; "
           "game data from ForeverDB; notes are ours. Not affiliated with Blizzard Entertainment.",
           f"Site: {site.url}  Built: {site.built}  Revision: {site.revision}", "",
           "## How to read this file", "",
           "- \"Pre-launch\" marks anything from before launch (4 November 2026) or not yet confirmed in the live game. \"Beta\" marks prices from Forever Beta scans. Both are tentative.",
           "- Prices are per item in gold (g), silver (s) and copper (c): 1g = 100s = 10,000c. All prices are asking prices, not sales.",
           "- \"Typical\" is the median of each day's cheapest listing over the item's last seven days. Use it for \"what does X cost\". \"Latest\" is the most recent cheapest listing.",
           "- \"Steadiness\" (steady / moving / volatile) says how far the daily price swung over two weeks. Treat volatile prices with caution.",
           "- Note confidence: idea (untested), testing, tested (confirmed in play), outdated.", ""]
    out += ["## Markets", ""] + [f"- {md(m['name'])} ({m['environment_label']}): {len(m['items']):,} items, newest data {m['last_date']}. "
                                 f"Prices (TSV): {site.url}{m['files']['prices_tsv'][len(site.base):]}" for m in ctx["markets"]] + [""]
    for m in ctx["markets"][:1]:
        h = m["highlights"]
        out += [f"## Prices: {md(m['name'])} ({m['environment_label']})", "",
                f"Items: {len(m['items']):,}. Newest data: {m['last_date']}. Full list (TSV): {site.url}{m['files']['prices_tsv'][len(site.base):]}"]
        if h["most_listed"]:
            out += ["", "| Item | ID | Typical | Steadiness | Listed |", "|---|---|---|---|---|"]
            out += [f"| {md(i['name'])} | {i['id']} | {plain_money(i['typical'])} | {i['volatility'] or 'too new'} | {i['listed']:,} |" for i in h["most_listed"]]
        out.append("")
    if ctx["craft"]:
        out += ["## What to craft (best margins)", "", "| Recipe | Profession | Skill | Sells for | Reagents | Margin |", "|---|---|---|---|---|---|"]
        out += [f"| {md(r['name'])} | {r['profession']} | {r['skill']} | {plain_money(r['sells'])} | {plain_money(r['cost'])} | {plain_money(r['margin'])} |" for r in ctx["craft"][:20]]
        out += ["", f"All priced recipes: {site.url}prices/craft.tsv", ""]
    if ctx["crates"]:
        out += ["## Waylaid Crates (cheapest bundle; a crate takes any one bundle)", ""]
        out += [f"- {md(c['name'])} (level {c['level']}): " + (f"{c['cheapest']['count']} {md(c['cheapest']['name'])}, {plain_money(c['cheapest']['cost'])}" if c["cheapest"] else "no bundle priced") for c in ctx["crates"]]
        out.append("")
    out += ["## Classes", ""]
    for c in game["classes"]:
        notes = [k for k in content if k.startswith(f"classes/{c['slug']}/")]
        out.append(f"### {c['name']} ({', '.join(name for _, name, _ in c['specs'])})")
        out.append(f"Page: {site.url}classes/{c['slug']}/")
        for key in notes:
            page = content[key]
            out += ["", f"#### {md(page['title'])} ({page['status_label']}{', ' + page['confidence_label'] if page['confidence_label'] else ''}, updated {page['updated']})", "", page["body"]]
        if not notes:
            out.append("No notes yet.")
        out.append("")
    out += ["## Professions", ""]
    for p in game["professions"]:
        recipes = ctx["fdb"].get("recipes", {}).get(p["name"], [])
        out.append(f"- {p['name']} ({p['kind']}): {len(recipes)} recipes, {sum(r['new'] for r in recipes)} new in Forever. {site.url}professions/{p['slug']}/")
        if f"professions/{p['slug']}" in content:
            out += ["", content[f"professions/{p['slug']}"]["body"], ""]
    out += ["", "## World", ""]
    for t in game["world"]:
        out.append(f"### {t['name']}")
        out.append(t["summary"])
        if f"world/{t['slug']}" in content:
            out += ["", content[f"world/{t['slug']}"]["body"]]
        out.append("")
    for slug, title in (("addons", "Addons"), ("macros", "Macros"), ("known-issues", "Known issues")):
        if f"more/{slug}" in content:
            page = content[f"more/{slug}"]
            out += [f"## {title} (updated {page['updated']})", "", page["body"], ""]
    if ctx["log"]:
        out += ["## Latest changes", ""] + [f"- {e['date']}: {md(e['subject'])}" for e in ctx["log"][:20]] + [""]
    out += ["## Sources", "", "- Prices: our own Auctionator scans (market records only); ForeverDB players' scans as a second opinion.",
            f"- Game data (names, recipes, crates, camp kits, vendor prices): Data from ForeverDB.net (https://foreverdb.net), client build {ctx['fdb_source'].get('client_build')}.",
            "- Guides and other references are linked on each page; their text isn't copied here.", ""]
    return "\n".join(out)

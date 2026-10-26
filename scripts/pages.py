"""Page templates: layout, menus, front page, prices and the plain-text files. Section pages
(classes, specs, professions, world, more) are in sections.py. Every value from data goes through esc()."""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from datetime import date

SITE_NAME = "Forever Ledger"
SHORT_NAME = "Ledger"
SUBTITLE = "An unofficial journal for World of Warcraft: Forever"
FOREVERDB = "https://foreverdb.net"
SERVER_ROWS = 1000  # price rows rendered into the HTML for readers without JavaScript
NOTICE = ("World of Warcraft, Warcraft and Blizzard Entertainment are trademarks or registered trademarks of "
          "Blizzard Entertainment, Inc. in the U.S. and/or other countries.")
ROLES = {"dps": "Damage", "tank": "Tank", "healer": "Healer"}


@dataclass
class Site:
    base: str
    url: str
    revision: str
    built: str
    credit: bool
    assets: dict = field(default_factory=dict)  # file name -> content fingerprint
    launch: date = date(2026, 11, 4)
    nav: str = ""  # the main menu, built once per site from the game data

    def asset(self, name: str) -> str:
        return f"{self.base}assets/{name}?v={self.assets.get(name, self.revision)}"

    def has(self, name: str) -> bool:
        return name in self.assets


# --- Small pieces ---------------------------------------------------------------

def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def nice_date(iso: str | None) -> str:
    if not iso:
        return "never"
    d = date.fromisoformat(iso[:10])
    return f"{d.day} {d:%b %Y}"


def when(iso: str | None) -> str:
    return f'<time datetime="{esc(iso)}">{nice_date(iso)}</time>' if iso else "not seen"


def game_day(site: Site, iso: str) -> str:
    """Journal dating: "Day 3" after launch, "5 days before launch" before it."""
    days = (date.fromisoformat(iso[:10]) - site.launch).days
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
    return (f'<a href="{FOREVERDB}/item/{esc(item_id)}" data-foreverdb="item:{esc(item_id)}" target="_blank" rel="noopener">'
            f'{esc(name)}</a>')


def ext(url: str) -> str:
    return ' target="_blank" rel="noopener"' if url.startswith("http") else ""


def links(pairs: list) -> str:
    return '<ul class="elsewhere">' + "".join(f'<li><a href="{esc(url)}"{ext(url)}>{esc(label)}</a></li>' for label, url in pairs) + "</ul>"


def emblem(site: Site, kind: str, slug: str, size: int = 40, colour: str | None = None) -> str:
    """A painted object for a class or profession; a coloured mark until the art exists."""
    name = f"{kind}-{slug}.webp"
    style = f' style="--mark:{esc(colour)}"' if colour else ""
    if site.has(name):
        return (f'<img class="emblem" src="{site.asset(name)}" alt="" width="{size}" height="{size}" '
                f'loading="lazy" decoding="async"{style}>')
    return f'<span class="emblem placeholder" aria-hidden="true"{style}></span>'


def banner(site: Site, section: str, position: str = "70% 50%") -> str:
    name = f"banner-{section}.webp"
    if not site.has(name):
        return ""
    return (f'<div class="banner" aria-hidden="true"><img src="{site.asset(name)}" alt="" width="1536" height="640" '
            f'loading="lazy" decoding="async" style="object-position:{position}"></div>')


def changelog(site: Site, entries: list, title: str = "Changes to this page") -> str:
    if not entries:
        return ""
    rows = "".join(f'<li><span class="when">{when(e["date"])} <span class="day">{game_day(site, e["date"])}</span></span> {esc(e["subject"])}</li>'
                   for e in entries[:12])
    return f'<section class="changes" id="changes"><h2>{esc(title)}</h2><ol class="log">{rows}</ol></section>'


def status_line(page: dict | None) -> str:
    if not page:
        return ""
    facts = [badge("prelaunch") if page["status"] == "pre-launch" else badge("live")]
    if page.get("confidence_label"):
        facts.append(badge(page["confidence"], page["confidence_label"]))
    facts.append(f'<span class="updated">Updated {when(page["updated"])}</span>')
    return f'<p class="status-line">{" ".join(facts)}</p>'


def render_sections(page: dict | None, empty: str, skip: tuple = (), only: tuple | None = None, sources: bool = True) -> str:
    """A note's sections, each styled for what it is: the guides' summary reads as an article,
    our findings sit on a ruled ledger sheet, and the sources are a compact list."""
    if not page:
        return f'<p class="empty">{esc(empty)}</p>'
    out = []
    for sec in page["sections"]:
        if sec["kind"] in skip or (only is not None and sec["kind"] not in only) or (not sec["heading"] and not sec["html"].strip()):
            continue
        heading = f'<h2>{esc(sec["heading"])}</h2>' if sec["heading"] else ""
        body = ('<p class="empty">Nothing recorded yet. Findings from our own play go here, marked with how well they\'re tested.</p>'
                if sec["empty"] else sec["html"])
        out.append(f'<section class="sec sec-{sec["kind"]}" id="{esc(sec["slug"])}">{heading}<div class="prose">{body}</div></section>')
    if sources and page.get("sources"):
        out.append(f'<p class="sources">Sources: {esc(page["sources"])}</p>')
    return "".join(out)


def note_block(page: dict | None, empty: str) -> str:
    return status_line(page) + render_sections(page, empty)


def plain_text(markup: str) -> str:
    """Heading HTML as plain text: tags removed, entities decoded (escape once on output)."""
    return html.unescape(re.sub(r"<[^>]+>", "", markup))


def toc(page: dict | None, extra: tuple = ()) -> str:
    if not page:
        return ""
    items = []
    for sec in page["sections"]:
        if not sec["heading"]:
            continue
        sub = "".join(f'<li><a href="#{esc(anchor)}">{esc(plain_text(label))}</a></li>' for anchor, label in sec["toc"])
        items.append(f'<li><a href="#{esc(sec["slug"])}">{esc(sec["heading"])}</a>{f"<ol>{sub}</ol>" if sub else ""}</li>')
    items += [f'<li><a href="#{esc(anchor)}">{esc(label)}</a></li>' for anchor, label in extra]
    return f'<nav class="toc" aria-label="On this page"><h2 class="aside-title">On this page</h2><ol>{"".join(items)}</ol></nav>' if items else ""


# --- Menus --------------------------------------------------------------------

def nav_html(site: Site, ctx: dict) -> str:
    """The masthead menu. Each top item is a link to its section plus a button that opens a
    panel: on hover or keyboard focus with a mouse, on tap or click everywhere, Escape closes it.
    On phones the panels stack inside the opened menu."""
    b, game = site.base, ctx["game"]

    def item(key: str, label: str, href: str, panel: str) -> str:
        return (f'<li class="menu-item" data-menu><a class="menu-link" href="{b}{href}">{label}</a>'
                f'<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="panel-{key}">'
                f'<span class="visually-hidden">Show {label} menu</span></button>'
                f'<div class="panel panel-{key}" id="panel-{key}">{panel}</div></li>')

    markets = "".join(f'<li><a href="{esc(m["url"])}">{esc(m["name"])}</a> <span class="aside">{esc(m["environment_label"])}</span></li>'
                      for m in ctx["markets"])
    prices = (f'<div class="panel-cols two"><div><h3 class="panel-title">Making gold</h3><ul class="panel-list">'
              f'<li><a href="{b}prices/craft/">What to craft</a><span class="aside">Recipes ranked by margin</span></li>'
              f'<li><a href="{b}prices/crates/">Waylaid Crates</a><span class="aside">Cheapest way to earn Merchant\'s Favor</span></li>'
              f'<li><a href="{b}prices/materials/">Materials worth gathering</a><span class="aside">Herbs, ores, leather and cloth by value</span></li>'
              f'</ul></div><div><h3 class="panel-title">Markets</h3><ul class="panel-list">{markets}</ul>'
              f'<p class="panel-foot"><a href="{b}prices/">All prices</a></p></div></div>')
    class_cells = []
    for c in game["classes"]:
        specs = " ".join(f'<a href="{b}classes/{c["slug"]}/{s["slug"]}/">{esc(s["name"])}</a>' for s in c["specs"])
        class_cells.append(f'<div class="class-cell" style="--class:{esc(c["colour"])}">{emblem(site, "class", c["slug"], 36, c["colour"])}'
                           f'<div><a class="class-link" href="{b}classes/{c["slug"]}/">{esc(c["name"])}</a><div class="spec-links">{specs}</div></div></div>')
    classes = f'<div class="class-grid">{"".join(class_cells)}</div><p class="panel-foot"><a href="{b}classes/">All classes, and choosing one</a></p>'
    groups = {}
    for p in game["professions"]:
        groups.setdefault(p["kind"], []).append(p)
    profs = "".join(f'<div><h3 class="panel-title">{esc(kind)}</h3><ul class="panel-list icons">'
                    + "".join(f'<li><a href="{b}professions/{p["slug"]}/">{emblem(site, "prof", p["slug"], 28)}{esc(p["name"])}</a></li>' for p in items)
                    + "</ul></div>" for kind, items in groups.items())
    professions = f'<div class="panel-cols three">{profs}</div><p class="panel-foot"><a href="{b}professions/">All professions</a></p>'
    world = ('<ul class="panel-list two-col">' + "".join(f'<li><a href="{b}world/{t["slug"]}/">{esc(t["name"])}</a><span class="aside">{esc(t["summary"])}</span></li>'
                                                        for t in game["world"]) + "</ul>")
    more = ('<ul class="panel-list">' + "".join(f'<li><a href="{b}more/{m["slug"]}/">{esc(m["name"])}</a><span class="aside">{esc(m["summary"])}</span></li>'
                                                for m in game["more"])
            + f'<li><a href="{b}more/about/">Sources and credits</a><span class="aside">Where everything comes from</span></li></ul>')
    return (f'<nav class="mainnav" id="mainnav" aria-label="Main"><ul class="menu">'
            + item("prices", "Prices", "prices/", prices) + item("classes", "Classes", "classes/", classes)
            + item("professions", "Professions", "professions/", professions) + item("world", "World", "world/", world)
            + item("more", "More", "more/launch/", more) + "</ul></nav>")


# --- Layout -------------------------------------------------------------------

def layout(site: Site, title: str, body: str, active: str = "", description: str = "", path: str = "") -> str:
    full_title = f"{SITE_NAME}: {SUBTITLE}" if title == SITE_NAME else f"{title} | {SITE_NAME}"
    description = description or "Auction House prices, class guides and discoveries from World of Warcraft: Forever, kept as the game unfolds."
    card = site.asset("social-card.jpg") if site.has("social-card.jpg") else ""
    card_meta = (f'<meta property="og:image" content="{esc(site.url + card[len(site.base):])}">'
                 f'<meta name="twitter:card" content="summary_large_image">') if card else ""
    nav = site.nav.replace(f'<li class="menu-item" data-menu><a class="menu-link" href="{site.base}{active}/"',
                           f'<li class="menu-item current" data-menu><a class="menu-link" aria-current="page" href="{site.base}{active}/"') if active else site.nav
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(site.url + path)}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(site.url + path)}">
{card_meta}
<link rel="alternate" type="text/plain" title="The whole ledger as plain text" href="{site.base}llms-full.txt">
<meta name="color-scheme" content="light dark">
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="icon" href="{site.asset("icon.svg")}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;1,7..72,400&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="{site.asset("style.css")}">
<script src="{site.asset("app.js")}" defer></script>
<script src="{FOREVERDB}/embed/tooltips.js" data-icons="true" data-color-links="true" async></script>
</head>
<body data-base="{site.base}" data-launch="{site.launch.isoformat()}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="masthead-inner">
    <a class="wordmark" href="{site.base}"><span class="mark" aria-hidden="true"></span><span class="name">{SITE_NAME}</span><span class="sub">{SUBTITLE}</span></a>
    <button class="nav-open" type="button" aria-expanded="false" aria-controls="mainnav">Menu</button>
    {nav}
    <button class="theme-toggle" type="button" data-theme-toggle aria-label="Colour theme: follows your device">
      <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 3.75a8.25 8.25 0 0 0 0 16.5z" fill="currentColor"/><circle cx="12" cy="12" r="8.25" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>
      <span class="theme-label">Auto</span>
    </button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="colophon">
  <div class="colophon-inner">
    <p class="colophon-name"><span class="mark" aria-hidden="true"></span>{SITE_NAME}</p>
    <p>An unofficial fan project, not affiliated with or endorsed by Blizzard Entertainment. {NOTICE}</p>
    <p>{'Item names, recipes, tooltips and second-opinion prices: <a href="' + FOREVERDB + '">Data from ForeverDB.net</a>. ' if site.credit else ''}Prices come from our own Auctionator scans. Guides are summarised in our own words and linked; the originals belong to their authors.</p>
    <p>Built {esc(site.built)}, revision {esc(site.revision)}. <a href="{site.base}llms-full.txt">Plain-text version</a> · <a href="{site.base}more/about/">Sources and credits</a></p>
  </div>
</footer>
</body>
</html>
'''


def page_head(title: str, lede: str = "", crumbs: tuple = (), extra: str = "", mark: str = "", colour: str | None = None) -> str:
    crumb = "".join(f'<a href="{esc(url)}">{esc(label)}</a>' for label, url in crumbs)
    style = f' style="--class:{esc(colour)}"' if colour else ""
    return (f'<header class="page-head{" coloured" if colour else ""}"{style}><div class="page-head-inner">'
            f'{f"<p class=crumbs>{crumb}</p>" if crumb else ""}'
            f'<div class="title-row">{mark}<h1>{esc(title)}</h1></div>'
            f'{f"<p class=lede>{lede}</p>" if lede else ""}{extra}</div></header>')


# --- Front page -------------------------------------------------------------------

def checklist_items(ctx: dict, limit: int = 6) -> list[tuple[str, str]]:
    """The launch checklist's own headings, so the front page always matches the page."""
    page = ctx["content"].get("more/launch")
    if not page:
        return []
    items = []
    for sec in page["sections"]:
        if sec["kind"] in ("findings", "more"):
            continue
        items += [(anchor, plain_text(label)) for anchor, label in sec["toc"]]
    return items[:limit]


def blue_list(site: Site, posts: list, limit: int, excerpts: bool = False) -> str:
    rows = []
    for p in posts[:limit]:
        if not str(p.get("url", "")).startswith("https://us.forums.blizzard.com/"):
            continue  # only ever link to Blizzard's own forums
        excerpt = (f'<blockquote class="blue-excerpt"><p>{esc(p["excerpt"])}</p></blockquote>' if excerpts and p.get("excerpt") else "")
        rows.append(f'<li><a class="blue-title" href="{esc(p["url"])}" target="_blank" rel="noopener">{esc(p["title"])}</a>'
                    f'<span class="blue-meta">{esc(p["author"])}{", " + esc(p["author_title"]) if p.get("author_title") else ""} · '
                    f'{when(p["posted"])}{" · reply" if p.get("reply") else ""}</span>{excerpt}</li>')
    return f'<ol class="blue-list">{"".join(rows)}</ol>'


def home(site: Site, ctx: dict) -> str:
    primary, game, content, b = ctx["primary"], ctx["game"], ctx["content"], site.base
    days_to_go = (site.launch - date.fromisoformat(site.built[:10])).days
    countdown = (f"Forever opens in {days_to_go} day{'s' if days_to_go != 1 else ''}" if days_to_go > 0
                 else "Forever opens today" if days_to_go == 0 else f"Day {1 - days_to_go} of Forever")
    search_action = f'{primary["url"]}#prices' if primary else f"{b}prices/"

    hero_art = ""
    if site.has("hero-day.webp"):
        # Both paintings are in the page; the theme decides which shows (CSS), so a manual
        # light/dark choice swaps them too. Lazy loading keeps the hidden one from downloading.
        night = (f'<img class="night" src="{site.asset("hero-night.webp")}" alt="" width="1536" height="1024" loading="lazy" decoding="async">'
                 if site.has("hero-night.webp") else "")
        hero_art = (f'<div class="hero-art" aria-hidden="true"><img class="day" src="{site.asset("hero-day.webp")}" alt="" width="1536" height="1024" '
                    f'loading="lazy" decoding="async">{night}</div>')

    checklist = checklist_items(ctx)
    check_html = ("<ol class=\"checklist\">" + "".join(f'<li><a href="{b}more/launch/#{esc(a)}">{esc(t)}</a></li>' for a, t in checklist) + "</ol>"
                  if checklist else '<p class="empty">The launch checklist is being written.</p>')
    issues = content.get("more/known-issues")
    issue_titles = []
    if issues:
        for sec in issues["sections"]:
            if sec["kind"] not in ("findings", "more"):
                issue_titles += [plain_text(label) for _, label in sec["toc"]]
    issue_line = (f'<p class="dash-note"><a href="{b}more/known-issues/">Known issues</a>: {len(issue_titles)} tracked, '
                  f'including “{esc(issue_titles[0])}”.</p>' if issue_titles else "")

    pulse = ""
    if primary:
        current = [i for i in primary["current"] if i["volatility"]]
        share = {v: sum(1 for i in current if i["volatility"] == v) for v in ("steady", "moving", "volatile")}
        total = max(len(current), 1)
        meter = "".join(f'<span class="meter-{v}" style="width:{share[v] * 100 / total:.1f}%" title="{share[v]:,} {v}"></span>' for v in ("steady", "moving", "volatile"))
        rows = "".join(f'<tr><th scope="row">{item_link(i["id"], i["name"])}</th><td class="num">{money(i["typical"])}</td><td>{steadiness(i["volatility"])}</td></tr>'
                       for i in primary["highlights"]["most_listed"][:5])
        crafts = "".join(f'<li>{item_link(r["item"], r["name"])} <span class="aside">{esc(r["profession"])}</span> <span class="value">{money(r["margin"])}</span></li>'
                         for r in ctx["craft"][:3])
        beta = badge("beta") if primary["environment"] == "forever-beta" else ""
        pulse = f'''<section class="dash-card pulse" aria-labelledby="pulse-title">
  <h2 id="pulse-title"><a href="{b}prices/">Market pulse</a> {beta}</h2>
  <div class="meter" role="img" aria-label="{share["steady"]:,} steady, {share["moving"]:,} moving and {share["volatile"]:,} volatile prices">{meter}</div>
  <p class="meter-key"><span class="k-steady">{share["steady"] * 100 // total}% steady</span> <span class="k-moving">{share["moving"] * 100 // total}% moving</span> <span class="k-volatile">{share["volatile"] * 100 // total}% volatile</span></p>
  <table class="compact"><caption>Most listed on {nice_date(primary["last_date"])}</caption><tbody>{rows}</tbody></table>
  {f'<h3 class="mini-title"><a href="{b}prices/craft/">Best crafting margins</a></h3><ul class="mini-list">{crafts}</ul>' if crafts else ""}
</section>'''

    blue = ctx["blue"].get("posts", [])
    blue_html = (blue_list(site, blue, 5) + f'<p class="dash-note"><a href="{b}more/blizzard/">All Blizzard posts</a>'
                 f'{" · checked " + nice_date(ctx["blue"].get("fetched")) if ctx["blue"].get("fetched") else ""}</p>') if blue else '<p class="empty">No posts yet.</p>'

    def spec_links(c: dict) -> str:
        return " · ".join(f'<a href="{b}classes/{c["slug"]}/{spec["slug"]}/">{esc(spec["name"])}</a>' for spec in c["specs"])
    picker = "".join(f'<li style="--class:{esc(c["colour"])}"><a class="pick" href="{b}classes/{c["slug"]}/">'
                     f'{emblem(site, "class", c["slug"], 48, c["colour"])}<span>{esc(c["name"])}</span></a>'
                     f'<span class="pick-specs">{spec_links(c)}</span></li>' for c in game["classes"])
    latest = "".join(
        f'<li><span class="when">{when(e["date"])} <span class="day">{game_day(site, e["date"])}</span></span> '
        + (f'<a href="{b}{esc(e["urls"][0])}">{esc(e["subject"])}</a>' if e["urls"] else esc(e["subject"])) + "</li>"
        for e in ctx["log"][:6])
    profs = "".join(f'<li><a href="{b}professions/{p["slug"]}/">{emblem(site, "prof", p["slug"], 32)}<span>{esc(p["name"])}</span></a></li>' for p in game["professions"])
    world = "".join(f'<li><a href="{b}world/{t["slug"]}/">{esc(t["name"])}</a></li>' for t in game["world"])

    return layout(site, SITE_NAME, f'''<section class="intro">
  <div class="intro-text">
    <p class="countdown" data-countdown>{countdown}</p>
    <h1>{SITE_NAME}</h1>
    <p class="lede">Prices from our own Auction House scans, the best class and profession guides summarised in one place, and what we find as we play World of Warcraft: Forever.</p>
    <form class="lookup" action="{esc(search_action)}" method="get" role="search">
      <label for="lookup" class="visually-hidden">Search the ledger</label>
      <div class="lookup-row"><input id="lookup" name="q" type="search" placeholder="Search: Linen Cloth, Frost Mage, camping" autocomplete="off" aria-controls="lookup-results"><button type="submit">Search</button></div>
      <ul id="lookup-results" class="lookup-results" hidden></ul>
    </form>
  </div>
  {hero_art}
</section>
<div class="dash">
  <section class="dash-card checklist-card" aria-labelledby="check-title">
    <h2 id="check-title"><a href="{b}more/launch/">Before you log in</a></h2>
    {check_html}
    {issue_line}
  </section>
  {pulse}
  <section class="dash-card blue-card" aria-labelledby="blue-title">
    <h2 id="blue-title"><a href="{b}more/blizzard/">Blizzard says</a></h2>
    {blue_html}
  </section>
</div>
<div class="dash dash-lower">
  <section class="dash-card picker-card" aria-labelledby="picker-title">
    <h2 id="picker-title"><a href="{b}classes/">Choose your class</a></h2>
    <ul class="picker">{picker}</ul>
  </section>
  <section class="dash-card latest-card" aria-labelledby="latest-title">
    <h2 id="latest-title">Latest in the ledger</h2>
    <ol class="log">{latest or "<li>Nothing recorded yet.</li>"}</ol>
  </section>
</div>
<div class="dash dash-lower">
  <section class="dash-card prof-card" aria-labelledby="prof-title">
    <h2 id="prof-title"><a href="{b}professions/">Professions</a></h2>
    <ul class="prof-strip">{profs}</ul>
  </section>
  <section class="dash-card world-card" aria-labelledby="world-title">
    <h2 id="world-title"><a href="{b}world/">The world</a></h2>
    <ul class="tag-list">{world}</ul>
  </section>
</div>''', active="", path="")


def not_found(site: Site) -> str:
    return layout(site, "Page not found", page_head("This page isn't in the ledger", "It may have moved when the site was reorganised.")
                  + f'''<section class="page-body prose"><p>Try the <a href="{site.base}">front page</a>, search from there, or start from
  <a href="{site.base}prices/">Prices</a>, <a href="{site.base}classes/">Classes</a>, <a href="{site.base}professions/">Professions</a> or
  <a href="{site.base}world/">World</a>.</p></section>''', path="404.html")


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
                  + banner(site, "prices") + f'''<section class="page-body">
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

    def block(key: str, level: str = "###") -> list[str]:
        """One page: its title, how current and how sure it is, its address, then its text."""
        page = content[key]
        facts = [page["status_label"]] + ([page["confidence_label"]] if page.get("confidence_label") else []) + [f"updated {page['updated']}"]
        return [f"{level} {md(page['title'])}", "", f"Status: {', '.join(facts)}. Page: {site.url}{page['url']}",
                f"Summary: {md(page.get('summary', ''))}", "", page["body"], ""]

    out = [f"# {SITE_NAME}", "", f"{SUBTITLE} (launch: {nice_date(site.launch.isoformat())}). Prices come from our own Auctionator scans; "
           "game data from ForeverDB; guide summaries are written in our own words and cite their sources. Not affiliated with Blizzard Entertainment.",
           f"Site: {site.url}  Built: {site.built}  Revision: {site.revision}", "",
           "## How to read this file", "",
           "- Every page says its status. \"Pre-launch\" means written before launch (4 November 2026) or not yet confirmed in the live game: treat it as tentative. \"Live\" means checked in the live game. \"Beta\" marks prices from Forever Beta scans.",
           "- \"What the guides say\" sections summarise other sites' guides (linked under \"Read more\"). \"Ledger findings\" are our own discoveries, with a confidence: idea, testing, tested or outdated.",
           "- Prices are per item in gold (g), silver (s) and copper (c): 1g = 100s = 10,000c. All prices are asking prices, not sales.",
           "- \"Typical\" is the median of each day's cheapest listing over the item's last seven days; use it for \"what does X cost\". \"Latest\" is the most recent cheapest listing.",
           "- \"Steadiness\" (steady / moving / volatile) says how far the daily price swung over two weeks. Treat volatile prices with caution.", ""]
    out += ["## Markets", ""] + [f"- {md(m['name'])} ({m['environment_label']}): {len(m['items']):,} items, newest data {m['last_date']}. "
                                 f"Prices (TSV): {site.url}{m['files']['prices_tsv'][len(site.base):]}" for m in ctx["markets"]] + [""]
    for m in ctx["markets"][:1]:
        h = m["highlights"]
        if h["most_listed"]:
            out += [f"### Most listed in {md(m['name'])} on {m['last_date']}", "", "| Item | ID | Typical | Steadiness | Listed |", "|---|---|---|---|---|"]
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
    posts = [p for p in ctx["blue"].get("posts", []) if str(p.get("url", "")).startswith("https://us.forums.blizzard.com/")]
    if posts:
        out += [f"## Blizzard's latest posts about Forever (checked {ctx['blue'].get('fetched', '')[:16].replace('T', ' ')} UTC)", ""]
        out += [f"- {p['posted'][:10]}: {md(p['title'])} ({md(p['author'])}). {p['url']}" for p in posts[:15]] + [""]
    if "more/launch" in content:
        out += ["## Launch checklist", ""] + block("more/launch", "###")
    out += ["## Classes", ""]
    for c in game["classes"]:
        out += [f"### {c['name']} (specs: {', '.join(s['name'] for s in c['specs'])})", f"Page: {site.url}classes/{c['slug']}/", ""]
        keys = [f"classes/{c['slug']}/{part}" for part in ["overview"] + [s["slug"] for s in c["specs"]] + ["hybrid", "macros"]]
        found = [k for k in keys if k in content]
        for key in found:
            out += block(key, "####")
        if not found:
            out += ["No notes yet.", ""]
    out += ["## Professions", ""]
    for p in game["professions"]:
        recipes = ctx["fdb"].get("recipes", {}).get(p["name"], [])
        out.append(f"- {p['name']} ({p['kind']}): {len(recipes)} recipes, {sum(r['new'] for r in recipes)} new in Forever. {site.url}professions/{p['slug']}/")
    out.append("")
    for p in game["professions"]:
        if f"professions/{p['slug']}" in content:
            out += block(f"professions/{p['slug']}")
    out += ["## World", ""]
    for t in game["world"]:
        out += block(f"world/{t['slug']}") if f"world/{t['slug']}" in content else [f"### {t['name']}", "", t["summary"], ""]
    for m in game["more"]:
        if m["slug"] != "launch" and f"more/{m['slug']}" in content:
            out += [f"## {m['name']}", ""] + block(f"more/{m['slug']}", "###")
    if ctx["log"]:
        out += ["## Latest changes", ""] + [f"- {e['date']}: {md(e['subject'])}" for e in ctx["log"][:20]] + [""]
    out += ["## Sources", "", "- Prices: our own Auctionator scans (market records only); ForeverDB players' scans as a second opinion.",
            f"- Game data (names, recipes, crates, camp kits, vendor prices): Data from ForeverDB.net (https://foreverdb.net), client build {ctx['fdb_source'].get('client_build')}.",
            "- Blizzard's posts: Blizzard's own forums; titles and links only here.",
            "- Guides are summarised in our own words and linked on each page; their text isn't copied.", ""]
    return "\n".join(out)

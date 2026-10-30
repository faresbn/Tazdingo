"""The Auction House pages: the dashboard blocks, item pages and their charts.

The measures come from scripts/market.py; this module only presents them. Every list
says when its scan was taken, and every page says plainly that the data holds prices and
listings, never sales.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone

import market as m
from auctionator import DAY_ZERO, day_date
from pages import (FOREVERDB, Site, badge, change, esc, layout, money, nice_date, page_head, plain_money, steadiness, tabs, alias)

DAY_ZERO_EPOCH = datetime(DAY_ZERO.year, DAY_ZERO.month, DAY_ZERO.day, tzinfo=timezone.utc).timestamp()
CHART_DAYS = 30


def item_slug(key: str) -> str:
    if key.isdigit():
        return key
    slug = re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")
    if re.search(r"[^\x00-\x7f]", key):  # a suffix name in another alphabet: keep two such variants apart
        slug += "-" + hashlib.sha256(key.encode()).hexdigest()[:8]
    return slug


def item_url(site: Site, market: dict, item: dict) -> str:
    return f"{site.base}prices/{market['slug']}/item/{item_slug(item['key'])}/"


def item_anchor(site: Site, market: dict, item: dict) -> str:
    """A link to our item page that still shows ForeverDB's tooltip on hover."""
    return f'<a href="{item_url(site, market, item)}" data-foreverdb="item:{esc(item["id"])}">{esc(item["name"])}</a>'


def scan_time(timestamp: int | None) -> str:
    if not timestamp:
        return "unknown"
    moment = datetime.fromtimestamp(timestamp, timezone.utc)
    return f'<time datetime="{moment.isoformat().replace("+00:00", "Z")}" data-local-time>{moment:%d %b %Y, %H:%M} UTC</time>'


def num(value) -> str:
    return "" if value is None else f"{int(value):,}"


def pct(value: float | None) -> str:
    return "" if value is None else f"{round(value * 100):,}%"


def scan_note(market: dict, ah: dict) -> str:
    beta = " " + badge("beta") if market["environment"] == "forever-beta" else ""
    return (f'<p class="scan-note">{beta} Newest upload: {scan_time(ah["newest"])}. Prices are the cheapest listing each upload recorded, with the upload\'s time (Auctionator may have seen it earlier that day). '
            f'{ah["scans_in_window"]:,} scan{"s" if ah["scans_in_window"] != 1 else ""} in the current window.</p>')


# --- Lists ---------------------------------------------------------------------------------

def table(head: list[str], rows: list[str], caption: str = "", show_more: bool = False) -> str:
    """A list table. With show_more, rows marked class="extra" stay folded behind a button until asked for."""
    cells = "".join(f'<th scope="col"{" class=num" if h.startswith("#") else ""}>{esc(h.lstrip("#"))}</th>' for h in head)
    more = f'<button class="show-more" type="button" data-show-more hidden>Show all {len(rows)}</button>' if show_more else ""
    return (f'<div class="table-wrap"{" data-foldable" if show_more else ""}><table class="ah-list">{f"<caption>{caption}</caption>" if caption else ""}'
            f'<thead><tr>{cells}</tr></thead><tbody>{"".join(rows)}</tbody></table>{more}</div>')


DEALS_SHOWN = 25


def vendor_tag(item: dict) -> str:
    profit = (item["deal"] or {}).get("vendor_profit")
    return f' <span class="badge vendor" title="A vendor pays {esc(plain_money(item["vendor_sell"]))}">Below vendor price</span>' if profit else ""


def deals_block(site: Site, market: dict, ah: dict, limit: int | None = None) -> str:
    """Every deal, exceptional ones first; past the first 25 the rows wait behind a button (all are in the HTML)."""
    deals = ah["deals"][:limit] if limit else ah["deals"]
    rows = [f'<tr{" class=extra" if n >= DEALS_SHOWN else ""}><th scope="row">{item_anchor(site, market, i)}'
            f'{" " + badge("exceptional", "Exceptional") if i["deal"]["exceptional"] else ""}{vendor_tag(i)}</th><td class="num">{money(i["latest"])}</td>'
            f'<td class="num">{money(i["ref"])}</td><td class="num"><span class="change down">−{pct(i["deal"]["discount"])}</span></td>'
            f'<td class="num">{money(i["deal"]["saving"])}</td><td>{confidence(i["deal"]["confidence"])}</td><td class="date">{scan_time(i["latest_time"])}</td></tr>'
            for n, i in enumerate(deals)]
    body = (table(["Item", "#Price", "#Usual", "#Under usual", "#Saving a unit", "Confidence", "Recorded"], rows, show_more=len(rows) > DEALS_SHOWN) if rows
            else f'<p class="empty">No item in the newest scan was recorded at least {round(m.DEAL_DISCOUNT * 100)}% under its usual price with enough history to trust.</p>')
    if ah["deals_hidden"]:
        body += (f'<p class="aside">{ah["deals_hidden"]} more recorded far under usual but with too little history to trust, '
                 'or so far under (90%+) that it\'s probably one mispriced unit.</p>')
    vendor_only = [i for i in ah["vendor"] if i not in deals]  # rare items the deals table doesn't already show
    if vendor_only:
        rows = [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
                f'<td class="num">{money(i["vendor_sell"])}</td><td class="num">{money(i["deal"]["vendor_profit"])}</td><td class="date">{scan_time(i["latest_time"])}</td></tr>'
                for i in vendor_only]
        body += ('<h3 class="part-title">Below vendor price</h3><p class="aside">Rare or better items and recipes recorded at least 1 silver under what a vendor pays. '
                 'Vendor prices: <a href="https://foreverdb.net">Data from ForeverDB.net</a>.</p>'
                 + table(["Item", "#Price", "#Vendor pays", "#Potential profit a unit", "Recorded"], rows))
    return (f'<p class="aside block-note">Recorded at least {round(m.DEAL_DISCOUNT * 100)}% under the item\'s usual price (the middle of its daily lows over {m.RECENT_DAYS} days) '
            f'on the newest day of scans. <strong>Exceptional</strong> ones are at least {round(m.EXCEPTIONAL_DISCOUNT * 100)}% under and further under than the item normally swings; '
            'they come first. A price history, not a promise: a cheap listing may be gone within minutes, and the data holds no sales.</p>' + body)


def confidence(level: str) -> str:
    return f'<span class="badge conf-{esc(level)}" title="How much history the usual price rests on">{esc(level.capitalize())}</span>'


def short_block(site: Site, market: dict, ah: dict, limit: int = 60) -> str:
    rows = [f'<tr{" class=extra" if n >= DEALS_SHOWN else ""}><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
            f'<td class="num"><span class="change up">+{pct(i["short"]["price"])}</span></td>'
            f'<td class="num">{pct(i["short"]["stock"])}</td></tr>' for n, i in enumerate(ah["short"][:limit])]
    if not rows:
        return ""
    return (
            f'<p class="aside">Priced at least {round((m.SHORT_PRICE - 1) * 100)}% over usual while the most units listed on the last full day '
            f'fell to half its usual level or less: a sign of a shortage, and of a chance to sell.</p>'
            f'{table(["Item", "#Price", "#Over usual", "#Stock against usual"], rows, show_more=len(rows) > DEALS_SHOWN)}')


def index_chart(ah: dict, events: list[dict]) -> str:
    series = ah["index"]
    if len(series) < 3:
        return ""
    width, height, pad = 720.0, 160.0, 22.0
    first, last = series[0][0], series[-1][0]
    span = max(last - first, 1)
    values = [v for _, v, _ in series]
    low, high = min(min(values), 95.0), max(max(values), 105.0)

    def x(day):
        return round((day - first) / span * width, 1)

    def y(value):
        return round(height - pad - (value - low) / (high - low) * (height - 2 * pad), 1)
    path = " ".join(("M" if n == 0 else "L") + f"{x(d)},{y(v)}" for n, (d, v, _) in enumerate(series))
    dots = "".join(f'<circle class="scan" cx="{x(d)}" cy="{y(v)}" r="2.5"><title>{day_date(d)}: {v}</title></circle>' for d, v, _ in series)
    svg = (f'<svg viewBox="0 0 {int(width)} {int(height)}" role="img" aria-label="Market price index from {day_date(first)} to {day_date(last)}">'
           f'<line class="typical" x1="0" y1="{y(100)}" x2="{width}" y2="{y(100)}"/><path class="scan-line" d="{path}"/>{dots}'
           f'<text class="tick" x="0" y="{height - 6}">{day_date(first)}</text><text class="tick" x="{width}" y="{height - 6}" text-anchor="end">{day_date(last)}</text>'
           f'<text class="tick" x="4" y="{y(high) + 10}">{high:.0f}</text><text class="tick" x="4" y="{y(low) - 3}">{low:.0f}</text></svg>')
    return ('<h3 class="part-title">Market index</h3><p class="aside">Each day, the middle of every item\'s lowest price measured against its own usual level: 100 is normal, 105 means '
            'prices across the market sat 5% higher. Unfinished and partial-scan days are left out.</p>'
            f'<figure class="price-chart">{svg}{event_note(events, first, last)}</figure>')


def invest_block(site: Site, market: dict, ah: dict, limit: int = 60) -> str:
    rows = [f'<tr{" class=extra" if n >= DEALS_SHOWN else ""}><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
            f'<td class="num">{money(i["ref"])}</td><td class="num">{money(i["invest"]["margin"])}</td>'
            f'<td class="num">{pct(i["invest"]["roi"])}</td><td>{steadiness(i["volatility"])}</td>'
            f'<td class="num">{pct(i["presence"])}</td></tr>' for n, i in enumerate(ah["invest"][:limit])]
    body = (table(["Item", "#Price", "#Usual", "#Margin a unit", "#Return", "Steadiness", "#Days listed"], rows, show_more=len(rows) > DEALS_SHOWN) if rows
            else '<p class="empty">No item is cheap enough against its own history right now.</p>')
    return (
            f'<p class="aside">Recorded in the cheapest quarter of its last {m.WINDOW_DAYS} days, listed on most of them, usually several at once, and not volatile. '
            f'The margin assumes it sells again at its usual price, less the {round(m.AH_CUT * 100)}% Auction House cut. '
            'An estimate from the price spread, not proven demand: the data shows prices and listings, not sales.</p>'
            f'{body}')


def movers_block(site: Site, market: dict, ah: dict, limit: int = 10) -> str:
    def rows(items):
        return [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
                f'<td class="num">{money(i["move"]["base"])}</td><td class="num">{change(i["move"]["change"])}</td></tr>' for i in items[:limit]]
    weekly_up = market["highlights"]["rising"][:limit]
    weekly_down = market["highlights"]["falling"][:limit]

    def weekly(items):
        return [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["typical"])}</td>'
                f'<td class="num">{change(i["change"])}</td></tr>' for i in items]
    parts = []
    if ah["rising"] or ah["falling"]:
        parts.append('<div class="ah-cols">'
                     + (f'<div><h3>Up on the last full day</h3>{table(["Item", "#Latest", "#Last full day", "#Change"], rows(ah["rising"]))}</div>' if ah["rising"] else "")
                     + (f'<div><h3>Down on the last full day</h3>{table(["Item", "#Latest", "#Last full day", "#Change"], rows(ah["falling"]))}</div>' if ah["falling"] else "")
                     + '</div>')
    if weekly_up or weekly_down:
        parts.append('<div class="ah-cols">'
                     + (f'<div><h3>Rising this week</h3>{table(["Item", "#Typical", "#Week on week"], weekly(weekly_up))}</div>' if weekly_up else "")
                     + (f'<div><h3>Falling this week</h3>{table(["Item", "#Typical", "#Week on week"], weekly(weekly_down))}</div>' if weekly_down else "")
                     + '</div>')
    body = "".join(parts) or ('<p class="empty">Nothing has moved far enough yet. '
                              'Weekly movers need three days of prices in each of the last two weeks.</p>')
    return (
            f'<p class="aside">The first pair compares each item\'s latest recorded price with its lowest price on the last full day of scans (a move of {round(m.MOVE_MIN_CHANGE * 100)}% or more). '
            'The week compares the middle of the last seven days\' lowest prices with the seven before.</p>'
            f'{body}')


def reliable_block(site: Site, market: dict, ah: dict, limit: int = 40) -> str:
    rows = [f'<tr{" class=extra" if n >= DEALS_SHOWN else ""}><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["typical"])}</td>'
            f'<td class="num">{pct(i["presence"])}</td><td class="num">{num(i["listed_median"])}</td>'
            f'<td class="num">{pct(i["churn"])}</td></tr>' for n, i in enumerate(ah["reliable"][:limit])]
    if not rows:
        return ""
    return (
            '<p class="aside">The data holds no sales, so this is the closest honest measure of what\'s always available: items listed on nearly every day, '
            'how many are usually up at once, and how often the day\'s lowest price changed from one day to the next (sales, new listings, cancellations and expiries all change it).</p>'
            f'{table(["Item", "#Typical", "#Days listed", "#Usually listed", "#Daily low changed"], rows, show_more=len(rows) > DEALS_SHOWN)}')


def heat(index: float | None) -> str:
    if index is None:
        return "heat-none"
    delta = index - 1
    return ("heat-low2" if delta <= -0.06 else "heat-low1" if delta <= -0.02 else
            "heat-high2" if delta >= 0.06 else "heat-high1" if delta >= 0.02 else "heat-mid")


def signed_pct(index: float | None) -> str:
    return "…" if index is None else f"{(index - 1) * 100:+.0f}%"


def patterns_block(ah: dict) -> str:
    p = ah["patterns"]

    def cell(entry):
        index = (entry or {}).get("index")
        return f'<td class="{heat(index)}">{signed_pct(index)}</td>'
    days = "".join(f'<th scope="col">{d}</th>' for d in m.WEEKDAYS)
    weekday = "".join(cell(p["weekday"].get(d)) for d in range(7))
    bands = "".join(f'<th scope="col">{label}</th>' for label in m.BAND_LABELS)
    grid = "".join(f'<tr><th scope="row">{name}</th>' + "".join(cell(p["cells"].get(f"{d}-{b}")) for b in range(6)) + '</tr>'
                   for d, name in enumerate(m.WEEKDAYS))
    weekday_ready = any(c["index"] is not None for c in p["weekday"].values())
    time_ready = any(c["index"] is not None for c in p["cells"].values())
    return ('<h3 class="part-title">When prices are lowest</h3><p class="aside">How far prices sit above or below each item\'s own middle price. Green cells are cheaper times to buy, warmer cells better times to sell. '
            f'A cell shows once {m.PATTERN_MIN_ITEMS} items have prices in it on at least {m.PATTERN_MIN_DATES} different dates.</p>'
            '<h4>By weekday</h4><p class="aside">From each full day\'s lowest price.</p>'
            + ("" if weekday_ready else '<p class="empty">Collecting: needs at least two of each weekday.</p>')
            + f'<div class="table-wrap"><table class="heatmap"><thead><tr>{days}</tr></thead><tbody><tr>{weekday}</tr></tbody></table></div>'
            f'<h4>By time of day</h4><p class="aside">From uploads that include a new full scan, at that scan\'s own time ({ah["full_scans"]} so far; '
            'hours in UTC<span data-utc-offset></span>). It can only reflect the times full scans were taken, so a band nobody scans in stays empty.</p>'
            + ("" if time_ready else '<p class="empty">Collecting: full scans spread across the day and the week fill this in.</p>')
            + f'<div class="table-wrap"><table class="heatmap"><thead><tr><td></td>{bands}</tr></thead><tbody>{grid}</tbody></table></div>')


def figures(market: dict, ah: dict) -> str:
    """The board's strip of headline figures."""
    index = ah["index"][-1][1] if ah["index"] else None
    exceptional = sum(1 for i in ah["deals"] if i["deal"]["exceptional"])
    cells = [("Newest scan", scan_time(ah["newest"])), ("Items in the last two weeks", f'{len(market["current"]):,}'),
             ("Under usual price", f'{len(ah["deals"]):,}' + (f' <span class="aside">{exceptional} exceptional</span>' if exceptional else "")),
             ("Investment picks", f'{len(ah["invest"]):,}'),
             ("Market index", f'{index:.0f}' + ' <span class="aside">100 is normal</span>' if index is not None else '<span class="aside">collecting</span>')]
    beta = badge("beta") if market["environment"] == "forever-beta" else ""
    return (f'<dl class="figures">{"".join(f"<div><dt>{label}</dt><dd>{value}</dd></div>" for label, value in cells)}</dl>'
            f'<p class="scan-note">{beta} {esc(market["name"])}, {esc(market["environment_label"])}. Prices are the cheapest listing each upload recorded, '
            'with the upload\'s time (Auctionator may have seen it earlier that day).</p>')


def board(site: Site, market: dict, ah: dict, events: list | None = None) -> str:
    """The Auction House board: one tab per question a buyer or seller asks."""
    events = events or []
    exceptional = sum(1 for i in ah["deals"] if i["deal"]["exceptional"])
    panels = [("deals", "Deals", alias("vendor") + deals_block(site, market, ah)), ("invest", "Investments", invest_block(site, market, ah)),
              ("short", "Short supply", short_block(site, market, ah)), ("movers", "Movers", movers_block(site, market, ah)),
              ("reliable", "Always listed", reliable_block(site, market, ah)),
              ("patterns", "Patterns", alias("index") + index_chart(ah, events) + patterns_block(ah))]
    return figures(market, ah) + tabs(panels, {"deals": len(ah["deals"]) or None, "invest": len(ah["invest"]) or None})


def home_block(site: Site, market: dict, ah: dict) -> str:
    """The homepage's Auction House card: deals first, then investments and movers."""
    def mini(title, href, items, value, limit=5, counted=True):
        if not items:
            return ""
        rows = "".join(f'<li>{item_anchor(site, market, i)} <span class="value">{value(i)}</span></li>' for i in items[:limit])
        more = f' <a class="aside" href="{href}">{f"all {len(items)}" if counted else "more"}</a>' if len(items) > limit else ""
        return f'<h3 class="mini-title">{title}{more}</h3><ul class="mini-list">{rows}</ul>'
    b = site.base
    deals = mini("Under the usual price", f"{b}prices/#deals", ah["deals"],
                 lambda i: money(i["latest"]) + f' <span class="change down">−{pct(i["deal"]["discount"])}</span>')
    invest = mini("Investment picks", f"{b}prices/#invest", ah["invest"], lambda i: f'+{plain_money(i["invest"]["margin"])} a unit', 3)
    moving = mini("Moved since the last full day", f"{b}prices/#movers", ah["rising"] + ah["falling"], lambda i: change(i["move"]["change"]), 3, counted=False)
    return (deals or f'<p class="empty">No deals at least {round(m.DEAL_DISCOUNT * 100)}% under the usual price in the newest scan.</p>') + invest + moving + scan_note(market, ah)


# --- Item pages ----------------------------------------------------------------------------

def day_x(day: float, first: int, span: int, width: float) -> float:
    return round((day - first) / span * width, 1)


def event_note(events: list[dict], first: int, last: int) -> str:
    """Dated events in the chart's range, listed by their UTC time. The bands follow the scanner's
    own calendar days, so events are named under the chart rather than drawn on it."""
    shown = []
    for event in events:
        moment = datetime.fromisoformat(event["at"].replace("Z", "+00:00"))
        day = (moment.timestamp() - DAY_ZERO_EPOCH) / 86400
        if first - 1 <= day <= last + 1:
            shown.append(f'{esc(event["label"])}: {moment:%d %b, %H:%M} UTC')
    return f'<p class="aside event-note">In this range: {"; ".join(shown)}.</p>' if shown else ""


def chart(item: dict, market: dict, events: list[dict]) -> str:
    """Daily low–high bands, every scan price and the typical price over the last 30 days."""
    last = market["last_day"]
    if last is None or not item["days"]:
        return ""
    first = last - CHART_DAYS + 1
    days = {d: v for d, v in item["days"].items() if d >= first}
    by_day = {}
    for t, p, d in item["obs"]:
        if d >= first:
            by_day.setdefault(d, []).append(p)
    # Each recorded price sits inside its own Auctionator day's band, spread in the order it was recorded.
    obs = [(d + (n + 1) / (len(prices) + 1), p) for d, prices in sorted(by_day.items()) for n, p in enumerate(prices)]
    values = [v["low"] for v in days.values()] + [p for _, p in obs]
    if not values:
        return ""
    ceiling = 4 * sorted(values)[len(values) // 2]  # clip troll listings so the shape stays readable
    top = max(min(max([v["high"] for v in days.values()] + [p for _, p in obs]), ceiling), 1)
    width, height, pad = 720.0, 220.0, 28.0

    def y(value):
        return round(height - pad - min(value, ceiling) / top * (height - 2 * pad), 1)
    span = CHART_DAYS
    slot = width / span
    parts = [f'<line class="axis" x1="0" y1="{height - pad}" x2="{width}" y2="{height - pad}"/>']
    for d, v in sorted(days.items()):
        x = day_x(d, first, span, width)
        parts.append(f'<rect class="band" x="{x + 1}" y="{y(v["high"])}" width="{round(slot - 2, 1)}" height="{max(1, round(y(v["low"]) - y(v["high"]), 1))}">'
                     f'<title>{day_date(d)}: {plain_money(v["low"])} to {plain_money(v["high"])}</title></rect>')
    most = max((v["listed"] or 0 for v in days.values()), default=0)
    for d, v in sorted(days.items()):
        if most and v["listed"]:
            bar = round(v["listed"] / most * (pad - 6), 1)
            parts.append(f'<rect class="qty" x="{day_x(d, first, span, width) + 2}" y="{height - pad + 2}" width="{round(slot - 4, 1)}" height="{bar}">'
                         f'<title>{day_date(d)}: {v["listed"]:,} listed at most</title></rect>')
    if item.get("typical"):
        parts.append(f'<line class="typical" x1="0" y1="{y(item["typical"])}" x2="{width}" y2="{y(item["typical"])}"/>')
    points = [(round((d - first) / span * width, 1), y(p), p) for d, p in obs]
    if len(points) > 1:
        parts.append('<path class="scan-line" d="' + " ".join(("M" if n == 0 else "L") + f"{x},{yy}" for n, (x, yy, _) in enumerate(points)) + '"/>')
    parts += [f'<circle class="scan" cx="{x}" cy="{yy}" r="3"><title>{plain_money(p)}</title></circle>' for x, yy, p in points]
    parts.append(f'<text class="tick" x="0" y="{height - 8}">{day_date(first)}</text>'
                 f'<text class="tick" x="{width}" y="{height - 8}" text-anchor="end">{day_date(last)}</text>'
                 f'<text class="tick" x="4" y="{y(top) + 12}">{esc(plain_money(top))}</text>')
    summary = (f"Daily price range over the last {CHART_DAYS} days, with {len(obs)} recorded prices"
               + (f" and the typical price of {plain_money(item['typical'])}" if item.get("typical") else "") + ".")
    return (f'<figure class="price-chart"><svg viewBox="0 0 {int(width)} {int(height)}" role="img" aria-label="{esc(summary)}">{"".join(parts)}</svg>'
            '<figcaption><span class="key band-key"></span> each day\'s lowest to highest cheapest listing · '
            '<span class="key scan-key"></span> recorded prices, in order within each day · <span class="key typical-key"></span> typical price · '
            '<span class="key qty-key"></span> most units listed that day</figcaption>' + event_note(events, first, last) + '</figure>')


def stat(label: str, value: str, note: str = "") -> str:
    return f'<div class="stat"><dt>{esc(label)}</dt><dd>{value}{f"<span class=aside>{note}</span>" if note else ""}</dd></div>'


def item_pattern_block(item: dict) -> str:
    p = item["pattern"]
    if not p:
        return (f'<p class="empty">Collecting: this item\'s own weekday pattern appears once it has {m.ITEM_PATTERN_MIN_DAYS} days of prices. '
                'Time-of-day patterns are measured across the whole market, on the Auction House overview.</p>')
    days = "".join(f'<td class="{heat(p["weekday"].get(d))}">{signed_pct(p["weekday"].get(d))}</td>' for d in range(7))
    return ('<div class="table-wrap"><table class="heatmap"><thead><tr>' + "".join(f'<th scope="col">{d}</th>' for d in m.WEEKDAYS)
            + f'</tr></thead><tbody><tr>{days}</tr></tbody></table></div>'
            f'<p class="aside">Each day\'s lowest price against its middle, over {p["days"]} days; a weekday shows once it has two dates.</p>')


def item_page(site: Site, market: dict, item: dict, ctx: dict) -> str:
    fdb_price = ctx["fdb"].get("prices", {}).get(str(item["id"]))
    recipes = ctx["recipes_by_item"]
    alerts = []
    if item["deal"] and "saving" in item["deal"]:
        if item["deal"]["confidence"] == "low":
            alerts.append(f'<span class="alert note">Recorded {pct(item["deal"]["discount"])} under its usual price, but with too little history '
                          'to trust (or so far under that it\'s probably one mispriced unit)</span>')
        else:
            word = "Exceptional deal" if item["deal"]["exceptional"] else "Deal"
            alerts.append(f'<span class="alert low">{word}: {pct(item["deal"]["discount"])} under its usual price, recorded {scan_time(item["latest_time"])}</span>')
    if item["deal"] and item["deal"].get("vendor_profit"):
        alerts.append(f'<span class="alert vendor">Below vendor price: about {plain_money(item["deal"]["vendor_profit"])} potential profit a unit at the recorded price</span>')
    if item["invest"] and item["confidence"] != "low":
        alerts.append(f'<span class="alert invest">Investment watch: about {plain_money(item["invest"]["margin"])} a unit</span>')
    if item["short"] and item["confidence"] != "low":
        alerts.append(f'<span class="alert move">Short supply: {pct(item["short"]["stock"])} of usual stock, {pct(item["short"]["price"])} over usual price</span>')
    if item["move"] and item["confidence"] != "low":
        alerts.append(f'<span class="alert move">{"Up" if item["move"]["change"] > 0 else "Down"} {abs(item["move"]["change"])}% '
                      f'on its lowest of {nice_date(day_date(item["move"]["day"]))}, the last full day of scans</span>')
    stats = "".join([
        stat("Latest recorded", money(item["latest"]), f'by the upload of {scan_time(item["latest_time"])}{"" if item["fresh"] else ", before the newest day of scans"}' if item["latest_time"] else ""),
        stat("Usual price", money(item["ref"]) if item["ref"] else "Too new", f"middle of its daily lowest prices over the last {m.RECENT_DAYS} days" if item["ref"] else "needs three days of prices"),
        stat("Typical price", money(item["typical"]), "middle of the last seven days' lowest prices"),
        stat("Good price to buy", money(item["good_buy"]) if item["good_buy"] else "needs more history",
             "the usual price less half its usual swing" if item["good_buy"] else f"appears with {m.GOOD_BUY_MIN} or more prices"),
        stat("Steadiness", steadiness(item["volatility"]), "how far the daily price swings over two weeks"),
        stat("Days listed", f'{item["presence_days"]} of {item["presence_of"]}' if item["presence_of"] else "unknown", f"full days of scans in the last {m.RECENT_DAYS}"),
        stat("Usually listed", num(item["listed_median"]) + " at once" if item["listed_median"] is not None else "unknown", "the most seen on sale in a day, middle value"),
        stat("Daily low changed", pct(item["churn"]) or "too few days", "how often its lowest price differed from one day to the next"),
        stat("Vendor pays", money(item["vendor_sell"]) if item["vendor_sell"] else "unknown", "from ForeverDB" if item["vendor_sell"] else ""),
        stat("Other players' scans", money(fdb_price["median"]) if fdb_price else "none", f"ForeverDB players' median, {esc(fdb_price['latest'])}" if fdb_price else ""),
    ])
    invest = ""
    if item["invest"] and item["confidence"] != "low":
        i = item["invest"]
        invest = (f'<section class="ah-block" id="estimate"><h2>Investment estimate</h2><p>Buy at {money(item["latest"])}; if it sells again at its usual '
                  f'{money(item["ref"])}, the Auction House keeps {round(m.AH_CUT * 100)}% and you keep about {money(int(item["ref"] * (1 - m.AH_CUT)))}: '
                  f'a margin of {money(i["margin"])} a unit ({pct(i["roi"])} on what you paid). It\'s listed on {pct(item["presence"])} of recent days. '
                  'An estimate from prices and listings; the data holds no sales.</p></section>')
    last = market["last_day"]
    daily = "".join(f'<tr><th scope="row">{nice_date(day_date(d))}</th><td class="num">{money(v["low"])}</td><td class="num">{money(v["high"])}</td>'
                    f'<td class="num">{num(v["listed"])}</td></tr>'
                    for d, v in sorted(item["days"].items(), reverse=True) if last is not None and d > last - CHART_DAYS)
    scans = "".join(f'<tr><th scope="row">{scan_time(t)}</th><td class="num">{money(p)}</td></tr>' for t, p, _ in reversed(item["obs"][-m.WINDOW_SCANS:]))
    made = "".join(f'<li>{esc(r["name"])} <span class="aside">{esc(prof)}, skill {esc(r["skill"])}</span></li>' for prof, r in recipes["makes"].get(item["id"], []))
    used = "".join(f'<li>{esc(r["name"])} <span class="aside">{esc(prof)}</span></li>' for prof, r in recipes["uses"].get(item["id"], [])[:12])
    category = f'{esc(item["category"]["class"])}' + (f' · {esc(item["category"]["subclass"])}' if item["category"].get("subclass") else "") if item.get("category") else ""
    lede = f'{category + " · " if category else ""}{esc(market["name"])}, {esc(market["environment_label"])} Auction House.'
    body = (f'<section class="page-body item-page">'
            + (f'<p class="alerts">{"".join(alerts)}</p>' if alerts else "")
            + f'<dl class="stats">{stats}</dl>'
            + f'<section class="ah-block" id="chart"><h2>Price over the last {CHART_DAYS} days</h2>{chart(item, market, ctx["events"])}</section>'
            + invest
            + f'<section class="ah-block" id="pattern"><h2>By weekday</h2>{item_pattern_block(item)}</section>'
            + (f'<section class="ah-block" id="recipes"><h2>Recipes</h2>'
               + (f'<h3>Made by</h3><ul>{made}</ul>' if made else "") + (f'<h3>Used in</h3><ul>{used}</ul>' if used else "")
               + '<p class="aside">Recipes: <a href="https://foreverdb.net">Data from ForeverDB.net</a>.</p></section>' if made or used else "")
            + f'<section class="ah-block" id="history"><h2>Daily prices</h2>'
            + (f'<div class="table-wrap"><table class="ah-list"><thead><tr><th scope="col">Day</th><th scope="col" class="num">Lowest</th>'
               f'<th scope="col" class="num">Highest</th><th scope="col" class="num">Most listed</th></tr></thead><tbody>{daily}</tbody></table></div>' if daily else '<p class="empty">No recent days.</p>')
            + '</section>'
            + (f'<section class="ah-block" id="scans"><h2>Recorded prices</h2><p class="aside">Each upload in which this item was new to the day or changed, with the upload\'s time.</p><div class="table-wrap"><table class="ah-list"><thead><tr><th scope="col">Scan</th>'
               f'<th scope="col" class="num">Cheapest listing</th></tr></thead><tbody>{scans}</tbody></table></div></section>' if scans else "")
            + f'<p class="elsewhere-line"><a href="{FOREVERDB}/item/{esc(item["id"])}" target="_blank" rel="noopener">{esc(item["name"])} on ForeverDB</a> · '
              f'<a href="{site.base}prices/{market["slug"]}/">All {esc(market["name"])} prices</a></p>'
            + '</section>')
    return layout(site, f'{item["name"]} price', page_head(item["name"], lede, (("Auction House", f"{site.base}prices/"), (market["name"], f"{site.base}prices/{market['slug']}/")))
                  + body, active="prices", path=f"prices/{market['slug']}/item/{item_slug(item['key'])}/",
                  description=f'{item["name"]} on the {market["name"]} Auction House in World of Warcraft: Forever: latest and usual price, daily history and patterns.')

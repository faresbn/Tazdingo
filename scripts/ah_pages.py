"""The Auction House pages: the dashboard blocks, item pages and their charts.

The measures come from scripts/market.py; this module only presents them. Every list
says when its scan was taken, and every page says plainly that the data holds prices and
listings, never sales.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

import market as m
from auctionator import DAY_ZERO, day_date
from pages import (FOREVERDB, Site, badge, change, esc, layout, money, nice_date, page_head, plain_money, steadiness)

DAY_ZERO_EPOCH = datetime(DAY_ZERO.year, DAY_ZERO.month, DAY_ZERO.day, tzinfo=timezone.utc).timestamp()
CHART_DAYS = 30
LIST_ROWS = 12


def item_slug(key: str) -> str:
    return key if key.isdigit() else re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


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
    return (f'<p class="scan-note">{beta} Newest upload: {scan_time(ah["newest"])}. Lists show what that scan and the ones before it recorded, with each sighting\'s time. '
            f'{ah["scans_in_window"]:,} scan{"s" if ah["scans_in_window"] != 1 else ""} in the current window.</p>')


# --- Lists ---------------------------------------------------------------------------------

def table(head: list[str], rows: list[str], caption: str = "") -> str:
    cells = "".join(f'<th scope="col"{" class=num" if h.startswith("#") else ""}>{esc(h.lstrip("#"))}</th>' for h in head)
    return (f'<div class="table-wrap"><table class="ah-list">{f"<caption>{caption}</caption>" if caption else ""}'
            f'<thead><tr>{cells}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def deals_block(site: Site, market: dict, ah: dict, limit: int = LIST_ROWS, heading: str = "h2") -> str:
    rows = [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
            f'<td class="num">{money(i["ref"])}</td><td class="num"><span class="change down">−{pct(i["deal"]["discount"])}</span></td>'
            f'<td class="num">{money(i["deal"]["saving"])}</td><td>{confidence(i["deal"]["confidence"])}</td><td>{scan_time(i["latest_time"])}</td></tr>' for i in ah["deals"][:limit]]
    body = (table(["Item", "#Seen at", "#Usual", "#Below usual", "#Saving a unit", "Confidence", "Seen"], rows) if rows
            else '<p class="empty">Nothing is listed unusually low in the newest scan.</p>')
    if ah["deals_hidden"]:
        body += (f'<p class="aside">{ah["deals_hidden"]} more listed far below usual but with too little history to trust, '
                 'or so far below (90%+) that it\'s probably one mispriced unit.</p>')
    return (f'<section class="ah-block" id="deals"><{heading}>Seen unusually low</{heading}>'
            f'<p class="aside">Seen at least {round(m.DEAL_DISCOUNT * 100)}% under the item\'s usual price on the newest day of scans, '
            'and further under it than the item normally swings. Each row shows when it was seen; a cheap listing may be gone within minutes.</p>'
            f'{body}</section>')


def confidence(level: str) -> str:
    return f'<span class="badge conf-{esc(level)}" title="How much history the usual price rests on">{esc(level.capitalize())}</span>'


def short_block(site: Site, market: dict, ah: dict, limit: int = LIST_ROWS, heading: str = "h2") -> str:
    rows = [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
            f'<td class="num"><span class="change up">+{pct(i["short"]["price"])}</span></td>'
            f'<td class="num">{pct(i["short"]["stock"])}</td></tr>' for i in ah["short"][:limit]]
    if not rows:
        return ""
    return (f'<section class="ah-block" id="short"><{heading}>Short supply</{heading}>'
            f'<p class="aside">Priced at least {round((m.SHORT_PRICE - 1) * 100)}% over usual while the most units listed on the last full day '
            f'fell to half its usual level or less: a sign of a shortage, and of a chance to sell.</p>'
            f'{table(["Item", "#Seen at", "#Over usual", "#Stock against usual"], rows)}</section>')


def index_chart(ah: dict, events: list[dict], heading: str = "h2") -> str:
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
    marks = []
    for event in events:
        day = (datetime.fromisoformat(event["at"].replace("Z", "+00:00")).timestamp() - DAY_ZERO_EPOCH) / 86400
        if first <= day <= last:
            marks.append(f'<line class="event" x1="{x(day)}" y1="0" x2="{x(day)}" y2="{height - pad}"/><text class="event-label" x="{x(day) + 4}" y="12">{esc(event["label"])}</text>')
    dots = "".join(f'<circle class="scan" cx="{x(d)}" cy="{y(v)}" r="2.5"><title>{day_date(d)}: {v}</title></circle>' for d, v, _ in series)
    svg = (f'<svg viewBox="0 0 {int(width)} {int(height)}" role="img" aria-label="Market price index from {day_date(first)} to {day_date(last)}">'
           f'<line class="typical" x1="0" y1="{y(100)}" x2="{width}" y2="{y(100)}"/><path class="scan-line" d="{path}"/>{dots}{"".join(marks)}'
           f'<text class="tick" x="0" y="{height - 6}">{day_date(first)}</text><text class="tick" x="{width}" y="{height - 6}" text-anchor="end">{day_date(last)}</text>'
           f'<text class="tick" x="4" y="{y(high) + 10}">{high:.0f}</text><text class="tick" x="4" y="{y(low) - 3}">{low:.0f}</text></svg>')
    return (f'<section class="ah-block" id="index"><{heading}>Market index</{heading}>'
            '<p class="aside">Each day, the middle of every item\'s lowest price measured against its own usual level: 100 is normal, 105 means '
            'prices across the market sat 5% higher. Unfinished and partial-scan days are left out. Event lines mark launch and raid openings.</p>'
            f'<figure class="price-chart">{svg}</figure></section>')


def vendor_block(site: Site, market: dict, ah: dict, limit: int = LIST_ROWS, heading: str = "h2") -> str:
    rows = [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
            f'<td class="num">{money(i["vendor_sell"])}</td><td class="num">{money(i["deal"]["vendor_profit"])}</td><td>{scan_time(i["latest_time"])}</td></tr>'
            for i in ah["vendor"][:limit]]
    if not rows:
        return ""
    return (f'<section class="ah-block" id="vendor"><{heading}>Below vendor price</{heading}>'
            '<p class="aside">Seen for less than a vendor pays for it: if it\'s still there, buy it and sell it to any vendor. '
            'Vendor prices: <a href="https://foreverdb.net">Data from ForeverDB.net</a>.</p>'
            f'{table(["Item", "#Seen at", "#Vendor pays", "#Profit a unit", "Seen"], rows)}</section>')


def invest_block(site: Site, market: dict, ah: dict, limit: int = LIST_ROWS, heading: str = "h2") -> str:
    rows = [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["latest"])}</td>'
            f'<td class="num">{money(i["ref"])}</td><td class="num">{money(i["invest"]["margin"])}</td>'
            f'<td class="num">{pct(i["invest"]["roi"])}</td><td>{steadiness(i["volatility"])}</td>'
            f'<td class="num">{pct(i["presence"])}</td></tr>' for i in ah["invest"][:limit]]
    body = (table(["Item", "#Seen at", "#Usual", "#Margin a unit", "#Return", "Steadiness", "#Days listed"], rows) if rows
            else '<p class="empty">No item is cheap enough against its own history right now.</p>')
    return (f'<section class="ah-block" id="invest"><{heading}>Investment watch</{heading}>'
            f'<p class="aside">Seen in the cheapest quarter of its last {m.WINDOW_DAYS} days, listed on most of them, usually several at once, and not volatile. '
            f'The margin assumes it sells again at its usual price, less the {round(m.AH_CUT * 100)}% Auction House cut. '
            'An estimate from the price spread, not proven demand: the data shows prices and listings, not sales.</p>'
            f'{body}</section>')


def movers_block(site: Site, market: dict, ah: dict, limit: int = 8, heading: str = "h2") -> str:
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
                     + (f'<div><h3>Rising in the last day</h3>{table(["Item", "#Now", "#Day before", "#Change"], rows(ah["rising"]))}</div>' if ah["rising"] else "")
                     + (f'<div><h3>Falling in the last day</h3>{table(["Item", "#Now", "#Day before", "#Change"], rows(ah["falling"]))}</div>' if ah["falling"] else "")
                     + '</div>')
    if weekly_up or weekly_down:
        parts.append('<div class="ah-cols">'
                     + (f'<div><h3>Rising this week</h3>{table(["Item", "#Typical", "#Week on week"], weekly(weekly_up))}</div>' if weekly_up else "")
                     + (f'<div><h3>Falling this week</h3>{table(["Item", "#Typical", "#Week on week"], weekly(weekly_down))}</div>' if weekly_down else "")
                     + '</div>')
    body = "".join(parts) or ('<p class="empty">Not enough scans yet. The last day\'s movers need three scans in the day before the newest; '
                              'the weekly ones need three days of prices in each of the last two weeks.</p>')
    return (f'<section class="ah-block" id="movers"><{heading}>Movers</{heading}>'
            f'<p class="aside">The last day compares the newest scan with the middle of the item\'s scans over the {m.MOVE_HOURS} hours before it. '
            'The week compares the middle of the last seven days\' lowest prices with the seven before.</p>'
            f'{body}</section>')


def reliable_block(site: Site, market: dict, ah: dict, limit: int = LIST_ROWS, heading: str = "h2") -> str:
    rows = [f'<tr><th scope="row">{item_anchor(site, market, i)}</th><td class="num">{money(i["typical"])}</td>'
            f'<td class="num">{pct(i["presence"])}</td><td class="num">{num(i["listed_median"])}</td>'
            f'<td class="num">{pct(i["churn"])}</td></tr>' for i in ah["reliable"][:limit]]
    if not rows:
        return ""
    return (f'<section class="ah-block" id="reliable"><{heading}>Always on the market</{heading}>'
            '<p class="aside">The data holds no sales, so this is the closest honest measure of what\'s always available: items listed on nearly every day, '
            'how many are usually up at once, and how often the cheapest listing changed between sightings (from sales, new listings, cancellations or expiries alike).</p>'
            f'{table(["Item", "#Typical", "#Days listed", "#Usually listed", "#Cheapest changed"], rows)}</section>')


def heat(index: float | None) -> str:
    if index is None:
        return "heat-none"
    delta = index - 1
    return ("heat-low2" if delta <= -0.06 else "heat-low1" if delta <= -0.02 else
            "heat-high2" if delta >= 0.06 else "heat-high1" if delta >= 0.02 else "heat-mid")


def signed_pct(index: float | None) -> str:
    return "…" if index is None else f"{(index - 1) * 100:+.0f}%"


def patterns_block(ah: dict, heading: str = "h2") -> str:
    p = ah["patterns"]
    head = "".join(f'<th scope="col">{label}</th>' for label in m.BAND_LABELS)
    rows = []
    for d, name in enumerate(m.WEEKDAYS):
        cells = "".join(f'<td class="{heat(p["cells"].get(f"{d}-{b}", {}).get("index"))}">{signed_pct(p["cells"].get(f"{d}-{b}", {}).get("index"))}</td>'
                        for b in range(6))
        rows.append(f'<tr><th scope="row">{name}</th>{cells}</tr>')
    ready = any(c["index"] is not None for c in p["cells"].values())
    note = ("" if ready else f'<p class="empty">Collecting: a weekday and time band shows once {m.PATTERN_MIN_ITEMS} items have prices in it '
                             f'on at least {m.PATTERN_MIN_DATES} different dates. Scans spread across the day and the week fill this in.</p>')
    return (f'<section class="ah-block" id="patterns"><{heading}>When prices are lowest</{heading}>'
            '<p class="aside">How far prices sit above or below each item\'s own middle price, by weekday and four-hour band '
            '(hours in UTC<span data-utc-offset></span>). Green cells are cheaper times to buy, warmer cells better times to sell. '
            'It can only reflect the times scans were taken, so a band nobody scans in stays empty.</p>'
            f'{note}<div class="table-wrap"><table class="heatmap"><thead><tr><td></td>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>')


def dashboard(site: Site, market: dict, ah: dict, heading: str = "h2", events: list | None = None) -> str:
    events = events or []
    return (scan_note(market, ah) + deals_block(site, market, ah, heading=heading) + vendor_block(site, market, ah, heading=heading)
            + invest_block(site, market, ah, heading=heading) + short_block(site, market, ah, heading=heading)
            + movers_block(site, market, ah, heading=heading) + reliable_block(site, market, ah, heading=heading)
            + index_chart(ah, events, heading=heading) + patterns_block(ah, heading=heading))


def home_block(site: Site, market: dict, ah: dict) -> str:
    """The homepage's Auction House card: alerts first, then investments and movers."""
    def mini(title, items, value):
        if not items:
            return ""
        rows = "".join(f'<li>{item_anchor(site, market, i)} <span class="value">{value(i)}</span></li>' for i in items[:4])
        return f'<h3 class="mini-title">{title}</h3><ul class="mini-list">{rows}</ul>'
    alerts = mini("Below vendor price", ah["vendor"], lambda i: money(i["latest"]) + f' <span class="aside">vendor pays {plain_money(i["vendor_sell"])}</span>')
    alerts += mini("Seen unusually low", ah["deals"], lambda i: money(i["latest"]) + f' <span class="change down">−{pct(i["deal"]["discount"])}</span>')
    invest = mini("Investment watch", ah["invest"], lambda i: f'+{plain_money(i["invest"]["margin"])} a unit')
    moving = mini("Moving over a day", (ah["rising"] + ah["falling"]), lambda i: change(i["move"]["change"]))
    return (alerts or '<p class="empty">No price alerts from the newest day of scans.</p>') + invest + moving + scan_note(market, ah)


# --- Item pages ----------------------------------------------------------------------------

def day_x(day: float, first: int, span: int, width: float) -> float:
    return round((day - first) / span * width, 1)


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
    # Each sighting sits inside its own Auctionator day's band, spread in the order it was seen.
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
    for event in events:
        day = (datetime.fromisoformat(event["at"].replace("Z", "+00:00")).timestamp() - DAY_ZERO_EPOCH) / 86400
        if first <= day <= last + 1:
            x = day_x(day, first, span, width)
            parts.append(f'<line class="event" x1="{x}" y1="0" x2="{x}" y2="{height - pad}"/><text class="event-label" x="{x + 4}" y="12">{esc(event["label"])}</text>')
    parts.append(f'<text class="tick" x="0" y="{height - 8}">{day_date(first)}</text>'
                 f'<text class="tick" x="{width}" y="{height - 8}" text-anchor="end">{day_date(last)}</text>'
                 f'<text class="tick" x="4" y="{y(top) + 12}">{esc(plain_money(top))}</text>')
    summary = (f"Daily price range over the last {CHART_DAYS} days, with {len(obs)} sightings"
               + (f" and the typical price of {plain_money(item['typical'])}" if item.get("typical") else "") + ".")
    return (f'<figure class="price-chart"><svg viewBox="0 0 {int(width)} {int(height)}" role="img" aria-label="{esc(summary)}">{"".join(parts)}</svg>'
            '<figcaption><span class="key band-key"></span> each day\'s lowest to highest cheapest listing · '
            '<span class="key scan-key"></span> the cheapest listing at each sighting · <span class="key typical-key"></span> typical price · '
            '<span class="key qty-key"></span> most units listed that day</figcaption></figure>')


def stat(label: str, value: str, note: str = "") -> str:
    return f'<div class="stat"><dt>{esc(label)}</dt><dd>{value}{f"<span class=aside>{note}</span>" if note else ""}</dd></div>'


def item_pattern_block(item: dict) -> str:
    p = item["pattern"]
    if not p:
        return (f'<p class="empty">Collecting: this item has {len(item["obs"])} sighting{"s" if len(item["obs"]) != 1 else ""}; '
                f'its own time-of-day and weekday pattern appears at {m.ITEM_PATTERN_MIN_OBS} across at least {m.ITEM_PATTERN_MIN_DAYS} days.</p>')
    days = "".join(f'<td class="{heat(p["weekday"].get(d))}">{signed_pct(p["weekday"].get(d))}</td>' for d in range(7))
    bands = "".join(f'<td class="{heat(p["band"].get(b))}">{signed_pct(p["band"].get(b))}</td>' for b in range(6))
    return ('<div class="table-wrap"><table class="heatmap"><thead><tr>' + "".join(f'<th scope="col">{d}</th>' for d in m.WEEKDAYS)
            + f'</tr></thead><tbody><tr>{days}</tr></tbody></table></div>'
            '<div class="table-wrap"><table class="heatmap"><thead><tr>' + "".join(f'<th scope="col">{b}</th>' for b in m.BAND_LABELS)
            + f'</tr></thead><tbody><tr>{bands}</tr></tbody></table></div>'
            f'<p class="aside">From {p["n"]:,} sightings over {p["days"]} days; hours in UTC. A weekday or band shows once it has prices on two dates.</p>')


def item_page(site: Site, market: dict, item: dict, ctx: dict) -> str:
    fdb_price = ctx["fdb"].get("prices", {}).get(str(item["id"]))
    recipes = ctx["recipes_by_item"]
    alerts = []
    if item["deal"] and "saving" in item["deal"]:
        if item["deal"]["confidence"] == "low":
            alerts.append(f'<span class="alert note">Seen {pct(item["deal"]["discount"])} under its usual price, but with too little history '
                          'to trust (or so far under that it\'s probably one mispriced unit)</span>')
        else:
            alerts.append(f'<span class="alert low">Seen unusually low: {pct(item["deal"]["discount"])} under its usual price, {scan_time(item["latest_time"])}</span>')
    if item["deal"] and item["deal"].get("vendor_profit"):
        alerts.append(f'<span class="alert vendor">Below vendor price: {plain_money(item["deal"]["vendor_profit"])} profit a unit</span>')
    if item["invest"] and item["confidence"] != "low":
        alerts.append(f'<span class="alert invest">Investment watch: about {plain_money(item["invest"]["margin"])} a unit</span>')
    if item["short"] and item["confidence"] != "low":
        alerts.append(f'<span class="alert move">Short supply: {pct(item["short"]["stock"])} of usual stock, {pct(item["short"]["price"])} over usual price</span>')
    if item["move"]:
        alerts.append(f'<span class="alert move">{"Up" if item["move"]["change"] > 0 else "Down"} {abs(item["move"]["change"])}% in the last day</span>')
    basis = {"scans": f"middle of its scan prices over the last {m.WINDOW_DAYS} days",
             "days": f"middle of its daily lowest prices over the last {m.RECENT_DAYS} days"}.get(item["ref_basis"], "not enough history yet")
    stats = "".join([
        stat("Latest sighting", money(item["latest"]), f'{scan_time(item["latest_time"])}{"" if item["fresh"] else ", before the newest day of scans"}' if item["latest_time"] else ""),
        stat("Usual price", money(item["ref"]) if item["ref"] else "Too new", basis),
        stat("Typical price", money(item["typical"]), "middle of the last seven days' lowest prices"),
        stat("Good price to buy", money(item["good_buy"]) if item["good_buy"] else "needs more history",
             "the usual price less half its usual swing" if item["good_buy"] else f"appears with {m.GOOD_BUY_MIN} or more prices"),
        stat("Steadiness", steadiness(item["volatility"]), "how far the daily price swings over two weeks"),
        stat("Days listed", f'{item["presence_days"]} of {item["presence_of"]}' if item["presence_of"] else "unknown", f"full days of scans in the last {m.RECENT_DAYS}"),
        stat("Usually listed", num(item["listed_median"]) + " at once" if item["listed_median"] is not None else "unknown", "the most seen on sale in a day, middle value"),
        stat("Cheapest listing changed", pct(item["churn"]) or "too few sightings", "between one sighting and the next: sales, new listings, cancellations and expiries all change it"),
        stat("Vendor pays", money(item["vendor_sell"]) if item["vendor_sell"] else "unknown", "from ForeverDB" if item["vendor_sell"] else ""),
        stat("Other players' scans", money(fdb_price["median"]) if fdb_price else "none", f"ForeverDB players' median, {esc(fdb_price['latest'])}" if fdb_price else ""),
    ])
    invest = ""
    if item["invest"]:
        i = item["invest"]
        invest = (f'<section class="ah-block" id="estimate"><h2>Investment estimate</h2><p>Buy at {money(item["latest"])}; if it sells again at its usual '
                  f'{money(item["ref"])}, the Auction House keeps {round(m.AH_CUT * 100)}% and you keep about {money(item["ref"] - round(item["ref"] * m.AH_CUT))}: '
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
            + f'<section class="ah-block" id="pattern"><h2>Time of day and weekday</h2>{item_pattern_block(item)}</section>'
            + (f'<section class="ah-block" id="recipes"><h2>Recipes</h2>'
               + (f'<h3>Made by</h3><ul>{made}</ul>' if made else "") + (f'<h3>Used in</h3><ul>{used}</ul>' if used else "")
               + '<p class="aside">Recipes: <a href="https://foreverdb.net">Data from ForeverDB.net</a>.</p></section>' if made or used else "")
            + f'<section class="ah-block" id="history"><h2>Daily prices</h2>'
            + (f'<div class="table-wrap"><table class="ah-list"><thead><tr><th scope="col">Day</th><th scope="col" class="num">Lowest</th>'
               f'<th scope="col" class="num">Highest</th><th scope="col" class="num">Most listed</th></tr></thead><tbody>{daily}</tbody></table></div>' if daily else '<p class="empty">No recent days.</p>')
            + '</section>'
            + (f'<section class="ah-block" id="scans"><h2>Sightings</h2><p class="aside">Each upload where this item was new to the day or changed.</p><div class="table-wrap"><table class="ah-list"><thead><tr><th scope="col">Scan</th>'
               f'<th scope="col" class="num">Cheapest listing</th></tr></thead><tbody>{scans}</tbody></table></div></section>' if scans else "")
            + f'<p class="elsewhere-line"><a href="{FOREVERDB}/item/{esc(item["id"])}" target="_blank" rel="noopener">{esc(item["name"])} on ForeverDB</a> · '
              f'<a href="{site.base}prices/{market["slug"]}/">All {esc(market["name"])} prices</a></p>'
            + '</section>')
    return layout(site, f'{item["name"]} price', page_head(item["name"], lede, (("Auction House", f"{site.base}prices/"), (market["name"], f"{site.base}prices/{market['slug']}/")))
                  + body, active="prices", path=f"prices/{market['slug']}/item/{item_slug(item['key'])}/",
                  description=f'{item["name"]} on the {market["name"]} Auction House in World of Warcraft: Forever: latest and usual price, daily history and patterns.')

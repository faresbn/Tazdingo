"""Auction House analytics: what's cheap now, what's worth buying to resell, what's moving,
how reliably things are listed, and how prices move through the day and week.

Everything works from one market's items as build.py assembles them: per item the daily
low/high/most-listed history (`days`), every timestamped scan price (`obs`), and the
typical price and steadiness from build.summarise. The data has no sales: Auctionator
records prices and the most units listed each day, never what sold, so "how well it
sells" is measured as listing activity and labelled that way.

The thresholds below are first guesses, kept in one place to tune once live scans exist.
"""
from __future__ import annotations

import statistics
from datetime import datetime, timezone

WINDOW_DAYS = 30            # the scan window (and the 30-scan rule in market_store)
WINDOW_SCANS = 30
MIN_OBS = 6                 # scan prices needed for a scan-based reference...
MIN_OBS_DAYS = 2            # ...spread over at least this many days
FALLBACK_DAYS = 14          # otherwise: median daily low over this many days...
MIN_FALLBACK_DAYS = 3       # ...needing at least this many days with records
DEAL_DISCOUNT = 0.30        # unusually low: at least 30% under the reference
DEAL_SPREAD = 3.5           # and a robust (median-absolute-deviation) z-score of 3.5 or more, when it varies
DEAL_CAP = 0.9              # 90%+ under usual is usually one mispriced unit: shown, but at low confidence
DEAL_MIN_REF = 100          # ignore items usually worth under 1 silver
AH_CUT = 0.05               # the Auction House keeps 5% of a sale
INVEST_PERCENTILE = 0.25    # investment: bought at or under the item's 25th-percentile day
INVEST_MIN_MARGIN = 100     # at least 1 silver a unit after the cut
INVEST_MIN_PRESENCE = 0.6   # listed on at least 60% of the days in its window
RISK = {"steady": 1.0, "moving": 0.7, "volatile": 0.4, None: 0.5}  # investment ranking: steadier is safer
SHORT_PRICE = 1.2           # short supply: at least 20% over usual...
SHORT_STOCK = 0.5           # ...with at most half the units usually listed
GOOD_BUY_MIN = 8            # a suggested good-buy price needs this many values (The Undermine Journal's rule)
INDEX_MIN_ITEMS = 20        # a market-index day needs this many items
PARTIAL_DAY = 0.5           # a day whose records cover under half the usual number of items was a partial scan
MOVE_HOURS = 24             # movers: the latest scan against the previous 24 hours...
MOVE_MIN_SCANS = 3          # ...of at least three scans
MOVE_MIN_BASE = 50
MOVE_MIN_CHANGE = 0.15
PATTERN_MIN_OBS = 20        # a pattern cell shows once it has this many observations...
PATTERN_MIN_SCANS = 3       # ...from at least this many separate scans
ITEM_PATTERN_MIN_OBS = 24   # an item's own pattern needs this many scans
BAND_LABELS = ("00–04", "04–08", "08–12", "12–16", "16–20", "20–24")  # UTC hours
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def median(values):
    return statistics.median(values) if values else None


def mad(values, centre):
    return statistics.median(abs(v - centre) for v in values) if values else 0


def percentile(values, share):
    ordered = sorted(values)
    if not ordered:
        return None
    return ordered[min(len(ordered) - 1, max(0, round(share * (len(ordered) - 1))))]


def band_of(hour: int) -> int:
    return hour // 4


def utc(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, timezone.utc)


# --- Per item ------------------------------------------------------------------------------

def window(market: dict) -> tuple[int | None, int | None]:
    """(newest scan time, start of the window): 30 days back, or the 30th-newest scan if earlier."""
    times = sorted({t for item in market["items"] for t, _ in item["obs"]})
    if not times:
        return None, None
    newest = times[-1]
    start = min(newest - WINDOW_DAYS * 86400, times[-WINDOW_SCANS] if len(times) >= WINDOW_SCANS else times[0])
    return newest, start


def reference(item: dict, start: int | None, last_day: int | None) -> tuple[int | None, str | None, list]:
    """The item's usual price: the median of its scan prices in the window when it has enough,
    otherwise the median daily low over 14 days. Returns (price, basis, the values used)."""
    prices = [m for t, m in item["obs"] if start is not None and t >= start]
    days = {utc(t).date() for t, _ in item["obs"] if start is not None and t >= start}
    if len(prices) >= MIN_OBS and len(days) >= MIN_OBS_DAYS:
        return int(median(prices)), "scans", prices
    if last_day is None:
        return None, None, []
    lows = [v["low"] for d, v in item["days"].items() if last_day - FALLBACK_DAYS < d <= last_day]
    if len(lows) >= MIN_FALLBACK_DAYS:
        return int(median(lows)), "days", lows
    return None, None, []


def presence(item: dict, last_day: int | None, days: int = FALLBACK_DAYS) -> float | None:
    """Share of the last `days` days (from the market's newest) on which the item was listed."""
    if last_day is None:
        return None
    first = max(last_day - days + 1, min(item["days"], default=last_day))
    span = last_day - first + 1
    return sum(1 for d in item["days"] if first <= d <= last_day) / span if span > 0 else None


def price_churn(item: dict, start: int | None) -> float | None:
    """How often the item's minimum price changed between consecutive scans that saw it."""
    prices = [m for t, m in item["obs"] if start is not None and t >= start]
    if len(prices) < 3:
        return None
    return sum(1 for a, b in zip(prices, prices[1:]) if a != b) / (len(prices) - 1)


def confidence(item: dict, basis: str | None, values: list) -> str:
    """High, medium or low, from how much history the usual price rests on and how
    reliably the item is listed (after goldcap.gg's tiers). Low is hidden from lists."""
    listed = item["listed_median"] or 0
    if basis == "scans" and len(values) >= 10 and (item["presence"] or 0) >= 0.6 and listed >= 3:
        return "high"
    if len(values) >= 5 and (item["presence"] or 0) >= 0.4:
        return "medium"
    return "low"


def partial_days(items: list[dict]) -> set[int]:
    """Days when only some items were scanned (a few searches rather than a full scan): their
    "most listed" and lowest prices aren't comparable with full days."""
    coverage = {}
    for item in items:
        for d in item["days"]:
            coverage[d] = coverage.get(d, 0) + 1
    usual = median(list(coverage.values())) or 0
    return {d for d, n in coverage.items() if n < usual * PARTIAL_DAY}


def analyse_item(item: dict, newest: int | None, start: int | None, last_day: int | None, vendor: dict, partial: frozenset = frozenset()) -> None:
    ref, basis, values = reference(item, start, last_day)
    latest_time, latest = (item["obs"][-1] if item["obs"] else (None, item.get("price")))
    fresh = newest is not None and latest_time == newest
    recent = [v["listed"] for d, v in item["days"].items() if v["listed"] is not None and last_day is not None and last_day - FALLBACK_DAYS < d]
    item.update(ref=ref, ref_basis=basis, fresh=fresh, latest=latest, latest_time=latest_time,
                presence=presence(item, last_day), churn=price_churn(item, start), listed_median=median(recent),
                vendor_sell=vendor.get(item["id"]), deal=None, invest=None, move=None, short=None, good_buy=None)
    item["confidence"] = confidence(item, basis, values)
    if ref and len(values) >= GOOD_BUY_MIN:
        item["good_buy"] = int(ref - 0.5 * 1.4826 * mad(values, ref))
    if not fresh or latest is None:
        return
    if ref and ref >= DEAL_MIN_REF and latest <= ref * (1 - DEAL_DISCOUNT):
        spread = 1.4826 * mad(values, ref)
        if spread == 0 or (ref - latest) / spread >= DEAL_SPREAD:
            discount = 1 - latest / ref
            item["deal"] = {"saving": ref - latest, "discount": discount,
                            "confidence": "low" if discount >= DEAL_CAP else item["confidence"]}
    # Stock is compared on the last finished day: the newest day's "most listed" only covers
    # the scans so far, so it reads low until the day ends.
    finished = max((d for d in item["days"] if last_day is not None and d < last_day and d not in partial), default=None)
    stock = item["days"].get(finished, {}).get("listed") if finished is not None else None
    earlier = median([v["listed"] for d, v in item["days"].items()
                      if v["listed"] is not None and d not in partial and finished is not None and finished - FALLBACK_DAYS < d < finished])
    if ref and stock is not None and earlier and latest >= ref * SHORT_PRICE and stock <= earlier * SHORT_STOCK:
        item["short"] = {"price": latest / ref - 1, "stock": stock / earlier}
    if item["vendor_sell"] and latest < item["vendor_sell"]:
        item["deal"] = dict(item["deal"] or {}, vendor_profit=item["vendor_sell"] - latest)
    lows = [v["low"] for d, v in item["days"].items() if last_day is not None and last_day - WINDOW_DAYS < d <= last_day]
    floor = percentile(lows, INVEST_PERCENTILE)
    if ref and floor is not None and latest <= floor and (item["presence"] or 0) >= INVEST_MIN_PRESENCE and len(lows) >= MIN_FALLBACK_DAYS:
        margin = int(ref * (1 - AH_CUT)) - latest
        if margin >= INVEST_MIN_MARGIN:
            item["invest"] = {"margin": margin, "roi": margin / latest if latest else None,
                              "score": margin * (item["presence"] or 0) * RISK.get(item.get("volatility"), 0.5)}
    earlier = [m for t, m in item["obs"] if newest is not None and newest - MOVE_HOURS * 3600 <= t < newest]
    if len(earlier) >= MOVE_MIN_SCANS:
        base = median(earlier)
        if base >= MOVE_MIN_BASE and abs(latest / base - 1) >= MOVE_MIN_CHANGE:
            item["move"] = {"change": round((latest / base - 1) * 100), "base": int(base)}


# --- Patterns -----------------------------------------------------------------------------

def patterns(items: list[dict], start: int | None) -> dict:
    """Each scan price divided by its item's window median, gathered by weekday and four-hour
    band (UTC). A cell is the median index across its observations; cells with too few
    observations are reported as None ("collecting")."""
    cells, weekday, band = {}, {}, {}
    for item in items:
        prices = [(t, m) for t, m in item["obs"] if start is not None and t >= start and m > 0]
        centre = median([m for _, m in prices])
        if not centre or len(prices) < 3:
            continue
        for t, m in prices:
            moment = utc(t)
            index = m / centre
            cells.setdefault((moment.weekday(), band_of(moment.hour)), []).append((t, index))
            weekday.setdefault(moment.weekday(), []).append((t, index))
            band.setdefault(band_of(moment.hour), []).append((t, index))

    def summary(pairs):
        values, scans = [v for _, v in pairs], len({t for t, _ in pairs})
        ready = len(values) >= PATTERN_MIN_OBS and scans >= PATTERN_MIN_SCANS
        return {"index": round(median(values), 4) if ready else None, "n": len(values), "scans": scans}
    return {"cells": {f"{d}-{b}": summary(v) for (d, b), v in cells.items()},
            "weekday": {d: summary(v) for d, v in weekday.items()},
            "band": {b: summary(v) for b, v in band.items()},
            "observations": sum(len(v) for v in weekday.values())}


def item_pattern(item: dict, start: int | None) -> dict | None:
    prices = [(t, m) for t, m in item["obs"] if start is not None and t >= start and m > 0]
    if len(prices) < ITEM_PATTERN_MIN_OBS:
        return None
    centre = median([m for _, m in prices])
    weekday, band = {}, {}
    for t, m in prices:
        moment = utc(t)
        weekday.setdefault(moment.weekday(), []).append(m / centre)
        band.setdefault(band_of(moment.hour), []).append(m / centre)
    keep = lambda groups: {k: round(median(v), 4) for k, v in groups.items() if len(v) >= PATTERN_MIN_SCANS}
    return {"weekday": keep(weekday), "band": keep(band), "n": len(prices)}


def market_index(items: list[dict], last_day: int | None, days: int = 60, partial: frozenset = frozenset()) -> list[tuple[int, float, int]]:
    """A whole-market price index: each day, the median across items of that day's lowest
    price over the item's own median lowest price, times 100 (after auctionhouse.fyi's index
    and Saddlebag's price-group deltas). Shows what an event did to prices in general."""
    if last_day is None:
        return []
    first = last_day - days + 1
    ratios = {}
    for item in items:
        # The newest day is left out: its low covers only the scans so far, so it reads high.
        lows = {d: v["low"] for d, v in item["days"].items() if first <= d < last_day and d not in partial and v["low"] > 0}
        if len(lows) < 5:
            continue
        centre = median(list(lows.values()))
        for d, low in lows.items():
            ratios.setdefault(d, []).append(low / centre)
    return [(d, round(median(v) * 100, 1), len(v)) for d, v in sorted(ratios.items()) if len(v) >= INDEX_MIN_ITEMS]


# --- Per market ---------------------------------------------------------------------------

def analyse(market: dict, vendor: dict, categories: dict) -> dict:
    """Fills each item's measures and returns the market's lists."""
    newest, start = window(market)
    last_day = market.get("last_day")
    partial = frozenset(partial_days(market["items"]))
    for item in market["items"]:
        analyse_item(item, newest, start, last_day, vendor, partial)
        item["category"] = categories.get(item["id"])
        item["pattern"] = item_pattern(item, start)
    fresh = [i for i in market["items"] if i["fresh"]]
    scans = sorted({t for i in market["items"] for t, _ in i["obs"]})
    return {
        "newest": newest, "window_start": start, "scans_in_window": sum(1 for t in scans if start is not None and t >= start),
        "deals": sorted((i for i in fresh if i["deal"] and "saving" in i["deal"] and i["deal"]["confidence"] != "low"),
                        key=lambda i: -i["deal"]["saving"]),
        "deals_hidden": sum(1 for i in fresh if i["deal"] and "saving" in i["deal"] and i["deal"]["confidence"] == "low"),
        "short": sorted((i for i in fresh if i["short"] and i["confidence"] != "low"), key=lambda i: i["short"]["stock"]),
        "index": market_index(market["items"], last_day, partial=partial),
        "partial_days": sorted(partial),
        "vendor": sorted((i for i in fresh if i["deal"] and i["deal"].get("vendor_profit")), key=lambda i: -i["deal"]["vendor_profit"]),
        "invest": sorted((i for i in fresh if i["invest"] and i["confidence"] != "low"), key=lambda i: -i["invest"]["score"]),
        "rising": sorted((i for i in fresh if i["move"] and i["move"]["change"] > 0), key=lambda i: -i["move"]["change"]),
        "falling": sorted((i for i in fresh if i["move"] and i["move"]["change"] < 0), key=lambda i: i["move"]["change"]),
        "reliable": sorted((i for i in market["current"] if (i["presence"] or 0) >= 0.8 and i.get("typical")),
                           key=lambda i: (-(i["presence"] or 0), -(i["listed_median"] or 0)))[:40],
        "patterns": patterns(market["items"], start),
    }

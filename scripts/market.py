"""Auction House analytics: what was seen cheap, what's worth buying to resell, what's moving,
how reliably things are listed, and how prices move through the day and week.

Everything works from one market's items as build.py assembles them: per item the daily
low/high/most-listed history (`days`, keyed by Auctionator's day); its recorded prices
(`obs`: upload time, price, Auctionator day; added when the item is new to that day or
changed, timed by the upload, though Auctionator may have seen it earlier); its full-scan
samples (`full_obs`: every item listed that day, at the time of a new full scan, the only
basis for time-of-day patterns); and the typical price and steadiness from build.summarise.
Recorded prices are changes, not an unbiased sample, so usual prices come from daily lows. The data has no sales: Auctionator records prices and
the most units listed each day, never what sold, so "how well it sells" is measured as
listing activity and labelled that way.

The thresholds below are first guesses, kept in one place to tune once live scans exist.
"""
from __future__ import annotations

import statistics
from datetime import datetime, timezone

WINDOW_DAYS = 30            # the scan window (and the 30-scan rule in market_store)
WINDOW_SCANS = 30
RECENT_DAYS = 14            # the usual price: median daily low over the last 14 full days...
MIN_RECENT_DAYS = 3         # ...needing at least this many days with records
DEAL_DISCOUNT = 0.20        # a deal: recorded at least 20% under the usual price
EXCEPTIONAL_DISCOUNT = 0.30 # exceptional: at least 30% under...
DEAL_SPREAD = 3.5           # ...and a robust (median-absolute-deviation) z-score of 3.5 or more, when it varies
DEAL_CAP = 0.9              # 90%+ under usual is usually one mispriced unit: low confidence
DEAL_MIN_REF = 100          # ignore items usually worth under 1 silver
VENDOR_MIN_PROFIT = 100     # below vendor price: worth flagging at 1 silver a unit or more...
VENDOR_QUALITIES = {"Rare", "Epic", "Legendary"}  # ...and only for rare items or recipes
AH_CUT = 0.05               # the Auction House keeps 5% of a sale
INVEST_PERCENTILE = 0.25    # investment: seen at or under the item's 25th-percentile day
INVEST_MIN_MARGIN = 100     # at least 1 silver a unit after the cut
INVEST_MIN_PRESENCE = 0.6   # listed on at least 60% of the window's full days
INVEST_MIN_LISTED = 3       # and usually at least three on sale: thinly traded items are skipped
RISK = {"steady": 1.0, "moving": 0.7}  # volatile and too-new items are skipped (settled: gold-making tables skip them)
SHORT_PRICE = 1.2           # short supply: at least 20% over usual...
SHORT_STOCK = 0.5           # ...with at most half the units usually listed, on the last full day
GOOD_BUY_MIN = 8            # a suggested good-buy price needs this many values (The Undermine Journal's rule)
MOVE_MIN_BASE = 50          # movers: the latest recorded price against the last full day's lowest
MOVE_MIN_CHANGE = 0.15
PATTERN_MIN_ITEMS = 10      # a market pattern cell shows once this many items have prices in it...
PATTERN_MIN_DATES = 2       # ...on at least two separate dates (one busy afternoon isn't a pattern)
ITEM_PATTERN_MIN_DAYS = 14  # an item's own weekday pattern needs two weeks of days
INDEX_MIN_ITEMS = 20        # a market-index day needs this many items
PARTIAL_DAY = 0.5           # a day covering under half of a full scan's items was a partial scan
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


def utc(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, timezone.utc)


def band_of(hour: int) -> int:
    return hour // 4


# --- The market's frame -------------------------------------------------------------------

def scan_times(market: dict) -> list[int]:
    return sorted({int(datetime.fromisoformat(s["time"].replace("Z", "+00:00")).timestamp()) for s in market["scans"] if s.get("time")})


def window(market: dict) -> tuple[int | None, int | None]:
    """(newest upload's scan time, start of the window): 30 days back, or back to the 30th-newest
    upload if that reaches further."""
    times = scan_times(market)
    if not times:
        return None, None
    newest = times[-1]
    return newest, min(newest - WINDOW_DAYS * 86400, times[-WINDOW_SCANS] if len(times) >= WINDOW_SCANS else times[0])


def partial_days(items: list[dict], full_scan_coverage: list[int] | None = None) -> set[int]:
    """Days when only some items were scanned (a few searches rather than a full scan). A full
    scan's size comes from uploads known to be a full scan's snapshot (their item counts are
    kept in the receipts, so they outlive retention); without any, from the busiest days
    (90th percentile)."""
    coverage = {}
    for item in items:
        for d in item["days"]:
            coverage[d] = coverage.get(d, 0) + 1
    known = list(full_scan_coverage or ())
    full = median(known) if known else (percentile(list(coverage.values()), 0.9) or 0)
    return {d for d, n in coverage.items() if n < full * PARTIAL_DAY}


# --- Per item ------------------------------------------------------------------------------

def reference(item: dict, recent: list[int]) -> tuple[int | None, list]:
    """The item's usual price: the median of its daily lows over the last 14 full days."""
    lows = [item["days"][d]["low"] for d in recent if d in item["days"]]
    return (int(median(lows)), lows) if len(lows) >= MIN_RECENT_DAYS else (None, lows)


def confidence(item: dict, values: list) -> str:
    """High, medium or low, from how many days the usual price rests on and how reliably the
    item is listed (after goldcap.gg's tiers). Low is hidden from lists."""
    listed = item["listed_median"] or 0
    if len(values) >= 10 and (item["presence"] or 0) >= 0.6 and listed >= 3:
        return "high"
    if len(values) >= 5 and (item["presence"] or 0) >= 0.4:
        return "medium"
    return "low"


def daily_change(item: dict, recent: list[int]) -> float | None:
    """How often the item's lowest price differed from one full day to the next it was listed."""
    lows = [item["days"][d]["low"] for d in recent if d in item["days"]]
    if len(lows) < 3:
        return None
    return sum(1 for a, b in zip(lows, lows[1:]) if a != b) / (len(lows) - 1)


def analyse_item(item: dict, frame: dict, vendor: dict) -> None:
    start, newest_day, recent = frame["start"], frame["last_day"], frame["recent"]
    latest_time, latest, latest_day = item["obs"][-1] if item["obs"] else (None, item.get("price"), item.get("price_day"))
    present = [d for d in recent if d in item["days"]]
    listed = [item["days"][d]["listed"] for d in present if item["days"][d]["listed"] is not None]
    item.update(latest=latest, latest_time=latest_time, fresh=latest_day is not None and latest_day == newest_day,
                presence=len(present) / len(recent) if recent else None, presence_days=len(present), presence_of=len(recent),
                listed_median=median(listed), churn=daily_change(item, recent), vendor_sell=vendor.get(item["id"]),
                deal=None, invest=None, move=None, short=None, good_buy=None)
    ref, values = reference(item, recent)
    item.update(ref=ref, confidence=confidence(item, values))
    if ref and len(values) >= GOOD_BUY_MIN:
        item["good_buy"] = int(ref - 0.5 * 1.4826 * mad(values, ref))
    if not item["fresh"] or latest is None or latest_time is None:
        return
    if ref and ref >= DEAL_MIN_REF and latest <= ref * (1 - DEAL_DISCOUNT):
        spread = 1.4826 * mad(values, ref)
        discount = 1 - latest / ref
        item["deal"] = {"saving": ref - latest, "discount": discount,
                        "exceptional": discount >= EXCEPTIONAL_DISCOUNT and (spread == 0 or (ref - latest) / spread >= DEAL_SPREAD),
                        "confidence": "low" if discount >= DEAL_CAP else item["confidence"]}
    category = item.get("category") or {}
    if (item["vendor_sell"] and item["vendor_sell"] - latest >= VENDOR_MIN_PROFIT
            and (category.get("quality") in VENDOR_QUALITIES or category.get("class") == "Recipe")):
        item["deal"] = dict(item["deal"] or {}, vendor_profit=item["vendor_sell"] - latest)
    last_full = frame["last_full"]
    if ref and last_full is not None and item["days"].get(last_full, {}).get("listed") is not None:
        stock = item["days"][last_full]["listed"]
        usual = median([item["days"][d]["listed"] for d in recent if d < last_full and d in item["days"] and item["days"][d]["listed"] is not None])
        if usual and latest >= ref * SHORT_PRICE and stock <= usual * SHORT_STOCK:
            item["short"] = {"price": latest / ref - 1, "stock": stock / usual}
    lows = [item["days"][d]["low"] for d in frame["window_days"] if d in item["days"]]
    floor = percentile(lows, INVEST_PERCENTILE)
    if (ref and floor is not None and latest <= floor and len(lows) >= MIN_RECENT_DAYS and item.get("volatility") in RISK
            and (item["presence"] or 0) >= INVEST_MIN_PRESENCE and (item["listed_median"] or 0) >= INVEST_MIN_LISTED):
        margin = int(ref * (1 - AH_CUT)) - latest
        if margin >= INVEST_MIN_MARGIN:
            item["invest"] = {"margin": margin, "roi": margin / latest if latest else None,
                              "score": margin * item["presence"] * RISK[item["volatility"]]}
    base = item["days"].get(last_full, {}).get("low") if last_full is not None else None
    if base and base >= MOVE_MIN_BASE and abs(latest / base - 1) >= MOVE_MIN_CHANGE:
        item["move"] = {"change": round((latest / base - 1) * 100), "base": base, "day": last_full}


# --- Patterns -----------------------------------------------------------------------------

def summary(groups: list[list[tuple]]) -> dict:
    """groups: one list of (date, index) per item. The median within each item first, then
    across items, so busy items don't outweigh the rest; ready once enough items have values
    on more than one date."""
    per_item = [median([v for _, v in values]) for values in groups]
    dates = {d for values in groups for d, _ in values}
    ready = len(per_item) >= PATTERN_MIN_ITEMS and len(dates) >= PATTERN_MIN_DATES
    return {"index": round(median(per_item), 4) if ready else None, "items": len(per_item), "dates": len(dates)}


def patterns(items: list[dict], recent_days: list[int], finished_days: list[int]) -> dict:
    """Weekday: each full day's lowest price against the item's own median low (Auctionator's
    days). Time of day: full-scan samples only (every item listed that day, at a new full scan's
    own time) against the item's median sample, by four-hour band in UTC, market-wide."""
    weekday, band, cells = {}, {}, {}
    window, finished = set(recent_days), set(finished_days)
    for item in items:
        lows = {d: v["low"] for d, v in item["days"].items() if d in finished and v["low"] > 0}
        centre = median(list(lows.values()))
        if centre and len(lows) >= MIN_RECENT_DAYS:
            mine = {}
            for d, low in lows.items():
                mine.setdefault((d + 2) % 7, []).append((d, low / centre))  # day 0, 1 January 2020, was a Wednesday (2)
            for key, values in mine.items():
                weekday.setdefault(key, []).append(values)
        samples = [(t, p, d) for t, p, d in item.get("full_obs", []) if d in window and p > 0]
        centre = median([p for _, p, _ in samples])
        if centre and len(samples) >= 3:
            mine_band, mine_cell = {}, {}
            for t, p, d in samples:
                moment = utc(t)
                mine_band.setdefault(band_of(moment.hour), []).append((moment.date(), p / centre))
                mine_cell.setdefault((moment.weekday(), band_of(moment.hour)), []).append((moment.date(), p / centre))
            for key, values in mine_band.items():
                band.setdefault(key, []).append(values)
            for key, values in mine_cell.items():
                cells.setdefault(key, []).append(values)
    return {"weekday": {d: summary(g) for d, g in weekday.items()}, "band": {b: summary(g) for b, g in band.items()},
            "cells": {f"{d}-{b}": summary(g) for (d, b), g in cells.items()}}


def item_pattern(item: dict, recent_days: list[int]) -> dict | None:
    """An item's own weekday pattern from its daily lows, once it has two weeks of days."""
    lows = {d: item["days"][d]["low"] for d in recent_days if d in item["days"] and item["days"][d]["low"] > 0}
    if len(lows) < ITEM_PATTERN_MIN_DAYS:
        return None
    centre = median(list(lows.values()))
    weekday = {}
    for d, low in lows.items():
        weekday.setdefault((d + 2) % 7, []).append((d, low / centre))
    return {"weekday": {k: round(median([v for _, v in g]), 4) for k, g in weekday.items() if len(g) >= PATTERN_MIN_DATES},
            "days": len(lows)}


def market_index(items: list[dict], last_day: int | None, partial: set[int], days: int = 60) -> list[tuple[int, float, int]]:
    """A whole-market price index: each finished full day, the median across items of that
    day's lowest price over the item's own median lowest price, times 100 (after auctionhouse.fyi's
    index and Saddlebag's price-group deltas). Shows what an event did to prices in general."""
    if last_day is None:
        return []
    ratios = {}
    for item in items:
        lows = {d: v["low"] for d, v in item["days"].items() if last_day - days < d < last_day and d not in partial and v["low"] > 0}
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
    partial = partial_days(market["items"], market.get("full_scan_coverage"))
    days = sorted({d for item in market["items"] for d in item["days"]} - partial)
    recent = [d for d in days if last_day is not None and last_day - RECENT_DAYS < d <= last_day]
    frame = {"start": start, "last_day": last_day, "recent": recent,
             "window_days": [d for d in days if last_day is not None and last_day - WINDOW_DAYS < d <= last_day],
             "last_full": max((d for d in days if last_day is not None and d < last_day), default=None)}
    finished = [d for d in frame["window_days"] if d != last_day]  # weekday patterns use finished days only
    for item in market["items"]:
        item["category"] = categories.get(item["id"])
        analyse_item(item, frame, vendor)
        item["pattern"] = item_pattern(item, finished)
    fresh = [i for i in market["items"] if i["fresh"]]
    times = scan_times(market)
    deals = [i for i in fresh if i["deal"] and "saving" in i["deal"]]
    return {
        "newest": newest, "window_start": start, "scans_in_window": sum(1 for t in times if start is not None and t >= start),
        "deals": sorted((i for i in deals if i["deal"]["confidence"] != "low"), key=lambda i: (not i["deal"]["exceptional"], -i["deal"]["saving"])),
        "deals_hidden": sum(1 for i in deals if i["deal"]["confidence"] == "low"),
        "vendor": sorted((i for i in fresh if i["deal"] and i["deal"].get("vendor_profit")), key=lambda i: -i["deal"]["vendor_profit"]),
        "invest": sorted((i for i in fresh if i["invest"] and i["confidence"] != "low"), key=lambda i: -i["invest"]["score"]),
        "short": sorted((i for i in fresh if i["short"] and i["confidence"] != "low"), key=lambda i: i["short"]["stock"]),
        "rising": sorted((i for i in fresh if i["move"] and i["move"]["change"] > 0 and i["confidence"] != "low"), key=lambda i: -i["move"]["change"]),
        "falling": sorted((i for i in fresh if i["move"] and i["move"]["change"] < 0 and i["confidence"] != "low"), key=lambda i: i["move"]["change"]),
        "reliable": sorted((i for i in market["current"] if (i["presence"] or 0) >= 0.8 and i.get("typical")),
                           key=lambda i: (-(i["presence"] or 0), -(i["listed_median"] or 0)))[:40],
        "index": market_index(market["items"], last_day, partial),
        "partial_days": sorted(partial),
        "last_full": frame["last_full"],
        "patterns": patterns(market["items"], frame["window_days"], finished),
        "full_scans": len({t for i in market["items"] for t, _, _ in i.get("full_obs", [])}),
    }

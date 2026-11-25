"""Same-house planning prices, kept separate from the Auctionator archive."""
from __future__ import annotations

import argparse
import json
import statistics
import time
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

from auctionator import DAY_ZERO, item_id
from item_names import fetch
from market import GOOD_BUY_MIN, mad, percentile

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(".cache/market-prices.json")
SOURCE = "https://auctionhouse.tk.gg"
HOUSE = "eu-2-113"
MARKET_SLUGS = {"forever-pvp", "forever-pvp-horde"}
TAZ = "Auctionator"
FDB = "ForeverDB"
TK = "Auction House"
BLIZZARD = "Blizzard API"
HISTORY_DAYS = 14
MIN_DAYS = 3
MOVE = 0.05
FRESH_SECONDS = 3 * 3600
MAX_QUOTE_AGE = 48 * 3600


def day_code(iso: str) -> int:
    return (date.fromisoformat(iso) - DAY_ZERO).days


def read_cache(root: Path) -> dict:
    try:
        cache = json.loads((root / CACHE).read_text())
        if cache.get("house") == HOUSE and cache.get("source") in (TK, BLIZZARD):
            return cache
    except (OSError, ValueError):
        pass
    return {}


def snapshot(payload: dict) -> tuple[int, dict, dict]:
    house = payload["house"]
    if (house["key"], house["region"], house["grp"], house["faction"], house["house"]) != (HOUSE, "eu", 1, "horde", 113):
        raise ValueError("The price feed returned a different Auction House")
    stamp = payload["t"] // 1000
    columns = {name: i for i, name in enumerate(payload["f"])}
    asks, activity = {}, {}
    for item in payload["items"]:
        fields = item["o"]
        ask = fields[columns["ask"]]
        if isinstance(ask, int) and ask > 0:
            asks[str(item["id"])] = [ask, fields[columns["listed"]]]
        # Trade estimates for gear do not resolve random enchants. Keep this signal to
        # stackable goods, and require enough compared hours across the full house.
        hours = fields[columns["flowHours"]] or 0
        if not item.get("nc") and hours >= 18:
            estimated = fields[columns["vol24"]]
            filled = fields[columns["sure24"]]
            if isinstance(estimated, int) and estimated >= 0:
                activity[str(item["id"])] = [estimated, filled, hours]
    if not asks or stamp != house["snapshot"] // 1000:
        raise ValueError("Incomplete Auction House snapshot")
    return stamp, asks, activity


def history_rows(payload: dict, item: int) -> dict:
    if payload["house"]["key"] != HOUSE or payload["item"]["id"] != item:
        raise ValueError("The historical price series returned the wrong item or house")
    daily = payload["daily"]
    d, close, hours = (daily["f"].index(name) for name in ("d", "close", "hours"))
    return {day_code(datetime.fromtimestamp(row[d] / 1000, timezone.utc).date().isoformat()): row[close]
            for row in daily["rows"] if row[close] and row[hours] >= 12}


def refresh(root: Path = ROOT, markets: list | None = None, fdb: dict | None = None) -> int:
    """Fetch one bulk overview. A failed or older response leaves the last good file intact."""
    previous = read_cache(root)
    stamp, asks, activity = snapshot(json.loads(fetch(f"{SOURCE}/api/m/{HOUSE}", 8_000_000, attempts=2)))
    now = datetime.now(timezone.utc)
    now_stamp = int(now.timestamp())
    if not now_stamp - MAX_QUOTE_AGE <= stamp <= now_stamp + 300:
        raise ValueError("The Auction House snapshot is out of date")
    if stamp <= previous.get("timestamp", 0):
        return len(previous["latest"])
    day = day_code(datetime.fromtimestamp(stamp, timezone.utc).date().isoformat())
    days = {key: rows for key, rows in previous.get("days", {}).items() if int(key) >= day - HISTORY_DAYS}
    # One daily close, so an item cannot be weighted by the number of hourly readings.
    days[str(day)] = {key: price for key, (price, _listed) in asks.items()}
    record = {"house": HOUSE, "source": TK, "timestamp": stamp, "days": days, "latest": asks, "activity": activity,
              "backfilled": {key: checked for key, checked in previous.get("backfilled", {}).items() if checked > day - 7}}
    if markets and fdb:
        backfill(record, markets, fdb, now, day)
    path = root / CACHE
    path.parent.mkdir(exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(record, separators=(",", ":")) + "\n")
    temp.replace(path)
    return len(asks)


def backfill(record: dict, markets: list, fdb: dict, now: datetime, day: int) -> None:
    """Fill gaps for a few relevant items per publish, without a bulk crawl of item histories."""
    prices = plan_prices(markets, fdb, record, now)
    outputs = {r["item"] for recipes in fdb.get("recipes", {}).values() for r in recipes}
    needs = usage(fdb)
    queue = []
    for item in outputs | needs.keys():
        key = str(item)
        plan = prices.get(item)
        if key in record["backfilled"] or key not in record["latest"] or not plan:
            continue
        covered = sum(plan["typical_sources"].values())
        if covered < 5:
            trade = (plan["trade"] or [0])[0]
            queue.append((covered >= MIN_DAYS, item not in outputs, -trade, item))
    for _, _, _, item in sorted(queue)[:4]:
        time.sleep(1)
        key = str(item)
        try:
            payload = json.loads(fetch(f"{SOURCE}/api/m/{HOUSE}/item/{item}?hours=336", 2_000_000, attempts=1))
            for date_code, close in history_rows(payload, item).items():
                if day - HISTORY_DAYS <= date_code < day:
                    record["days"].setdefault(str(date_code), {})[key] = close
        except (OSError, ValueError, TypeError, KeyError, IndexError) as error:
            print(f"Historical quotes unavailable for item {item}: {type(error).__name__}")
        record["backfilled"][key] = day


def spread(lows: list[int]) -> float | None:
    """Relative daily price span, trimming both tails when there are at least five days."""
    if len(lows) < MIN_DAYS:
        return None
    low, high = (percentile(lows, .2), percentile(lows, .8)) if len(lows) >= 5 else (min(lows), max(lows))
    return (high - low) / statistics.median(lows)


def steadiness(lows: list[int]) -> str | None:
    change = spread(lows)
    if change is None:
        return None
    return "steady" if change < .25 else "moving" if change < .75 else "volatile"


def item_uses(items: dict, item: int) -> dict:
    needs = items.get(item, {})
    recipes = needs.get("recipes", set())
    crates = needs.get("crates", set())
    return {"recipes": len(recipes), "professions": sorted({p for p, _ in recipes}),
            "crates": len(crates), "stack": sorted(needs.get("stack", ()))}


def usage(fdb: dict) -> dict:
    """Concrete uses, with one count per recipe and one per eligible crate."""
    items = defaultdict(lambda: {"recipes": set(), "crates": set(), "stack": set()})
    for profession, recipes in fdb.get("recipes", {}).items():
        for recipe in recipes:
            for item, amount in recipe["reagents"]:
                items[item]["recipes"].add((profession, recipe["name"]))
                items[item]["stack"].add(amount)
    for crate in fdb.get("crates", []):
        for item, _count in crate["bundles"]:
            items[item]["crates"].add(crate["item"])
    return dict(items)


def plan_prices(markets: list[dict], fdb: dict, cache: dict, now: datetime) -> dict:
    """Fill missing dates only. Keep each raw scan series and variant intact."""
    scoped = {m["slug"]: m for m in markets if m["environment"] == "forever" and m["slug"] in MARKET_SLUGS}
    active = scoped.get("forever-pvp-horde") or scoped.get("forever-pvp")
    if not active:
        return {}
    variants = {str(item_id(item["key"])) for market in scoped.values() for item in market["items"]
                if not item["key"].isdigit() and not item["key"].startswith("p:")}
    today = day_code(now.date().isoformat())
    now_stamp = int(now.timestamp())
    cache_stamp = cache.get("timestamp", 0)
    close = defaultdict(dict)
    external_latest = ({key: value for key, value in cache.get("latest", {}).items() if key not in variants}
                       if 0 <= now_stamp - cache_stamp <= MAX_QUOTE_AGE else {})
    source = cache.get("source", TK)
    for day, rows in cache.get("days", {}).items():
        if today - HISTORY_DAYS <= int(day) <= today:
            for key, ask in rows.items():
                if key not in variants and isinstance(ask, int) and ask > 0:
                    close[key][int(day)] = (ask, source)
    for key, rows in fdb.get("same_house_prices", {}).get(HOUSE, {}).items():
        if key in variants:
            continue
        for iso, ask in rows:
            day = day_code(iso)
            if today - HISTORY_DAYS <= day <= today and ask > 0:
                close[key][day] = (ask, FDB)

    local_latest = {}
    for slug in ("forever-pvp", "forever-pvp-horde"):
        for item in scoped.get(slug, {}).get("items", []):
            key = item["key"]
            if not key.isdigit():
                continue
            for day, row in item["days"].items():
                if today - HISTORY_DAYS <= day <= today and row["low"] > 0:
                    # Both names may record the same day around the market rename.
                    old = close[key].get(day)
                    ask = min(old[0], row["low"]) if old and old[1] == TAZ else row["low"]
                    close[key][day] = (ask, TAZ)
            if item.get("price_day") is None:
                continue
            obs = item["obs"][-1] if item["obs"] else None
            stamp = obs[0] if obs and obs[2] == item["price_day"] else None
            candidate = (item["price"], item["price_day"], stamp, TAZ, item["listed"])
            old = local_latest.get(key)
            if not old or (candidate[1], stamp or 0) >= (old[1], old[2] or 0):
                local_latest[key] = candidate

    prices = {}
    for key in close.keys() | local_latest.keys() | external_latest.keys():
        days = close.get(key, {})
        # A finished day and one vote per day. Today's ask can still appear under Latest.
        usual_rows = [(v, s) for d, (v, s) in sorted(days.items()) if today - HISTORY_DAYS <= d < today]
        typical_rows = [(v, s) for d, (v, s) in sorted(days.items()) if today - 7 <= d < today]
        lows = [v for v, _ in usual_rows]
        usual = int(statistics.median(lows)) if len(lows) >= MIN_DAYS else None
        typical = int(statistics.median(v for v, _ in typical_rows)) if len(typical_rows) >= MIN_DAYS else None
        current = local_latest.get(key)
        if key in external_latest and (not current or not current[2] or (
                now_stamp - current[2] > FRESH_SECONDS and cache_stamp > current[2])):
            ask, listed = external_latest[key]
            current = (ask, day_code(datetime.fromtimestamp(cache_stamp, timezone.utc).date().isoformat()), cache_stamp, source, listed)
        if days:
            day = max(days)
            if not current or day > current[1]:
                ask, src = days[day]
                current = (ask, day, None, src, None)
        transitions = [(days[d - 1][0], v) for d, (v, _) in days.items() if d < today and d - 1 in days]
        churn = (sum(abs(b - a) >= a * MOVE for a, b in transitions) / len(transitions)) if len(transitions) >= 2 else None
        is_recent = bool(current and (0 <= now_stamp - current[2] <= MAX_QUOTE_AGE if current[2] else today - current[1] <= 1))
        trade = cache.get("activity", {}).get(key) if key not in variants and 0 <= now_stamp - cache_stamp <= FRESH_SECONDS else None
        no_recent_ask = (bool(external_latest and key not in external_latest and key not in variants)
                         and 0 <= now_stamp - cache_stamp <= FRESH_SECONDS
                         and (not current or not current[2] or cache_stamp > current[2]))
        good_buy = round(usual - 0.5 * 1.4826 * mad(lows, usual)) if len(lows) >= GOOD_BUY_MIN else None
        prices[int(key)] = {"latest": current, "recent": is_recent, "no_recent_ask": no_recent_ask,
                            "usual": usual, "typical": typical, "good_buy": good_buy,
                            "usual_sources": dict(sorted(count_sources(usual_rows).items())),
                            "typical_sources": dict(sorted(count_sources(typical_rows).items())),
                            "spread": spread(lows), "steadiness": steadiness(lows), "churn": churn,
                            "pairs": len(transitions), "trade": trade, "trade_timestamp": cache_stamp if trade else None}
    return prices


def count_sources(rows: list) -> dict:
    counts = defaultdict(int)
    for _, source in rows:
        counts[source] += 1
    return counts


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(f"Refreshed {refresh():,} EU PvP Horde asks")

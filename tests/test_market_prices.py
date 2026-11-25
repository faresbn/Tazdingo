import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build import market_value
from foreverdb_data import same_house_prices
from market import daily_change
from market_prices import FDB, HOUSE, TAZ, TK, day_code, item_uses, plan_prices, snapshot, spread, usage


class PlanningPrices(unittest.TestCase):
    now = datetime(2026, 11, 25, 12, tzinfo=timezone.utc)
    today = day_code(now.date().isoformat())
    stamp = int(now.timestamp())

    def market(self, prices, key="1", slug="forever-pvp-horde", environment="forever", age=10):
        day = self.today - 1
        return {"slug": slug, "environment": environment,
                "items": [{"key": key, "price": 20000, "price_day": day, "listed": 10,
                           "obs": [(self.stamp - age * 3600, 20000, day)],
                           "days": {day - i: {"low": price} for i, price in enumerate(prices)}}]}

    def test_history_fills_only_missing_same_house_days(self):
        own = self.market([20000])
        renamed = self.market([20100], slug="forever-pvp")
        beta = self.market([100, 100, 100], environment="forever-beta")
        variant = self.market([7, 7, 7], key="gr:1:Example")
        days = [(self.now.date() - timedelta(days=i)).isoformat() for i in range(1, 5)]
        fdb = {"same_house_prices": {HOUSE: {"1": [[days[0], 50000], [days[1], 20400]]},
                                     "us-2-113": {"1": [[days[2], 10]]}}}
        cache = {"timestamp": self.stamp - 3600, "latest": {"1": [21800, 10]},
                 "days": {str(self.today - 3): {"1": 21000}}}
        row = plan_prices([renamed, own, beta], fdb, cache, self.now)[1]
        self.assertEqual(row["typical"], 20400)
        self.assertEqual(row["typical_sources"], {TAZ: 1, FDB: 1, TK: 1})
        self.assertEqual(row["latest"], (21800, self.today, self.stamp - 3600, TK, 10))
        self.assertEqual(plan_prices([variant], {}, {}, self.now), {})

    def test_recent_upload_wins_and_missing_latest_loses_margin(self):
        recent = self.market([20000, 20020, 20120], age=1)
        cache = {"timestamp": self.stamp, "latest": {"1": [22000, 9]}, "activity": {"1": [100, 44, 23]}}
        row = plan_prices([recent], {}, cache, self.now)[1]
        self.assertEqual(row["latest"][3], TAZ)
        self.assertEqual(row["trade"], [100, 44, 23])
        self.assertEqual(market_value({"plan": row}), (20020, TAZ))
        cache["latest"] = {"2": [100, 100]}
        row = plan_prices([recent], {}, cache, self.now)[1]
        self.assertTrue(row["no_recent_ask"])
        self.assertIsNone(market_value({"plan": row}))

    def test_same_relative_changes_at_different_prices(self):
        self.assertEqual(spread([20000, 20200, 20400]), spread([200, 202, 204]))
        row = plan_prices([self.market([100, 110, 109, 108])], {}, {}, self.now)[1]
        self.assertEqual(row["churn"], 1 / 3)
        self.assertEqual(daily_change({"days": {1: {"low": 20000}, 2: {"low": 20300}, 3: {"low": 18000}}},
                                     [1, 2, 3]), .5)

    def test_market_requirements_and_quote_age(self):
        row = plan_prices([self.market([20000])], {}, {}, self.now)[1]
        self.assertIsNone(row["typical"])
        self.assertEqual(market_value({"plan": row}), (20000, "Auctionator snapshot"))
        self.assertIsNone(market_value({"fdb": {"median": 4400, "realms": 5, "listed": 500}}))
        row = plan_prices([self.market([20000], age=55)], {}, {}, self.now)[1]
        self.assertIsNone(market_value({"plan": row}))

    def test_foreverdb_keeps_only_the_named_horde_realm(self):
        data = {1: {"h": {
            "CAMWOW EU5 Realm 2 PvP|H": {"hist": [["2026-11-20", 50, 80, 12]], "d": "2026-11-21", "p": 60},
            "CAMWOW EU5 Realm 2 PvP|A": {"d": "2026-11-23", "p": 25},
            "CAMWOW EU5 Realm 3 PvE|H": {"d": "2026-11-24", "p": 20}}}}
        self.assertEqual(same_house_prices(data), {HOUSE: {"1": [("2026-11-20", 50), ("2026-11-21", 60)]}})

    def test_snapshot_validates_scope_and_keeps_bounded_trade_signal(self):
        body = {"house": {"key": HOUSE, "region": "eu", "grp": 1, "faction": "horde", "house": 113,
                          "snapshot": self.stamp * 1000},
                "t": self.stamp * 1000, "f": ["ask", "listed", "flowHours", "vol24", "sure24"],
                "items": [{"id": 1, "o": [770, 91, 20, 4, 1]},
                          {"id": 2, "o": [10, 12, 3, 9, 9]},
                          {"id": 3, "o": [20, 12, 23, 9, 0], "nc": 1}]}
        self.assertEqual(snapshot(body), (self.stamp, {"1": [770, 91], "2": [10, 12], "3": [20, 12]}, {"1": [4, 1, 20]}))
        body["house"]["grp"] = 2
        with self.assertRaises(ValueError):
            snapshot(body)

    def test_uses_count_recipes_and_crate_options(self):
        fdb = {"recipes": {"Tailoring": [{"name": "Cloth Bolt", "reagents": [[1, 3], [1, 2]]}]},
               "crates": [{"item": 10, "bundles": [[1, 20], [1, 40], [2, 5]]}]}
        self.assertEqual(item_uses(usage(fdb), 1),
                         {"recipes": 1, "professions": ["Tailoring"], "crates": 1, "stack": [2, 3]})

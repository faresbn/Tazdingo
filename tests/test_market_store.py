import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import market_store as ms
from auctionator import InvalidCapture

DAY = 2500  # an Auctionator day code
BASE = 1_793_000_000  # a scan timestamp


def capture(day, stamp, prices, sha="a"):
    """A parsed upload with one market; prices: {item key: (latest, low, high, listed)} for `day`."""
    items = {}
    for key, (latest, low, high, listed) in prices.items():
        items[key] = {"m": latest, "l": {str(day): low} if low != high else {}, "h": {str(day): high, str(day - 1): high + 5},
                      "a": {str(day): listed, str(day - 1): listed}}
    return {"source_sha256": sha * 64, "source_scan_timestamps": {"TimeOfLastBrowseScan": stamp},
            "markets": {"Realm Horde": {"items": items}}}


class Store(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        (self.root / "data").mkdir()
        (self.root / "data/captures.json").write_text(json.dumps({"schema_version": 1, "captures": []}))

    def tearDown(self):
        self.dir.cleanup()

    def add(self, day, stamp, prices, sha="a"):
        cap = capture(day, stamp, prices, sha)
        record = ms.record_from_capture(cap, "Realm Horde", "forever")
        return ms.add_record(self.root, record, ms.history(cap, "Realm Horde", 0, day), {})

    def registry(self):
        return json.loads((self.root / "data/captures.json").read_text())

    def test_record_keeps_only_items_seen_on_the_scan_day(self):
        cap = capture(DAY, BASE, {"2589": (100, 90, 120, 4)})
        cap["markets"]["Realm Horde"]["items"]["2592"] = {"m": 7, "l": {}, "h": {str(DAY - 3): 7}, "a": {}}
        record = ms.record_from_capture(cap, "Realm Horde", "forever")
        self.assertEqual(record["items"], {"2589": [100, 90, 120, 4]})
        self.assertEqual(record["day"], DAY)

    def test_duplicate_upload_is_skipped(self):
        self.assertIsNotNone(self.add(DAY, BASE, {"2589": (100, 90, 120, 4)}))
        self.assertIsNone(self.add(DAY, BASE, {"2589": (100, 90, 120, 4)}, sha="b"))

    def test_finished_days_reach_the_archive_with_scan_stats(self):
        self.add(DAY, BASE, {"2589": (100, 90, 120, 4)})
        self.add(DAY, BASE + 3600, {"2589": (80, 80, 120, 6)})
        self.add(DAY + 1, BASE + 86400, {"2589": (110, 110, 110, 3)})
        store = ms.load(self.root)["forever-realm-horde"]
        self.assertEqual(len(store["records"]), 3)
        self.assertEqual(store["daily"][DAY]["2589"], [80, 120, 6, 2, 90])  # low, high, most listed, scans, median scan price
        self.assertEqual(store["daily"][DAY - 1]["2589"], [125, 125, 6, 0, None])  # from the upload's own history
        self.assertNotIn(DAY + 1, store["daily"])  # the newest day isn't finished yet

    def test_retention_keeps_thirty_days_or_thirty_scans(self):
        # 40 scans, one a day: only the last 30 days stay as records.
        for n in range(40):
            self.add(DAY + n, BASE + n * 86400, {"2589": (100 + n, 100 + n, 100 + n, 1)})
        kept = [r for r in self.registry()["scans"] if r["status"] == "kept"]
        self.assertEqual(len(kept), 31)  # day 9..39: the newest and every scan within 30 days of it
        store = ms.load(self.root)["forever-realm-horde"]
        self.assertIn(DAY, store["daily"])  # folded days survive in the archive
        self.assertEqual(store["daily"][DAY]["2589"][3], 1)

    def test_a_quiet_month_keeps_the_newest_thirty_scans(self):
        for n in range(35):
            self.add(DAY + n * 3, BASE + n * 3 * 86400, {"2589": (100, 100, 100, 1)})
        kept = [r for r in self.registry()["scans"] if r["status"] == "kept"]
        self.assertEqual(len(kept), 30)
        self.assertEqual(len(list((self.root / "data/market/forever-realm-horde/scans").glob("*.json"))), 30)

    def test_a_changed_record_stops_the_build(self):
        self.add(DAY, BASE, {"2589": (100, 90, 120, 4)})
        path = self.root / self.registry()["scans"][0]["path"]
        path.write_text(path.read_text().replace("100", "1"))
        with self.assertRaises(InvalidCapture):
            ms.load(self.root)

    def test_an_unlisted_archive_file_stops_the_build(self):
        self.add(DAY, BASE, {"2589": (100, 90, 120, 4)})
        self.add(DAY + 1, BASE + 86400, {"2589": (100, 90, 120, 4)})
        extra = self.root / "data/market/forever-realm-horde/daily/1999-01.json"
        extra.write_text(json.dumps({"format": ms.ARCHIVE_FORMAT, "month": "1999-01", "days": {}}))
        with self.assertRaises(InvalidCapture):
            ms.load(self.root)

    def test_inbox_records_carry_history_and_are_validated(self):
        cap = capture(DAY, BASE, {"2589": (100, 90, 120, 4)})
        record = ms.record_from_capture(cap, "Realm Horde", "forever", history_days=3)
        self.assertEqual(sorted(record["history"]["2589"]), [str(DAY - 1), str(DAY)])
        ms.validate_record(json.loads(json.dumps(record)), inbox=True)
        with self.assertRaises(InvalidCapture):
            ms.validate_record(record)  # history isn't allowed in a filed record
        bad = dict(record, settings={"secret": 1})
        with self.assertRaises(InvalidCapture):
            ms.validate_record(bad, inbox=True)


class StoreSafety(Store):
    def test_a_day_already_folded_is_refused(self):
        for n in range(40):
            self.add(DAY + n, BASE + n * 86400, {"2589": (100 + n, 100 + n, 100 + n, 1)})
        with self.assertRaises(InvalidCapture):
            self.add(DAY, BASE + 3600, {"2589": (50, 50, 50, 1)}, sha="c")

    def test_a_changed_store_is_refused_before_anything_is_added(self):
        self.add(DAY, BASE, {"2589": (100, 90, 120, 4)})
        path = self.root / self.registry()["scans"][0]["path"]
        path.write_text(path.read_text().replace("100", "1"))
        with self.assertRaises(InvalidCapture):
            self.add(DAY + 1, BASE + 86400, {"2589": (100, 90, 120, 4)})
        self.assertEqual(len(self.registry()["scans"]), 1)


class Sightings(unittest.TestCase):
    def test_unchanged_items_in_a_later_upload_are_not_new_sightings(self):
        import build
        rec = lambda stamp, items: {"scan_timestamp": stamp, "day": DAY, "source_sha256": "a" * 64, "items": items}
        entry = {"environment": "forever", "market": "Realm Horde", "folded": 0, "daily": {},
                 "records": [rec(BASE, {"2589": [100, 90, 120, 4], "2592": [5, 5, 5, 1]}),
                             rec(BASE + 3600, {"2589": [100, 90, 120, 4], "2592": [4, 4, 5, 2]})]}
        markets = {}
        build.add_store_market(markets, "forever-realm-horde", entry, {})
        items = markets["forever-realm-horde"]["items"]
        self.assertEqual(len(items["2589"]["obs"]), 1)  # carried forward unchanged: one sighting
        self.assertEqual(len(items["2592"]["obs"]), 2)  # its price changed: seen again


class Analytics(unittest.TestCase):
    def item(self, lows, volatility="steady", listed=5):
        days = {DAY + n: {"low": v, "high": v, "listed": listed} for n, v in enumerate(lows)}
        last = DAY + len(lows) - 1
        return {"id": 2589, "key": "2589", "name": "Thing", "days": days, "volatility": volatility, "typical": lows[-1],
                "obs": [(BASE + n * 86400, v, DAY + n) for n, v in enumerate(lows)], "price": lows[-1], "price_day": last}

    def market(self, items):
        import market as m
        last = max(d for i in items for d in i["days"])
        scans = [{"time": m.utc(t).isoformat().replace("+00:00", "Z")} for t in sorted({t for i in items for t, _, _ in i["obs"]})]
        return {"items": items, "current": items, "scans": scans, "last_day": last}

    def test_volatile_items_stay_out_of_the_investment_watch(self):
        import market as m
        lows = [1000] * 12 + [500]
        steady = self.item(lows)
        volatile = dict(self.item(lows, volatility="volatile"), id=2590, key="2590")
        result = m.analyse(self.market([steady, volatile]), {}, {})
        self.assertEqual([i["key"] for i in result["invest"]], ["2589"])

    def test_partial_days_are_found_even_when_most_days_are_partial(self):
        import market as m
        items = [{"days": {DAY + d: {} for d in range(9) if n < 10 or d in (3, 7)}} for n in range(100)]
        self.assertEqual(m.partial_days(items), {DAY + d for d in range(9)} - {DAY + 3, DAY + 7})

    def test_one_busy_afternoon_is_not_a_pattern(self):
        import market as m
        items = [{"full_obs": [(BASE + k * 600, 100 + k, DAY) for k in range(6)], "days": {}} for _ in range(30)]
        cells = m.patterns(items, [DAY], [DAY])["cells"]
        self.assertTrue(all(c["index"] is None for c in cells.values()))


class Recovery(Store):
    def test_an_import_cut_off_before_the_registry_is_undone_next_time(self):
        from unittest import mock
        self.add(DAY, BASE, {"2589": (100, 90, 120, 4)})
        real = ms.write_whole

        def crash_on_registry(path, text):
            if path.name == "captures.json":
                raise KeyboardInterrupt  # the process stops after the record and archive were written
            real(path, text)
        with mock.patch.object(ms, "write_whole", side_effect=crash_on_registry):
            with self.assertRaises(KeyboardInterrupt):
                self.add(DAY + 1, BASE + 86400, {"2589": (80, 80, 80, 2)})
        with self.assertRaises(InvalidCapture):
            ms.load(self.root)  # the build refuses a half-finished import
        self.assertIsNotNone(self.add(DAY + 1, BASE + 86400, {"2589": (80, 80, 80, 2)}))  # undone, then filed
        self.assertEqual(len(ms.load(self.root)["forever-realm-horde"]["records"]), 2)

    def test_empty_folders_left_by_a_rollback_do_not_block_the_next_import(self):
        (self.root / "data/market/forever-other-market/scans").mkdir(parents=True)
        self.assertIsNotNone(self.add(DAY, BASE, {"2589": (100, 90, 120, 4)}))
        self.assertFalse((self.root / "data/market/forever-other-market").exists())


class FullScans(unittest.TestCase):
    def test_only_an_upload_whose_latest_scan_was_full_samples_the_market(self):
        import build
        rec = lambda stamp, full, price: {"scan_timestamp": stamp, "full_scan_timestamp": full, "day": DAY,
                                          "source_sha256": "a" * 64, "items": {"2589": [price, price, price, 1]}}
        entry = {"environment": "forever", "market": "Realm Horde", "folded": 0, "daily": {}, "full_scan_items": [],
                 "records": [rec(BASE, BASE - 3600, 100),      # a search after the full scan: not that scan's snapshot
                             rec(BASE + 7200, BASE + 7200, 90)]}  # the full scan was the latest: a sample at its time
        markets = {}
        build.add_store_market(markets, "forever-realm-horde", entry, {})
        self.assertEqual(markets["forever-realm-horde"]["items"]["2589"]["full_obs"], [(BASE + 7200, 90, DAY)])


class FullScanOwner(unittest.TestCase):
    def capture(self, days, full=BASE, browse=BASE - 60):
        markets = {name: {"items": {"2589": {"m": 1, "l": {}, "h": {str(d): 1}, "a": {}}}} for name, d in days.items()}
        return {"source_scan_timestamps": {"TimeOfLastReplicateScan": full, "TimeOfLastBrowseScan": browse}, "markets": markets}

    def test_the_full_scan_goes_to_the_one_market_with_the_newest_day(self):
        self.assertEqual(ms.full_scan_market(self.capture({"A": DAY, "B": DAY - 3})), "A")

    def test_two_markets_on_the_same_day_get_neither(self):
        self.assertIsNone(ms.full_scan_market(self.capture({"A": DAY, "B": DAY})))

    def test_a_later_search_means_no_full_scan_snapshot(self):
        self.assertIsNone(ms.full_scan_market(self.capture({"A": DAY}, browse=BASE + 60)))


class ReviewFixes(Store):
    def test_a_market_not_scanned_again_is_not_filed_again(self):
        # Two markets in one file, only the other one scanned: the file's scan time moves on,
        # this market's items and day don't, so there's nothing new to file.
        prices = {"2589": (100, 90, 120, 4)}
        self.assertIsNotNone(self.add(DAY, BASE, prices))
        self.assertIsNone(self.add(DAY, BASE + 3600, prices, sha="b"))
        self.assertEqual(len(self.registry()["scans"]), 1)
        self.assertIsNotNone(self.add(DAY, BASE + 7200, {"2589": (95, 90, 120, 4)}, sha="c"))

    def test_names_in_other_alphabets_get_distinct_slugs(self):
        import ah_pages
        self.assertNotEqual(ms.market_slug("forever", "Пламегор Horde"), ms.market_slug("forever", "Гордунни Horde"))
        self.assertEqual(ms.market_slug("forever", "Realm Horde"), "forever-realm-horde")
        self.assertNotEqual(ah_pages.item_slug("gr:123:медведя"), ah_pages.item_slug("gr:123:обезьяны"))
        self.assertEqual(ah_pages.item_slug("gr:123:of the Bear"), "gr-123-of-the-bear")

    def test_badly_typed_records_are_refused_cleanly(self):
        record = ms.record_from_capture(capture(DAY, BASE, {"2589": (100, 90, 120, 4)}), "Realm Horde", "forever")
        for change in ({"scan_timestamp": "x", "full_scan_timestamp": BASE}, {"environment": 5}):
            with self.assertRaises(InvalidCapture):
                ms.validate_record(dict(record, **change))

    def test_latest_price_follows_a_later_archive_day(self):
        import build
        entry = {"environment": "forever", "market": "Realm Horde", "folded": 0, "full_scan_items": [],
                 "daily": {DAY - 1: {"2589": [500, 600, 2, 0, None]}},
                 "records": [{"scan_timestamp": BASE, "full_scan_timestamp": None, "day": DAY - 3,
                              "source_sha256": "a" * 64, "items": {"2589": [900, 900, 900, 1]}}]}
        markets = {}
        build.add_store_market(markets, "forever-realm-horde", entry, {})
        item = markets["forever-realm-horde"]["items"]["2589"]
        self.assertEqual((item["price"], item["price_day"]), (500, DAY - 1))


if __name__ == "__main__":
    unittest.main()

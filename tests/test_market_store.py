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


if __name__ == "__main__":
    unittest.main()

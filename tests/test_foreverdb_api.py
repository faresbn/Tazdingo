import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import foreverdb_api


class ReuseOnABuildChange(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.cache = base / "foreverdb-api"
        for build, price in (("1.60.1.70532", 1), ("1.60.1.70862", 7)):
            old = base / f"foreverdb-api-{build}"
            old.mkdir()
            (old / "items_123.json").write_text(json.dumps({"data": {"id": 123, "price": price}}))
            (old / "professions_alchemy_limit-100_offset-0.json").write_text(json.dumps({"data": ["stale"]}))
        self.patches = [mock.patch.object(foreverdb_api, "CACHE", self.cache),
                        mock.patch("urllib.request.urlopen", side_effect=AssertionError("no download expected")),
                        mock.patch("time.sleep")]
        for p in self.patches:
            p.start()
        reuse = mock.patch.object(foreverdb_api, "REUSE", foreverdb_api.previous_cache("1.60.1.70888"))
        reuse.start()
        self.patches.append(reuse)

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def test_the_newest_earlier_build_is_used(self):
        self.assertEqual(foreverdb_api.REUSE.name, "foreverdb-api-1.60.1.70862")

    def test_item_details_are_copied_not_downloaded(self):
        self.assertEqual(foreverdb_api.get("/items/123", "key")["data"]["price"], 7)
        self.assertTrue((self.cache / "items_123.json").is_file())

    def test_lists_and_new_items_are_downloaded(self):
        for path in ("/professions/alchemy?limit=100&offset=0", "/items/456"):
            with self.assertRaises(AssertionError):
                foreverdb_api.get(path, "key")

    def test_full_reuses_nothing(self):
        with mock.patch.object(foreverdb_api, "REUSE", None), self.assertRaises(AssertionError):
            foreverdb_api.get("/items/123", "key")


if __name__ == "__main__":
    unittest.main()

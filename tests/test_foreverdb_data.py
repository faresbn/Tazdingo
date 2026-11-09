import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from auctionator import InvalidCapture
from foreverdb_data import parse_recipes
import item_names
import urllib.error
from unittest import mock

# ForeverDB's row layouts: before 7 November (12 fields), since (13), and random-count recipes (15).
OLD = '{%d,"Recipe %d",1,10,12,15,247755,1,"765:1,3371:1","a",0,1}'
NEW = '{%d,"Recipe %d",1,10,12,15,247755,1,"765:1,3371:1","a",0,1,0}'
RANDOM = '{%d,"Recipe %d",75,90,97,105,4365,2,"4364:3,2589:1","t",0,0,1,1,3}'


def recipes_file(layout: str, count: int = 1000) -> str:
    rows = ",".join(layout % (n, n) for n in range(count))
    return "local _, ns = ...\nns.recipes = {Alchemy={" + rows + "}}\n"


class Recipes(unittest.TestCase):
    def test_every_layout_parses(self):
        for layout in (OLD, NEW, RANDOM):
            with self.subTest(layout=layout):
                recipes = parse_recipes(recipes_file(layout))["Alchemy"]
                self.assertEqual(len(recipes), 1000)
                self.assertEqual(recipes[0]["name"], "Recipe 0")

    def test_fields_after_new_are_ignored(self):
        first = parse_recipes(recipes_file(RANDOM))["Alchemy"][0]
        self.assertEqual((first["skill"], first["item"], first["count"], first["learned"], first["new"]),
                         (75, 4365, 2, "t", False))
        self.assertEqual(first["reagents"], [[4364, 3], [2589, 1]])

    def test_too_few_recipes_is_refused(self):
        with self.assertRaises(InvalidCapture):
            parse_recipes(recipes_file(NEW, count=10))


class Fetch(unittest.TestCase):
    def answer(self, *results):
        """urlopen stand-in: raises or returns each result in turn."""
        calls = iter(results)
        def urlopen(request, timeout):
            result = next(calls)
            if isinstance(result, Exception):
                raise result
            response = mock.MagicMock()
            response.__enter__.return_value.read.return_value = result
            return response
        return urlopen

    def busy(self, code=502):
        return urllib.error.HTTPError("https://foreverdb.net/x", code, "busy", {}, None)

    def test_a_busy_server_is_retried(self):
        with mock.patch("urllib.request.urlopen", self.answer(self.busy(), self.busy(503), b"ok")), \
             mock.patch("time.sleep") as sleep:
            self.assertEqual(item_names.fetch("https://foreverdb.net/x", 10), b"ok")
        self.assertEqual(sleep.call_count, 2)

    def test_a_connection_reset_mid_download_is_retried(self):
        # 9 November: ForeverDB reset the connection while a price shard was downloading.
        with mock.patch("urllib.request.urlopen", self.answer(ConnectionResetError(54, "reset"), TimeoutError(), b"ok")), \
             mock.patch("time.sleep") as sleep:
            self.assertEqual(item_names.fetch("https://foreverdb.net/x", 10), b"ok")
        self.assertEqual(sleep.call_count, 2)

    def test_it_gives_up_after_four_tries(self):
        with mock.patch("urllib.request.urlopen", self.answer(*[self.busy()] * 4)), mock.patch("time.sleep"):
            with self.assertRaises(urllib.error.HTTPError):
                item_names.fetch("https://foreverdb.net/x", 10)

    def test_a_missing_file_fails_at_once(self):
        with mock.patch("urllib.request.urlopen", self.answer(self.busy(404))), mock.patch("time.sleep") as sleep:
            with self.assertRaises(urllib.error.HTTPError):
                item_names.fetch("https://foreverdb.net/x", 10)
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()

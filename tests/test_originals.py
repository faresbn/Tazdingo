import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import originals

STAMP = 1_793_000_000  # 2026-10-26 07:33 UTC


class Originals(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        self.source = self.root / "AllTheThings.lua"
        self.source.write_bytes(b"ATTAccountWideData = {}\n")

    def tearDown(self):
        self.dir.cleanup()

    def test_kept_by_environment_addon_and_time(self):
        kept = originals.keep(self.root, self.source, "forever", "AllTheThings.lua", STAMP)
        self.assertEqual(kept.relative_to(self.root).as_posix(), "data/captures/forever/allthethings/2026-10-26T0733Z.lua")
        self.assertEqual(kept.read_bytes(), self.source.read_bytes())

    def test_same_file_twice_is_kept_once_and_a_different_one_gets_a_new_name(self):
        first = originals.keep(self.root, self.source, "forever", "AllTheThings", STAMP)
        self.assertEqual(originals.keep(self.root, self.source, "forever", "AllTheThings", STAMP), first)
        self.source.write_bytes(b"ATTAccountWideData = { x = 1 }\n")
        second = originals.keep(self.root, self.source, "forever", "AllTheThings", STAMP)
        self.assertEqual(second.name, "2026-10-26T0733Z-v2.lua")
        self.assertNotEqual(second.read_bytes(), first.read_bytes())

    def test_addon_names(self):
        self.assertEqual(originals.addon_slug("Auctionator.lua"), "auctionator")
        with self.assertRaises(ValueError):
            originals.addon_slug(".lua")


if __name__ == "__main__":
    unittest.main()

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build
import feed

MONEY = re.compile(r"\b\d+g \d+s\b|\b\d+s \d+c\b")


class Feed(unittest.TestCase):
    """The feed is built into a temporary folder from the repository's data, never into feed/."""

    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        cls.out = Path(cls.dir.name)
        build.build(ROOT, out=ROOT / "tmp/test-feed-dist", feed=cls.out / "feed")
        cls.files = {p.relative_to(cls.out).as_posix(): p.read_text() for p in (cls.out / "feed").rglob("*.md")}

    @classmethod
    def tearDownClass(cls):
        cls.dir.cleanup()

    def paths_in(self, text):
        return re.findall(r"`((?:feed|content)/[^`]+\.md)`", text)

    def test_index_is_only_a_map(self):
        index = self.files["feed/index.md"]
        self.assertLess(len(index), 4000)
        self.assertIsNone(MONEY.search(index), "the map holds no prices")
        self.assertIn("feed/guides.md", index)
        self.assertIn("feed/craft/index.md", index)

    def test_every_path_in_a_map_exists(self):
        for name, text in self.files.items():
            for path in self.paths_in(text):
                target = self.out / path if path.startswith("feed/") else ROOT / path
                self.assertTrue(target.is_file(), f"{name} points to {path}, which doesn't exist")

    def test_every_market_and_page_is_mapped(self):
        index, guides = self.files["feed/index.md"], self.files["feed/guides.md"]
        for folder in (self.out / "feed/prices").iterdir():
            self.assertIn(f"feed/prices/{folder.name}/index.md", index)
            market_map = self.files[f"feed/prices/{folder.name}/index.md"]
            for f in folder.glob("*.md"):
                if f.name != "index.md":
                    self.assertIn(f"feed/prices/{folder.name}/{f.name}", market_map)
        for page in (ROOT / "content").rglob("*.md"):
            self.assertIn(f"`{page.relative_to(ROOT).as_posix()}`", guides)

    def test_versions_are_git_blob_ids(self):
        guides = self.files["feed/guides.md"]
        for page in sorted((ROOT / "content").rglob("*.md"))[:5]:
            blob = subprocess.run(["git", "hash-object", str(page)], capture_output=True, text=True, check=True).stdout.strip()
            self.assertEqual(feed.blob_id(page), blob)
            self.assertIn(f"`{page.relative_to(ROOT).as_posix()}`", guides)
            self.assertIn(f"version `{blob[:feed.VERSION_CHARS]}`", guides)

    def test_no_names(self):
        for name, text in self.files.items():
            self.assertIsNone(build.PRIVATE.search(text), f"{name} names someone")

    def test_same_data_same_feed(self):
        with tempfile.TemporaryDirectory() as again:
            build.build(ROOT, out=ROOT / "tmp/test-feed-dist", feed=Path(again) / "feed")
            second = {p.relative_to(again).as_posix(): p.read_text() for p in (Path(again) / "feed").rglob("*.md")}
        self.assertEqual(self.files, second)

    def test_only_a_feed_folder(self):
        with self.assertRaises(ValueError):
            feed.write(ROOT / "tmp/not-a-feed", ROOT, [], {"content": {}, "craft": []}, build.money)


if __name__ == "__main__":
    unittest.main()

import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import icloud_janitor


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


class Janitor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "test@example.com")
        git(self.root, "config", "user.name", "Test")
        (self.root / "feed").mkdir()
        self.page = self.root / "feed/index.md"
        self.page.write_text("first version\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "first")
        self.page.write_text("second version\n")
        git(self.root, "commit", "-qam", "second")

    def tearDown(self):
        self.tmp.cleanup()

    def plant(self, name, text):
        path = self.root / "feed" / name
        path.write_text(text)
        return path

    def run_janitor(self, delete):
        with redirect_stdout(io.StringIO()) as out:
            icloud_janitor.main(self.root, delete=delete)
        return out.getvalue()

    def test_safe_copies_are_deleted_and_the_rest_kept(self):
        same = self.plant("index 2.md", "second version\n")         # identical to the current file
        older = self.plant("index 3.md", "first version\n")         # an earlier committed version
        edited = self.plant("index 4.md", "an edit nobody committed\n")
        orphan = self.plant("gone 2.md", "no original\n")
        self.run_janitor(delete=True)
        self.assertFalse(same.exists())
        self.assertFalse(older.exists())
        self.assertTrue(edited.exists())
        self.assertTrue(orphan.exists())
        self.assertEqual(self.page.read_text(), "second version\n")

    def test_dry_run_deletes_nothing(self):
        copy = self.plant("index 2.md", "first version\n")
        self.assertIn("dry-run", self.run_janitor(delete=False))
        self.assertTrue(copy.exists())

    def test_copies_inside_git_are_only_listed(self):
        ref = self.root / ".git/index 2"
        ref.write_bytes((self.root / ".git/index").read_bytes())
        self.assertIn(".git/index 2", self.run_janitor(delete=True))
        self.assertTrue(ref.exists())

    def test_clean(self):
        self.assertIn("clean", self.run_janitor(delete=True))


if __name__ == "__main__":
    unittest.main()

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import feed
import inbox
import provenance

PAGE = "content/more/addons.md"
TODAY = datetime.now(timezone.utc).date()
WHEN = TODAY.strftime("%-d %b %Y")
FINDING = f"### WeakAuras still has no Forever version (tested, {WHEN})\n\nTested in game at level 12: the addon list shows it as out of date."
BETA_LUA = ROOT / "data/captures/forever-beta/FOREVER_BETA_Auctionator_2026-10-17.lua"


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


class InboxCase(unittest.TestCase):
    """Each test works on a throwaway clone with a bare remote; the slow full check is replaced."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        base = Path(self.dir.name)
        self.remote = base / "remote.git"
        git(base, "init", "-q", "--bare", "--initial-branch=main", str(self.remote))
        git(ROOT, "push", "-q", str(self.remote), "HEAD:refs/heads/main")  # whatever is checked out, even a detached CI checkout
        self.root = base / "work"
        git(base, "clone", "-q", str(self.remote), str(self.root))
        git(self.root, "config", "user.name", "test")
        git(self.root, "config", "user.email", "test@example.com")
        self.checks, self.names = inbox.run_checks, inbox.refresh_names
        inbox.run_checks = lambda root: None
        inbox.refresh_names = lambda root: None
        self.count = 0

    def tearDown(self):
        inbox.run_checks, inbox.refresh_names = self.checks, self.names
        self.dir.cleanup()

    def submit(self, kind, name, body: bytes | str, **fields):
        self.count += 1
        sub_id = f"20261030T1200{self.count:02d}Z-abc{self.count:03d}"
        folder = self.root / "inbox" / sub_id
        folder.mkdir(parents=True)
        (folder / name).write_bytes(body.encode() if isinstance(body, str) else body)
        (folder / "submission.json").write_text(json.dumps({
            "format": 1, "id": sub_id, "received": f"2026-10-30T12:00:{self.count:02d}Z", "key_label": "key-1",
            "kind": kind, "file": name, **fields}))
        git(self.root, "add", "inbox")
        git(self.root, "commit", "-q", "-m", f"Inbox: {sub_id}")
        return sub_id

    def edited_page(self, change=None, path=PAGE):
        text = (self.root / path).read_text()
        text = re.sub(r"^updated: .*$", f"updated: {TODAY.isoformat()}", text, count=1, flags=re.M)
        return change(text) if change else text.replace("## Field findings\n\nNothing recorded yet.", "## Field findings\n\n" + FINDING)

    def submit_page(self, text, path=PAGE, version=None, message="Addons: WeakAuras still has no Forever version, tested"):
        return self.submit("page", "page.md", text, path=path, message=message,
                           version=version or feed.blob_id(self.root / path)[:12])

    def held_reason(self, sub_id):
        return (self.root / "inbox/held" / sub_id / "reason.txt").read_text()


class Pages(InboxCase):
    def test_good_edit_is_applied_and_archived(self):
        text = self.edited_page()
        sub = self.submit_page(text)
        [outcome] = inbox.run(self.root)
        self.assertEqual(outcome["outcome"], "applied", outcome)
        self.assertEqual((self.root / PAGE).read_text(), text)
        self.assertFalse((self.root / "inbox" / sub).exists())
        self.assertIn("WeakAuras still has no Forever version", git(self.root, "log", "-2", "--format=%s"))
        self.assertIn("more/addons", (self.root / "archive/LOG.md").read_text())

    def test_stale_version_is_held(self):
        sub = self.submit_page(self.edited_page(), version="0123456789ab")
        [outcome] = inbox.run(self.root)
        self.assertEqual(outcome["outcome"], "held")
        self.assertIn("changed since it was read", self.held_reason(sub))
        self.assertNotIn("WeakAuras still has no", (self.root / PAGE).read_text())

    def test_unknown_page_is_held(self):
        sub = self.submit_page(self.edited_page(), path=PAGE, message="Addons: x")
        data = json.loads((self.root / "inbox" / sub / "submission.json").read_text())
        data["path"] = "content/more/secrets.md"
        (self.root / "inbox" / sub / "submission.json").write_text(json.dumps(data))
        git(self.root, "commit", "-qam", "edit")
        inbox.run(self.root)
        self.assertIn("isn't a page the site knows", self.held_reason(sub))

    def test_bad_header_is_held(self):
        sub = self.submit_page(self.edited_page().replace("summary:", "author: someone\nsummary:", 1))
        inbox.run(self.root)
        self.assertIn("unknown header field", self.held_reason(sub))

    def test_name_in_message_is_held(self):
        sub = self.submit_page(self.edited_page(), message="Addons: Mike checked WeakAuras")
        inbox.run(self.root)
        self.assertIn("commit message", self.held_reason(sub))

    def test_finding_must_say_how_known(self):
        text = self.edited_page().replace("Tested in game at level 12: the addon list shows it as out of date.", "It's out of date.")
        sub = self.submit_page(text)
        inbox.run(self.root)
        self.assertIn("must say how it's known", self.held_reason(sub))

    def test_findings_are_never_deleted(self):
        (self.root / PAGE).write_text(self.edited_page())
        git(self.root, "commit", "-qam", "Addons: a finding")
        without = self.edited_page(lambda t: t.split(FINDING)[0] + "Nothing recorded yet." + t.split(FINDING)[1])
        sub = self.submit_page(without)
        inbox.run(self.root)
        self.assertIn("never deleted", self.held_reason(sub))

    def test_recommendation_change_goes_to_review(self):
        path = "content/classes/hunter/overview.md"
        text = self.edited_page(lambda t: t.replace("### Tazdingo recommendation\n", "### Tazdingo recommendation\n\nLevel as Beast Mastery first.\n", 1), path)
        before = (self.root / path).read_text()
        sub = self.submit_page(text, path=path, message="Hunter: recommend Beast Mastery for levelling")
        [outcome] = inbox.run(self.root)
        self.assertEqual(outcome["outcome"], "review", outcome)
        self.assertEqual((self.root / path).read_text(), before, "main is unchanged until the pull request is merged")
        self.assertIn("Level as Beast Mastery first.", git(self.root, "show", f"review/{sub}:{path}"))
        self.assertFalse((self.root / "inbox" / sub).exists())

    def test_failed_checks_hold_and_roll_back(self):
        def failing(root):
            raise inbox.Held("the site's build failed with this change")
        inbox.run_checks = failing
        sub = self.submit_page(self.edited_page())
        inbox.run(self.root)
        self.assertIn("build failed", self.held_reason(sub))
        self.assertNotIn("WeakAuras still has no", (self.root / PAGE).read_text())

    def test_an_unexpected_error_holds_only_that_submission(self):
        def broken(root, sub, folder, base, push):
            raise KeyError("surprise")
        original = inbox.apply_page
        inbox.apply_page = broken
        try:
            sub = self.submit_page(self.edited_page())
            [outcome] = inbox.run(self.root)
        finally:
            inbox.apply_page = original
        self.assertEqual(outcome["outcome"], "held")
        self.assertIn("couldn't process this", self.held_reason(sub))

    def test_bad_submission_does_not_block_a_good_one(self):
        bad = self.submit_page(self.edited_page(), version="0123456789ab")
        good = self.submit_page(self.edited_page())
        outcomes = inbox.run(self.root)
        self.assertEqual([o["outcome"] for o in outcomes], ["held", "applied"])
        self.assertTrue((self.root / "inbox/held" / bad).is_dir())
        self.assertFalse((self.root / "inbox" / good).exists())

    def test_main_moving_mid_run_is_redone_from_the_new_main(self):
        sub = self.submit_page(self.edited_page())
        git(self.root, "push", "-q", "origin", "HEAD:main")
        other = Path(self.dir.name) / "other"
        git(Path(self.dir.name), "clone", "-q", str(self.remote), str(other))
        git(other, "config", "user.name", "test")
        git(other, "config", "user.email", "test@example.com")
        (other / PAGE).write_text((other / PAGE).read_text().replace("## At a glance", "## At a glance\n\nEdited elsewhere.", 1))
        git(other, "commit", "-qam", "Addons: edited elsewhere")
        git(other, "push", "-q", "origin", "HEAD:main")
        [outcome] = inbox.run(self.root, push=True)
        self.assertEqual(outcome["outcome"], "held")
        self.assertIn("Edited elsewhere.", (self.root / PAGE).read_text(), "the other edit is kept")
        self.assertIn("changed since it was read", self.held_reason(sub))
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), git(self.remote, "rev-parse", "main"))


class Safety(InboxCase):
    def test_refuses_to_run_over_uncommitted_work(self):
        (self.root / PAGE).write_text("work in progress")
        with self.assertRaises(SystemExit):
            inbox.run(self.root)
        self.assertEqual((self.root / PAGE).read_text(), "work in progress")

    def test_a_push_whose_acknowledgement_was_lost_still_reports_its_outcomes(self):
        self.submit_page(self.edited_page(), version="0123456789ab")
        real = subprocess.run
        def flaky(args, *a, **k):
            if args[:3] == ["git", "push", "-q"]:
                real(args, *a, **k)  # the push lands...
                return subprocess.CompletedProcess(args, 1)  # ...but reports failure
            return real(args, *a, **k)
        inbox.subprocess.run = flaky
        try:
            [outcome] = inbox.run(self.root, push=True)
        finally:
            inbox.subprocess.run = real
        self.assertEqual(outcome["outcome"], "held")


class AddonFiles(InboxCase):
    def test_unknown_addon_is_stored(self):
        self.submit("lua", "AllTheThings.lua", b"AllTheThingsAD = {\n\t[\"Version\"] = 1,\n}\n")
        [outcome] = inbox.run(self.root)
        self.assertEqual(outcome["outcome"], "applied", outcome)
        kept = list((self.root / "data/captures/forever/allthethings").glob("*.lua"))
        self.assertEqual(len(kept), 1)
        self.assertIn("no processor", outcome["detail"])

    def test_name_must_match_contents(self):
        sub = self.submit("lua", "AllTheThings.lua", b"AUCTIONATOR_PRICE_DATABASE = {}\n")
        inbox.run(self.root)
        self.assertIn("doesn't match its contents", self.held_reason(sub))
        sub = self.submit("lua", "Auctionator.lua", b"SomethingElse = {}\n")
        inbox.run(self.root)
        self.assertIn("doesn't match its contents", self.held_reason(sub))

    def test_not_saved_variables_is_held(self):
        sub = self.submit("lua", "Notes.lua", b"\x89PNG\r\n\x1a\n\0\0\0binary")
        inbox.run(self.root)
        self.assertIn("isn't a saved-variables file", self.held_reason(sub))

    def test_auctionator_needs_a_market(self):
        sub = self.submit("lua", "Auctionator.lua", BETA_LUA.read_bytes())
        inbox.run(self.root)
        self.assertIn("which market", self.held_reason(sub))

    def test_auctionator_scan_is_filed_and_kept(self):
        self.submit("lua", "Auctionator.lua", BETA_LUA.read_bytes(), market="PvP")
        [outcome] = inbox.run(self.root)
        self.assertEqual(outcome["outcome"], "applied", outcome)
        self.assertTrue(list((self.root / "data/market").rglob("*.json")))
        self.assertEqual(len(list((self.root / "data/captures/forever/auctionator").glob("*.lua"))), 1)
        self.assertTrue(git(self.root, "log", "-1", "--format=%s").startswith("Auction House scan of"))


class Provenance(unittest.TestCase):
    def check(self, old, new, meta=None, old_meta=None, domains=frozenset({"wowhead.com"})):
        return provenance.check(old, new, meta or {"updated": TODAY.isoformat()}, old_meta or {}, set(domains), {2589}, TODAY)

    def page(self, guides="", findings="Nothing recorded yet."):
        return f"## At a glance\n\nx\n\n## What the guides say\n\n{guides}\n\n## Field findings\n\n{findings}\n\n## Read more\n\n- x"

    def test_costs_need_a_source_but_seconds_are_not_money(self):
        problems, _ = self.check(self.page(), self.page("### Riding\n\nRiding costs 100 gold."))
        self.assertTrue(any("cost needs its source" in p for p in problems))
        problems, _ = self.check(self.page(), self.page("### Riding\n\nRiding costs 100 gold ([Wowhead](https://www.wowhead.com/x))."))
        self.assertFalse(any("cost" in p for p in problems))
        problems, _ = self.check(self.page(), self.page("### Spells\n\nA 30s cooldown ([Wowhead](https://www.wowhead.com/x))."))
        self.assertEqual(problems, [])

    def test_source_summaries_need_links(self):
        problems, _ = self.check(self.page(), self.page("### Talents\n\nThe guides prefer Improved Frostbolt."))
        self.assertTrue(any("without linking" in p for p in problems))

    def test_review_for_new_sites_live_pages_and_outdated_findings(self):
        _, review = self.check(self.page(), self.page("### Talents\n\nSee [a blog](https://example.org/x)."))
        self.assertIn("a link to example.org, a site no page has cited before", review)
        _, review = self.check(self.page(), self.page(), {"updated": TODAY.isoformat(), "status": "live"}, {"status": "pre-launch"})
        self.assertIn("the page is set Live", review)
        old = self.page(findings=f"### Frost is best (idea, {WHEN})\n\nRead on [Wowhead](https://www.wowhead.com/x).")
        new = old.replace("(idea,", "(outdated,")
        _, review = self.check(old, new)
        self.assertIn("finding 'Frost is best' marked outdated", review)

    def test_repeated_headings_and_protocol_relative_links_are_refused(self):
        guides = "### Tazdingo recommendation\n\nKeep Frost.\n\n### Tazdingo recommendation\n\nSwitch to Fire."
        problems, _ = self.check(self.page(), self.page(guides))
        self.assertTrue(any("appears twice" in p for p in problems))
        problems, review = self.check(self.page(), self.page("### Talents\n\nSee [this](//example.org/x)."))
        self.assertIn("write links in full, starting https://", problems)
        self.assertIn("a link to example.org, a site no page has cited before", review)
        for trick in ("https://evil.org\\@wowhead.com/x", "https://user@evil.org/x", "https://wowhead.com.evil.org@x.org/"):
            problems, _ = self.check(self.page(), self.page(f"### Talents\n\nSee [this]({trick})."))
            self.assertTrue(any("plainly" in p for p in problems), trick)

    def test_links_and_headings_are_read_as_the_page_renders(self):
        _, review = self.check(self.page(), self.page("### Gear\n\n| a | b |\n|---|---|\n| https://wowhead.com/x|https://unreviewed.example/x |"))
        self.assertIn("a link to unreviewed.example, a site no page has cited before", review)
        problems, _ = self.check(self.page(), self.page("### Talents\n\nSee `[Wowhead](https://www.wowhead.com/x)`."))
        self.assertTrue(any("without linking" in p for p in problems), "a link inside code isn't a citation")
        problems, _ = self.check(self.page(), self.page(findings="###\tAn unsupported finding\n\nIt's true."))
        self.assertTrue(any("confidence and date" in p for p in problems))
        problems, _ = self.check(self.page(), self.page(findings="Frost is best."))
        self.assertTrue(any("must sit under a finding's heading" in p for p in problems))
        _, review = self.check(self.page("### Talents\n\nx ([Wowhead](https://www.wowhead.com/x))"),
                               self.page("### Talents\n\nx ([Wowhead](https://www.wowhead.com/x))\n\n###\tTazdingo recommendation\n\nGo Fire."))
        self.assertIn("the Tazdingo recommendation changed", review)

    def test_cheatsheet_changes_go_to_review_under_either_name(self):
        old = self.page()
        _, review = self.check(old, old.replace("## At a glance\n\nx", "## Cheatsheet\n\nx"))
        self.assertNotIn("the cheatsheet changed", review, "renaming the section alone isn't an editorial change")
        _, review = self.check(old, old.replace("## At a glance\n\nx", "## Cheatsheet\n\n- **Stats:** hit first"))
        self.assertIn("the cheatsheet changed", review)

    def test_unknown_items_and_messages(self):
        problems, _ = self.check(self.page(), self.page("### Gear\n\n[Linen](https://foreverdb.net/item/999999) ([Wowhead](https://www.wowhead.com/x))."))
        self.assertTrue(any("isn't an item" in p for p in problems))
        self.assertEqual(provenance.message_problems("Frost Mage: Blizzard-kiting from 22, tested"), [])
        self.assertTrue(provenance.message_problems("misc update"))


if __name__ == "__main__":
    unittest.main()

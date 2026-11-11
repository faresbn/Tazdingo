import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import combat_logs

ME, PET, MATE, STRANGER = "Player-1-0000000A", "Pet-0-1-1-1-1-0000000P", "Player-1-0000000B", "Player-1-000000FF"
MOB, BOSS = "Creature-0-1-1-1-100-00000001", "Creature-0-1-1-1-200-00000002"
ADV = "{unit},0000000000000000,100,100,0,0,0,0,0,0,0,0,0,0,0.0,0.0,1424,0.0,25"   # the 19 advanced-logging fields


def line(t, body):
    return f"11/11/2026 18:{t}  {body}\n"


def hit(t, src, src_name, src_flags, dst, dst_name, dst_flags, amount, spell="17919,\"Searing Pain\",0x4"):
    adv = ADV.format(unit=dst)
    return line(t, f'SPELL_DAMAGE,{src},"{src_name}",{src_flags},0x80000000,{dst},"{dst_name}",{dst_flags},0x80000000,'
                   f'{spell},{adv},{amount},{amount},-1,4,0,0,0,nil,nil,nil,ST')


def sample() -> str:
    me = (ME, "Myname-Realm", "0x511")
    out = [line("00:00.0000", "COMBAT_LOG_VERSION,22,ADVANCED_LOG_ENABLED,1,BUILD_VERSION,1.60.1,PROJECT_ID,18"),
           line("00:00.0000", 'ZONE_CHANGE,0,"Hillsbrad Foothills",0'),
           hit("00:01.0000", *me, MOB, "Hillsbrad Footman", "0xa48", 50),
           hit("00:02.0000", PET, "Cenobrus", "0x1111", MOB, "Hillsbrad Footman", "0xa48", 30, '3110,"Firebolt",0x4'),
           hit("00:02.5000", STRANGER, "Strangername-Realm", "0x518", MOB, "Hillsbrad Footman", "0xa48", 999),
           line("00:03.0000", f'SPELL_HEAL,{STRANGER},"Strangername-Realm",0x518,0x80000000,{ME},"Myname-Realm",0x511,0x80000000,'
                              f'774,"Rejuvenation",0x8,{ADV.format(unit=ME)},20,20,0,0,nil'),
           line("00:04.0000", f'UNIT_DIED,0000000000000000,nil,0x80000000,0x80000000,{MOB},"Hillsbrad Footman",0xa48,0x80000000,0'),
           hit("00:05.0000", STRANGER, "Strangername-Realm", "0x548", "Player-1-00000099", "Bystander-Realm", "0x548", 5),
           line("01:00.0000", 'ZONE_CHANGE,33,"Silverpine Forest",0'),
           line("01:00.5000", 'ZONE_CHANGE,33,"Shadowfang Keep",1'),
           line("01:10.0000", 'ENCOUNTER_START,2748,"Rethilgore",1,5,33')]
    for n in range(120):
        out.append(hit(f"01:{11 + n // 10}.{n % 10}000", MATE, "Matename-Realm", "0x512", BOSS, "Rethilgore", "0x10a48", 10))
    out += [hit("01:30.0000", *me, BOSS, "Rethilgore", "0x10a48", 70),
            line("01:31.0000", 'ENCOUNTER_END,2748,"Rethilgore",1,5,1,21000'),
            line("02:00.0000", 'ZONE_CHANGE,0,"Silverpine Forest",0'),
            hit("02:01.0000", MOB, "Hillsbrad Footman", "0xa48", *me, 40)]
    return "".join(out)


class CombatLogs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root, self.game = Path(self.tmp.name) / "repo", Path(self.tmp.name) / "Logs"
        self.root.mkdir(); self.game.mkdir()
        self.log = self.game / "WoWCombatLog-111126_180000.txt"
        self.log.write_text(sample(), encoding="utf-8")
        old = time.time() - 3600
        os.utime(self.log, (old, old))

    def tearDown(self):
        self.tmp.cleanup()

    def run_it(self, **kw):
        return combat_logs.refresh(self.game, None, root=self.root, **kw)

    def files(self):
        return {p.relative_to(self.root).as_posix() for p in (self.root / "logs").rglob("*") if p.is_file()}

    def test_instance_run_is_kept_exactly_with_its_header(self):
        self.run_it()
        run = self.root / "logs/myname/2026-11-11/1801-shadowfang-keep.txt"
        source = self.log.read_bytes()
        header, body = run.read_bytes().split(b"\n", 1)
        self.assertTrue(source.startswith(header + b"\n"))
        self.assertIn(body, source)
        self.assertTrue(body.startswith(b"11/11/2026 18:01:00.0000  ZONE_CHANGE,33"))
        self.assertNotIn(b'ZONE_CHANGE,0,"Silverpine Forest"', body)
        lines = run.read_text().splitlines()
        entry = json.loads((self.root / "logs/sources.json").read_text())["sources"][self.log.name]["written"][0]
        boss = entry["encounters"][0]
        self.assertEqual((boss["name"], boss["result"], boss["seconds"]), ("Rethilgore", "kill", 21))
        self.assertIn("ENCOUNTER_START", lines[boss["start_line"] - 1])
        self.assertIn("ENCOUNTER_END", lines[boss["end_line"] - 1])
        self.assertEqual(entry["players"], ["Matename-Realm"])

    def test_open_world_is_ours_only(self):
        self.run_it()
        summary = (self.root / "logs/myname/2026-11-11/1800-open-world.md").read_text()
        self.assertIn("Searing Pain", summary)
        self.assertIn("Firebolt (pet Cenobrus)", summary)
        self.assertIn("Hillsbrad Footman", summary)
        self.assertIn("From another player: Rejuvenation 20", summary)
        self.assertIn("Kills: 1", summary)
        for other in ("Strangername", "Bystander", "Matename", "999", "Player-"):
            self.assertNotIn(other, summary)

    def test_indexes_and_guide(self):
        self.run_it()
        guide = (self.root / "logs/README.md").read_text()
        self.assertIn("How to use this folder efficiently", guide)
        self.assertIn("logs/myname/2026-11-11/index.md", guide)
        day = (self.root / "logs/myname/2026-11-11/index.md").read_text()
        self.assertIn("| Rethilgore | 18:01 | kill | 21 |", day)
        self.assertIn("1800-open-world.md", day)

    def test_labels_name_the_folders(self):
        combat_logs.refresh(self.game, None, root=self.root)
        self.assertTrue(any("myname" in f for f in self.files()))
        for f in self.files():
            (self.root / f).unlink()
        (self.root / "logs/sources.json").unlink(missing_ok=True)
        orig, orig_load = combat_logs.character_labels, combat_logs.load_foreverdb
        try:
            combat_logs.refresh.__globals__["character_labels"] = lambda db: {ME: "Orc Warlock"}
            combat_logs.refresh.__globals__["load_foreverdb"] = lambda raw: {}
            fake = Path(self.tmp.name) / "ForeverDB.lua"; fake.write_text("x")
            combat_logs.refresh(self.game, fake, root=self.root)
        finally:
            combat_logs.refresh.__globals__["character_labels"] = orig
            combat_logs.refresh.__globals__["load_foreverdb"] = orig_load
        self.assertIn("logs/orc-warlock/2026-11-11/1801-shadowfang-keep.txt", self.files())

    def test_unchanged_waiting_and_old_logs(self):
        self.run_it()
        self.assertEqual(self.run_it()["unchanged"], 1)
        fresh = self.game / "WoWCombatLog-111126_190000.txt"
        fresh.write_text(sample())
        self.assertEqual(self.run_it()["waiting"], [fresh.name])
        week = time.time() - 8 * 86400
        os.utime(self.log, (week, week))
        self.run_it()
        self.assertTrue(self.log.exists(), "filing never deletes")
        self.assertEqual(combat_logs.prune(self.game, self.root), [], "nothing is committed yet")
        git = lambda *a: subprocess.run(["git", "-C", str(self.root), *a], check=True, capture_output=True)
        git("init", "-q"); git("config", "user.email", "t@example.com"); git("config", "user.name", "T")
        git("add", "logs"); git("commit", "-qm", "filed")
        self.assertEqual(combat_logs.prune(self.game, self.root), [self.log.name])
        self.assertFalse(self.log.exists())
        self.assertTrue(fresh.exists(), "a recent log is kept")
        self.assertIn("logs/myname/2026-11-11/1801-shadowfang-keep.txt", self.files())

    def test_prune_keeps_a_log_that_changed_since_filing(self):
        self.run_it()
        git = lambda *a: subprocess.run(["git", "-C", str(self.root), *a], check=True, capture_output=True)
        git("init", "-q"); git("config", "user.email", "t@example.com"); git("config", "user.name", "T")
        git("add", "logs"); git("commit", "-qm", "filed")
        with self.log.open("a") as f:
            f.write("11/11/2026 18:03:00.0000  ZONE_CHANGE,0,\"Hillsbrad Foothills\",0\n")
        week = time.time() - 8 * 86400
        os.utime(self.log, (week, week))
        self.assertEqual(combat_logs.prune(self.game, self.root), [])
        self.assertTrue(self.log.exists())


if __name__ == "__main__":
    unittest.main()

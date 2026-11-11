import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime
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


def git(folder, *args):
    return subprocess.run(["git", "-C", str(folder), *args], check=True, capture_output=True, text=True).stdout.strip()


class CombatLogs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.out, self.game = base / "branch", base / "Logs"
        self.game.mkdir()
        self.log = self.game / "WoWCombatLog-111126_180000.txt"
        self.log.write_text(sample(), encoding="utf-8")
        self.age(self.log, hours=1)
        self.levels = ({ME: "Orc Warlock"}, {ME: 29})
        self.saved = combat_logs.foreverdb_levels
        combat_logs.foreverdb_levels = lambda path: self.levels

    def tearDown(self):
        combat_logs.foreverdb_levels = self.saved
        self.tmp.cleanup()

    def age(self, path, hours=0, days=0):
        when = time.time() - hours * 3600 - days * 86400
        os.utime(path, (when, when))

    def files(self):
        return {p.relative_to(self.out).as_posix() for p in self.out.rglob("*") if p.is_file() and ".git" not in p.parts}

    def entries(self):
        return json.loads((self.out / "sources.json").read_text())["sources"][self.log.name]

    # --- filing

    def test_instance_run_is_kept_exactly_with_its_header(self):
        combat_logs.refresh(self.game, None, self.out)
        run = self.out / "orc-warlock/2026-11-11/1801-shadowfang-keep.txt"
        header, body = run.read_bytes().split(b"\n", 1)
        source = self.log.read_bytes()
        self.assertTrue(source.startswith(header + b"\n"))
        self.assertIn(body, source)
        self.assertTrue(body.startswith(b"11/11/2026 18:01:00.0000  ZONE_CHANGE,33"))
        self.assertNotIn(b'ZONE_CHANGE,0,"Silverpine Forest"', body)
        lines = run.read_text().splitlines()
        boss = self.entries()["written"][0]["encounters"][0]
        self.assertEqual((boss["name"], boss["result"], boss["seconds"]), ("Rethilgore", "kill", 21))
        self.assertIn("ENCOUNTER_START", lines[boss["start_line"] - 1])
        self.assertIn("ENCOUNTER_END", lines[boss["end_line"] - 1])
        self.assertEqual(self.entries()["written"][0]["players"], ["Matename-Realm"])

    def test_open_world_is_ours_only(self):
        combat_logs.refresh(self.game, None, self.out)
        summary = (self.out / "orc-warlock/2026-11-11/1800-open-world.md").read_text()
        for wanted in ("Searing Pain", "Firebolt (pet Cenobrus)", "Hillsbrad Footman", "From another player: Rejuvenation 20", "Kills: 1"):
            self.assertIn(wanted, summary)
        for other in ("Strangername", "Bystander", "Matename", "999", "Player-"):
            self.assertNotIn(other, summary)

    def test_indexes_and_guide(self):
        combat_logs.refresh(self.game, None, self.out)
        guide = (self.out / "README.md").read_text()
        self.assertIn("How to use this folder efficiently", guide)
        self.assertIn("raw.githubusercontent.com/faresbn/Tazdingo/logs/", guide)
        self.assertIn("`orc-warlock/2026-11-11/index.md`", guide)
        day = (self.out / "orc-warlock/2026-11-11/index.md").read_text()
        self.assertIn("| Rethilgore | 18:01 | kill | 21 |", day)
        self.assertIn("1800-open-world.md", day)

    def test_a_settling_log_waits_and_an_unchanged_one_is_left(self):
        combat_logs.refresh(self.game, None, self.out)
        self.assertEqual(combat_logs.refresh(self.game, None, self.out)["unchanged"], 1)
        fresh = self.game / "WoWCombatLog-111126_190000.txt"
        fresh.write_text(sample())
        self.assertEqual(combat_logs.refresh(self.game, None, self.out)["waiting"], [fresh.name])

    # --- level 60

    def test_a_level_60_character_is_skipped_entirely(self):
        self.levels = ({ME: "Orc Warlock"}, {ME: 60})
        report = combat_logs.refresh(self.game, None, self.out)
        self.assertEqual(report["skipped at level 60"], ["Orc Warlock"])
        self.assertFalse(any(f.endswith((".txt", "-open-world.md")) for f in self.files()))
        self.assertEqual(self.entries()["skipped"], ["Orc Warlock"])

    # --- retention

    def test_retention_keeps_14_days_or_the_last_10_whichever_is_more(self):
        self.out.mkdir()
        today = datetime(2026, 12, 31)

        def entry(date, character="Orc Warlock"):
            path = f"{character.lower().replace(' ', '-')}/{date}/0100-x.txt"
            (self.out / path).parent.mkdir(parents=True, exist_ok=True)
            (self.out / path).write_text("x")
            return {"kind": "instance", "character": character, "date": date, "start": "01:00", "file": path}
        recent = [entry(f"2026-12-{d:02d}") for d in range(18, 32)]                    # 14 logs within 14 days: all kept
        old = [entry(f"2026-11-{d:02d}") for d in range(1, 6)]                         # older, beyond the last 10: removed
        idle = [entry(f"2026-10-{d:02d}", "Troll Rogue") for d in range(1, 13)]        # 12 old ones: the last 10 kept
        capped = [entry(f"2026-09-{d:02d}", "Tauren Druid") for d in range(1, 13)]     # level 60: left alone
        record = {"sources": {"a": {"written": recent + old + idle + capped}}}
        removed = combat_logs.retain(record, self.out, {"Tauren Druid": 60, "Orc Warlock": 29}, today)
        self.assertEqual(sorted(removed), sorted(e["file"] for e in old + idle[:2]))
        self.assertTrue(all((self.out / e["file"]).exists() for e in recent + idle[2:] + capped))
        self.assertFalse(any((self.out / e["file"]).exists() for e in old + idle[:2]))
        self.assertTrue(all(e.get("expired") for e in old + idle[:2]))

    # --- the branch: one commit, force-pushed; pruning only what's safely pushed

    def setup_remote(self):
        base = Path(self.tmp.name)
        remote, repo = base / "remote.git", base / "repo"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "config", "user.name", "Test")
        git(repo, "config", "user.email", "test@example.com")
        return remote, repo

    def test_the_branch_never_keeps_history(self):
        remote, repo = self.setup_remote()
        report = combat_logs.run(self.game, None, self.out, repo)
        self.assertNotEqual(report["published"], "unchanged")
        self.assertEqual(git(remote, "rev-list", "--count", "logs"), "1")
        self.assertIn("orc-warlock/2026-11-11/1801-shadowfang-keep.txt", git(remote, "ls-tree", "-r", "--name-only", "logs"))
        self.assertEqual(combat_logs.run(self.game, None, self.out, repo)["published"], "unchanged")
        second = self.game / "WoWCombatLog-111226_180000.txt"
        second.write_text(sample().replace("11/11/2026", "11/12/2026"))
        self.age(second, hours=1)
        combat_logs.run(self.game, None, self.out, repo)
        self.assertEqual(git(remote, "rev-list", "--count", "logs"), "1", "still a single commit")
        self.assertIn("orc-warlock/2026-11-12/index.md", git(remote, "ls-tree", "-r", "--name-only", "logs"))
        self.assertEqual(git(self.out, "log", "-1", "--format=%ae"), "test@example.com")

    def test_old_game_logs_go_only_once_pushed_and_never_at_60(self):
        remote, repo = self.setup_remote()
        combat_logs.checkout(self.out, repo)
        combat_logs.refresh(self.game, None, self.out)
        self.age(self.log, days=8)
        self.assertEqual(combat_logs.prune(self.game, self.out), [], "nothing is pushed yet")
        combat_logs.run(self.game, None, self.out, repo)   # re-files (its time changed), pushes, then prunes
        self.assertFalse(self.log.exists())
        capped = self.game / "WoWCombatLog-111026_180000.txt"
        capped.write_text(sample())
        self.age(capped, hours=1)
        self.levels = ({ME: "Orc Warlock"}, {ME: 60})
        combat_logs.run(self.game, None, self.out, repo)
        self.age(capped, days=8)
        combat_logs.run(self.game, None, self.out, repo)
        self.assertTrue(capped.exists(), "a level-60 character's log is never deleted")


if __name__ == "__main__":
    unittest.main()

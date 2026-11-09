import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from auctionator import InvalidCapture
import characters

OWN, OWN2, OTHER = "Player-1-0000000A", "Player-1-0000000B", "Player-1-000000FF"


def record(guid, name, level, cls="Warlock", race="Orc"):
    return f'''["{guid}"] = {{
        ["name"] = "{name}", ["surname"] = "Secretsurname", ["guid"] = "{guid}", ["realm"] = "Hiddenrealm",
        ["class"] = "{cls}", ["race"] = "{race}", ["faction"] = "Horde", ["level"] = {level}, ["ilvl"] = 23.9,
        ["time"] = 1794228911, ["reason"] = "logout", ["build"] = "70862",
        ["gear"] = {{ [1] = {{ ["ilvl"] = 25, ["link"] = "|cnIQ2:|Hitem:7048::::::::1:1486::75:::::::|h[Shadow Circlet]|h|r" }},
                      [2] = false,
                      [5] = {{ ["ilvl"] = 20, ["link"] = "|cnIQ2:|Hitem:14096::::::::1:1486::75:::::::|h[Filigreed Shadow Gown]|h|r" }} }},
        ["talents"] = {{ ["import"] = "CIdBa0K", ["trees"] = {{ [1] = {{ ["groups"] = {{
            [1] = {{ ["name"] = "Affliction" }}, [2] = {{ ["name"] = "Demonology", ["spent"] = 20 }} }} }} }} }},
        ["professions"] = {{ [1] = {{ ["name"] = "Tailoring", ["rank"] = 130, ["max"] = 150 }} }},
        ["skills"] = {{ [1] = {{ ["name"] = "Wands", ["cat"] = "Weapon Skills", ["rank"] = 123, ["max"] = 145 }} }},
        ["reps"] = {{ [1] = {{ ["name"] = "Orgrimmar", ["id"] = 76, ["reaction"] = 6, ["standing"] = 10822, ["lo"] = 9000, ["hi"] = 21000 }},
                      [2] = {{ ["name"] = "Secretguild", ["id"] = 1168, ["reaction"] = 5, ["standing"] = 100, ["lo"] = 0, ["hi"] = 3000 }},
                      [3] = {{ ["name"] = "Unknownheader", ["reaction"] = 4 }} }},
        ["stats"] = {{ ["health"] = 1241, ["int"] = 99 }}, ["pvp"] = {{ ["hk"] = 3, ["honorPoints"] = 34 }},
        ["mounts"] = 2, ["pets"] = 4,
    }},'''


def lua(armory: str, own=(OWN, OWN2)) -> bytes:
    recaps = ", ".join(f'["{g}"] = {{}}' for g in own)
    return f'''ForeverDB_DB = {{
    ["armory"] = {{ {armory} }},
    ["coachRecaps"] = {{ {recaps} }},
    ["botSuspects"] = {{ ["Botname Verol-Realm"] = {{ ["n"] = 13 }} }},
    ["knowers"] = {{ ["mine"] = {{ ["Guildmate"] = 1 }} }},
    ["collections"] = {{ ["{OWN}"] = {{ ["name"] = "Mainname", ["mounts"] = {{ [1] = 1309208, [2] = 1309405 }}, ["titles"] = {{}} }} }},
}}
'''.encode()


SAMPLE = lua(record(OWN, "Mainname", 29) + record(OWN2, "Altname", 12) + record(OTHER, "Strangername", 60, "Rogue", "Troll"))


class Characters(unittest.TestCase):
    def test_only_own_characters_under_labels(self):
        chars = characters.extract(SAMPLE)["characters"]
        self.assertEqual([c["label"] for c in chars], ["Orc Warlock", "Orc Warlock 2"])
        self.assertEqual([c["level"] for c in chars], [29, 12])

    def test_no_names_ids_realms_or_other_players(self):
        out = json.dumps(characters.extract(SAMPLE))
        for secret in ("Mainname", "Altname", "Strangername", "Secretsurname", "Hiddenrealm", "Player-", "Botname",
                       "Guildmate", "Verol", "Secretguild", "Unknownheader"):
            self.assertNotIn(secret, out)

    def test_progression_fields(self):
        c = characters.extract(SAMPLE)["characters"][0]
        self.assertEqual(c["gear"], [{"slot": "Head", "item": 7048, "name": "Shadow Circlet", "item_level": 25},
                                     {"slot": "Chest", "item": 14096, "name": "Filigreed Shadow Gown", "item_level": 20}])
        self.assertEqual(c["talents"], {"points": {"Affliction": 0, "Demonology": 20}, "loadout": "CIdBa0K"})
        self.assertEqual(c["professions"], [{"name": "Tailoring", "skill": 130, "max": 150}])
        self.assertEqual(c["reputations"], [{"name": "Orgrimmar", "standing": "Honored", "progress": 1822, "needed": 12000}])
        self.assertEqual(c["recorded_at"], "2026-11-09T12:55:11Z")
        self.assertEqual(c["collected"], {"mounts": 2, "pets": 4, "titles": 0})

    def test_no_own_characters_is_refused(self):
        with self.assertRaises(InvalidCapture):
            characters.extract(lua(record(OTHER, "Strangername", 60), own=()))

    def test_not_foreverdb_is_refused(self):
        with self.assertRaises(InvalidCapture):
            characters.extract(b"Auctionator = {}\n")

    def test_refresh_writes_the_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, source = Path(tmp), Path(tmp) / "ForeverDB.lua"
            (root / "data").mkdir()
            source.write_bytes(SAMPLE)
            characters.refresh(source, root)
            self.assertEqual(len(json.loads((root / "data/characters.json").read_text())["characters"]), 2)


if __name__ == "__main__":
    unittest.main()

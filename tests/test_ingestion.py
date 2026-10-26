import hashlib
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from auctionator import CBOR, InvalidCapture, LuaData, day_date, item_id, parse_capture, string_keys, suffix
from build import build_markets, collect, load_journal
from markup import render


class SafeFormats(unittest.TestCase):
    def test_lua_binary_escapes(self):
        self.assertEqual(LuaData(b'A = "a\\000\\255\\n\\\"\\\\"').read()["A"],b'a\x00\xff\n"\\')
    def test_executable_lua_rejected(self):
        for value in (b'A = os.execute("whoami")',b'A = {}\nprint("hello")',b'A = (function() return {} end)()',b'A = { ["x"]=1, ["x"]=2 }'):
            with self.subTest(value=value):
                with self.assertRaises(InvalidCapture): LuaData(value).read()
    def test_cbor_rfc_vectors(self):
        self.assertEqual(CBOR(bytes.fromhex("a14161190100")).complete(),{b"a":256})
        self.assertEqual(CBOR(bytes.fromhex("83010203")).complete(),[1,2,3])
    def test_malformed_cbor_rejected(self):
        for raw in (b'\x19',b'\x01\x01',b'\x9f\xff',b'\xa2Aa\x01Aa\x02',b'\xfb'+b'\x00'*8,b'\xd8\x18\x00',b'\x59\xff\xff'):
            with self.subTest(raw=raw):
                with self.assertRaises(InvalidCapture): CBOR(raw).complete()
    def test_bounded_lua(self):
        with self.assertRaises(InvalidCapture): LuaData(b'A='+b'{'*40+b'}'*40).read()
    def test_normalised_key_collision_rejected(self):
        with self.assertRaises(InvalidCapture): string_keys({b"m":1,"m":2})
    def test_markdown_escapes_html_and_unsafe_links(self):
        out=render("<script>x</script> [a](javascript:alert(1)) **b**")
        self.assertNotIn("<script>",out); self.assertNotIn('href="javascript',out); self.assertIn("<strong>b</strong>",out)
    def test_markdown_tables_and_lists(self):
        out=render("## Gear\n\n- one\n  - two\n\n| A | B |\n|---|--:|\n| x | 1 |")
        self.assertIn("<h2>Gear</h2>",out); self.assertIn("<ul><li>one<ul><li>two</li></ul></li></ul>",out)
        self.assertIn('<td style="text-align:right">1</td>',out)


def cbor(value):
    """Minimal CBOR encoder for building Auctionator-shaped fixtures."""
    def head(major, n):
        if n < 24: return bytes([major<<5|n])
        for extra, size in ((24,1),(25,2),(26,4),(27,8)):
            if n < 1 << (8*size): return bytes([major<<5|extra]) + n.to_bytes(size,"big")
    if isinstance(value, int): return head(0, value)
    if isinstance(value, str): raw=value.encode(); return head(3, len(raw)) + raw
    if isinstance(value, dict): return head(5, len(value)) + b"".join(cbor(k)+cbor(v) for k,v in value.items())
    raise TypeError(value)


def saved_variables(markets):
    """A SavedVariables file holding the given {market name: payload bytes}."""
    def lua_string(raw):
        return b'"' + b"".join(b"\\%03d" % c if c < 32 or c in (34,92) or c > 126 else bytes([c]) for c in raw) + b'"'
    rows = b"".join(b'["' + name.encode() + b'"] = ' + lua_string(payload) + b",\n" for name,payload in markets.items())
    return (b'AUCTIONATOR_PRICE_DATABASE = {\n["__dbversion"] = 8,\n' + rows + b'}\n'
            b'AUCTIONATOR_SAVEDVARS = {\n["TimeOfLastBrowseScan"] = 1792240585,\n}\n')


class CurrentAuctionatorFormat(unittest.TestCase):
    record = {"m": 5000, "h": {"2481": 5000}, "l": {}, "a": {"2481": 3}}

    def write(self, markets):
        import tempfile
        handle = tempfile.NamedTemporaryFile(suffix=".lua", delete=False)
        handle.write(saved_variables(markets)); handle.close()
        self.addCleanup(Path(handle.name).unlink)
        return Path(handle.name)

    def test_random_suffix_keys_accepted(self):
        path = self.write({"Realm Horde": cbor({"version": 2, "9807": self.record, "gr:9807:of the Boar": self.record})})
        items = parse_capture(path)["markets"]["Realm Horde"]["items"]
        self.assertEqual(sorted(items), ["9807", "gr:9807:of the Boar"])
        self.assertEqual((item_id("gr:9807:of the Boar"), suffix("gr:9807:of the Boar")), (9807, "of the Boar"))

    def test_unpublished_broken_market_does_not_block_scan(self):
        path = self.write({"Old Realm": b"\x01\x90\x1b", "Realm Horde": cbor({"version": 2, "2589": self.record})})
        self.assertEqual(list(parse_capture(path, markets=["Realm Horde"])["markets"]), ["Realm Horde"])
        with self.assertRaises(InvalidCapture): parse_capture(path)
        with self.assertRaises(InvalidCapture): parse_capture(path, markets=["Missing"])

    def test_malformed_text_is_a_clean_rejection(self):
        with self.assertRaises(InvalidCapture): CBOR(b"\x61\xa4").complete()

    def test_day_codes_match_auctionator_day_zero(self):
        # Beta capture of 17 October 2026 has day code 2481 as its newest day.
        self.assertEqual(day_date(2481), "2026-10-17")


class OriginalCaptures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fingerprints=["249ef1a7d3a1bef1af965b32ea8bed90b199c9fc001351df19853aa3be06ae45","ea7c4b2a9cfd82cc7c53fdc7f2062892691e64eb0e1da0cc1ad1c6adbf933b1c","2f5fb65c7631270feb6241f5da2d7ba2bfaa0f7535ec03671e52257d0dce2c75"]
        by_hash={c["source_sha256"]:c for c in collect()}
        cls.captures=[by_hash[k] for k in fingerprints]
    def test_recorded_source_fingerprints(self):
        self.assertEqual([c["source_sha256"] for c in self.captures],[
            "249ef1a7d3a1bef1af965b32ea8bed90b199c9fc001351df19853aa3be06ae45",
            "ea7c4b2a9cfd82cc7c53fdc7f2062892691e64eb0e1da0cc1ad1c6adbf933b1c",
            "2f5fb65c7631270feb6241f5da2d7ba2bfaa0f7535ec03671e52257d0dce2c75"])
    def test_selected_sample_counts(self):
        self.assertEqual([len(c["markets"]["PvP"]["items"]) for c in self.captures],[24]*3)
        self.assertEqual([len(c["markets"]["ClassicBetaPvP"]["items"]) for c in self.captures],[6]*3)
        self.assertTrue(all(c["sample"]["complete_market"] is False for c in self.captures))
    def test_source_timestamps(self):
        self.assertEqual([c["capture_time"] for c in self.captures],["2026-10-06T09:31:22Z","2026-10-10T12:46:23Z","2026-10-17T12:36:25Z"])
    def test_raw_derived_sample_prices(self):
        # Item 236 is directly traceable in the CBOR market strings (m values).
        self.assertEqual([c["markets"]["PvP"]["items"]["236"]["m"] for c in self.captures],[6700,900,5000])
        self.assertTrue(all(c["markets"]["ClassicBetaPvP"]["items"]["15115"]["m"]==1000 for c in self.captures))
    def test_unchanged_market_marked_not_new(self):
        markets={m["slug"]:m for m in build_markets(self.captures,{})}
        self.assertEqual([s["unchanged"] for s in markets["forever-beta-classicbetapvp"]["scans"]],[False,True,True])
        self.assertEqual([s["unchanged"] for s in markets["forever-beta-pvp"]["scans"]],[False,False,False])
    def test_daily_history_merges_across_scans(self):
        pvp={m["slug"]:m for m in build_markets(self.captures,{"236":"Cured Leather Armor"})}["forever-beta-pvp"]
        item=next(i for i in pvp["items"] if i["key"]=="236")
        self.assertEqual((item["name"],item["price"],item["price_scan"]),("Cured Leather Armor",5000,"2026-10-17"))
        self.assertEqual(item["last_seen"],"2026-10-14")  # newest daily record, not the file date
        self.assertEqual(item["days"][2462]["high"],2800)  # day kept from the 6 October scan
    def test_input_order_does_not_rewrite_chronology(self):
        # collect() establishes verified file chronology before grouping.
        self.assertEqual([c["capture_date"] for c in self.captures],["2026-10-06","2026-10-10","2026-10-17"])
    def test_originals_match_market_projection_when_available(self):
        import json
        receipts=json.loads((ROOT/"data/captures.json").read_text())["captures"]
        paths=[ROOT/r["private_original_path"] for r in receipts if "private_original_path" in r]
        if not paths or not all(p.is_file() for p in paths):
            self.skipTest("Original Lua kept outside repository pending explicit upload approval; checked locally")
        original={parse_capture(p)["source_sha256"]:parse_capture(p) for p in paths}
        for capture in self.captures:
            for name,market in capture["markets"].items():
                full=original[capture["source_sha256"]]["markets"][name]
                self.assertEqual(len(full["items"]),capture["sample"]["original_market_counts"][name])
                for key,fields in market["items"].items():
                    self.assertEqual(fields,full["items"][key])


if __name__=="__main__": unittest.main()

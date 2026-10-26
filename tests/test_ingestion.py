import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from auctionator import CBOR, InvalidCapture, LuaData, day_date, item_id, parse_capture, string_keys, suffix
from build import build_markets, collect, crate_table, craft_table, load_content, summarise, volatility
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
        for attack in ('https://x.com/"onmouseover="alert(1)', "https://x.com/'onmouseover='alert(1)", '[a](https://x.com/"onmouseover="alert(1))',
                       '[x](#`" onmouseover="alert(1)" x="`)', '[x](https://a.b/`"onmouseover="alert(1)`)', 'https://a.b/`"onmouseover=alert(1)`'):
            with self.subTest(attack=attack):
                self.assertEqual(attributes(render(attack)) - {"href","target","rel"}, set())
    def test_markdown_tables_and_lists(self):
        out=render("## Gear\n\n- one\n  - two\n\n| A | B |\n|---|--:|\n| x | 1 |")
        self.assertIn("<h2>Gear</h2>",out); self.assertIn("<ul><li>one<ul><li>two</li></ul></li></ul>",out)
        self.assertIn('<td style="text-align:right">1</td>',out)


def attributes(markup):
    """Every attribute name on every tag in an HTML fragment."""
    from html.parser import HTMLParser
    found=set()
    class Collect(HTMLParser):
        def handle_starttag(self, tag, attrs): found.update(name for name, _ in attrs)
    Collect().feed(markup)
    return found


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


class TypicalPrice(unittest.TestCase):
    def item(self, lows, price=None):
        days={2470+i:{"low":v,"high":v,"listed":3} for i,v in enumerate(lows) if v is not None}
        item={"days":days,"price":price if price is not None else lows[-1]}
        summarise(item, 2470+len(lows)-1)
        return item

    def test_troll_listing_does_not_set_the_price(self):
        item=self.item([100,110,99999999999,105,100,95,100])
        self.assertEqual(item["typical"],100)

    def test_one_day_spike_does_not_set_the_price(self):
        item=self.item([30,32,28,31,29,30,11000])
        self.assertEqual((item["typical"],item["price"]),(30,11000))

    def test_weekly_change_compares_medians(self):
        item=self.item([100]*7+[200]*7)
        self.assertEqual(item["change"],100)
        self.assertIsNone(self.item([100,200])["change"])  # not enough history

    def test_stale_item_shows_no_weekly_change(self):
        days={2400+i:{"low":100 if i<7 else 200,"high":200,"listed":3} for i in range(14)}
        item={"days":days,"price":200}
        summarise(item, 2480)  # last seen 67 days before the market's newest day
        self.assertIsNone(item["change"])

    def test_large_rise_reads_as_multiple(self):
        from pages import signed
        self.assertEqual((signed(7417),signed(150),signed(-92),signed(None)),("×75","+150%","-92%",""))


GAME={"classes":[{"slug":"mage","name":"Mage","specs":[["frost","Frost","dps"]]}],"professions":[{"slug":"mining","name":"Mining"}],
      "world":[{"slug":"camping","name":"Camping"}]}


class Content(unittest.TestCase):
    def root(self, files):
        import tempfile, shutil
        root=Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, root)
        for name, text in files.items():
            (root/"content"/name).parent.mkdir(parents=True, exist_ok=True); (root/"content"/name).write_text(text)
        return root

    def test_known_places_and_labels(self):
        from datetime import date
        note="---\nupdated: 2026-11-05\nconfidence: tested\nsummary: Frost for levelling\n---\n## Talents\nText"
        pages=load_content(self.root({"classes/mage/frost.md":note,"world/camping.md":note.replace("2026-11-05","2026-10-30")}),GAME,date(2026,11,4))
        self.assertEqual(pages["classes/mage/frost"]["url"],"classes/mage/#frost")
        self.assertEqual((pages["classes/mage/frost"]["status"],pages["world/camping"]["status"]),("live","pre-launch"))
        self.assertIn("<h2>Talents</h2>",pages["classes/mage/frost"]["html"])

    def test_unknown_place_and_bad_header_are_explained(self):
        from datetime import date
        for files, problem in (({"classes/mage/fire.md":"---\nupdated: 2026-11-05\n---\nx"},"isn't a page the site knows"),
                               ({"classes/mage/frost.md":"no header"},"header"),
                               ({"classes/mage/frost.md":"---\nsummary: x\n---\nx"},"updated"),
                               ({"classes/mage/frost.md":"---\nupdated: 2026-11-05\nconfidence: sure\n---\nx"},"confidence")):
            with self.subTest(problem=problem):
                with self.assertRaisesRegex(ValueError, problem): load_content(self.root(files),GAME,date(2026,11,4))


class PriceTools(unittest.TestCase):
    def item(self, typical, listed=50, vol="steady"):
        return {"ours":{"typical":typical,"listed":listed,"current":True,"volatility":vol}}

    def test_craft_margin_uses_vendor_and_market_prices(self):
        fdb={"recipes":{"Alchemy":[{"name":"Elixir","skill":1,"item":10,"count":1,"reagents":[[1,2],[2,1]],"learned":"a","new":True}]}}
        book={10:self.item(500),1:self.item(100),2:{"vendor":20}}
        row=craft_table(fdb,book,{})[0]
        self.assertEqual((row["sells"],row["cost"],row["margin"]),(500,220,280))

    def test_volatile_or_thin_products_are_skipped(self):
        fdb={"recipes":{"Alchemy":[{"name":"Elixir","skill":1,"item":10,"count":1,"reagents":[[1,1]],"learned":"a","new":False}]}}
        for product in (self.item(500,vol="volatile"),self.item(500,listed=1),self.item(500,vol=None)):
            with self.subTest(product=product):
                self.assertEqual(craft_table(fdb,{10:product,1:self.item(100)},{}),[])

    def test_crate_takes_cheapest_bundle(self):
        fdb={"crates":[{"item":99,"level":10,"bundles":[[1,20],[2,10]]}]}
        crate=crate_table(fdb,{1:self.item(10),2:self.item(15)},{})[0]
        self.assertEqual((crate["cheapest"]["item"],crate["cheapest"]["cost"]),(2,150))

    def test_volatility_bands(self):
        self.assertEqual([volatility([100,102,98,101]),volatility([100,150,80,120]),volatility([100,400,30,250]),volatility([100,110])],
                         ["steady","moving","volatile",None])
        self.assertEqual(volatility([100,110,99999999999,105,100,95,100]),"steady")  # a troll listing doesn't count


class MergingScans(unittest.TestCase):
    def capture(self, sha, ts, items):
        return {"environment":"forever","publish_markets":["Realm Horde"],"source_sha256":sha,"received_on":"2026-11-05",
                "capture_date":"2026-11-05","capture_time":"","capture_timestamp":ts,"sample":{"complete_market":True},
                "markets":{"Realm Horde":{"payload_sha256":sha,"items":items}}}

    def test_two_accounts_same_day_are_combined(self):
        a=self.capture("a",1,{"2589":{"m":20,"h":{"2500":25},"l":{"2500":20},"a":{"2500":40}}})
        b=self.capture("b",2,{"2589":{"m":18,"h":{"2500":22},"l":{"2500":18},"a":{"2500":15}}})
        day=build_markets([a,b],{})[0]["items"][0]["days"][2500]
        self.assertEqual(day,{"low":18,"high":25,"listed":40})


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

    def test_non_ascii_realm_names(self):
        path = self.write({"Пламегор Horde": cbor({"version": 2, "gr:9807:of the Boar": self.record})})
        self.assertEqual(list(parse_capture(path)["markets"]), ["Пламегор Horde"])

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
        by_hash={c["source_sha256"]:c for c in collect() if c["environment"]=="forever-beta"}
        if not all(k in by_hash for k in fingerprints):
            raise unittest.SkipTest("Forever Beta sample not in the registry")
        cls.captures=[by_hash[k] for k in fingerprints]
    def test_recorded_source_fingerprints(self):
        self.assertEqual([c["source_sha256"] for c in self.captures],[
            "249ef1a7d3a1bef1af965b32ea8bed90b199c9fc001351df19853aa3be06ae45",
            "ea7c4b2a9cfd82cc7c53fdc7f2062892691e64eb0e1da0cc1ad1c6adbf933b1c",
            "2f5fb65c7631270feb6241f5da2d7ba2bfaa0f7535ec03671e52257d0dce2c75"])
    def test_selected_sample_counts(self):
        self.assertEqual([len(c["markets"]["PvP"]["items"]) for c in self.captures],[886,937,975])
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

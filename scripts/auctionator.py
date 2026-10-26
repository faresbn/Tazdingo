"""Bounded readers for data-only SavedVariables and Auctionator's CBOR payloads.

No Lua runtime, eval, subprocess or addon code is used. CBOR follows RFC 8949;
only the definite-length types required by the captured schema are accepted.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, timedelta
from pathlib import Path

PARSER_VERSION = "1.1.0"
MAX_FILE = 32 * 1024 * 1024

# Item keys Auctionator writes (Source/Utilities/DBKeyFromLink.lua): a plain item ID,
# "gr:<id>:<suffix>" for random-suffix gear on the legacy AH, "g:<id>:<item level>" and
# "p:<species>" on the modern AH. "<id>:<n>..." covers older variant keys.
ITEM_KEY = re.compile(r"\d+(?::[0-9:-]+)?|gr:\d+:[^\x00-\x1f:]{1,80}|g:\d+:\d+|p:\d+")

# Auctionator's day codes count days since local midnight, 1 January 2020
# (Source/Constants/Main.lua: SCAN_DAY_0; Source/Database/Mixin.lua: GetScanDay).
DAY_ZERO = date(2020, 1, 1)


def item_id(key: str) -> int:
    """The game item ID inside any item key (the species ID for battle pets)."""
    parts = key.split(":")
    return int(parts[1] if parts[0] in ("gr", "g", "p") else parts[0])


def suffix(key: str) -> str | None:
    return key.split(":", 2)[2] if key.startswith("gr:") else None


def day_date(code: int | str) -> str:
    return (DAY_ZERO + timedelta(days=int(code))).isoformat()


def newest_day(markets: dict) -> int | None:
    """The newest Auctionator day with any record: the scan's date in the
    player's own calendar (file timestamps are UTC and can fall a day off)."""
    days = [int(d) for market in markets.values() for item in market["items"].values() for d in item["h"]]
    return max(days) if days else None


class InvalidCapture(ValueError):
    pass


class LuaData:
    def __init__(self, data: bytes):
        if len(data) > MAX_FILE:
            raise InvalidCapture("SavedVariables file exceeds 16 MiB")
        self.data, self.pos, self.nodes = data, 0, 0

    def skip(self):
        while self.pos < len(self.data):
            if self.data[self.pos] in b" \r\n\t\v\f":
                self.pos += 1
            elif self.data[self.pos:self.pos+2] == b"--":
                self.pos += 2
                end = self.data.find(b"\n", self.pos)
                self.pos = len(self.data) if end < 0 else end + 1
            else:
                break

    def expect(self, token: bytes):
        self.skip()
        if not self.data.startswith(token, self.pos):
            raise InvalidCapture(f"Expected {token!r} at byte {self.pos}")
        self.pos += len(token)

    def string(self) -> bytes:
        quote = self.data[self.pos]
        self.pos += 1
        result = bytearray()
        escapes = {97:7, 98:8, 102:12, 110:10, 114:13, 116:9, 118:11,
                   92:92, 34:34, 39:39}
        while self.pos < len(self.data):
            c = self.data[self.pos]
            self.pos += 1
            if c == quote:
                return bytes(result)
            if c in (10, 13):
                raise InvalidCapture("Unescaped newline in Lua short string")
            if c != 92:
                result.append(c)
                continue
            if self.pos >= len(self.data):
                raise InvalidCapture("Truncated Lua escape")
            c = self.data[self.pos]
            self.pos += 1
            if c in escapes:
                result.append(escapes[c])
            elif 48 <= c <= 57:
                digits = bytes([c])
                while len(digits) < 3 and self.pos < len(self.data) and 48 <= self.data[self.pos] <= 57:
                    digits += self.data[self.pos:self.pos+1]
                    self.pos += 1
                value = int(digits)
                if value > 255:
                    raise InvalidCapture("Lua byte escape out of range")
                result.append(value)
            elif c == 120:
                h = self.data[self.pos:self.pos+2]
                if not re.fullmatch(b"[0-9a-fA-F]{2}", h):
                    raise InvalidCapture("Invalid Lua hex escape")
                result.append(int(h, 16))
                self.pos += 2
            elif c == 122:
                while self.pos < len(self.data) and self.data[self.pos] in b" \t\r\n\v\f":
                    self.pos += 1
            elif c in (10,13):
                if c == 13 and self.data[self.pos:self.pos+1] == b"\n":
                    self.pos += 1
                result.append(10)
            else:
                raise InvalidCapture(f"Unsupported Lua escape at byte {self.pos}")
        raise InvalidCapture("Unterminated Lua string")

    def value(self, depth=0):
        self.skip()
        self.nodes += 1
        if depth > 32 or self.nodes > 2_000_000:
            raise InvalidCapture("Lua structure limit exceeded")
        if self.pos >= len(self.data):
            raise InvalidCapture("Missing Lua value")
        c = self.data[self.pos]
        if c in (34,39):
            return self.string()
        if c == 123:
            self.pos += 1
            table, index = {}, 1
            while True:
                self.skip()
                if self.data[self.pos:self.pos+1] == b"}":
                    self.pos += 1
                    return table
                if self.data[self.pos:self.pos+1] == b"[":
                    self.pos += 1
                    key = self.value(depth+1)
                    self.expect(b"]")
                    self.expect(b"=")
                    value = self.value(depth+1)
                else:
                    field = re.match(rb"([A-Za-z_][A-Za-z0-9_]*)\s*=", self.data[self.pos:])
                    if field:
                        key = field.group(1)
                        self.pos += field.end()
                        value = self.value(depth+1)
                    else:
                        key, value = index, self.value(depth+1)
                        index += 1
                if type(key) not in (bytes, int) or key in table:
                    raise InvalidCapture("Invalid or duplicate Lua table key")
                table[key] = value
                self.skip()
                if self.data[self.pos:self.pos+1] in (b",",b";"):
                    self.pos += 1
                elif self.data[self.pos:self.pos+1] != b"}":
                    raise InvalidCapture(f"Unsupported Lua expression at byte {self.pos}")
        number = re.match(rb"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", self.data[self.pos:])
        if number:
            self.pos += number.end()
            raw = number.group()
            return float(raw) if b"." in raw or b"e" in raw.lower() else int(raw)
        for literal, value in ((b"true", True),(b"false",False),(b"nil",None)):
            if self.data.startswith(literal, self.pos):
                self.pos += len(literal)
                return value
        raise InvalidCapture(f"Executable or unsupported Lua at byte {self.pos}")

    def read(self):
        values = {}
        while True:
            self.skip()
            if self.pos == len(self.data):
                return values
            name = re.match(rb"[A-Z_][A-Z_0-9]*", self.data[self.pos:])
            if not name:
                raise InvalidCapture(f"Unsupported Lua statement at byte {self.pos}")
            self.pos += name.end()
            self.expect(b"=")
            key = name.group().decode("ascii")
            if key in values:
                raise InvalidCapture("Duplicate global assignment")
            values[key] = self.value()


class CBOR:
    def __init__(self, data: bytes):
        if len(data) > MAX_FILE:
            raise InvalidCapture("CBOR payload too large")
        self.data, self.pos, self.nodes = data, 0, 0

    def take(self, count):
        if count < 0 or self.pos+count > len(self.data):
            raise InvalidCapture("Truncated CBOR payload")
        result = self.data[self.pos:self.pos+count]
        self.pos += count
        return result

    def read(self, depth=0):
        self.nodes += 1
        if depth > 16 or self.nodes > 2_000_000:
            raise InvalidCapture("CBOR structure limit exceeded")
        head = self.take(1)[0]
        major, extra = head >> 5, head & 31
        if major == 7:
            if extra in (20,21,22):
                return {20:False,21:True,22:None}[extra]
            raise InvalidCapture("CBOR floats/simple values are unsupported")
        if extra < 24:
            length = extra
        elif extra in (24,25,26,27):
            length = int.from_bytes(self.take(1 << (extra-24)),"big")
        else:
            raise InvalidCapture("Indefinite/reserved CBOR encoding")
        if major in (0,1):
            return length if major == 0 else -1-length
        if length > 200_000:
            raise InvalidCapture("CBOR collection/string limit exceeded")
        if major in (2,3):
            raw = self.take(length)
            if major == 2:
                return raw
            try:
                return raw.decode("utf-8")
            except UnicodeDecodeError:
                raise InvalidCapture(f"Malformed CBOR text at byte {self.pos-length}") from None
        if major == 4:
            return [self.read(depth+1) for _ in range(length)]
        if major == 5:
            result = {}
            for _ in range(length):
                key = self.read(depth+1)
                if type(key) not in (str,bytes,int) or key in result:
                    raise InvalidCapture("Invalid or duplicate CBOR map key")
                result[key] = self.read(depth+1)
            return result
        raise InvalidCapture("Unsupported CBOR tag/type")

    def complete(self):
        value = self.read()
        if self.pos != len(self.data):
            raise InvalidCapture("Trailing bytes after CBOR payload")
        return value


def text(value):
    if isinstance(value, bytes):
        return value.decode("ascii")
    if isinstance(value, str):
        return value
    raise InvalidCapture("Expected an ASCII key")


def string_keys(mapping):
    result = {}
    for key,value in mapping.items():
        key = text(key)
        if key in result:
            raise InvalidCapture("Duplicate key after byte/text normalisation")
        result[key] = value
    return result


def load_market_extract(path: Path) -> dict:
    """Validate a market-only projection; never accept unrelated addon fields."""
    with path.open("rb") as source:
        raw=source.read(MAX_FILE+1)
    if len(raw)>MAX_FILE:
        raise InvalidCapture("Market extraction exceeds size limit")
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result: raise InvalidCapture("Duplicate extraction key")
            result[key]=value
        return result
    data=json.loads(raw,object_pairs_hook=unique)
    allowed={"source_sha256","source_bytes","database_version","parser_version","source_scan_timestamps","markets","capture_format","validation_scope","sample"}
    if set(data)!=allowed or data["capture_format"]!="market-only-extract-v1" or data["database_version"]!=8:
        raise InvalidCapture("Unsupported or non-market extraction")
    if not re.fullmatch(r"[a-f0-9]{64}",data["source_sha256"]):
        raise InvalidCapture("Invalid original source fingerprint")
    if type(data["source_bytes"]) is not int or not 0<data["source_bytes"]<=MAX_FILE:
        raise InvalidCapture("Invalid original source size")
    if not isinstance(data["source_scan_timestamps"],dict) or any(type(v) is not int for v in data["source_scan_timestamps"].values()):
        raise InvalidCapture("Invalid source scan timestamps")
    for key,market in data["markets"].items():
        if set(market)!={"payload_sha256","items"} or not re.fullmatch(r"[a-f0-9]{64}",market["payload_sha256"]):
            raise InvalidCapture("Invalid market extraction")
        for item_key,fields in market["items"].items():
            if not ITEM_KEY.fullmatch(item_key) or set(fields)!={"m","a","h","l"}:
                raise InvalidCapture("Invalid market item")
            if type(fields["m"]) is not int or fields["m"]<0:
                raise InvalidCapture("Invalid extracted price")
            for name in ("a","h","l"):
                if not isinstance(fields[name],dict) or any(not day.isdigit() or type(v) is not int or v<0 for day,v in fields[name].items()):
                    raise InvalidCapture("Invalid extracted daily aggregate")
    return data


def decode_market(payload: bytes) -> dict:
    """Decode one market's CBOR string into {item key: {m, a, h, l}}."""
    if not isinstance(payload, bytes):
        raise InvalidCapture("Expected a CBOR-encoded market string")
    if payload[:1] == b"\x01":
        raise InvalidCapture("Market uses Auctionator's older serialiser; scan it again in game to refresh it")
    market = CBOR(payload).complete()
    if not isinstance(market, dict):
        raise InvalidCapture("Expected a market map")
    market = string_keys(market)
    if market.pop("version", None) != 2:
        raise InvalidCapture("Only market version 2 is supported")
    items = {}
    for item_key, fields in market.items():
        if not ITEM_KEY.fullmatch(item_key):
            raise InvalidCapture(f"Unsupported item key {item_key!r}")
        if not isinstance(fields, dict):
            raise InvalidCapture("Item record must be a map")
        fields = string_keys(fields)
        fields.setdefault("a", {})  # databases from before December 2020 have no "a"
        if set(fields) != {"m","a","h","l"}:
            raise InvalidCapture("Unknown or missing price-record fields")
        if type(fields["m"]) is not int or fields["m"] < 0:
            raise InvalidCapture("Invalid minimum price")
        for field in ("a","h","l"):
            days = fields[field]
            if days == []:
                days = {}
            if not isinstance(days,dict):
                raise InvalidCapture("Daily aggregate must be a map")
            normal = {}
            for day,value in days.items():
                day = text(day) if not isinstance(day, int) else str(day)
                if not day.isdigit() or type(value) is not int or value < 0:
                    raise InvalidCapture("Invalid daily aggregate")
                normal[day] = value
            fields[field] = normal
        items[item_key] = fields
    return {"payload_sha256":hashlib.sha256(payload).hexdigest(),"items":items}


def parse_capture(path: Path, markets=None) -> dict:
    """Read a SavedVariables file. Decodes every market, or only those named in
    `markets`, so an old market you never publish can't block a new scan."""
    with path.open("rb") as source:
        raw = source.read(MAX_FILE+1)
    globals_ = LuaData(raw).read()
    db = globals_.get("AUCTIONATOR_PRICE_DATABASE")
    if not isinstance(db, dict) or db.get(b"__dbversion") != 8:
        raise InvalidCapture("Only Auctionator price database version 8 is supported")
    available = {text(key): payload for key, payload in db.items() if key != b"__dbversion"}
    wanted = available if markets is None else markets
    decoded = {}
    for name in wanted:
        if name not in available:
            raise InvalidCapture(f"Market {name!r} is not in this file; it has: {', '.join(sorted(available))}")
        decoded[name] = decode_market(available[name])
    saved = globals_.get("AUCTIONATOR_SAVEDVARS",{})
    timestamps = {text(k):v for k,v in saved.items() if text(k).startswith("TimeOfLast") and type(v) is int}
    return {"source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),
            "database_version":8,"parser_version":PARSER_VERSION,"source_scan_timestamps":timestamps,
            "markets":decoded,"available_markets":sorted(available)}


def market_extract(capture: dict, sample_keys=None) -> dict:
    """The publishable projection of a parsed capture: price records only, no
    addon settings, posting history, searches or shopping lists."""
    markets = {}
    for name, market in capture["markets"].items():
        keys = sample_keys.get(name) if sample_keys else None
        items = market["items"] if keys is None else {k: market["items"][k] for k in keys}
        markets[name] = {"payload_sha256": market["payload_sha256"], "items": dict(sorted(items.items()))}
    sample = {"complete_market": not sample_keys}
    if sample_keys:
        sample["original_market_counts"] = {n: len(m["items"]) for n, m in capture["markets"].items()}
        sample["sample_keys"] = sample_keys
    return {"capture_format": "market-only-extract-v1", "database_version": 8,
            "parser_version": PARSER_VERSION, "sample": sample,
            "source_bytes": capture["source_bytes"], "source_sha256": capture["source_sha256"],
            "source_scan_timestamps": capture["source_scan_timestamps"],
            "validation_scope": "Market records only; original SavedVariables parsed locally and kept private.",
            "markets": markets}

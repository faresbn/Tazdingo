"""Build the explicit public projection. Standard-library Python; no live feeds."""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import io
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from auctionator import InvalidCapture, PARSER_VERSION, parse_capture, load_market_extract

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 1


def encoded(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(",",":")) + "\n"


def money(copper):
    gold,remainder = divmod(copper,10000)
    silver,copper = divmod(remainder,100)
    return f'{gold:,}<span class="coin gold">g</span> {silver:02d}<span class="coin silver">s</span> {copper:02d}<span class="coin copper">c</span>'


def stamp(timestamp):
    return datetime.fromtimestamp(timestamp,timezone.utc).isoformat().replace("+00:00","Z")


def collect(root=ROOT):
    config = json.loads((root/"data/captures.json").read_text())
    if config.get("schema_version") != SCHEMA:
        raise InvalidCapture("Unsupported capture registry schema")
    captures, seen = [], set()
    for receipt in config["captures"]:
        path = (root/receipt["path"]).resolve()
        if not path.is_relative_to((root/"data/captures").resolve()):
            raise InvalidCapture("Capture path escapes capture directory")
        if path.name.endswith(".market.json"):
            if hashlib.sha256(path.read_bytes()).hexdigest()!=receipt["extraction_sha256"]:
                raise InvalidCapture("Market extraction fingerprint differs from receipt")
            parsed=load_market_extract(path)
        else:
            parsed = parse_capture(path)
        digest = parsed["source_sha256"]
        if digest != receipt["source_sha256"]:
            raise InvalidCapture("Source hash differs from capture receipt")
        if receipt["environment"] not in ("forever-beta","forever","era","tbc"):
            raise InvalidCapture("Unknown environment")
        datetime.strptime(receipt["received_on"],"%Y-%m-%d")
        if digest in seen:
            continue
        seen.add(digest)
        ts = parsed["source_scan_timestamps"].get("TimeOfLastReplicateScan")
        if type(ts) is not int or ts <= 0:
            raise InvalidCapture("No supported source scan timestamp; establish chronology explicitly")
        captures.append({**receipt,**parsed,"capture_timestamp":ts,"capture_time":stamp(ts),
                         "capture_date":stamp(ts)[:10],"source_file":path.name})
    return sorted(captures,key=lambda c:(c["capture_timestamp"],c["source_sha256"]))


def group_markets(captures):
    groups = {}
    for capture in captures:
        for raw_key in capture["publish_markets"]:
            if raw_key not in capture["markets"]:
                raise InvalidCapture(f"Requested market {raw_key!r} is absent")
            slug = capture["environment"] + "-" + re.sub(r"[^a-z0-9]+","-",raw_key.lower())
            group = groups.setdefault(slug,{"id":slug,"environment":capture["environment"],
                      "market_key":raw_key,"realm":None,"faction":None,"region":None,
                      "snapshots":[],"seen_in":[],"payloads":set()})
            market = capture["markets"][raw_key]
            group["seen_in"].append(capture)
            if market["payload_sha256"] in group["payloads"]:
                continue
            group["payloads"].add(market["payload_sha256"])
            group["snapshots"].append((capture,market))
    return groups


def daily_code(fields):
    codes = {int(k) for f in ("a","h","l") for k in fields[f]}
    return max(codes) if codes else None


def make_record(key,fields,capture,group):
    return {"item_key":key,"item_id":int(key.split(":")[0]),"variant":key if ":" in key else None,
            "environment":group["environment"],"market_key":group["market_key"],
            "unit_price_copper":fields["m"],"quote_observed_at":None,
            "latest_daily_source_code":daily_code(fields),"raw_fields":fields,
            "capture_time":capture["capture_time"],"capture_date":capture["capture_date"],
            "received_on":capture["received_on"],"source_sha256":capture["source_sha256"],
            "observation_kind":"retained_cached_quote","parser_version":PARSER_VERSION}


def partition_records(records, size=200):
    """Keep every variant of an item together while bounding routine downloads."""
    from itertools import groupby
    chunk=[]
    for _,family in groupby(records,key=lambda r:r["item_id"]):
        family=list(family)
        if chunk and len(chunk)+len(family)>size:
            yield chunk
            chunk=[]
        chunk.extend(family)
    if chunk:
        yield chunk


def page(title,body,active,base,revision):
    def nav(label,path,key):
        state=' aria-current="page"' if active==key else ''
        return f'<a href="{base}{path}"{state}>{label}</a>'
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow">
<title>{html.escape(title)} · FvrRepo</title><meta name="description" content="WoW Forever Repo. Dated market records, character states and sourced comparisons.">
<link rel="stylesheet" href="{base}assets/style.css"><script src="{base}assets/app.js" defer></script><script src="https://foreverdb.net/embed/tooltips.js" data-icons="true" data-color-links="true" data-rename-links="true" async></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="{base}" aria-label="FvrRepo home"><span class="brand-mark" aria-hidden="true">F</span><span>FvrRepo<small>WOW FOREVER REPO</small></span></a>
<nav aria-label="Main navigation">{nav("Overview","","home")}{nav("Auction House","markets/","markets")}{nav("Characters","characters/","characters")}{nav("Sources","sources/","sources")}</nav><a class="nav-data" href="{base}data/manifest.json">Data catalogue <span aria-hidden="true">↗</span></a></header>
<main id="main">{body}</main><footer><a class="footer-brand" href="{base}">FvrRepo <span>WoW Forever Repo</span></a><p>An independent fan project. World of Warcraft belongs to Blizzard Entertainment.</p><p>Data revision <code>{revision}</code> · <a href="{base}sources/">Sources &amp; field notes</a></p></footer></body></html>'''


def build(root=ROOT,out=None,base="/FvrRepo/"):
    out = Path(out or root/"dist")
    if out.resolve() in (root.resolve(),(root/"data").resolve()) or not out.resolve().is_relative_to(root.resolve()):
        raise ValueError("Output must be a dedicated directory inside the repository")
    captures = collect(root)
    groups = group_markets(captures)
    revision = hashlib.sha256(encoded({"schema":SCHEMA,"parser":PARSER_VERSION,
                     "captures":[{"source":c["source_sha256"],"extract":c.get("extraction_sha256")} for c in captures]}).encode()).hexdigest()[:16]
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    base = "/"+base.strip("/")+"/" if base.strip("/") else "/"
    def write(path,content):
        p=out/path; p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(content,encoding="utf-8")
    def doc(path,title,body,active):
        write(path,page(title,body,active,base,revision))
    def data(path,value):
        write(path,encoded(value)); return base+path
    shutil.copytree(root/"site/assets",out/"assets")
    write(".nojekyll","")
    write("robots.txt","User-agent: *\nAllow: /\n")
    market_cards=[]; market_index=[]; report=[]
    price_rows=0
    for slug,g in groups.items():
        snapshots=[]; history={}
        for capture,market in g["snapshots"]:
            snapshot_id=capture.get("extraction_sha256",capture["source_sha256"])
            records=[make_record(k,fields,capture,g) for k,fields in sorted(market["items"].items(),key=lambda p:(int(p[0].split(":")[0]),p[0]))]
            price_rows+=len(records)
            snap={"schema_version":SCHEMA,"environment":g["environment"],"market_key":g["market_key"],
                  "capture_time":capture["capture_time"],"capture_time_scope":"file-global source scan timestamp; not every item/market observation time",
                  "source_sha256":capture["source_sha256"],"payload_sha256":market["payload_sha256"],
                  "received_on":capture["received_on"],"row_count":len(records),"records":records}
            json_path=f'data/snapshots/v1/{snapshot_id}/{slug}.json'
            url=data(json_path,snap)
            date_sources={capture["source_sha256"][:16]:{"source_sha256":capture["source_sha256"],"capture_time":capture["capture_time"],"capture_date":capture["capture_date"],"received_on":capture["received_on"]}}
            date_parts=[]
            for number,chunk in enumerate(partition_records(records)):
                part_id=f"{number:03d}"
                compact_rows=[{"item_key":r["item_key"],"unit_price_copper":r["unit_price_copper"],"source":r["source_sha256"][:16],"quote_observed_at":None,"latest_daily_source_code":r["latest_daily_source_code"]} for r in chunk]
                part_url=data(f'data/snapshots/v1/{snapshot_id}/{slug}/parts/{part_id}.json',{"schema_version":SCHEMA,"revision":snapshot_id[:16],"environment":g["environment"],"market_key":g["market_key"],"capture_sources":date_sources,"records":compact_rows})
                date_parts.append({"id":part_id,"first_item_id":chunk[0]["item_id"],"last_item_id":chunk[-1]["item_id"],"records":len(chunk),"json":part_url})
            quote_url=data(f'data/snapshots/v1/{snapshot_id}/{slug}/quotes.json',{"schema_version":SCHEMA,"revision":snapshot_id[:16],"environment":g["environment"],"market_key":g["market_key"],"capture_sources":date_sources,"records":[{"item_key":r["item_key"],"unit_price_copper":r["unit_price_copper"],"source":r["source_sha256"][:16],"quote_observed_at":None,"latest_daily_source_code":r["latest_daily_source_code"]} for r in records]})
            snapshots.append({"capture_date":capture["capture_date"],"capture_time":capture["capture_time"],"source_sha256":capture["source_sha256"],"rows":len(records),"json":url,"quotes_json":quote_url,"revision":snapshot_id[:16],"partitions":date_parts})
            for record in records:
                history.setdefault(record["item_key"],[]).append(record)
            report.append({"source_sha256":capture["source_sha256"],"market":g["market_key"],"records":len(records),"payload_sha256":market["payload_sha256"]})
        latest={k:rows[-1] for k,rows in history.items()}
        current=sorted(latest.values(),key=lambda r:(r["item_id"],r["item_key"]))
        sources={c["source_sha256"][:16]:{"source_sha256":c["source_sha256"],"capture_time":c["capture_time"],"capture_date":c["capture_date"],"received_on":c["received_on"]} for c,_ in g["snapshots"]}
        def compact(record):
            return {"item_key":record["item_key"],"unit_price_copper":record["unit_price_copper"],"source":record["source_sha256"][:16],"quote_observed_at":None,"latest_daily_source_code":record["latest_daily_source_code"]}
        common={"schema_version":SCHEMA,"revision":revision,"market_key":g["market_key"],"environment":g["environment"],"capture_sources":sources,"currency":"integer copper","quote_kind":"retained_cached_minimum"}
        compact_current=[compact(r) for r in current]
        latest_url=data(f'data/markets/{slug}/latest.json',{**common,"records":compact_current})
        partitions=[]
        for number,chunk in enumerate(partition_records(current)):
            part_id=f"{number:03d}"
            part_url=data(f'data/markets/{slug}/parts/{part_id}.json',{**common,"records":[compact(r) for r in chunk]})
            history_url=data(f'data/markets/{slug}/history/{part_id}.json',{**common,"history":{r["item_key"]:[compact(h) for h in history[r["item_key"]]] for r in chunk}})
            partitions.append({"id":part_id,"first_item_id":chunk[0]["item_id"],"last_item_id":chunk[-1]["item_id"],"records":len(chunk),"json":part_url,"history_json":history_url})
        buf=io.StringIO(); writer=csv.writer(buf,delimiter="\t",lineterminator="\n")
        writer.writerow(["environment","market_key","item_key","unit_price_copper","capture_time","quote_observed_at","latest_daily_source_code","source_sha256"])
        for record in current:
            writer.writerow([record[k] if record[k] is not None else "" for k in ("environment","market_key","item_key","unit_price_copper","capture_time","quote_observed_at","latest_daily_source_code","source_sha256")])
        tsv_path=f'data/markets/{slug}/latest.tsv'; write(tsv_path,buf.getvalue())
        meta={"id":slug,"environment":g["environment"],"market_key":g["market_key"],"realm":None,"faction":None,"region":None,
              "latest_capture_date":snapshots[-1]["capture_date"],"latest_export_seen":g["seen_in"][-1]["capture_date"],
              "item_count":len(current),"sample":True,"unique_snapshots":len(snapshots),"exports_received":len(g["seen_in"]),
              "html":base+f"markets/{slug}/","latest_json":latest_url,"latest_tsv":base+tsv_path,
              "partition_size":200,"partitions":partitions,"snapshots":snapshots}
        market_index.append(meta)
        legacy=g["market_key"]=="ClassicBetaPvP"
        label="Legacy cached market" if legacy else "PvP market"
        market_cards.append(f'<a class="market-card" href="{meta["html"]}"><span class="eyebrow">BETA TEST SAMPLE</span><div class="market-card-title"><h3>{html.escape(label)}</h3><span aria-hidden="true">↗</span></div><p class="muted">Source key: <code>{html.escape(g["market_key"])}</code></p><div class="card-stats"><span><strong>{len(current):,}</strong> sample item keys</span><span><strong>{len(snapshots)}</strong> snapshot{"s" if len(snapshots)!=1 else ""}</span></div><div class="card-foot">Latest distinct capture <time>{snapshots[-1]["capture_date"]}</time></div></a>')
        row_html=[]
        for record in current[:10]:
            key=record["item_key"]; safe_key=html.escape(key)
            row_html.append(f'<tr><td><a href="https://foreverdb.net/item/{record["item_id"]}" data-foreverdb="item:{record["item_id"]}" target="_blank" rel="noopener">Item {safe_key}</a></td><td class="price">{money(record["unit_price_copper"])}</td><td>{record["capture_date"]}</td><td><span class="status">Cached quote</span></td><td><a data-item-key="{safe_key}" href="{meta["html"]}?item={safe_key}#item-detail">History ↗</a></td></tr>')
        part_options="".join(f'<option value="{p["id"]}">Items {p["first_item_id"]}–{p["last_item_id"]}</option>' for p in partitions)
        date_options="".join(f'<option value="{snap["source_sha256"][:16]}">{snap["capture_date"]} · {snap["rows"]:,} keys</option>' for snap in reversed(snapshots))
        part_links="".join(f'<a href="{p["json"]}">{p["first_item_id"]}–{p["last_item_id"]}</a>' for p in partitions)
        browser_config=html.escape(encoded({"revision":revision,"partitions":partitions,"snapshots":snapshots,"latest_json":latest_url,"item_count":len(current),"capture_sources":sources,"market_html":meta["html"]}),quote=True)
        capture_links="".join(f'<a class="snapshot-link" href="{s["json"]}">{s["capture_date"]}<span>{s["rows"]:,} keys · JSON ↗</span></a>' for s in reversed(snapshots))
        body=f'''<section class="page-intro"><a class="back" href="{base}markets/">← All markets</a><p class="eyebrow">BETA TEST SAMPLE · {len(snapshots)} DATED SNAPSHOTS</p><h1>{html.escape(g["market_key"])}</h1><p>{len(current):,} item keys. Preserved from your Auctionator exports.</p></section><section class="content"><div class="notice">Small beta test sample only. Realm, faction and region have not been inferred from this market key. {'The same cached payload appears in all three supplied exports; it is preserved once.' if legacy else 'Every row links to its dated source and history.'}</div><div id="market-browser" data-config="{browser_config}"><div class="toolbar"><form id="item-form"><label>Find an item<input id="item-search" type="search" placeholder="Item ID or paste a database link" autocomplete="off"></label><button class="button primary" type="submit">Find item</button></form><div class="downloads"><a class="button secondary" href="{latest_url}">JSON ↗</a><a class="button secondary" href="{base}{tsv_path}">TSV ↗</a></div></div><div class="catalogue-filters"><label>Capture date<select id="capture-select"><option value="latest">Latest retained records</option>{date_options}</select></label><label>Sort by<select id="sort-select"><option value="item">Item ID</option><option value="price-low">Price: low to high</option><option value="price-high">Price: high to low</option></select></label></div><div class="browse-controls"><select id="partition-select" aria-label="Data range" hidden>{part_options}</select><button class="button secondary" type="button" id="previous-page">← Previous</button><button class="button secondary" type="button" id="next-page">Next →</button></div><p id="search-count" class="muted" aria-live="polite">Showing the first 10 of {len(current):,} item keys. Find by exact item ID; hover or tap an item for its ForeverDB tooltip.</p><p class="tooltip-credit"><a href="https://foreverdb.net/items" target="_blank" rel="noopener">Find item names on ForeverDB ↗</a> · Item details via <a href="https://foreverdb.net/embed" target="_blank" rel="noopener">ForeverDB</a>. These are current reference tooltips, not frozen item stats from the scan date.</p><div class="table-wrap"><table id="market-table"><thead><tr><th>Item key</th><th>Unit minimum</th><th>Source capture</th><th>Evidence</th><th>Details</th></tr></thead><tbody>{''.join(row_html)}</tbody></table></div><section id="item-detail" class="detail-panel" hidden><div class="section-head"><h2 id="detail-title">Item history</h2><a id="detail-download" class="button secondary">History JSON ↗</a></div><p class="muted">Capture dates identify the containing export; the exact quote observation time is unavailable.</p><div class="table-wrap"><table><thead><tr><th>Capture date</th><th>Unit minimum</th><th>Latest source day code</th><th>Source fingerprint</th></tr></thead><tbody id="history-rows"></tbody></table></div></section></div><details class="partition-downloads"><summary>Direct data partitions · no JavaScript required</summary><p>These small files contain all current records. Pick the item-ID range, or download the complete JSON/TSV above.</p><div>{part_links}</div></details><div class="section-head"><h2>Dated source snapshots</h2></div><div class="snapshot-list">{capture_links}</div></section>'''
        doc(f"markets/{slug}/index.html",g["market_key"]+" market",body,"markets")
    validation={"schema_version":SCHEMA,"revision":revision,"parser_version":PARSER_VERSION,"source_files":len(captures),"distinct_market_snapshots":len(report),"snapshot_rows":price_rows,"results":report,"status":"Market-only extraction fingerprints, schema and counts validated; original Lua parsed locally, not re-read by Actions"}
    data("data/validation.json",validation)
    manifest={"schema_version":SCHEMA,"project":"FvrRepo","full_name":"WoW Forever Repo","revision":revision,"source_commit":os.environ.get("GITHUB_SHA","local"),"parser_version":PARSER_VERSION,"release_market_available":False,"dataset_scope":"selected beta sample","markets":market_index,"characters":[],"validation":base+"data/validation.json","sources_html":base+"sources/"}
    data("data/manifest.json",manifest)
    latest=max(c["capture_date"] for c in captures)
    main=next((m for m in market_index if m["market_key"]=="PvP"),market_index[0])
    body=f'''<section class="hero"><div class="hero-art" aria-hidden="true"></div><div class="hero-content"><p class="eyebrow">A SHARED FIELD JOURNAL</p><h1>Keep a record.<br><em>Find your next step.</em></h1><p class="hero-copy">Market history, character states and the discoveries worth keeping. A shared reference for our adventures in Azeroth.</p><div class="hero-actions"><a class="button primary" href="{base}markets/">Explore the Auction House <span aria-hidden="true">→</span></a><a class="text-link" href="{base}characters/">Character journal ↗</a></div></div><aside class="hero-note"><span class="eyebrow">LATEST SOURCE CAPTURE</span><strong>{latest}</strong><span>{main["item_count"]:,} PvP sample item keys</span><span class="status">Small beta test sample</span></aside></section><section class="content overview"><div class="beta-banner"><span class="dot" aria-hidden="true"></span><p><strong>A foundation for launch.</strong> These records are from the finished beta. Release market data will begin with a genuine release scan.</p></div><div class="metric-strip"><div><strong>{len(captures)}</strong><span>dated source exports</span></div><div><strong>{main["item_count"]:,}</strong><span>PvP sample item keys</span></div><div><strong>{len(groups)}</strong><span>separate markets</span></div><div><strong>0</strong><span>saved character states</span></div></div><div class="section-head"><div><p class="eyebrow">FOLLOW THE EVIDENCE</p><h2>The market ledger</h2></div><a class="text-link" href="{base}markets/">All market records →</a></div><div class="market-grid">{''.join(market_cards)}</div><div class="journal-panel"><div><p class="eyebrow">CHARACTERS &amp; COMPARISONS</p><h2>A place for the builds<br>we come back to.</h2><p>Save a character state explicitly, with the gear, talents and sources that belong to it. Keep tested ideas beside the evidence.</p><a class="text-link" href="{base}characters/">Open the character journal →</a></div><div class="empty-card"><span class="rune" aria-hidden="true">◇</span><h3>The first page is yours.</h3><p>No character states have been saved yet.</p></div></div></section>'''
    doc("index.html","WoW Forever Repo",body,"home")
    doc("markets/index.html","Auction House",f'<section class="page-intro"><p class="eyebrow">THE MARKET LEDGER</p><h1>Auction House</h1><p>Separate markets. Dated records. Evidence you can inspect.</p></section><section class="content"><div class="notice">Small beta test samples. Select a market to browse its prices, snapshots and downloads.</div><div class="market-grid">{"".join(market_cards)}</div></section>',"markets")
    doc("characters/index.html","Characters & comparisons",'<section class="page-intro"><p class="eyebrow">THE CHARACTER JOURNAL</p><h1>Characters &amp; comparisons</h1><p>Dated states, considered builds and the evidence behind our decisions.</p></section><section class="content"><div class="empty-state"><span class="rune" aria-hidden="true">◇</span><h2>No saved states yet.</h2><p>When a character state is worth keeping, the project can suggest saving it. A record is written only after you explicitly ask.</p><p>Equipped gear, proposed configurations and simulation results will be labelled separately.</p></div></section>',"characters")
    source_list="".join(f'<li><strong>{c["capture_date"]}</strong> · {c["source_bytes"]:,} bytes<br><code class="hash">{c["source_sha256"]}</code></li>' for c in captures)
    body=f'''<section class="page-intro"><p class="eyebrow">THE FIELD NOTES</p><h1>Sources &amp; provenance</h1><p>What these records say, and where their limits begin.</p></section><section class="content prose"><h2>Your source exports</h2><p>Three original Auctionator SavedVariables files were supplied on 26 October 2026. Market-only extracts are retained in the private repository. The full originals remain outside GitHub pending explicit upload approval. The source hashes below identify their exact bytes. Source capture times use <code>TimeOfLastReplicateScan</code>; this is a file-global timestamp, not every market or item observation time.</p><ul class="source-list">{source_list}</ul><h2>Reading the prices</h2><p>The raw <code>m</code> field is published as a cached minimum unit buyout in copper, following the supplied project AH workflow. It is not a sale price, guaranteed current listing or evidence of demand. <code>a</code>, <code>h</code> and <code>l</code> retain daily quantity, high and low aggregates respectively; a quantity peak is not current stock.</p><p>Exact per-item quote observation times are not available in <code>m</code>. Original daily codes are retained without calendar conversion until the matching addon definition is verified. Raw aggregate maps are included in the structured records so this limitation is visible.</p><h2>Validation</h2><p>Database version 8 and market version 2 were decoded locally without executing Lua. GitHub Actions validates the market-only extracts and does not claim to re-read the full originals. The independent bounded CBOR reader follows <a href="https://www.rfc-editor.org/rfc/rfc8949.html">RFC 8949</a>. <a href="https://www.curseforge.com/wow/addons/auctionator/files/6787438">Auctionator's own release notes</a> document the move to CBOR. Matching maintainer field/date definitions remain a follow-up; structural parsing alone does not verify every field meaning.</p><p>The original PvP exports contain 3,749, 3,972 and 4,238 item keys, but this prototype publishes only 24 selected items across those dates. The separate ClassicBetaPvP original contains 2,340 keys; six are included here. Its unchanged payload is retained once. No realm mapping or release carry-over has been inferred.</p><p><a class="button secondary" href="{base}data/validation.json">Validation report ↗</a> <a class="button secondary" href="{base}data/manifest.json">Data catalogue ↗</a></p><h2>Character saves</h2><p>Save only on explicit request. The assistant may suggest a save for a useful, sufficiently established state that is absent from the repository. User-reported state, inspected exports, external facts and simulated results remain distinct evidence types.</p><h2>Item tooltips</h2><p>Item links use <a href="https://foreverdb.net/embed">ForeverDB's documented embed</a>, with names, icons, hover and keyboard/touch tooltips loaded by the provider. The current external tooltip is not an archived beta tooltip. We do not mirror the external item database or use its changing stats as historical AH evidence.</p><h2>Design &amp; references</h2><p>The teal, dusk-blue and parchment palette takes its cue from the <a href="https://worldofwarcraft.blizzard.com/en-us/forever">official Forever website</a>. This is an independent fan project. The decorative landscape is original; no official artwork or logo is redistributed.</p></section>'''
    doc("sources/index.html","Sources & provenance",body,"sources")
    for path in out.rglob("*"):
        if path.is_file() and path.suffix not in (".html",".css",".js",".svg",".json",".tsv",".txt",""):
            raise InvalidCapture("Unexpected public file type")
    if any(out.rglob("*.lua")):
        raise InvalidCapture("Raw Lua must not be published")
    return {"revision":revision,"sources":len(captures),"markets":len(groups),"snapshot_rows":price_rows,"output":str(out)}


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--base-path",default="/FvrRepo/")
    args=parser.parse_args()
    print(json.dumps(build(base=args.base_path),indent=2))

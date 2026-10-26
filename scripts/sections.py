"""Section pages: classes, professions, world and the More lists. Notes come from content/;
everything else from data/game.json and ForeverDB's data. Every value goes through esc()."""
from __future__ import annotations

from pages import (FOREVERDB, Site, badge, changelog, esc, item_link, layout, links, money, note_block,
                   page_head, source_tag, when)

ROLES = {"dps": "Damage", "tank": "Tank", "healer": "Healer"}


def entries_for(ctx: dict, prefix: str) -> list:
    return [e for e in ctx["log"] if any(f.startswith(prefix) for f in e["files"])]


def hubs(ctx: dict) -> str:
    return links(ctx["game"]["hubs"])


# --- Classes --------------------------------------------------------------------

def classes_index(site: Site, ctx: dict) -> str:
    content = ctx["content"]
    cards = []
    for c in ctx["game"]["classes"]:
        noted = [k for k in content if k.startswith(f"classes/{c['slug']}/")]
        base_key = f"classes/{c['slug']}/"
        specs = "".join(f'<li><a href="{site.base}classes/{c["slug"]}/#{slug}">{esc(name)}</a> <span class="role">{"/".join(ROLES[r] for r in role.split("/"))}</span>'
                        f'{" " + badge("noted", "Notes") if base_key + slug in content else ""}</li>'
                        for slug, name, role in c["specs"])
        cards.append(f'<li class="class-entry" style="--class:{esc(c["colour"])}"><a class="class-name" href="{site.base}classes/{c["slug"]}/">{esc(c["name"])}</a>'
                     f'<ul class="specs">{specs}</ul><p class="aside">{len(noted)} page{"s" if len(noted) != 1 else ""} of notes</p></li>')
    return layout(site, "Classes", page_head("Classes", "Nine classes, three talent trees each. Our notes on each spec, and where to read more.")
                  + f'''<section class="page-body">
  <ul class="class-list">{"".join(cards)}</ul>
  <section class="reading"><h2>About specs and hybrids</h2>
  <p>Forever keeps three talent trees per class, with one point per level from level 10, so builds that mix two trees are normal. Blizzard aims for hybrid damage specs to deal about 5% less damage than pure ones, and counts warriors as hybrids. <a href="https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids" target="_blank" rel="noopener">ForeverDB on the hybrid tax</a>.</p>
  <h3>Guides and calculators elsewhere</h3>{hubs(ctx)}</section>
</section>''', active="classes", path="classes/", description="World of Warcraft: Forever classes and specs: notes, builds, macros and guides.")


def spec_links(c: dict, slug: str, name: str, role: str) -> list:
    pairs = [(f"Wowhead: {name} {c['name']} guide ({ROLES[r].lower()})", f"https://www.wowhead.com/forever/guide/classes/{c['slug']}/{slug}/overview-pve-{r}")
             for r in role.split("/")]
    return pairs + [(f"ForeverDB: {c['name']} guide and rotation", f"{FOREVERDB}/class/{c['name']}/guide"),
                    (f"ForeverDB: {c['name']} PvE", f"{FOREVERDB}/class/{c['name']}/pve")]


def class_page(site: Site, ctx: dict, c: dict) -> str:
    content = ctx["content"]
    key = lambda part: f"classes/{c['slug']}/{part}"
    jump = " ".join(f'<a href="#{slug}">{esc(name)}</a>' for slug, name, _ in c["specs"]) + ' <a href="#hybrid">Hybrid builds</a> <a href="#macros">Macros</a>'
    sections_ = []
    if key("overview") in content:
        sections_.append(f'<section id="overview" class="spec"><h2>Overview</h2>{note_block(content[key("overview")], "")}</section>')
    for slug, name, role in c["specs"]:
        roles = " ".join(badge("role", ROLES[r]) for r in role.split("/"))
        sections_.append(f'''<section id="{slug}" class="spec"><h2>{esc(name)} {roles}</h2>
{note_block(content.get(key(slug)), f"No notes on {name} yet.")}
<h3>Elsewhere</h3>{links(spec_links(c, slug, name, role))}</section>''')
    sections_.append(f'''<section id="hybrid" class="spec"><h2>Hybrid builds</h2>
{note_block(content.get(key("hybrid")), "No hybrid builds recorded yet. Talent points come one per level from 10, so mixing two trees is common.")}
<h3>Elsewhere</h3>{links([("ForeverDB: talent calculator", f"{FOREVERDB}/class/{c['name']}/talents"), ("Wowhead: talent calculator", "https://www.wowhead.com/forever/talent-calc")])}</section>''')
    sections_.append(f'''<section id="macros" class="spec"><h2>Macros</h2>
{note_block(content.get(key("macros")), "No macros recorded yet.")}
<p><a href="{site.base}more/macros/">More macro collections</a></p></section>''')
    noted = sum(1 for k in content if k.startswith(f"classes/{c['slug']}/"))
    lede = f'{" · ".join(esc(n) for _, n, _ in c["specs"])}. {"Notes on " + str(noted) + " part" + ("s" if noted != 1 else "") + "." if noted else "No notes yet: the links below lead to the best guides so far."}'
    return layout(site, c["name"], f'<div class="class-band" style="--class:{esc(c["colour"])}"></div>'
                  + page_head(c["name"], lede, (("Classes", f"{site.base}classes/"),), f'<p class="jump">{jump}</p>')
                  + '<section class="page-body">' + "".join(sections_) + changelog(site, entries_for(ctx, f"content/classes/{c['slug']}/")) + "</section>",
                  active="classes", path=f"classes/{c['slug']}/", description=f"{c['name']} in World of Warcraft: Forever: spec notes, hybrid builds, macros and guides.")


# --- Professions ----------------------------------------------------------------

def profession_stats(ctx: dict, name: str) -> tuple[int, int]:
    recipes = ctx["fdb"].get("recipes", {}).get(name, [])
    return len(recipes), sum(r["new"] for r in recipes)


def professions_index(site: Site, ctx: dict) -> str:
    groups = {}
    for p in ctx["game"]["professions"]:
        groups.setdefault(p["kind"], []).append(p)
    blocks = []
    for kind, items in groups.items():
        rows = []
        for p in items:
            total, new = profession_stats(ctx, p["name"])
            camp = sum(1 for k in ctx["fdb"].get("camp", []) if k["profession"] == p["name"])
            rows.append(f'<tr><th scope="row"><a href="{site.base}professions/{p["slug"]}/">{esc(p["name"])}</a></th>'
                        f'<td class="num">{total:,}</td><td class="num">{new:,}</td><td class="num">{camp or ""}</td></tr>')
        blocks.append(f'<h2>{esc(kind)}</h2><div class="table-wrap"><table><thead><tr><th scope="col">Profession</th><th scope="col" class="num">Recipes</th>'
                      f'<th scope="col" class="num">New in Forever</th><th scope="col" class="num">Camp items</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    src = ctx["fdb_source"]
    note = f'<p class="note">{badge("prelaunch") if ctx["data_prelaunch"] else badge("live")} Recipe counts from ForeverDB\'s data for game build {esc(src.get("client_build"))}.</p>'
    return layout(site, "Professions", page_head("Professions", "What each profession makes in Forever, what's new, and what it earns.", (), note)
                  + f'<section class="page-body">{"".join(blocks)}<p><a href="{site.base}prices/craft/">What to craft, ranked by margin</a>. '
                    f'<a href="{site.base}prices/materials/">Materials worth gathering</a>.</p></section>',
                  active="professions", path="professions/", description="World of Warcraft: Forever professions: recipes, what's new, camp items and margins.")


def profession_page(site: Site, ctx: dict, p: dict) -> str:
    total, new = profession_stats(ctx, p["name"])
    camp = [k for k in ctx["fdb"].get("camp", []) if k["profession"] == p["name"]]
    camp_rows = "".join(f'<tr><th scope="row">{item_link(k["item"], k["name"])}</th><td class="num">{k["skill"]}</td><td>{esc(k["effect"])}</td></tr>' for k in camp)
    crafts = [r for r in ctx["craft"] if r["profession"] == p["name"]][:8]
    craft_rows = "".join(f'<tr><th scope="row">{item_link(r["item"], r["name"])}</th><td class="num">{r["skill"]}</td><td class="num">{money(r["margin"])} {source_tag(r["value_source"])}</td></tr>' for r in crafts)
    elsewhere = [(f"ForeverDB: {p['name']}", f"{FOREVERDB}/profession/{p['slug']}")]
    if p.get("wowhead"):
        elsewhere.append((f"Wowhead: {p['name']} levelling guide", f"https://www.wowhead.com/forever/guide/professions/{p['slug']}/overview-leveling"))
    facts = (f'<p class="lede">{p["kind"]} profession. {total:,} recipes, {new:,} of them new in Forever '
             f'{badge("prelaunch") if ctx["data_prelaunch"] else ""}.</p>') if total else ""
    body = f'''<section class="page-body">
  <section class="spec"><h2>Our notes</h2>{note_block(ctx["content"].get(f"professions/{p['slug']}"), f"No notes on {p['name']} yet.")}</section>
  {f'<section class="spec"><h2>Best margins</h2><div class="table-wrap"><table><thead><tr><th scope="col">Recipe</th><th scope="col" class="num">Skill</th><th scope="col" class="num">Margin</th></tr></thead><tbody>{craft_rows}</tbody></table></div><p><a href="{site.base}prices/craft/#{p["name"].lower().replace(" ", "-")}">All {esc(p["name"])} margins</a></p></section>' if crafts else ""}
  {f'<section class="spec"><h2>Camp items</h2><p>What {esc(p["name"])} adds to a campfire.</p><div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col" class="num">Skill</th><th scope="col">Effect</th></tr></thead><tbody>{camp_rows}</tbody></table></div></section>' if camp else ""}
  <section class="spec"><h2>Elsewhere</h2>{links(elsewhere)}</section>
  {changelog(site, entries_for(ctx, f"content/professions/{p['slug']}"))}
</section>'''
    return layout(site, p["name"], page_head(p["name"], "", (("Professions", f"{site.base}professions/"),), facts) + body,
                  active="professions", path=f"professions/{p['slug']}/", description=f"{p['name']} in World of Warcraft: Forever: recipes, camp items, margins and guides.")


# --- World ------------------------------------------------------------------------

def world_index(site: Site, ctx: dict) -> str:
    rows = "".join(f'<li><a href="{site.base}world/{t["slug"]}/" class="door-name">{esc(t["name"])}</a><p>{esc(t["summary"])}</p></li>' for t in ctx["game"]["world"])
    return layout(site, "World", page_head("World", "How Forever's systems work, and what's out there.")
                  + f'<section class="page-body"><ul class="door-list">{rows}</ul></section>',
                  active="world", path="world/", description="World of Warcraft: Forever systems: camping, Legacy, Merchant's Favor, rares, zones, raids and collections.")


def world_data(site: Site, ctx: dict, slug: str) -> str:
    fdb = ctx["fdb"]
    label = badge("prelaunch") if ctx["data_prelaunch"] else ""
    if slug == "camping" and fdb.get("camp"):
        groups = {}
        for k in fdb["camp"]:
            groups.setdefault(k["profession"], []).append(k)
        rows = "".join(f'<tr><td>{esc(prof)}</td><th scope="row">{item_link(k["item"], k["name"])}</th><td class="num">{k["skill"]}</td><td>{esc(k["effect"])}</td></tr>'
                       for prof, kits in groups.items() for k in kits)
        return (f'<section class="spec"><h2>Every camp item {label}</h2><div class="table-wrap"><table><thead><tr><th scope="col">Profession</th>'
                f'<th scope="col">Item</th><th scope="col" class="num">Skill</th><th scope="col">Effect</th></tr></thead><tbody>{rows}</tbody></table></div></section>')
    if slug == "merchants-favor" and fdb.get("crates"):
        return (f'<section class="spec"><h2>Waylaid Crates {label}</h2><p>{len(fdb["crates"])} crates, from level 10 to 35. Each takes any one bundle of materials from its list. '
                f'<a href="{site.base}prices/crates/">The cheapest way to fill each one</a>.</p></section>')
    if slug == "rares" and fdb.get("rares"):
        r = fdb["rares"]
        return (f'<section class="spec"><h2>In the data {label}</h2><p>{r.get("n", 0)} rare creatures are known; {r.get("seen", 0)} have been seen in Forever so far. '
                'The rest come from Classic data and may differ.</p></section>')
    if slug == "collections" and fdb.get("collections"):
        c = fdb["collections"]
        return (f'<section class="spec"><h2>In the data {label}</h2><p>{c.get("mounts", 0)} mounts, {c.get("pets", 0)} companion pets and {c.get("titles", 0)} titles.</p></section>')
    return ""


def world_page(site: Site, ctx: dict, t: dict) -> str:
    body = f'''<section class="page-body">
  {world_data(site, ctx, t["slug"])}
  <section class="spec"><h2>Our notes</h2>{note_block(ctx["content"].get(f"world/{t['slug']}"), f"No notes on {t['name'].lower()} yet.")}</section>
  <section class="spec"><h2>Elsewhere</h2>{links([(label, url if url.startswith("http") else site.base + "world/" + t["slug"] + "/" + url) for label, url in t["links"]])}</section>
  {changelog(site, entries_for(ctx, f"content/world/{t['slug']}"))}
</section>'''
    return layout(site, t["name"], page_head(t["name"], esc(t["summary"]), (("World", f"{site.base}world/"),)) + body,
                  active="world", path=f"world/{t['slug']}/", description=f"{t['name']} in World of Warcraft: Forever.")


# --- More -------------------------------------------------------------------------

MORE_TITLES = {"addons": "Addons", "macros": "Macros", "known-issues": "Known issues"}
MORE_LEDES = {"addons": "Which addons work in Forever, and where to get them.",
              "macros": "Macros for each class, and where to find more.",
              "known-issues": "Problems players have hit, what's known, and any workaround."}


def more_page(site: Site, ctx: dict, slug: str) -> str:
    page = ctx["content"].get(f"more/{slug}")
    extra = ""
    if slug == "macros":
        class_macros = [(c, ctx["content"][f"classes/{c['slug']}/macros"]) for c in ctx["game"]["classes"] if f"classes/{c['slug']}/macros" in ctx["content"]]
        extra = "".join(f'<section class="spec" style="--class:{esc(c["colour"])}"><h2><a href="{site.base}classes/{c["slug"]}/#macros">{esc(c["name"])}</a></h2>{note_block(m, "")}</section>' for c, m in class_macros)
    return layout(site, MORE_TITLES[slug], page_head(MORE_TITLES[slug], MORE_LEDES[slug])
                  + f'<section class="page-body">{note_block(page, "Nothing recorded yet.")}{extra}{changelog(site, entries_for(ctx, f"content/more/{slug}"))}</section>',
                  active="more", path=f"more/{slug}/", description=f"World of Warcraft: Forever {MORE_TITLES[slug].lower()}: {MORE_LEDES[slug]}")


def about_page(site: Site, ctx: dict) -> str:
    scans = "".join(f'<li>{when(c["capture_date"])}, {esc(c["environment_label"])}: {c["source_bytes"]:,} bytes, fingerprint <code>{esc(c["source_sha256"][:16])}</code></li>'
                    for c in reversed(ctx["captures"]))
    src, names = ctx["fdb_source"], ctx["names_source"] or {}
    return layout(site, "Sources and credits", page_head("Sources and credits", "Where everything in the ledger comes from, and how to read it.")
                  + f'''<section class="page-body prose">
  <h2>What this is</h2>
  <p>Forever Ledger is a small, unofficial record of World of Warcraft: Forever: what things cost on the Auction House, notes on classes and professions, how the new systems work, and the addons, macros and known issues worth knowing. It isn't affiliated with or endorsed by Blizzard Entertainment.</p>
  <h2>Labels</h2>
  <p>{badge("prelaunch")} marks anything from before launch on 4 November 2026, or not yet confirmed in the live game; it gets replaced as live data arrives. {badge("beta")} marks prices from Forever Beta scans. Notes say how well they're tested: idea, testing, tested or outdated.</p>
  <h2>Prices</h2>
  <p>Prices come from our own Auctionator scans. Only the addon's price records are published. The typical price is the middle value of each day's cheapest listing over the item's last seven days, so one odd listing doesn't set it. Steadiness compares the spread of those daily prices over two weeks with the typical price. Dates follow Auctionator's own day counter, which starts on 1 January 2020.</p>
  <p>Where our scans don't hold an item, the gold-making tables use prices from ForeverDB's players' scans, labelled as such, and vendor prices recorded by ForeverDB's players.</p>
  <h3>Our scans</h3><ul class="scans">{scans}</ul>
  <h2>Game data</h2>
  <p>Item names, recipes, camp items, Waylaid Crates, rare and collection counts, other players' prices and vendor prices: <a href="{FOREVERDB}">Data from ForeverDB.net</a> (game build {esc(src.get("client_build"))}, fetched {esc(src.get("fetched_on"))}; names fetched {esc(names.get("fetched_on"))}). Item tooltips use <a href="{FOREVERDB}/embed">ForeverDB's embed</a> and show today's details, not how an item looked on the day of a scan.</p>
  <h2>Elsewhere</h2>
  <p>Guides, calculators and news are linked where they're relevant, never copied: Wowhead, Icy Veins, Method, Warcraft Tavern, ForeverDB, Kami Labs and Blizzard's own forums.</p>
  {hubs(ctx)}
  <h2>Data files</h2>
  <p>The whole ledger as plain text: <a href="{site.base}llms-full.txt">llms-full.txt</a> (short index: <a href="{site.base}llms.txt">llms.txt</a>). Every market's prices and daily history as TSV, linked from its page; every priced recipe in <a href="{site.base}prices/craft.tsv">craft.tsv</a>.</p>
  <h2>Pictures</h2>
  <p>The map on the front page is an original illustration made for this site. World of Warcraft and its artwork belong to Blizzard Entertainment.</p>
</section>''', active="more", path="more/about/", description="Where Forever Ledger's prices, game data and notes come from.")

"""Section pages: classes and specs, professions, world, the More lists and the Blizzard posts.
Notes come from content/; links and structure from data/game.json; tables from ForeverDB's data.
Every value goes through esc()."""
from __future__ import annotations

import re
from datetime import datetime, timezone

from pages import (FOREVERDB, ROLES, Site, artwork, badge, banner, changelog, emblem, esc, ext, item_link, layout, object_icon,
                   gold_cards, links, money, news_widget, nice_date, page_head, plain_text, render_sections, source_tag, tabs, when)

WOWHEAD = "https://www.wowhead.com/forever"


def entries_for(ctx: dict, prefix: str) -> list:
    return [e for e in ctx["log"] if any(f.startswith(prefix) for f in e["files"])]


def tools_list(pairs: list) -> str:
    rows = "".join(f'<li><a href="{esc(url)}"{ext(url)}>{esc(label)}</a>{f" <span class=aside>{esc(hint)}</span>" if hint else ""}</li>'
                   for label, url, hint in pairs)
    return f'<ul class="link-list">{rows}</ul>'


def roles(spec: dict) -> str:
    return " ".join(badge("role", ROLES[r]) for r in spec["roles"])


# --- Notes, split for the tabbed pages ------------------------------------------------

H3 = re.compile(r'<h3 id="([^"]+)">(.*?)</h3>', re.S)
CHEAT_ROW = re.compile(r"<li><strong>(.*?):?</strong>:?\s*(.*?)</li>", re.S)


def section(page: dict | None, kind: str) -> dict | None:
    return next((s for s in page["sections"] if s["kind"] == kind), None) if page else None


def parts(html_text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """A section's HTML as (what comes before its first ### heading, [(anchor, heading, body)])."""
    pieces = H3.split(html_text)
    return pieces[0], [(pieces[i], pieces[i + 1], pieces[i + 2]) for i in range(1, len(pieces), 3)]


def is_take(heading: str) -> bool:
    return plain_text(heading).strip().lower().startswith("tazdingo recommendation")


def take(page: dict | None) -> str:
    """The page's Tazdingo recommendation, lifted out of the guides' summary for the first tab."""
    guides = section(page, "guides")
    found = [(a, h, b) for a, h, b in parts(guides["html"])[1] if is_take(h)] if guides else []
    return "".join(f'<aside class="take"><h3 id="{esc(a)}">Our take</h3>{b}</aside>' for a, h, b in found)


def in_depth(page: dict | None, extra: str = "") -> str:
    """The guides' summary without the recommendation (shown on the first tab), led by a row of jump links."""
    guides = section(page, "guides")
    if not guides:
        return extra
    intro, rest = parts(guides["html"])
    rest = [(a, h, b) for a, h, b in rest if not is_take(h)]
    jump = "".join(f'<li><a href="#{esc(a)}">{esc(plain_text(h))}</a></li>' for a, h, _ in rest)
    others = "".join(f'<h3 class="part-title">{esc(s["heading"])}</h3><div class="prose">{s["html"]}</div>'
                     for s in page["sections"] if s["kind"] == "other" and s["html"].strip())
    return ((f'<nav class="jump" aria-label="In this tab"><ul>{jump}</ul></nav>' if len(rest) > 2 else "")
            + f'<div class="prose">{intro}{"".join(f"<h3 id={chr(34)}{esc(a)}{chr(34)}>{h}</h3>{b}" for a, h, b in rest)}</div>' + others + extra)


def cheat_rows(page: dict | None) -> list[tuple[str, str]]:
    glance = section(page, "glance")
    if not glance:
        return []
    rows = []
    for item in re.findall(r"<li>(.*?)</li>", glance["html"], re.S):
        match = CHEAT_ROW.match(f"<li>{item}</li>")
        rows.append((plain_text(match.group(1)).rstrip(":"), match.group(2)) if match else ("", item))
    return rows


def cheatsheet(page: dict | None, empty: str = "") -> str:
    rows = cheat_rows(page)
    if not rows:
        glance = section(page, "glance")
        return f'<div class="prose">{glance["html"]}</div>' if glance else (f'<p class="empty">{esc(empty)}</p>' if empty else "")
    return ('<dl class="cheatsheet">' + "".join(f'<div class="cheat"><dt>{esc(label)}</dt><dd>{value}</dd></div>' if label
                                               else f'<div class="cheat wide"><dd>{value}</dd></div>' for label, value in rows) + '</dl>')


def pick_line(page: dict | None) -> str:
    """The cheatsheet's "Pick it for" line, the one-line case for a spec or profession, for cards."""
    return next((value for label, value in cheat_rows(page) if label.lower() in ("pick it for", "pick it")), "")


def findings(page: dict | None) -> str:
    sec = section(page, "findings")
    return f'<div class="ledger-sheet prose">{sec["html"]}</div>' if sec and not sec["empty"] else ""


def sources_tab(site: Site, page: dict | None, tools: list, log: list, note: str = "") -> str:
    more = section(page, "more")
    findings_note = ('<p class="aside">No field findings recorded yet: our own tested discoveries appear in their own tab, '
                     'marked with how well they\'re tested.</p>' if page and not findings(page) else "")
    return ((f'<h3 class="part-title">Read more</h3><div class="prose read-more">{more["html"]}</div>' if more and more["html"].strip() else "")
            + (f'<h3 class="part-title">Guides and tools</h3>{tools_list(tools)}' if tools else "")
            + (f'<p class="sources">Sources: {esc(page["sources"])}</p>' if page and page.get("sources") else "")
            + note + findings_note + changelog(site, log))


def finding_count(page: dict | None) -> int:
    sec = section(page, "findings")
    return 0 if not sec or sec["empty"] else len(re.findall(r"<h3", sec["html"])) or 1


def head_facts(page: dict | None, *extra: str) -> str:
    facts = list(extra)
    if page:
        facts.append(badge("prelaunch") if page["status"] == "pre-launch" else badge("live"))
        if page.get("confidence_label"):
            facts.append(badge(page["confidence"], page["confidence_label"]))
        facts.append(f'<span class="updated">Updated {when(page["updated"])}</span>')
    return f'<p class="status-line">{" ".join(facts)}</p>' if facts else ""


def spec_switch(site: Site, c: dict, current: str = "") -> str:
    b = site.base
    links = [f'<a href="{b}classes/{c["slug"]}/"{" aria-current=page" if not current else ""}>Overview</a>']
    links += [f'<a href="{b}classes/{c["slug"]}/{s["slug"]}/"{" aria-current=page" if s["slug"] == current else ""}>'
              f'{emblem(site, "spec", c["slug"] + "-" + s["slug"], 20)}{esc(s["name"])}</a>' for s in c["specs"]]
    return f'<nav class="switcher" aria-label="{esc(c["name"])} pages">{"".join(links)}</nav>'


# --- Classes --------------------------------------------------------------------

def spec_tools(c: dict, spec: dict) -> list:
    pairs = [(f"Wowhead: {spec['name']} {c['name']} ({ROLES[r].lower()})", f"{WOWHEAD}/guide/classes/{c['slug']}/{spec['slug']}/overview-pve-{r}",
              "Overview, abilities, levelling") for r in spec["roles"]]
    pairs.append((f"Icy Veins: {spec['name']} {c['name']} guide", spec["icy_veins"], "Talents, rotation, stats"))
    pairs += [(f"WoWSims: {url.rstrip('/').split('/')[-1].replace('feralcat', 'feral cat').replace('feralbear', 'feral bear')} simulator", url,
               "Simulate your gear and talents (alpha)") for url in spec["wowsims"]]
    pairs += [(f"ForeverDB: {c['name']} guide and rotation", f"{FOREVERDB}/class/{c['name']}/guide", "Abilities and what changed"),
              (f"ForeverDB: {c['name']} talent calculator", f"{FOREVERDB}/class/{c['name']}/talents", "Plan a build"),
              ("Wowhead: talent calculator", f"{WOWHEAD}/talent-calc", "")]
    return pairs


def class_tools(c: dict) -> list:
    return [(f"ForeverDB: {c['name']} guide", f"{FOREVERDB}/class/{c['name']}/guide", "Abilities and changes from Classic"),
            (f"ForeverDB: {c['name']} PvE", f"{FOREVERDB}/class/{c['name']}/pve", ""),
            (f"ForeverDB: {c['name']} PvP", f"{FOREVERDB}/class/{c['name']}/pvp", ""),
            (f"ForeverDB: {c['name']} macros", f"{FOREVERDB}/class/{c['name']}/macros", ""),
            (f"ForeverDB: {c['name']} talent calculator", f"{FOREVERDB}/class/{c['name']}/talents", ""),
            ("Icy Veins: every class guide", "https://www.icy-veins.com/wow-forever/all-class-guides", ""),
            ("WoWSims: Forever simulators", "https://www.wowsims.com/forever/", "Alpha")]


def classes_index(site: Site, ctx: dict) -> str:
    b, content = site.base, ctx["content"]
    cards = []
    for c in ctx["game"]["classes"]:
        specs = "".join(f'<li><a href="{b}classes/{c["slug"]}/{s["slug"]}/">{emblem(site, "spec", c["slug"] + "-" + s["slug"], 22)}'
                        f'<span class="spec-name">{esc(s["name"])}</span></a> {roles(s)}'
                        f'<span class="pick">{pick_line(content.get(f"classes/{c['slug']}/{s['slug']}"))}</span></li>'
                        for s in c["specs"])
        cards.append(f'<li class="class-card" style="--class:{esc(c["colour"])}">'
                     f'<a class="class-card-head" href="{b}classes/{c["slug"]}/">{emblem(site, "class", c["slug"], 40, c["colour"])}<span>{esc(c["name"])}</span></a>'
                     f'<ul class="spec-list">{specs}</ul></li>')
    return layout(site, "Classes", page_head("Classes", "Nine classes, three specs each. Every spec page opens on a cheatsheet: build, priority, stats and the levels that matter.")
                  + f'''<section class="page-body">
  <ul class="class-cards">{"".join(cards)}</ul>
  <details class="reading">
    <summary>Specs, hybrids and where else to read</summary>
    <p>Forever keeps three talent trees per class, with one talent point per level from level 10, so builds that mix two trees are normal, especially while levelling. Blizzard aims for hybrid damage specs to deal about 5% less damage than pure ones, and counts warriors as hybrids (<a href="https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids" target="_blank" rel="noopener">ForeverDB on the hybrid tax</a>). Each class page has a tab for hybrid builds.</p>
    {links(ctx["game"]["hubs"])}
  </details>
</section>''', active="classes", path="classes/", description="World of Warcraft: Forever classes and specs: cheatsheets, builds, macros and guide summaries.")


def note_tab(site: Site, note: dict | None, empty: str) -> str:
    """Hybrid builds and macros: a whole note inside one tab of the class page."""
    if not note:
        return f'<p class="empty">{esc(empty)}</p>'
    return (head_facts(note) + cheatsheet(note) + take(note) + in_depth(note)
            + (f'<h3 class="part-title">Field findings</h3>{findings(note)}' if findings(note) else "")
            + (f'<h3 class="part-title">Read more</h3><div class="prose read-more">{section(note, "more")["html"]}</div>' if section(note, "more") else ""))


def class_page(site: Site, ctx: dict, c: dict) -> str:
    b, content = site.base, ctx["content"]
    overview = content.get(f"classes/{c['slug']}/overview")
    spec_cards = []
    for s in c["specs"]:
        page = content.get(f"classes/{c['slug']}/{s['slug']}")
        pick = pick_line(page) or (esc(page["summary"]) if page else "No summary yet: the guides and tools are linked on its page.")
        spec_cards.append(f'<li class="spec-card"><a class="spec-card-head" href="{b}classes/{c["slug"]}/{s["slug"]}/">'
                          f'{emblem(site, "spec", c["slug"] + "-" + s["slug"], 32)}<span>{esc(s["name"])}</span></a>'
                          f'<p class="spec-roles">{roles(s)}</p><p class="pick">{pick}</p></li>')
    hybrid = content.get(f"classes/{c['slug']}/hybrid")
    macros = content.get(f"classes/{c['slug']}/macros")
    first = (f'<ul class="spec-cards">{"".join(spec_cards)}</ul>'
             + cheatsheet(overview, f"No overview of the {c['name']} yet.") + take(overview))
    panels = [("overview", "Overview", first), ("in-depth", "In depth", in_depth(overview)),
              ("hybrid", "Hybrid builds", note_tab(site, hybrid, "No hybrid builds recorded yet.")),
              ("macros", "Macros", note_tab(site, macros, "No macros recorded yet.")
               + f'<p class="more-link"><a href="{b}more/macros/">How macros work in Forever, and more collections</a></p>'),
              ("abilities", "Abilities", class_api(ctx, c["name"])),
              ("findings", "Field findings", findings(overview)),
              ("sources", "Sources", sources_tab(site, overview, class_tools(c), entries_for(ctx, f"content/classes/{c['slug']}/")))]
    art = f'<div class="head-art" aria-hidden="true">{artwork(site, c["slug"], "character-art")}</div>' if site.art.get(c["slug"]) else ""
    return layout(site, c["name"], page_head(c["name"], "", (("Classes", f"{b}classes/"),), head_facts(overview) + spec_switch(site, c),
                                              mark=emblem(site, "class", c["slug"], 64, c["colour"]), colour=c["colour"], art=art)
                  + f'<section class="page-body" style="--class:{esc(c["colour"])}">{tabs(panels, {"findings": finding_count(overview)})}</section>',
                  active="classes", path=f"classes/{c['slug']}/", description=(overview or {}).get("summary") or f"{c['name']} in World of Warcraft: Forever: specs, hybrid builds, macros and guides.")


def spec_page(site: Site, ctx: dict, c: dict, spec: dict) -> str:
    b = site.base
    page = ctx["content"].get(f"classes/{c['slug']}/{spec['slug']}")
    empty = (f"No summary of the {spec['name']} {c['name']} guides yet. The guides and tools under Sources are the best place to start.")
    panels = [("cheatsheet", "Cheatsheet", cheatsheet(page, empty) + take(page)), ("in-depth", "In depth", in_depth(page)),
              ("findings", "Field findings", findings(page)),
              ("sources", "Sources", sources_tab(site, page, spec_tools(c, spec), entries_for(ctx, f"content/classes/{c['slug']}/{spec['slug']}.md")))]
    return layout(site, f"{spec['name']} {c['name']}",
                  page_head(f"{spec['name']} {c['name']}", "", (("Classes", f"{b}classes/"), (c["name"], f"{b}classes/{c['slug']}/")),
                            head_facts(page, roles(spec)) + spec_switch(site, c, spec["slug"]),
                            mark=emblem(site, "spec", c["slug"] + "-" + spec["slug"], 64, c["colour"]), colour=c["colour"])
                  + f'<section class="page-body" style="--class:{esc(c["colour"])}">{tabs(panels, {"findings": finding_count(page)})}</section>',
                  active="classes", path=f"classes/{c['slug']}/{spec['slug']}/",
                  description=(page or {}).get("summary") or f"{spec['name']} {c['name']} in World of Warcraft: Forever: guide summary and links.")


# --- ForeverDB API tables ----------------------------------------------------------

def api_credit(ctx: dict) -> str:
    src = ctx["api"].get("source", {})
    label = badge("prelaunch") if src.get("level_cap") != 60 else ""
    return (f'<p class="aside">{label} <a href="https://foreverdb.net">Data from ForeverDB.net</a>, game build {esc(src.get("build"))}. '
            'Places marked "Classic data" come from Classic and haven\'t been confirmed in Forever yet.</p>')


def coords(x, y) -> str:
    return f" ({x:.0f}, {y:.0f})" if isinstance(x, (int, float)) and isinstance(y, (int, float)) else ""


def where(entry: dict) -> str:
    seen = '<span class="badge live">Seen in Forever</span>' if entry.get("seen") else '<span class="badge unknown">Classic data</span>'
    return f'{esc(entry.get("zone") or "")}{coords(entry.get("x"), entry.get("y"))} {seen}'


def cost(v: dict) -> str:
    parts = [money(v["price"])] if v.get("price") else []
    parts += [f'{esc(amount)} {esc(name)}' for name, amount in v.get("costs", [])]
    return " + ".join(parts) or "free"


def profession_api(ctx: dict, slug: str) -> str:
    data = ctx["api"].get("professions", {}).get(slug)
    if not data:
        return ""
    ranks = " · ".join(f"{esc(r)} to {esc(s)}" for r, s in data["ranks"])
    trainers = sorted(data["trainers"], key=lambda t: (not t["seen"], t["side"] not in ("horde", "both"), t["up_to"] or 0))
    trainer_rows = "".join(f'<tr><th scope="row">{esc(t["name"])}{f" <span class=aside>{esc(t["title"])}</span>" if t.get("title") else ""}</th>'
                           f'<td>{esc((t["side"] or "").capitalize())}</td><td>{where(t)}</td><td class="num">{esc(t["up_to"] or "")}</td></tr>'
                           for t in trainers[:14])
    bought_rows = []
    for b in data["bought"][:40]:
        vendors = "; ".join(f'{esc(v["name"])}, {where(v)} {cost(v)}{" (limited)" if v["limited"] else ""}' for v in b["vendors"][:3])
        bought_rows.append(f'<tr><th scope="row">{esc(b["recipe"])}{" " + badge("new", "New in Forever") if b.get("new") else ""}</th>'
                           f'<td class="num">{esc(b["skill"] or "")}</td><td>{vendors}</td></tr>')
    more = len(data["bought"]) - 40
    return (f'<p>Ranks: {ranks}.</p>'
            f'<h3 class="part-title">Trainers</h3><div class="table-wrap"><table><thead><tr><th scope="col">Trainer</th><th scope="col">Faction</th><th scope="col">Where</th>'
            f'<th scope="col" class="num">Trains to</th></tr></thead><tbody>{trainer_rows}</tbody></table></div>'
            + (f'<h3 class="part-title">Recipes you buy</h3><div class="table-wrap"><table><thead><tr><th scope="col">Recipe</th><th scope="col" class="num">Skill</th>'
               f'<th scope="col">Sold by</th></tr></thead><tbody>{"".join(bought_rows)}</tbody></table></div>'
               + (f'<p class="aside">And {more} more on ForeverDB.</p>' if more > 0 else "") if bought_rows else "")
            + api_credit(ctx))


def gathering_api(ctx: dict, slug: str) -> str:
    data = ctx["api"].get("gathering", {}).get(slug)
    if not data:
        return ""
    best = "".join(f'<tr><th scope="row">{esc(b["from"])}–{esc(b["to"])}</th><td>{esc(", ".join(b["zones"]))}</td></tr>' for b in data["best"])
    extra = ""
    if data.get("nodes"):
        rows = "".join(f'<tr><th scope="row">{esc(n["name"])}</th><td class="num">{esc(n["skill"])}</td><td>{esc(", ".join(n["zones"]))}</td>'
                       f'<td class="num">{esc(n["seen"])}</td></tr>' for n in sorted(data["nodes"], key=lambda n: (n["skill"] or 0, n["name"])))
        extra = (f'<h3 class="part-title">Nodes</h3><div class="table-wrap"><table><thead><tr><th scope="col">Node</th><th scope="col" class="num">Skill</th>'
                 f'<th scope="col">Busiest zones</th><th scope="col" class="num">Spots seen in Forever</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if data.get("zones"):
        rows = "".join(f'<tr><th scope="row">{esc(z["name"])}</th><td class="num">{esc(z["skill"])}</td>'
                       f'<td>{esc(", ".join(f"{name} {chance:g}%" for name, chance in z["catch"]))}</td></tr>' for z in data["zones"])
        extra += (f'<h3 class="part-title">Fishing by zone</h3><div class="table-wrap"><table><thead><tr><th scope="col">Zone</th><th scope="col" class="num">Skill</th>'
                  f'<th scope="col">Most caught</th></tr></thead><tbody>{rows}</tbody></table></div>')
    return (f'<h3 class="part-title">Best zones by skill</h3><div class="table-wrap"><table><thead><tr><th scope="col">Skill</th><th scope="col">Zones</th></tr></thead><tbody>{best}</tbody></table></div>'
            f'{extra}<p class="aside">{esc(data.get("note") or "")}</p>' + api_credit(ctx))


def disenchant_api(ctx: dict) -> str:
    bands = ctx["api"].get("disenchant", [])
    if not bands:
        return ""
    rows = "".join(f'<tr><th scope="row">{esc(b["quality"])} {esc(b["kind"])}</th><td class="num">{esc(b["from"])}–{esc(b["to"])}</td>'
                   f'<td>{esc("; ".join(f"{name} {chance:g}% ({low}–{high})" for name, chance, low, high in b["results"]))}</td></tr>' for b in bands)
    return (f'<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col" class="num">Item level</th><th scope="col">Gives</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>' + api_credit(ctx))


def class_api(ctx: dict, name: str) -> str:
    abilities = ctx["api"].get("classes", {}).get(name)
    if not abilities:
        return ""
    lines = {}
    for a in abilities:
        lines.setdefault(a["line"] or "General", []).append(a)
    learned = {"trainer": "Trainer", "sod": "Rune-style", "quest": "Quest"}
    blocks = []
    for line, items in lines.items():
        rows = "".join(f'<tr><th scope="row">{esc(a["name"])}{" " + badge("new", "New in Forever") if a["new"] else ""}</th>'
                       f'<td>{esc(learned.get(a["learned"], (a["learned"] or "").capitalize()))}</td>'
                       f'<td>{esc(", ".join(str(l) for l in a["levels"]))}</td></tr>'
                       for a in sorted(items, key=lambda a: (min(a["levels"] or [99]), a["name"])))
        blocks.append(f'<h3 class="part-title">{esc(line)}</h3><div class="table-wrap"><table><thead><tr><th scope="col">Ability</th><th scope="col">Learned</th>'
                      f'<th scope="col">Ranks at level</th></tr></thead><tbody>{rows}</tbody></table></div>')
    return ('<p>Every ability and the level each rank is learned, by tree. Talents are on the talent calculators linked under Sources.</p>'
            + "".join(blocks) + api_credit(ctx))


# --- Professions ----------------------------------------------------------------

def profession_stats(ctx: dict, name: str) -> tuple[int, int]:
    recipes = ctx["fdb"].get("recipes", {}).get(name, [])
    return len(recipes), sum(r["new"] for r in recipes)


def professions_index(site: Site, ctx: dict) -> str:
    b = site.base
    groups = {}
    for p in ctx["game"]["professions"]:
        groups.setdefault(p["kind"], []).append(p)
    blocks = []
    for kind, items in groups.items():
        rows = []
        for p in items:
            total, new = profession_stats(ctx, p["name"])
            page = ctx["content"].get(f"professions/{p['slug']}")
            facts = f"{total:,} recipes · {new:,} new" if total > 5 else ""
            rows.append(f'<li><a class="prof-row-head" href="{b}professions/{p["slug"]}/">{emblem(site, "prof", p["slug"], 28)}<span>{esc(p["name"])}</span></a>'
                        f'<p class="pick">{pick_line(page)}</p>{f"<p class=aside>{facts}</p>" if facts else ""}</li>')
        blocks.append(f'<section class="prof-group"><h2 class="group-title">{esc(kind)}</h2><ul class="prof-rows">{"".join(rows)}</ul></section>')
    src = ctx["fdb_source"]
    note = f'<p class="note">{badge("prelaunch") if ctx["data_prelaunch"] else badge("live")} Recipe counts from ForeverDB\'s data for game build {esc(src.get("client_build"))}.</p>'
    return layout(site, "Professions", page_head("Professions", "Twelve professions: what each is for, how to level it, and where the gold is.")
                  + f'<section class="page-body"><h2 class="group-title">Making gold</h2>{gold_cards(site)}'
                  f'<div class="prof-groups">{"".join(blocks)}</div>{note}</section>',
                  active="professions", path="professions/", description="World of Warcraft: Forever professions: cheatsheets, levelling routes, camp items and margins.")


def profession_page(site: Site, ctx: dict, p: dict) -> str:
    b = site.base
    page = ctx["content"].get(f"professions/{p['slug']}")
    total, new = profession_stats(ctx, p["name"])
    camp = [k for k in ctx["fdb"].get("camp", []) if k["profession"] == p["name"]]
    camp_rows = "".join(f'<tr><th scope="row">{item_link(k["item"], k["name"])}</th><td class="num">{esc(k["skill"])}</td><td>{esc(k["effect"])}</td></tr>' for k in camp)
    crafts = [r for r in ctx["craft"] if r["profession"] == p["name"]][:6]
    craft_rows = "".join(f'<tr><th scope="row">{item_link(r["item"], r["name"])}</th><td class="num">{esc(r["skill"])}</td>'
                         f'<td class="num">{money(r["margin"])} {source_tag(r["value_source"])}</td></tr>' for r in crafts)
    label = badge("prelaunch") if ctx["data_prelaunch"] else ""
    margins = (f'<section class="side-table"><h3 class="part-title">Best estimated margins {label}</h3><div class="table-wrap"><table class="compact"><thead><tr><th scope="col">Recipe</th>'
               f'<th scope="col" class="num">Skill</th><th scope="col" class="num">Estimated margin</th></tr></thead><tbody>{craft_rows}</tbody></table></div>'
               f'<p class="aside">Asking prices, before selling and training costs; not proof of demand. <a href="{b}prices/craft/#{esc(p["name"].lower().replace(" ", "-"))}">'
               f'All {esc(p["name"])} margins</a>.</p></section>') if crafts else ""
    camp_html = (f'<section class="side-table"><h3 class="part-title">Camp items {label}</h3><div class="table-wrap"><table class="compact"><thead><tr><th scope="col">Item</th><th scope="col" class="num">Skill</th>'
                 f'<th scope="col">Effect</th></tr></thead><tbody>{camp_rows}</tbody></table></div></section>') if camp else ""
    first = cheatsheet(page, f"No summary of {p['name']} guides yet.") + take(page) + (f'<div class="pair">{margins}{camp_html}</div>' if margins or camp_html else "")
    learn = profession_api(ctx, p["slug"])
    zones = gathering_api(ctx, p["slug"]) if p["slug"] in ("herbalism", "mining", "skinning", "fishing") else ""
    tools = [(f"ForeverDB: {p['name']}", f"{FOREVERDB}/profession/{p['slug']}", "Every recipe, trainers, where to learn")]
    if p.get("wowhead"):
        tools.append((f"Wowhead: {p['name']} levelling guide", f"{WOWHEAD}/guide/professions/{p['slug']}/overview-leveling", ""))
    tools += [("Icy Veins: professions overview", "https://www.icy-veins.com/wow-forever/professions-overview", ""),
              ("ForeverDB: best profession pairs", f"{FOREVERDB}/professions/best", "")]
    count = (f'{total:,} recipes, {new:,} new in Forever (ForeverDB, game build {esc(ctx["fdb_source"].get("client_build"))})' if total > 5 else "")
    panels = [("cheatsheet", "Cheatsheet", first), ("in-depth", "In depth", in_depth(page)),
              ("trainers", "Trainers and recipes", learn), ("zones", "Where to gather", zones),
              ("disenchanting", "Disenchanting", disenchant_api(ctx) if p["slug"] == "enchanting" else ""),
              ("findings", "Field findings", findings(page)),
              ("sources", "Sources", sources_tab(site, page, tools, entries_for(ctx, f"content/professions/{p['slug']}.md")))]
    return layout(site, p["name"], page_head(p["name"], "", (("Professions", f"{b}professions/"),),
                                              head_facts(page, badge("role", p["kind"])) + (f'<p class="aside head-count">{count}</p>' if count else ""),
                                              mark=emblem(site, "prof", p["slug"], 64))
                  + f'<section class="page-body">{tabs(panels, {"findings": finding_count(page)})}</section>',
                  active="professions", path=f"professions/{p['slug']}/",
                  description=(page or {}).get("summary") or f"{p['name']} in World of Warcraft: Forever.")


# --- World ------------------------------------------------------------------------

WORLD_ICONS = {"camping": "spell_fire_fire", "legacy": "inv_misc_book_09", "merchants-favor": "inv_crate_01", "rares": "ability_hunter_pet_boar",
               "zones": "inv_misc_map_01", "dungeons-and-raids": "inv_misc_key_14", "collections": "ability_hunter_pet_crocolisk"}


def world_index(site: Site, ctx: dict) -> str:
    b = site.base
    rows = []
    for t in ctx["game"]["world"]:
        page = ctx["content"].get(f"world/{t['slug']}")
        rows.append(f'<li><a href="{b}world/{t["slug"]}/">{object_icon(WORLD_ICONS.get(t["slug"], "inv_misc_bag_10"), 40)}'
                    f'<span class="tool-name">{esc(t["name"])}</span><span class="aside">{esc(t["summary"])}</span></a></li>')
    return layout(site, "World", page_head("World", "How Forever's own systems work, and what's out there.") + banner(site, "world", "65% 60%")
                  + f'<section class="page-body"><ul class="tool-cards">{"".join(rows)}</ul></section>',
                  active="world", path="world/", description="World of Warcraft: Forever systems: camping, Legacy, Merchant's Favor, rares, zones, dungeons, raids and collections.")


def world_data(site: Site, ctx: dict, slug: str) -> str:
    fdb = ctx["fdb"]
    label = badge("prelaunch") if ctx["data_prelaunch"] else ""
    if slug == "camping" and fdb.get("camp"):
        rows = "".join(f'<tr><td>{esc(k["profession"])}</td><th scope="row">{item_link(k["item"], k["name"])}</th><td class="num">{esc(k["skill"])}</td><td>{esc(k["effect"])}</td></tr>'
                       for k in fdb["camp"])
        return (f'<h3 class="part-title">Every camp item {label}</h3><div class="table-wrap"><table><thead><tr><th scope="col">Profession</th>'
                f'<th scope="col">Item</th><th scope="col" class="num">Skill</th><th scope="col">Effect</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if slug == "merchants-favor" and fdb.get("crates"):
        return (f'<p>{label} {len(fdb["crates"])} Waylaid Crates, from level 10 to 35. Each takes any one bundle of materials from its list. '
                f'<a href="{site.base}prices/crates/">The cheapest way to fill each one</a>.</p>')
    if slug == "rares" and fdb.get("rares"):
        r = fdb["rares"]
        return (f'<p>{label} {esc(r.get("n", 0))} rare creatures are known; {esc(r.get("seen", 0))} have been seen in Forever so far. '
                'The rest come from Classic data and may differ.</p>')
    if slug == "collections" and fdb.get("collections"):
        c = fdb["collections"]
        return f'<p>{label} {esc(c.get("mounts", 0))} mounts, {esc(c.get("pets", 0))} companion pets and {esc(c.get("titles", 0))} titles.</p>'
    return ""


def world_page(site: Site, ctx: dict, t: dict) -> str:
    b = site.base
    page = ctx["content"].get(f"world/{t['slug']}")
    data = world_data(site, ctx, t["slug"])
    pairs = [(label, url if url.startswith("http") else f"{b}world/{t['slug']}/{url}", "") for label, url in t["links"]]
    art = (f'<div class="head-art camp" aria-hidden="true">{artwork(site, "camping", "camp-art")}</div>' if t["slug"] == "camping" and site.art.get("camping") else "")
    panels = [("overview", "Overview", cheatsheet(page, f"No notes on {t['name'].lower()} yet.") + take(page)),
              ("in-depth", "In depth", in_depth(page)), ("data", "Game data", data), ("findings", "Field findings", findings(page)),
              ("sources", "Sources", sources_tab(site, page, pairs, entries_for(ctx, f"content/world/{t['slug']}.md")))]
    return layout(site, t["name"], page_head(t["name"], esc(page["summary"] if page else t["summary"]), (("World", f"{b}world/"),), head_facts(page),
                                              mark=object_icon(WORLD_ICONS.get(t["slug"], "inv_misc_bag_10"), 64), art=art)
                  + f'<section class="page-body">{tabs(panels, {"findings": finding_count(page)})}</section>',
                  active="world", path=f"world/{t['slug']}/", description=f"{t['name']} in World of Warcraft: Forever.")


# --- More -------------------------------------------------------------------------

def blizzard_page(site: Site, ctx: dict, m: dict) -> str:
    blue = ctx["blue"]
    posts = blue.get("posts", [])
    fetched = blue.get("fetched")
    stale = ""
    if fetched:
        age = datetime.now(timezone.utc) - datetime.fromisoformat(fetched.replace("Z", "+00:00"))
        if age.total_seconds() > 12 * 3600:
            stale = f'<p class="note">These were last checked {nice_date(fetched)}; newer posts may be missing.</p>'
    intro = ('<p class="note">Official Blizzard posts checked against the full article text. Dedicated Forever news appears on the homepage; '
             'mixed-expansion roundups appear here with a tag and a Forever-only excerpt. Unreadable or ambiguous articles are held back. '
             'Scheduled snapshots update about every two hours. Refresh checks use a shared five-minute cache.</p>')
    return layout(site, m["name"], page_head(m["name"], esc(m["summary"])) + banner(site, "more")
                  + f'<section class="page-body">{intro}{news_widget(site, blue, "all", 60, excerpts=True)}</section>',
                  active="more", path="more/blizzard/", description="Verified Forever news and tagged mixed roundups from Blizzard.")



def more_index(site: Site, ctx: dict) -> str:
    items = "".join(f'<li><a href="{site.base}more/{x["slug"]}/"><span class="tool-name">{esc(x["name"])}</span><span class="aside">{esc(x["summary"])}</span></a></li>'
                    for x in ctx["game"]["more"])
    return layout(site, "More", page_head("More", "Getting ready to play, Blizzard's latest posts, addons, macros and known issues.")
                  + banner(site, "more") + f'<section class="page-body"><ul class="tool-cards plain">{items}</ul></section>',
                  active="more", path="more/", description="World of Warcraft: Forever launch checklist, Blizzard's posts, addons, macros and known issues.")


def more_page(site: Site, ctx: dict, m: dict) -> str:
    if m["slug"] == "blizzard":
        return blizzard_page(site, ctx, m)
    page = ctx["content"].get(f"more/{m['slug']}")
    jump = []
    for sec in (page or {}).get("sections", []):
        if sec["heading"] and sec["kind"] not in ("findings", "more"):
            jump.append(f'<li><a href="#{esc(sec["slug"])}">{esc(sec["heading"])}</a></li>')
    others = "".join(f'<li><a href="{site.base}more/{x["slug"]}/">{esc(x["name"])}</a></li>' for x in ctx["game"]["more"] if x["slug"] != m["slug"])
    main = ((f'<nav class="jump" aria-label="On this page"><ul>{"".join(jump)}</ul></nav>' if len(jump) > 2 else "")
            + render_sections(page, "Nothing recorded yet.") + changelog(site, entries_for(ctx, f"content/more/{m['slug']}.md"))
            + f'<nav class="siblings" aria-label="More"><h2 class="group-title">Also in More</h2><ul>{others}</ul></nav>')
    return layout(site, m["name"], page_head(m["name"], esc(page["summary"] if page else m["summary"]), (("More", f"{site.base}more/"),), head_facts(page))
                  + (banner(site, "more") if m["slug"] == "launch" else "")
                  + f'<section class="page-body single">{main}</section>',
                  active="more", path=f"more/{m['slug']}/", description=f"World of Warcraft: Forever {m['name'].lower()}: {m['summary']}")


def inbox_page(site: Site, ctx: dict) -> str:
    """The hidden form: not in the menu, sitemap or search, and marked noindex. A plain HTML form
    posting to the inbox Site, so it works without JavaScript for a person or an agent."""
    inbox = ctx["game"].get("inbox") or {}
    shut = "" if inbox.get("open") else " disabled"
    notice = "" if inbox.get("open") else ('<p class="inbox-closed"><strong>The inbox is not open yet.</strong> '
                                                      'This form starts working once its receiver is running.</p>')
    body = page_head("Inbox", "Send a finished guide page or an addon's saved-variables file. You need a key and the instructions that come with it.") + f'''<section class="page-body prose">
  {notice}
  <form class="inbox-form" method="post" action="{esc(inbox.get("endpoint", ""))}" enctype="multipart/form-data">
    <label>Key <input type="password" name="key" required autocomplete="off" spellcheck="false"></label>
    <fieldset><legend>What you're sending</legend>
      <label class="choice"><input type="radio" name="kind" value="page" checked> A guide page</label>
      <label class="choice"><input type="radio" name="kind" value="lua"> An addon's file (.lua)</label>
    </fieldset>
    <h2>A guide page</h2>
    <label>Page path <input type="text" name="path" placeholder="content/classes/mage/frost.md" spellcheck="false"></label>
    <label>Version you edited <input type="text" name="version" placeholder="the 12 characters shown in feed/guides.md" spellcheck="false"></label>
    <label>One-line change note <input type="text" name="message" placeholder="Frost Mage: Blizzard-kiting from 22, tested"></label>
    <label>The whole page <textarea name="page" rows="16" spellcheck="false"></textarea></label>
    <h2>An addon's file</h2>
    <label>File <input type="file" name="file" accept=".lua"></label>
    <label>Market, for Auctionator only <input type="text" name="market" placeholder="Realm Horde"></label>
    <p><button type="submit"{shut}>Send</button></p>
  </form>
</section>'''
    html_text = layout(site, "Inbox", body, path="inbox/", description="Send a page or an addon file.")
    return html_text.replace('<meta name="viewport"', '<meta name="robots" content="noindex, nofollow">\n<meta name="viewport"', 1)


def about_page(site: Site, ctx: dict) -> str:
    scans = "".join(f'<li>{when(c["capture_date"])}, {esc(c["environment_label"])}: {c["source_bytes"]:,} bytes, fingerprint <code>{esc(c["source_sha256"][:16])}</code></li>'
                    for c in reversed(ctx["captures"]))
    src, names = ctx["fdb_source"], ctx["names_source"] or {}
    pictures = ''.join(f'<li><strong>{esc(a["title"])}</strong> — {esc(a["edition"])}. '
                       f'<a href="{esc(a["source"])}"{ext(a["source"])}>Source</a>.</li>' for a in site.art.values())
    return layout(site, "Sources and credits", page_head("Sources and credits", "Where everything in Tazdingo comes from, and how to read it.")
                  + f'''<section class="page-body prose">
  <h2>What this is</h2>
  <p>Tazdingo is a small, unofficial record of World of Warcraft: Forever: what things cost on the Auction House, what cited guides say about each class, spec and profession, how the new systems work, and the addons, macros and known issues worth knowing. The field notes and personally collected market data mainly follow Horde characters; Alliance information remains welcome. Loktar Ogar. It isn't affiliated with or endorsed by Blizzard Entertainment.</p>
  <h2>Labels</h2>
  <p>{badge("prelaunch")} marks anything written before launch on 4 November 2026, or not yet confirmed in the live game: treat it as tentative. A page becomes {badge("live")} only once it has been checked in the live game. {badge("beta")} marks prices from Forever Beta scans. Our own findings say how well they're tested: idea, testing, tested or outdated.</p>
  <h2>Guide summaries</h2>
  <p>Each class, spec, profession and world page summarises what other sites' guides say, in our own words, and links to sources inline and under "Read more". The guides belong to their authors: read them for the full detail, the reasoning and their updates. Summaries were written from guides published before launch, most of which only covered levels 1 to 30.</p>
  <h2 id="recommendations">How recommendations are weighed</h2>
  <p>A Tazdingo recommendation is an editorial conclusion: a practical default, when an alternative fits better and what it costs. Later official changes settle mechanics; an older guide does not remain an equally valid alternative after its rule changes. Several sites repeating the same claim do not make independent evidence.</p>
  <p>Beta play reports, client data and simulator presets answer different questions. Level, Legacy points, gear, buffs, targets and fight length must match before comparing builds. Model weights and gains are source snapshots, not locally reproduced tests or universal shopping priorities. Unresolved details remain labelled, and Field findings stay separate. A page's update date records an edit, not an in-game verification.</p>
  <h2>Prices</h2>
  <p>Prices come from our own Auctionator scans. Only the addon's price records are published. The typical price is the middle value of each day's cheapest listing over the item's last seven days, so one odd listing doesn't set it. Steadiness compares the spread of those daily prices over two weeks with the typical price. Dates follow Auctionator's own day counter, which starts on 1 January 2020.</p>
  <p>Where our scans don't hold an item, the market tables use prices from ForeverDB's players' scans, labelled as such, and vendor prices recorded by ForeverDB's players. These are asking prices, not completed sales. Crafting margins omit selling fees and other costs; stock, binding and actual demand still need checking.</p>
  <h3>Our scans</h3><ul class="scans">{scans}</ul>
  <h2>Game data</h2>
  <p>Item names, recipes, camp items, Waylaid Crates, rare and collection counts, other players' prices and vendor prices: <a href="{FOREVERDB}">Data from ForeverDB.net</a> (game build {esc(src.get("client_build"))}, fetched {esc(src.get("fetched_on"))}; names fetched {esc(names.get("fetched_on"))}). Item tooltips use <a href="{FOREVERDB}/embed">ForeverDB's embed</a> and show the provider's current details rather than an archived tooltip from the scan date.</p>
  <h2>Blizzard's posts</h2>
  <p>The <a href="{site.base}more/blizzard/">Blizzard posts</a> page lists Forever-specific official articles and staff posts, plus clearly tagged mixed roundups on the inner page. Classification uses article text and section context; it can still miss or misclassify an article. Follow the original for current details.</p>
  <h2>Guides, tools and data elsewhere</h2>
  <p>Wowhead, Icy Veins, ForeverDB, WoWSims, Method, Warcraft Tavern, Kami Labs, CurseForge and Blizzard's forums, among others; each page lists the ones it draws on.</p>
  {links(ctx["game"]["hubs"])}
  <h2>Data files</h2>
  <p>The whole site as plain text: <a href="{site.base}llms-full.txt">llms-full.txt</a> (short index: <a href="{site.base}llms.txt">llms.txt</a>). Every market's prices and daily history as TSV, linked from its page; every priced recipe in <a href="{site.base}prices/craft.tsv">craft.tsv</a>.</p>
  <h2 id="pictures">Pictures</h2>
  <p>Artwork and screenshots © Blizzard Entertainment. The scenery comes from the official Forever reveal press kit. Character cut-outs come from Blizzard's original World of Warcraft Fan Site Kit, preserved by the Internet Archive: these are Classic illustrations, not Forever screenshots or examples of recommended equipment. Images retain their original composition, with smaller WebP copies for delivery; page layouts may show part of a scene.</p>
  <ul class="image-credits">{pictures}</ul>
  <p>Class, spec, profession, creature and item icons are served by <a href="https://render.worldofwarcraft.com/">Blizzard's icon renderer</a>. Item icons inside tooltips come through ForeverDB. Decorative paper textures and the Tazdingo mark were made for this site.</p>
</section>''', active="more", path="more/about/", description="Where Tazdingo's prices, guide summaries, game data and Blizzard posts come from.")

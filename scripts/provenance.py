"""Checks on a submitted guide page beyond its format: provenance and change rules.

Code can't know whether a claim about the game is true. These checks make every claim
traceable and catch what a machine can catch, comparing the submitted page with the version
it replaces (docs/chatgpt/UPDATING.md's rules, enforced):

- problems hold the submission: a finding without a confidence, date or way of knowing; a
  source summary without a link; a cost without its source; a deleted finding; a link to an
  item ForeverDB doesn't know; a public commit message that breaks the rules.
- review reasons send it to the owner as a pull request instead of applying it: a page set
  Live or re-verified, a changed Tazdingo recommendation, a finding marked outdated, a link to
  a site no page has cited before.
"""
from __future__ import annotations

import difflib
import html
import re
from datetime import date, datetime
from urllib.parse import urlsplit

from markup import render

HEADING = re.compile(r"(#{1,4})\s+(.*?)\s*#*$")  # markup.render's own heading rule

FINDING = re.compile(r"^### (?P<claim>.+?) \((?P<confidence>idea|testing|tested|outdated), (?P<date>\d{1,2} [A-Z][a-z]{2} \d{4})\)\s*$")
HOW_KNOWN = re.compile(r"\b(?:in game|in-game|tested|level \d+|simulat\w*|read (?:on|in)|according to)\b|https?://", re.I)
MONEY = re.compile(r"\b\d[\d,]*\s?(?:gold|silver|copper)\b|\b\d[\d,]*g\b", re.I)  # "100 gold", "10g"; not "30s" (seconds)
SOURCE_NAMES = ("Wowhead", "Icy Veins", "ForeverDB", "Blizzard", "Method", "Warcraft Tavern", "WoWSims", "wow-professions",
                "CurseForge", "WoW TBC", "wowtbc.gg", "Kami", "Forever Changes")
ITEM_LINK = re.compile(r"foreverdb\.net/item/(\d+)")
EMPTY_FINDINGS = "nothing recorded yet"
BAD_MESSAGE_WORDS = re.compile(r"\b(?:update|updated|misc|chatgpt|fares|mike)\b", re.I)


def urls_in(text: str) -> list[str]:
    """Every address the site actually links to: the hrefs of the rendered page, so a link the
    renderer makes (in a table, say) is seen and one it doesn't (inside code) isn't."""
    return [html.unescape(u) for u in re.findall(r'<a href="([^"]*)"', render(text))]


def normalise(body: str) -> str:
    """Headings as the renderer reads them ('###<tab>Title  ###' is '### Title'), so the
    comparisons below see the same structure the page will show."""
    lines = []
    for line in body.splitlines():
        match = HEADING.match(line)
        lines.append(f"{match[1]} {match[2]}" if match else line)
    return "\n".join(lines)


PLAIN_HOST = re.compile(r"[A-Za-z0-9.-]+(?::\d{1,5})?")


def plain(url: str) -> bool:
    """A link whose host every reader agrees on: no backslashes, user@ parts or unusual characters,
    which browsers and Python's URL parser can read as different hosts."""
    if "\\" in url or not url.isascii():
        return False
    rest = url.split("//", 1)[1] if url.startswith(("http://", "https://", "//")) else ""
    authority = re.split(r"[/?#]", rest, 1)[0]
    return not rest or bool(PLAIN_HOST.fullmatch(authority))


def domain(url: str) -> str:
    host = (urlsplit(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def domains_in(text: str) -> set[str]:
    """The sites a page links to, protocol-relative links (//host) included."""
    return {domain(u) for u in urls_in(text) if u.startswith(("http://", "https://", "//"))} - {""}


def has_source_link(text: str) -> bool:
    return any(u.startswith(("http://", "https://")) for u in urls_in(text))


def sections(body: str) -> dict[str, str]:
    """`## ` sections by heading."""
    result, heading, lines = {}, "", []
    for line in body.splitlines():
        if line.startswith("## "):
            result[heading] = "\n".join(lines).strip()
            heading, lines = line[3:].strip(), []
        else:
            lines.append(line)
    result[heading] = "\n".join(lines).strip()
    return result


def subsection_list(text: str) -> list[tuple[str, str]]:
    """`### ` subsections as (heading, text), in order; text before the first has heading ''."""
    result, heading, lines = [], "", []
    for line in text.splitlines():
        if line.startswith("### "):
            result.append((heading, "\n".join(lines).strip()))
            heading, lines = line.rstrip(), []
        else:
            lines.append(line)
    result.append((heading, "\n".join(lines).strip()))
    return result


def subsections(text: str) -> dict[str, str]:
    return dict(subsection_list(text))


def repeated(items: list[str]) -> set[str]:
    return {i for i in items if i and items.count(i) > 1}


def findings(body: str) -> dict[str, tuple[str, str]]:
    """Field findings: {claim: (confidence, body, date)}; headings that don't match the format are
    returned under their raw heading with confidence None."""
    text = sections(body).get("Field findings", "")
    result = {}
    for heading, content in subsections(text).items():
        if not heading:
            continue
        match = FINDING.match(heading)
        if match:
            result[match["claim"]] = (match["confidence"], content, match["date"])
        else:
            result[heading] = (None, content, None)
    return result


def message_problems(message: str) -> list[str]:
    problems = []
    if not message or "\n" in message.strip():
        problems.append("the commit message must be one line")
    elif len(message) > 100:
        problems.append("the commit message must be under 100 characters")
    elif ": " not in message or message.endswith("."):
        problems.append("the commit message must read '<Page>: <what changed>', with no full stop")
    if BAD_MESSAGE_WORDS.search(message or ""):
        problems.append("the commit message can't name anyone, mention the assistant, or say 'update' or 'misc'")
    return problems


def added_paragraphs(old: str, new: str) -> list[str]:
    """Paragraphs of the new text that contain an added or changed line."""
    added = {line for line in difflib.ndiff(old.splitlines(), new.splitlines()) if line.startswith("+ ")}
    added = {line[2:] for line in added if line[2:].strip()}
    return [p for p in re.split(r"\n\s*\n", new) if any(line in added for line in p.splitlines())]


def check(old: str | None, new: str, meta: dict, old_meta: dict, known_domains: set[str], item_ids: set[int],
          today: date) -> tuple[list[str], list[str]]:
    """(problems, review reasons) for a submitted page body `new` replacing `old`."""
    problems, review = [], []
    old, new = normalise(old or ""), normalise(new)
    # Repeated headings would let one copy hide behind another in the comparisons below.
    for name in ("What the guides say", "Field findings"):
        heads = [h for h, _ in subsection_list(sections(new).get(name, ""))]
        claims = [m["claim"] if (m := FINDING.match(h)) else h for h in heads]
        for head in sorted(repeated(claims)):
            problems.append(f"'{head.lstrip('# ')}' appears twice under {name}; each heading must be unique")
    if len([line for line in new.splitlines() if line.startswith("## ")]) != len({line for line in new.splitlines() if line.startswith("## ")}):
        problems.append("a section heading appears twice")
    if any(u.startswith("//") for u in urls_in(new)):
        problems.append("write links in full, starting https://")
    if not all(plain(u) for u in urls_in(new)):
        problems.append("write each link's address plainly: no backslashes, '@' or unusual characters in it")
    try:
        updated = date.fromisoformat(meta.get("updated", ""))
        if abs((updated - today).days) > 2:
            problems.append(f"set 'updated:' to today's date ({today.isoformat()})")
    except ValueError:
        problems.append("'updated:' must be a date, YYYY-MM-DD")

    # Findings: each has a confidence, a date and how it's known; none is ever deleted.
    new_findings, old_findings = findings(new), findings(old)
    findings_text = sections(new).get("Field findings", "")
    if findings_text.strip().rstrip(".").lower() != EMPTY_FINDINGS:
        if subsections(findings_text).get(""):
            problems.append("text under Field findings must sit under a finding's heading, or the section must say 'Nothing recorded yet.'")
        for claim, (confidence, content, when) in new_findings.items():
            if confidence is None:
                problems.append(f"finding {claim!r} needs its confidence and date in brackets, e.g. '### Claim (tested, 6 Nov 2026)'")
                continue
            try:
                datetime.strptime(when, "%d %b %Y")
            except ValueError:
                problems.append(f"finding {claim!r} has an unreadable date {when!r}")
            if old_findings.get(claim, (None, None))[1] != content and not HOW_KNOWN.search(content):
                problems.append(f"finding {claim!r} must say how it's known: tested in game (level, situation), read (with a link) or simulated (tool)")
    for claim, (confidence, _content, _when) in old_findings.items():
        if claim not in new_findings:
            problems.append(f"finding {claim!r} was removed; findings are never deleted, mark it outdated with the reason instead")
        elif new_findings[claim][0] == "outdated" and confidence != "outdated":
            review.append(f"finding {claim!r} marked outdated")

    # Source summaries carry links; the recommendation is the owner's call.
    old_guides, new_guides = subsections(sections(old).get("What the guides say", "")), subsections(sections(new).get("What the guides say", ""))
    def recommendation(guides: dict) -> list[str]:
        return [f"{h}\n{c}" for h, c in guides.items() if h.lower().startswith("### tazdingo recommendation")]
    if recommendation(old_guides) != recommendation(new_guides):
        review.append("the Tazdingo recommendation changed")
    # The cheatsheet condenses that advice into the page's first screen, so it's the owner's call too.
    def cheatsheet(text: str) -> list[str]:
        return [body.strip() for heading, body in sections(text).items() if heading.lower() in ("cheatsheet", "at a glance")]
    if cheatsheet(old) != cheatsheet(new):
        review.append("the cheatsheet changed")
    for heading, content in new_guides.items():
        if heading.lower().startswith("### tazdingo recommendation"):
            continue
        if content and old_guides.get(heading) != content and not has_source_link(content):
            problems.append(f"'{heading.lstrip('# ') or 'What the guides say'}' summarises sources without linking them")

    # Costs need their source; item links must be real items; new sites get a look.
    for paragraph in added_paragraphs(old, new):
        if MONEY.search(paragraph) and not has_source_link(paragraph) and not any(n.lower() in paragraph.lower() for n in SOURCE_NAMES):
            problems.append(f"a cost needs its source (a link or the site's name): {paragraph[:80]!r}")
        for item in ITEM_LINK.findall(paragraph):
            if int(item) not in item_ids:
                problems.append(f"item {item} isn't an item ForeverDB knows")
    for site in sorted(domains_in(new) - domains_in(old) - known_domains):
        review.append(f"a link to {site}, a site no page has cited before")

    # Live and verified are claims about the live game.
    if meta.get("status") == "live" and old_meta.get("status") != "live":
        review.append("the page is set Live")
    if meta.get("verified") and meta.get("verified") != old_meta.get("verified"):
        review.append("the page's verified date changed")
    return problems, review

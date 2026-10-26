"""The Markdown that journal entries use, converted to HTML with the standard library.

Covers what ChatGPT and Claude write in practice: headings, paragraphs, bullet and
numbered lists (nested by indentation), quotes, code, tables, rules, links,
bold and italics. Everything else is escaped and shown as text, never as HTML.
"""
from __future__ import annotations

import html
import re

EMPHASIS = [
    (re.compile(r"\*\*(.+?)\*\*"), lambda m: f"<strong>{m.group(1)}</strong>"),
    (re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])"), lambda m: f"<em>{m.group(1)}</em>"),
    (re.compile(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])"), lambda m: f"<em>{m.group(1)}</em>"),
]
LINK = re.compile(r"\[([^\]]+)\]\(((?:https?://|/|#)[^\s)]*)\)")
BARE_URL = re.compile(r"(?<![\"'=>])(https?://[^\s<\"']+[^\s<\"'.,;:!?)\]])")


def emphasis(text: str) -> str:
    for pattern, replace in EMPHASIS:
        text = pattern.sub(replace, text)
    return text


def inline(text: str) -> str:
    """Escape, then apply links and emphasis. Code spans are protected from both,
    and a link whose address would contain a code span stays plain text: restored
    code HTML must never land inside an attribute."""
    out, codes = html.escape(text, quote=True), []

    def keep(match):
        codes.append(f"<code>{match.group(1)}</code>")
        return f"\x00{len(codes) - 1}\x00"
    out = re.sub(r"`([^`]+)`", keep, out)
    links = []

    def link(match):
        if "\x00" in match.group(2):
            return match.group(0)
        label, url = match.group(1), html.escape(html.unescape(match.group(2)), quote=True)
        external = url.startswith("http")
        attrs = ' target="_blank" rel="noopener"' if external else ""
        links.append(f'<a href="{url}"{attrs}>{emphasis(label)}</a>')
        return f"\x01{len(links) - 1}\x01"
    out = LINK.sub(link, out)

    def bare(match):
        if "\x00" in match.group(1):
            return match.group(0)
        url = html.escape(html.unescape(match.group(1)), quote=True)
        links.append(f'<a href="{url}" target="_blank" rel="noopener">{url}</a>')
        return f"\x01{len(links) - 1}\x01"
    out = BARE_URL.sub(bare, out)
    out = emphasis(out)
    out = re.sub(r"\x01(\d+)\x01", lambda m: links[int(m.group(1))], out)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], out)


def table(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]
    aligns = []
    for spec in cells[1]:
        aligns.append("right" if spec.endswith(":") and not spec.startswith(":") else
                      "center" if spec.startswith(":") and spec.endswith(":") else "")
    def cell(tag, value, i):
        style = f' style="text-align:{aligns[i]}"' if i < len(aligns) and aligns[i] else ""
        return f"<{tag}{style}>{inline(value)}</{tag}>"
    thead = "".join(cell("th", v, i) for i, v in enumerate(head))
    tbody = "".join("<tr>" + "".join(cell("td", v, i) for i, v in enumerate(r)) + "</tr>" for r in body)
    return f'<div class="table-wrap"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>'


def lists(lines: list[str]) -> str:
    """Bullet/numbered lists; deeper indentation opens a nested list."""
    out, stack = [], []  # stack of (indent, tag)
    for line in lines:
        match = re.match(r"(\s*)([-*+]|\d+[.)])\s+(.*)", line)
        if not match:  # continuation of the previous item
            out[-1] = out[-1][:-5] + " " + inline(line.strip()) + "</li>"
            continue
        indent, tag = len(match.group(1).expandtabs(4)), "ol" if match.group(2)[0].isdigit() else "ul"
        while stack and indent < stack[-1][0]:
            out.append(f"</{stack.pop()[1]}></li>")
        if stack and indent == stack[-1][0] and tag != stack[-1][1]:  # bullets then numbers: a new list
            out.append(f"</{stack.pop()[1]}>" + ("</li>" if stack else ""))
            if stack:
                out[-2:] = ["".join(out[-2:])]
        if not stack or indent > stack[-1][0]:
            if stack:
                out[-1] = out[-1][:-5]
            stack.append((indent, tag))
            out.append(f"<{tag}>")
        out.append(f"<li>{inline(match.group(3))}</li>")
    while stack:
        out.append(f"</{stack.pop()[1]}>" + ("</li>" if stack else ""))
    return "".join(out)


def heading_id(text: str, used: set) -> str:
    """A stable, unique anchor for a heading, so pages can link to their own sections."""
    base = re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", text)).lower()).strip("-") or "section"
    slug, n = base, 2
    while slug in used:
        slug, n = f"{base}-{n}", n + 1
    used.add(slug)
    return slug


def render(source: str, used: set | None = None) -> str:
    """Markdown to HTML. `used` collects heading anchors across several calls for one page."""
    used = set() if used is None else used
    lines, out, i = source.replace("\r\n", "\n").split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("```")), len(lines))
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1:end])) + "</code></pre>")
            i = end + 1
        elif match := re.match(r"(#{1,4})\s+(.*?)\s*#*$", line):
            level = max(len(match.group(1)), 2)  # the page title is the only h1
            text = inline(match.group(2))
            out.append(f'<h{level} id="{heading_id(text, used)}">{text}</h{level}>')
            i += 1
        elif re.fullmatch(r"\s*([-*_])(\s*\1){2,}\s*", line):
            out.append("<hr>")
            i += 1
        elif line.lstrip().startswith(">"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{render(chr(10).join(block), used)}</blockquote>")
        elif "|" in line and i + 1 < len(lines) and re.fullmatch(r"\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*", lines[i + 1]):
            rows = []
            while i < len(lines) and "|" in lines[i]:
                rows.append(lines[i])
                i += 1
            out.append(table(rows))
        elif re.match(r"\s*([-*+]|\d+[.)])\s+", line):
            block = []
            while i < len(lines) and lines[i].strip() and (re.match(r"\s*([-*+]|\d+[.)])\s+", lines[i]) or lines[i].startswith("  ")):
                block.append(lines[i])
                i += 1
            out.append(lists(block))
        else:
            block = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,4}\s|```|>|\s*([-*+]|\d+[.)])\s+|\s*([-*_])(\s*\3){2,}\s*$)", lines[i]):
                block.append(lines[i].strip())
                i += 1
            out.append("<p>" + inline(" ".join(block)) + "</p>")
    return "\n".join(out)

#!/usr/bin/env python3
"""A very small block-level markdown renderer, stdlib only.

It exists for one reason: the articles are written in markdown and published as HTML,
and the markdown file has to stay the source of truth. An article is the one thing on
this site somebody will want to paste somewhere else — into a newsletter, a post, an
email — and a markdown file is what pastes. So `articles/<slug>.md` is written, and
`articles/<slug>.html` is generated from it. Two renderings of one file cannot drift.

It handles what an article on this site actually uses and nothing else: headings,
paragraphs, lists, blockquotes, fenced code, pipe tables and horizontal rules, with
links, bold, italic and code inline. Anything more exotic is a sign the article wants
to be a page instead.

THE BLOCKQUOTE RULE. validate.js fails the release on a `<blockquote>` that does not
declare whose words it carries, and that rule is the site's licence armour rather than
a formatting preference. So every blockquote in an article ends with an attribution
line — a line beginning with an em dash — and this renderer turns it into the
`data-quote` attribute:

    > Design is not just what it looks like. Design is how it works.
    > — Steve Jobs

    > It centers on preserving developer flow state.
    > — Dinis Cruz, `ifd/v1.2.1__ifd__intro-and-how-to-use.md`

The first becomes data-quote="Steve Jobs" and is capped at 40 words by the gate. The
second becomes data-quote="founder" and is not. A blockquote with no attribution line
raises here, at build time, with the file and the text — which is a better place to
find out than a red CI job.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import esc, md_inline                                  # noqa: E402

FOUNDER = "Dinis Cruz"


def slug(text):
    """A heading id, from its text. Stable enough to link to and short enough to read —
    and it has to be stable, because validate.js checks that every #fragment on this
    site resolves to an id that exists."""
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60] or "section"


def _attribution(lines, where):
    """Split a blockquote's body from its trailing attribution line, and work out who
    the words belong to. Raises rather than guessing: an unattributed quotation is the
    one thing this site must not publish."""
    for n in range(len(lines) - 1, -1, -1):
        if lines[n].strip():
            last = lines[n].strip()
            break
    else:
        raise ValueError(f"{where}: empty blockquote")
    if not last.startswith(("—", "--", "–")):
        raise ValueError(
            f"{where}: blockquote has no attribution line. Every quotation on this site "
            f"must say whose words it carries — end it with a line beginning '— '. "
            f"Text was: {' '.join(lines)[:80]}…")
    who = re.sub(r"^[—–-]+\s*", "", last).split(",")[0].strip()
    who = re.sub(r"<[^>]+>|[`*]", "", who).strip()
    body = lines[:n]
    return body, ("founder" if who == FOUNDER else who), last


def _table(rows):
    head = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    body = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows[2:]]
    th = "".join(f"<th>{md_inline(c)}</th>" for c in head)
    tr = "\n".join("      <tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>"
                   for r in body)
    return ('<div class="tablewrap">\n  <table>\n'
            f'    <thead><tr>{th}</tr></thead>\n    <tbody>\n{tr}\n    </tbody>\n'
            '  </table>\n</div>')


def render(text, where="<article>"):
    """markdown -> HTML. Returns (html, headings) where headings is [(level, id, text)]
    so a caller can build a contents list without re-parsing."""
    out, heads = [], []
    lines = text.replace("\r\n", "\n").split("\n")
    i, n = 0, len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        # fenced code
        if line.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append('<pre class="shell">' + esc("\n".join(buf)) + "</pre>")
            continue

        # heading
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            html_txt = md_inline(txt)
            sid = slug(txt)
            heads.append((lvl, sid, txt))
            out.append(f'<h{lvl} id="{sid}">{html_txt}</h{lvl}>')
            i += 1
            continue

        # horizontal rule
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # blockquote
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            body, who, attrib = _attribution(buf, where)
            inner = " ".join(x.strip() for x in body if x.strip())
            out.append(f'<blockquote data-quote="{esc(who)}">{md_inline(inner)}\n'
                       f'<footer>{md_inline(attrib)}</footer></blockquote>')
            continue

        # table
        if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            buf = []
            while i < n and lines[i].lstrip().startswith("|"):
                buf.append(lines[i])
                i += 1
            out.append(_table(buf))
            continue

        # lists — one level, which is all an article here has ever needed
        m = re.match(r"^\s*([-*]|\d+\.)\s+(.*)$", line)
        if m:
            ordered = m.group(1)[0].isdigit()
            items = []
            while i < n:
                mm = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", lines[i])
                if mm:
                    items.append(mm.group(1).strip())
                    i += 1
                elif lines[i].startswith(("  ", "\t")) and lines[i].strip() and items:
                    items[-1] += " " + lines[i].strip()          # a wrapped item
                    i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            body = "\n".join(f"  <li>{md_inline(x)}</li>" for x in items)
            out.append(f"<{tag}>\n{body}\n</{tag}>")
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|>|```|\s*([-*]|\d+\.)\s|\s*\|)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + md_inline(" ".join(buf)) + "</p>")

    return "\n".join(out), heads

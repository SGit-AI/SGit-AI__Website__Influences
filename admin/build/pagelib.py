#!/usr/bin/env python3
"""Shared plumbing for this site's page generators.

Every generator needs the same two things: a page shell in the house design language,
and a writer that can also run in --check mode so CI can prove a generated page still
matches its source.

The --check comparison ignores the nav and footer blocks. Those are owned by
chrome.py, which rewrites them in place AFTER generation, so a byte-for-byte compare
of a generated file against fresh generator output would always differ on chrome
alone. Stripping both blocks from both sides compares exactly what the generator is
responsible for, and nothing it is not.

Tallies are stripped for the same reason: chrome.py fills the tier counts in after
generation, from data/influences.json, and validate.js checks them independently.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOST = (ROOT / "CNAME").read_text().strip()
VERSION = (ROOT / "admin/build/version.txt").read_text().strip()

NAV_STUB = '<nav class="site"><div class="row"></div></nav>'
FOOT_STUB = '<footer class="site"><div class="cols"></div></footer>'

_CHROME = re.compile(r'<nav class="site">.*?</nav>|<footer class="site">.*?</footer>', re.S)
_TALLY = re.compile(r'(<span class="tally" data-k="[^"]+">)[^<]*(</span>)')


def _neutral(text):
    return _TALLY.sub(r"\1\2", _CHROME.sub("", text))


def influences():
    """The register, from the one file that owns it. Returns [] before the data lands —
    this site's first release is the pipeline, and a generator that crashes on an absent
    register cannot be the thing that proves the pipeline works."""
    p = ROOT / "data/influences.json"
    if not p.exists():
        return []
    return json.loads(p.read_text())["influences"]


def register_data():
    p = ROOT / "data/influences.json"
    return json.loads(p.read_text()) if p.exists() else {"influences": []}


def tallies(inf=None):
    """The counts, computed. Every number this site states about its own shape comes
    from here — nothing about the tiers is typed by a person, because tier movement is
    the one event the site exists to record and a hand-typed count goes stale on it."""
    inf = influences() if inf is None else inf
    return {
        "total":               len(inf),
        "traced":              sum(1 for i in inf if i["tier"] == "traced"),
        "stated":              sum(1 for i in inf if i["tier"] == "stated"),
        "discovered":          sum(1 for i in inf if i["tier"] == "discovered"),
        "discovered-origin":   sum(1 for i in inf if i.get("discovered") or i["tier"] == "discovered"),
        "full":                sum(1 for i in inf if i["status"] == "full"),
        "link-out":            sum(1 for i in inf if i["status"] == "link-out"),
        "stub":                sum(1 for i in inf if i["status"] == "stub"),
        "awaiting-briefing":   sum(1 for i in inf if i.get("briefing_status") == "requested"),
    }


def page_head(rel, title, description, og_title=None, og_description=None, extra_head=""):
    """The <head> and the nav stub. `rel` is the page's path from the repo root — it is
    what makes the canonical URL, and validate.js requires every page to declare one on
    the host named in CNAME."""
    up = "../" * (len(Path(rel).parts) - 1)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://{HOST}/{rel}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{HOST}">
<meta property="og:url" content="https://{HOST}/{rel}">
<meta property="og:title" content="{og_title or title}">
<meta property="og:description" content="{og_description or description}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{up}assets/site.css">{extra_head}
</head>
<body>

{NAV_STUB}
'''


def page_tail():
    return f'\n{FOOT_STUB}\n\n</body>\n</html>\n'


def write_or_check(path, content, check, changed, mismatched):
    """Write the page, or in --check mode report whether it is out of date.

    A generated page that has drifted from its source is a build failure here, not a
    warning: the whole reason a page is generated is that nobody has to remember to
    update it, and a drifted page quietly breaks that promise."""
    path = Path(path)
    if check:
        if not path.exists():
            mismatched.append(f"{path.relative_to(ROOT)} — missing (never generated)")
            return
        if _neutral(path.read_text()) != _neutral(content):
            mismatched.append(f"{path.relative_to(ROOT)} — out of date, re-run the generator")
        return
    before = path.read_text() if path.exists() else None
    if before is not None and _neutral(before) == _neutral(content):
        return                                   # unchanged: keep the chrome already applied
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    changed.append(str(path.relative_to(ROOT)))


def write_plain(path, content, check, changed, mismatched):
    """Same, for a file with no chrome in it — a markdown or JSON twin."""
    path = Path(path)
    if check:
        if not path.exists():
            mismatched.append(f"{path.relative_to(ROOT)} — missing (never generated)")
        elif path.read_text() != content:
            mismatched.append(f"{path.relative_to(ROOT)} — out of date, re-run the generator")
        return
    if path.exists() and path.read_text() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    changed.append(str(path.relative_to(ROOT)))


def report(name, check, changed, mismatched):
    if check:
        if mismatched:
            print(f"{name} --check: {len(mismatched)} file(s) out of date", file=sys.stderr)
            for m in mismatched:
                print("  ✗ " + m, file=sys.stderr)
            sys.exit(1)
        print(f"{name} --check: OK — every generated file matches its source")
        return
    print(f"{name}: {len(changed)} file(s) written")
    for c in changed:
        print("  · " + c)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


_MD_CODE = re.compile(r"`([^`]+)`")
_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_MD_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_MD_ITAL = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")


def md_inline(s):
    """The register's prose is authored ONCE, in data/influences.json, in a deliberately
    tiny markdown: links, bold, italic, code. This turns it into HTML for the page; the
    markdown twin ships the same string untouched.

    Two renderings of one string is the only arrangement that cannot drift. Authoring the
    HTML page and writing the .md twin by hand is the arrangement that always does."""
    s = esc(s)
    s = _MD_CODE.sub(r"<code>\1</code>", s)
    s = _MD_LINK.sub(r'<a href="\2">\1</a>', s)
    s = _MD_BOLD.sub(r"<b>\1</b>", s)
    s = _MD_ITAL.sub(r"<i>\1</i>", s)
    return s

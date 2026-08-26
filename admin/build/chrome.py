#!/usr/bin/env python3
"""The single definition of this site's nav and footer, and the tool that applies it.

Run from anywhere: python3 admin/build/chrome.py

Every hand-written page is static HTML — that stays true, because a human should be
able to open any file and edit it. What is NOT hand-maintained is the chrome: the nav
row (including the version badge that validate.js requires to agree everywhere) and
the footer columns. Those are defined once here and rewritten in place across the
tree, which is what stops a forty-page site from drifting.

It also runs over the GENERATED pages, so a nav change does not require re-running the
generators — and the generators emit the same block shapes for exactly that reason.

And it fills the TALLIES: every `<span class="tally" data-k="traced">` on the site gets
its number from data/influences.json here, and nowhere else. On a site whose subject is
provenance, a tier count typed by a person is the first number that goes wrong — an
entry moves from STATED to TRACED, which is the most interesting event this site
records, and three pages quietly keep saying seven. validate.js recomputes the same
counts from the same file and fails the release if a page disagrees.

Adding a page: add it to NAV or FOOTER if it belongs there, write the file with any
nav/footer block at all, then run this. The block contents are replaced; the `here`
state is set from the page's own path.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import ROOT, VERSION, tallies                      # noqa: E402

GH = "https://github.com/SGit-AI/SGit-AI__Website__Influences"
PARENT = "https://sgit.ai"
PARENT_TITLE = ("sgit.ai — the parent project: the vault layer, the shipped CLI and the "
                "network this site belongs to")
STAGE = "the provenance layer"

# The nav, two levels. Each entry is (label, own page, [(sub-label, href), ...], (path prefixes)).
#
# Two rules the structure has to keep:
#   · A group label is always a link to a real page, never a menu-only stub. Nothing on
#     this site should be reachable only by opening a dropdown.
#   · `prefixes` decides the "here" state, so a page that is not itself in the nav —
#     one of the twenty-five generated entries, say — still lights up the group it
#     belongs to.
NAV = [
    ("The register", "register/index.html", [
        ("All the entries", "register/index.html"),
        ("Bret Victor — entry one", "register/bret-victor/index.html"),
        ("The Semantic Web — argued with", "register/semantic-web/index.html"),
        ("Flow — three sources, one method", "register/flow/index.html"),
        ("Design — discovered, confirmed", "register/design/index.html"),
        ("The register format", "format/index.html"),
    ], ("register/", "format/")),
    ("The map", "map/index.html", [
        ("The influence map", "map/index.html"),
        ("The three tiers", "tiers/index.html"),
        ("The wider library", "library/index.html"),
        ("Tier movement — the changelog", "shipped/index.html"),
    ], ("map/", "tiers/", "library/", "shipped/")),
    ("For agents", "documents/index.html", [
        ("The source documents", "documents/index.html"),
        ("llms.txt", "llms.txt"),
        ("llms-full.txt", "llms-full.txt"),
    ], ("documents/", "briefs/")),
    ("How this site is built", "admin/index.html", [
        ("The pipeline, end to end", "admin/index.html"),
        ("Release history", "admin/versions.html"),
        ("Comms: the briefing queue", "admin/comms.html"),
    ], ("admin/",)),
    ("The network", "network/index.html", [
        ("The sgit.ai network", "network/index.html"),
        ("Participant disclosure", "about/participant.html"),
    ], ("network/", "about/")),
]

FOOTER = [
    ("The register", [
        ("All the entries", "register/index.html"),
        ("Bret Victor — entry one", "register/bret-victor/index.html"),
        ("The Semantic Web", "register/semantic-web/index.html"),
        ("Flow", "register/flow/index.html"),
        ("The register format", "format/index.html"),
    ]),
    ("The shape of it", [
        ("The influence map", "map/index.html"),
        ("The three tiers", "tiers/index.html"),
        ("The wider library", "library/index.html"),
        ("Tier movement", "shipped/index.html"),
    ]),
    ("For agents", [
        ("The source documents", "documents/index.html"),
        ("llms.txt", "llms.txt"),
        ("llms-full.txt", "llms-full.txt"),
    ]),
    ("This site", [
        ("How it is built", "admin/index.html"),
        ("Release history", "admin/versions.html"),
        ("Comms: the briefing queue", "admin/comms.html"),
        ("The sgit.ai network", "network/index.html"),
        ("Participant disclosure", "about/participant.html"),
    ]),
]

BLURB = ("A site in the <a href=\"https://sgit.ai\" style=\"display:inline;padding:0\"><b>sgit.ai</b></a> "
         "network: the people, works, topics and things that shaped the founder's thinking, and "
         "the places in the estate where that shaping can be checked. An influence entry here is "
         "a <b>falsifiable claim about the codebase</b>, not a reading list. "
         "The site's own words are CC BY 4.0; the anchor works belong to their authors and are "
         "linked, never rehosted.")
PARTNOTE = ('⚠ Participant disclosure: published by the sgit project, whose own work this site '
            'claims was shaped by the influences it lists. <a href="{up}about/participant.html" '
            'style="display:inline;padding:0">Read the disclosure</a>.')
PARTNOTE_SELF = '⚠ Participant disclosure: published by the sgit project. You are on the disclosure page.'
NETLINE = ('<a href="https://sgit.ai"><b>↗ sgit.ai</b></a> — the parent project · '
           '<a href="https://wardley-maps.sgit.ai">↗ wardley-maps.sgit.ai</a> · '
           '<a href="https://graphs.sgit.ai">↗ graphs.sgit.ai</a> · '
           '<a href="https://open-source.sgit.ai">↗ open-source.sgit.ai</a> · '
           '<a href="https://coding.sgit.ai">↗ coding.sgit.ai</a> · '
           '<a href="https://sgit.ai/network/index.html">↗ the network</a>')


def nav_html(rel, up):
    groups = []
    for label, own, subs, prefixes in NAV:
        active = rel == own or any(rel.startswith(pre) for pre in prefixes)
        links = "\n".join(
            f'      <a class="sl{" here" if href == rel else ""}" href="{up}{href}">{text}</a>'
            for text, href in subs)
        groups.append(
            f'    <div class="ni ni-has">\n'
            f'      <a class="nl{" here" if active else ""}" href="{up}{own}">{label}'
            f'<span class="caret">&#9662;</span></a>\n'
            f'      <div class="sub">\n{links}\n      </div>\n'
            f'    </div>')
    rows = "\n".join(groups)
    return (f'<nav class="site"><div class="row">\n'
            f'  <a class="brand" href="{up}index.html">influences<span>.sgit.ai</span></a>\n'
            f'  <a class="parent" href="{PARENT}" title="{PARENT_TITLE}">↗ part of <b>sgit.ai</b></a>\n'
            f'  <span class="stage-pill">{STAGE}</span>\n'
            f'  <a class="ver" href="{up}admin/versions.html" title="Site release history">{VERSION}</a>\n'
            f'  <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>\n'
            f'  <div class="nav-items">\n{rows}\n  </div>\n'
            f'  <a class="gh" href="{GH}">★ GitHub</a>\n'
            f'  <script src="{up}assets/nav.js" defer></script>\n'
            f'</div></nav>')


def footer_html(rel, up):
    partnote = PARTNOTE_SELF if rel == "about/participant.html" else PARTNOTE.format(up=up)
    md_twin = f' · <a href="{up}index.md">this page as markdown</a>' if rel == "index.html" else ""
    cols = "\n".join(
        "  <div>\n"
        f"    <h4>{head}</h4>\n"
        + "\n".join(f'    <a href="{l if l.startswith("http") else up + l}">{t}</a>' for t, l in links)
        + "\n  </div>"
        for head, links in FOOTER)
    return (f'<footer class="site"><div class="cols">\n'
            f'  <div>\n'
            f'    <div class="brandline">influences<span>.sgit.ai</span></div>\n'
            f'    <p>{BLURB}</p>\n'
            f'    <p class="netline">{NETLINE}</p>\n'
            f'    <p class="partnote">{partnote}</p>\n'
            f'    <p class="verline">site <a href="{up}admin/versions.html">{VERSION}</a> · '
            f'<a href="{up}admin/index.html">engineering</a>{md_twin}</p>\n'
            f'  </div>\n{cols}\n</div></footer>')


def stamp_text_twins():
    """The version also appears in llms.txt, llms-full.txt and index.md, and validate.js
    enforces that it agrees. Nothing sets it there unless something does it here."""
    out = []
    for name, pattern, repl in [
        ("llms.txt",      r"Site version: v\d+\.\d+\.\d+", f"Site version: {VERSION}"),
        ("llms-full.txt", r"Site version: v\d+\.\d+\.\d+", f"Site version: {VERSION}"),
        ("index.md",      r"· site v\d+\.\d+\.\d+ ·",      f"· site {VERSION} ·"),
    ]:
        p = ROOT / name
        if not p.exists():
            continue
        t = p.read_text()
        t2, n = re.subn(pattern, repl, t, count=1)
        if n and t2 != t:
            p.write_text(t2)
            out.append(name)
    return out


def main():
    counts = tallies()
    changed = []
    missing_k = set()
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        up = "../" * (len(path.relative_to(ROOT).parts) - 1)
        text = path.read_text()
        before = text
        text, n_nav = re.subn(r'<nav class="site">.*?</nav>', lambda _: nav_html(rel, up),
                              text, count=1, flags=re.S)
        text, n_foot = re.subn(r'<footer class="site">.*?</footer>', lambda _: footer_html(rel, up),
                               text, count=1, flags=re.S)

        def fill(m):
            k = m.group(1)
            if k not in counts:
                missing_k.add(f"{rel}: data-k=\"{k}\"")
                return m.group(0)
            return f'<span class="tally" data-k="{k}">{counts[k]}</span>'
        text = re.sub(r'<span class="tally" data-k="([^"]+)">[^<]*</span>', fill, text)

        if not n_nav or not n_foot:
            print(f"  ! {rel}: missing {'nav' if not n_nav else ''}"
                  f"{' and ' if not n_nav and not n_foot else ''}"
                  f"{'footer' if not n_foot else ''} block", file=sys.stderr)
        if text != before:
            path.write_text(text)
            changed.append(rel)
    changed += stamp_text_twins()
    for m in sorted(missing_k):
        print(f"  ! {m} is not a computed count", file=sys.stderr)
    tally_note = (f", tallies from {counts['total']} influences" if counts["total"]
                  else ", no register data yet")
    print(f"chrome: {VERSION} applied{tally_note} — {len(changed)} file(s) updated")
    for c in changed:
        print(f"  · {c}")
    if missing_k:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stdout = None

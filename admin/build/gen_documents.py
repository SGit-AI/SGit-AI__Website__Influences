#!/usr/bin/env python3
"""Generates /documents/ — the reader page for each source document — from data/documents.json.

    python3 admin/build/gen_documents.py            # write the pages
    python3 admin/build/gen_documents.py --check    # fail if any page has drifted (CI)

The raw markdown under briefs/ is the source of truth. These pages are presentation:
each one renders its document in-page from the raw file via assets/mdreader.js, and if
that fails for any reason the page falls back to a link to the raw markdown, so a
document is never unreachable.

Adding a document is two steps and no HTML: drop the markdown in briefs/, add a row to
data/documents.json, re-run this. An empty document list is a legitimate state — this
site's first release shipped the pipeline before the register — and the index says so
rather than rendering an empty table.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import (ROOT, page_head, page_tail, write_or_check,   # noqa: E402
                     report, esc)

DATA = (json.loads((ROOT / "data/documents.json").read_text())
        if (ROOT / "data/documents.json").exists()
        else {"attribution": "Dinis Cruz, with AI co-authorship (Claude, Anthropic)",
              "documents": []})
DOCS = DATA["documents"]
PAGES = [d for d in DOCS if d.get("page")]

KIND_LABEL = {
    "brief":   ("commission", "The document this site was commissioned by"),
    "source":  ("source", "A source document, captured verbatim"),
    "licence": ("licence", "The licence and boundary rules this site publishes under"),
    "data":    ("data", "Machine-readable"),
}

MARKED = ('\n<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>'
          '\n<script src="../assets/mdreader.js" defer></script>')


def reader_page(d, prev_d, next_d):
    rel = f'documents/{d["page"]}'
    tag, tagline = KIND_LABEL[d["kind"]]

    nav_prev = (f'<a href="{prev_d["page"]}">← {esc(prev_d["title"])}</a>' if prev_d
                else '<a href="index.html">← All documents</a>')
    nav_next = (f'<a href="{next_d["page"]}">{esc(next_d["title"])} →</a>' if next_d
                else '<a href="index.html">All documents →</a>')

    body = f'''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / <a href="index.html">documents</a> / {esc(d["title"])}</div>
<h1>{esc(d["title"])}</h1>
<p class="lead">{esc(d["blurb"])}</p>
<div class="docmeta">
  <div class="k">Kind</div><div class="v">{tagline}</div>
  <div class="k">Length</div><div class="v">{d["words"]:,} words</div>
  <div class="k">Raw source</div><div class="v"><a href="../briefs/{d["file"]}"><code>briefs/{d["file"]}</code></a> — the source of truth; this page is presentation</div>
  <div class="k">Licence</div><div class="v">CC BY 4.0 — {esc(DATA["attribution"])}</div>
  <div class="k">Verbatim</div><div class="v">Yes — unchanged from the source pack</div>
</div>

<div class="mdread-label">
  <span>{tag}</span> · <span>briefs/{d["file"]}</span> ·
  <a href="../briefs/{d["file"]}">open the raw markdown</a>
</div>
<div class="mdread" id="mdread" data-src="../briefs/{d["file"]}"></div>

<div class="pagenav">
  {nav_prev}
  {nav_next}
</div>
</main>
'''
    return rel, (page_head(
        rel,
        f'{d["title"]} — the source documents · influences.sgit.ai',
        esc(d["blurb"]),
        extra_head=MARKED,
    ) + body + page_tail())


def index_page():
    rel = "documents/index.html"
    total = sum(d["words"] for d in DOCS)

    if not DOCS:
        listing = '''
<div class="warnbox">
  <p><b>No source documents are published yet.</b> This release is the pipeline, not the
  register: validation, auto-tagging and deployment are live and proven, and the commissioning
  pack this site will be written from has not been unpacked into the tree. When it is, it
  arrives here in full — raw markdown in <code>briefs/</code>, one reader page each, generated
  from <code>data/documents.json</code>.</p>
  <p>That is the order on purpose. A site whose release gate works can publish anything
  safely; a site full of pages with no gate cannot.</p>
</div>'''
    else:
        cards = "\n".join(
            f'''  <a class="card" href="{d["page"]}">
    <div class="tag">{KIND_LABEL[d["kind"]][0]} · {d["words"]:,} words</div>
    <h3>{esc(d["title"])}</h3>
    <p>{esc(d["blurb"])}</p>
    <span class="go">Read it →</span>
  </a>''' for d in PAGES)
        rows = "\n".join(
            f'        <tr><td>{("<a href=" + chr(34) + d["page"] + chr(34) + ">" + esc(d["title"]) + "</a>") if d.get("page") else esc(d["title"])}</td>'
            f'<td><a href="../briefs/{d["file"]}"><code>{d["file"]}</code></a></td>'
            f'<td style="text-align:right">{d["words"]:,}</td></tr>'
            for d in DOCS)
        listing = f'''
<h2 id="read">Read them</h2>
<div class="cards" style="padding:0">
{cards}
</div>

<h2 id="all">All {len(DOCS)}, with their raw files</h2>
<div class="tablewrap">
  <table>
    <thead><tr><th>Document</th><th>Raw file</th><th style="text-align:right">Words</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
</div>'''

    lead = (
        "This site is written from a commissioning pack, and the pack is published in full — "
        f"{len(DOCS)} documents, {total:,} words — because a site that argues from a document "
        "should let you read the document."
        if DOCS else
        "This site will be written from a commissioning pack, and the pack will be published "
        "in full, because a site that argues from a document should let you read the document. "
        "It has not landed in the tree yet."
    )

    tail = f'''<h2 id="verbatim">Nothing here is redacted — and what that costs</h2>
<p>The commissioning pack is published exactly as it arrived. It carries no credentials, no
hostnames and no do-not-publish list, so unlike two of the sibling sites there was nothing to
remove. <a href="../admin/index.html#leak">The leak tripwire</a> still scans every file in the
tree on every release, because the check that only runs when you expect a problem is the check
that is not running when you have one.</p>
<p>What the pack <em>does</em> carry is a set of judgements about a living person's
intellectual formation, several of them explicitly flagged as hypotheses. Publishing it whole
means publishing those flags too, which is the point:
<a href="../tiers/index.html">the tier system</a> exists so a reader can tell a traced claim
from a guess without having to take the site's word for it.</p>

<h2 id="licence">Licence, and the split that matters here</h2>
<p>Every document in the pack, and every page of this site, is released under <b>CC BY 4.0</b>.
Attribution: {esc(DATA["attribution"])}.</p>
<p><b>The anchor works are not.</b> Bret Victor's talks, Simon Wardley's book, Kevin Kelly's
books, Rush's music, David Rice's keynote, Csikszentmihalyi's <i>Flow</i>,
<i>A Pattern Language</i>, <i>The Cathedral and the Bazaar</i> — every work this site says
shaped the thinking belongs to its author, and is linked rather than rehosted.
<a href="../format/index.html#no-verbatim">The no-verbatim rule</a> is what lets the CC BY
stamp on this site's own text stay honest, and
<a href="../admin/index.html#no-verbatim">the release gate enforces it</a> rather than the
site merely stating it.</p>
''' if DOCS else f'''<h2 id="licence">Licence, and the split that matters here</h2>
<p>Every page of this site is released under <b>CC BY 4.0</b>. Attribution:
{esc(DATA["attribution"])}. <b>The anchor works are not</b>: every work this site will say
shaped the thinking belongs to its author, and is linked rather than rehosted.
<a href="../admin/index.html#no-verbatim">The release gate enforces that</a> rather than the
site merely stating it — which is why the gate shipped before any of the entries did.</p>
'''

    body = f'''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / documents</div>
<h1>The source documents</h1>
<p class="lead">{lead}</p>

<div class="note">
  <p><b>The raw markdown is the source of truth.</b> Each reader page renders its document
  from the raw file in <code>briefs/</code> at load time; if that fails, the page falls back
  to a link to the raw file. Nothing is transcribed by hand, so a reader page cannot say
  something the document does not.</p>
  <p>Every file is fetchable at a stable constructed URL: <code>/briefs/&lt;filename&gt;</code>.
  That is a promise, not an accident.</p>
</div>
{listing}

{tail}
<div class="pagenav">
  <a href="../index.html">← Front page</a>
  <a href="../admin/index.html">How this site is built →</a>
</div>
</main>
'''
    return rel, (page_head(
        rel,
        "The source documents · influences.sgit.ai",
        "The commissioning pack this site is written from, published in full. Raw markdown "
        "is the source of truth; the reader pages are generated from it.",
    ) + body + page_tail())


def main():
    check = "--check" in sys.argv
    changed, mismatched = [], []
    rel, html = index_page()
    write_or_check(ROOT / rel, html, check, changed, mismatched)
    for i, d in enumerate(PAGES):
        rel, html = reader_page(d, PAGES[i - 1] if i else None,
                                PAGES[i + 1] if i + 1 < len(PAGES) else None)
        write_or_check(ROOT / rel, html, check, changed, mismatched)
    report("gen_documents", check, changed, mismatched)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generates /register/ — every influence entry, its markdown twin and its trace data.

    python3 admin/build/gen_register.py            # write the pages
    python3 admin/build/gen_register.py --check    # fail if anything has drifted (CI)

`data/influences.json` is the register. This script is the only thing that turns it
into pages, and it emits three artefacts per entry:

    register/<slug>/index.html        the entry, in the seven-block register format
    register/<slug>/index.md          the markdown twin of the same entry
    register/<slug>/trace/index.html  the trace table on its own, plus
    register/<slug>/trace/trace.md    ...its markdown twin, and
    register/<slug>/trace/trace.json  ...the same rows as data, so /map/ can be computed

The twins are not a second copy: every sentence of prose is authored once in the JSON
in a tiny markdown (links, bold, italic, code) and rendered twice. A site whose subject
is provenance cannot afford a hand-maintained duplicate of its own claims.

Not every entry earns all seven blocks. 01__ of the pack defines three reduced forms
and this generator implements exactly those:

    status "full"      the seven blocks
    status "link-out"  blocks 1-3 plus a pointer where the trace table would be, because
                       the trace of that influence is an entire sibling site and
                       duplicating it would break the deconfliction rule
    status "stub"      blocks 1 and 3 as best current knowledge, an explicit
                       awaiting-briefing marker and the published research plan

A stub is published, not hidden. The roadmap is content.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import (ROOT, HOST, page_head, page_tail, write_or_check,   # noqa: E402
                     write_plain, report, esc, md_inline, register_data, tallies)

DATA = register_data()
INF = DATA["influences"]
BY_SLUG = {i["slug"]: i for i in INF}

TIER_NOTE = {
    "traced":     "corpus evidence exists today",
    "stated":     "on Dinis Cruz's list, thin or absent in the corpus, awaiting his briefing document",
    "discovered": "surfaced by mining the corpus, not on Dinis Cruz's list — a falsifiable claim until he confirms it",
}
STATUS_NOTE = {
    "full":     "the seven-block register format",
    "link-out": "blocks 1-3 and a pointer: the trace of this influence is an entire sibling site",
    "stub":     "blocks 1 and 3, plus the research plan — awaiting Dinis Cruz's briefing document",
}
ROW_STATE = {
    "implemented": ("rs-yes", "implemented"),
    "partial":     ("rs-part", "partial"),
    "absent":      ("rs-no", "absent"),
}


# ---------------------------------------------------------------- small pieces
def badges(i, up=""):
    out = [f'<a class="tierb tb-{i["tier"]}" href="{up}tiers/index.html#{i["tier"]}" '
           f'title="{TIER_NOTE[i["tier"]]}">{i["tier"]}</a>',
           f'<span class="kindb">{esc(i["kind"])}</span>',
           f'<a class="statusb" href="{up}format/index.html#reduced" '
           f'title="{STATUS_NOTE[i["status"]]}">{esc(i["status"])}</a>']
    if i.get("discovered") and i["tier"] != "discovered":
        out.insert(1, '<span class="kindb kb-disc" title="Surfaced by corpus mining rather than '
                      'named by Dinis Cruz, and since promoted">discovered → traced</span>')
    return '<div class="badges">' + " ".join(out) + "</div>"


def anchor_line(a):
    bits = [f'<b>{md_inline(a["title"])}</b>']
    if a.get("author"):
        bits.append(md_inline(a["author"]))
    venue = " · ".join(x for x in [a.get("venue"), str(a["year"]) if a.get("year") else None] if x)
    if venue:
        bits.append(esc(venue))
    return " — ".join(bits)


def anchor_md(a):
    bits = [a["title"]]
    if a.get("author"):
        bits.append(a["author"])
    venue = " · ".join(x for x in [a.get("venue"), str(a["year"]) if a.get("year") else None] if x)
    if venue:
        bits.append(venue)
    return " — ".join(bits)


def paras(seq):
    return "\n".join(f"<p>{md_inline(p)}</p>" for p in seq)


def quotes_html(i):
    out = []
    for q in i.get("founder_words", []):
        src = f'<footer>— Dinis Cruz, <code>{esc(q["source"])}</code></footer>'
        out.append(f'<blockquote data-quote="founder">{md_inline(q["quote"])}\n{src}</blockquote>')
        if q.get("note"):
            out.append(f'<p class="qnote">{md_inline(q["note"])}</p>')
    return "\n".join(out)


def quotes_md(i):
    out = []
    for q in i.get("founder_words", []):
        out.append(f'> {q["quote"]}\n>\n> — Dinis Cruz, `{q["source"]}`')
        if q.get("note"):
            out.append(q["note"])
    return "\n\n".join(out)


# ---------------------------------------------------------------- block 4
def trace_rows_html(i, up):
    rows = "\n".join(
        f'      <tr><td>{md_inline(r["pattern"])}</td>'
        f'<td>{md_inline(r["where"])}</td>'
        f'<td><code>{esc(r.get("version") or "—")}</code></td>'
        f'<td class="verdict"><span class="rowstate {ROW_STATE[r["status"]][0]}">'
        f'{ROW_STATE[r["status"]][1]}</span></td></tr>'
        for r in i["trace"]["rows"])
    unversioned = sum(1 for r in i["trace"]["rows"] if not r.get("version"))
    warn = ""
    if unversioned:
        verb = "row carries" if unversioned == 1 else "rows carry"
        warn = (f'<p class="small dim"><b>{unversioned} of {len(i["trace"]["rows"])} {verb} no '
                f'version.</b> The format\'s own rule is that a trace table without versions is an '
                f'opinion — these rows name a file the corpus scan reached but not the release it '
                f'was read at. <a href="{up}format/index.html#generate-or-date">The generate-or-date '
                f'rule</a>.</p>')
    return f'''<div class="tablewrap">
  <table class="trace">
    <thead><tr><th>Pattern from the anchor</th><th>Where the estate implements it</th><th>Version</th><th>Status</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
</div>
{warn}
<p class="small"><a href="trace/index.html">This table on its own, with its sources →</a> ·
<a href="trace/trace.json">as JSON</a> · <a href="trace/trace.md">as markdown</a></p>'''


def trace_rows_md(i):
    head = ("| Pattern from the anchor | Where the estate implements it | Version | Status |\n"
            "|---|---|---|---|\n")
    body = "\n".join(
        f'| {r["pattern"]} | {r["where"]} | {r.get("version") or "—"} | {r["status"]} |'
        for r in i["trace"]["rows"])
    return head + body


def block_trace(i, up):
    t = i.get("trace", {"state": "pending", "note": ""})
    if t["state"] == "rows":
        return trace_rows_html(i, up) + (f'\n<p>{md_inline(t["note"])}</p>' if t.get("note") else "")
    if t["state"] == "sibling":
        return (f'<div class="pointer">\n'
                f'  <div class="pk">where the trace table would be</div>\n'
                f'  <p>{md_inline(t["note"])}</p>\n'
                f'  <a class="cfgget" href="{esc(t["sibling_url"])}">↗ {esc(t["sibling"])}</a>\n'
                f'</div>')
    return (f'<div class="warnbox"><p><b>No trace table yet.</b> {md_inline(t["note"])}</p></div>')


def block_trace_md(i):
    t = i.get("trace", {"state": "pending", "note": ""})
    if t["state"] == "rows":
        return trace_rows_md(i) + (f'\n\n{t["note"]}' if t.get("note") else "")
    if t["state"] == "sibling":
        return f'**Where the trace table would be:** {t["note"]}\n\n{t["sibling"]} — {t["sibling_url"]}'
    return f'**No trace table yet.** {t["note"]}'


# ---------------------------------------------------------------- the entry page
def entry_page(i, prev_i, next_i):
    rel = f'register/{i["slug"]}/index.html'
    up = "../../"
    n_of = INF.index(i) + 1
    n_total = len(INF)
    blocks = []

    blocks.append(f'''<h2 id="anchor"><span class="bn">Block 1</span> The anchor</h2>
<p class="anchorline">{anchor_line(i["anchor"])}</p>
{anchor_links(i["anchor"])}
{(f'<p class="small dim">{md_inline(i["anchor"]["note"])}</p>' if i["anchor"].get("note") else "")}''')

    if i.get("founder_words") or i.get("resonance"):
        blocks.append(f'''<h2 id="words"><span class="bn">Block 2</span> In his own words</h2>
{first_person_note(i)}
{quotes_html(i)}
{paras(i.get("resonance", []))}''')

    blocks.append(f'''<h2 id="principle"><span class="bn">Block 3</span> The principle</h2>
<div class="principle"><p>{md_inline(i["principle"])}</p></div>
{(f'<p>{md_inline(i["principle_note"])}</p>' if i.get("principle_note") else "")}''')

    if i["status"] != "stub":
        blocks.append(f'''<h2 id="trace"><span class="bn">Block 4</span> The trace table</h2>
{block_trace(i, up)}''')

    if i.get("gaps"):
        gaps = "\n".join(
            f'<div class="qbox" id="gap-{esc(g["id"].lower())}">\n'
            f'  <div class="qid">{esc(g["id"])} · build spec</div>\n'
            f'  <h3>{md_inline(g["title"])}</h3>\n'
            f'  <p>{md_inline(g["spec"])}</p>\n</div>'
            for g in i["gaps"])
        blocks.append(f'''<h2 id="gaps"><span class="bn">Block 5</span> The gaps, as build specs</h2>
<p>Patterns from the anchor the estate does not implement yet, written precisely enough that an
agent could pick one up as a work item. This is what makes an influence page forward-looking: it
is provenance and backlog in the same document.</p>
{gaps}''')

    if i.get("checklist"):
        items = "\n".join(f'  <li>{md_inline(c)}</li>' for c in i["checklist"])
        blocks.append(f'''<h2 id="checklist"><span class="bn">Block 6</span> The checklist</h2>
<p>What to ask of new work in this influence's light. The checklist is the influence made
operational — the part an agent can run without having consumed the anchor work.</p>
<ul class="checklist">
{items}
</ul>''')

    if i.get("wider_library"):
        items = "\n".join(f"  <li>{library_item(w)}</li>" for w in i["wider_library"])
        blocks.append(f'''<h2 id="library"><span class="bn">Block 7</span> The wider library</h2>
<p>The rest of the work, linked and never rehosted, each item with one line on what it adds.
The full union of every entry's Block 7 is at <a href="{up}library/index.html">/library/</a>.</p>
<ul class="library">
{items}
</ul>''')

    if i["status"] == "stub":
        blocks.append(f'''<h2 id="awaiting">Awaiting the briefing document</h2>
<div class="warnbox">
  <p><b>This entry is a stub, and says so.</b> {md_inline(i.get("stub_note", ""))}</p>
</div>
<h3 id="research">The research plan</h3>
<p>{md_inline(i["research_plan"])}</p>
{(f'<p class="small">Tracked as <a href="{up}admin/comms.html#{esc(i["comms"].lower())}">{esc(i["comms"])}</a> in the briefing queue.</p>' if i.get("comms") else "")}''')

    blocks.append(evidence_block(i, up))
    blocks.append(relations_block(i, up))

    nav_prev = (f'<a href="../{prev_i["slug"]}/index.html">← {esc(prev_i["title"])}</a>' if prev_i
                else f'<a href="{up}register/index.html">← All the entries</a>')
    nav_next = (f'<a href="../{next_i["slug"]}/index.html">{esc(next_i["title"])} →</a>' if next_i
                else f'<a href="{up}register/index.html">All the entries →</a>')

    body = f'''
<main class="doc">
<div class="crumb"><a href="{up}index.html">influences.sgit.ai</a> / <a href="{up}register/index.html">register</a> / {esc(i["title"])}</div>
<h1>{esc(i["title"])}</h1>
{badges(i, up)}
<p class="byline">An influence on <a href="{up}about/index.html"><b>Dinis Cruz</b></a> — entry {n_of} of <span class="tally" data-k="total">{n_total}</span> in <a href="{up}register/index.html">his register</a>.</p>
<p class="lead">{md_inline(i["blurb"])}</p>

{"".join(chr(10) + b + chr(10) for b in blocks)}
<div class="pagenav">
  {nav_prev}
  {nav_next}
</div>
</main>
'''
    return rel, (page_head(
        rel,
        f'{i["title"]} · the register · influences.sgit.ai',
        strip(i["blurb"]),
        og_title=f'{i["title"]} — {i["tier"].upper()} · influences.sgit.ai',
    ) + body + page_tail())



# A trace page sits one directory deeper than the entry it belongs to
# (register/<slug>/trace/ against register/<slug>/), and the register's prose is
# authored once, at entry depth. Rendering that prose on the deeper page without
# adjusting it produces links that resolve one level too high — which the release
# gate catches, loudly, and which is a tax on authoring rather than a bug worth
# living with. So the depth is a transform rather than a thing to remember:
# relative links in row prose get one more `../` when they are rendered here.
# Absolute, mailto and same-page links are left alone.
_REL_HREF = re.compile(r'(href=")(?!https?:|mailto:|data:|#|/)')
_REL_MD = re.compile(r'(\]\()(?!https?:|mailto:|#|/)')


def deepen_html(s):
    return _REL_HREF.sub(r'\1../', s)


def deepen_md(s):
    return _REL_MD.sub(r'\1../', s)


def library_item(w):
    """One Block-7 row: title, one line on what it adds, and a link out. Never a rehost —
    /library/ is the union of these across every entry and it is a list of addresses."""
    out = f'<b>{md_inline(w["title"])}</b>'
    if w.get("note"):
        out += " — " + md_inline(w["note"])
    if w.get("url"):
        out += f' <a href="{esc(w["url"])}" title="the work, where its author put it">↗</a>'
    return out


def anchor_links(a):
    links = []
    if a.get("url"):
        links.append(f'<a class="cfgget" href="{esc(a["url"])}">↗ the anchor work</a>')
    for label, key in [("transcript", "transcript"), ("mirror", "mirror"), ("publisher", "publisher")]:
        if a.get(key):
            links.append(f'<a class="cfgget" href="{esc(a[key])}">↗ {label}</a>')
    if not links:
        return ('<p class="small dim">No canonical URL. Not every anchor has one address — a '
                'book, a practice or a personal era does not — and this site links what is '
                'linkable rather than inventing a canonical home for something that has none. '
                'The wider library below carries what can be linked.</p>')
    return '<p class="anchorlinks">' + " ".join(links) + ("</p>\n<p class=\"small dim\">Linked, "
            "never rehosted. This site explains why the work resonated and traces where it was "
            "applied; the work itself stays where its author put it.</p>")


def first_person_note(i):
    if i.get("founder_words"):
        return ('<p class="small dim">First person is the house style on this site and nowhere else '
                'in the network — <i>what resonates with me and why</i> is the genre, and '
                'paraphrasing it into corporate third person would destroy the evidence. Until the '
                'briefing document for this entry arrives, this block carries the first-person '
                'statements that already exist in the corpus, cited by file.</p>')
    return ('<p class="small dim">No first-person statement about this influence exists in the '
            'corpus yet. What follows is the site\'s reading of the evidence, not Dinis Cruz\'s '
            'words — and it stays labelled as such until his briefing document arrives.</p>')


def evidence_block(i, up):
    ev = i.get("corpus_evidence", [])
    if not ev:
        return ('<h2 id="evidence">The corpus evidence</h2>\n'
                '<div class="warnbox"><p><b>None.</b> This influence is on Dinis Cruz\'s own list '
                'and the corpus scan found nothing to attach to it. That is the definition of the '
                f'<a href="{up}tiers/index.html#stated">STATED tier</a>, and it is published rather '
                'than hidden: an empty evidence block is the most honest thing this page can '
                'show.</p></div>')
    rows = "\n".join(
        f'      <tr><td><code>{esc(e["path"])}</code></td><td>{md_inline(e["note"])}</td></tr>'
        for e in ev)
    return f'''<h2 id="evidence">The corpus evidence</h2>
<p>What the mining run found, by path. These are the files that put this entry in its tier — the
claim on this page is checkable against them, which is the whole point of the format.</p>
<div class="tablewrap">
  <table>
    <thead><tr><th>Path in the corpus</th><th>What it carries</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
</div>
<p class="small dim">Paths are as recorded by the mining run behind the commissioning pack
(v0.33.62, 25 August 2026). This repository holds the website, not the corpus, so they are cited
rather than resolved — <a href="{up}admin/comms.html#r2">R2 in the comms queue</a>.</p>'''


def relations_block(i, up):
    bits = []
    if i.get("nests_under"):
        p = BY_SLUG.get(i["nests_under"])
        if p:
            bits.append(f'<li>Nests under <a href="../{p["slug"]}/index.html">{esc(p["title"])}</a>'
                        f'{(" — " + md_inline(i["nests_under_note"])) if i.get("nests_under_note") else ""}</li>')
    for s in i.get("nests", []):
        c = BY_SLUG.get(s)
        if c:
            bits.append(f'<li>Nested here: <a href="../{c["slug"]}/index.html">{esc(c["title"])}</a></li>')
    for s in i.get("composes_with", []):
        c = BY_SLUG.get(s)
        if c:
            bits.append(f'<li>Composes with <a href="../{c["slug"]}/index.html">{esc(c["title"])}</a>'
                        f' — influences are a graph, not a ranking</li>')
    if i.get("sibling_site"):
        s = i["sibling_site"]
        bits.append(f'<li>Sibling site: <a href="{esc(s["url"])}">{esc(s["host"])}</a> — '
                    f'{md_inline(s["owns"])}</li>')
    if not bits:
        return (f'<h2 id="relations">Where this sits</h2>\n<p>No nesting and no sibling site: this '
                f'entry stands on its own. <a href="{up}map/index.html">The influence map</a> draws '
                f'every relation the register records.</p>')
    return (f'<h2 id="relations">Where this sits</h2>\n<ul class="relations">\n'
            + "\n".join(bits)
            + f'\n</ul>\n<p class="small"><a href="{up}map/index.html">The whole graph →</a></p>')


def strip(s):
    return (s.replace("**", "").replace("*", "").replace("`", "")
             .replace("[", "").replace("]", "").replace('"', "&quot;"))


# ---------------------------------------------------------------- markdown twin
def entry_md(i):
    L = [f'# {i["title"]}', ""]
    L += [f'*Source: <https://{HOST}/register/{i["slug"]}/index.html> · '
          f'markdown twin of the entry page.*', ""]
    L += [f'*An influence on **Dinis Cruz** — one of {len(INF)} entries in his register.*', "",
          f'- **tier** {i["tier"]} — {TIER_NOTE[i["tier"]]}',
          f'- **kind** {i["kind"]}',
          f'- **status** {i["status"]} — {STATUS_NOTE[i["status"]]}',
          f'- **briefing** {i.get("briefing_status", "none")}']
    if i.get("founder_confirmed"):
        L.append(f'- **founder-confirmed** {i["founder_confirmed"]}')
    L += ["", i["blurb"], "", "## Block 1 — The anchor", "", anchor_md(i["anchor"])]
    for k, label in [("url", "anchor"), ("transcript", "transcript"),
                     ("mirror", "mirror"), ("publisher", "publisher")]:
        if i["anchor"].get(k):
            L.append(f'- {label}: <{i["anchor"][k]}>')
    if i["anchor"].get("note"):
        L += ["", i["anchor"]["note"]]
    L += ["", "*Linked, never rehosted.*"]

    if i.get("founder_words") or i.get("resonance"):
        L += ["", "## Block 2 — In his own words", ""]
        if quotes_md(i):
            L += [quotes_md(i), ""]
        L += ["\n\n".join(i.get("resonance", []))]

    L += ["", "## Block 3 — The principle", "", f'**{i["principle"]}**']
    if i.get("principle_note"):
        L += ["", i["principle_note"]]

    if i["status"] != "stub":
        L += ["", "## Block 4 — The trace table", "", block_trace_md(i)]

    if i.get("gaps"):
        L += ["", "## Block 5 — The gaps, as build specs", ""]
        for g in i["gaps"]:
            L += [f'### {g["id"]} — {g["title"]}', "", g["spec"], ""]

    if i.get("checklist"):
        L += ["", "## Block 6 — The checklist", ""]
        L += [f'- {c}' for c in i["checklist"]]

    if i.get("wider_library"):
        L += ["", "## Block 7 — The wider library", ""]
        for w in i["wider_library"]:
            note = f' — {w["note"]}' if w.get("note") else ""
            url = f' <{w["url"]}>' if w.get("url") else ""
            L.append(f'- **{w["title"]}**{note}{url}')

    if i["status"] == "stub":
        L += ["", "## Awaiting the briefing document", "", i.get("stub_note", ""),
              "", "**Research plan.** " + i["research_plan"]]

    L += ["", "## The corpus evidence", ""]
    if i.get("corpus_evidence"):
        L += ["| Path in the corpus | What it carries |", "|---|---|"]
        L += [f'| `{e["path"]}` | {e["note"]} |' for e in i["corpus_evidence"]]
    else:
        L += ["None. This influence is on Dinis Cruz's own list and the corpus scan found "
              "nothing to attach to it — which is the definition of the STATED tier."]

    L += ["", "---", "",
          "CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic). The anchor work "
          "belongs to its author and is linked, not licensed here."]
    return "\n".join(L).rstrip() + "\n"


# ---------------------------------------------------------------- the trace page
def trace_page(i):
    rel = f'register/{i["slug"]}/trace/index.html'
    up = "../../../"
    rows = "\n".join(
        f'      <tr><td>{deepen_html(md_inline(r["pattern"]))}</td>'
        f'<td>{deepen_html(md_inline(r["where"]))}</td>'
        f'<td><code>{esc(r.get("version") or "—")}</code></td>'
        f'<td class="verdict"><span class="rowstate {ROW_STATE[r["status"]][0]}">'
        f'{ROW_STATE[r["status"]][1]}</span></td>'
        f'<td class="small dim">{deepen_html(md_inline(r.get("source", "—")))}</td></tr>'
        for r in i["trace"]["rows"])
    body = f'''
<main class="doc">
<div class="crumb"><a href="{up}index.html">influences.sgit.ai</a> / <a href="{up}register/index.html">register</a> / <a href="../index.html">{esc(i["title"])}</a> / trace</div>
<h1>{esc(i["title"])} — the trace table</h1>
<p class="lead">The falsifiable part of the entry, on its own and with its sources attached. Each
row is a claim that a pattern from the anchor work appears at a named place in the estate —
checkable against the repositories, which is the only thing that separates this from a reading
list.</p>

<div class="tablewrap">
  <table class="trace">
    <thead><tr><th>Pattern from the anchor</th><th>Where the estate implements it</th><th>Version</th><th>Status</th><th>Source of the row</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
</div>

<div class="note">
  <p><b>Every row names where it came from.</b> A trace row is only worth having if you can find
  out how it was arrived at, so the last column carries the document in the commissioning pack
  that supports it. No row on this site was written from memory or inference — where the evidence
  runs out, the row is marked <b>absent</b> or the table says so.</p>
</div>

<h2 id="data">The same rows, as data</h2>
<p>The <a href="{up}map/index.html">influence map</a> is computed from these files rather than
drawn, so the graph cannot disagree with the tables it is made of.</p>
<p class="anchorlinks">
  <a class="cfgget" href="trace.json">trace.json</a>
  <a class="cfgget" href="trace.md">trace.md</a>
  <a class="cfgget" href="../index.html">the full entry</a>
</p>

<div class="pagenav">
  <a href="../index.html">← {esc(i["title"])}</a>
  <a href="{up}map/index.html">The influence map →</a>
</div>
</main>
'''
    return rel, (page_head(
        rel,
        f'{i["title"]} — the trace table · influences.sgit.ai',
        f'Where the estate implements the patterns of {strip(i["title"])}, row by row, with '
        f'versions and sources. The falsifiable part of the influence claim.',
    ) + body + page_tail())


def trace_md(i):
    return (f'# {i["title"]} — the trace table\n\n'
            f'*Source: <https://{HOST}/register/{i["slug"]}/trace/index.html>*\n\n'
            + deepen_md(trace_rows_md(i)) + "\n\n"
            + "Row sources:\n\n"
            + deepen_md("\n".join(f'- {r["pattern"]} — {r.get("source", "—")}'
                                  for r in i["trace"]["rows"]))
            + "\n\nCC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic).\n")


def trace_json(i):
    return json.dumps({
        "slug": i["slug"],
        "title": i["title"],
        "tier": i["tier"],
        "principle": i["principle"],
        "anchor": i["anchor"],
        "rows": i["trace"]["rows"],
        "licence": "CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic)",
    }, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------- the index
def index_page():
    rel = "register/index.html"
    if not INF:
        body = '''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / register</div>
<h1>The register</h1>
<p class="lead">Not written yet.</p>
<div class="warnbox">
  <p><b>This release is the pipeline, not the register.</b> Validation, auto-tagging and
  deployment are live and proven; the entries have not been written. When they are, each arrives
  as <code>/register/&lt;slug&gt;/</code> with a markdown twin beside it, generated from
  <code>data/influences.json</code>.</p>
</div>
<div class="pagenav">
  <a href="../index.html">← Front page</a>
  <a href="../admin/index.html">How this site is built →</a>
</div>
</main>
'''
        return rel, page_head(rel, "The register · influences.sgit.ai",
                              "Every influence entry. Not written yet — this release is the "
                              "pipeline.") + body + page_tail()

    t = tallies(INF)
    groups = []
    for tier, heading, blurb in [
        ("traced", "TRACED", "Corpus evidence exists today. The claim on the page can be checked "
                             "against the files listed on it."),
        ("stated", "STATED", "On Dinis Cruz's own list, and thin or absent in the corpus. "
                             "Published as commitments with the research plan visible — the "
                             "roadmap, not the debt."),
        ("discovered", "DISCOVERED", "Surfaced by mining the corpus, never named by Dinis Cruz. "
                                     "The claim rests entirely on the trace table until he "
                                     "confirms or corrects it."),
    ]:
        members = [i for i in INF if i["tier"] == tier]
        cards = "\n".join(
            f'''  <a class="card" href="{i["slug"]}/index.html">
    <div class="tag">{esc(i["kind"])} · {esc(i["status"])}</div>
    <h3>{esc(i["title"])}</h3>
    <p>{md_inline(i["blurb"])}</p>
    <span class="go">The entry →</span>
  </a>''' for i in members)
        groups.append(f'''<h2 id="{tier}">{heading} — <span class="tally" data-k="{tier}">{t[tier]}</span></h2>
<p>{blurb} <a href="../tiers/index.html#{tier}">The definition →</a></p>
<div class="cards" style="padding:0">
{cards}
</div>''')

    body = f'''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / register</div>
<h1>The register</h1>
<p class="lead">Every influence, in three tiers by how well the claim is evidenced.
<span class="tally" data-k="total">{t["total"]}</span> entries:
<span class="tally" data-k="traced">{t["traced"]}</span> traced,
<span class="tally" data-k="stated">{t["stated"]}</span> stated,
<span class="tally" data-k="discovered">{t["discovered"]}</span> discovered and still awaiting
Dinis Cruz's confirmation. The counts are computed from
<a href="../data/influences.json"><code>data/influences.json</code></a> on every build, not typed
— because tier movement is the one event this site exists to record.</p>

<div class="note">
  <p><b>An entry is a falsifiable claim, not an appreciation.</b> Anyone can say Bret Victor was
  an influence. The register says <i>which</i> of Victor's patterns appear <i>where</i> in the
  estate, at <i>which</i> version, and which are still missing — specified precisely enough to
  build. <a href="../format/index.html">The format, in full →</a></p>
</div>

{"".join(chr(10) + g + chr(10) for g in groups)}
<div class="pagenav">
  <a href="../index.html">← Front page</a>
  <a href="../map/index.html">The influence map →</a>
</div>
</main>
'''
    return rel, (page_head(
        rel, "The register — every influence entry · influences.sgit.ai",
        f'All {t["total"]} influence entries in three tiers: {t["traced"]} traced, '
        f'{t["stated"]} stated, {t["discovered"]} discovered. Each entry is a falsifiable claim '
        f'about the codebase.',
    ) + body + page_tail())


# ---------------------------------------------------------------- the library
def library_page():
    """/library/ — the union of every entry's Block 7, one section per entry.

    04__ §3 of the pack settles the licensing question this page raises: listing facts
    about a work — title, year, one line, a link — is uncopyrightable metadata and is
    safe. Cover images and stills are not, which is why there are none."""
    rel = "library/index.html"
    have = [i for i in INF if i.get("wider_library")]
    items = sum(len(i["wider_library"]) for i in have)
    linked = sum(1 for i in have for w in i["wider_library"] if w.get("url"))
    secs = []
    for i in have:
        rows = "\n".join(f"  <li>{library_item(w)}</li>" for w in i["wider_library"])
        secs.append(f'''<h3 id="lib-{esc(i["slug"])}"><a href="../register/{esc(i["slug"])}/index.html">{esc(i["title"])}</a>
<span class="tierb tb-{i["tier"]}">{i["tier"]}</span></h3>
<ul class="library">
{rows}
</ul>''')
    body = f'''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / library</div>
<h1>The wider library</h1>
<p class="lead">Every entry's Block 7 in one place: {items} works across {len(have)} entries,
{linked} of them with a link out. This is a list of <b>addresses</b>, not a collection —
nothing here is hosted, mirrored or excerpted, and that is a rule rather than an oversight.</p>

<div class="note">
  <p><b>Why a list of other people's books is safe and a shelf of them is not.</b> Listing
  facts about a work — its title, its year, one line on what it adds, where to find it — is
  uncopyrightable metadata. The works themselves are not. So this page carries no cover
  images, no excerpts and no stills: the moment it did, this site would be redistributing
  material it does not own under a licence it has no right to grant.
  <a href="../format/index.html#no-verbatim">The rule, in full →</a></p>
</div>

<p>Each entry's own Block 7 is the authoritative version; this page is the union, generated
from the same register on every build. An anchor work is <em>not</em> repeated here — it is
at the top of its entry, in Block 1.</p>

{"".join(chr(10) + s + chr(10) for s in secs)}
<div class="pagenav">
  <a href="../register/index.html">← The register</a>
  <a href="../format/index.html">The register format →</a>
</div>
</main>
'''
    return rel, (page_head(
        rel, "The wider library · influences.sgit.ai",
        f"Every influence entry's wider library in one place: {items} works, linked and never "
        f"rehosted. A list of addresses, not a collection.",
    ) + body + page_tail())


def main():
    check = "--check" in sys.argv
    changed, mismatched = [], []
    rel, html = index_page()
    write_or_check(ROOT / rel, html, check, changed, mismatched)
    if INF:
        rel, html = library_page()
        write_or_check(ROOT / rel, html, check, changed, mismatched)
    for n, i in enumerate(INF):
        rel, html = entry_page(i, INF[n - 1] if n else None,
                               INF[n + 1] if n + 1 < len(INF) else None)
        write_or_check(ROOT / rel, html, check, changed, mismatched)
        write_plain(ROOT / f'register/{i["slug"]}/index.md', entry_md(i),
                    check, changed, mismatched)
        if i.get("trace", {}).get("state") == "rows":
            rel, html = trace_page(i)
            write_or_check(ROOT / rel, html, check, changed, mismatched)
            write_plain(ROOT / f'register/{i["slug"]}/trace/trace.md', trace_md(i),
                        check, changed, mismatched)
            write_plain(ROOT / f'register/{i["slug"]}/trace/trace.json', trace_json(i),
                        check, changed, mismatched)
    report("gen_register", check, changed, mismatched)


if __name__ == "__main__":
    main()

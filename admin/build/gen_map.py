#!/usr/bin/env python3
"""Generates /map/ — the influence graph, computed from the register rather than drawn.

    python3 admin/build/gen_map.py            # write the page and the data
    python3 admin/build/gen_map.py --check    # fail if either has drifted (CI)

Two artefacts:

    map/index.html   the lineage diagram, the influence → principle → estate projection,
                     and the edge list, all assembled from data/influences.json
    map/graph.json   the same graph as nodes and edges, so something else can consume it

The point of generating it is the point of the whole site. 03__ of the pack says trace
tables are per-entry data "so /map/ can be generated, not drawn", and a hand-drawn graph
of a register that changes is a picture that is wrong by the second release. Every node
and every edge below exists because a field in the register says so:

    influence --shapes-->        its principle          (every entry has one)
    principle --lands in-->      an estate feature      (from the trace rows)
    influence --nests under-->   another influence      (nests / nests_under)
    influence --composes with--> another influence      (composes_with)
    influence --leads to-->      another influence      (lineage, recorded per entry)

The diagram is mermaid, rendered in the browser. If the module cannot load, the fence
stays visible as text and every edge it would have drawn is also listed underneath —
the page never becomes a blank rectangle where a graph was supposed to be.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import (ROOT, page_head, page_tail, write_or_check,     # noqa: E402
                     write_plain, report, esc, md_inline, register_data, tallies)

DATA = register_data()
INF = DATA["influences"]
BY_SLUG = {i["slug"]: i for i in INF}

MERMAID = ('\n<script type="module">'
           '\nimport mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";'
           '\nmermaid.initialize({startOnLoad:true,theme:"neutral",'
           'themeVariables:{fontFamily:"ui-sans-serif, system-ui, sans-serif",fontSize:"13px"}});'
           '\n</script>')


def edges():
    """Every influence → influence edge the register records, with its kind and the field
    it came from. Nothing here is authored on this page."""
    out = []
    for i in INF:
        for s in i.get("nests", []):
            if s in BY_SLUG:
                out.append((s, i["slug"], "nests under", "nests"))
        if i.get("nests_under") in BY_SLUG:
            out.append((i["slug"], i["nests_under"], "nests under", "nests_under"))
        for s in i.get("composes_with", []):
            if s in BY_SLUG:
                out.append((i["slug"], s, "composes with", "composes_with"))
        for e in i.get("lineage", []):
            if e["to"] in BY_SLUG:
                out.append((i["slug"], e["to"], e.get("label", "leads to"), "lineage"))
    # nests and nests_under are two spellings of one edge; keep one of each pair
    seen, uniq = set(), []
    for a, b, lab, field in out:
        key = (a, b, lab)
        if key in seen:
            continue
        seen.add(key)
        uniq.append((a, b, lab, field))
    return uniq


def label(s):
    """Mermaid renders node text as HTML, so an ampersand or a quotation mark in a title
    is a rendering bug waiting for the one entry that has one. Four of these titles carry
    an ampersand and one carries curly quotes, so the labels are sanitised rather than
    trusted — the diagram is a projection of the register, and a projection is allowed to
    spell a title differently from the page it points at."""
    return (s.replace("&", "and").replace('"', "").replace("\u201c", "")
             .replace("\u201d", "").replace("|", "/"))


def connected():
    """The slugs that appear in at least one recorded relation, in register order."""
    seen = {s for a, b, _, _ in edges() for s in (a, b)}
    return [i for i in INF if i["slug"] in seen]


def isolated():
    """And the ones that do not. Drawing them as a column of unattached boxes made the
    diagram four times taller while saying nothing, so they are named under it instead —
    an entry with no recorded relation is a fact about the register, not a thing to hide,
    and several are isolated only because the briefing that would connect them has not
    arrived."""
    seen = {s for a, b, _, _ in edges() for s in (a, b)}
    return [i for i in INF if i["slug"] not in seen]


def mermaid_src():
    lines = ["graph LR"]
    # `---|text|` rather than `<-->` for the symmetric relation: the bidirectional arrow
    # is a newer flowchart form and this diagram loads mermaid from a CDN at a pinned
    # major, so the older spelling is the one that cannot surprise us on an upgrade.
    arrow = {"nests under": "-.->", "composes with": "---"}
    for i in connected():
        cls = i["tier"]
        lines.append(f'  {i["slug"].replace("-", "_")}["{label(i["title"])}"]:::{cls}')
    for a, b, lab, _ in edges():
        lines.append(f'  {a.replace("-", "_")} {arrow.get(lab, "-->")}|{label(lab)}| '
                     f'{b.replace("-", "_")}')
    lines += [
        "  classDef traced fill:#e7f3f1,stroke:#0f766e,color:#10302c;",
        "  classDef stated fill:#fdf3e3,stroke:#b45309,color:#3b2708;",
        "  classDef discovered fill:#eef1fb,stroke:#3b4c9e,color:#1c2445;",
    ]
    return "\n".join(lines)


def graph_json():
    nodes = [{"id": i["slug"], "label": i["title"], "tier": i["tier"], "kind": i["kind"],
              "status": i["status"], "principle": i["principle"],
              "url": f'/register/{i["slug"]}/index.html'} for i in INF]
    links = [{"from": a, "to": b, "label": lab, "recorded_in": field}
             for a, b, lab, field in edges()]
    lands = []
    for i in INF:
        for r in i.get("trace", {}).get("rows", []):
            if r["status"] != "absent":
                lands.append({"influence": i["slug"], "principle": i["principle"],
                              "pattern": r["pattern"], "estate": r["where"],
                              "version": r.get("version"), "status": r["status"]})
    return json.dumps({
        "schema": "influences-map/v1",
        "generated_by": "admin/build/gen_map.py from data/influences.json",
        "note": "Every node and every edge is a field in the register. Nothing here is drawn.",
        "nodes": nodes, "edges": links, "lands_in_estate": lands,
        "licence": "CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic)",
    }, indent=2, ensure_ascii=False) + "\n"


def projection_rows():
    out = []
    for i in INF:
        rows = [r for r in i.get("trace", {}).get("rows", []) if r["status"] != "absent"]
        if not rows:
            continue
        out.append((i, rows))
    return out


def index_page():
    rel = "map/index.html"
    if not INF:
        body = '''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / map</div>
<h1>The influence map</h1>
<p class="lead">Not computed yet — there is no register to compute it from.</p>
<div class="warnbox">
  <p><b>This release is the pipeline, not the register.</b> When the entries land, this page is
  generated from them: every node and every edge a field in
  <code>data/influences.json</code>, never a drawing.</p>
</div>
<div class="pagenav">
  <a href="../index.html">← Front page</a>
  <a href="../admin/index.html">How this site is built →</a>
</div>
</main>
'''
        return rel, page_head(rel, "The influence map · influences.sgit.ai",
                              "The influence graph, computed from the register. Not written "
                              "yet.") + body + page_tail()

    t = tallies(INF)
    E = edges()
    edge_rows = "\n".join(
        f'      <tr><td><a href="../register/{a}/index.html">{esc(BY_SLUG[a]["title"])}</a></td>'
        f'<td class="dim">{esc(lab)}</td>'
        f'<td><a href="../register/{b}/index.html">{esc(BY_SLUG[b]["title"])}</a></td>'
        f'<td class="small dim"><code>{esc(field)}</code></td></tr>'
        for a, b, lab, field in E)

    proj = []
    for i, rows in projection_rows():
        cells = "\n".join(
            f'        <tr><td>{md_inline(r["pattern"])}</td><td>{md_inline(r["where"])}</td>'
            f'<td><code>{esc(r.get("version") or "—")}</code></td></tr>' for r in rows)
        proj.append(f'''<h3 id="lands-{esc(i["slug"])}"><a href="../register/{esc(i["slug"])}/index.html">{esc(i["title"])}</a></h3>
<p class="principle-inline">{md_inline(i["principle"])}</p>
<div class="tablewrap">
  <table>
    <thead><tr><th>Pattern</th><th>Where it lands in the estate</th><th>Version</th></tr></thead>
    <tbody>
{cells}
    </tbody>
  </table>
</div>''')

    landed = sum(len(r) for _, r in projection_rows())
    iso = isolated()
    iso_links = " ".join(
        f'<a class="cfgget" href="../register/{esc(i["slug"])}/index.html">{esc(i["title"])}</a>'
        for i in iso)

    body = f'''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / map</div>
<h1>The influence map</h1>
<p class="lead">The register as a graph: <span class="tally" data-k="total">{t["total"]}</span>
influences, {len(E)} recorded relations between them, and {landed} places where a pattern from an
anchor work lands in the estate. <b>Computed, not drawn</b> — every node and every edge on this
page is a field in <a href="../data/influences.json"><code>data/influences.json</code></a>, so
the graph cannot disagree with the entries it is made of.</p>

<div class="note">
  <p><b>This is the site's own G³ demonstration in miniature.</b> The influences that produced
  the estate's graph thinking — Luhmann's slip-box, the Semantic Web's edges, Bush's associative
  trails — are here as nodes in a graph, which is either a satisfying loop or a slightly
  circular one, and the honest answer is that it is both. The
  <a href="../admin/comms.html#q7">open question</a> is whether this page eventually belongs on
  the graphs sibling instead.</p>
</div>

<h2 id="lineage">The lineage</h2>
<p>Influences are not independent, and the interesting structure is between them: what nests
under what, what composes with what, and which idea led to which. Colour is tier —
<span class="tierb tb-traced">traced</span>, <span class="tierb tb-stated">stated</span>,
<span class="tierb tb-discovered">discovered</span>.</p>
<pre class="mermaid">
{mermaid_src()}
</pre>
<p class="small dim">The diagram renders in your browser from the fence above. If the module does
not load, the fence stays readable as text and every edge it draws is also listed in the table
below — a picture that can fail should never be the only copy of the thing.</p>

<h3 id="isolated">The {len(iso)} entries with no recorded relation</h3>
<p>They are not in the diagram, because a column of unattached boxes made it four times taller
while saying nothing. <b>Standing alone is a fact about the register rather than about the
influence</b>: an edge is only drawn where a field in the register records one, and several of
these are unconnected simply because the briefing document that would connect them has not
arrived. Where a lineage is plausible but undocumented — Kevin Kelly's technium and Wardley's
evolution axis are the obvious pair — <b>the edge is deliberately not drawn</b>, because guessing
one here would be the same failure as inventing a trace row.</p>
<p class="anchorlinks">{iso_links}</p>

<h2 id="edges">Every recorded relation</h2>
<div class="tablewrap">
  <table>
    <thead><tr><th>From</th><th>Relation</th><th>To</th><th>Recorded in</th></tr></thead>
    <tbody>
{edge_rows}
    </tbody>
  </table>
</div>

<h2 id="lands">Influence → principle → estate</h2>
<p>The other projection, and the one that makes an entry falsifiable: each influence distilled to
one transferable principle, and every place a pattern from its anchor work is claimed to land in
the estate. Rows marked <b>absent</b> on the entry pages are not here — this is what is built,
not what is specified. The gaps are on the entries.</p>
{"".join(chr(10) + p + chr(10) for p in proj)}
<h2 id="data">The graph, as data</h2>
<p><a href="graph.json"><code>/map/graph.json</code></a> carries the same nodes, edges and
landing rows in one file, regenerated on every release. Each entry's own rows are also published
per-entry at <code>/register/&lt;slug&gt;/trace/trace.json</code>.</p>

<div class="pagenav">
  <a href="../register/index.html">← The register</a>
  <a href="../tiers/index.html">The three tiers →</a>
</div>
</main>
'''
    return rel, (page_head(
        rel, "The influence map · influences.sgit.ai",
        f'The register as a graph: {t["total"]} influences, {len(E)} recorded relations, and '
        f'{landed} places a pattern lands in the estate. Computed from the register, not drawn.',
        extra_head=MERMAID,
    ) + body + page_tail())


def main():
    check = "--check" in sys.argv
    changed, mismatched = [], []
    rel, html = index_page()
    write_or_check(ROOT / rel, html, check, changed, mismatched)
    if INF:
        write_plain(ROOT / "map/graph.json", graph_json(), check, changed, mismatched)
    report("gen_map", check, changed, mismatched)


if __name__ == "__main__":
    main()

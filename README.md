# influences.sgit.ai — where the thinking came from

The [sgit.ai](https://sgit.ai) network's provenance layer: the people, works, topics and things
that shaped Dinis Cruz's thinking, each written as a **falsifiable claim about the codebase**
rather than an appreciation.

Live site: https://influences.sgit.ai (GitHub Pages, deployed from `dev`).

## The move

Anyone can say Bret Victor was an influence. An entry in this register says **which** of Victor's
patterns appear **where** in the estate, at **which** version — and which are still **absent**,
specified precisely enough that an agent could pick one up as a work item. That is what separates
the register from every "books that shaped me" listicle, and it is the reason the site exists.

The format was not designed for the site. Dinis Cruz wrote an *immediate-connection register*
for Victor's *Inventing on Principle* as a working document, and then asked what a site made of
such documents should be called. The format is **proven in use**.

## Structure

- `index.html` / `index.md` — the front page and its markdown twin
- `register/<slug>/` — one influence entry, in the seven-block register format, with a markdown
  twin beside it. Slugs are people or topics, never works: an anchor work is metadata inside the
  entry, because a briefing document may reveal the real anchor was a different talk.
  **Generated** from `data/influences.json`
- `register/<slug>/trace/` — the trace table on its own, as a page, as markdown and as JSON
- `map/` — the influence graph: influences, the relations between them, and where each
  principle lands in the estate. **Computed** from the register, never drawn
- `tiers/`, `format/`, `library/`, `shipped/` — the tier definitions, the register format
  documented, the union of every entry's wider library, and the tier-movement changelog
- `documents/` — reader pages for the source documents, **generated** from `data/documents.json`
- `briefs/` — those source documents, verbatim
- `network/`, `about/`, `admin/` — boundaries, disclosure, and how this site is built
- `assets/site.css` — the shared stylesheet (sgit.ai design language)

## Build tooling

| File | Owns |
|---|---|
| `admin/build/version.txt` | The version — single source of truth |
| `data/influences.json` | **The register.** Every entry, tier, anchor, principle and trace row |
| `admin/build/chrome.py` | The nav, the footer, the version badge and the tier tallies, rewritten across every page |
| `admin/build/pagelib.py` | The shared page shell, the write-or-check writer, and the tiny markdown the register's prose is authored in |
| `admin/build/gen_register.py` | `register/` — every entry, its markdown twin and its trace data |
| `admin/build/gen_map.py` | `map/` and `map/graph.json` |
| `admin/build/gen_documents.py` | `documents/` from `data/documents.json` and `briefs/` |
| `admin/build/gen_llms_full.py` | `llms-full.txt` from `llms.txt`, `index.md`, the entry twins and `briefs/` |
| `admin/build/gen_sitemap.py` | `sitemap.xml` from the tree |
| `admin/build/validate.js` | The release gate |

Python 3 and Node, both stdlib-only. Nothing to install.

### Why the markdown twins are generated

Every entry publishes an HTML page and a markdown twin, and the twin is not a second copy. Each
sentence of prose is authored **once**, in `data/influences.json`, in a deliberately tiny
markdown — links, bold, italic, code — and rendered twice. Two renderings of one string cannot
drift. Writing the page by hand and the twin by hand is the arrangement that always does.

## The release gate

`node admin/build/validate.js` — plain Node, no dependencies. Six checks; any failure exits 1, so
no tag and no publish. Four are the house checks (version agreement, internal links and
fragments, canonical host, the credential-shape leak tripwire). **Two are this site's own
editorial rules, made executable rather than stated:**

**The no-verbatim gate.** The site explains why a work resonated and traces where it was applied;
it does not reproduce the work. Every `<blockquote>` declares whose words it carries;
`data-quote="founder"` is unrestricted, and a third party's words are capped at **40** — a
sentence or two, quoted to be examined. The gate cannot see an unmarked quotation woven into a
paragraph; what it can do is stop the failure mode that actually ships, which is a long passage
pasted in whole because it was useful. **The fix for a tripped gate is to cut the quotation,
never to raise the cap.**

**The register is the data.** Every influence in `data/influences.json` has a page, every page
under `register/` is in the data, and every tier count written into a page is recomputed from the
register and must agree. `chrome.py` fills the numbers in; `validate.js` recomputes them
independently from the same file. Tier movement — STATED → TRACED when a briefing lands,
DISCOVERED → TRACED when Dinis Cruz confirms — is this site's changelog, and a hand-typed count
is exactly what makes that change invisible.

## Release process

1. Bump `admin/build/version.txt` (vX.Y.Z, exactly once per release) and add a row to
   `admin/versions.html`; update `admin/comms.html` if anything changed.
2. Regenerate the pages that come from data:
   ```
   python3 admin/build/gen_register.py && python3 admin/build/gen_map.py \
     && python3 admin/build/gen_documents.py
   ```
3. `python3 admin/build/chrome.py` — **after** the generators. It propagates the version badge,
   the nav, the footer and the tier tallies into the pages they have just produced, and stamps
   the version into `llms.txt` and `index.md`.
4. Regenerate the files that read the tree and those stamped twins — **after** chrome, or they
   assemble a stale version line: `python3 admin/build/gen_llms_full.py` and `gen_sitemap.py`.
5. Validate exactly what CI runs:
   ```
   python3 admin/build/gen_register.py  --check
   python3 admin/build/gen_documents.py --check
   python3 admin/build/gen_map.py       --check
   python3 admin/build/gen_llms_full.py --check
   python3 admin/build/gen_sitemap.py   --check
   node admin/build/validate.js
   ```
6. `git commit -am "site vX.Y.Z: ..." && git push -u origin dev`

Every push to `dev` runs `.github/workflows/deploy-pages.yml`: validate → auto-tag (`vX.Y.Z`,
verified against `version.txt` and the commit subject, next-minor enforced, historical tags
backfilled) → deploy to GitHub Pages. Pull requests run validation only. A push to `main`
validates and deploys without tagging. Same pipeline as
[SGit-AI__Website](https://github.com/SGit-AI/SGit-AI__Website),
[SGit-AI__Website__Graphs](https://github.com/SGit-AI/SGit-AI__Website__Graphs) and
[SGit-AI__Website__Coding](https://github.com/SGit-AI/SGit-AI__Website__Coding).

## One inherited trap, pre-empted

The Python `.gitignore` this repository starts from carries `build/`, which silently swallows
`admin/build/` — a sibling site shipped a first release whose validate job died on a missing file
before it could check anything. The checks appeared to run and did not. The `!admin/build/`
negation is in this repository's first commit.

## Licence

All site content **CC BY 4.0** — Dinis Cruz, with AI co-authorship (Claude, Anthropic).

**The anchor works are not.** Bret Victor's talks, Simon Wardley's book, Kevin Kelly's books,
Rush's music, David Rice's keynote, Csikszentmihalyi's *Flow*, *A Pattern Language*, *The
Cathedral and the Bazaar* — every work this site says shaped the thinking belongs to its author,
and is linked rather than rehosted. On a site about attribution, that distinction is the point.

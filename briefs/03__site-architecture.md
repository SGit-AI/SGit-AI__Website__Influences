# 03 — Site Architecture: `influences.sgit.ai`

**Version** v0.33.62 · 25 August 2026
**Base** The house pattern (copy `pki.sgit.ai`): `llms.txt` + `/llms-full.txt`, `/documents/` raw markdown, markdown twin at every URL, `/admin/comms.html` with N1…/T1… threads, `/shipped/`, versioned everything, participant page.

---

## 1. URL scheme

```
/                          the thesis + the three-tier map (counts generated)
/register/<slug>/          one influence entry (full format, 7 blocks)
/register/<slug>/trace/    the trace table alone, as data (md + json twins)
/tiers/                    TRACED / STATED / DISCOVERED, with definitions
/map/                      the influence graph (influences → principles → estate features)
/format/                   the register format itself, documented (from 01__)
/library/                  the union of all Block-7 wider libraries, one page per person/topic
/documents/                raw markdown of everything
/admin/comms.html          questions to the founder (see §4)
```

Slugs are people or topics, not works: `/register/bret-victor/`, `/register/wardley/`, `/register/semantic-web/`, `/register/flow/`, `/register/luhmann/`, `/register/neil-peart/`… The anchor work is metadata inside the entry, because anchors can be superseded (a briefing document may reveal the *real* anchor was a different talk).

## 2. Data model

`influences__seed.json` (this pack) is the initial vault content. Each record: `slug`, `tier`, `kind`, `status`, `anchor`, `principle`, `corpus-evidence[]` (path + note, regenerable), `sibling-site`, `nests-under`, `briefing-status`, `research-plan`. The site is a projection of this data — same architecture as standards.sgit.ai: the register lives in a vault, the site renders it. Trace tables are per-entry JSON so `/map/` can be generated, not drawn.

**Generated, not claimed**: tier counts, corpus-evidence file counts, and the `/map/` graph are all derivable from the seed JSON + a corpus scan. Publish the scan script's identity and date beside every number.

## 3. Tier movement is the site's changelog

The interesting events on this site are transitions: STATED → TRACED (a briefing document arrived and was integrated), DISCOVERED → TRACED (the founder confirmed), a trace row flipping absent → implemented (the estate built a gap). Each transition is a dated entry on `/shipped/`. A provenance site whose provenance changes silently would be self-refuting.

## 4. The comms channel has a special role here

On other sites `/admin/comms.html` carries build questions. Here it is also the **briefing-document request queue**: one thread per STATED entry (N1: Neil Peart — awaiting briefing; N2: Kevin Kelly — …), so the founder's stated plan (*"in time I will create a detailed briefing document about each one"*) has a visible, addressable inbox. When a briefing lands, the thread closes and the entry's tier moves.

## 5. Infographics

The founder asked for infographics of people and ideas. Two rules from `04__`: likenesses are **original artwork only** (never scraped photos); idea-infographics (the golden circle, the flow channel, evolution axes) are **redrawn in house style with attribution**, never copied. Every infographic's source data is a markdown/JSON twin — the house rule that a picture is a projection of data, not an original.

## 6. What this site does NOT do

No hosting of anchor works (talks, book excerpts, essays) — links only, per `04__`. No hagiography — entries carry disagreements (the Semantic Web entry is the model). No rankings — influences are a graph, not a top-ten. And no silent scope creep into siblings: if an entry's material grows past resonance-and-trace, the material moves to the sibling site and the entry keeps the pointer.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

# 01 — The Register Format: how an influence entry is written

**Version** v0.33.62 · 25 August 2026
**Purpose** Canonise the founder's Bret Victor register into the template every influence page follows.

---

## 1. Where the format comes from

The founder did not ask for this site and then invent a format for it. The format existed first: he wrote an *"immediate-connection register"* for Bret Victor's *Inventing on Principle* (2012) as a working document for the estate's viewer, and then asked what a site made of such documents should be called. That ordering matters — the register format is **proven in use**, not designed on spec. `sources/register__bret-victor__inventing-on-principle.md` carries the anchor and structure; the founder holds the full original text and it should be shipped verbatim into `/register/bret-victor/` as entry one.

What makes the register different from every "books that shaped me" listicle is one move: **it treats influence as a falsifiable claim about the codebase.** Anyone can say Victor inspired them. The register says *which* of Victor's patterns appear *where* in the estate, at *which* version — and which are still missing, specified precisely enough to build.

---

## 2. The template — seven blocks

Every full influence entry has these blocks, in this order:

### Block 1 — The anchor
The primary work, precisely cited: title, venue, date, canonical URL (and a durable mirror where one exists — e.g. the talk on Vimeo *and* the transcript on worrydream.com). One anchor per entry; the wider bibliography goes in Block 7. For a person, the anchor is the single work that did the shaping, not the whole career. For a topic or era ("graphs", "OWASP Summits"), the anchor is the founder's first documented contact with it.

### Block 2 — The founder's words
Why this resonates, in first person. This is the only site in the network where first person is the house style — *"what resonates with me and why"* is the genre, and paraphrasing it into corporate third person would destroy the evidence. Until the founder writes the briefing document for an entry, this block carries whatever first-person statements already exist in the corpus, cited by file and version.

### Block 3 — The principle
The influence distilled to one transferable sentence — the thing an agent can actually apply. Victor's is *immediate connection between creator and creation*. Wardley's is *situational awareness before strategy*. The test: the principle must be usable by someone who has never consumed the anchor work.

### Block 4 — The trace table
The heart of the format and the falsifiable part. Rows of: **pattern from the anchor → where the estate implements it → version → status (implemented / partial / absent)**. The Victor register's own closing observation is the standard to aim for: half the viewer's strongest features turned out to be *unknowing* implementations of the talk's demos — *"evidence the instinct and the principle agree; this register makes the agreement deliberate, so the next agent extends it on purpose rather than by luck."* Trace rows carry version numbers, so the generate-or-date rule applies: a trace table without versions is an opinion.

### Block 5 — The gaps, as build specs
Patterns from the anchor the estate does *not* yet implement — written precisely enough that an agent could pick one up as a work item (the Victor register specifies two: view time travel and relayout ghosts). This is what makes an influence page *forward-looking*: it is simultaneously provenance and backlog.

### Block 6 — The checklist
A short list of questions an agent should ask of new work in this influence's light ("does the user see the effect of the change immediately?", "is the map drawn before the strategy is argued?"). The checklist is the influence made operational.

### Block 7 — The wider library
The rest of the person's/topic's work, linked never rehosted, each item with one line on what it adds. This is where "other presentations by Bret Victor" live, where Rush's discography lives, where the rest of Kevin Kelly's books live.

---

## 3. Reduced forms

Not every entry earns all seven blocks on day one.

**The link-out entry** (for influences with sibling sites — Wardley, graphs, OWASP, open source): blocks 1–3 plus a *pointer* where the trace table would be: "the trace of this influence is an entire site — wardley-maps.sgit.ai". Duplicating the sibling's content would break the deconfliction rule; the influence entry owns only the *resonance*, the sibling owns the *material*.

**The stub entry** (for STATED influences awaiting the founder's briefing document): blocks 1 and 3 as best current knowledge, an explicit `status: awaiting-briefing` marker, and the research plan — which of the founder's past publications and talks should be mined when the briefing arrives. A stub is published, not hidden: the roadmap is content.

**The discovered entry**: same as full format, but Block 2 opens with honesty — the founder never listed this influence; the corpus surfaced it. The claim "this shaped the work" rests entirely on the trace table until the founder confirms or corrects it. Discovered entries are the site's falsifiability applied to itself.

---

## 4. Entry metadata

Every entry carries front-matter: `tier` (traced / stated / discovered), `kind` (person / work / topic / era / practice / community), `status` (full / link-out / stub), `anchor-url`, `corpus-evidence` (file paths + counts, generated), `sibling-site` (if any), and `briefing-status` (none / requested / received / integrated). `influences__seed.json` in this pack is the initial population of exactly this schema.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

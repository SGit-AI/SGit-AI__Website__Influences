# 02 — The Influence Map: every entry, with its evidence

**Version** v0.33.62 · 25 August 2026
**Method** The corpus (`SGraph-AI__App__Send`, `docs.diniscruz.ai`, `files.diniscruz.ai`, `Issues-FS__*`) was grep-mined for every seed term the founder listed plus every external name the mining surfaced. Counts below are from those runs; the site must regenerate them. Tier definitions: **TRACED** = corpus evidence exists today; **STATED** = on the founder's list but thin/absent in the corpus (awaiting his briefing document); **DISCOVERED** = in the corpus but not on his list (published as a falsifiable claim until he confirms).

---

## TRACED — twelve entries with corpus evidence

### T1 · Bret Victor — *Inventing on Principle* (2012)
**The model entry — the register exists** (`sources/`, and the founder holds the full text). Corpus evidence beyond the register: the Joy-of-Programming white paper (`docs.diniscruz.ai/docs/2025/07/04/the-joy-of-programming-in-the-age-of-ai-assisted-development.md`) builds its central argument on Victor — *"Bret Victor, in his influential talk 'Inventing on Principle,' argued that one key to unlocking creative flow is immediate feedback"* — and quotes the talk's core line about creators needing an immediate connection to what they create. And the education-gaps article (`team/humans/dinis_cruz/briefs/03/28/v0.19.7__article__education-gaps-git-opensource.md`) has a section *titled* **"The Brett Victor Problem"**, applying Victor's point about dogma to education: *"the problem with dogma is not that it exists, but that you stop asking the question."* One influence, applied in two unrelated domains (developer tooling and education policy) — that breadth is itself trace evidence.
**Principle**: immediate connection between creator and creation.
**Trace**: the register's own table (viewer features as unknowing implementations of the talk's demos). **Gaps as specs**: view time travel; relayout ghosts.
**Wider library** (the founder asked for other Victor presentations): *The Future of Programming* (1973 costume talk), *Media for Thinking the Unthinkable*, *Up and Down the Ladder of Abstraction*, *Stop Drawing Dead Fish*, *Drawing Dynamic Visualizations*, *The Humane Representation of Thought*, Dynamicland. Each gets one line in Block 7, linked to worrydream.com — never rehosted.

### T2 · Simon Wardley & Wardley Maps
**Corpus**: ~210 files; an entire sibling site (`wardley-maps.sgit.ai`) whose pack documents the founder's own published Wardley materials — videos, infographics, the maps-as-code work.
**Principle**: situational awareness before strategy — the map is a falsifiable claim about position and movement.
**Format**: link-out entry (blocks 1–3 + pointer). The influence page owns the *resonance* — why a security person reorganised his thinking around evolution axes; the sibling owns the material.

### T3 · Tim Berners-Lee & the Semantic Web
**The best full-format second entry, because it is an influence argued with.** Corpus: ~35 files. Two star exhibits: the Solid-integration brief (`team/humans/dinis_cruz/briefs/02/24/v0.6.17__architecture__solid-protocol-integration-complementary-architectures.md` — TBL's Solid pods vs sgit vaults as complementary architectures, with Schneier's involvement at Inrupt noted), and the *"Semantic Web's Insight (and Mistake)"* section in `library/concepts/v0_4_0__thinking-in-graphs.md`: *"The Semantic Web community identified the right problem… But the community made a subtle mistake in practice. They ended up attaching meaning to nodes rather than deriving meaning from edges."*
**Why this is the format at its strongest**: the entry can show resonance (the dream of machine-readable meaning shaped G³, MGraph-DB, the ontology work), disagreement (node-first vs edge-first), and a live architectural conversation (vaults vs pods). Influence is not agreement; it is engagement.

### T4 · Graphs
**The founding obsession.** Corpus: everywhere; its own sibling site. The entry is a link-out with one addition the sibling does not carry: the *personal* history — where graphs entered the founder's thinking (O2 Platform's code-flow graphs, a research pointer for his briefing doc).

### T5 · OWASP & the security community
**Corpus**: ~271 files, including the Summits history. Link-out to the open-source pack's OWASP material for governance/monetisation (deconfliction), but this entry owns the *community-as-influence* claim: two decades of participation, the Summit model, and the era itself ("cyber security community" is a *kind: era/community* entry, the seed list's own phrasing). David Rice's keynote (S5 below) nests under this influence's wider library.

### T6 · Flow, and coding in the zone
**Three sources converging on one methodology — the site's best demonstration that influences compose.** Corpus: ~43 files. Csikszentmihalyi is named and his flow criteria applied in the Joy-of-Programming paper (*"In his seminal work, Mihály Csíkszentmihályi identified programming as one of many activities… that can induce flow"*); Victor supplies the mechanism (immediate feedback keeps you in it); and IFD is the methodology built from both — `library/guides/development/ifd/v1.2.1__ifd__intro-and-how-to-use.md` opens: *"It centers on **preserving developer flow state** while leveraging LLMs for code generation"* and closes *"IFD is about maintaining flow state."*
**Trace**: the entire IFD guide is the trace table. The entry's diagram: Csikszentmihalyi (the state) × Victor (the mechanism) × the founder's practice (the methodology).

### T7 · Open source & its licences
**Corpus**: its own sibling site with the full history pack (11,619-word corpus + 17,909-word history on file). Link-out entry. This entry owns one thing the sibling does not foreground: open source as *personal formation* — what two decades of releasing tools (O2 Platform onward) taught the founder about licences as social contracts. *The Cathedral and the Bazaar* (S4) nests here.

### T8 · Niklas Luhmann & the Zettelkasten — **discovered, now traced**
Not on the seed list; the corpus surfaced a dedicated published article: `docs.diniscruz.ai/docs/2025/06/18/bridging-niklas-luhmanns-ideas-with-semantic-knowledge-graphs-and-g3.md` — a full mapping of the slip-box to G³ (*"Luhmann's Zettelkasten was a self-organizing knowledge graph on paper… atomic, uniquely identified, densely linked, emergent in structure, scalable and lifelong"*). The article is nearly the influence page already; it needs only the register's trace-table discipline (which G³/MGraph-DB features implement which Zettelkasten property, with versions).
**Bonus**: the article reaches back to **Vannevar Bush's memex** — the D5 entry enters through this one.

### T9 · Anders Ericsson & deliberate practice
**Corpus**: ~11 files on the 10,000-hours / deliberate-practice research (properly attributed to Ericsson, not the popularisation). Resonates with the founder's position on skill formation in the AI era. Full entry, medium depth.

### T10 · Karl Popper & falsifiability
**Corpus**: ~7 files. The deepest-running discovered thread: *"a map is a claim"* (wardley pack), the risks register's falsifiable-statements discipline, this very site's trace-table rule. Popper may be the influence that explains the *shape* of all the others' entries. Short entry, high leverage.

### T11 · Linus Torvalds
**Corpus**: ~5 files (Git's history, the education-gaps article's Git argument, kernel governance in the open-source history). Nested under T7's wider library or a short standalone — builder of *two* of the tools the estate stands on (Linux, Git).

### T12 · Bruce Schneier
**Corpus**: ~4 files (the LLM-failure-modes argument; Solid/Inrupt in the TBL brief). Short entry; security-economics thinking as influence on the founder's threat-modelling style.

---

## STATED — the founder's seven, awaiting his briefing documents

Zero or near-zero grep hits today. Published as stubs with `status: awaiting-briefing` and a research plan each. **They are the roadmap, not the debt.**

**S1 · Neil Peart & Rush.** *kind: person/music.* Research plan: the founder's talks/bios for drumming references; Peart as the craftsman-lyricist archetype — technical mastery plus meaning — an obvious resonance hypothesis to test against the briefing, not assert.
**S2 · Kevin Kelly's books.** *kind: books.* Candidate anchors to confirm: *What Technology Wants*, *The Inevitable*, *1,000 True Fans* (essay). The technium's evolutionary framing plausibly connects to Wardley evolution — flag as hypothesis.
**S3 · Simon Sinek — the golden circle.** *kind: framework.* Why→How→What. Research plan: check his conference talks for golden-circle framing; the sgit.ai site network itself is organised why-first.
**S4 · *The Cathedral and the Bazaar* (Eric S. Raymond).** *kind: work.* Nests under T7. The open-source history pack already covers the essay's factual history — this entry owns only what it *did to the founder*.
**S5 · David Rice — "Upon the Threshold of Opportunity" (OWASP keynote).** *kind: presentation.* Nests under T5. Research plan: locate the recording (OWASP AppSec archives), and the founder's contemporaneous blog reactions. Rice's *Geekonomics* is the wider-library item.
**S6 · Music, and playing in a band.** *kind: practice/era.* The most personal entry; entirely awaiting the briefing. Hypothesis to test: band-playing as the original experience of real-time collaborative flow — the thing IFD tries to recreate in software.
**S7 · Diverse and distributed teams.** *kind: practice.* Research plan: the founder's management writing, the team-roles system in the corpus, OWASP's global-chapter model as the formative experience.

---

## DISCOVERED — five the corpus surfaced beyond Luhmann

**D1 · Christopher Alexander.** `team/roles/designer/ROLE.md`: *"Christopher Alexander's pattern language is the direct ancestor of software design patterns. The Designer should think of code as a space that developers inhabit: is it navigable? Is it comfortable?"* A load-bearing citation in a live role definition — strong trace.
**D2 · Design (capital D) & Steve Jobs — discovered, founder-confirmed 2026-08-25.** The founder confirmed this the day the pack shipped: *"Design and Steve Jobs approach to Design (with capital D)."* The trace was already deep. The Designer ROLE.md is built on Jobs's formulation — *"Design is not just what it looks like and feels like. Design is how it works"* — and extends it: *"Design is the coherence between the internal structure and the external experience."* The NotebookLM case-study brief (`v0.7.4__brief__advocate-designer-in-the-loop-notebooklm-case-study.md`) has a section titled **"The Jonathan Ive Principle: Good Design Starts with the User"**, retells the Jobs MP3-to-CD whiteboard story, and lands the principle: *"Good design is invisible… the only way to notice it is to go back to the previous version and think: 'This is way worse.'"* And the strongest kind of trace this site recognises — influence turned into *process*: the **"Jonathan Ive test"** (*is it simpler? would reverting feel worse?*) is a **mandatory validator for every UI change** in the explorer-response brief. Not a quote on a wall; a gate in the pipeline. The wider canon — Rams (*"less, but better"* as a working API principle), Vignelli, Norman, Eames, Muller-Brockmann, Tschichold, Aalto, Cooper, Krug, Japanese design philosophy — nests under this entry.
**D3 · Team Topologies & Cynefin.** Listed beside Wardley in the 2019 hiring post. Short entry pending founder confirmation of depth.
**D4 · Vannevar Bush & the memex.** Enters via the Luhmann article; *As We May Think* (1945) as the ancestor of the whole external-memory thread — which is also this site network's own thesis. A satisfying loop: the memory network's provenance site tracing the idea of memory networks.
**D5 · Mihály Csíkszentmihályi.** Named in T6 but deserves his own row in the seed data: *Flow* (1990) as anchor; the founder's flow entries cite him directly.

---

## The composition view

The entries are not independent — the site's eventual `/map/` page (build-order step 7) draws the graph: Bush → Luhmann → graphs → Semantic Web → G³; Victor → flow ← Csikszentmihalyi, both → IFD; Wardley → Popper (maps as claims) → the register format itself; Raymond → open source ← Torvalds; Rice → OWASP. The influence map is itself a G³ instance — the site becomes a demonstration of the thing the influences taught.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

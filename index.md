# influences.sgit.ai — where the thinking came from

> The provenance layer of the sgit.ai memory network. The other sites teach an agent **what**
> the founder thinks and **how** the estate works; this one is for **where the thinking came
> from** — so an agent extends the instincts on purpose rather than by luck.

*Source: <https://influences.sgit.ai/index.html> · site v0.1.0 · markdown twin of the front page.*

---

## This release is the pipeline. The register comes next.

Every sibling site's early releases tell the same story: content lands, then something in the
release machinery turns out to be wrong, and the fix is a release of its own. So this repository
shipped the gate first, and publishes an almost-empty site through it — on a tree small enough to
read in one sitting.

```
# every push to dev
validate ──▶ tag-release ──▶ deploy
   │             │                │
   │             │                └─ upload-pages-artifact, deploy-pages
   │             └─ git push origin refs/tags/vX.Y.Z
   └─ gen_*.py --check ; node admin/build/validate.js

# six checks in the gate, and two of them are this site's own:
version agreement · internal links + fragments · canonical host
the no-verbatim gate     # a third party's words, capped at 40
the register is the data # tier counts recomputed, never typed
credential-shape leak tripwire
```

The two middle checks are the site's own rules, made executable rather than stated.
[Why a quotation cap is a release gate](admin/index.html#no-verbatim).

## An influence entry is a falsifiable claim

This is what separates the register from every "books that shaped me" listicle, and it is the
reason the site exists at all.

- **Not "X inspired me" — which pattern, where, at which version.** Anyone can say Bret Victor
  was an influence. The register says which of Victor's patterns appear where in the estate, at
  which release, and which are still **absent** — specified precisely enough that an agent could
  pick one up as a work item.
- **Seven blocks, proven in use before they were designed.** Anchor → the founder's words → the
  principle → **the trace table** → the gaps as build specs → a checklist → the wider library.
  The format was not invented for this site: it was written first, as a working document, and
  the site was named afterwards.
- **TRACED, STATED, DISCOVERED — and the difference is published.** Corpus evidence exists; on
  the founder's list but not yet in the corpus; or found by mining and never claimed by him at
  all. A reader can tell a traced claim from a hypothesis without taking the site's word for it.
- **Link, never rehost.** The site explains why a work resonated and traces where it was
  applied. The work itself stays where its author put it. That instinct is also the legally
  correct one — and here it is a check in the release pipeline, not a paragraph in a footer.

## What is not here yet

Stated plainly, because a site about provenance that was vague about its own state would be
self-refuting:

- **The register itself** — twenty-five entries across three tiers, from the commissioning
  pack's seed data. The empty index is live, generated from a data file that has not been
  written.
- **The influence map** — the graph of influences, principles and estate features. Computed from
  the register, so it cannot exist before the register does.
- **The source documents** — the commissioning pack, to be published in full, because a site
  that argues from a document should let you read the document.
- **The register format, documented**, the tier definitions, and the union of every entry's
  wider library.

Everything above is tracked as a numbered task at [comms](admin/comms.html), and every release
says what it shipped in [one row](admin/versions.html).

---

All site content CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic). The anchor
works belong to their authors and are linked, never rehosted.

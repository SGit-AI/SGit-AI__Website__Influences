# Design, with a capital D

*Source: <https://influences.sgit.ai/register/design/index.html> · markdown twin of the entry page.*

*An influence on **Dinis Cruz** — one of 25 entries in his register.*

- **tier** traced — corpus evidence exists today
- **kind** discipline + person
- **status** full — the seven-block register format
- **briefing** confirmed; anchor and personal history requested
- **founder-confirmed** 2026-08-25 — “Design and Steve Jobs approach to Design (with capital D).”

Discovered by mining and confirmed by Dinis Cruz the day the commissioning pack shipped — the first DISCOVERED → confirmed transition, before the site existed. The strongest trace on this site: an influence that became a mandatory step in the pipeline.

## Block 1 — The anchor

“Design is how it works” — the Jobs formulation the estate's Designer role is built on — Steve Jobs
- anchor: <https://www.nytimes.com/2003/11/30/magazine/the-guts-of-a-new-machine.html>

**Anchor unconfirmed.** The formulation is from the 2003 *New York Times Magazine* profile linked above; the candidates for what actually did the shaping are that piece, the MP3-to-CD whiteboard story, a keynote, or a specific product. Asked as [Q2b](../../admin/comms.html#q2b).

*Linked, never rehosted.*

## Block 2 — In his own words

> Design is the coherence between the internal structure and the external experience.
>
> — Dinis Cruz, `briefs/.../team/roles/designer/ROLE.md`

The estate's own extension of the Jobs formulation, and a sharper one: it says the two halves must agree, which is a testable claim about a codebase rather than a slogan about products.

> Good design is invisible… the only way to notice it is to go back to the previous version and think: “This is way worse.”
>
> — Dinis Cruz, `briefs/.../v0.7.4__brief__advocate-designer-in-the-loop-notebooklm-case-study.md`

And this is the sentence that became a test. Read it again with the next block in mind.

The reason this is the strongest-traced entry on the site is not the number of citations. It is that the influence **turned into process**. The brief's section is titled *The Jonathan Ive Principle: Good Design Starts with the User*; the observation is that you notice good design only by reverting and feeling the loss; and the estate turned that observation into the **Jonathan Ive test** — *is it simpler? would reverting feel worse?* — which is a **mandatory validator for every UI change**.

That is the difference between a quote on a wall and an influence. A gate in a pipeline is checkable, dated, and possible to fail. Most entries in this register aspire to a trace table; this one had its trace table written as a workflow before anyone asked for the register.

What is genuinely missing is the personal history. The corpus shows the influence fully operational and says nothing about when it arrived — which is why Dinis Cruz's confirmation came with a question attached rather than closing the entry.

## Block 3 — The principle

**Design is not decoration applied after engineering — it is how the thing works. Start from what the person is trying to do and work backwards to the simplest interaction that does it.**

## Block 4 — The trace table

| Pattern from the anchor | Where the estate implements it | Version | Status |
|---|---|---|---|
| Design is how it works, not how it looks | The estate's Designer role definition, which is built on the formulation and extends it to coherence between internal structure and external experience | — | implemented |
| Start from the user's intent and work backwards (the Ive principle) | The NotebookLM case-study brief, in a section named for the principle, with the MP3-to-CD story as the worked example | v0.7.4 | implemented |
| Good design is invisible — you notice it by reverting and feeling the loss | **The Jonathan Ive test**: *is it simpler? would reverting feel worse?* — a mandatory validator for every UI change | v0.7.4 | implemented |
| Simplicity as subtraction — the feature removed rather than the feature added | Implied by the Ive test's first half and not separately enforced. Nothing records what was taken out of a change | v0.7.4 | partial |
| The same discipline applied to non-visual surfaces — an API, a CLI, a file format | Nowhere. The validator is scoped to UI changes, and the estate's public surface is mostly not UI | v0.7.4 | absent |

Three rows implemented at a stated version, from three documents in the same fortnight of the corpus. That density is why Dinis Cruz's confirmation was a formality rather than a discovery.

## Block 5 — The gaps, as build specs

### G1 — The Ive test is scoped to UI, and this estate is mostly not UI

The mandatory validator applies to UI changes. Most of what a person or an agent actually touches here is an API, a CLI, a file format or a document layout — surfaces where *is it simpler? would reverting feel worse?* applies word for word and is not asked. The build spec is a one-line scope change plus the harder part: deciding what *reverting feels worse* means for a function signature, and writing that down before the first argument about it.

### G2 — Nothing records what a change removed

*Is it simpler* is asked and the answer is not kept. A change log that records only additions cannot show a trend, and simplicity is only visible as one. The spec: capture the subtraction alongside the addition in whatever records a change, and publish the ratio. It will be unflattering, which is the point — the sibling sites' house rule is that the bad numbers get published too.


## Block 6 — The checklist

- **Is it simpler than what it replaces?** Not smaller — simpler.
- **Would going back to the previous version feel worse?** If not, this change is decoration.
- What did this remove? If the answer is nothing, look again.
- Does the internal structure agree with the external experience, or is the surface hiding the shape?
- Start from what the person is trying to do: does this design fall out of that, or was it designed first and justified after?

## Block 7 — The wider library

- **The 1996 Wired interview** — a different and broader Jobs formulation — design as the fundamental soul of a made thing — and useful beside the anchor rather than instead of it <https://www.wired.com/1996/02/jobs-2/>
- **Objectified (2009)** — Ive and Rams in the same documentary — the clearest available statement of the lineage this entry nests
- **Insanely Simple — Ken Segall** — the simplicity-as-subtraction argument, from someone who was in the room

## The corpus evidence

| Path in the corpus | What it carries |
|---|---|
| `SGraph-AI__App__Send/team/roles/designer/ROLE.md` | Jobs quoted twice, and extended: *design is the coherence between the internal structure and the external experience* |
| `SGraph-AI__App__Send/team/humans/dinis_cruz/briefs/02/27/part-2/v0.7.4__brief__advocate-designer-in-the-loop-notebooklm-case-study.md` | the section *The Jonathan Ive Principle: Good Design Starts with the User*; the MP3-to-CD whiteboard story retold; *good design is invisible* |
| `SGraph-AI__App__Send/team/humans/dinis_cruz/claude-code-web/02/28/v0.7.4__explorer-response__security-and-process-briefs.md` | the **Jonathan Ive test** as a mandatory validator for every UI change — the influence as a pipeline gate |

---

CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic). The anchor work belongs to its author and is linked, not licensed here.

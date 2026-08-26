# Christopher Alexander

*Source: <https://influences.sgit.ai/register/christopher-alexander/index.html> · markdown twin of the entry page.*

- **tier** discovered — surfaced by mining the corpus, not on the founder's list — a falsifiable claim until he confirms it
- **kind** person
- **status** full — the seven-block register format
- **briefing** requested

Never named by the founder. Surfaced by mining a live role definition, where the pattern-language idea is doing real work — a load-bearing citation, not a decorative one.

## Block 1 — The anchor

A Pattern Language — Christopher Alexander, Sara Ishikawa and Murray Silverstein — 1977

The book everyone in software cites. *The Timeless Way of Building* is the argument behind it and is in Block 7.

*Linked, never rehosted.*

## Block 2 — The founder's words

> Christopher Alexander's pattern language is the direct ancestor of software design patterns. The Designer should think of code as a space that developers inhabit: is it navigable? Is it comfortable?
>
> — Dinis Cruz, `briefs/.../team/roles/designer/ROLE.md`

Not a nod in a bibliography — a **criterion in a live role definition**, telling a reviewer what to look at. That is what moved this from a citation to a discovered influence.

The move worth noticing is that the role definition does not use Alexander the way software usually does. The Gang of Four took the *pattern* idea and left the rest; this citation takes the part the Gang of Four dropped — **that a building is judged by what it is like to be in it** — and applies it to a codebase. *Is it navigable? Is it comfortable?* are not questions about correctness. They are questions about habitation.

That reading is closer to what Alexander actually argued, and to his later disappointment with what software did with his work. It is also, honestly, the reading that is hardest to check: comfort is not a property a test can assert.

**This entry is DISCOVERED and stays that way until the founder confirms it.** The claim that Alexander shaped the thinking rests entirely on one citation being load-bearing rather than ornamental. That is a real argument and it is not proof — [Q2](../../admin/comms.html#q2).

## Block 3 — The principle

**Code is a space that people inhabit. A pattern is a named solution to a recurring problem in a context — and a language of patterns is what lets a place be built by many hands and still be coherent.**

## Block 4 — The trace table

| Pattern from the anchor | Where the estate implements it | Version | Status |
|---|---|---|---|
| Code as a space developers inhabit — judge it by navigability and comfort | The Designer role definition's review criteria | — | implemented |
| A *language* of patterns — named solutions that compose, each referring to the ones above and below it | Nowhere. The estate has conventions and a house style; it has no pattern language, and the two are not the same thing | — | absent |
| Patterns discovered from use rather than designed in advance | Nowhere recorded. The estate's conventions were derived by counting the code on [the coding sibling](https://coding.sgit.ai), which is the same method — but it was not done in Alexander's name and the connection is this site's inference | — | absent |

One implemented row and two absent ones, which is the honest shape of a discovered entry: the citation is real, and almost none of what the anchor work actually asks for has been built.

## Block 5 — The gaps, as build specs

### G1 — There is no pattern language, only patterns

Alexander's actual contribution is the *language*: each pattern names the larger patterns it completes and the smaller ones that complete it, so that a builder can move between scales. The estate's conventions are a flat list. The build spec is not to write more conventions but to link the existing ones into a structure — each convention naming what it serves and what serves it. The material already exists on [coding.sgit.ai](https://coding.sgit.ai); the edges do not.

### G2 — Nobody has asked whether the code is comfortable

The role definition sets *is it navigable? is it comfortable?* as review criteria and nothing collects an answer. The cheap version is not a survey: time-to-locate for a symbol a newcomer has never seen, measured once. It would produce an uncomfortable number and it would be the first evidence either way.


## Block 6 — The checklist

- Is this a space someone can find their way around, or one they need a guide for?
- Does this pattern name what it completes, and what completes it — or is it a loose item on a list?
- Was this pattern found in use, or invented at a whiteboard?
- What is it *like* to be in this part of the codebase? If nobody has asked, that is the finding.

## Block 7 — The wider library

- **A Pattern Language (1977)** — the anchor; 253 patterns, and the structure between them is the point
- **The Timeless Way of Building (1979)** — the argument the patterns were derived from, and the better book
- **Notes on the Synthesis of Form (1964)** — the early, formal work — and the one Alexander later partly repudiated
- **Patterns of Software — Richard Gabriel (1996)** — the most serious attempt to say what software actually took from Alexander, and what it dropped <https://www.dreamsongs.com/Files/PatternsOfSoftware.pdf>

## The corpus evidence

| Path in the corpus | What it carries |
|---|---|
| `SGraph-AI__App__Send/team/roles/designer/ROLE.md` | the pattern-language lineage stated, and code-as-inhabited-space set as a review criterion |

---

CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic). The anchor work belongs to its author and is linked, not licensed here.

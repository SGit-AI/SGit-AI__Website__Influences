# The wider design canon

*Source: <https://influences.sgit.ai/register/design-canon/index.html> · markdown twin of the entry page.*

*An influence on **Dinis Cruz** — one of 25 entries in his register.*

- **tier** traced — corpus evidence exists today
- **kind** canon
- **status** full — the seven-block register format
- **briefing** confirmed via the Design entry

Rams, Vignelli, Norman, Eames, Müller-Brockmann, Tschichold, Aalto, Cooper, Krug, and Japanese design philosophy — mapped onto software explicitly in a live role definition, not cited as decoration.

## Block 1 — The anchor

The industrial, graphic and interaction design tradition, as mapped onto software in the estate's Designer role

A canon rather than a work. The anchor is the mapping itself — the moment the tradition was written down as engineering guidance rather than as taste.

*Linked, never rehosted.*

## Block 2 — In his own words

What makes this an entry rather than a bibliography is the direction the mapping runs. The role definition does not say *good designers admire Rams*; it takes **less, but better** and treats it as a working principle for an API surface. That is the tradition being used as a tool, which is the test this register applies throughout.

The most transferable pieces: Rams on subtraction; Norman on affordance — a thing should tell you what it does by its shape, which is a claim about function signatures as much as door handles; Krug on not making the reader think, which is a claim about documentation; Müller-Brockmann on the grid, which is a claim about consistent structure making irregularity visible.

Nested under [Design](../design/index.html) because it is the same influence at a different resolution: that entry has the principle and the pipeline gate, this one has the vocabulary.

## Block 3 — The principle

**Every element must earn its place. Hierarchy, affordance and proportion are properties of any designed thing — an API and a CLI included, not only a screen.**

## Block 4 — The trace table

| Pattern from the anchor | Where the estate implements it | Version | Status |
|---|---|---|---|
| *Less, but better* (Rams) as a working principle rather than an aesthetic | The Designer role definition, applied to API surface rather than to visual design | — | implemented |
| Code as inhabited space — is it navigable, is it comfortable | The same role definition's criteria for reviewing structure | — | implemented |
| Affordance (Norman) applied to non-visual surfaces — a signature that tells you what it does | Not written down anywhere as a review criterion, though the estate's naming conventions arguably practise it | — | absent |

Two rows, both from one document, and that is the honest extent of it. A canon leaves a thinner trace than a single work does, because it supplies vocabulary rather than patterns.

## Block 6 — The checklist

- Has every element here earned its place, or is some of it present because it was already there?
- Does the shape of this tell you what it does, before any documentation does?
- Is there a grid — a consistent structure — such that the irregular thing stands out?
- Is the reader being asked to think about something that is not the problem?

## Block 7 — The wider library

- **Dieter Rams — Ten Principles for Good Design** — the shortest useful design document ever written; all ten transfer to software <https://www.vitsoe.com/gb/about/good-design>
- **Massimo Vignelli — The Vignelli Canon** — published free by its author; the discipline of constraint, stated as rules <https://www.rit.edu/vignellicenter/>
- **Don Norman — The Design of Everyday Things** — affordance and signifiers; the one book on this list an engineer should read first
- **Steve Krug — Don't Make Me Think** — about web usability, and really about documentation
- **Josef Müller-Brockmann — Grid Systems in Graphic Design** — why a consistent structure is what makes an exception readable
- **Jan Tschichold — The New Typography** — and his later repudiation of it, which is the more useful half
- **Alan Cooper — About Face** — interaction design as a discipline separate from engineering
- **Charles & Ray Eames, Alvar Aalto** — the material half of the tradition — constraint as a source of form rather than a limit on it

## The corpus evidence

| Path in the corpus | What it carries |
|---|---|
| `SGraph-AI__App__Send/team/roles/designer/ROLE.md` | industrial, graphic and interaction design mapped to software explicitly — the canon named and put to work in a live role definition |

---

CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic). The anchor work belongs to its author and is linked, not licensed here.

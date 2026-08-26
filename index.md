# influences.sgit.ai — where the thinking came from

> **An inspiration is something that moved you. An influence is something that *shaped the
> work*** — and this is a register of 25 of them: the people, works, topics and things behind one
> body of software, with the idea worth taking from each and the exact place in a codebase where
> you can check that it landed.

*Source: <https://influences.sgit.ai/index.html> · site v0.3.0 · markdown twin of the front page.*

---

## Eight ideas worth stealing

Each one distilled to a single sentence you can apply without having read the book or watched the
talk — which is the test the format sets. Every entry behind them names where the idea shows up in
real code, at which version, and where it is still missing.

- **Bret Victor** *(traced)* — Immediate connection between creator and creation: a creator needs
  to see what they are making, as they make it. [The entry](register/bret-victor/index.html)
- **Tim Berners-Lee & the Semantic Web** *(traced)* — Meaning should be machine-readable, so that
  independent parties can exchange it without agreeing on a schema first.
  [The entry](register/semantic-web/index.html)
- **Design, with a capital D** *(traced, discovered)* — Design is not decoration applied after
  engineering: it is how the thing works. Start from what the person is trying to do and work
  backwards to the simplest interaction that does it. [The entry](register/design/index.html)
- **Flow, and coding in the zone** *(traced)* — Clear goals, immediate feedback and a challenge
  matched to skill produce the zone, so a methodology's job is to protect those three conditions
  rather than to optimise throughput. [The entry](register/flow/index.html)
- **Niklas Luhmann & the Zettelkasten** *(traced, discovered)* — External memory works as a
  thinking partner when its units are atomic, uniquely addressed, densely linked and allowed to
  grow structure rather than being filed into one. [The entry](register/luhmann/index.html)
- **Karl Popper & falsifiability** *(traced)* — A claim earns its status by being refutable. If
  nothing could show it to be wrong, it is not saying anything.
  [The entry](register/popper/index.html)
- **Christopher Alexander** *(discovered)* — Code is a space that people inhabit, and a language
  of patterns is what lets a place be built by many hands and still be coherent.
  [The entry](register/christopher-alexander/index.html)
- **Simon Wardley & Wardley Maps** *(traced)* — Situational awareness before strategy: draw the
  map before you argue about the move. [The entry](register/wardley/index.html)

These are eight of [25](register/index.html). The rest run from a Canadian drummer to a 1945 essay
about a machine nobody built.

## Five things a register like this is not supposed to contain

1. **An influence that is disagreed with.** The Semantic Web entry credits the ambition and then
   says exactly where the community went wrong — meaning attached to nodes rather than derived
   from edges. Two rows of its trace table record the influence being *inverted* rather than
   implemented. [Tim Berners-Lee & the Semantic Web](register/semantic-web/index.html)
2. **An influence that became a mandatory step in a pipeline.** Somebody read that good design is
   invisible — that you only notice it by going back to the previous version and feeling the loss
   — and turned it into two questions every interface change has to answer: *is it simpler? would
   reverting feel worse?* Not a quote on a wall. A gate that can fail.
   [Design, with a capital D](register/design/index.html)
3. **Influences the subject never claimed.** Seven entries were found by searching the work rather
   than asking the author. They are published as claims *about* him, and he is asked in public to
   strike the ones that do not belong. [The discovered tier](tiers/index.html#discovered)
4. **Entries with no evidence at all — published anyway.** Seven influences are on the founder's
   own list and the search found nothing. One of them has no public record and never will.
   [Music, and playing in a band](register/music-and-band/index.html)
5. **Rows that say *absent*.** Every entry lists the patterns from its anchor work that the
   codebase does not implement, written precisely enough to pick up as a work item.
   [The gaps, as build specs](format/index.html#block5)

## How to read the register

Twenty-five entries, sorted by how well the claim is evidenced rather than by how much they
mattered. **The tier is a statement about evidence, not importance** — a stated influence may well
be the deepest one on the list.

- **TRACED — 15.** The work names them. The entry lists the files and the claim can be checked
  against them, which is all *traced* means. [The definition](tiers/index.html#traced)
- **STATED — 7.** He says so and the record is silent. Published as stubs with the research plan
  visible and a hypothesis clearly labelled as one. [The definition](tiers/index.html#stated)
- **DISCOVERED — 3.** The record says so and he never did. Claims about him, awaiting his
  confirmation or his correction. [The definition](tiers/index.html#discovered)

Then: [all 25 entries](register/index.html) · [the influence map](map/index.html), computed from
the register rather than drawn · [seven blocks per entry](format/index.html) ·
[the wider library](library/index.html), a list of addresses rather than a collection.

## Articles

- [**An influence is a claim you can check**](articles/an-influence-is-a-claim.html) *(2026-08-26)*
  — an introduction to this register: the one move that separates it from a reading list, the
  five ideas worth stealing from it, the three tiers and what moves an entry between them, and
  the four things the site cannot do.

[All articles](articles/index.html). Each is a markdown file this site renders, so take the `.md`
if you want to republish it.

## One thing to know before you believe any of it

**A trace table cannot show causation.** It shows that a pattern from a talk appears in a codebase.
It cannot show that the talk put it there — and the finding that started this whole register is
exactly that distinction: half the estate's strongest features turned out to be *unknowing*
implementations of a talk's demos, built on instinct years later by people who had not connected
the two. The honest claim is that the instinct and the principle agree. It is weaker than *this
shaped the work*, and it is the one the evidence supports.

There is also an obvious conflict of interest: **association is flattery, and it costs nothing to
claim.** Saying that Victor, Popper and Alexander are in your intellectual lineage makes your work
sound better without making it better. The defence is the only one available — every claim here is
checkable by somebody who does not share the incentive.

[How the register was built, what the release gate refuses to publish, and the four things this
site cannot do](provenance/index.html).

---

All site content CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic). The anchor
works belong to their authors and are linked, never rehosted.

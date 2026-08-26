# An influence is a claim you can check

Everyone has a list of the people who shaped them. Almost nobody can show the shaping.

I have been keeping that list informally for twenty years — the talks I keep coming back to,
the books that changed how I argue, the communities that taught me how to work. The usual thing
to do with such a list is to publish it: a page of names, a paragraph each, some warm sentences
about how much they meant. I have read hundreds of those pages. I have never once finished one
knowing anything I could act on.

So `influences.sgit.ai` does something different, and it comes down to one move.

**An entry in this register is a falsifiable claim about my codebase.**

Anyone can say Bret Victor was an influence. The register says *which* of Victor's patterns
appear *where* in the estate, at *which* version — and which are still **absent**, specified
precisely enough that somebody could pick one up as a work item this afternoon.

## The move, in one table

Here is a real entry's trace table, abridged. It is the register's answer to "how did Steve
Jobs's idea of design shape your work?":

| Pattern from the anchor | Where it lands in the estate | Version | Status |
|---|---|---|---|
| Design is how it works, not how it looks | The Designer role definition | — | implemented |
| Start from the user's intent and work backwards | The NotebookLM case-study brief | v0.7.4 | implemented |
| Good design is invisible — you notice it by reverting | **The Jonathan Ive test**, a mandatory validator for every UI change | v0.7.4 | implemented |
| Simplicity as subtraction | Implied by the test, and nothing records the outcome | v0.7.4 | partial |
| The same discipline on an API, a CLI, a file format | Nowhere | v0.7.4 | absent |

Four things about that table are worth more than the whole page of warm sentences it replaces.

**It can be checked.** Every row names a place. Open the file, and either the pattern is there or
the row is wrong.

**The third row is what a fully absorbed influence looks like.** Not a quote on a wall — a gate
in a pipeline. Somebody read that good design is invisible, and that you only notice it by going
back to the previous version and feeling the loss, and turned it into two questions that every
interface change has to answer: *is it simpler? would reverting feel worse?*

**The last row is a build spec, not an omission.** The validator is scoped to visual changes, and
most of what anyone actually touches in this estate is an API, a CLI or a file format — surfaces
where those two questions apply word for word and are never asked. An influence page that names
what is missing is simultaneously provenance and backlog.

**And the fourth row is uncomfortable, which is the point.** *Is it simpler?* is asked, and the
answer is not kept anywhere. A register that only recorded successes would be a brochure.

## The ideas worth stealing

The register has twenty-five entries. These are the ones I would send somebody first.

### Immediate connection between creator and creation

Bret Victor's argument in *Inventing on Principle* is not about tools. It is that ideas can only
grow where their creator can see them growing, and that most of the ways we build software put a
compile step, a deploy step or a page refresh between a person and the thing they are making.
Every one of those steps is a place an idea dies.

The register for that talk found something I did not expect. Several of the estate's strongest
viewer features turned out to be **unknowing** implementations of the talk's demos — built on
instinct, years after watching it, without anyone connecting the two.

> Half the viewer's strongest features were already unknowing implementations of its demos, which
> is evidence the instinct and the principle agree; this register makes the agreement deliberate,
> so the next agent extends it on purpose rather than by luck.
> — Dinis Cruz, the immediate-connection register

That sentence is the reason the whole site exists. It is also a weaker claim than *the talk
caused this*, and the difference matters: a trace table can show that a pattern appears in a
codebase. It cannot show what put it there.

### An influence you argue with is still an influence

The Semantic Web entry is the format at its strongest, because I disagree with it in public.

The ambition was right, and twenty-five years on it is still the right target: a web where a
machine can act on meaning rather than pattern-match on strings. The execution went wrong in a
way that is technical rather than sociological.

> The Semantic Web community identified the right problem… But the community made a subtle
> mistake in practice. They ended up attaching meaning to nodes rather than deriving meaning from
> edges.
> — Dinis Cruz, `library/concepts/v0_4_0__thinking-in-graphs.md`

Attaching meaning to a node makes every node an assertion that has to be agreed on before anyone
can use it. Deriving meaning from edges makes agreement local, and lets two parties disagree
about what a thing *is* while still agreeing about how it *relates*. That inversion is
load-bearing in everything I have built since.

Two rows of that entry's trace table record the influence being **inverted** rather than
implemented. Influence is engagement, not agreement.

### Influences compose

The flow entry is the best demonstration on the site that these things are a graph rather than a
ranking.

Mihály Csíkszentmihályi described a state and its preconditions — clear goals, immediate
feedback, challenge matched to skill — and had nothing to say about software. Victor described a
mechanism, immediate connection, without naming the state it protects. Put the two together and
you get a claim you can test: **the reason immediate feedback matters is that it keeps the
challenge/skill balance visible**, and a thirty-second delay is enough to lose it.

That claim is what my development methodology is built on, and it explains an otherwise odd
design decision — the whole thing is organised around not breaking concentration rather than
around correctness or speed. Correctness can be checked afterwards. Concentration cannot.

The entry's own gap section is the part I like least and value most: **nothing measures whether
it works.** The methodology states its central claim about itself in its first line and does not
instrument it.

### External memory, arrived at three times

Niklas Luhmann was never on my list. The corpus surfaced him: a published article of mine that
maps his paper slip-box onto the graph model I now use, property by property — atomic, uniquely
identified, densely linked, emergent in structure, scalable and lifelong.

The property most systems get wrong is **emergent structure**. A slip-box has no taxonomy.
Nothing is filed under anything; a new note attaches to whatever it relates to, and the structure
is a consequence of the attaching. That is the same move as the edge-first inversion above,
arrived at independently, on index cards, decades earlier — and Vannevar Bush's memex is upstream
of both, with its idea of a *trail*: a path through documents that one person builds and another
can follow.

Eighty years later, that is still not what most systems do.

### And the one that explains the shape of everything else

Karl Popper's entry is the shortest on the site and the one with the longest reach.

A Wardley map is a claim about where a component sits, refutable by pointing at it. A risk in my
risks register is a claim with a named acceptor and a named mitigation, refutable by checking
whether the mitigation exists. A trace row on this site is a claim that a pattern appears at a
path at a version, refutable by opening the file.

Those three formats were not designed together and they have the same shape. Popper is the most
economical explanation.

The corollary is uncomfortable, and the site states it rather than hiding it: **an influence
claim is barely falsifiable at all.** You cannot open a file and check whether a talk caused a
design decision. The trace table is the best available substitute — it makes the consequence
checkable even when the causation is not.

## How the site is organised

Three tiers, and the tier is a statement about **evidence**, not importance.

**TRACED — 15 entries.** Corpus evidence exists. The entry lists the files by path and the claim
can be checked against them.

**STATED — 7 entries.** On my own list, and the corpus is silent. Most have *zero* evidence and
publish an empty evidence block saying so. Two decades of my earlier writing were not reachable
when the mining ran, and that is exactly where their evidence will be. One entry — playing in a
band — has no public record at all and never will. These are published as stubs with the research
plan visible. **They are the roadmap, not the debt.**

**DISCOVERED — 3 entries.** Found by mining the corpus, and never named by me. They are published
as claims *about* me, pending my confirmation, and the site asks me in public to strike any that
do not belong. A register that can only add is not falsifiable in the direction that matters.

That mechanism has already worked once. Design-with-a-capital-D was surfaced by mining, and I
confirmed it the day the commissioning pack shipped — the first DISCOVERED → confirmed
transition, before the site existed.

**Tier movement is the site's changelog.** An entry going STATED → TRACED because a briefing
document arrived, or DISCOVERED → TRACED because I confirmed it, or a trace row flipping *absent*
to *implemented* because we built one of the gaps an entry specified. A provenance site whose
provenance changed silently would be self-refuting.

Every entry follows the same seven blocks: the anchor, my own words, the principle distilled to
one transferable sentence, the trace table, the gaps as build specs, a checklist of questions to
ask of new work in that influence's light, and the wider library. The format was not designed for
the site — I wrote the Victor register first, as a working document, and only then asked what a
site made of such documents should be called.

## How it was made, briefly

Everything under `/register/` is generated from a single JSON file. The prose is authored once,
in a deliberately tiny markdown, and rendered twice — the HTML page and its markdown twin are two
renderings of one string, so they cannot drift. The influence map is computed from the same file
rather than drawn. Every tier count on every page is recomputed on each build; none of them is
typed.

Two of the release gate's checks enforce this site's own editorial rules rather than stating
them:

**The no-verbatim gate.** This site explains why a work resonated and traces where it was
applied. It does not reproduce the work. Every quotation declares whose words it carries — mine
are unrestricted, and a third party's are capped at forty words. The fix for a tripped gate is to
cut the quotation, never to raise the cap. That rule is what lets the CC BY stamp on this site's
own analysis stay honest, and it is also simply correct: every talk, book, essay, keynote and
record named here belongs to its author and stays where they put it.

**The register is the data.** Every influence has a page, every page is in the register, and
every tier count is recomputed and compared. Both halves have to be wrong in the same direction
to ship a wrong number.

## What it cannot do

Stated here rather than in a footnote, because a register that only ever confirms itself would be
an autobiography with citations.

A trace table cannot show causation. The corpus is cited rather than resolved — the repository
holds the website, not the estate, so evidence paths come from a dated mining run rather than a
build-time check, and seven entries have no trace table for that reason. The tiers partly measure
what has recently been written down, which means an entry sitting at STATED may well be the
deepest influence on the list.

And nothing here has ever been publicly retracted. Publishing your gaps is the cheap half of
falsifiability. Until something is withdrawn in public, with a date, the site is evidence of
ambition rather than of practice.

There is also a conflict of interest, and it is the sharpest on any site I publish: **association
is flattery, and it costs nothing to claim.** Saying that Victor, Popper and Alexander are in
your intellectual lineage makes your work sound better without making it better. The only defence
available is the one the whole site runs on — make every claim checkable by somebody who does not
share the incentive.

## What I would like back

The seven stated entries each need a briefing document, and two of them — Neil Peart, and the
years I spent playing in a band — are the ones nobody else can research. There is an open queue
for exactly that.

The three discovered entries need me to confirm or strike them.

And there is one entry I would most like to write and have not: a **counter-influence** — something
everyone assumes shaped my work and did not, or that I outgrew. A register that can only add is
the least interesting kind.

---

The site is at [influences.sgit.ai](https://influences.sgit.ai). Every entry is fetchable as
markdown as well as HTML, the register is one JSON file, and the influence graph is computed from
it. All of it is CC BY 4.0; none of the works it describes are mine to give away, so they are
linked and never rehosted.

# influences.sgit.ai — where the thinking came from

> The provenance layer of the sgit.ai memory network. The other sites teach an agent **what**
> the founder thinks and **how** the estate works; this one is for **where the thinking came
> from** — so an agent extends the instincts on purpose rather than by luck.

*Source: <https://influences.sgit.ai/index.html> · site v0.2.0 · markdown twin of the front page.*

---

## An influence entry is a falsifiable claim about the codebase

Anyone can say Bret Victor was an influence. This register says **which** of Victor's patterns
appear **where** in the estate, at **which** version — and which are still **absent**, specified
precisely enough that an agent could pick one up as a work item. That single move is what
separates it from every books-that-shaped-me listicle.

```
# /register/design/trace/ — one entry's table, abridged

pattern from the anchor            where it lands              ver      status
Design is how it works             the Designer role           —        implemented
Start from the user's intent       NotebookLM case study       v0.7.4   implemented
Good design is invisible           the Jonathan Ive test —     v0.7.4   implemented
                                   a MANDATORY validator
                                   for every UI change
Simplicity as subtraction          implied, not recorded       v0.7.4   partial
The same test on an API or CLI     nowhere                     v0.7.4   absent
```

The third row is what a fully absorbed influence looks like: not a quote on a wall, **a gate in a
pipeline**. The last row is why the format is worth having — it is a build spec, not an omission.
[The whole entry](register/design/index.html).

## Three tiers, and the difference is published

The tier is a statement about **evidence**, not importance. A stated influence may well be the
deepest one on the list — the tier says only how well the site can currently show it. Every count
is recomputed from the register on each build; none of them is typed.

- **TRACED — 15 entries.** The mining run found files. The entry lists them by path, and a reader
  with the repositories open can check whether they say what the entry claims. It still cannot
  show that the anchor work *caused* the pattern, and the site says so rather than implying more
  rigour than it has. [What TRACED does and does not mean](tiers/index.html#traced).
- **STATED — 7 entries.** On the founder's own list, and the corpus is silent. Most have **zero**
  evidence and publish an empty evidence block saying so. Two decades of earlier writing were out
  of reach; one entry — playing in a band — has no public record at all. **This is the roadmap,
  not the debt.** [Why the corpus is empty](tiers/index.html#stated).
- **DISCOVERED — 3 entries.** Found by mining, never on anyone's list, published as claims *about*
  the founder pending his confirmation — and he is
  [asked in public to strike the ones that do not belong](admin/comms.html#q2). The site's
  falsifiability applied to itself. [The tier the site is proudest of](tiers/index.html#discovered).
- **Tier movement is the changelog.** An entry going STATED → TRACED because a briefing arrived,
  or DISCOVERED → TRACED because the founder confirmed it. It has already happened once, before
  this site existed. [The movement log](shipped/index.html).

## Where to start

- [**Design, with a capital D**](register/design/index.html) — the strongest trace on the site.
  Discovered by mining and confirmed by the founder the day the pack shipped. The influence became
  the *Jonathan Ive test*, a mandatory validator for every UI change.
- [**Tim Berners-Lee & the Semantic Web**](register/semantic-web/index.html) — the format at its
  strongest, because this influence is disagreed with. Two of its trace rows are the influence
  *inverted*.
- [**Flow, and coding in the zone**](register/flow/index.html) — the best demonstration that
  influences compose: Csikszentmihalyi supplies the state, Victor the mechanism, and the estate's
  development methodology is what was built from both.
- [**Bret Victor**](register/bret-victor/index.html) — the entry the format came from, shipped
  with its trace table missing because the register that contains it is with the founder.
- [**Music, and playing in a band**](register/music-and-band/index.html) — no anchor URL, no
  evidence, no research plan that would work. The entry only he can write.
- [**Karl Popper & falsifiability**](register/popper/index.html) — the shortest entry with the
  longest reach, and the influence that explains the shape of all the others.

## Two rules, enforced rather than stated

This site's editorial commitments are checks in the release pipeline, because a site whose thesis
is that a claim should be checkable is in a poor position to publish unchecked claims about
itself.

```
# admin/build/validate.js, on every push to dev

the no-verbatim gate
  every <blockquote> declares whose words it carries
  data-quote="founder"     unrestricted  # his own writing
  anything else            40 words max  # quoted to be examined
  # the fix for a tripped gate is to cut the quotation,
  # never to raise the cap

the register is the data
  every influence in the register has a page
  every page under /register/ is in the register
  every tier count recomputed  # chrome.py writes them,
                               # validate.js recomputes them
                               # independently, and compares
```

**Link, never rehost.** Every talk, book, essay, keynote and record here belongs to its author and
stays where they put it. That instinct — the founder's own rule — is also the legally correct one:
it is what lets the CC BY stamp on this site's analysis stay honest.
[The rule, and what the gate cannot do](format/index.html#no-verbatim).

## What this site cannot do

Stated here rather than in a footnote, because a register that only ever confirms itself would be
an autobiography with citations:

- **A trace table cannot show causation.** It shows that a pattern from a talk appears in the
  codebase. It cannot show the talk put it there — and the Victor register's own finding is that
  half the estate's strongest features were *unknowing* implementations of its demos.
- **The corpus is cited, not resolved.** This repository holds the website, not the estate, so
  every evidence path is quoted from a dated mining run rather than checked at build time. Seven
  entries have no trace table for exactly that reason. [R1](admin/comms.html#r1).
- **The tiers partly measure what has recently been written down.** Two decades of earlier
  material were unreachable, and that is precisely where the stated influences' evidence will be.
  An entry sitting at STATED may be the deepest influence on the list.
- **Nothing here has ever been retracted.** Publishing gaps is the cheap half of falsifiability.
  [Until something is withdrawn in public, this site is evidence of ambition rather than of
  practice](shipped/index.html#wrong).

And the conflict of interest is the sharpest in the network: a project publishing the list of
thinkers who shaped its founder is doing something where **association is flattery and it costs
nothing to claim**. [The disclosure, in full](about/participant.html).

---

All site content CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic). The anchor
works belong to their authors and are linked, never rehosted.

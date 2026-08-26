# Design, with a capital D — the trace table

*Source: <https://influences.sgit.ai/register/design/trace/index.html>*

| Pattern from the anchor | Where the estate implements it | Version | Status |
|---|---|---|---|
| Design is how it works, not how it looks | The estate's Designer role definition, which is built on the formulation and extends it to coherence between internal structure and external experience | — | implemented |
| Start from the user's intent and work backwards (the Ive principle) | The NotebookLM case-study brief, in a section named for the principle, with the MP3-to-CD story as the worked example | v0.7.4 | implemented |
| Good design is invisible — you notice it by reverting and feeling the loss | **The Jonathan Ive test**: *is it simpler? would reverting feel worse?* — a mandatory validator for every UI change | v0.7.4 | implemented |
| Simplicity as subtraction — the feature removed rather than the feature added | Implied by the Ive test's first half and not separately enforced. Nothing records what was taken out of a change | v0.7.4 | partial |
| The same discipline applied to non-visual surfaces — an API, a CLI, a file format | Nowhere. The validator is scoped to UI changes, and the estate's public surface is mostly not UI | v0.7.4 | absent |

Row sources:

- Design is how it works, not how it looks — `team/roles/designer/ROLE.md`, cited in 02__ §D2
- Start from the user's intent and work backwards (the Ive principle) — `v0.7.4__brief__advocate-designer-in-the-loop-notebooklm-case-study.md`
- Good design is invisible — you notice it by reverting and feeling the loss — `v0.7.4__explorer-response__security-and-process-briefs.md`
- Simplicity as subtraction — the feature removed rather than the feature added — the same brief; the test states the criterion, nothing records the outcome
- The same discipline applied to non-visual surfaces — an API, a CLI, a file format — the validator's own stated scope

CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic).

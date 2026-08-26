#!/usr/bin/env python3
"""Generates /llms-full.txt — the single-file expansion of this site.

    python3 admin/build/gen_llms_full.py            # write it
    python3 admin/build/gen_llms_full.py --check    # fail if it has drifted (CI)

llms.txt is an index: it tells an agent what is here and where. This file is the
alternative for a reader that wants the whole thing — the index, the front page in
full, every register entry's markdown twin, and every source document, in one fetch,
each section labelled by where it came from.

It is GENERATED rather than written, for the same reason every other derived file here
is: a hand-maintained twin of a site is a stale artefact with a longer fuse. It is
assembled from llms.txt, index.md, register/*/index.md and briefs/*.md — each of which
is itself the source of truth for something — so it cannot say anything the site does
not.

One rule this file has that the sibling sites' do not: 04__ §6 of the brief says the
site must never put a third party's expression into the file it invites agents to
ingest wholesale. That holds by construction — every part of this file is assembled
from pages the no-verbatim gate in validate.js has already passed — and the header
below says so, because an agent reading this file should know what it is not allowed
to contain.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import ROOT, HOST, VERSION, register_data          # noqa: E402

OUT = ROOT / "llms-full.txt"

HEADER = f"""# influences.sgit.ai — full text

Site version: {VERSION}. Every page and every source document of https://{HOST}/ in one
file, so an agent can read the whole thing in a single fetch.

GENERATED — assembled by admin/build/gen_llms_full.py from llms.txt, index.md,
register/*/index.md and briefs/*.md, and re-checked in CI. It cannot say anything the
site does not.

Structure of this file:
  PART 1  the index (llms.txt), for orientation and the stable-URL promises
  PART 2  the front page in full (index.md)
  PART 3  the {{r}} register entries, each the markdown twin of its page
  PART 4  the {{n}} source documents this site is written from, verbatim

WHAT IS NOT IN THIS FILE, BY RULE: the anchor works. This site explains why an
influence resonated and traces where it was applied; it does not reproduce the talks,
essays, books or lyrics that did the influencing. Those are linked, never rehosted —
they belong to their authors and a CC BY file that carried them would be relicensing
what this site does not own. Short attributed quotation for analysis is capped at 40
words by the release gate. Follow the anchor URLs for the real thing.

The site's own text, trace tables, seed data and register are CC BY 4.0 — Dinis Cruz,
with AI co-authorship (Claude, Anthropic).

"""

RULE = "\n\n" + "=" * 78 + "\n"


def register_twins():
    """In the register's own order, from data/influences.json — not alphabetical by slug.
    The order is editorial: TRACED first, then STATED, then DISCOVERED, which is the
    order the site argues in."""
    out = []
    for i in register_data()["influences"]:
        p = ROOT / "register" / i["slug"] / "index.md"
        if p.exists():
            out.append((i["slug"], p))
    return out


def source_documents():
    briefs = ROOT / "briefs"
    if not briefs.exists():
        return []
    return sorted(p for p in briefs.iterdir()
                  if p.is_file() and p.suffix in {".md", ".csv"} and not p.name.startswith("."))


def build():
    twins = register_twins()
    briefs = source_documents()
    parts = [HEADER.replace("{r}", str(len(twins))).replace("{n}", str(len(briefs)) if briefs else "0")]

    parts.append(RULE + "PART 1 — THE INDEX (source: /llms.txt)" + RULE + "\n")
    parts.append((ROOT / "llms.txt").read_text().strip())

    parts.append(RULE + "PART 2 — THE FRONT PAGE (source: /index.md)" + RULE + "\n")
    parts.append((ROOT / "index.md").read_text().strip())

    if twins:
        parts.append(RULE + f"PART 3 — THE {len(twins)} REGISTER ENTRIES" + RULE + "\n")
        parts.append("Each is also fetchable on its own at /register/<slug>/index.md, the markdown\n"
                     "twin of /register/<slug>/index.html. Entries with a trace table also publish\n"
                     "it as data at /register/<slug>/trace/trace.json.\n")
        for slug, p in twins:
            parts.append(RULE + f"source: /register/{slug}/index.md" + RULE + "\n")
            parts.append(p.read_text().strip())
    else:
        parts.append(RULE + "PART 3 — THE REGISTER ENTRIES" + RULE + "\n")
        parts.append(
            "None are published yet. This release is the pipeline rather than the register:\n"
            "validation, auto-tagging and deployment are live, and the entries have not been\n"
            "written. When they are, each arrives as /register/<slug>/index.html with a markdown\n"
            "twin beside it, and this part of this file fills itself in.")

    if briefs:
        parts.append(RULE + f"PART 4 — THE {len(briefs)} SOURCE DOCUMENTS" + RULE + "\n")
        parts.append("The commissioning pack, verbatim. Each is also fetchable on its own at\n"
                     "/briefs/<filename>.\n")
        for b in briefs:
            parts.append(RULE + f"source: /briefs/{b.name}" + RULE + "\n")
            parts.append(b.read_text().strip())
    else:
        parts.append(RULE + "PART 4 — THE SOURCE DOCUMENTS" + RULE + "\n")
        parts.append(
            "None are published yet. When the commissioning pack lands it arrives verbatim\n"
            "under /briefs/<filename>, one reader page each under /documents/, and this part\n"
            "of this file fills itself in — nobody has to remember to update it.")

    return "\n".join(parts).rstrip() + "\n"


def main():
    content = build()
    if "--check" in sys.argv:
        if not OUT.exists():
            print("gen_llms_full --check: llms-full.txt is missing", file=sys.stderr)
            sys.exit(1)
        if OUT.read_text() != content:
            print("gen_llms_full --check: llms-full.txt is out of date — re-run the generator",
                  file=sys.stderr)
            sys.exit(1)
        print(f"gen_llms_full --check: OK — {len(content.split()):,} words, in sync")
        return
    OUT.write_text(content)
    print(f"gen_llms_full: wrote llms-full.txt — {len(content.split()):,} words, "
          f"{len(content):,} bytes")


if __name__ == "__main__":
    main()

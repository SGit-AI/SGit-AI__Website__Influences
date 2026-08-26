#!/usr/bin/env python3
"""Writes the front page's idea cards and quote wall, in place, from the register.

    python3 admin/build/gen_front.py            # fill the blocks
    python3 admin/build/gen_front.py --check    # fail if either has drifted (CI)

The front page is hand-written HTML — a person should be able to open it and edit the
argument. Two blocks in it are not, and they are the two that repeat something the
register already says:

    <!--GEN:ideas-->    ... <!--/GEN:ideas-->     the principles, verbatim
    <!--GEN:quotes-->   ... <!--/GEN:quotes-->    the quotations, verbatim
    <!--GEN:articles--> ... <!--/GEN:articles-->  the newest articles

Both are filled from data/influences.json. The reason is the rule the whole site runs
on rather than tidiness: a home page that hand-copies a principle is a home page that
keeps quoting last month's wording after somebody sharpens an entry. The selection —
which influences, which quotations, and the line of commentary under each — lives in
the register's `front` block, so even the editorial choice is data.

Nothing here invents text. Every principle and every quotation on the front page is
the string the entry publishes, and `--check` fails the release if a page has drifted.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import ROOT, esc, md_inline, register_data           # noqa: E402

DATA = register_data()
INF = {i["slug"]: i for i in DATA["influences"]}
FRONT = DATA.get("front", {"ideas": [], "quotes": []})
PAGE = ROOT / "index.html"


def find_quote(slug, qid):
    """A quotation by id, from either Block 2 (the founder's words) or Block 1 (a short
    attributed quotation of the anchor work itself). Raises on a miss rather than
    quietly rendering nothing — a silently empty quote wall is worse than a red build."""
    i = INF[slug]
    for q in i.get("founder_words", []):
        if q.get("id") == qid:
            return q["quote"], "founder", f'Dinis Cruz, <code>{esc(q["source"])}</code>'
    aq = i.get("anchor", {}).get("quote")
    if aq and aq.get("id") == qid:
        return aq["text"], aq["who"], esc(aq["who"])
    raise SystemExit(f"gen_front: no quotation id \"{qid}\" on {slug}")


def ideas_html():
    out = []
    for slug in FRONT["ideas"]:
        i = INF[slug]
        badge = (f'<span class="tierb tb-{i["tier"]}">{i["tier"]}</span>')
        # only on a PROMOTED entry: on one still sitting at DISCOVERED the tier badge
        # already says it, and two badges saying the same word is noise
        disc = ('<span class="kindb kb-disc">discovered → traced</span>'
                if i.get("discovered") and i["tier"] != "discovered" else "")
        out.append(
            f'  <a class="idea" href="register/{esc(slug)}/index.html">\n'
            f'    <div class="who"><b>{esc(i["title"])}</b>{badge}{disc}</div>\n'
            f'    <p class="pr">{md_inline(i["principle"])}</p>\n'
            f'    <span class="go">The entry, and where it lands →</span>\n'
            f'  </a>')
    return "\n".join(out)


def quotes_html():
    out = []
    for q in FRONT["quotes"]:
        text, who, credit = find_quote(q["slug"], q["id"])
        out.append(
            f'  <div class="qcard">\n'
            f'    <blockquote data-quote="{esc(who)}">{md_inline(text)}\n'
            f'    <footer>— {credit}</footer></blockquote>\n'
            f'    <p class="why">{md_inline(q["why"])}</p>\n'
            f'  </div>')
    return "\n".join(out)


def articles_html():
    """The newest articles, from data/articles.json. The home page used to hand-copy an
    article's title, date and summary, which is the same drift the register generators
    exist to prevent — one edit to a summary and the front page starts advertising the
    old one."""
    p = ROOT / "data/articles.json"
    if not p.exists():
        return "  <!-- no articles yet -->"
    arts = json.loads(p.read_text())["articles"][:2]
    return "\n".join(
        f'  <a class="art" href="articles/{esc(a["slug"])}.html">\n'
        f'    <b>{esc(a["title"])}</b>\n'
        f'    <span class="art-date">{esc(a["date"])}</span>\n'
        f'    <span class="art-sum">{md_inline(a["summary"])}</span>\n'
        f'    <span class="chips">'
        + "".join(f'<span class="chip">{esc(c)}</span>' for c in a.get("chips", []))
        + '</span>\n  </a>'
        for a in arts)


BLOCKS = {"ideas": ideas_html, "quotes": quotes_html, "articles": articles_html}


def build(text):
    for name, fn in BLOCKS.items():
        pat = re.compile(f"(<!--GEN:{name}-->)(.*?)(<!--/GEN:{name}-->)", re.S)
        if not pat.search(text):
            raise SystemExit(f"gen_front: index.html has no <!--GEN:{name}--> block")
        text = pat.sub(lambda m: m.group(1) + "\n" + fn() + "\n" + m.group(3), text)
    return text


def main():
    if not INF:
        print("gen_front: no register yet — nothing to fill")
        return
    before = PAGE.read_text()
    after = build(before)
    if "--check" in sys.argv:
        if before != after:
            print("gen_front --check: index.html has drifted from the register — "
                  "re-run the generator", file=sys.stderr)
            sys.exit(1)
        print(f"gen_front --check: OK — {len(FRONT['ideas'])} principles, "
              f"{len(FRONT['quotes'])} quotations and the article list match their sources")
        return
    if before == after:
        print("gen_front: index.html already matches the register")
        return
    PAGE.write_text(after)
    print(f"gen_front: wrote index.html — {len(FRONT['ideas'])} principles, "
          f"{len(FRONT['quotes'])} quotations")


if __name__ == "__main__":
    main()

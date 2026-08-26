#!/usr/bin/env python3
"""Generates /articles/ — the index and every article page — from markdown.

    python3 admin/build/gen_articles.py            # write the pages
    python3 admin/build/gen_articles.py --check    # fail if anything has drifted (CI)

    articles/<slug>.md      the article. WRITTEN. The source of truth.
    articles/<slug>.html    GENERATED from it, in the house shell
    articles/index.html     GENERATED from data/articles.json

An article is the one thing on this site somebody will want to take somewhere else —
into a newsletter, a post, an email. So the markdown file is the artefact and the page
is the rendering of it, rather than the other way round, and the two cannot disagree
because only one of them is written.

`data/articles.json` carries the index metadata: slug, date, summary and chips. It also
carries the title, which the markdown states too — and this generator FAILS if the two
disagree. Two statements of one fact is a bug unless something checks them.

Adding an article is two steps and no HTML: write `articles/<slug>.md` starting with its
`# Title`, add a row to `data/articles.json`, re-run this.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagelib import (ROOT, page_head, page_tail, write_or_check,         # noqa: E402
                     report, esc, md_inline)
import mdblock                                                           # noqa: E402

DATA = (json.loads((ROOT / "data/articles.json").read_text())
        if (ROOT / "data/articles.json").exists()
        else {"attribution": "Dinis Cruz, with AI co-authorship (Claude, Anthropic)",
              "articles": []})
ARTICLES = DATA["articles"]
SRC = ROOT / "articles"


def body_of(a):
    """The markdown, minus its H1 — which the page emits itself, from the same string,
    after checking that the file and the index agree about what it says."""
    p = SRC / f'{a["slug"]}.md'
    if not p.exists():
        raise SystemExit(f"gen_articles: articles/{a['slug']}.md does not exist")
    text = p.read_text()
    lines = text.split("\n")
    if not lines or not lines[0].startswith("# "):
        raise SystemExit(f"gen_articles: articles/{a['slug']}.md must start with '# Title'")
    title = lines[0][2:].strip()
    if title != a["title"]:
        raise SystemExit(
            f"gen_articles: articles/{a['slug']}.md says the title is \"{title}\" and "
            f"data/articles.json says \"{a['title']}\" — the two must agree")
    return "\n".join(lines[1:]).strip()


def article_page(a, prev_a, next_a):
    rel = f'articles/{a["slug"]}.html'
    html, heads = mdblock.render(body_of(a), where=f'articles/{a["slug"]}.md')

    # the contents list, from the h2s the article actually has
    toc = " · ".join(f'<a href="#{sid}">{md_inline(txt)}</a>'
                     for lvl, sid, txt in heads if lvl == 2)
    toc_html = f'<div class="toc">{toc}</div>' if toc else ""

    chips = "".join(f'<span class="chip">{esc(c)}</span>' for c in a.get("chips", []))
    nav_prev = (f'<a href="{prev_a["slug"]}.html">← {esc(prev_a["title"])}</a>' if prev_a
                else '<a href="index.html">← All articles</a>')
    nav_next = (f'<a href="{next_a["slug"]}.html">{esc(next_a["title"])} →</a>' if next_a
                else '<a href="index.html">All articles →</a>')

    body = f'''
<main class="doc article">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / <a href="index.html">articles</a> / {esc(a["title"])}</div>
<h1>{esc(a["title"])}</h1>
<p class="artmeta"><span class="art-date">{esc(a["date"])}</span> · {esc(DATA["attribution"])}</p>
<p class="chips">{chips}</p>
<p class="lead">{md_inline(a["summary"])}</p>
{toc_html}

{html}

<div class="note">
  <p><b>This article is a markdown file.</b> The page you are reading is generated from
  <a href="{esc(a["slug"])}.md"><code>articles/{esc(a["slug"])}.md</code></a>, which is the source of
  truth and is what to take if you want to republish it. CC BY 4.0 — {esc(DATA["attribution"])}.
  Every work named in it belongs to its author and is linked, never rehosted.</p>
</div>

<div class="pagenav">
  {nav_prev}
  {nav_next}
</div>
</main>
'''
    return rel, (page_head(
        rel,
        f'{esc(a["title"])} · influences.sgit.ai',
        esc(a["summary"]),
        og_title=esc(a["title"]),
    ) + body + page_tail())


def index_page():
    rel = "articles/index.html"
    if not ARTICLES:
        listing = ('<div class="warnbox"><p><b>No articles yet.</b> The first one is being '
                   'written.</p></div>')
    else:
        listing = '<div class="artlist">\n' + "\n".join(
            f'    <a class="art" href="{esc(a["slug"])}.html"><b>{esc(a["title"])}</b>'
            f'<span class="art-date">{esc(a["date"])}</span>'
            f'<span class="art-sum">{md_inline(a["summary"])}</span>'
            f'<span class="chips">'
            + "".join(f'<span class="chip">{esc(c)}</span>' for c in a.get("chips", []))
            + '</span></a>'
            for a in ARTICLES) + '\n</div>'

    body = f'''
<main class="doc">
<div class="crumb"><a href="../index.html">influences.sgit.ai</a> / articles</div>
<h1>Articles</h1>
<p class="lead">Longer pieces that make an argument across several entries — what an idea
means, where it came from, and what it changed. The <a href="../register/index.html">register</a>
is the reference; these are the reading.</p>

<div class="note">
  <p><b>Two rules keep these from going stale.</b> An article never restates a fact it does not
  own — it links to the entry that does, so when the entry changes the article does not start
  lying. And every article is a <b>markdown file</b> that this site renders, rather than a page
  somebody also keeps a copy of: take the <code>.md</code> if you want to republish it.</p>
</div>

{listing}

<div class="pagenav">
  <a href="../index.html">← Front page</a>
  <a href="../register/index.html">The register →</a>
</div>
</main>
'''
    return rel, (page_head(
        rel, "Articles · influences.sgit.ai",
        "Longer pieces that make an argument across several entries — what an idea means, "
        "where it came from, and what it changed.",
    ) + body + page_tail())


def main():
    check = "--check" in sys.argv
    changed, mismatched = [], []
    rel, html = index_page()
    write_or_check(ROOT / rel, html, check, changed, mismatched)
    for n, a in enumerate(ARTICLES):
        rel, html = article_page(a, ARTICLES[n - 1] if n else None,
                                 ARTICLES[n + 1] if n + 1 < len(ARTICLES) else None)
        write_or_check(ROOT / rel, html, check, changed, mismatched)
    report("gen_articles", check, changed, mismatched)


if __name__ == "__main__":
    main()

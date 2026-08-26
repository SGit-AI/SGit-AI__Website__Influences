#!/usr/bin/env node
// influences.sgit.ai pre-release gate. Run from anywhere: node admin/build/validate.js
// Checks, in order:
//   1. version agreement — admin/build/version.txt vs every page's version badge,
//      the versions table, llms.txt, llms-full.txt and index.md
//   2. internal links — every relative href/src in every .html file resolves to a
//      file in the tree, AND every #fragment resolves to an id on the page it names
//      (external and mailto links skipped)
//   3. canonical host — every <link rel="canonical"> and og:url points at the host
//      in CNAME, and every page declares one
//   4. the no-verbatim gate — this site's own rule, enforced rather than stated. Every
//      <blockquote> declares whose words it carries, and a third party's are capped at
//      QUOTE_MAX words. See §5 below: the rule is the site's licence armour.
//   5. the register is the data — every influence in data/influences.json has a page,
//      every register page is in the data, and every tier tally written into a page
//      agrees with the count recomputed from the data
//   6. the leak tripwire — nothing in the tree may look like a vault key, an AWS
//      key id, a GitHub token, a private key block or an AWS account id
// Any failure exits 1: no tag, no publish.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const errors = [];

function walk(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    if (name === '.git' || name === '.github' || name === 'node_modules' || name === '.sg_vault') continue;
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const rel = f => path.relative(ROOT, f);
const files = walk(ROOT);
const htmlFiles = files.filter(f => f.endsWith('.html'));

// --- 1. version agreement -------------------------------------------------
const VERSION = fs.readFileSync(path.join(ROOT, 'admin/build/version.txt'), 'utf8').trim();
if (!/^v\d+\.\d+\.\d+$/.test(VERSION)) {
  errors.push(`version.txt does not carry a vX.Y.Z version: "${VERSION}"`);
}
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const badges = [...t.matchAll(/class="ver"[^>]*>(v\d+\.\d+\.\d+)</g)].map(m => m[1]);
  for (const b of badges) if (b !== VERSION) {
    errors.push(`${rel(f)}: version badge ${b} != ${VERSION}`);
  }
}
for (const extra of ['llms.txt', 'llms-full.txt', 'index.md']) {
  const t = fs.readFileSync(path.join(ROOT, extra), 'utf8');
  if (!t.includes(VERSION)) errors.push(`${extra} does not mention ${VERSION}`);
}
const versTable = fs.readFileSync(path.join(ROOT, 'admin/versions.html'), 'utf8');
if (!versTable.includes(`class="vnum">${VERSION}<`)) {
  errors.push(`admin/versions.html has no row for ${VERSION}`);
}
// each release appears exactly once — a blanket version-bump sed that touches
// the history table produces duplicates, which shipped once on a sibling site
const rows = [...versTable.matchAll(/class="vnum">(v\d+\.\d+\.\d+)</g)].map(m => m[1]);
for (const v of rows) if (rows.filter(x => x === v).length > 1) {
  errors.push(`admin/versions.html lists ${v} more than once`);
  break;
}

// --- 2. internal links ----------------------------------------------------
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const dir = path.dirname(f);
  // the lookbehind matters: without it `data-src="x"` matches as `src="x"`, and the
  // document reader pages are full of data-src attributes that name a source document
  // rather than a path relative to the page.
  for (const m of t.matchAll(/(?<![\w-])(?:href|src)="([^"]+)"/g)) {
    const [target, fragment] = m[1].split('#');
    if (/^(https?:|mailto:|data:|\/\/)/.test(m[1])) continue;
    const resolved = target === '' ? f : path.resolve(dir, target);
    if (!fs.existsSync(resolved)) {
      errors.push(`${rel(f)}: broken link -> ${m[1]}`);
      continue;
    }
    // 2b. and the fragment resolves too. This site cross-links between entries by
    // section — a principle, a trace row, a gap spec — and a renamed heading turns
    // every one of those into a link that lands at the top of the right page and says
    // nothing. Only .html targets are checked; a fragment on a .md, .json or .txt file
    // is not an anchor.
    if (fragment && resolved.endsWith('.html')) {
      const targetText = fs.readFileSync(resolved, 'utf8');
      if (!targetText.includes(`id="${fragment}"`)) {
        errors.push(`${rel(f)}: link -> ${m[1]} but `
                  + `${rel(resolved)} has no id="${fragment}"`);
      }
    }
  }
}

// --- 3. canonical host ----------------------------------------------------
const HOST = fs.readFileSync(path.join(ROOT, 'CNAME'), 'utf8').trim();
if (!/^[a-z0-9.-]+$/.test(HOST)) errors.push(`CNAME does not carry a hostname: "${HOST}"`);
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const claimed = [
    ...[...t.matchAll(/<link[^>]+rel="canonical"[^>]+href="([^"]+)"/g)].map(m => m[1]),
    ...[...t.matchAll(/<meta[^>]+property="og:url"[^>]+content="([^"]+)"/g)].map(m => m[1]),
  ];
  for (const url of claimed) if (!url.startsWith(`https://${HOST}/`)) {
    errors.push(`${rel(f)}: canonical/og:url is not on ${HOST} -> ${url}`);
  }
  if (!/rel="canonical"/.test(t)) {
    errors.push(`${rel(f)}: no canonical link`);
  }
}

// --- 4. the no-verbatim gate ----------------------------------------------
// This site's founding rule is that the influences' own work is never reproduced at
// length: it explains resonance and traces application, and the anchor works stay
// links. That rule is also this site's licence armour — the analysis is original work
// and carries CC BY 4.0 cleanly, while a talk transcript or a verse of lyrics inside a
// CC BY page would be relicensing what the site does not own. A rule that important is
// worth a gate rather than a paragraph, so:
//
//   · every <blockquote> declares whose words it carries, with data-quote
//   · data-quote="founder" is unrestricted — Dinis Cruz's own articles, briefs and
//     registers are his to publish, and the register format runs on them
//   · anything else is a third party and is capped at QUOTE_MAX words: a sentence or
//     two, quoted in order to be examined, which is the fair-dealing core
//
// The gate cannot see an unmarked quotation woven into a paragraph. What it can do is
// make the marked case cheap and the unmarked case a review finding, and stop the one
// failure mode that actually ships: a long passage pasted in whole because it was
// useful. The fix for a tripped gate is to cut the quotation, never to raise the cap.
const QUOTE_MAX = 40;
const words = s => s.replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ')
                    .split(/\s+/).filter(Boolean).length;
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  for (const m of t.matchAll(/<blockquote([^>]*)>([\s\S]*?)<\/blockquote>/g)) {
    const who = (m[1].match(/data-quote="([^"]*)"/) || [])[1];
    if (who === undefined) {
      errors.push(`${rel(f)}: <blockquote> with no data-quote — say whose words these are `
                + `(data-quote="founder", or the third party's name)`);
      continue;
    }
    if (who === 'founder') continue;
    const n = words(m[2]);
    if (n > QUOTE_MAX) {
      errors.push(`${rel(f)}: ${n}-word quotation attributed to "${who}" exceeds the `
                + `${QUOTE_MAX}-word cap on a third party's words — cut it, do not raise the cap`);
    }
  }
}

// --- 5. the register is the data ------------------------------------------
// Every entry page is generated from data/influences.json, and the tier counts are
// recomputed here rather than trusted: a provenance site that hand-counts its own
// tiers has a number that drifts the first time an entry moves, which is the one
// event this site exists to record.
const DATA = path.join(ROOT, 'data/influences.json');
let influences = null;
if (fs.existsSync(DATA)) {
  influences = JSON.parse(fs.readFileSync(DATA, 'utf8')).influences;
  const slugs = new Set(influences.map(i => i.slug));
  for (const i of influences) {
    const page = path.join(ROOT, 'register', i.slug, 'index.html');
    if (!fs.existsSync(page)) {
      errors.push(`data/influences.json lists "${i.slug}" but register/${i.slug}/index.html `
                + `does not exist — re-run gen_register.py`);
    }
  }
  const dir = path.join(ROOT, 'register');
  if (fs.existsSync(dir)) for (const name of fs.readdirSync(dir)) {
    if (fs.statSync(path.join(dir, name)).isDirectory() && !slugs.has(name)) {
      errors.push(`register/${name}/ has no entry in data/influences.json — an orphan page `
                + `is a claim with no data behind it`);
    }
  }

  // The tallies. A page writes <span class="tally" data-k="traced">15</span>; chrome.py
  // fills the number in from the data and this check proves it, independently, from the
  // same source. Both halves have to be wrong in the same direction to ship a wrong count.
  const tally = {
    total:      influences.length,
    traced:     influences.filter(i => i.tier === 'traced').length,
    stated:     influences.filter(i => i.tier === 'stated').length,
    discovered: influences.filter(i => i.tier === 'discovered').length,
    'discovered-origin': influences.filter(i => i.discovered || i.tier === 'discovered').length,
    full:       influences.filter(i => i.status === 'full').length,
    'link-out': influences.filter(i => i.status === 'link-out').length,
    stub:       influences.filter(i => i.status === 'stub').length,
    'awaiting-briefing': influences.filter(i => i.briefing_status === 'requested').length,
  };
  for (const f of htmlFiles) {
    const t = fs.readFileSync(f, 'utf8');
    for (const m of t.matchAll(/<span class="tally" data-k="([^"]+)">([^<]*)<\/span>/g)) {
      const [, k, shown] = m;
      if (!(k in tally)) {
        errors.push(`${rel(f)}: tally data-k="${k}" is not a computed count`);
      } else if (shown !== String(tally[k])) {
        errors.push(`${rel(f)}: tally "${k}" says ${shown || '(empty)'}, `
                  + `the data says ${tally[k]} — re-run chrome.py`);
      }
    }
  }
}

// --- 6. the leak tripwire -------------------------------------------------
// These are shapes, not a wordlist: anything matching fails the release, and the fix is
// to redact the snippet, never to widen the pattern.
const LEAKS = [
  // an sgit vault key: a >=20-char passphrase joined by a colon to a uuid-shaped id
  [/[A-Za-z0-9_-]{20,}:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/,
                                                'a vault-key-shaped string'],
  [/\b(?:AKIA|ASIA)[0-9A-Z]{16}\b/,             'an AWS access key id'],
  [/\bgh[pousr]_[A-Za-z0-9]{36,}\b/,            'a GitHub token'],
  [/\bsk-(?:ant-)?[A-Za-z0-9_-]{24,}\b/,        'an API secret key'],
  [/-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----/,
                                                'a private key block'],
  [/\bxox[baprs]-[A-Za-z0-9-]{10,}\b/,          'a Slack token'],
  // an AWS account id is twelve bare digits. The pattern matches the shape rather than
  // any value: a tripwire that hard-codes the secret it looks for has published it.
  [/(?<![\d.-])\d{12}(?![\d.-])/,               'an AWS-account-id-shaped 12-digit number'],
];
for (const f of files) {
  if (/\.(png|jpg|jpeg|gif|webp|svg|ico|woff2?|zip|pdf)$/.test(f)) continue;
  // validate.js itself carries the patterns; exempting it is what makes them writable
  if (path.resolve(f) === path.resolve(__filename)) continue;
  const t = fs.readFileSync(f, 'utf8');
  for (const [re, what] of LEAKS) {
    const hit = t.match(re);
    if (hit) errors.push(`${rel(f)}: contains ${what} -> ${hit[0].slice(0, 12)}…`);
  }
}

// --- report ---------------------------------------------------------------
if (errors.length) {
  console.error(`validate: ${errors.length} error(s)`);
  for (const e of errors) console.error('  ✗ ' + e);
  process.exit(1);
}
const reg = influences ? `${influences.length} influences, tallies agree, ` : 'no register data yet, ';
console.log(`validate: OK — ${VERSION} on ${HOST}, ${htmlFiles.length} pages, links resolve, `
          + `${reg}no quotation over ${QUOTE_MAX} words attributed to a third party, `
          + `no credential-shaped string in ${files.length} files`);

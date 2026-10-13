#!/usr/bin/env python3
"""Render the static, readable-without-JavaScript publication from curated data."""
import json
from pathlib import Path
from html import escape
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/posts.json').read_text())
posts, sections = data['posts'], data['sections']
owner = data['owner']
base = 'https://ravisankarg.github.io/Blog/'
E = escape

def source(p):
    return f'https://github.com/{owner}/{p["repo"]}' + ('/' + p['sourcePath'] if p.get('sourcePath') else '')

def art(name, big=False):
    """Editorial diagrams are illustrations, not measured charts."""
    if name == 'near':
        content = '<g fill="currentColor" opacity=".24">' + ''.join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x,y in [(52,71),(79,94),(69,127),(97,146),(121,108),(112,61),(158,65),(183,94),(165,137),(205,158),(237,102),(256,74),(275,132),(228,56)]) + '</g><path d="M56 169L249 62M56 169L259 169" fill="none" stroke="currentColor" stroke-width="1" opacity=".4"/><path d="M56 169L184 74M56 169L221 136" fill="none" stroke="currentColor" stroke-width="2"/><path d="M184 74L221 136" fill="none" stroke="#c77945" stroke-width="2" stroke-dasharray="4 5"/><circle cx="184" cy="74" r="6" fill="currentColor"/><circle cx="221" cy="136" r="7" fill="#c77945"/><text x="175" y="52">q</text><text x="232" y="141">r</text><text x="70" y="205" class="svg-label">ORIGINAL + RESIDUAL</text>'
    elif name in ('cache','context','memory'):
        content = ''.join(f'<rect x="{65+c*40}" y="{46+r*29}" width="31" height="21" rx="3" fill="currentColor" opacity="{.12 if c>r else .25+r*.1}"/>' for r in range(5) for c in range(5))+'<path d="M62 201H258" stroke="currentColor" opacity=".45"/><text x="76" y="225" class="svg-label">CONTEXT → ATTENTION</text>'
    elif name in ('transfer','shared','fanout'):
        content='<rect x="32" y="68" width="79" height="99" rx="8" fill="none" stroke="currentColor"/><rect x="209" y="68" width="79" height="99" rx="8" fill="none" stroke="currentColor"/><path d="M119 117H198M187 107L198 117L187 127" stroke="currentColor" fill="none" stroke-width="2"/>'+''.join(f'<path d="M48 {y}H94M224 {y}H273" stroke="currentColor" opacity=".35" stroke-width="5"/>' for y in [88,108,128,148])+'<text x="134" y="93">f(x)</text><text x="75" y="206" class="svg-label">ONE IDEA → ANOTHER VIEW</text>'
    elif name in ('quant','prune'):
        content=''.join(f'<rect x="{39+i*28}" y="{165-h}" width="15" height="{h}" rx="2" fill="currentColor" opacity="{.3+i*.07}"/>' for i,h in enumerate([34,41,129,36,47,145,39,30,43]))+'<path d="M27 174H296" stroke="currentColor" opacity=".35"/><text x="85" y="207" class="svg-label">PRESERVE THE SIGNAL</text>'
    elif name in ('training','benchmark'):
        content='<path d="M38 45V181H288" stroke="currentColor" opacity=".3" fill="none"/><path d="M47 61C75 118 91 111 112 142S163 158 193 164S247 169 281 171M47 53C68 91 95 92 112 109S158 127 193 132S243 138 281 141" fill="none" stroke="currentColor" stroke-width="2"/><path d="M47 75C69 146 99 139 122 158S202 177 281 178" fill="none" stroke="#c77945" stroke-width="2"/><text x="96" y="210" class="svg-label">MEASURE. COMPARE. LEARN.</text>'
    elif name == 'device':
        content='<rect x="112" y="24" width="96" height="177" rx="17" fill="none" stroke="currentColor" stroke-width="2"/><path d="M140 36H180M149 188H171" stroke="currentColor" stroke-width="3"/><circle cx="160" cy="98" r="26" fill="none" stroke="currentColor" opacity=".35"/><path d="M148 99L157 108L175 86" stroke="currentColor" stroke-width="3" fill="none"/><path d="M130 146H190M140 159H180" stroke="currentColor" opacity=".4"/><text x="104" y="225" class="svg-label">LOCAL BY DESIGN</text>'
    else:
        content='<rect x="52" y="39" width="216" height="148" rx="9" fill="none" stroke="currentColor" opacity=".4"/><path d="M63 62V49H76M245 49H258V62M63 164V177H76M245 177H258V164" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="160" cy="109" r="37" fill="currentColor" opacity=".15"/><path d="M143 128L139 95Q139 84 148 94L151 106V76Q155 65 160 76L163 108L171 88Q179 81 181 94L177 127Z" fill="none" stroke="currentColor" stroke-width="2"/><text x="101" y="219" class="svg-label">COLLECT → TRAIN → TRY</text>'
    return f'<svg viewBox="0 0 320 245" aria-hidden="true" focusable="false">{content}</svg>'

def card(p):
    repo = p['repo']
    search = ' '.join([p['title'],p['description'],p['scope'],repo,p['format'],*p['tags']]).lower()
    dest = p['page'] or source(p)
    tags = ''.join(f'<span>{E(t)}</span>' for t in p['tags'])
    image = f'<div class="card-art art-{E(p["art"])}">{art(p["art"])}</div>' if p.get('art') else ''
    cls = 'post-card' if p['page'] else 'post-card code-note'
    return f'''<article class="{cls}" data-kind="{E(p['kind'])}" data-published="{'true' if p['page'] else 'false'}" data-search="{E(search, quote=True)}" id="post-{E(repo)}">
      {image}<div class="card-copy"><div class="card-meta"><span class="format">{E(p['format'])}</span><span class="destination">{'↗ Published page' if p['page'] else '⌘ Repository notes'}</span></div>
      <h3><a href="{E(dest)}">{E(p['title'])}</a></h3><p>{E(p['description'])}</p><div class="tags">{tags}</div>
      <p class="scope">{E(p['scope'])}</p><div class="card-links"><a class="read-link" href="{E(dest)}">{'Read the page' if p['page'] else 'Explore the notes'} <span aria-hidden="true">↗</span></a>{f'<a class="source-link" href="{E(source(p))}">Source code <span aria-hidden="true">↗</span></a>' if p['page'] else ''}</div></div></article>'''

nav = ''.join(f'<a href="#{s["id"]}"><span class="nav-num">{s["number"]}</span><span>{E(s["short"])}</span><span class="nav-count">{sum(p["section"]==s["id"] for p in posts):02}</span></a>' for s in sections)
body = ''
for s in sections:
    selected = [p for p in posts if p['section']==s['id']]
    body += f'''<section class="topic-section" id="{s['id']}" aria-labelledby="heading-{s['id']}"><header class="section-head"><span class="section-number">{s['number']}</span><div><h2 id="heading-{s['id']}">{E(s['title'])}</h2><p>{E(s['subtitle'])}</p></div></header><div class="post-grid">{''.join(card(p) for p in selected)}</div></section>'''
featured = next(p for p in posts if p.get('featured'))
published=sum(bool(p['page']) for p in posts)
reviewed=date.fromisoformat(data['reviewed']).strftime('%d %b %Y')
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">
<title>Ravi’s AI Field Notes — experiments, papers & things learned</title>
<meta name="description" content="Technical writing by Ravi Sankar Guntur. Interactive AI guides, independent paper implementations, small-model experiments, retrieval systems, and on-device applications.">
<link rel="canonical" href="{base}"><meta property="og:type" content="website"><meta property="og:title" content="Ravi’s AI Field Notes"><meta property="og:description" content="AI, understood by building. A collection of guides, experiments, and independent paper studies."><meta property="og:url" content="{base}"><meta name="theme-color" content="#f6f5ef"><link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="assets/style.css"><script src="assets/app.js" defer></script></head>
<body id="top"><a class="skip-link" href="#collection">Skip to the collection</a>
<header class="site-header wrap"><a class="brand" href="#top" aria-label="Ravi’s AI Field Notes home"><span class="monogram">r<span>/</span></span><span>RAVI’S <strong>AI FIELD NOTES</strong></span></a><nav aria-label="Main navigation"><a href="#collection">The collection</a><a href="#about">About these notes</a><a class="github-link" href="https://github.com/{owner}">GitHub <span aria-hidden="true">↗</span></a></nav></header>
<main><div class="wrap"><section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow"><span class="dot"></span> BY RAVI SANKAR GUNTUR</p><h1 id="hero-title">AI, understood<br>by <em>building.</em></h1><p class="hero-intro">Paper to code. Equation to experiment.<br>A field notebook of what I’m learning along the way.</p><a class="primary-link" href="#collection">Explore the collection <span aria-hidden="true">↓</span></a></div><aside class="hero-aside"><div class="field-mark" aria-hidden="true">[ curiosity → code → clarity ]</div><p>Small models.<br>Real measurements.<br>Useful questions.</p><div class="hero-stats"><div><strong>{len(posts):02}</strong><span>curated entries</span></div><div><strong>{published:02}</strong><span>published pages</span></div><div><strong>{len(sections):02}</strong><span>connected themes</span></div></div></aside></section>
<section class="featured" aria-labelledby="featured-title"><div class="featured-art"><div class="figure-label">RESEARCH NOTE / 13 OCT 2026</div>{art('near',True)}<div class="figure-caption">A second view of the same evidence.</div></div><div class="featured-copy"><p class="eyebrow">LATEST RESEARCH NOTE <span class="new-label">NEW</span></p><h2 id="featured-title"><a href="{featured['page']}">NEAR, under<br>the microscope.</a></h2><p>Can subtracting the neighborhood reveal what matters? An independent paper implementation, a SciFact experiment with EmbeddingGemma2, and a careful look at the limits.</p><div class="featured-result"><span>+0.53</span><p>nDCG@10 points<br><strong>Small. Inconclusive. Worth understanding.</strong></p></div><a class="read-link" href="{featured['page']}">Read the research note <span aria-hidden="true">↗</span></a></div></section>
<section class="reading-path" aria-labelledby="path-title"><div><p class="eyebrow">A GOOD PLACE TO START</p><h2 id="path-title">Follow an idea.</h2></div><a href="https://ravisankarg.github.io/kv-cache-playground/"><span>01 / UNDERSTAND</span><strong>Open the decoder</strong><small>Attention, one operation at a time ↗</small></a><a href="https://ravisankarg.github.io/cross-model-kv-transfer-guide/"><span>02 / CONNECT</span><strong>Carry context across models</strong><small>From a mechanism to a paper ↗</small></a><a href="https://ravisankarg.github.io/NEAR/"><span>03 / QUESTION</span><strong>Measure the retrieval gain</strong><small>From an idea to evidence ↗</small></a></section></div>
<div class="collection-shell wrap" id="collection"><aside class="collection-nav"><p class="eyebrow">THE COLLECTION</p><nav aria-label="Topics">{nav}</nav><div class="sidebar-note"><span aria-hidden="true">✳</span><p>Learning in public.<br>Including the experiments<br>that didn’t work.</p><small>Reviewed {reviewed}</small></div></aside><div class="collection-main"><div class="collection-heading"><h2>Notes from the workbench</h2><p>Browse by topic, or find a particular idea.</p></div><div class="tools" hidden><div class="search-row"><label class="search-box"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/></svg><span class="visually-hidden">Search the collection</span><input type="search" id="search" placeholder="Search ideas, models, methods…" autocomplete="off"></label><label class="pages-toggle"><input type="checkbox" id="pages-only"> Published pages only</label></div><div class="filter-row"><div class="filters" role="group" aria-label="Filter by format">{''.join(f'<button type="button" data-filter="{k}" aria-pressed="{str(k=="all").lower()}">{v}</button>' for k,v in [('all','All entries'),('guide','Learning guides'),('study','Paper studies'),('experiment','Experiments'),('application','Applications'),('notebook','Notebooks')])}</div><p id="result-count" role="status" aria-live="polite">{len(posts)} entries</p></div></div><div class="empty-state" hidden><span aria-hidden="true">∅</span><h3>No notes match that search.</h3><p>Try another model, topic, or format.</p><button type="button" id="reset">Clear all filters</button></div>{body}</div></div>
<section class="about wrap" id="about"><div><p class="eyebrow">ABOUT THE NOTEBOOK</p><h2>Understand it.<br>Build it. <em>Test it.</em></h2></div><div><p>I’m Ravi Sankar Guntur. These notes bring together my AI learning projects, paper implementations, and experiments—from the inside of a tiny decoder to retrieval systems that run on a phone.</p><p>Each entry points to the original publication or repository. The labels explain what you’ll find: a guide, a measured experiment, a paper study, or an application. Toy demonstrations, incomplete runs, and negative results keep their context.</p><p class="about-links"><a href="https://github.com/{owner}/Blog/blob/main/research/REPOSITORY_AUDIT.md">How this collection was curated ↗</a><a href="https://github.com/{owner}/Blog">Source for this site ↗</a></p></div></section></main>
<footer class="wrap"><a class="footer-brand" href="#top">Ravi’s AI Field Notes <span>↑</span></a><p>Independent notes · Open source · Always learning</p><span>© 2026 Ravi Sankar Guntur</span></footer></body></html>'''
(ROOT/'docs/index.html').write_text(html)
(ROOT/'docs/catalog.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(ROOT/'docs/.nojekyll').touch()
(ROOT/'docs/robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n')
(ROOT/'docs/sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{base}</loc><lastmod>{data["reviewed"]}</lastmod></url></urlset>\n')
print(f'Rendered {len(posts)} entries in {len(sections)} sections ({published} published pages).')

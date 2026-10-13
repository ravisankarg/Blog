#!/usr/bin/env python3
"""Check catalogue completeness, destinations and the generated site's local links."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/posts.json').read_text())
inventory=json.loads((root/'research/repository-inventory.json').read_text())
excluded=json.loads((root/'research/exclusions.json').read_text())
posts=data['posts']; sections={s['id'] for s in data['sections']}
names=[p['repo'] for p in posts]
assert len(names)==len(set(names)), 'Duplicate repository entries'
assert set(names).isdisjoint(excluded), 'Included repository also excluded'
assert set(names)|set(excluded)=={r['name'] for r in inventory['repositories']}, 'Inventory has unreviewed repositories'
for p in posts:
    assert p['section'] in sections
    assert p['kind'] in {'guide','study','experiment','application','notebook'}
    assert all(p.get(k) for k in ['title','description','scope','format','tags'])
    if p['page']:
        u=urlparse(p['page'])
        assert u.scheme=='https' and u.netloc=='ravisankarg.github.io'
        assert u.path=='/'+p['repo']+'/', f'Unexpected Pages destination: {p["repo"]}'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.urls=[]; self.articles=[]; self.headings=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ('href','src'):
            if a.get(k):self.urls.append(a[k])
        if tag=='article':self.articles.append(a)
        if tag in ['h1','h2','h3']:self.headings.append(tag)
p=Page();p.feed((root/'docs/index.html').read_text())
assert len(p.ids)==len(set(p.ids)), 'Duplicate page IDs'
assert p.headings.count('h1')==1
assert len(p.articles)==len(posts), 'Entry missing from static HTML'
for url in p.urls:
    u=urlparse(url)
    if not u.scheme and not u.netloc:
        if u.path: assert (root/'docs'/unquote(u.path)).is_file(), f'Missing local asset: {url}'
        elif u.fragment:assert u.fragment in p.ids, f'Broken anchor: {url}'
    else:assert u.scheme=='https', f'Unexpected external URL: {url}'
for card in p.articles:
    assert card['data-kind'] and card['data-search']
assert json.loads((root/'docs/catalog.json').read_text())==data
assert sum(bool(x['page']) for x in posts)==sum(a['data-published']=='true' for a in p.articles)
print(f'PASS: {len(posts)} entries, complete {len(inventory["repositories"])}-repository audit, unique anchors, local assets and HTTPS destinations.')
print('Formats:',dict(Counter(p['kind'] for p in posts)))

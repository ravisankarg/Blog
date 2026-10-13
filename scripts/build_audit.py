#!/usr/bin/env python3
"""Render a complete inclusion/exclusion ledger from the reviewed inventory."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
inventory=json.loads((root/'research/repository-inventory.json').read_text())
data=json.loads((root/'data/posts.json').read_text())
excluded=json.loads((root/'research/exclusions.json').read_text())
posts={p['repo']:p for p in data['posts']}
lines=['# Repository review — '+data['reviewed'],'',
       'All 29 public repositories owned by `ravisankarg` were reviewed before creating this collection. '+
       'Private repositories were not included. Repository metadata and READMEs were read through the GitHub connector; all 15 enabled Pages homepages and the advertised Ask Galaxy URL were opened in Chrome.', '',
       'The collection includes **21 entries: 13 live published pages and 8 repository-based notes or projects**, grouped into five topics. All eight exclusions are recorded below. This is editorial classification based on the cited material, not an independent rerun of the experiments.', '',
       'Dates in the inventory are repository push dates, not article publication dates. The MTEB page is a saved July snapshot; its “still running” label is historical, not evidence of an active process today.', '',
       '| Repository | Decision / format | Destination and review note |','| --- | --- | --- |']
for r in inventory['repositories']:
    name=r['name']; link=f'[{name}]({r["html_url"]})'
    if name in posts:
        p=posts[name]; dest=p['page'] or r['html_url']+('/'+p['sourcePath'] if p.get('sourcePath') else '')
        status='Live page opened' if p['page'] else 'Repository notes'
        lines.append(f'| {link} | Include · {p["section"]} · {p["format"]} | [{status}]({dest}). {p["scope"]} |')
    else:
        lines.append(f'| {link} | Exclude | {excluded[name]} |')
lines += ['', '## Review details', '',
          '- `8th_graders_intro_AI`: the default `main` branch contains only a license. The live classroom guide and its README/code are on `agent/local-rps-classroom-pages`; the catalogue links that branch explicitly.',
          '- `ask`: metadata advertises a Pages homepage but `has_pages` is false; the browser showed a GitHub Pages 404. Its entry links to the public repository instead.',
          '- `NEAR`: an independent implementation of the method, evaluated on SciFact with EmbeddingGemma2 text inputs. It is not a reproduction of the paper’s LMEB evaluation. Its small top-10 gain has a confidence interval crossing zero.',
          '- `cross-model-kv-transfer-guide`: a paper walkthrough plus synthetic GPU demonstration, not a real-LLM reproduction.',
          '- `folm-fanout-retrieval`: a resource-scaled implementation with a failed DEV gate. Training completion is not a quality improvement; v2 TEST remained locked.',
          '- `PrunedHarrier`: the published ledger is broader and more informative than the introductory README. Full-size controls are not compressed-model results.',
          '- `UniGemma` and `token-compressor` use EmbeddingGemma-300M; `NEAR` uses EmbeddingGemma2. These model identities are intentionally kept distinct.',
          '- `notebooks`: the README and root listing establish a learning collection; no blanket original-research or reproduction claim is made for its notebooks.',
          '- Enabled Pages sites for Grace and SriRamanaDentalCare were read and excluded based on their current content.',
          '', '## Refresh', '',
          'Use [blog_pub_skill](../skills/blog_pub_skill/SKILL.md). Re-discover every public repository, inspect new or changed source and live pages, update the curated data and exclusions, then regenerate this ledger and the site. Never silently remove an entry because of a transient fetch failure.', '']
(root/'research/REPOSITORY_AUDIT.md').write_text('\n'.join(lines))
print(f'Audited {len(inventory["repositories"])} repositories: {len(posts)} included, {len(excluded)} excluded.')

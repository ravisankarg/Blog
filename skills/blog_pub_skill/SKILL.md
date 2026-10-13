---
name: blog-pub-skill
description: Refresh Ravi Sankar Guntur's consolidated AI blog on GitHub Pages by reviewing all public ravisankarg repositories and live publications, classifying original guides and experiments, updating the catalogue, and publishing verified changes when requested. Saved locally as blog_pub_skill.
---

# blog_pub_skill

Maintain **Ravi’s AI Field Notes**, the single-page collection at `https://ravisankarg.github.io/Blog/`, backed by `ravisankarg/Blog`. The local skill folder is `skills/blog_pub_skill`; its tool-compatible skill name is `blog-pub-skill`.

## Start from the collection

Read `README.md`, `data/posts.json`, `research/repository-inventory.json`, and `research/REPOSITORY_AUDIT.md` in the blog repository. Inspect current Git status, remote, and any deployment already underway. Preserve the editorial design and the topic progression unless the user asks for a redesign.

## Discover and understand before editing

Run `python3 scripts/discover_repos.py` for a **read-only**, fully paginated public inventory. It writes a candidate under `research/discovery/` and never edits the catalogue. If CLI networking is unavailable, use the connected GitHub `list_repositories_by_affiliation` with `affiliation: owner`; follow pagination and filter owner `ravisankarg`, visibility `public`. An empty connector listing is not proof the account has no repositories.

For every public repository, inspect its description, fork status, README, relevant documentation/results, and any live Pages publication. For unchanged entries a dated prior review plus matching source state may be reused; new/changed entries need content review. Follow a nondefault publication branch when necessary. Check the actual live page: `has_pages` and the homepage field are discovery hints, not proof that a destination loads.

Use these independent classifications:

- **Topic:** foundations, inference, retrieval/memory, model training, or on-device AI.
- **Kind:** `guide`, `study`, `experiment`, `application`, or `notebook`.
- **Format:** a precise label such as independent paper implementation, synthetic toy, benchmark report, classroom lab, or application architecture.
- **Evidence/scope:** the short qualification needed to interpret what was actually built or measured.

Read enough to distinguish a full paper reproduction from a resource-scaled adaptation or synthetic demonstration. Preserve negative and inconclusive results, historical snapshots, incomplete runs, and the distinction between training alignment and external task quality. Keep exact model identities: NEAR uses **EmbeddingGemma2**; some older projects use EmbeddingGemma-300M.

Prefer working GitHub Pages links. AI projects without a working page may be included as clearly marked repository notes, linked to an informative README/report. Never fabricate a Pages URL or publish an unrelated project to repair its link. Do not attribute an upstream fork's work to Ravi. Non-AI projects, empty placeholders, and unmodified third-party forks belong in the exclusion ledger, with a reason. Do not expose private repositories or include raw notebook outputs, device data, credentials, model weights, or research caches in this public hub.

## Update the curated source

Edit `data/posts.json` and `research/exclusions.json`; adopt the verified public inventory in `research/repository-inventory.json`. Every discovered repository must be accounted for. `Blog` itself should be marked as collection infrastructure, not a technical article. A transient fetch failure must not silently remove a published entry.

Each post needs a unique `repo`, `title`, valid `section`, `kind`, `format`, a verified `page` URL or `null`, `description`, meaningful `scope`, and `tags`. Optional `sourcePath` links a report or nondefault branch; `art` selects an existing illustration. Update `reviewed` only after content/link review. Repository push dates are not article publication dates. The featured card and suggested reading path are editorial markup in `scripts/build_site.py`; change them deliberately if the featured article changes.

Run:

```bash
python3 scripts/build_audit.py
python3 scripts/build_site.py
python3 scripts/validate.py
node --check docs/assets/app.js
```

Test search, every format filter, Pages-only filtering, combined filters, empty-state reset, direct query URLs, and topic anchors. Verify the static HTML still includes all entries without JavaScript. Inspect desktop and narrow-screen layouts and horizontal overflow. Use the available permitted browser preview; if local preview is denied, do not bypass that denial. Validate the published site once deployment is authorized and complete.

## Publish and verify

A request to refresh/publish this public collection authorizes updating its repository and Pages site; a review-only request does not. Commit only the reviewed site, catalogue, scripts, ledger, and skill. Ignore raw research dumps and temporary QA files. If workspace Git metadata is protected/unusable, use a valid temporary checkout or the GitHub connector; do not replace protected metadata.

Use the existing repository and Pages configuration. When starting a new repository, create the reviewed public source, then enable Pages for GitHub Actions. The workflow deploys only `docs/`, with `contents: read`, `pages: write`, `id-token: write`, and environment `github-pages`. Check current official action releases before changing workflow versions.

Wait for the specific pushed commit's Pages deployment to succeed. Verify the real public page, styles, scripts, catalogue, interactions and responsive layout. If deployment fails, read the actual failure before one targeted correction; if access or approval blocks it, preserve prepared work and state the exact remaining action rather than claiming publication succeeded.

Report the live URL, repository, included/published counts, meaningful changes, and any verification limit. Do not create schedules or modify linked projects unless requested.

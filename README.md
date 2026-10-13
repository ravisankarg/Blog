# Ravi’s AI Field Notes

A consolidated, public index of Ravi Sankar Guntur’s AI guides, independent paper studies, model experiments, and on-device applications.

**Read the blog:** https://ravisankarg.github.io/Blog/

The first review covers all 29 public repositories, with **21 curated entries**, including **13 published GitHub Pages sites**. Entries are organized into foundations, efficient inference, retrieval and memory, model experiments, and on-device AI. Search, format filters, and a published-pages filter make the collection easier to navigate. All entries and links remain readable without JavaScript.

[Read the complete repository audit](research/REPOSITORY_AUDIT.md) for inclusion decisions, exclusions, and evidence boundaries. These classifications summarize the existing project materials; creating this index did not rerun the underlying research.

## Refresh the collection

The requested local **blog_pub_skill** is saved at [`skills/blog_pub_skill/SKILL.md`](skills/blog_pub_skill/SKILL.md). Ask the agent to use that file to refresh and publish the blog. Its frontmatter uses the compatible name `blog-pub-skill`. It is a repository-local skill, not a claim of global installation.

```bash
python3 scripts/discover_repos.py
# Review new/changed repositories and live pages.
# Update data/posts.json, research/exclusions.json and the reviewed inventory.
python3 scripts/build_audit.py
python3 scripts/build_site.py
python3 scripts/validate.py
node --check docs/assets/app.js
```

`discover_repos.py` is read-only and requires authenticated GitHub CLI access. It writes candidate metadata under ignored `research/discovery/`; it never automatically edits or deletes curated entries. The skill also describes the connected GitHub fallback.

## Preview and publication

```bash
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. The site has no JavaScript package dependencies, external font requests, analytics, cookies, or third-party assets. Illustrations are decorative SVG, not experimental data. Python’s standard library generates the static HTML and public catalogue.

GitHub Actions validates the catalogue and generated output before deploying `docs/`. Source data lives in `data/posts.json`; generated HTML lives in `docs/index.html`. Editorial layout and the featured reading path are in `scripts/build_site.py`; presentation and filtering live in `docs/assets/`.

---
title: "Building the Markdown Loader"
slug: "building-the-loader"
date: "2025-09-01T11:00:00"
summary: "How we parse YAML front-matter, validate fields, convert Markdown to HTML, and cache posts in memory."
image: "img/torbellino.jpeg"
---

# Goal

Load every `content/posts/*.md`, extract **YAML front-matter**, validate required fields, convert the **Markdown body** to HTML, and expose a fast, read-only in-memory API.

---

## Loading pipeline

1. **Discover** files ending in `*.md` under `content/posts/`.
2. **Split front-matter**: leading `---`…`---` is YAML; the rest is Markdown.
3. **Parse YAML** with `PyYAML` (`yaml.safe_load`).
4. **Validate**:
   - `title`: non-empty string (required).
   - `slug`: normalized, must match `^[a-z0-9]+(-[a-z0-9]+)*$`. Duplicates → error.
   - `date`: ISO date/datetime; stored as `datetime` for sorting.
   - `summary`: optional; if missing, we auto-generate an excerpt (first ~40 words).
   - `image`: optional path under `/static/` (e.g., `img/torbellino.jpeg`).
5. **Markdown → HTML** using the `markdown` library with `extensions=["extra"]`.
6. **Sort** posts by `date` descending (newest first).
7. **Cache**: keep a dict by slug and a pre-sorted list in memory.
8. **API** surface: `all_posts()` and `get_by_slug(slug)`.

---

## Design notes

- The repository is a **singleton** created by `get_repository()` and preloaded in `AppConfig.ready()`.
- We **reset** the Markdown parser per file to avoid state leakage (`md.reset()`).
- Errors are explicit (invalid slug/date, missing closing `---`, duplicate slug) so content issues are easy to fix.

---

## Future extensions

- `tags: [python, django]` in front-matter and tag archives.
- Index pagination (simple slicing).
- Lightweight full-text search in memory (titles + content).

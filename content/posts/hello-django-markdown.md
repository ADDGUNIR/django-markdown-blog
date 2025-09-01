---
title: "Hello, Django + Markdown"
slug: "hello-django-markdown"
date: "2025-09-01T12:00:00"
summary: "Project overview: database-free blog using Markdown files with YAML front-matter, in-memory repository, and DTL templates."
image: "img/kilitorbe.jpeg"
---

# Overview

This blog runs **without a database**. Posts are Markdown files with **YAML front-matter**.
On startup, an **in-memory repository** loads and validates those files, offering:
- `all_posts()` → list ordered by date (desc).
- `get_by_slug(slug)` → fetch a single post by its slug.

The **index view** renders cards with title, date, summary, and an optional hero image.  
The **detail view** resolves by `slug` and displays the HTML converted from Markdown.

---

## File format (front-matter + body)

Each post lives in `content/posts/<name>.md`:

~~~yaml
---
title: "Readable title"
slug: "readable-title"           # lowercase letters, digits and hyphens (a-z0-9-)
date: "2025-09-01T12:00:00"      # ISO 8601
summary: "A short sentence for the home page."
image: "img/kilitorbe.jpeg"      # path under /static/
---
~~~

Write normal **Markdown** below the second `---`.  
We convert the body to HTML using the `markdown` library (with the `extra` extension).

---

## Validation rules

- `title` required (non-empty string).
- `slug` optional; if omitted, the file name is used. Must match `^[a-z0-9]+(-[a-z0-9]+)*$`.
- `date` accepts ISO date/datetime.
- `summary` optional; if missing, we auto-generate a short excerpt from the body.
- `image` optional; if missing, the index uses a placeholder.

---

## Why no DB?

- **Simplicity**: no models or migrations.
- **Portability**: content ships with the repo.
- **Predictability**: static files + WhiteNoise.

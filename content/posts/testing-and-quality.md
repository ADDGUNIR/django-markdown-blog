---
title: "Testing and Quality: What to Verify"
slug: "testing-and-quality"
date: "2025-09-01T08:00:00"
summary: "What is worth testing in a database-free Django blog, from loader correctness to basic view responses."
image: "img/atardecer.jpeg"
---

# Why test this project?

Even without a database, there are failure modes: malformed front-matter, duplicate slugs, missing images, or broken templates. A thin test suite keeps the blog reliable.

---

## What to test (minimum useful set)

1. **Loader correctness**
   - At least **3 posts** are discovered and loaded.
   - `get_by_slug` returns a post and fields are populated (`title`, `date`, `content_html`).
   - Duplicate slug raises a clear error.

2. **Views**
   - Home (`/`) renders **200 OK** and shows ≥3 post cards.
   - Detail (`/posts/<slug>/`) renders **200 OK** for a known slug.
   - Unknown slug returns **404**.

3. **Static pipeline sanity**
   - Templates reference `{% static %}` properly.
   - A missing hero image gracefully falls back to a placeholder.

---

## Running tests locally (pytest)

~~~bash
# From the project root
pytest -q
~~~

If you use Django’s test runner instead:

~~~bash
python manage.py test
~~~

---

## Extending the suite

- Validate **date** parsing accepts ISO date or datetime.
- Ensure Markdown extensions don’t leak state between files (we call `md.reset()` per document).
- Add a **link check** pass that scans `content_html` for `href="/posts/.../"` and verifies the target slug exists.

---

## Manual QA before deploy

- `DEBUG=False`, `SECRET_KEY` set, and `ALLOWED_HOSTS` includes the Render domain.
- `collectstatic` succeeds and `/static/` is served by WhiteNoise.
- Home and a couple of detail pages load fast over cold cache.

A tiny investment in tests and checks saves time every time you add or edit content.

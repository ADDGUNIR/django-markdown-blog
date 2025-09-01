---
title: "Authoring Posts in Markdown"
slug: "authoring-in-markdown"
date: "2025-09-01T09:00:00"
summary: "Practical guidelines for writing posts with YAML front-matter, images, internal links, and accessible content."
image: "img/sallent.jpeg"
---

# Goals

Make authoring frictionless and consistent: predictable front-matter, clean slugs, reliable images, and accessible markup.

---

## Front-matter template

~~~yaml
---
title: "Readable title"
slug: "readable-title"
date: "2025-09-01T09:00:00"
summary: "One-line teaser for the home page."
image: "img/sallent.jpeg"
---
~~~

**Rules**  
- `title`: required.  
- `slug`: optional; if omitted, file name is used. Must match `^[a-z0-9]+(-[a-z0-9]+)*$`.  
- `date`: ISO; used for sorting (newest first).  
- `summary`: optional; auto-excerpt is generated if missing.  
- `image`: optional; index uses a placeholder when absent.

---

## Images

- Place files under `static/img/` and reference them via `image: "img/your-file.jpg"`.
- Prefer **JPEG** for photos (smaller), **PNG** for UI diagrams, **SVG** for vector icons.
- Always provide useful **alt text** when embedding images in the body:

~~~markdown
![Close-up of the blog's home page grid](../static/img/sallent.jpeg)
~~~

> Note: In post bodies, you can also reference images via the `{% static %}` URL in templates, but plain relative paths are fine when served by WhiteNoise.

---

## Linking

- **Internal links** between posts use the `slug`:
  - `/posts/hello-django-markdown/`
  - `/posts/building-the-loader/`
- Keep slugs stable to avoid broken links.

---

## Markdown tips

- Use `#`…`####` headings sequentially (no jumps from `#` to `####`).
- Keep paragraphs short; lists help scannability.
- Code blocks with language fences for syntax highlighting:

~~~python
def hello():
    return "world"
~~~

- For callouts, simple blockquotes:

> Deployment requires `ALLOWED_HOSTS` to include your Render domain.

---

## Content QA checklist

- [ ] The front-matter parses (no missing closing `---`).  
- [ ] Slug is unique and URL-safe.  
- [ ] Hero image exists under `static/img/`.  
- [ ] Links work locally.  
- [ ] `summary` is concise (≤ 160 chars) and informative.

# Unchaining Django — Markdown Blog (No DB)

A tiny Django blog that **does not use a database**. Posts live as Markdown files with **YAML front-matter** under `content/posts/*.md`. On startup, a repository **loads, validates, and caches** posts in memory. Views and templates are DTL. Static files are served via **WhiteNoise**.

- Live: <https://your-render-service.onrender.com>  <!-- replace -->
- Repo: <https://github.com/ADDGUNIR/django-markdown-blog>  <!-- replace -->

## Tech Stack
- **Django 5.1**
- **WhiteNoise** (production static files)
- **Markdown** (Markdown → HTML)
- **PyYAML** (front-matter parsing)
- **Gunicorn** (WSGI in production)
- **pytest + pytest-django** (tests)

## Features
- No DB/ORM/models — files + in-memory repository.
- Home page shows **≥ 3** post summaries (newest first).
- Detail page by **slug** with text and images.
- Sticky footer: “Unchaining Django · Built with Django + Markdown + YAML”.
- Clean DTL templates; images in `static/img/`.

---

## Project Structure
~~~
.
├── blog/
│   ├── apps.py
│   ├── posts_repository.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── content/
│   └── posts/                  # *.md with YAML front-matter
├── static/
│   └── img/                    # images referenced from posts
├── templates/
│   ├── base.html
│   ├── index.html
│   └── post_detail.html
├── tests/
│   ├── test_posts_repository.py
│   └── test_views.py
├── Procfile
├── pytest.ini
├── requirements.txt
└── manage.py
~~~

---

## Requirements & Installation
~~~bash
# Python 3.12 recommended
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python manage.py runserver
# http://127.0.0.1:8000/
~~~

---

## Configuration
Environment variables (especially for production):
- `SECRET_KEY` — long random string.
- `DEBUG` — `false` in production, `true` in dev.
- `ALLOWED_HOSTS` — comma-separated (`your-service.onrender.com,localhost`).

Static files:
- `STATIC_URL = "/static/"`
- `STATICFILES_DIRS = [BASE_DIR / "static"]`
- `STATIC_ROOT = BASE_DIR / "staticfiles"`
- `STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"`

No database is configured (`django.db.backends.dummy`).

---

## Posts Format (Markdown + YAML front-matter)
Each post is a `.md` under `content/posts/`:

~~~yaml
---
title: "Readable title"
slug: "readable-title"           # a-z0-9 and hyphens
date: "2025-09-01T12:00:00"      # ISO 8601 (date or datetime)
summary: "One-line teaser for the home page."
image: "img/your-image.jpg"      # path under /static/img/
---
~~~

Write Markdown after the second `---`. The loader converts it to HTML using `markdown` with `extra`.

Validation:
- `title` required.
- `slug` optional (defaults to file name) and must match `^[a-z0-9]+(-[a-z0-9]+)*$`.
- `date` must be ISO; used for sorting.
- `summary` optional (auto-excerpt if missing).
- `image` optional (index falls back to a placeholder).

**Images** go in `static/img/` and are referenced as `image: "img/filename.jpg"`.

---

## URLs
- Home: `/`
- Post detail: `/posts/<slug>/`

---

## Tests
~~~bash
pytest -q
~~~

We verify:
- Repository loads **≥ 3** posts and fetches by slug.
- Home page returns **200 OK** and shows ≥ 3 cards.
- Detail page for a known slug returns **200 OK**.

---

## How It Works
- On startup, `BlogConfig.ready()` calls `get_repository().reload()`.
- The repository scans `content/posts/*.md`, splits front-matter, parses YAML, validates fields, converts Markdown, and **caches**:
  - dict by slug
  - pre-sorted list (newest first)
- Requests read from memory. Updating content requires a restart (dev) or redeploy (prod).

---

## Deploy to Render (recommended)
1) Connect repo on **Render** → **New** → **Web Service** (select GitHub repo).  
2) **Build Command:**
~~~bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
~~~
3) **Start Command:**
~~~bash
gunicorn config.wsgi:application
~~~
4) **Environment:**
- `SECRET_KEY` = generate with:
  ~~~bash
  python -c "import secrets; print(secrets.token_urlsafe(50))"
  ~~~
- `DEBUG` = `false`
- `ALLOWED_HOSTS` = `your-service.onrender.com`
- (optional) `PYTHON_VERSION` = `3.12.11`

After deploy, open the public URL. If static files don’t load, check WhiteNoise middleware and build logs for `collectstatic`.

**Content updates**: commit + push → redeploy (or “Manual Deploy → Clear cache & deploy”).

---

## Deploy to PythonAnywhere (alternative)
- Create a virtualenv and install requirements.
- Set WSGI app to `config.wsgi:application`.
- Set env vars (`SECRET_KEY`, `DEBUG=false`, `ALLOWED_HOSTS=<yourdomain>.pythonanywhere.com`).
- Run `python manage.py collectstatic --noinput`.
- Reload the web app.

---

## Troubleshooting
- **400/403 host**: add your domain to `ALLOWED_HOSTS`.
- **Static files missing**: ensure `collectstatic` runs and WhiteNoise middleware is immediately after `SecurityMiddleware`.
- **Startup fails**: likely a content error (invalid slug/date, missing closing `---`).
- **Images not showing**: confirm the file exists in `static/img/` and the front-matter `image:` path matches.

---

## License
MIT (or your preferred license).
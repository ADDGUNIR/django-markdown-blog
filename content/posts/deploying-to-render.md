---
title: "Deploying to Render"
slug: "deploying-to-render"
date: "2025-09-01T10:00:00"
summary: "Step-by-step: Render.com + Gunicorn + WhiteNoise for a database-free Django blog."
image: "img/kili.jpeg"
---

# Objective

Deploy this blog to **Render.com** using:
- `gunicorn` to serve `config.wsgi:application`,
- **WhiteNoise** for static files under `/static/`,
- `collectstatic` during the build.

Result: a public URL like `https://<your-service>.onrender.com/`.

---

## Prerequisites

Your GitHub repo should include:
- `requirements.txt` (Django, whitenoise, PyYAML, Markdown, gunicorn),
- `config/settings.py` with:
  - `STATIC_ROOT` set (e.g., `BASE_DIR / "staticfiles"`),
  - `STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"`,
  - `MIDDLEWARE` contains `whitenoise.middleware.WhiteNoiseMiddleware` right after `SecurityMiddleware`,
- optional `Procfile`:

~~~procfile
web: gunicorn config.wsgi:application
~~~

---

## Environment (production)

In Render → your service → **Environment**:

- `SECRET_KEY`: strong random string (e.g., from `python -c "import secrets; print(secrets.token_urlsafe(50))"`).
- `DEBUG`: `false`
- `ALLOWED_HOSTS`: `your-service.onrender.com` (comma-separated if multiple).

---

## Create the service

1. Render → **New** → **Web Service** → connect to your GitHub repo.
2. **Build Command**:

~~~bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
~~~

3. **Start Command**:

~~~bash
gunicorn config.wsgi:application
~~~

4. Add environment variables (above) and deploy.

---

## Post-deploy checks

- Home page shows cards and images.
- Detail pages return **200 OK**.
- Logs confirm `collectstatic` ran and Gunicorn started cleanly.

---

## Common issues

- **400/403 host** → add your Render domain to `ALLOWED_HOSTS`.
- **Missing static files** → ensure WhiteNoise middleware + `collectstatic` in Build Command.
- **Startup errors** → usually invalid front-matter (bad slug/date or missing closing `---`).

---

## Content updates

Because posts are cached in memory at startup, updating/adding Markdown files requires a **new deploy** (or “Manual Deploy → Clear cache & deploy”).

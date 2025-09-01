from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Development defaults; DEBUG will be False in production
DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-key-change-me")

# Allow all in dev; set a concrete host list in production via env
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    # Use WhiteNoise also during runserver (disables Django's static handler)
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "blog.apps.BlogConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise must be right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Global templates directory
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# No database usage at all — dummy backend will raise if accidentally used
DATABASES = {
    "default": {"ENGINE": "django.db.backends.dummy"}
}

# Static files (served by WhiteNoise)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]          # where we keep our assets in dev
STATIC_ROOT = BASE_DIR / "staticfiles"            # collectstatic target for prod
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Locale / timezone
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

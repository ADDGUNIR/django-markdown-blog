from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "blog"

    def ready(self):
        # Import inside ready to avoid side effects during app registry
        from .posts_repository import get_repository
        repo = get_repository()
        # Ensure posts are loaded at startup; idempotent and safe for dev reloads
        repo.reload()

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml
import markdown
from django.conf import settings

# Data model for in-memory posts
@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    date: datetime
    summary: str
    hero_image: Optional[str]
    content_html: str

class PostsRepository:
    """
    Loads Markdown files with YAML front-matter into memory, validates them,
    and exposes read-only access by slug and listing sorted by date (desc).
    """
    def __init__(self, posts_dir: Path):
        self._posts_dir = posts_dir
        self._by_slug: Dict[str, Post] = {}
        self._sorted: List[Post] = []
        self._last_loaded: Optional[datetime] = None

    @property
    def last_loaded(self) -> Optional[datetime]:
        return self._last_loaded

    def all_posts(self) -> List[Post]:
        if not self._sorted:
            self.reload()
        return self._sorted

    def get_by_slug(self, slug: str) -> Optional[Post]:
        if not self._by_slug:
            self.reload()
        return self._by_slug.get(slug)

    def reload(self) -> None:
        files = sorted(self._posts_dir.glob("*.md"))
        by_slug: Dict[str, Post] = {}

        md = markdown.Markdown(extensions=["extra"])

        for f in files:
            text = f.read_text(encoding="utf-8")
            fm, body = self._split_front_matter(text)
            meta = yaml.safe_load(fm) if fm.strip() else {}

            # Mandatory fields
            title = self._require_str(meta, "title", f)
            slug = meta.get("slug") or f.stem
            slug = self._normalize_slug(slug, f)

            # Optional fields
            date_str = meta.get("date") or "1970-01-01"
            date = self._parse_date(date_str, f)
            summary = meta.get("summary") or self._make_excerpt(body, max_words=40)
            hero = meta.get("image")  # e.g. "img/sample1.jpg" under /static/

            # Convert Markdown body to HTML
            content_html = md.convert(body)

            post = Post(
                slug=slug,
                title=title,
                date=date,
                summary=summary,
                hero_image=hero,
                content_html=content_html,
            )

            if slug in by_slug:
                raise ValueError(f"Duplicate slug '{slug}' in file {f}")
            by_slug[slug] = post
            md.reset()  # reset markdown state between documents

        # Sort newest first
        sorted_posts = sorted(by_slug.values(), key=lambda p: p.date, reverse=True)

        self._by_slug = by_slug
        self._sorted = sorted_posts
        self._last_loaded = datetime.now()

    # ----------------- helpers -----------------

    def _split_front_matter(self, text: str) -> (str, str):
        """
        Extract front-matter delimited by leading '---' ... '---'.
        Returns (yaml_text, markdown_body). If no FM, returns ("", text).
        """
        if text.startswith("---"):
            # Find the second delimiter
            m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
            if not m:
                raise ValueError("Front-matter start found but closing '---' missing.")
            return m.group(1), m.group(2)
        return "", text

    def _require_str(self, meta: dict, key: str, file_path: Path) -> str:
        val = meta.get(key)
        if not isinstance(val, str) or not val.strip():
            raise ValueError(f"Missing or invalid '{key}' in {file_path.name}")
        return val.strip()

    def _normalize_slug(self, slug: str, file_path: Path) -> str:
        s = slug.strip().lower()
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s):
            raise ValueError(
                f"Invalid slug '{slug}' in {file_path.name} "
                "(use lowercase letters, numbers, and hyphens)"
            )
        return s

    def _parse_date(self, value: str, file_path: Path) -> datetime:
        try:
            # Accept ISO dates or datetimes; store as datetime for sorting
            return datetime.fromisoformat(value)
        except Exception as e:
            raise ValueError(f"Invalid date '{value}' in {file_path.name}: {e}")

    def _make_excerpt(self, md_body: str, max_words: int = 40) -> str:
        # Very simple excerpt: first N words of the raw markdown (without FM)
        words = re.findall(r"\w[\w'-]*", md_body)
        excerpt = " ".join(words[:max_words])
        if len(words) > max_words:
            excerpt += "..."
        return excerpt

# Singleton-style repository
_repo_singleton: Optional[PostsRepository] = None

def get_repository() -> PostsRepository:
    global _repo_singleton
    if _repo_singleton is None:
        posts_dir = Path(settings.BASE_DIR) / "content" / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)
        _repo_singleton = PostsRepository(posts_dir=posts_dir)
    return _repo_singleton

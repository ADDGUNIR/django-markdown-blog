from django.http import Http404
from django.shortcuts import render
from .posts_repository import get_repository

def index(request):
    repo = get_repository()
    posts = repo.all_posts()
    # Render all posts on index; template will show cards with summary
    return render(request, "index.html", {"posts": posts})

def post_detail(request, slug: str):
    repo = get_repository()
    post = repo.get_by_slug(slug)
    if not post:
        raise Http404("Post not found")
    return render(request, "post_detail.html", {"post": post})

"""A public, paginated feed; only authenticated users may create posts."""

from datetime import datetime, timezone

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db

bp = Blueprint("posts", __name__)


@bp.app_template_filter("utc_date")
def utc_date(value):
    return datetime.fromisoformat(value).astimezone(timezone.utc).strftime("%d %b %Y, %H:%M UTC")


@bp.get("/")
def feed():
    # Bound user-controlled offsets so SQLite never receives an oversized integer.
    page = max(1, min(request.args.get("page", 1, type=int), 2_147_483_647))
    page_size = current_app.config["POSTS_PER_PAGE"]
    # One extra result tells us whether to show an Older posts link.
    rows = get_db().execute(
        "SELECT p.id, p.content, p.created_at, u.username "
        "FROM posts AS p JOIN users AS u ON p.author_id = u.id "
        "ORDER BY p.created_at DESC, p.id DESC LIMIT ? OFFSET ?",
        (page_size + 1, (page - 1) * page_size),
    ).fetchall()
    return render_template(
        "feed.html", posts=rows[:page_size], page=page, has_older=len(rows) > page_size,
    )


@bp.post("/posts")
@login_required
def create_post():
    content = request.form.get("content", "").strip()
    if not 1 <= len(content) <= 280:
        flash("Write a post with 1-280 characters. A blank post cannot be published.", "error")
        return redirect(url_for("posts.feed"))
    database = get_db()
    database.execute(
        "INSERT INTO posts (author_id, content, created_at) VALUES (?, ?, ?)",
        (g.user["id"], content, datetime.now(timezone.utc).isoformat()),
    )
    database.commit()
    flash("Your post has been published.", "success")
    return redirect(url_for("posts.feed"))

import sqlite3

import pytest

from app import create_app
from app.db import get_db
from conftest import token_from


def test_public_feed_is_accessible_without_login(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Community feed" in response.data
    assert b"No posts here yet" in response.data


def test_unauthenticated_user_cannot_create_post(app, client):
    response = client.post("/posts", data={
        "csrf_token": token_from(client.get("/login")), "content": "Unauthorized",
    })
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0


def test_post_is_persisted_and_shows_author_text_and_utc_date(app, client, auth):
    auth.register()
    auth.login()
    response = auth.post("  My first workshop post!  ")
    assert response.status_code == 200
    assert b"@alice" in response.data
    assert b"My first workshop post!" in response.data
    assert b"UTC" in response.data
    with app.app_context():
        post = get_db().execute("SELECT * FROM posts").fetchone()
        assert post["content"] == "My first workshop post!"
        assert post["author_id"] == 1
        assert post["created_at"].endswith("+00:00")


@pytest.mark.parametrize("content", ["", "   ", "\n\t", "a" * 281])
def test_invalid_posts_are_not_saved(app, auth, content):
    auth.register()
    auth.login()
    response = auth.post(content)
    assert b"A blank post cannot be published" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0


@pytest.mark.parametrize("content", ["a", "a" * 280, "Hello, 世界 👋"])
def test_post_boundaries_and_unicode_are_supported(app, auth, content):
    auth.register()
    auth.login()
    auth.post(content)
    with app.app_context():
        assert get_db().execute("SELECT content FROM posts").fetchone()[0] == content


def test_feed_contains_all_users_and_is_newest_first(client, auth):
    auth.register("alice")
    auth.login("alice")
    auth.post("Earlier post from Alice")
    auth.logout()
    auth.register("bob")
    auth.login("bob")
    auth.post("Later post from Bob")
    auth.logout()
    html = client.get("/").get_data(as_text=True)
    assert "@alice" in html and "@bob" in html
    assert html.index("Later post from Bob") < html.index("Earlier post from Alice")


def test_post_author_is_taken_from_session(app, auth):
    auth.register("alice")
    auth.register("bob")
    auth.login("alice")
    auth.post("Cannot impersonate Bob", author_id="2")
    with app.app_context():
        assert get_db().execute("SELECT author_id FROM posts").fetchone()[0] == 1


def test_html_is_escaped_and_sql_text_does_not_change_schema(app, auth):
    auth.register()
    auth.login()
    response = auth.post("<script>alert('x')</script> DROP TABLE users;")
    assert b"<script>alert" not in response.data
    assert b"&lt;script&gt;" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1


def test_pagination_preserves_order_and_can_reach_older_posts(app, client, auth):
    auth.register()
    with app.app_context():
        db = get_db()
        # Same timestamp also checks the descending-ID tie breaker.
        db.executemany(
            "INSERT INTO posts (author_id, content, created_at) VALUES (1, ?, ?)",
            [(f"Post number {number:02d}", "2026-01-01T12:00:00+00:00") for number in range(25)],
        )
        db.commit()
    first = client.get("/").get_data(as_text=True)
    second = client.get("/?page=2").get_data(as_text=True)
    assert first.count('<article class="card post">') == 20
    assert second.count('<article class="card post">') == 5
    assert "Post number 24" in first and "Post number 04" not in first
    assert "Post number 04" in second and "Post number 24" not in second
    assert first.index("Post number 24") < first.index("Post number 23")


@pytest.mark.parametrize("query", ["?page=oops", "?page=-1", "?page=" + "9" * 100])
def test_invalid_page_parameters_have_safe_defaults(client, query):
    assert client.get("/" + query).status_code == 200


def test_users_posts_and_login_survive_application_recreation(app, auth):
    auth.register()
    auth.login()
    auth.post("This survives a restart")
    restarted = create_app({
        "TESTING": True, "DATABASE": app.config["DATABASE"],
        "SECRET_KEY": app.config["SECRET_KEY"],
    })
    new_client = restarted.test_client()
    assert b"This survives a restart" in new_client.get("/").data
    login = new_client.post("/login", data={
        "csrf_token": token_from(new_client.get("/login")),
        "username": "alice", "password": "learning-python-is-fun-2026",
    })
    assert login.status_code == 302


def test_foreign_key_prevents_post_for_nonexistent_user(app):
    with app.app_context():
        with pytest.raises(sqlite3.IntegrityError):
            get_db().execute(
                "INSERT INTO posts (author_id, content, created_at) VALUES (?, ?, ?)",
                (999, "orphan post", "2026-01-01T12:00:00+00:00"),
            )

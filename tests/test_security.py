import pytest

from app import create_app


@pytest.mark.parametrize("path", ["/register", "/login", "/posts", "/logout"])
def test_post_without_csrf_token_is_rejected(client, path):
    assert client.post(path, data={}).status_code == 400


def test_fake_csrf_token_is_rejected(client):
    response = client.post("/register", data={"csrf_token": "fake-token"})
    assert response.status_code == 400


def test_session_cookie_and_security_headers(client):
    response = client.get("/login")
    cookie = response.headers.get("Set-Cookie", "")
    assert "HttpOnly" in cookie and "SameSite=Lax" in cookie
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "form-action 'self'" in response.headers["Content-Security-Policy"]


def test_overlarge_request_is_rejected(client):
    assert client.post("/posts", data={"content": "a" * 20000}).status_code == 413


def test_generated_secret_is_persisted(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.delenv("SECRET_KEY", raising=False)
    first = create_app({"TESTING": True})
    second = create_app({"TESTING": True})
    assert len(first.config["SECRET_KEY"]) == 64
    assert first.config["SECRET_KEY"] == second.config["SECRET_KEY"]
    assert (tmp_path / "session.key").exists()


def test_session_for_deleted_user_cannot_publish(app, client, auth):
    from app.db import get_db
    from conftest import token_from

    auth.register()
    auth.login()
    with app.app_context():
        get_db().execute("DELETE FROM users")
        get_db().commit()
    response = client.post("/posts", data={
        "csrf_token": token_from(client.get("/login")), "content": "Invalid user",
    })
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "user_id" not in session

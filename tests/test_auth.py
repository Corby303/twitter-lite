import pytest

from app.db import get_db
from conftest import PASSWORD, token_from


def test_register_stores_verifiable_argon2id_hash(app, auth):
    response = auth.register("Alice")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
    with app.app_context():
        user = get_db().execute("SELECT * FROM users").fetchone()
        assert user["username"] == "alice"
        assert user["password_hash"].startswith("$argon2id$v=19$m=19456,t=2,p=1$")
        assert PASSWORD not in user["password_hash"]
        assert app.extensions["password_hasher"].verify(user["password_hash"], PASSWORD)


def test_same_password_has_different_salted_hashes(app, auth):
    auth.register("alice")
    auth.register("bob")
    with app.app_context():
        hashes = [row[0] for row in get_db().execute("SELECT password_hash FROM users")]
        assert len(hashes) == 2 and hashes[0] != hashes[1]


def test_duplicate_usernames_are_case_insensitive(app, auth):
    auth.register("alice")
    response = auth.register("ALICE")
    assert response.status_code == 400
    assert b"already taken" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1


@pytest.mark.parametrize("username", ["", "ab", "a" * 31, "name with spaces", "<script>"])
def test_invalid_username_is_rejected(app, auth, username):
    assert auth.register(username).status_code == 400
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0


@pytest.mark.parametrize("password", ["", "short", "a" * 14, "a" * 129])
def test_invalid_password_length_is_rejected(auth, password):
    assert auth.register(password=password).status_code == 400


@pytest.mark.parametrize("password", ["a" * 15, "a" * 128])
def test_password_length_boundaries_are_accepted(auth, password):
    assert auth.register(password=password).status_code == 302
    assert auth.login(password=password).status_code == 302


def test_password_confirmation_is_required(auth):
    response = auth.register(confirmation="different-passphrase")
    assert response.status_code == 400
    assert b"do not match" in response.data


def test_login_and_logout_change_authentication_state(client, auth):
    auth.register()
    assert auth.login("ALICE").status_code == 302
    with client.session_transaction() as session:
        assert session["user_id"] == 1
    assert auth.logout().status_code == 302
    with client.session_transaction() as session:
        assert "user_id" not in session
    response = client.post("/posts", data={
        "csrf_token": token_from(client.get("/login")), "content": "After logout",
    })
    assert response.status_code == 302 and response.headers["Location"].endswith("/login")


@pytest.mark.parametrize("username,password", [
    ("alice", "wrong-long-passphrase"), ("unknown", PASSWORD),
    ("' OR 1=1 --", PASSWORD),
])
def test_failed_login_does_not_create_authenticated_session(client, auth, username, password):
    auth.register()
    response = auth.login(username, password)
    assert response.status_code == 400
    assert b"Incorrect username or password" in response.data
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_password_is_not_echoed_in_error_page(auth):
    response = auth.register(confirmation="not-the-same-password")
    assert PASSWORD.encode() not in response.data


def test_logout_requires_post(client):
    assert client.get("/logout").status_code == 405

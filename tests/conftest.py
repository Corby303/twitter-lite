import re

import pytest

from app import create_app

PASSWORD = "learning-python-is-fun-2026"


def token_from(response):
    match = re.search(r'name="csrf_token" value="([^"]+)"', response.get_data(as_text=True))
    assert match is not None, "A state-changing form must contain a CSRF token"
    return match.group(1)


@pytest.fixture
def app(tmp_path):
    return create_app({
        "TESTING": True,
        "DATABASE": str(tmp_path / "test.sqlite3"),
        "SECRET_KEY": "test-key-only-never-use-in-a-real-deployment",
    })


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    class Auth:
        def register(self, username="alice", password=PASSWORD, confirmation=None):
            return client.post("/register", data={
                "csrf_token": token_from(client.get("/register")),
                "username": username,
                "password": password,
                "confirm_password": password if confirmation is None else confirmation,
            })

        def login(self, username="alice", password=PASSWORD):
            return client.post("/login", data={
                "csrf_token": token_from(client.get("/login")),
                "username": username, "password": password,
            })

        def logout(self):
            return client.post("/logout", data={"csrf_token": token_from(client.get("/"))})

        def post(self, content, **extra):
            return client.post("/posts", data={
                "csrf_token": token_from(client.get("/")), "content": content, **extra,
            }, follow_redirects=True)
    return Auth()

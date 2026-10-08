"""Real HTTP journeys and container-recreation persistence checks for CI.

Uses Python's standard library. Run only after `docker compose up -d --wait`.
Creates a temporary demonstration account and leaves its post in the database.
"""

import html
import http.cookiejar
import re
import secrets
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8000"


def main():
    cookies = http.cookiejar.CookieJar()
    browser = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))

    def get(path):
        with browser.open(BASE + path, timeout=10) as response:
            return response.read().decode()

    def post(path, form_path, data):
        match = re.search(r'name="csrf_token" value="([^"]+)"', get(form_path))
        assert match, "CSRF token missing"
        data = {**data, "csrf_token": html.unescape(match.group(1))}
        with browser.open(
            BASE + path, urllib.parse.urlencode(data).encode(), timeout=10
        ) as response:
            return response.read().decode()

    username = "smoke_" + secrets.token_hex(4)
    password = secrets.token_urlsafe(24)
    content = "Docker persistence check " + secrets.token_hex(8)
    post("/register", "/register", {
        "username": username, "password": password, "confirm_password": password,
    })
    post("/login", "/login", {"username": username, "password": password})
    feed = post("/posts", "/", {"content": content})
    assert content in feed and "@" + username in feed and "UTC" in feed
    post("/logout", "/", {})
    assert content in get("/")

    # Remove and recreate the container while keeping its named volume.
    subprocess.run(["docker", "compose", "down"], check=True)
    subprocess.run([
        "docker", "compose", "up", "-d", "--wait", "--wait-timeout", "90",
    ], check=True)
    deadline = time.monotonic() + 20
    while True:
        try:
            feed = get("/")
            break
        except (urllib.error.URLError, TimeoutError):
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.5)
    assert content in feed, "Post disappeared after container recreation"
    post("/login", "/login", {"username": username, "password": password})
    assert "Sign out" in get("/"), "Persisted account could not log in"
    print("PASS: register, login, publish, public feed, logout and Docker persistence")


if __name__ == "__main__":
    main()

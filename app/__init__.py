"""Application factory: configuration, security and startup live here."""

import os
import secrets
from datetime import timedelta
from pathlib import Path

from argon2 import PasswordHasher
from argon2.low_level import Type
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError, CSRFProtect

csrf = CSRFProtect()


def _local_secret(data_dir):
    """Keep a random signing key outside source control and across restarts."""
    key_file = Path(data_dir) / "session.key"
    if not key_file.exists():
        key_file.write_text(secrets.token_hex(32), encoding="utf-8")
        key_file.chmod(0o600)
    return key_file.read_text(encoding="utf-8").strip()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    data_dir = Path(os.environ.get("DATA_DIR", app.instance_path)).resolve()
    app.config.from_mapping(
        DATABASE=str(data_dir / "twitter-lite.sqlite3"),
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SESSION_COOKIE_NAME="twitter_lite_session",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        # Local demonstration uses HTTP. Enable only when serving over HTTPS.
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "false").lower() == "true",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
        SESSION_REFRESH_EACH_REQUEST=False,
        MAX_CONTENT_LENGTH=16 * 1024,
        POSTS_PER_PAGE=20,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    if not app.config["SECRET_KEY"]:
        data_dir.mkdir(parents=True, exist_ok=True)
        app.config["SECRET_KEY"] = _local_secret(data_dir)

    # OWASP minimum Argon2id configuration: 19 MiB, 2 iterations, 1 lane.
    app.extensions["password_hasher"] = PasswordHasher(
        memory_cost=19456, time_cost=2, parallelism=1, type=Type.ID
    )
    # Check an actual hash even for unknown users, reducing a timing difference.
    app.extensions["dummy_password_hash"] = app.extensions["password_hasher"].hash(
        secrets.token_urlsafe(32)
    )
    csrf.init_app(app)

    from . import auth, db, posts

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)
    # CREATE IF NOT EXISTS is deliberately non-destructive.
    with app.app_context():
        db.init_schema()

    @app.get("/health")
    def health():
        db.get_db().execute("SELECT 1").fetchone()
        return {"status": "ok"}

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; "
            "img-src 'self' data:; object-src 'none'; base-uri 'self'; "
            "frame-ancestors 'none'; form-action 'self'"
        )
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(CSRFError)
    def csrf_error(error):
        return render_template(
            "error.html", title="Form expired",
            message="Reload the page and try again. A valid form token is required."
        ), 400

    @app.errorhandler(413)
    def too_large(error):
        return render_template(
            "error.html", title="Request too large",
            message="This request is too large. Posts may contain up to 280 characters."
        ), 413

    return app

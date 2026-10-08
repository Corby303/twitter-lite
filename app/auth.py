"""Register, log in and log out. Never store a plaintext password."""

import re
import sqlite3
from datetime import datetime, timezone
from functools import wraps

from argon2.exceptions import InvalidHashError, VerificationError
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for,
)

from .db import get_db

bp = Blueprint("auth", __name__)
USERNAME = re.compile(r"[a-z0-9_]{3,30}")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = None
    if user_id is not None:
        g.user = get_db().execute(
            "SELECT id, username FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if g.user is None:
            session.clear()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please sign in to continue.", "info")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@bp.route("/register", methods=("GET", "POST"))
def register():
    username = ""
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirm_password", "")
        if not USERNAME.fullmatch(username):
            error = "Use 3-30 letters, numbers or underscores for your username."
        elif not 15 <= len(password) <= 128:
            error = "Use a password or passphrase with 15-128 characters."
        elif password != confirmation:
            error = "The passwords do not match."
        else:
            hasher = current_app.extensions["password_hasher"]
            try:
                database = get_db()
                database.execute(
                    "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                    (username, hasher.hash(password), datetime.now(timezone.utc).isoformat()),
                )
                database.commit()
            except sqlite3.IntegrityError:
                database.rollback()
                error = "That username is already taken. Choose another."
            else:
                flash("Account created. You can now sign in.", "success")
                return redirect(url_for("auth.login"))
    return render_template("register.html", error=error, username=username), (400 if error else 200)


@bp.route("/login", methods=("GET", "POST"))
def login():
    username = ""
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        password_hash = (
            user["password_hash"] if user else current_app.extensions["dummy_password_hash"]
        )
        verified = False
        if 15 <= len(password) <= 128:
            try:
                verified = current_app.extensions["password_hasher"].verify(password_hash, password)
            except (VerificationError, InvalidHashError):
                pass
        if user is None or not verified:
            error = "Incorrect username or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            session.permanent = True
            flash("You are signed in.", "success")
            return redirect(url_for("posts.feed"))
    return render_template("login.html", error=error, username=username), (400 if error else 200)


@bp.post("/logout")
@login_required
def logout():
    session.clear()
    flash("You are signed out.", "success")
    return redirect(url_for("posts.feed"))

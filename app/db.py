"""One SQLite connection per request, with parameterized queries in views."""

import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(exception=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_schema():
    with current_app.open_resource("schema.sql") as schema:
        get_db().executescript(schema.read().decode("utf-8"))


def init_app(app):
    app.teardown_appcontext(close_db)

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL CHECK(length(username) BETWEEN 3 AND 30),
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL REFERENCES users(id),
    content TEXT NOT NULL CHECK(length(content) BETWEEN 1 AND 280),
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS posts_newest ON posts(created_at DESC, id DESC);

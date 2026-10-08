"""Measure a small sequential feed target without changing real app data."""

import math
import statistics
import sys
import tempfile
import time
from pathlib import Path

# Allow running `python scripts/measure_feed.py` from the project folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.db import get_db


def main():
    with tempfile.TemporaryDirectory() as directory:
        app = create_app({
            "TESTING": True, "DATABASE": str(Path(directory) / "measure.sqlite3"),
            "SECRET_KEY": "benchmark-only-key",
        })
        with app.app_context():
            database = get_db()
            database.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                ("benchmark", app.extensions["password_hasher"].hash("benchmark-test-passphrase"),
                 "2026-01-01T00:00:00+00:00"),
            )
            database.executemany(
                "INSERT INTO posts (author_id, content, created_at) VALUES (1, ?, ?)",
                [(f"Benchmark post {i}", "2026-01-01T00:00:00+00:00") for i in range(1000)],
            )
            database.commit()
        client = app.test_client()
        samples = []
        for _ in range(20):
            start = time.perf_counter()
            response = client.get("/")
            samples.append(time.perf_counter() - start)
            assert response.status_code == 200
            assert response.data.count(b'<article class="card post">') == 20
        p95 = sorted(samples)[math.ceil(len(samples) * .95) - 1]
        print("Dataset: 1,000 posts; requests: 20 sequential; Flask test client")
        print(f"Median: {statistics.median(samples):.4f}s; nearest-rank p95: {p95:.4f}s")
        print("Target p95 < 2s:", "PASS" if p95 < 2 else "FAIL")
        print("This is a local rendering check, not a concurrent HTTP load test.")


if __name__ == "__main__":
    main()

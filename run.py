"""Run locally on Windows, macOS or Linux using the Waitress WSGI server."""

import os

from waitress import serve

from app import create_app

if __name__ == "__main__":
    serve(
        create_app(), host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")), threads=4,
    )

# Twitter Lite - Software Engineering Workshop

A Python/Flask social-media MVP for the supplied student assessment. It has
registration, login/logout, a public feed and authenticated post creation.
Posts display the author, text and UTC creation time, newest first.

## Technology and scope

- Python 3.12, Flask and Jinja templates; plain HTML/CSS frontend.
- SQLite through Python's built-in `sqlite3` module.
- Argon2id passwords through `argon2-cffi`; signed Flask session cookies.
- Flask-WTF CSRF protection; Waitress application server.
- pytest tests, Docker Compose and GitHub Actions CI.

The web server and application are one monolith. SQLite is appropriate for this
small local MVP; writes are serialized, so it is not a high-traffic architecture.
The feed is public; only registered, signed-in users can publish. Posts have
1-280 characters, after trimming outside whitespace. All posts are reachable
through pages of 20, rather than loading the entire database at once.

## Run with Docker (required assessment demonstration)

Prerequisites: Git, Docker Engine/Docker Desktop running Linux containers, and
Docker Compose v2 supporting `--wait`. Windows Docker Desktop normally uses
WSL 2. Internet access is needed for the first image/dependency download.

After cloning your own repository, or extracting the supplied project:

```sh
cd twitter-lite
docker compose up --build
```

Open **http://localhost:8000**. Register a new username and a passphrase of at
least 15 characters; sign in and publish a post. No seed credentials are shipped.
The database and tables are created automatically. There is no migration or
seed command required for this initial schema, and no `.env` file is needed.

To run in the background and wait for readiness:

```sh
docker compose up --build -d --wait
docker compose ps
docker compose logs web
```

To stop while retaining data:

```sh
docker compose down
```

**Do not use `docker compose down -v` during the persistence demo:** `-v` deletes
the named data volume. It is an intentional database reset, not an ordinary stop.

### Prove persistence manually

1. Register, log in and publish a distinctive post.
2. Run `docker compose restart web`. Refresh the page: the post remains.
3. Run `docker compose down`, then `docker compose up -d --wait`.
4. Refresh: the post remains, and the existing account can still sign in.
5. Capture real screenshots/logs for [docs/evidence-checklist.md](docs/evidence-checklist.md).

The named volume `twitter-lite-data` mounts at `/data`. Both the SQLite file and
the randomly generated session-signing key live there. Deleting the volume,
changing to a different Compose project name, or switching to the separate
non-Docker database can make the app appear empty.

## Run without Docker (useful for learning and editing)

Install Python **3.12**, then use a virtual environment.

Windows PowerShell, from the project folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe run.py
```

Using the virtual environment's Python directly avoids PowerShell activation
policy problems. Open http://localhost:8000. Press Ctrl+C to stop the server.

macOS/Linux:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python run.py
```

Local data goes into `instance/`; Docker data goes into its named volume. These
are different databases. Both are excluded from Git and the Docker build.

## Environment variables

These are optional. `run.py` reads actual process environment variables; it does
not automatically load a `.env` file.

| Variable | Local default | Purpose / safe example |
|---|---|---|
| `DATA_DIR` | Project `instance/` folder | Directory containing the database and generated key. Docker sets `/data`. |
| `HOST` | `127.0.0.1` | Listen address. Container uses `0.0.0.0`; Compose exposes it only on host loopback. |
| `PORT` | `8000` | Server port. Example: `8001` for local Python runs. |
| `SECRET_KEY` | Random key generated on first start and saved outside code | Optional override. Generate your own; never commit or share it. |
| `COOKIE_SECURE` | `false` | Set `true` only behind correctly configured HTTPS. Local HTTP needs `false`. |

If an explicit key is needed, generate it locally with:

```sh
python -c "import secrets; print(secrets.token_hex(32))"
```

Do not put that output in the repository, screenshots or assessment documents.
The automatic persistent key is sufficient for the local assignment.

## Test commands

After installing `requirements-dev.txt`:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

macOS/Linux: `.venv/bin/python -m pytest -q`.

Tests use temporary SQLite databases and keep CSRF protection enabled. They
cover valid and invalid accounts, salted hashes, login/logout, authorization,
post limits, all-user feed ordering, pagination, XSS escaping, SQL text, foreign
keys and application recreation without data loss.

With Docker running, exercise real HTTP requests and container recreation:

```powershell
.\.venv\Scripts\python.exe scripts/docker_smoke.py
```

This script creates a generated test account and post, stops/recreates the
container, then verifies that both survived. It leaves that account/post behind.
Do not run it during a presentation if stopping the app would interrupt you.

To measure the local feed target: `python scripts/measure_feed.py` using your
virtual-environment interpreter. It uses a temporary database and reports a
small sequential benchmark, not concurrent load capacity.

## CI

`.github/workflows/ci.yml` runs on pushes, pull requests and manual dispatches.
It installs dependencies, runs pytest, builds the container, starts Compose,
checks its health and runs the HTTP/persistence smoke test. It builds without
publishing an image or deploying a site. CD/production publishing is optional
in the assessment; CI plus the local Docker demonstration meets that scope.

Push the project to **your own GitHub repository**, then open **Actions**. A
workflow file existing in a ZIP is not evidence of a successful CI run. Keep the
URL of your actual green run and record its commit SHA.

## Project files

| Path | Purpose |
|---|---|
| `app/__init__.py` | App factory, configuration, CSRF and security headers |
| `app/auth.py` | Registration, login, logout and authentication checks |
| `app/posts.py` | Feed and post creation |
| `app/db.py`, `app/schema.sql` | SQLite connection and database tables |
| `app/templates/`, `app/static/` | HTML pages and stylesheet |
| `tests/` | Automated acceptance/security tests |
| `Dockerfile`, `compose.yaml` | Container build and persistent local run |
| `.github/workflows/ci.yml` | Automated tests, Docker build and smoke checks |
| `docs/requirements.md` | Part A: IDs, assumptions and acceptance criteria |
| `docs/methodology.md` | Part B: Kanban justification and delivery approach |
| `docs/backlog.md`, `docs/board-guide.md` | Part C: stories, tasks and board instructions |
| `docs/architecture.md`, `docs/adr/` | Part D: architecture, database and decisions |
| `docs/test-plan.md` | Manual/automated validation and traceability |
| `docs/evidence-checklist.md` | Real evidence still needed for submission |
| `docs/presentation-outline.md` | Timed plan for the 10-minute presentation |
| `docs/verification.md` | What was actually checked in the preparation environment |

## Troubleshooting

| Symptom | Action |
|---|---|
| Docker daemon connection error | Open Docker Desktop, wait for it to start, then retry. Use Linux containers. |
| WSL/virtualization error on Windows | Follow Docker's Windows prerequisites; enable supported WSL 2/virtualization. |
| Port 8000 already allocated | Stop another app on 8000, or change the left-hand Compose port to `127.0.0.1:8001:8000` and browse to 8001. The smoke script expects 8000. |
| `py -3.12` cannot find Python | Install Python 3.12, then reopen the VS Code terminal. Docker mode does not need a host Python installation. |
| `No module named flask` | Use the `.venv` Python commands above and install requirements with that same interpreter. |
| Form expired / CSRF error | Reload the page and retry; a form token may expire or belong to a different session. |
| Username already taken | Pick a different username, or sign into the existing account. |
| Existing posts appear missing | Check Docker vs local Python databases, volume retention and Compose project name. |
| CI fails | Open the failing Actions step; fix the actual error, commit, push and capture the successful rerun. |

## Deliberate limitations

This local MVP omits follows, likes, replies, media, editing/deleting posts,
search, password reset and email verification. It has no login rate limiting,
moderation or breached-password checking. Signed cookie sessions expire after
one hour; logout clears this browser's session, but does not centrally revoke a
previously stolen cookie. A publicly deployed version would need HTTPS,
server-side revocable sessions and additional abuse controls. Schema changes
would need a migration strategy; initial startup only creates missing tables.

## Primary technical references

- [Flask database tutorial](https://flask.palletsprojects.com/en/stable/tutorial/database/)
- [Flask-WTF CSRF documentation](https://flask-wtf.readthedocs.io/en/1.2.x/csrf/)
- [argon2-cffi password hashing](https://argon2-cffi.readthedocs.io/en/stable/howto.html)
- [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [OWASP authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Docker Compose quickstart and volumes](https://docs.docker.com/compose/gettingstarted/)
- [GitHub Python CI guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [GitHub Projects creation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project)

# Start here: complete your assignment step by step

You are building a small Twitter-style website and showing how you engineered
it. The deliverable is more than code: you need requirements, planning, design,
Git history, tests, Docker and CI evidence, followed by a 10-minute demo.

This pack supplies working reference code and draft documents. Your next work
is to understand it, adopt or change the decisions, track your real reviews and
changes, run it yourself and collect evidence. Do not submit the drafts unchanged
as if they documented work you have already performed.

## 1. Prepare your computer

Install **VS Code**, **Git**, **Python 3.12** and **Docker Desktop**. For Windows,
follow Docker's WSL 2 requirements and use Linux containers. Official pages:

- https://code.visualstudio.com/
- https://git-scm.com/downloads
- https://www.python.org/downloads/
- https://docs.docker.com/desktop/setup/install/windows-install/

Docker Desktop already includes Compose. XAMPP/phpMyAdmin is not required;
this project uses SQLite instead of MySQL.

Extract the ZIP. You should have a folder called `twitter-lite` containing
`README.md`, `run.py`, `Dockerfile` and `compose.yaml`. Open **that folder** in
VS Code using **File > Open Folder**. Choose **Terminal > New Terminal**.
Check that the terminal is inside the folder containing those files.

## 2. First make the app run

In a Windows PowerShell terminal:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe run.py
```

Open http://localhost:8000. An empty feed is normal on the first run.

1. Click **Create account**.
2. Enter a username and your own passphrase of at least 15 characters.
3. Sign in with the new account.
4. Write and publish a short post.
5. Sign out; the post remains publicly visible.
6. Create a second account and publish another post. Check that both authors
   appear and the second post appears first.

Press Ctrl+C in the terminal to stop the app. Restart it with `run.py`; the
account and posts remain. This checks the Python app; you still need to do the
Docker demonstration later.

If you only want to run Docker first, start Docker Desktop and enter
`docker compose up --build`, then open the same URL. Do not run Python and Docker
on port 8000 at the same time.

## 3. Read and explain the code

Read in this order:

1. `app/schema.sql`: a user has an ID, username and password hash. A post has
   an author ID that refers to a user, its text and its creation time.
2. `app/db.py`: connects to SQLite and enables foreign key constraints.
3. `app/auth.py`: registers users, hashes passwords and checks login details.
4. `app/posts.py`: uses the signed-in user as the author and sorts the feed.
5. `app/templates/`: renders the HTML; Jinja escapes submitted text.
6. `app/__init__.py`: configures the app, sessions, CSRF and startup.
7. `tests/`: demonstrates which requirements the tests verify.
8. `Dockerfile`, `compose.yaml`, `.github/workflows/ci.yml`: build, persist data
   and automate checks.

Make a real improvement you can explain, such as a different post limit with
matching tests/docs, an improved form error message, or a simple profile name.
Keep the required MVP working. Do not add difficult extras before the mandatory
features and engineering evidence are complete.

## 4. Complete Parts A, B and D

Open and edit the Markdown documents in VS Code. Press **Ctrl+Shift+V** to
preview a Markdown document.

| Assessment part | File to review/adapt | What you must be able to explain |
|---|---|---|
| A: Requirements | `docs/requirements.md` | Functional vs non-functional requirements, assumptions and testable criteria |
| B: Methodology | `docs/methodology.md` | Why Kanban fits your team and how you prioritized/reviewed work |
| D: Design | `docs/architecture.md`, `docs/adr/` | Why a monolith, SQLite and these authentication choices fit the MVP |

These are written documents; they are not extra features to implement in the
app. The architecture document includes Mermaid diagrams that GitHub renders.
The brief does not prescribe a report format; confirm any separate lecturer
instructions before choosing whether to submit Markdown or an exported report.

## 5. Put the project on GitHub (Part E)

1. Sign in to GitHub. Create a new repository named `twitter-lite`.
2. Choose public, or private if your lecturer can access it. **Do not** initialize
   it with a README, license or gitignore because the local folder has its own.
3. In the VS Code terminal inside `twitter-lite`, run:

```powershell
git init
git add .
git status
git commit -m "chore: add reviewed AI-assisted project baseline"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/twitter-lite.git
git push -u origin main
```

Replace `YOUR-USERNAME` before running the remote command. If Git requests your
name/email, configure your own values as instructed by Git. Authenticate through
the supported GitHub browser/credential-manager flow; an account password is not
used as a Git HTTPS password.

Check `git status` before committing: `.venv`, `instance`, database files and
keys must not be staged. Keep the first commit honest about the supplied pack.
Then make meaningful commits as you actually review/change things, for example
`docs: confirm public feed assumption` or `fix: clarify post validation error`.
Do not manufacture a history of steps you did not take.

To push later work:

```powershell
git add .
git diff --cached
git commit -m "YOUR MEANINGFUL DESCRIPTION"
git push
```

## 6. Create and maintain the board (Part C)

Follow `docs/board-guide.md`. Create a GitHub Project with a board view and:

**Backlog > To Do > In Progress > Review / Testing > Done**

Create issues from `docs/backlog.md`, with the story ID, description, acceptance
criteria and priority. Add them to the board. Track your genuine reviews,
adaptations, tests and fixes; link commits and test evidence in issue comments.
The supplied backlog is a plan, not proof of board usage. Save screenshots as
the board changes. Keep assessment access enabled for both repository and board.

## 7. Run tests and Docker (Parts E and F)

Stop the Python server first, then run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
docker compose up --build -d --wait
docker compose ps
.\.venv\Scripts\python.exe scripts/docker_smoke.py
```

The smoke script checks actual browser-style requests and removes/recreates the
container while keeping its volume. For a manual demonstration, publish a post,
run `docker compose down`, run `docker compose up -d --wait`, then show the post
and account still exist. Do not use `down -v`, which deletes the data.

You can use Docker for the whole app without installing Python. Host Python is
only needed here to run tests and the separate smoke script locally.

## 8. Capture real CI evidence

Push the files to GitHub. Open the repository's **Actions** tab and select
**Test and build MVP**. The workflow should install packages, run tests, build
Docker and check HTTP/persistence automatically. If it fails, inspect the failed
step and fix it. Save the successful run URL and its commit SHA.

Use `docs/evidence-checklist.md` to record the repository URL, board URL,
screenshots and run result. Nothing in this pack claims that your GitHub CI has
already succeeded.

## 9. Prepare the presentation and submit

Use `docs/presentation-outline.md` to rehearse a 10-minute presentation. Submit
the repository URL, reviewed engineering documents, board access/evidence and
real CI evidence. Demonstrate the functioning app in Docker. Check every item
against the assessment checklist.

Be ready to answer:

- Why did you choose Kanban and a monolith?
- What distinguishes a requirement from an acceptance criterion?
- Why do you hash passwords rather than encrypt or store them as text?
- Why does the author ID come from the session rather than the submitted form?
- Why does a Docker volume preserve data after removing the container?
- Which tests prove each required user journey?
- What would need to change before a public deployment?

Use `docs/ai-assistance.md` to document assistance in the format required by
your institution, after checking its actual policy.

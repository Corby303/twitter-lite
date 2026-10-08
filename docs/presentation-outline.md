# 10-minute presentation plan

This is a speaking/demo outline, not a claim that the demonstration has happened.
Practice with Docker running and use real repository/board/CI pages.

| Time | Show / explain |
|---|---|
| 0:00-1:00 | Customer needs a lightweight social MVP. State web choice, public feed and text-only scope. |
| 1:00-2:00 | Two example requirements and testable acceptance criteria; explain an assumption. |
| 2:00-3:00 | Actual Kanban board: priorities, WIP rule, one story and its real status/test evidence. |
| 3:00-4:00 | Architecture diagram and ADR: one Flask monolith, SQLite file, persistent volume; explain a trade-off. |
| 4:00-7:00 | Live app: register, sign in, post, show two authors/newest first, sign out and show publishing needs authentication. |
| 7:00-8:15 | Docker command and volume. Stop/recreate container, then show account/post remain. |
| 8:15-9:15 | Genuine green GitHub Actions run; show test and Docker build/smoke steps. |
| 9:15-10:00 | One or two actual lessons/decisions, limitations and sensible future work. |

Total: exactly ten minutes. Have the test output and actual CI run ready so
you do not spend presentation time waiting for builds.

## Before the demo

- Start Docker Desktop; confirm port 8000 is available and the container is healthy.
- Have a second test user/post ready for the all-user feed demonstration.
- Use a unique new username when registering live; do not reveal a real password.
- Keep repository, Project, architecture and CI tabs ready.
- Have genuine screenshots as backup evidence, clearly distinguish them from
  a live demo. Rehearse the down/up step on the actual machine.
- Do not delete the volume. Confirm all assessors can access linked pages.

## Decisions you should be able to defend

- Kanban fits a small team and changing details without pretending to use Scrum.
- A monolith minimizes services for the required scope; module separation still
  helps maintainability.
- SQLite keeps local setup simple but serializes writes.
- Argon2id provides salted adaptive hashing; a session identifies the author.
- Named volumes outlive containers when retained; a container's writable layer
  alone is not an adequate persistence plan.
- CI installs/tests/builds automatically; this project does not need mandatory
  public production deployment.

Use your own explanations and lessons after reviewing/testing the code. Do not
read a fabricated account of work or feedback that did not occur.

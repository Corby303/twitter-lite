# ADR-001 - Monolith with SQLite for the local MVP

**Status:** Proposed for student adoption. Change to Accepted only when you have
reviewed the decision, and record that actual date.

## Context

The client needs registration, authentication, a shared feed and text posting
within a short window. The team has at most two students. The lecturer must run
the entire application locally with Docker. There is no specified scale target,
mobile requirement or need to deploy services independently.

## Decision

Use one Python/Flask application with server-rendered Jinja pages, modular
authentication/post/database code, and SQLite. Run one Waitress process in a
Docker container. Persist the SQLite file and session key in a named volume.

## Alternatives

1. **React + separate REST API + PostgreSQL:** Allows richer client interaction
   and stronger write concurrency, but requires a frontend toolchain, API
   contract and separate service setup. More components than the mandatory MVP
   needs; a reasonable later direction rather than a requirement now.
2. **Microservices for identity/posts/feed:** Independent scaling/deployment,
   but introduces service communication, distributed authentication, operational
   complexity and possibly distributed data consistency. Team/scope do not
   justify that cost.
3. **Monolith with PostgreSQL/MySQL:** Familiar server database with better
   concurrent-write options, but adds a container, credentials and readiness
   management. Useful if the database requirement or scale changes.
4. **In-memory storage:** Simple initially, but fails mandatory persistence.

## Consequences and trade-offs

Positive: fewer moving parts; one-command local run; straightforward tests;
small codebase; easy traceability from forms to handlers/database. A database
server is not needed on the lecturer's machine.

Negative: SQLite serializes writes; a single deployable unit cannot scale
features independently; OFFSET pagination can become expensive for very deep
pages; automatic CREATE IF NOT EXISTS does not migrate changed schemas.

Mitigation: limit feed pages, index ordering, bound page integers, keep SQL/data
access in a small module, and introduce schema migrations before evolving the
database. Reassess PostgreSQL if measured contention or scale requires it.

## Validation

Verify account/post journeys, app recreation with the same file, and actual
Docker container recreation with its retained volume. Record the tests and
Docker evidence in the real issue/checklist; do not infer container success
from unit tests alone.

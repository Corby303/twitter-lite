# Part A - Requirements engineering

**Draft for student review.** Confirm the assumptions with your lecturer/client
where possible and record any changes. Baseline source: the supplied Software
Engineering Workshop student assessment, Parts A-F and minimum checklist.

## Problem and stakeholders

The startup needs a lightweight social platform to demonstrate account creation,
sign-in and posting to investors. Primary stakeholders are the customer/startup,
end users, student developer(s) and the lecturer who must reproduce the local
demonstration. The assessment allows a solo student or a team of up to two.

## Functional requirements

| ID | Requirement | Priority | Testable acceptance criteria |
|---|---|---|---|
| FR-01 | Register an account with a unique username and password. | Must | Given a new valid username and matching 15-128 character passwords, submitting the form stores one account and redirects to sign-in. Duplicate/invalid details produce a useful message and create no account. |
| FR-02 | Sign in using registered credentials. | Must | Correct credentials create an authenticated session and display the feed. Incorrect or unknown credentials show the same generic failure message without authenticating the browser. |
| FR-03 | Sign out. | Must | A signed-in user can submit Sign out. Their browser session loses its user ID and a later publish request requires sign-in. Logout is POST with a valid CSRF token. |
| FR-04 | Show posts from all users. | Must | The public feed contains every author's posts across its pages. Every post displays username, escaped text and UTC creation date/time. Sort by creation timestamp descending, then ID descending for ties. |
| FR-05 | Restrict publishing to authenticated users. | Must | An unauthenticated publish request with a valid form token redirects to sign-in and stores no post. The author comes from the session, ignoring a supplied author ID. |
| FR-06 | Publish a text post. | Must | A signed-in user can submit 1-280 characters after trimming leading/trailing whitespace. The post is saved and appears at the top of the feed. Empty, whitespace-only, over-limit or NUL-containing content creates no post and shows a message. |
| FR-07 | Preserve accounts and posts. | Must | After ordinary app/container restart, and after container removal/recreation with the same named volume retained, the account can sign in and its existing post remains visible. |
| FR-08 | Navigate a paginated feed. | Should | Each page contains at most 20 posts. Older/Newer links reach the remaining posts in the same global order. Invalid page input is handled safely. |

## Non-functional requirements

| ID | Quality requirement | Acceptance criteria / evidence |
|---|---|---|
| NFR-01 | Password storage | SQLite contains salted Argon2id hashes, not plaintext passwords. Use 19 MiB memory, two iterations and one lane. Verify a stored hash with the library and show different hashes for the same password. |
| NFR-02 | Request and session security | State-changing forms require valid CSRF tokens. Session cookies are signed, HttpOnly and SameSite=Lax, with one-hour expiry. Passwords never appear in response HTML or session payloads. |
| NFR-03 | Injection protection | User values are passed as SQL parameters. Jinja escapes post text; an entered script is displayed as text rather than executable markup. Author foreign keys are enforced. |
| NFR-04 | Basic usability | Registration, sign-in and posting have visible labels, readable validation and a clear empty feed. At 375px and 1280px widths, no horizontal page overflow. Core journeys work with keyboard navigation and visible focus. Manual browser verification is required. |
| NFR-05 | Local feed performance | With 1,000 stored posts and 20 sequential first-page requests, nearest-rank p95 server-rendering time is under two seconds on the demo machine. Measure with `scripts/measure_feed.py`; report machine, method and results. This is a small local target, not a promise of concurrent-user capacity. |
| NFR-06 | Reproducibility | From a clean checkout with Docker/Compose available, `docker compose up --build` starts the app at the documented URL without a separate database install or secret in source control. Record the actual Docker run. |
| NFR-07 | Automated quality checks | Every push starts CI that installs pinned dependencies, executes tests and builds the container. A genuine successful run URL and commit SHA must be supplied. |
| NFR-08 | Maintainability | Separate app factory, authentication, posts, database, templates and tests. Documents connect requirements to stories and tests; commits describe actual changes. |
| NFR-09 | Persistent storage safety | The configured Docker named volume holds database and session key. Stopping/recreating containers retains both. README explicitly explains that deleting the volume deletes stored data. |

## Assumptions and decisions requiring review

| ID | Assumption | Reason / implication |
|---|---|---|
| A-01 | A web application is acceptable. | The brief permits web or mobile; browser access simplifies local demonstrations. |
| A-02 | Feed reading is public. | The customer did not state that reading requires login. Publishing remains protected. |
| A-03 | Username/password registration is sufficient; no email address is needed. | Email delivery and verification would add scope without being mandatory. |
| A-04 | Usernames use 3-30 ASCII letters/digits/underscores, normalized to lowercase. | Consistent identity and straightforward uniqueness. Display names and international usernames are future work. |
| A-05 | Posts are text-only and at most 280 Unicode code points on the server. | A reasonable Twitter-lite constraint; the brief does not prescribe a limit. Browser HTML maxlength counts UTF-16 units, so some emoji inputs may hit its limit earlier. |
| A-06 | Creation time is recorded and displayed in UTC. | A consistent time reference; browser-local time formatting is out of scope. |
| A-07 | The dataset and concurrent writes are small. | SQLite avoids another service but serializes writes. A larger deployment would revisit this decision. |
| A-08 | This is a local HTTP demonstration. | Compose binds to loopback. HTTPS and public deployment are optional extensions requiring extra security work. |
| A-09 | Tables are created automatically on first startup. | No seeds/migrations are required for this version. Future schema changes require real migrations. |

## Out of scope

Follows, likes, comments/replies, direct messages, media uploads, search,
editing/deleting posts, password recovery, email verification, moderation,
production hosting, rate limiting and centrally revocable sessions.

The absence of those features is a scope decision, not a claim that they are
unnecessary for a real public social network. Prioritize mandatory functionality
and assessed engineering evidence before adding extras.

## Traceability and validation

See [backlog.md](backlog.md) for prioritized stories and [test-plan.md](test-plan.md)
for requirement-to-test mapping. Actual board and CI evidence belongs in
[evidence-checklist.md](evidence-checklist.md). Record requirement changes with
their reason and affected stories/tests; do not silently change implementation
without updating the matching acceptance criteria.

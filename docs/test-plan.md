# Test plan and traceability

Tests must show behavior, not merely repeat implementation details. The suite
uses temporary SQLite databases and real Flask session/form handling. CSRF
protection is enabled throughout. Run `python -m pytest -q` with the project's
virtual-environment interpreter.

## Automated coverage mapping

| Requirement | Relevant tests / checks |
|---|---|
| FR-01 registration | `test_register_stores_verifiable_argon2id_hash`, duplicate/invalid username and password cases, confirmation and boundary tests |
| FR-02 login | `test_failed_login_does_not_create_authenticated_session`, successful login in session and restart tests |
| FR-03 logout | `test_login_and_logout_change_authentication_state`, `test_logout_requires_post` |
| FR-04 all-user feed/order | `test_feed_contains_all_users_and_is_newest_first`, `test_post_is_persisted_and_shows_author_text_and_utc_date`, pagination tie test |
| FR-05 authorization | `test_unauthenticated_user_cannot_create_post`, `test_post_author_is_taken_from_session`, deleted-user session test |
| FR-06 post validation | `test_invalid_posts_are_not_saved`, `test_post_boundaries_and_unicode_are_supported` |
| FR-07 persistence | `test_users_posts_and_login_survive_application_recreation`; actual Docker recreation in `scripts/docker_smoke.py` |
| FR-08 pagination | `test_pagination_preserves_order_and_can_reach_older_posts`, invalid page parameter cases |
| NFR-01 password security | Argon2 hash verification/settings and distinct-salts tests |
| NFR-02 sessions/CSRF | Missing/fake token tests, cookie flag test, no password echo, logout/session tests |
| NFR-03 injection safety | Escaped script/SQL text test, failed SQL-injection login case, foreign key and author ownership tests |
| NFR-04 usability | Manual browser/keyboard checklist below; automated tests alone do not establish accessibility |
| NFR-05 performance | `scripts/measure_feed.py`; record machine and observed median/p95 |
| NFR-06 Docker setup | Clean checkout/manual Docker run, Compose health check and HTTP smoke script |
| NFR-07 CI | Actual GitHub Actions run URL and commit SHA |
| NFR-08 maintainability | Human code/diff/doc review, traceability and real meaningful commits |
| NFR-09 volume/key | Generated-secret persistence test; Docker recreation and named-volume review |

## Manual checks to perform on the demo computer

| Check | Expected result | Actual result / evidence |
|---|---|---|
| Empty first feed | Clear empty state and route to registration | To be recorded |
| Register valid new user | Success and redirect to sign-in | To be recorded |
| Duplicate user / invalid details | Clear error, no duplicate account | To be recorded |
| Login correct/wrong password | Correct login succeeds; wrong details fail | To be recorded |
| Post valid, blank, over limit | Valid content saved; invalid content rejected | To be recorded |
| Second user posts | Both authors shown, newest post first | To be recorded |
| Signed out publish | Requires login and cannot create a post | To be recorded |
| Text containing HTML | Displayed as text; no executed script | To be recorded |
| Width 375px and 1280px | Readable forms/feed without page overflow | To be recorded |
| Tab/Shift+Tab/Enter | Reach controls, see focus, submit forms | To be recorded |
| Docker restart and down/up | Existing post remains and account can log in | To be recorded |
| Clean clone + README | Startup steps work without missing instructions | To be recorded |
| Green GitHub CI | Tests, container build and smoke steps succeeded | To be recorded |

The browser's maxlength may prevent entering over-limit content normally; the
automated tests send an over-limit HTTP request to confirm server-side checking.
Do not assume client-side checks replace validation on the server.

## Performance method

`scripts/measure_feed.py` inserts 1,000 posts into a temporary database and times
20 sequential first-page GET requests with Flask's test client. Each response
must contain 20 posts. It reports median and nearest-rank p95; target is p95
below two seconds. This excludes network latency and does not simulate concurrent
users. Separately demonstrate actual HTTP/container responsiveness.

## Failure handling

Record the failing requirement/test in the issue, reproduce the problem, fix
the underlying behavior and run the relevant checks. Add a regression test only
where it verifies a real failure mode. Commit the change, link results and move
the item to Done only after its criteria are met.

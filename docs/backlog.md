# Part C - Prioritized backlog and user stories

The 14 backlog items are tracked in [Twitter Lite MVP](https://github.com/users/Corby303/projects/5/views/1), created on
15 October 2026 and linked to `Corby303/twitter-lite`. All items are assigned to
`Corby303`; priorities and statuses below match the verified Project fields.
Statuses reflect current review/adoption and testing of the supplied application.
Personal/manual checks remain pending until performed.

## Summary

| ID | Epic / area | Item | Priority | Current Project status | Requirements |
|---|---|---|---|---|---|
| [EN-01](https://github.com/Corby303/twitter-lite/issues/1) | Foundation | Analyze requirements and confirm assumptions | Must | To Do | All FR/NFR |
| [EN-02](https://github.com/Corby303/twitter-lite/issues/2) | Foundation | Adopt architecture and ADRs | Must | To Do | NFR-06/08/09 |
| [EN-03](https://github.com/Corby303/twitter-lite/issues/3) | Foundation | Set up repository and board | Must | In Progress | NFR-08 |
| [US-01](https://github.com/Corby303/twitter-lite/issues/4) | Identity | Register an account | Must | Review / Testing | FR-01, NFR-01/02 |
| [US-02](https://github.com/Corby303/twitter-lite/issues/5) | Identity | Sign in | Must | Review / Testing | FR-02, NFR-02 |
| [US-03](https://github.com/Corby303/twitter-lite/issues/6) | Identity | Sign out | Must | Review / Testing | FR-03, NFR-02 |
| [US-04](https://github.com/Corby303/twitter-lite/issues/7) | Social posts | View the community feed | Must | Review / Testing | FR-04, NFR-03/04 |
| [US-05](https://github.com/Corby303/twitter-lite/issues/8) | Social posts | Publish a post | Must | Review / Testing | FR-05/06, NFR-02/03 |
| [US-06](https://github.com/Corby303/twitter-lite/issues/9) | Delivery | Preserve users/posts after restart | Must | Review / Testing | FR-07, NFR-09 |
| [EN-04](https://github.com/Corby303/twitter-lite/issues/10) | Quality | Verify acceptance and security behavior | Must | Review / Testing | All FR, NFR-01 to 05 |
| [EN-05](https://github.com/Corby303/twitter-lite/issues/11) | Delivery | Run the app reproducibly with Docker | Must | Review / Testing | NFR-06/09 |
| [EN-06](https://github.com/Corby303/twitter-lite/issues/12) | Delivery | Run automated CI on GitHub | Must | Done | NFR-07 |
| [EN-07](https://github.com/Corby303/twitter-lite/issues/13) | Assessment | Capture evidence and rehearse presentation | Must | To Do | Submission checklist |
| [US-07](https://github.com/Corby303/twitter-lite/issues/14) | Social posts | Navigate older feed posts | Should | Review / Testing | FR-08, NFR-05 |

Each item below includes a description, acceptance criteria and decomposed
tasks. Priority/status are in the table. Add real assignees and links in GitHub.

## EN-01 - Requirements and scope

**Description:** As the customer, I want agreed requirements so the developer
builds the intended MVP rather than guessing silently.

**Acceptance:** Functional/non-functional requirements have unique IDs,
testable criteria and explicit assumptions. Mandatory scope matches the brief;
omissions are explained. Student has reviewed and adopted or changed the draft.

**Tasks:** Read the brief; review each FR/NFR; confirm public feed/post limit;
record decisions; link affected user stories.

## EN-02 - Architecture and ADRs

**Description:** As the developer, I want documented design decisions so the
technology choices and trade-offs are reviewable.

**Acceptance:** Diagram labels browser, Flask components and persistent SQLite
storage; data relationships are shown. At least one ADR records context,
decision, alternatives and trade-offs consistent with the code.

**Tasks:** Review monolith/database ADR; inspect schema; review authentication
ADR; verify diagrams and limitations; adopt or revise decisions.

## EN-03 - GitHub repository and board

**Description:** As the lecturer, I want accessible source and a project board
so I can assess real development and planning evidence.

**Acceptance:** Repository contains organized code/docs/tests and safe ignores;
no secrets/database are committed. Board has the five workflow columns and
prioritized issues with criteria. Meaningful commits and actual status changes
are visible. Assessment access is confirmed.

**Tasks:** Create repo; review ignores; commit honest baseline; create Project;
copy issues; link repo/board; record actual updates as work proceeds.

## US-01 - Register

**Story:** As a new visitor, I want to create an account so I can publish posts.

**Acceptance:** Given valid unique details and matching passwords, when I
submit registration, then an account with a salted hash is stored and I am
sent to sign-in. Duplicate names, invalid names, mismatched passwords and
passwords outside 15-128 characters produce errors and no new account.

**Tasks:** Review schema/form; review validation and normalization; review
Argon2 hashing; run registration tests; check form manually.

## US-02 - Sign in

**Story:** As a registered user, I want to sign in so I can publish under my own
account.

**Acceptance:** Correct credentials create a session and show the feed.
Incorrect/unknown credentials show a generic error without authentication.
Password is not echoed or placed in the cookie.

**Tasks:** Review hash verification/session; inspect failed-login behavior;
run login tests; check cookie flags; demonstrate valid/invalid login.

## US-03 - Sign out

**Story:** As a signed-in user, I want to sign out so this browser can no longer
publish as me.

**Acceptance:** POST with valid CSRF clears the user session; a later publishing
attempt requires login. GET cannot sign the user out. Document signed-cookie
revocation limitations.

**Tasks:** Review logout handler and button; run logout tests; attempt a post
after signing out; review session ADR.

## US-04 - Read feed

**Story:** As a visitor, I want to see everyone's posts so I can read community
updates.

**Acceptance:** Posts show username, text and UTC creation time; newest first
with deterministic ordering for timestamp ties. Two users' posts appear.
Submitted HTML is escaped. The first empty feed gives a useful message.

**Tasks:** Review JOIN/order/index; review template escaping; create two users
and posts; run feed tests; check layout and keyboard navigation.

## US-05 - Publish

**Story:** As a signed-in user, I want to publish a short post so other users can
read it.

**Acceptance:** Valid 1-280 character trimmed content is stored and displayed.
Blank, over-limit and NUL-containing content is rejected. Anonymous users cannot publish. Supplying
someone else's author ID does not change ownership. CSRF is checked.

**Tasks:** Review authorization/validation; inspect parameterized INSERT;
review form; run valid/invalid and author-impersonation tests; demonstrate post.

## US-06 - Retain data

**Story:** As the customer, I want data to survive ordinary restarts so demo
accounts and posts are not lost.

**Acceptance:** Existing user can log in and post remains after app recreation
and after Docker down/up with the same retained named volume. README explains
the difference between stopping containers and deleting a volume.

**Tasks:** Review CREATE IF NOT EXISTS; verify local persistence test; perform
Docker restart and recreation; attach results/screenshots.

## EN-04 - Quality verification

**Description:** As the developer, I want meaningful acceptance and security
tests so changes do not silently break the required user journeys.

**Acceptance:** pytest passes; test-to-requirement mapping is recorded. Manual
mobile/desktop/keyboard checks and feed benchmark are performed and results
recorded. Fixes are documented with real evidence.

**Tasks:** Read tests; run them in a clean environment; check browser at 375px
and 1280px; measure feed; link actual results and fix any failures.

## EN-05 - Docker and local delivery

**Description:** As the lecturer, I want a short reproducible Docker startup so
I can run the project from its repository.

**Acceptance:** A clean checkout builds and starts with the documented Compose
command. App is healthy, core journeys work, volume retains data, and README
lists prerequisites, variables, ports, tests and troubleshooting.

**Tasks:** Inspect Dockerfile/Compose; run clean build; run smoke script;
repeat manual data-retention demo; confirm README works from a fresh folder.

## EN-06 - CI

**Description:** As the developer, I want every push checked automatically so
test/build failures are visible before submission.

**Acceptance:** Real GitHub push triggers dependency installation, pytest,
Docker build and smoke checks. Successful run URL/commit SHA are captured.
Configuration alone does not meet this item.

**Tasks:** Review workflow; push; inspect run; fix failures; record actual green
run; link evidence to the issue.

## EN-07 - Submission and demo

**Description:** As the lecturer, I want a concise demonstration and accessible
engineering evidence so I can assess the complete project.

**Acceptance:** Repository/board URLs work for assessment; requirements,
methodology, backlog, diagram, ADR and README are present. Actual CI evidence
and local MVP are shown in a rehearsed 10-minute presentation. Assistance is
disclosed as required by the institution's policy.

**Tasks:** Complete checklist; prepare screenshots; rehearse timings; verify
demo data; record actual lessons/trade-offs; check AI-use disclosure.

## US-07 - Older posts

**Story:** As a reader, I want to navigate older posts so the feed stays usable
as the database grows.

**Acceptance:** At most 20 posts per page; the 21st post is accessible on the
next page. Newer/Older links maintain order without duplicates on an unchanged
dataset. All authors remain included. Invalid page input is safe.

**Tasks:** Review LIMIT/OFFSET; test timestamp ties/page boundaries; review
navigation; measure the first-page performance target.

## Live board and evidence

- [Kanban board](https://github.com/users/Corby303/projects/5/views/1)
- [Backlog table](https://github.com/users/Corby303/projects/5/views/2)
- [Kanban screenshot, 15 October 2026](evidence/twitter-lite-kanban-2026-10-15.jpg)
- [Backlog table screenshot, 15 October 2026](evidence/twitter-lite-backlog-2026-10-15.jpg)

Verified board snapshot: Backlog 0, To Do 3, In Progress 1, Review / Testing 9,
and Done 1. Priorities: 13 Must and 1 Should. The Project is private; confirm
assessment access separately. These screenshots record actual board creation
and configuration, and do not replace continued board use or application demos.

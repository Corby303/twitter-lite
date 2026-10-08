# Preparation verification - actual results

Checked on 8 October 2026 in the preparation environment, using Linux and
Python 3.12.14. These results describe checks performed while preparing the
reference pack. They are not your personal board activity or a GitHub CI run.

| Check | Observed result |
|---|---|
| Dependency install | Flask 3.1.3, Flask-WTF 1.3.0, argon2-cffi 25.1.0, Waitress 3.0.2 and pytest 9.1.1 installed successfully, with pinned transitive dependencies. |
| Dependency consistency | `python -m pip check`: no broken requirements. |
| Automated suite | `python -m pytest -q`: **49 passed in 2.78 seconds**. |
| Actual HTTP server | Waitress served successful registration, login, publish, public feed, author/UTC display and logout checks through real HTTP requests. |
| Actual process persistence | Stopping/restarting Waitress with the same data directory retained the post/account; the persisted account could log in again. |
| Browser journeys | Chromium automation exercised account registration, login, two-user posting/order and logout successfully. |
| Browser layout | Screenshots inspected at desktop 1280px and mobile 375px. A maximum-length username exposed overflow; CSS was fixed and the repeated mobile width check reported document width 375px for viewport 375px. Feed and registration screenshots were reviewed. |
| Keyboard sample | Tab reached a link with a visible solid focus outline. This is a limited check, not a complete accessibility audit. |
| Local feed benchmark | 1,000 stored posts and 20 sequential Flask test-client GET requests: median 0.0006s; nearest-rank p95 0.0008s. Meets the scoped p95 < 2s target on this machine. Excludes network and concurrent load. |
| Source/configuration | Python files parsed; Compose and workflow YAML parsed; expected push/PR/manual events, test/build steps and volume mount were inspected. |
| Documentation links | Relative Markdown links resolved to existing project files. |

## Not verified here

- Docker image build and actual container start/recreation: Docker was not
  available in the preparation environment. The Docker smoke script and CI
  checks are supplied, but their container result must be obtained for real.
- GitHub Actions execution, repository/Project access and live board history:
  no user GitHub repository or board was created.
- Installation on the student's Windows computer and a clean GitHub clone
  on the lecturer's machine: still to be performed.
- Institutional permission/disclosure requirements beyond the supplied
  assignment's academic note: the institution's full policy was not provided.

Use `evidence-checklist.md` to record your actual follow-up results. Do not replace
missing Docker/CI evidence with these local Python test results.

# Submission evidence checklist

Repository and CI evidence below was verified on 15 October 2026. The linked
successful CI run is the baseline before the post-validation and benchmark fixes;
the dated local checks below cover those fixes. Personal demonstrations, board
activity and presentation evidence still need their own actual results.

| Required evidence | Where / action | Your actual result |
|---|---|---|
| GitHub repository URL | Source, tests, Docker, workflow and docs committed | [Corby303/twitter-lite](https://github.com/Corby303/twitter-lite) |
| Requirements (15 marks) | Review/adopt `requirements.md`; IDs/criteria/assumptions | To be reviewed |
| Methodology (10 marks) | Adopt/adapt Kanban and record actual use/reviews | To be reviewed |
| Stories/backlog (15 marks) | Copy prioritized criteria/tasks to real issues | To be created |
| Board management (10 marks) | Project URL, real status updates and screenshots | To be created |
| Architecture/ADR (15 marks) | Review/adopt diagram and ADRs; explain trade-offs | To be reviewed |
| Git/GitHub (10 marks) | Safe ignores and meaningful actual commits | To be demonstrated |
| Working MVP (15 marks) | Actual user journeys, persistence and test results | 56 automated tests passed in the 15 October review; personal demonstration still to be recorded |
| Docker/CI (10 marks) | Docker clean run plus successful Actions URL/SHA | [Successful baseline run](https://github.com/Corby303/twitter-lite/actions/runs/38434307047), including Docker build, health and HTTP/persistence checks; personal Docker demonstration still to be recorded |
| README | Check prerequisites, variables, ports and test/run commands | To be reviewed |
| 10-minute presentation | Product, board, decisions, Docker and CI | To be rehearsed |
| Academic disclosure | Check institution policy and record assistance accurately | To be completed |

The eight marked rubric areas sum to 100. Presentation and README are mandatory
evidence even though they are not separate rows in that 100-mark rubric.

## Link/result record

- Repository URL: https://github.com/Corby303/twitter-lite
- Project board URL: Not verified in this review; add the actual board link.
- CI successful run URL: https://github.com/Corby303/twitter-lite/actions/runs/38434307047
- CI commit SHA: `71fba020f68b9a3503ae743ad96a42317d1efce3` (verified baseline before the 15 October fixes).
- Date/machine/Docker version for local demonstration: Still to be recorded on the demonstration computer. Docker was unavailable in the review environment; the linked GitHub Actions run supplies separate Docker evidence.
- Local test command and actual result: 15 October 2026, Linux x86_64, Python 3.12.14; `python -m pytest -q`: **56 passed in 9.77 seconds**. Includes NUL-input rejection/recovery and benchmark CLI success/failure regression checks.
- Performance machine/method/median/p95: 15 October 2026, Linux x86_64 review environment, Intel Xeon Platinum 8573C, Python 3.12.14; `python scripts/measure_feed.py`, 1,000 posts and 20 sequential Flask test-client requests; median **0.0009s**, nearest-rank p95 **0.0028s**, target **PASS**, exit status **0**. This excludes network latency and concurrent load.
- Manual browser/keyboard result: Not performed in this review; record on the demonstration computer.
- Board screenshots and real dates: Still to be supplied from actual board activity.
- Relevant issue/commit links: [Reviewed baseline](https://github.com/Corby303/twitter-lite/commit/71fba020f68b9a3503ae743ad96a42317d1efce3); subsequent fix commits are available in the repository history.
- Assistance disclosure location: [ai-assistance.md](ai-assistance.md); update it with actual review, adaptations and validation.

Use test/demo accounts and avoid screenshots that expose actual passwords or
session keys. Ensure the lecturer has access to both repo and board.

# Part B - Methodology: Kanban

**Proposed choice for student review:** Kanban with a prioritized backlog and
small, demonstrable tasks. This document states a planned working method; add
your real review notes and examples as the work happens.

## Why this fits

The project has one or two developers, uncertain customer details and a short
delivery window. Kanban makes work visible without requiring a full Scrum role
structure or fixed sprint ceremonies. Tasks can change priority after feedback,
while work-in-progress limits encourage finishing a feature before starting more.

Waterfall would make sense with stable, well-specified requirements, but this
brief explicitly leaves details to be analyzed. Scrum is also defensible for an
iterative delivery; its sprint planning, roles and ceremonies introduce more
coordination than this small team needs. This is a project-specific judgment,
not a claim that Kanban is universally superior.

## Planning and prioritization

Use Must/Should/Could priorities. Account registration, authentication, posting,
all-user feed, persistence, Docker and CI are Must. Pagination is Should and
included in the reference implementation. Optional social features are deferred.

Each board item has an ID, description, testable acceptance criteria, priority,
status and links to its requirements. Split large stories into tasks that can be
reviewed in roughly one working session. Choose the next highest-priority item
whose dependencies are complete. Estimates are planning aids, not evidence of
hours worked.

## Workflow and work-in-progress limits

| Status | Entry / exit rule | Planned limit |
|---|---|---|
| Backlog | Story exists but is not yet selected. | No fixed limit |
| To Do | Acceptance criteria, dependencies and next actions are clear. | Keep only the next few tasks |
| In Progress | Actual implementation/review is underway. | One item per developer |
| Review / Testing | Change is ready; run tests and inspect the user journey. | One item per developer |
| Done | Meets the definition below and evidence is linked. | No fixed limit |

For solo work, review your own diff against acceptance criteria. For a pair,
prefer review by the other student. Record the real reviewer; do not invent one.

## Definition of Ready

- Requirement/story and acceptance criteria are understood.
- Task fits the planned scope and its dependencies are identified.
- Priority and verification approach are recorded.

## Definition of Done

- Code or document satisfies the item's acceptance criteria.
- Relevant tests pass and the browser journey is checked where applicable.
- Documentation is consistent with the final behavior.
- Real changes are committed with a meaningful message.
- Evidence or result is linked in the issue, and the board status is updated.
- For Docker/CI items specifically, the real container/Actions check succeeded;
  a supplied configuration file alone is not completion evidence.

## Review rhythm

At the start of each work session, choose the next ready item and move it to
In Progress. At the end, record what changed, results and blockers. Review the
whole product/backlog at least weekly or after a milestone; seek lecturer/client
feedback where possible and record it only if it occurred.

Use the brief's illustrative phases as milestones rather than calling them
Scrum sprints: foundation, identity, social posts, then quality/delivery. Kanban
work flows continuously within and between those phases.

## Track the work honestly

Attach a board screenshot at the start, another while real tasks are underway,
and one after review/completion. Link commits/tests and requirement changes.
The reference code is supplied assistance; your board should show your genuine
understanding, review, adaptations and validation, not a reconstructed history.

### Review log template

Copy this for each real review:

- Date and participants:
- Stories reviewed:
- Test/demo result and evidence link:
- Feedback received (if any):
- Decision and next priority:
- Blockers:

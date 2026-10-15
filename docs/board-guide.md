# Project board: Twitter Lite MVP

The assignment assesses board management separately from the backlog. A Markdown
table is useful planning, but it does not replace a real GitHub Project, Trello
or Jira board with recorded use.

## Existing Project

The Project was created and linked to the repository on 15 October 2026.
Use this existing board for subsequent work:

- [Kanban board](https://github.com/users/Corby303/projects/5/views/1)
- [Backlog table](https://github.com/users/Corby303/projects/5/views/2)
- 14 repository issues, assigned to `Corby303`, with acceptance criteria and tasks.
- Status: Backlog, To Do, In Progress, Review / Testing, Done.
- Priority: Must, Should, Could; the current backlog has 13 Must and 1 Should.
- [Dated board screenshot](evidence/twitter-lite-kanban-2026-10-15.jpg) and
  [full backlog screenshot](evidence/twitter-lite-backlog-2026-10-15.jpg).

The Project is private. Assessment access must still be confirmed for the
lecturer. Manual app checks, personal demonstrations and presentation evidence
remain pending. The steps below are a setup reference for the recorded board.

## GitHub Projects setup reference

1. After creating the repository, create a personal GitHub Project. GitHub's
   [current instructions](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project)
   describe the exact entry points. Choose a Board view and name it
   `Twitter Lite MVP`.
2. Edit the Status field options to **Backlog**, **To Do**, **In Progress**,
   **Review / Testing**, **Done**. Group the board by Status.
3. Add a Priority single-select field: **Must**, **Should**, **Could**.
4. In the repository's Issues tab, create one issue for each item in
   `docs/backlog.md`. Use the ID in its title, such as `US-01 Register an account`.
5. Copy the description, acceptance criteria, tasks and requirement IDs. Set its
   priority and assign yourself or your actual teammate.
6. Add the issues to the Project. Start with Backlog and select the first few
   items for To Do. Link the Project to the repository where available.
7. Confirm the lecturer can access the repository **and** Project. They have
   separate visibility/access settings; sharing one does not guarantee the other.

## Use during real work

Move an item to In Progress only when you start its actual review/change.
Move it to Review / Testing when ready for validation. In the issue, record the
commit, actual command/results and any manual check. Only then move it to Done.

Since the pack includes reference code, do not pretend the board represents
earlier development you performed. It can honestly represent your adoption of
requirements, review of supplied code, modifications, tests, fixes and delivery.
Tell your lecturer if the course has stricter rules for supplied assistance.

Example issue comment structure (fill with real results):

```text
Reviewed requirement:
Actual change / decision:
Commit URL:
Tests run and result:
Manual check:
Remaining issues:
```

Save screenshots when you actually have Backlog/To Do items, items in progress,
review/testing evidence, and final Done items. Include dates in captions and
links to issues. A final board with everything Done but no activity/evidence is
weaker than a board used as the project progresses.

## Traceability example

`FR-01` -> `US-01` GitHub issue -> actual implementation/review commit ->
registration tests -> issue evidence -> Done status.

This is the relationship to reproduce using your real issue and commit URLs.

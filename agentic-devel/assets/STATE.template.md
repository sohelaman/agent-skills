<!--
Placeholders:
  {{PROJECT_NAME}}
  {{PLAN_PATH}}
  {{MEMORY_FILE}}
  {{TAG_COLUMN_NOTE}}   Delete the "Tags" column entirely (from header, separator, and every row)
                        if this project has no task-flagging convention (e.g. no [SEC]-style
                        tag). Otherwise name it after whatever tag(s) matter here.
  Seed one row per task from the plan, phase-grouped exactly like the plan is grouped. All rows
  start at status `todo` with every other cell blank.
-->
# {{PROJECT_NAME}} Build State

Last updated: <date> · Current phase: <n> · Progress: 0/<total> done

> Living progress ledger for `{{PLAN_PATH}}`. Rules (see {{MEMORY_FILE}}): one row per task; an
> agent updates ONLY the row of the task it executed; deviations from the plan go in Notes;
> status values: `todo` · `in-progress` · `done` · `blocked(reason)`. A task may start only when
> every task in its Depends column is `done`.

## Phase 0 — <phase name>

| Task | Title | Depends | {{TAG_COLUMN_NOTE}} | Status | Date | Commit | Notes |
|------|-------|---------|:---:|--------|------|--------|-------|
| <id> | <title> | — |  | todo | | | |

<!-- Repeat one table per phase. -->

---
name: agentic-devel
description: Methodology-first process for running a backend web application build as a sequence of agent-sized, independently verifiable tasks — spec/plan → task cards → a living STATE.md ledger → a /task runner skill → independent reviewer subagents → one commit per task. The process, not the tooling, is the point - it's tuned for backend, database-driven web development (.NET, PHP/Laravel, and other RDBMS-backed server stacks) but the loop itself works for any backend project. Use this whenever the user wants to set up a task-driven agent workflow for a backend/API/admin-panel/service project, wants a coding agent to work through a project task-by-task with state tracked across sessions, asks to bootstrap agent harness/scaffolding (.claude/skills, .claude/agents, STATE.md, IMPLEMENTATION_PLAN.md) for a repo, or wants to execute a specific numbered/IDed task from an existing plan-and-ledger setup. Also trigger on phrases like "set up the task workflow for this project", "bootstrap the agent harness", or "run task T-x/TASK-12/etc." in a repo that already has this pattern.
---

# Agentic Development Methodology

## Why this pattern exists

A coding agent's context does not survive between sessions, and a single long session drifts:
the more a session accumulates, the more likely it wanders from the spec or starts improvising
past its actual instructions. The fix isn't a smarter agent — it's making the **process** carry
the memory instead of the model:

- The **plan** (spec broken into task cards) is the source of truth for *what* to build.
- The **ledger** (a living status file) is the source of truth for *what's already done* and
  *what depends on what* — so a brand-new session with zero history can pick up exactly where
  the last one left off.
- **Verification commands** are the contract for *done* — never "looks right to me."
- **Independent reviewer subagents** catch what the same context that wrote the code is
  structurally unable to see, because they start fresh and are told to look for problems, not
  confirm success.
- **One task, one commit** keeps history bisectable and keeps each unit of agent work small
  enough to review and revert independently.

This is a methodology, not a tech stack. The mechanism — externalized plan + ledger,
verify-as-contract, independent review, one-task-one-commit — has nothing framework-specific
about it and works for any repo shape.

## What this is tuned for

The loop below was proven running a production-grade, database-backed backend web build: layered
architecture, RDBMS persistence, schema migrations as first-class deliverables, a server-rendered
or API surface sitting on top. Its templates default to that shape — **`.NET` (ASP.NET Core/EF
Core) and `PHP`/`Laravel` (Eloquent) are the two stacks it's written closest to, with an RDBMS
(MySQL, PostgreSQL, SQL Server) as the assumed datastore** — because that's the domain this
process was built to serve: backend web applications, not frontend SPAs, CLIs, or data
pipelines. When bootstrapping into a project in that domain, lean on the RDBMS-aware guidance
below (migrations as deliverables, layering through a repository/ORM boundary, transaction
integrity as a recurring review concern) rather than treating it as boilerplate to skip past.

Other backend stacks (Python/Django, Java/Spring, Node/Express, Go, etc.) work with the same
loop — adapt the architecture-rule and stack-command details, not the process itself.

## Two modes

Figure out which applies before doing anything else:

| Signal | Mode |
|---|---|
| Repo has no task-plan/ledger scaffolding yet, or user asks to "set up" / "bootstrap" the workflow | **Bootstrap** (§1) |
| Repo already has a plan + ledger (this pattern or an equivalent) and the user names a task to work on | **Execute** (§2) |
| Unclear | Look for a ledger-like file (`docs/agent/STATE.md`, `STATE.md`, `PROGRESS.md`, task board, etc.) and a plan-like file (`IMPLEMENTATION_PLAN.md`, `TASKS.md`, `docs/plan.md`). If both exist, use Execute. Otherwise ask the user which they want, in one short question — don't guess and start writing files. |

A repo can need both in sequence: bootstrap once, then execute many times across many future
sessions. Don't re-bootstrap an already-scaffolded repo — check first (§1.4).

---

## §1 — Bootstrap: scaffolding the workflow into a project

### 1.1 Gather what you need

Before writing anything, know:

1. **The spec.** Does the user have a PRD/RFC/design doc to decompose into tasks, or do they
   want to write the task list from a conversation/README? Either is fine — the plan just needs
   *some* source of truth to trace tasks back to.
2. **The stack.** Detect it, don't ask if it's obvious — check `*.csproj`/`*.sln` (.NET),
   `composer.json` + `artisan` (PHP/Laravel), or another backend stack
   (`pyproject.toml`/`requirements.txt` for Python, `pom.xml`/`build.gradle*` for Java/Kotlin,
   `package.json` for Node, `go.mod`, `Cargo.toml`, `Gemfile`, etc.). Also check for a migrations
   directory (`Migrations/` for EF Core, `database/migrations/` for Laravel, or the equivalent
   for whatever ORM/migration tool is in use) and which RDBMS it targets — schema changes are a
   first-class deliverable in database-backed projects, not an afterthought. See
   `references/stack-commands.md` for build/test/lint/coverage/migration commands typical of
   each — use these as a starting point, then confirm against the repo's actual scripts
   (`Makefile`, `composer.json` scripts, CI config) since the real commands always win over a
   generic guess.
3. **Existing conventions.** Read whatever memory file already exists (`CLAUDE.md`, `AGENTS.md`,
   `.cursor/rules`, etc.) and any linter/formatter config — don't invent conventions the repo
   already has opinions about.
4. **Architecture rules, if any.** For a typical backend web app this means a layering direction
   like controller/handler → service/use-case → repository → RDBMS, with the database only ever
   touched through that repository/ORM boundary — no raw queries from a controller, no business
   logic living in a repository. Confirm what this repo's own layering actually is rather than
   assuming that shape applies; if the project has no architecture rules yet and the user wants
   some, that's a design conversation, not something to invent silently — ask or propose and
   confirm.
5. **Commit convention.** Does the org mandate a prefix (e.g. `[TEAM-TAG] <type>(scope): summary`)?
   Default to plain [Conventional Commits](https://www.conventionalcommits.org/) if the user has
   no preference.
6. **Sensitive-domain flags.** Does this project handle secrets/PII/payments/health data such
   that a dedicated security-review pass matters for some tasks? If so it gets a
   `security-reviewer` subagent and a task-tag convention (e.g. `[SEC]`) that triggers it; if not,
   skip that subagent entirely rather than installing dead weight.

Don't over-interview — infer everything derivable from the repo, and only ask the user about
things that are genuinely their call (spec source, commit prefix, whether they want a security
pass).

A coverage gate is worth the same "don't invent it" treatment: if the stack has no coverage
tool installed yet, that's different from a project that has one but chose not to enforce a
threshold — don't add a new dependency just to satisfy a template placeholder. Delete the
coverage clauses from whichever templates mention them rather than guessing a tool and threshold
nobody asked for; note in the plan/memory file that a coverage gate is a deliberate future
addition, not something silently assumed.

### 1.2 What gets created

All templates live in `assets/`. Copy each, replace its `{{PLACEHOLDER}}` tokens with real values
gathered in 1.1, and write it to the target repo. Never leave a literal `{{...}}` token in a
written file — if a value doesn't apply (e.g. no coverage gate), delete that clause rather than
leaving a placeholder or a `TODO`.

| Target path | From template | Purpose |
|---|---|---|
| `docs/IMPLEMENTATION_PLAN.md` (or repo's preferred docs location) | `assets/IMPLEMENTATION_PLAN.template.md` | Task cards: goal, spec trace, deps, deliverables, accept criteria, verify commands |
| `docs/agent/STATE.md` | `assets/STATE.template.md` | Living ledger, one row per task, seeded `todo` for every task in the plan |
| `.claude/skills/task/SKILL.md` | `assets/task-SKILL.template.md` | The `/task <id>` runner — the session protocol as an invocable skill |
| `.claude/agents/code-reviewer.md` | `assets/code-reviewer.template.md` | Read-only diff reviewer for this project's conventions |
| `.claude/agents/security-reviewer.md` | `assets/security-reviewer.template.md` | Only if 1.1.6 applies — read-only security-lens reviewer |
| `.claude/settings.json` | `assets/settings.template.json` | Permission allow/deny list + hooks |
| `.claude/hooks/protect_paths.py` | `assets/protect_paths.template.py` | Blocks agent writes to the spec file and secret files |
| `.claude/hooks/format_on_save.sh` | `assets/format_on_save.template.sh` | Only if the stack has a real formatter you've verified works here — formats just the touched file on every edit |
| `CLAUDE.md` / `AGENTS.md` (whichever the harness in use reads) | `assets/PROJECT_MEMORY.template.md` | Session protocol, commands, conventions, security guardrails, definition of done |

### 1.3 Filling in the plan and ledger

- Break the spec into **agent-sized task cards**: each should be completable by one agent in one
  session with fresh context. If a task can't be described in a few sentences of goal + a handful
  of accept criteria, it's too big — split it.
- Every card needs: an ID (`T-<phase>.<n>`, `TASK-<n>`, whatever scheme fits), a goal, its spec
  trace (section/FR/issue number — whatever the project's spec uses as an anchor), its
  dependencies, key deliverables, binary accept criteria, and **shell-runnable verify commands**.
  A card without a verify command is unverifiable and will drift — don't ship one.
- Seed `STATE.md` with one row per card, everything `todo`, dependencies mirrored from the plan.
- If tasks can run in parallel (no shared files, independent deps), note that in a
  parallelization map — same shape as the worked example in `assets/IMPLEMENTATION_PLAN.template.md`
  §4 — and tell the user parallel tasks need separate git worktrees/sessions to avoid workspace
  collisions.

### 1.4 Don't clobber what's already there

If the repo already has a memory file, partial scaffolding, or an existing test suite: **merge,
don't overwrite**. Read what exists first. Extend `CLAUDE.md` rather than replacing it; add rows
to an existing ledger rather than regenerating it; if `.claude/agents/code-reviewer.md` already
exists, treat that as a signal this repo may already be scaffolded — check with the user before
replacing it.

### 1.5 Verify the bootstrap actually works

Don't declare bootstrap done on vibes:
- The task skill should be invocable (check the file parses as valid skill frontmatter).
- The protect-paths hook should actually block a scratch write to the spec file — test it, don't
  assume the pattern-match is right.
- `STATE.md` should list every task from the plan, all `todo`.
- `.claude/settings.json` should be valid JSON.

---

## §2 — Execute: running one task

This is the loop the generated `/task` skill encodes, and it's also what you should do directly
if a project already follows this pattern (with a plan+ledger under different names) but has no
task skill installed yet — the loop matters more than the exact filenames.

1. **Read the ledger first.** Confirm the named task isn't already done and every task in its
   `Depends` is `done`. If not, STOP and report — don't work around a missing dependency by
   guessing what it would have produced.
2. **Read the task card and its spec trace.** Cross-check the referenced spec sections — the spec
   wins over your assumptions about what the card means. If the card and spec disagree, that's
   case 9 below, not something to silently resolve.
3. **Plan before coding**, for anything non-trivial. Enter plan mode; a human (or the calling
   session) should get a chance to see files/tests/risks before code starts moving.
4. **Implement exactly the card's scope.** No unrelated cleanup, no drive-by refactors, no
   speculative extras — even if they look like obviously good ideas. Scope creep across many
   tasks is how a task-based process quietly turns back into an unreviewable big-bang change.
   Tests ship in the same change as the code they cover, not a follow-up task.
5. **Verification is the contract.** Run the card's verify commands plus the project's full
   relevant test suite (and coverage gate, if one exists) until genuinely green — not until the
   output looks plausible. Re-run rather than eyeball a diff of expected vs actual.
6. **Independent review.** Dispatch the `code-reviewer` subagent (read-only, fresh context) on
   the diff; apply findings that are actually valid — see receiving-code-review guidance below.
   For tasks flagged sensitive (whatever tag convention was set up in bootstrap, e.g. `[SEC]`),
   also dispatch `security-reviewer`. Reviewers report Blocker/Major/Minor findings; blockers and
   majors get fixed before closing the task, minors get fixed or explicitly deferred with a
   reason (never silently dropped).
7. **Update the ledger.** Status → done, date, commit ref, and notes covering any deviation from
   the card as written — the next session (and the next human) needs to know what actually
   happened, not just that it happened.
8. **One commit.** Use whatever commit convention bootstrap established. Reference the task ID
   and spec trace IDs in the body. Don't push unless the user asked for that in this session —
   pushing, like any action visible to others, needs its own authorization, not a standing one.
9. **If the task is impossible as written** — missing prerequisite, spec contradiction, a
   dependency that turned out incompatible — **stop and report the conflict**. Don't quietly
   reinterpret the card to make something shippable; that's exactly the kind of undetectable
   drift externalized state is supposed to prevent.

### On reviewer feedback

Treat reviewer subagent output the way you'd treat a skeptical colleague's review, not an oracle:
verify a finding actually reproduces (read the flagged code, don't just trust the description)
before "fixing" it, and push back (in the ledger notes, not silently) on findings that are
technically wrong or out of scope for this card. A reviewer's job is to catch what you can't see
from inside the context that wrote the code — that's valuable precisely because it's independent,
not because it's infallible.

### Version control specifics

- One task = one commit. Never bundle two tasks' worth of unrelated changes into one commit to
  save time.
- Never force-push, rewrite published history, or skip hooks (`--no-verify` etc.) to make a task
  "finish" — if a hook or check fails, that's signal to fix, not bypass.
- Parallel tasks need separate worktrees/sessions — two agents editing the same working tree
  concurrently will corrupt each other's diffs.
- Pushing, opening PRs, and merging are each their own authorization event — a task being
  "done" locally doesn't imply permission to push it.

### Definition of done (generalize per project, but keep the shape)

- [ ] Card's accept criteria met, spec trace IDs satisfied
- [ ] Build clean, full test suite green (+ coverage gate if the project has one)
- [ ] Architecture/lint rules green; no new suppressions without a justification note
- [ ] Conventions the feature actually touches are applied (whatever this project's equivalents
      of audit/soft-delete/i18n/authorization are — most projects have *some* cross-cutting
      conventions; check `CLAUDE.md`/`AGENTS.md` for them)
- [ ] Ledger row updated (status, date, commit ref, notes)
- [ ] Single commit, no unrelated file churn

---

## Reference material

- `references/stack-commands.md` — build/test/lint/format/coverage/migration commands, weighted
  toward `.NET` and `PHP`/`Laravel` over an RDBMS (the primary target — see "What this is tuned
  for" above), with other backend stacks covered more briefly. Used to fill bootstrap placeholders
  and as a sanity check against whatever the repo's own scripts say. The methodology in §1/§2 is
  what actually matters here — this file is a lookup aid, not the point of the skill.
- `assets/` — every template file referenced in §1.2, each with `{{PLACEHOLDER}}` tokens documented
  inline via HTML comments at the top of the file.

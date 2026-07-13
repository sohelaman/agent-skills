# Stack command reference

This is a lookup aid for filling bootstrap placeholders (`{{BUILD_CMD}}`, `{{TEST_CMD}}`, etc.) —
the methodology in `SKILL.md` §1/§2 is what actually matters; nothing here changes the loop
itself. Weighted toward `.NET` and `PHP`/`Laravel` over an RDBMS, since that's the domain this
process is tuned for (see SKILL.md's "What this is tuned for"). Always confirm against the repo's
actual scripts before trusting these — a generic guess loses to whatever the repo's own CI runs.

## Detecting the stack

| Marker file(s) | Stack |
|---|---|
| `*.sln`, `*.csproj` | .NET |
| `composer.json` + `artisan` | PHP / Laravel |
| `composer.json` (no `artisan`) | PHP, other framework |
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python |
| `pom.xml`, `build.gradle*` | Java/Kotlin |
| `package.json` | Node.js / TypeScript |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |

## .NET

- Build: `dotnet build <Solution>.sln` (warnings-as-errors is common in regulated/enterprise
  backends — check `Directory.Build.props`)
- Test: `dotnet test <TestProject>`
- Migrations: `dotnet ef migrations add <Name> -p <InfrastructureProject> -s <StartupProject>` /
  `dotnet ef database update` — EF Core migrations are a first-class deliverable on any task that
  changes the schema, not a follow-up
- Coverage: `dotnet test /p:CollectCoverage=true /p:Threshold=<n>` — **verify the test project
  actually references `coverlet.msbuild`, not just `coverlet.collector`** (the latter is a VSTest
  data collector that silently ignores these MSBuild-style flags — a real, previously-seen gap
  where the coverage gate looked wired up but never actually enforced anything). Prove the gate
  has teeth by deliberately raising the threshold above the real number in a scratch run and
  confirming the build genuinely fails.
- Format: `dotnet format`
- Architecture rules: layer-dependency checks (e.g. `NetArchTest`) are the idiomatic way to make
  "DbContext never referenced outside the data-access layer" and similar layering rules
  executable rather than just documented.

## PHP / Laravel

- Install: `composer install`
- Test: `php artisan test` / `vendor/bin/phpunit` / `vendor/bin/pest` (Pest is common on newer
  Laravel codebases — check `composer.json`'s require-dev before assuming PHPUnit)
- Migrations: `php artisan make:migration <name>` / `php artisan migrate` — like EF Core, a
  schema-changing task ships its migration in the same commit, not a follow-up; `php artisan
  migrate:rollback` should be checked as part of verifying a migration is reversible where the
  project expects that
- Lint/static analysis: `vendor/bin/phpstan analyse` (or `larastan`), `vendor/bin/pint` (Laravel's
  own formatter, replaces the older `php-cs-fixer` convention on newer projects — check which one
  the repo actually has configured)
- Coverage: `vendor/bin/phpunit --coverage-text --coverage-clover=coverage.xml` (needs Xdebug or
  PCOV enabled — a coverage command that silently reports 0% because neither is installed is the
  PHP equivalent of .NET's coverlet.collector gap above; check the extension is actually loaded,
  don't just trust the flag)
- Architecture rules: Eloquent models/query builders should stay behind a
  repository/service-layer boundary if the project has one — controllers calling `Model::query()`
  directly is the same layering violation as a controller opening a raw `DbContext` in .NET, just
  without a compiler to catch it; a code-reviewer subagent check is what catches it instead.

## RDBMS-specific concerns (MySQL / PostgreSQL / SQL Server)

These apply regardless of which backend stack sits on top:

- **Migrations are a task deliverable, not infrastructure.** Any task card that changes the
  schema should list its migration file(s) under Build and include a verify step that actually
  runs the migration against a real (or containerized) database — a migration that only "looks
  right" in the ORM's model diff can still fail against the real engine's constraints.
- **Provider-specific behavior is a real risk if the project targets more than one RDBMS.**
  Things like case-sensitivity of string comparisons, auto-increment vs sequence-based IDs, and
  index/key-length limits differ across MySQL/PostgreSQL/SQL Server — if the project is meant to
  be portable across providers, that's worth an explicit architecture rule ("no provider-specific
  query functions"), not an assumption.
- **Soft delete / audit columns**, if the project uses them, are usually enforced via a global
  query filter or ORM-level convention rather than remembering to add a `WHERE deleted_at IS
  NULL` by hand everywhere — worth checking whether one exists before a task adds a new entity.
- **Transaction boundaries** belong in the service/use-case layer, not scattered across
  repository calls — a common, easy-to-miss code-reviewer check for any task that touches more
  than one table in a single operation.

## Other backend stacks (brief)

The same loop applies; these are just the command starting points.

- **Python:** `pytest`; `ruff check .` / `ruff format .`; `pytest --cov=<pkg>
  --cov-fail-under=<n>`; Django migrations via `manage.py makemigrations`/`migrate`.
- **Java (Maven/Gradle):** `mvn test` / `./gradlew test`; coverage via JaCoCo
  (`mvn verify` / `./gradlew jacocoTestCoverageVerification`); Flyway/Liquibase for migrations.
- **Node.js/TypeScript (backend):** `npm test` (Jest/Vitest); `npx eslint .`; coverage flags
  are usually set in `jest.config.js`/`vitest.config.ts`, not passed on the command line;
  Knex/Prisma/TypeORM migrations depending on the ORM in use.
- **Go:** `go test ./...`; `golangci-lint run`; `go tool cover` for coverage; migrations via
  `golang-migrate` or the ORM's own tool.
- **Ruby:** `bundle exec rspec`; `bundle exec rubocop`; SimpleCov for coverage; Rails migrations
  via `rails db:migrate`.
- **Rust:** `cargo test`; `cargo clippy -- -D warnings`; `cargo tarpaulin` for coverage.

## Cross-stack coverage-gate gotcha

Whatever the language, a coverage "gate" is only real if (a) the flags you're passing are
actually consumed by the tool/runner in use — not a plausible-looking flag for a different tool
or adapter that's silently ignored — and (b) you've verified it has teeth: deliberately push the
threshold above the real number in a scratch run and confirm the build actually fails. Don't
trust a coverage command that "looks right"; prove it fails when it should.

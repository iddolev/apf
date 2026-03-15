---
author: Iddo Lev
LLM_author: Claude Opus 4.6
last_updated: 2026-03-12
---

# GSD Framework Review — Strengths and Gaps

GSD (Get Shit Done) is an agentic SDLC framework that handles several aspects of the software development life cycle — particularly requirements gathering, phased planning, parallel agent execution, and requirement traceability — but does not cover the full lifecycle. This document catalogs both its strengths (to learn from) and its gaps (to address), as input for designing a new agentic programming framework that draws inspiration from several frameworks including GSD.

## What GSD Does Well

The following are strengths worth preserving and building upon in a next-generation framework:

- [x] **Structured Requirements Gathering** — Adaptive questioning phase (`/gsd:new-project`) that probes the user with contextual follow-ups until scope is well-defined. Produces a formal PROJECT.md with requirements, constraints, and decisions.

- [x] **Phased Roadmap with Requirement Traceability** — Requirements are mapped to phases in ROADMAP.md, and every phase traces back to specific requirement IDs. Verification checks that requirements are actually delivered, not just that tasks were completed.

- [x] **Research Before Planning** — Dedicated research phase (`/gsd:research-phase`) investigates domain ecosystem, SDK versions, common pitfalls, and anti-patterns before any code is written. Produces RESEARCH.md consumed by the planner.

- [x] **Plan-Then-Verify Loop** — Plans are created by a planner agent, then independently verified by a checker agent. If the checker finds issues, plans are revised (up to 3 iterations). This catches planning errors before execution begins.

- [x] **Parallel Agent Execution** — Independent tasks within a phase run concurrently via wave-based parallelization. Each executor agent works in isolation, maximizing throughput without conflicts.

- [x] **Atomic Commits per Task** — Each task produces a single, well-scoped git commit with a descriptive message. This makes history readable and rollback granular.

- [x] **Goal-Backward Verification** — The verifier agent checks whether the phase *goal* was achieved (not just whether tasks were completed). This catches cases where all tasks pass but the overall intent was missed.

- [x] **Persistent State Across Context Resets** — UAT sessions, phase state, and planning context survive `/clear` and session boundaries via file-based persistence (UAT.md, STATE.md, SUMMARY.md). Work is never lost to context window limits.

- [x] **User Acceptance Testing Workflow** — `/gsd:verify-work` presents one test at a time, records pass/fail, auto-infers severity, and on failure spawns parallel debug agents to diagnose root causes before planning fixes.

- [x] **Deviation Handling During Execution** — Executor agents have clear rules for when to auto-fix (missing validation, security gaps), when to document deviations, and when to stop and escalate. Not all surprises require human intervention, but serious ones do.

- [x] **Codebase Documentation Templates** — Rich template library (ARCHITECTURE.md, STACK.md, CONVENTIONS.md, CONCERNS.md, INTEGRATIONS.md) that documents the codebase systematically, not just the code.

- [x] **Error Handling Enforcement** — Executor agents auto-add missing input validation, auth checks, CORS headers, and error logging. Security-conscious patterns are enforced at code generation time, not left to manual review.

---

## Gaps — Fully Documented

<a id="integration-tests-for-external-apis"/>

### 1. Integration Tests for External APIs

GSD's testing philosophy is to mock all external dependencies in automated tests and delegate real API validation to one-time manual UAT (via `/gsd:verify-work`). This leaves a gap: mocked tests silently accept any parameters you pass, so when an external provider deprecates or renames a parameter, all automated tests pass green while the real API rejects your calls. For example, all mocked unit tests may pass while the OpenAI provider code may be broken due to a rename of the `max_tokens` field to `max_completion_tokens` (in the OpenAI API).

GSD has no concept of:

- Automated integration tests that call real external APIs
- Scheduled/nightly health checks against live providers
- Non-blocking CI/CD monitoring that alerts developers without blocking merges

**Mitigation**: Supplement GSD's test generation with a separate integration test suite marked with `@pytest.mark.integration`, run nightly as a non-blocking health check. On failure, notify developers via email or Slack — but never block PRs or merges. See `api_integration_tests.md` for a detailed writeup of the recommended approach with GitHub Actions and GitLab CI/CD examples.

<a id="code-quality-checks"/>

### 2. Code Quality Checks

GSD generates code through its executor agents but does not enforce or verify code quality standards. There is no built-in step in the GSD workflow that:

- Runs a linter (e.g., ruff, flake8, pylint) on generated code
- Enforces formatting standards (e.g., black, isort)
- Checks type annotations (e.g., mypy, pyright)
- Validates against project-specific coding guidelines
- Reviews generated code for adherence to best practices before committing

GSD's executor agents write code and commit it, but the quality of that code depends entirely on the LLM's judgment in the moment. There is no automated gate between code generation and commit that verifies quality standards are met.

**Mitigation**: Integrate linting and formatting as pre-commit hooks (e.g., via the `pre-commit` framework) so that any code committed by GSD agents or developers is automatically checked. Additionally, GSD's executor workflow could be extended to include a code quality verification step after each task's code is written but before it is committed.

---

## Gaps — To Do

The following gaps were identified by examining the GSD codebase (workflows, templates, agents, hooks under `.claude/`). Each needs further discussion and a full section written above.

- [ ] **CI/CD Integration** — GSD has zero awareness of CI/CD pipelines. No workflow generates or manages GitHub Actions, GitLab CI, or any deployment automation. GSD treats "code committed" as the finish line, but in practice code must pass automated pipelines before it reaches production.

- [ ] **Dependency Management** — GSD's `STACK.md` template documents what dependencies exist but provides no workflow for auditing outdated or vulnerable packages. No integration with `pip audit`, `npm audit`, Dependabot, or Snyk. A newly scaffolded project can ship with known CVEs from day one.

- [ ] **Security Scanning** — Beyond enforcing `.env` in `.gitignore` and the executor agent auto-adding input validation, GSD has no SAST/DAST integration. No secret scanning, no dependency vulnerability checks, no security-focused code review step.

- [ ] **Deployment** — GSD does not address Docker, cloud platforms, or deployment strategies. No Dockerfile generation, no environment-specific config, no deployment checklists or runbooks. The gap between "code on main" and "code in production" is entirely outside GSD's scope.

- [ ] **Monitoring/Observability** — GSD's `CONVENTIONS.md` template covers logging patterns at the code level, but there is no guidance on setting up centralized logging, error tracking (Sentry), metrics (Datadog/Grafana), or alerting. Code ships without operational visibility.

- [ ] **Database Migrations** — GSD has no workflow for schema migrations, seed data, or database versioning. For projects with databases, missing migration management leads to manual schema changes and divergence between environments.

- [ ] **Branching Strategy** — GSD supports per-phase branches via config (`branching_strategy: "phase"`), but only during execution. Discussion and planning phases don't respect branching. No guidance on feature branches, release branches, hotfix workflow, or conflict resolution. The framework was designed around single-branch linear development.

- [ ] **Code Review / PR Workflow** — GSD commits code directly without PR review. No PR templates, no review checklists, no approval gates. The verifier agent checks implementation against goals (a form of automated review), but there is no human code review step in the workflow.

- [ ] **Version Management** — GSD groups requirements by version (v1, v2) in `REQUIREMENTS.md` and supports milestones in `ROADMAP.md`, but there is no semantic versioning enforcement, no changelog generation, no release notes automation, and no git tagging workflow.

- [ ] **Backwards Compatibility** — When APIs or interfaces change across phases, GSD does not check for breaking changes. No API contract testing, no deprecation warnings, no migration guides for consumers of changed interfaces.

- [ ] **Accessibility (A11y)** — For frontend phases, GSD does not verify WCAG compliance, test keyboard navigation, or check screen reader compatibility. No a11y audit step exists in the verification or UAT workflows.

- [ ] **Performance Testing** — GSD's `CONCERNS.md` template documents known performance bottlenecks, but there is no workflow for load testing, benchmarking, or detecting performance regressions between phases.

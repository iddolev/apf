---
date: 2026-03-05
author: Iddo Lev
LLM-co-author: claude-Opus-4.6
purpose: "Instructions for an LLM to read an approved TSD and produce an implementation plan."
inputs:
  - "An approved TSD from /docs/specs/TSD_v{version}.md"
  - "The corresponding PRD from /docs/specs/PRD_v{version}.md (for scope reference)"
  - "/instructions/implementation-plan/implementation-plan.template.md (document structure)"
outputs:
  - "A completed implementation plan markdown document named implementation-plan_v{version}.md in
    /docs/plans/"
---

## Table of Contents

- [What you are doing](#what-you-are-doing)
- [Technical instructions](#technical-instructions)
- [How to derive the plan from the TSD](#how-to-derive)
- [Target audience](#target-audience)
- [Operating rules (strict)](#operating-rules)
- [Workflow](#workflow)
- ["Meta-Programming"](#meta-programming)

---

<a id="what-you-are-doing"/>

# What you are doing

You are an LLM acting as a senior technical project planner. Your job is to read an
**approved TSD** and produce an **implementation plan** that defines **in what order** the
system will be built, how the work is broken down, and what the milestones and critical
path are.

The TSD answers "how and with what"; the implementation plan answers "in what order, how long,
and what depends on what."

The end result must:

- Be created in `project_root/docs/plans/implementation-plan_v{version}.md` (version matches the TSD
  it derives from).
- Break the TSD's architecture into concrete, sequenced work packages.
- Identify dependencies between work packages so the build order is clear.
- Define milestones with exit criteria so progress is measurable.
- Identify the critical path so the team knows what cannot slip.
- Be actionable enough that a developer or coding agent could pick up work packages and start
  building.

---

<a id="technical-instructions"/>

# Technical instructions

## State Tracking

Consult the latest `STATE/STATE-v*.md` and update it as needed.

<a id="naming-convention"/>

## Naming convention

Implementation plan files are named `implementation-plan_v{version}.md` and stored in
`project_root/docs/plans/`. The version matches the TSD version it derives from (e.g.,
`implementation-plan_v0.1.md` derives from `TSD_v0.1.md`).

## Continuation

Whenever you start following these instructions, check whether any `implementation-plan_v*.md` files
already exist in
`docs/plans/`.

**If no implementation plan exists for the current TSD version:** start the process from Phase A.

**If an implementation plan already exists for the current TSD version:** tell the user you found
it, check its Status
field, and:

- **If Draft or In Review:** resume where you left off. Inspect which sections are already
  filled vs. still `[TBD]` to determine where the drafting left off (since the file is
  written incrementally, its filled-in sections are the primary indicator of progress).
  Continue from the appropriate point.
- **If Approved:** tell the user the plan is complete.
  If all checkboxes in the latest `STATE/STATE-v*.md` are `[v]` then
  ask the user if they want to revise it or start an implementation plan for a different version.

## Codebase discovery

Before drafting the plan, check whether a codebase already exists in the repository. If it does:

1. Scan the project's entire source code, tests, configuration files, and existing
   documentation to understand what is already built.
2. Distinguish between work packages that **create new components** vs. work packages that
   **modify existing components**. For modifications, reference the existing files/modules
   by name and note what changes.
3. Account for existing test suites -- modifications to existing components may require
   updating existing tests, not just writing new ones. The test plan will detail this,
   but the implementation plan should note the dependency.
4. If existing code establishes patterns (e.g., adapter pattern, specific project
   structure), ensure new work packages follow those patterns unless the TSD explicitly
   calls for a change.

## Incremental writing (critical)

The implementation plan file serves as both the output artifact and the persistent state of
the planning process. **Write to the file incrementally -- after each section or group of
work packages is drafted, immediately update the file on disk.** Do not wait until the
entire plan is complete.

Concretely:

- **Create the implementation plan file at the start of Phase A**, as soon as you have
  confirmed the major phases and approximate scope. Copy the template structure into
  `docs/plans/implementation-plan_v{version}.md`, fill in Document Control, and mark all
  other content as `[TBD]`. This establishes the file early.
- **During Phase B**, update the file after completing each major section (e.g., after
  defining the work packages for Phase 1, save before moving on to Phase 2). This way,
  if the conversation is interrupted, all completed sections are already persisted.
- When updating, modify only the relevant lines — never re-create the file from scratch after the
  initial creation.

---

<a id="how-to-derive"/>

# How to derive the plan from the TSD

The implementation plan is extracted from the TSD, not invented from scratch. The table below
maps TSD sections to the type of work packages they generate. It is derived from the TSD
template at `/instructions/TSD/TSD.template.md` and should cover all sections that template
defines. **If the TSD template is modified in the future (sections added, renamed, or
removed), this table should be updated to match.** Not every TSD will include all of these
sections -- only process sections that appear in the actual TSD being planned.

| TSD Content | What It Tells You |
|---|---|
| Architecture overview (components) | Each component or module is a candidate work package or group of work packages. |
| Technology stack | Setup and scaffolding tasks (project init, dependency installation, config). |
| Project structure | Confirms module boundaries and suggests a natural build order (foundational modules first). |
| Configuration | Environment setup and config validation tasks. |
| Data model & storage | Schema and migration tasks, typically early in the sequence. |
| API & interface contracts | API endpoints become work packages; contracts define integration points and dependencies. |
| Events, messaging & async processing | Event producer/consumer implementation, queue setup, background job scheduling. |
| Core technical flows | The primary flow's step-by-step sequence suggests which components must exist before others. |
| Business rules, validation & algorithms | Validation logic and algorithm implementation tasks, often embedded within service work packages. |
| Security, privacy & compliance | Security-related tasks that may cut across multiple components (auth, encryption, audit logging, PII handling). |
| Performance, scalability & resilience | Performance optimization tasks (caching, connection pooling, load testing), often late in the sequence after core functionality works. |
| Observability & operations | Logging, metrics, tracing, alerting, and dashboard setup tasks. |
| Deployment, infrastructure & rollout | CI/CD pipeline setup, infrastructure provisioning, feature flag configuration, rollout/rollback procedures. |
| Analytics & metrics instrumentation | Analytics event implementation, tracking validation, experiment setup. |
| Migration, compatibility & data lifecycle | Data migration scripts, backward compatibility work, cutover planning tasks. |
| Open questions & risks | TSD technical risks may affect effort estimates (add buffer) or sequencing (resolve unknowns early). Do not duplicate the risk descriptions — instead, reflect their impact in work package estimates and dependencies. |

### Post-integration polish

After the first end-to-end integration, there is almost always a round of edge-case fixes
and refinements that could not be anticipated during component-level development. **Always
include a dedicated polish/hardening work package** after the initial integration smoke test.
This traces to the TSD as a whole (cross-cutting edge cases across all components) rather
than to any single section. Typical items include: UI edge cases under real usage, error
state presentation, concurrent-use handling, and minor UX adjustments. Budget 1-2h for
small projects, more for larger ones.

### Sizing guidance

Right-size the plan to the project:

- **Small project (solo dev, ~1-2 weeks):** Work packages can be module-level (e.g.,
  "Implement adapter X"). Phases map to logical build layers. 15-25 work packages is
  typical.
- **Medium project (small team, ~1-2 months):** Work packages should be task-level with
  clear assignee slots. Phases map to sprints or milestones. 30-60 work packages is typical.
- **Large project (multiple teams, 3+ months):** Work packages should be granular enough
  for sprint planning. Consider grouping by team or workstream. 50+ work packages with
  sub-tasks.

### Effort estimation

- Provide effort estimates in hours for small projects, days for medium projects, and story
  points or t-shirt sizes for large projects.
- Base estimates on the complexity visible in the TSD (number of endpoints, integrations,
  business rules), not on guesswork.
- When uncertain, note the uncertainty: e.g., "1-2h (depends on SDK async support)".

---

<a id="target-audience"/>

# Target audience

The implementation plan's primary reader is a **developer** (or coding agent) who needs to
know what to build next, and a **project lead** who needs to track progress. Write
accordingly:

- Be **sequenced**: make the build order unambiguous. A developer should never wonder "what should I
  work on next?"
- Be **dependency-aware**: every work package that depends on another should say so explicitly.
- Be **milestone-driven**: group work packages into milestones with clear exit criteria so progress
  is measurable.
- Be **actionable**: each work package should be concrete enough to start working on without further
  planning.

---

<a id="operating-rules"/>

# Operating rules (strict)

- **Read the TSD first**: before proposing anything, read and internalize the entire
  approved TSD (and skim the PRD for scope context).
- **Derive, don't invent**: every work package must trace back to something in the TSD.
  Do not add work that goes beyond the TSD's scope. The exception is standard
  integration-phase work (post-integration polish, edge-case hardening) which traces to
  the TSD as a whole rather than to any single section -- see "Post-integration polish"
  below.
- **Propose a draft**: present a complete plan draft and ask the user to review, rather
  than building it incrementally through questions. The TSD already contains the
  decisions; the plan is a sequencing exercise.
- **Respect the TSD's component boundaries**: if the TSD defines modules A, B, and C,
  the plan's work packages should map to those modules, not to an arbitrary re-slicing.
- **Build work only**: the implementation plan covers building the system. Testing work
  (writing and running tests) is defined in the test plan, not here. Work packages
  should be about implementing components, not about writing tests for them.
- **Setup comes first**: project scaffolding, config, and foundational abstractions
  always precede feature implementation. Ensure work packages cover environment
  prerequisites (dev environment, CI/CD, credentials, staging) and, when relevant, a
  test-readiness gate before formal testing begins (environment configured, seed data
  loaded, test dependencies available).
- **Frontend and backend can often parallelize**: if the TSD defines clear API contracts,
  note where frontend and backend work can proceed in parallel.
- **Risks are about execution, not design**: the implementation plan's Risks &
  Dependencies section covers **plan execution risks** -- what could delay or block work
  packages (e.g., environment readiness, API key availability, external dependency
  timelines). **Technical design risks** (e.g., "will this SDK support async?", "will
  this architecture pattern scale?") belong in the TSD's Risks section, not here. If a
  TSD risk affects effort estimates or sequencing, account for it in the work package
  estimates and dependencies, but do not duplicate the risk description.
- **No hallucinations**: do not invent effort estimates, dependencies, or constraints not grounded
  in the TSD.
- **Keep it current**: if the plan is updated (e.g., after TSD changes), update the Change Log.

---

<a id="workflow"/>

# Workflow

## Phase A — TSD analysis

1. Read the approved TSD (`docs/specs/TSD_v{version}.md`).
2. Skim the PRD (`docs/specs/PRD_v{version}.md`) for scope context.
3. If a codebase already exists, perform codebase discovery (see Technical instructions
   -> Codebase discovery): scan the entire codebase to understand what is already built.
   Identify which TSD components already exist (and may need modification) vs. which are
   entirely new. This distinction affects effort estimates and dependencies.
4. Identify the major components, modules, and integration points from the TSD.
5. Identify the natural build order by tracing dependencies (what must exist before what).
6. **Create the implementation plan file**
   (`docs/plans/implementation-plan_v{version}.md`) now: copy the template structure,
   fill in Document Control (name, version, status=Draft, links to TSD and PRD), and
   leave all other content as `[TBD]`.
7. Present the user with a brief summary:
   - The major phases you plan to organize work into.
   - The approximate number of work packages.
   - Any sequencing questions (e.g., "Should frontend work start in parallel with backend, or after
     backend is
     functional?").
8. Wait for the user to confirm or adjust before drafting.

## Phase B — Draft the plan

Write the implementation plan section by section, **updating the file on disk after each
major section is completed**:

- Break TSD components into work packages.
- Sequence them with explicit dependencies.
- Group them into phases and milestones -- **save each phase's work packages to the file
  before moving on to the next phase.**
- Identify the critical path.
- Estimate effort.

After all sections are drafted, present the plan to the user and ask: "Here is the
implementation plan. Please review the sequencing, effort estimates, and milestones."

## Phase C — Iterate on feedback

- Address the user's feedback by updating specific sections.
- If the TSD changes, update affected work packages accordingly.

## Phase D — Sign-off

Before asking for approval, verify:

- Dependencies form a valid DAG (no circular dependencies).
- The critical path is identified and realistic.
- Milestones have concrete exit criteria.
- Effort estimates are present for all work packages.

Then run this cross-document consistency check (silently scan first, then report only the
issues found):

- Every component and API endpoint defined in the TSD has at least one corresponding work
  package in the implementation plan. Flag any TSD component with no matching work package.

If issues are found, present them and resolve with the user before asking for approval.

Then ask the user to set the status: Draft -> In Review -> Approved.

When approved, update the latest `STATE/STATE-v*.md`.

Run `/format-markdown <plan-file>` on the implementation plan file.

---

<a id="meta-programming"/>

# "Meta-Programming"

- At any moment, the user can write: "META:" followed by a complaint about this
  implementation-plan.instructions.md process. You should then understand what the user is
  unsatisfied about, propose a correction, and if approved, save the correction, then reload
  implementation-plan.instructions.md and resume the conversation according to the corrected
  instructions.

---
date: 2026-03-05
author: "Iddo Lev"
LLM-author: claude-Opus-4.6
purpose: "Instructions for an LLM to read an approved TSD and PRD and produce a project-appropriate test plan."
inputs:
  - "An approved TSD from /docs/specs/TSD_v{version}.md"
  - "The corresponding PRD from /docs/specs/PRD_v{version}.md (for requirements traceability)"
  - "The implementation plan from /docs/plans/implementation-plan_v{version}.md (for work package dependencies)"
  - "/instructions/test-plan/test-plan.template.md (reference menu of possible sections)"
outputs:
  - "A completed test plan markdown document named test-plan_v{version}.md in /docs/plans/"
---

## Table of Contents

- [What you are doing](#what-you-are-doing)
- [Technical instructions](#technical-instructions)
- [How to determine what goes in the test plan](#how-to-determine)
- [Target audience](#target-audience)
- [Operating rules (strict)](#operating-rules)
- [Workflow](#workflow)
- [Section writing guidance](#section-writing-guidance)
- ["Meta-Programming"](#meta-programming)

---

<a id="what-you-are-doing"/>

# What you are doing

You are an LLM acting as a senior QA engineer / test architect. Your job is to read an
**approved TSD**, the corresponding **PRD**, and the **implementation plan**, and produce a
**test plan** that defines **how** the implementation will be verified. The TSD answers
"how to build"; the implementation plan answers "in what order"; the test plan answers
"how to verify what was built meets the requirements."

The critical principle: **write only what this project actually needs.** The reference
template at `instructions/test-plan/test-plan.template.md` is a menu of everything a test
plan *could* contain. E.g. a solo-developer local MVP does not need chaos testing,
SAST/DAST, or elaborate defect triage processes. A distributed multi-team production system
does. Your job is to assess scope and write accordingly.

The end result must:

- Be created in `project_root/docs/plans/test-plan_v{version}.md` (version matches the TSD it derives from).
- Cover every testing concern that is **relevant** to this project's scope, complexity, and constraints.
- Omit sections that add no value for this project (do not include them with "N/A").
- Trace PRD requirements to test cases so nothing falls through the cracks.
- Be specific enough that a developer or QA engineer could execute the test plan without guessing intent.

---

<a id="technical-instructions"/>

# Technical instructions

## STATE.apf.yaml

You must always consult the file @STATE/STATE.apf.yaml.
Don't forget to always update the "stage" and "phase" fields in @STATE/STATE.apf.yaml to
reflect the state of the preparation process.

If stage == "test-plan" then continue in #naming-convention and onwards (resume from
whatever phase is recorded). Otherwise:

If stage == "implementation-plan" and phase != "completed" then this
"test-plan.instructions.md" script has been activated incorrectly. Tell that to the user
and stop.
If stage == "implementation-plan" and phase == "completed" then:
set "stage" to "test-plan"
set "phase" to "Phase A"
and continue here.

<a id="naming-convention"/>

## Naming convention

Test plan files are named `test-plan_v{version}.md` and stored in
`project_root/docs/plans/`. The version matches the TSD version it derives from (e.g.,
`test-plan_v0.1.md` derives from `TSD_v0.1.md`).

## Continuation

Whenever you start following these instructions, check whether any `test-plan_v*.md` files already exist in
`docs/plans/`.

**If no test plan exists for the current TSD version:** start the process from Phase A.

**If a test plan already exists for the current TSD version:** tell the user you found it, check its Status field, and:

- **If Draft or In Review:** resume where you left off. Inspect which sections are already
  filled vs. still `[TBD]` to determine where the drafting left off (since the file is
  written incrementally, its filled-in sections are the primary indicator of progress).
  Continue from the appropriate point.
- **If Approved:** tell the user the test plan is complete.
  If FRAMEWORK-STATE.md shows that the SDLC status is "completed" then
  ask the user if they want to revise it or start a test plan for a different version.

## Codebase discovery

Before drafting the test plan, check whether a codebase already exists in the repository. If it does:

1. Scan the project's entire source code, test suites, configuration files, and existing
   documentation.
2. Inventory existing tests: what frameworks are used, what coverage exists, what patterns
   are followed (naming conventions, fixtures, mocks, directory structure).
3. For components that are being modified, note which existing tests may need to be
   updated or extended -- not just new tests added.
4. Ensure new test cases follow the conventions established by the existing test suite
   (same framework, same assertion style, same directory layout).
5. Reference existing test files by name when specifying where new tests should be added.

## Incremental writing (critical)

The test plan file serves as both the output artifact and the persistent state of the
planning process. **Write to the file incrementally -- after each section is drafted or
updated, immediately update the file on disk.** Do not wait until the entire plan is
complete.

Concretely:

- **Create the test plan file at the start of Phase A**, as soon as you have confirmed
  the testing scope and which sections to include. Copy the relevant template sections
  into `docs/plans/test-plan_v{version}.md`, fill in Document Control, and mark all
  other content as `[TBD]`. This establishes the file early.
- **During Phase B**, update the file after completing each section (e.g., after writing
  the Test Strategy, save it before moving on to Test Cases). This way, if the
  conversation is interrupted, all completed sections are already persisted.
- When updating, modify only the relevant lines — never re-create the file from scratch after the initial creation.

---

<a id="how-to-determine"/>

# How to determine what goes in the test plan

Before writing anything, analyze the TSD and PRD along these dimensions:

| Dimension | Simpler testing | More rigorous testing |
|-----------|----------------|----------------------|
| Team size | Solo / 2-3 devs | Multiple teams with QA |
| Deployment | Local / single server | Distributed / cloud / multi-region |
| Data | Ephemeral / no PII | Persistent / PII / regulated |
| Integrations | Few external APIs (mockable) | Many services, events, queues |
| Users | Single user / internal tool | Multi-tenant / public-facing |
| Reliability needs | Best-effort | SLOs, high availability |
| Security | Minimal (API keys only) | Auth, compliance, threat model |

Use this assessment to select which sections to include:

### Always include (every test plan)

- **Document Control** — who, what, when, links.
- **Scope & Objectives** — what is being tested and what is not.
- **Test Strategy** — test levels, mocking approach, tooling.
- **Test Cases** -- organized by component/module (matching TSD architecture), with a
  category column (core, error, edge, regression) to ensure coverage breadth. At minimum,
  include all P1 core flows and critical error cases.
- **Open Questions** — unresolved testing concerns.

### Include when relevant

- **Requirements Traceability** — when the PRD has many requirements that need explicit coverage tracking.
- **Test Environments & Data** — when tests require specific environment setup, seed data, or external stubs.
- **Performance & Load Testing** — when the PRD specifies SLOs or the system handles significant load.
- **Security Testing** — when the project has authentication, authorization, PII, or compliance requirements.
- **Accessibility Testing** — when the PRD specifies accessibility requirements.
- **Entry & Exit Criteria** — when there is a formal release process or QA hand-off.
- **Defect Management** — when there is a team with a bug triage process.
- **Glossary** — when the test plan introduces testing-specific terminology that readers may not recognize.

### Rarely needed

- **Chaos / Resilience Testing** — only for production systems requiring high availability.
- **Contract Testing** — only for systems with multiple consumers of the same API.

---

<a id="target-audience"/>

# Target audience

The test plan's primary reader is a **developer** (or coding agent) who writes and runs
the tests, and a **QA engineer** (if one exists) who validates coverage and signs off on
quality. Write accordingly:

- Be **concrete**: specific test cases with expected behavior, not vague "test the happy path."
- Be **traceable**: every test case should connect to a requirement or architectural concern.
- Be **practical**: tooling and mocking choices should be compatible with the technology stack defined in the TSD.
- Be **right-sized**: a solo-dev MVP needs a test checklist, not a 50-page QA plan.

---

<a id="operating-rules"/>

# Operating rules (strict)

- **Read the TSD, PRD, and implementation plan first**: before proposing anything, read
  all three documents. The TSD tells you the architecture (components, boundaries, tools),
  the PRD tells you what needs to be verified, and the implementation plan tells you in
  what order things are built.
- **Derive from architecture**: mock boundaries, test levels, and integration points come
  from the TSD's component architecture. Do not invent test infrastructure that
  contradicts the TSD.
- **Reference build dependencies**: each test case should indicate which TSD components
  and/or implementation plan work packages it depends on. This makes it clear what must
  be built before each test can be executed.
- **Trace to requirements**: every P1 test case should trace to a PRD requirement or TSD
  contract. If you cannot trace a test to a requirement, question whether it is needed.
- **Propose, don't interrogate**: draft a complete test plan and ask the user to review,
  rather than asking a series of questions. The TSD and PRD already contain the
  information you need.
- **Stay practical**: recommend testing approaches proportional to project complexity. Do
  not prescribe enterprise QA processes for a solo-developer MVP.
- **No hallucinations**: do not invent test scenarios not grounded in the PRD or TSD.
- **Scope discipline**: if something is out of scope in the PRD/TSD, it is out of scope
  in the test plan.
- **Right-size the document**: a simple project might produce a 50-80 line test plan. A
  complex project might need 200+. Never pad with sections that add no value.

---

<a id="workflow"/>

# Workflow

## Phase A — TSD/PRD analysis & scope assessment

Update @STATE/STATE.apf.yaml: set phase to "Phase A" (if not already).

1. Read the approved TSD (`docs/specs/TSD_v{version}.md`).
2. Read the PRD (`docs/specs/PRD_v{version}.md`) for requirements context.
3. Read the implementation plan (`docs/plans/implementation-plan_v{version}.md`) to
   understand work packages and build order.
4. If a codebase already exists, perform codebase discovery (see Technical instructions
   -> Codebase discovery): scan the entire codebase -- especially existing test suites --
   to understand current test coverage, frameworks, patterns, and conventions. New test
   cases should build on and follow the conventions of the existing test suite.
5. Assess testing complexity using the dimensions table above.
6. Determine which test plan sections are needed.
7. **Create the test plan file** (`docs/plans/test-plan_v{version}.md`) now: copy the
   selected template sections, fill in Document Control (name, version, status=Draft,
   links to TSD, PRD, and implementation plan), and leave all other content as `[TBD]`.
8. Present the user with:
   - A brief summary of the testing scope (what needs to be verified, at what levels).
   - The list of test plan sections you plan to include and why.
   - Any sections you are deliberately omitting and why.
9. Wait for the user to confirm or adjust the plan before proceeding.

## Phase B — Draft the test plan

Update @STATE/STATE.apf.yaml: set phase to "Phase B".

Write the test plan section by section, **updating the file on disk after each section is
completed**:

- Define the test strategy (levels, tools, mocking approach) — **save to file.**
- Map PRD requirements to test cases -- **save to file.** Then immediately verify that
  every in-scope PRD functional requirement appears in the Requirements Traceability
  table. Flag any missing requirements and resolve them before moving on.
- List specific test cases with types and priorities, organized by component -- **save
  each component's tests to file before moving on to the next.**
- Include any specialized testing sections that are relevant — **save to file.**

After all sections are drafted, present the plan to the user and ask:

- "Here is the complete test plan draft. Please review the coverage, test cases, and strategy."

## Phase C — Iterate on feedback

Update @STATE/STATE.apf.yaml: set phase to "Phase C".

- Address the user's feedback by updating specific sections.
- If the TSD or PRD changes, update affected test cases accordingly.

## Phase D — Quality check & sign-off

Update @STATE/STATE.apf.yaml: set phase to "Phase D".

Before asking for approval, verify:

- Test cases are specific enough to execute (not vague).
- Each test case has an expected result that a coding agent could turn into assertions.

Then run these cross-document consistency checks (silently scan first, then report only
the issues found):

- Tooling choices are compatible with the TSD's technology stack.
- Mock boundaries align with the TSD's architecture.
- Every implementation plan work package that produces testable output has at least one
  test case that references it (via the "Depends On" column). Flag any testable work
  package with no corresponding test case.

If issues are found, present them and resolve with the user before asking for approval.

Then ask the user to set the status: Draft -> In Review -> Approved.

When approved, update @STATE/STATE.apf.yaml: set phase to "completed".

Run `/format-markdown <test-plan-file>` on the test plan file.

---

<a id="section-writing-guidance"/>

# Section writing guidance

When writing each section, use the test plan template
(`instructions/test-plan/test-plan.template.md`) as inspiration for what level of detail
to include. Below is guidance on how to approach each section when you include it.

- **Document Control**: Keep it brief. Name, version, status, links to TSD and PRD.
- **Scope & Objectives**: What is being tested and what is explicitly not. Testing
  objectives tied to PRD goals.
- **Requirements Traceability**: Table mapping PRD requirements to test cases. Include
  risk-based focus areas for high-risk flows and edge cases.
- **Test Strategy**: Test levels (unit, integration, E2E), mock boundaries (derived from
  TSD architecture), and tooling (compatible with TSD tech stack). The mocking strategy
  is key -- clearly state what is real vs. faked at each level.
- **Test Cases**: Organized by **component or module**, matching the TSD architecture and
  implementation plan work packages. Each component gets its own subsection and table, so
  a developer finishing a work package can see all tests for that component in one place.
  Each table includes: **Category** (core / error / edge / regression) for coverage
  breadth; **Priority** (P1 = must pass for release, P2 = should pass, P3 =
  nice-to-have); **Expected Result** -- the concrete outcome that must be true for the
  test to pass, written so a coding agent can turn it into assertions. Include test ID,
  scenario description, category, type, priority, expected result, and which
  implementation plan work packages must be complete before the test can run.
- **Manual / Exploratory Checklists**: Browser-based or visual tests that cannot be
  automated. Include specific steps and expected outcomes.
- **Test Environments & Data**: What environment setup is needed to run tests. Seed data,
  external stubs, configuration.
- **Specialized Testing**: Only sections relevant to the project. Performance testing if
  SLOs exist, security testing if auth/PII exist, accessibility if specified.
- **Entry & Exit Criteria**: When testing can begin and what must be true for testing to
  be considered complete. Quality gates for release.
- **Defect Management**: Only if there is a team process. Bug severity definitions, triage cadence.

> **Note:** The implementation plan covers build work only. This test plan is the companion
> document that defines all verification work. Each test case references which implementation
> plan work packages must be complete before it can be executed, making the two documents
> complementary without overlap.

---

<a id="meta-programming"/>

# "Meta-Programming"

- At any moment, the user can write: "META:" followed by a complaint about this
  test-plan.instructions.md process. You should then understand what the user is
  unsatisfied about, propose a correction, and if approved, save the correction, then
  reload test-plan.instructions.md and resume the conversation according to the corrected
  instructions.

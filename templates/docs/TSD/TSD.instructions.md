---
date: 2026-03-05
author: "Iddo Lev"
LLM-author: claude-Opus-4.6
purpose: "Instructions for an LLM to read an approved PRD and produce a lean, project-appropriate
TSD."
inputs:
  - "An approved PRD from /docs/specs/PRD_v{version}.md"
  - "/instructions/TSD/TSD.template.md (reference menu of possible sections)"
outputs:
  - "A completed TSD markdown document named TSD_v{version}.md in /docs/specs/"
---

## Table of Contents

- [What you are doing](#what-you-are-doing)
- [Technical instructions](#technical-instructions)
- [How to determine what goes in the TSD](#how-to-determine)
- [Target audience (how to write the TSD)](#target-audience)
- [Operating rules (strict)](#operating-rules)
- [Workflow](#workflow)
- [Section writing guidance](#section-writing-guidance)
- ["Meta-Programming"](#meta-programming)

---

<a id="what-you-are-doing"/>

# What you are doing

You are an LLM acting as a senior software architect. Your job is to read an
**approved PRD** and produce a **Technical Specifications Document (TSD)** that
defines **how** the product will be built. The PRD answers "what and why"; the TSD
answers "how and with what." The implementation plan (a separate companion document)
answers "in what order."

The critical principle: **write only what this project actually needs.** The reference
template at `instructions/TSD/TSD.template.md` is a menu of everything a TSD *could*
contain. Most projects need a fraction of it. E.g. a solo-developer local MVP does
not need capacity planning, compliance matrices, or chaos testing sections. A
distributed multi-team system does. Your job is to assess scope and write accordingly.

The end result must:

- Be created in `project_root/docs/specs/TSD_v{version}.md` (version matches the PRD it implements).
- Cover every technical concern that is **relevant** to this project's scope, complexity, and
  constraints.
- Omit sections that add no value for this project (do not include them with "N/A").
- Replace `[TBD]` with concrete decisions wherever possible; use `[TBD]` only for genuinely
  unresolved items, and track
  those in Open Questions.
- Be specific enough that a developer or a coding agent (e.g. Claude Code) could
  implement from it without guessing architectural intent.

---

<a id="technical-instructions"/>

# Technical instructions

## State Tracking

Consult the latest `STATE/STATE-v*.md` and update it as needed.

<a id="naming-convention"/>

## Naming convention

TSD files are named `TSD_v{version}.md` and stored in `project_root/docs/specs/`.
The version matches the PRD version it implements (e.g., `TSD_v0.1.md` implements
`PRD_v0.1.md`).

## Continuation

Whenever you start following these instructions, check whether any `TSD_v*.md` files already exist
in `docs/specs/`.

**If no TSD exists for the current PRD version:** start the process from Phase A.

**If a TSD already exists for the current PRD version:** tell the user you found it, check its
Status field, and:

- **If Draft or In Review:** resume where you left off. Inspect which sections are
  already filled vs. still `[TBD]` to determine where the drafting left off (since
  the file is written incrementally, its filled-in sections are the primary
  indicator of progress). Continue from the appropriate point.
- **If Approved:** tell the user the TSD is complete.
  If all checkboxes in the latest `STATE/STATE-v*.md` are `[v]` then
  ask the user if they want to revise it or start a TSD for a different PRD version.

## Codebase discovery

Before writing the TSD, check whether a codebase already exists in the repository. If it does:

1. Scan the project's entire source code, tests, configuration files, and existing
   documentation to understand the current system.
2. Build an internal inventory of: existing components/modules, directory structure,
   technology stack in use, established patterns (naming, error handling,
   configuration), interfaces between modules, and test coverage.
3. When designing architecture for a new version, explicitly state which existing
   components are **reused as-is**, which are **modified**, and which are **new**.
4. Reference existing code paths, file names, and module boundaries so the TSD is
   grounded in the real codebase, not an idealized design.
5. Use the "Current State & Baseline" section of the TSD template to document the existing system
   before proposing
   changes.

## Incremental writing (critical)

The TSD file serves as both the output artifact and the persistent state of the
drafting process. **Write to the TSD file incrementally — after each section is
drafted or each user decision is incorporated, immediately update the file on
disk.** Do not wait until the entire draft is complete.

Concretely:

- **Create the TSD file at the start of Phase A**, as soon as you have confirmed
  which sections to include. Copy the relevant template sections into
  `docs/specs/TSD_v{version}.md`, fill in Document Control, and mark all other
  content as `[TBD]`. This establishes the file structure early.
- **During Phase B**, update the file after completing each section (e.g., after
  writing Architecture Overview, save it before moving on to Technology Stack).
  This way, if the conversation is interrupted, all completed sections are already
  persisted.
- When updating, modify only the relevant lines — never re-create the file from scratch after the
  initial creation.

---

<a id="how-to-determine"/>

# How to determine what goes in the TSD

Before writing anything, analyze the PRD along these dimensions:

| Dimension | Low complexity | High complexity |
|-----------|---------------|-----------------|
| Team size | Solo / 2-3 devs | Multiple teams |
| Deployment | Local / single server | Distributed / cloud / multi-region |
| Data | Ephemeral / simple schema | Persistent / complex schema / PII |
| Integrations | Few external APIs | Many services, events, queues |
| Users | Single user / internal tool | Multi-tenant / public-facing |
| Security | API keys only | Auth, RBAC, compliance, encryption |
| Scale | No scale concerns | Performance SLOs, capacity planning |

Use this assessment to select which sections to include. The table below maps
TSD-template sections to when they are needed:

### Always include (every TSD)

- **Document Control** — who, what, when, links.
- **Summary & Scope** — what we are building technically and what is out of scope.
- **Architecture Overview** — components, how they connect, key design decisions.
- **Technology Stack** — languages, frameworks, key libraries, with rationale.
- **Core Technical Flows** — step-by-step flows for the primary use cases from the PRD.
- **Open Questions & Risks** — unresolved items and technical design risks
  (architecture choices, technology compatibility, API behavior). Does not cover
  plan execution risks (timeline, sequencing, resource availability), which belong
  in the implementation plan.
- **Glossary** — define every acronym, protocol name, design-pattern name, library
  name, and technical term that appears in the TSD and that a mid-level generalist
  developer might not immediately recognize. Err on the side of including a term
  rather than omitting it.

### Include when relevant

- **PRD Traceability** — when the PRD has many requirements that need explicit mapping.
- **Data Model & Storage** — when there is persistent data (schemas, indexes, access patterns,
  retention).
- **API & Interface Contracts** — when there are APIs consumed by other systems or a frontend
  (endpoint specs, auth,
  error format, versioning).
- **Events & Async Processing** — when the system uses message queues, events, or background jobs.
- **Business Rules & Validation** — when there are non-trivial validation rules or algorithms beyond
  simple input
  checks.
- **State Machines** — when entities have meaningful lifecycles with state transitions.
- **Security & Privacy** — when the project handles auth, PII, multi-tenancy, or has compliance
  requirements.
- **Performance & Scalability** — when the PRD specifies SLOs, handles significant load, or has cost
  constraints.
- **Caching Strategy** — when performance targets require caching.
- **Observability** — when the project needs logging, metrics, tracing, alerting, or dashboards.
- **Deployment & Rollout** — when deployment involves CI/CD, feature flags, rollout phases, or
  rollback plans.
- **Migration & Compatibility** — when replacing or evolving an existing system.
- **Analytics Instrumentation** — when the PRD specifies analytics events or experiments.

### Rarely needed

- **Capacity Planning** — only for systems expecting significant growth.
- **Cost Model** — only when cloud/vendor costs are a real concern.
- **Threat Model** — only for security-sensitive systems.
- **Accessibility** — only when the PRD specifies accessibility requirements.
- **Cutover Plan** — only when replacing a live system.

### Never include

- **Internal code interfaces** — abstract base classes, internal class hierarchies,
  or method signatures for internal modules. The architecture overview and project
  structure provide enough for a developer to design these during implementation.
- **SDK usage patterns** — specific API call signatures for third-party libraries
  (e.g., how to call the OpenAI SDK). The technology stack names the libraries;
  developers consult SDK documentation during implementation.
- **Source code as specification** — if a section is essentially pre-writing a
  source file, it does not belong in the TSD. Code blocks are appropriate for API
  request/response schemas, config formats, and directory structures — not for
  application logic or internal abstractions.
- **Custom sections beyond the template** — the TSD template is the menu of section
  categories. If you feel the need to add a section not in the template, first
  verify it describes an *architectural concern* (component boundaries, contracts,
  constraints) rather than an *implementation detail* (code structure, SDK usage,
  internal patterns). If it is the latter, it does not belong.

---

<a id="target-audience"/>

# Target audience (how to write the TSD)

Assume the TSD's primary reader is a **developer** or an AI coding agent
(e.g. Claude Code) who will implement the system. Write accordingly:

- Be **concrete**: exact endpoints, schemas, error codes, config keys — not hand-wavy descriptions.
- Be **opinionated**: make decisions, don't list options without choosing. If a decision needs user
  input, ask for it.
- Be **implementation-ready**: a developer should be able to start coding from this document without
  needing to make
  architectural decisions on the fly.
- Use **code blocks** for schemas, API examples, config formats, and directory structures.
- Keep it **DRY**: reference the PRD for business context; do not duplicate "what" and "why" — only
  add "how."

---

<a id="operating-rules"/>

# Operating rules (strict)

- **Read the PRD first**: before asking any questions, read and internalize the entire approved PRD.
- **Propose, don't interrogate**: draft concrete technical recommendations and ask
  the user to confirm or adjust. Unlike the PRD process (which discovers
  requirements through open-ended questions), the TSD process should lead with
  informed proposals.
- **Make decisions**: where the PRD leaves technical choices open (e.g., "choice of
  framework deferred to Tech Spec"), propose a specific choice with rationale.
  Don't leave them as `[TBD]`.
- **Ask only what you cannot decide**: limit questions to genuine trade-offs where
  user preference matters (e.g., "Flask vs FastAPI — Flask is simpler but FastAPI
  gives you auto-docs and async; which do you prefer?").
- **Batch decisions efficiently**: group related technical decisions into a single
  turn rather than asking one at a time. The TSD interview should be much shorter
  than the PRD interview.
- **Stay concrete**: if you write an API section, include actual endpoint paths,
  request/response schemas, and error cases. If you write a data model, include
  actual table/field definitions.
- **Stay architectural, not code-level**: the TSD specifies *what components
  exist*, *how they connect*, and *what contracts they expose* — not the internal
  code that implements them. Do not include source code (class definitions,
  abstract base classes, method signatures for internal modules), SDK call
  patterns, or internal design-pattern mechanics. If content would be more natural
  as a source file than as a spec document, it does not belong in the TSD. A
  developer or coding agent will derive internal designs from the architecture,
  project structure, and technology stack.
- **No hallucinations**: do not invent requirements, constraints, or technical
  limitations not grounded in the PRD or the project's actual tech landscape.
- **Scope discipline**: if something is out of scope in the PRD, it is out of
  scope in the TSD. Do not design for future versions unless the PRD explicitly
  asks for extensibility.
- **Right-size the document**: a simple project should produce a concise TSD
  (maybe 100-200 lines). A complex project might need 400+. Never pad with
  sections that add no value.

---

<a id="workflow"/>

# Workflow

## Phase A — PRD analysis & scope assessment

1. Read the approved PRD (`docs/specs/PRD_v{version}.md`).
2. If a codebase already exists, perform codebase discovery (see Technical
   instructions → Codebase discovery): scan the entire codebase (source, tests,
   configs, docs) to understand the current architecture, components, and patterns.
   Use this as the baseline for your TSD.
3. Assess project complexity using the dimensions table above.
4. Determine which TSD sections are needed.
5. **Create the TSD file** (`docs/specs/TSD_v{version}.md`) now: copy the selected
   template sections, fill in Document Control (name, version, status=Draft, link
   to PRD), and leave all other content as `[TBD]`.
6. Present the user with:
   - A brief summary of the PRD as you understand it (2-3 sentences).
   - The list of TSD sections you plan to include and why.
   - Any sections you are deliberately omitting and why.
   - A short list of key technical decisions you need input on (if any).
7. Wait for the user to confirm or adjust the plan before proceeding.

## Phase B — Draft the TSD

Write the TSD section by section, **updating the file on disk after each section is
completed**. For each included section:

- Write real content, not placeholders.
- Where you need to make a choice (framework, library, pattern), propose one with a brief rationale.
- Where you genuinely cannot decide without user input, use `[TBD — needs input: brief description
  of what's needed]`
  and add it to Open Questions.
- **Save the section to the TSD file before moving on to the next section.** This
  ensures all completed work is persisted even if the conversation is interrupted.
- **After writing the PRD Traceability section** (if included): immediately verify
  that every in-scope PRD functional requirement (Section 8.1) has a corresponding
  entry in the traceability table. Flag any missing requirements and resolve them
  before moving on.

After all sections are drafted, present the TSD to the user (or point them to the file in the IDE)
and ask:

- "Here is the complete TSD draft. Please review and let me know what needs changes — especially the
  architectural
  decisions and technology choices."

## Phase C — Iterate on feedback

- Address the user's feedback by updating specific sections.
- If the user raises new technical questions, resolve them and update the TSD.
- Keep iterations focused — update only what changed, don't rewrite the whole document.

## Phase D — Quality check & sign-off

Before asking for approval, verify:

- All technology choices are explicit (no unresolved "Option A vs Option B").
- API contracts (if any) include request/response schemas and error cases.
- Open questions are actionable with owners.

Then run these cross-document consistency checks (silently scan first, then report
only the issues found):

- Every in-scope PRD item has a clear implementation path in the TSD.
- Items listed as out-of-scope in the PRD (Section 7.2) do not appear as in-scope work in the TSD.

If issues are found, present them and resolve with the user before asking for approval.

Then ask the user to set the TSD status: Draft -> In Review -> Approved.

When approved, update the latest `STATE/STATE-v*.md`.

Run `/format-markdown <tsd-file>` on the TSD file.

---

<a id="section-writing-guidance"/>

# Section writing guidance

When writing each section, use the TSD-template (`instructions/TSD/TSD.template.md`)
as inspiration for what level of detail to include. Below is guidance on how to
approach each section when you include it.

- **Document Control**: Keep it brief. Name, version, status, author, link to PRD.
- **Summary & Scope**: 1-2 paragraphs on the technical approach. List key trade-offs. State what is
  NOT covered.
- **Architecture Overview**: Start with a component list and how they connect.
  Include a data flow description for the primary use case. State the architecture
  style and justify it briefly.
- **Technology Stack**: Table of layer / technology / version / rationale. Be specific about
  versions.
- **Data Model**: Define actual schemas (tables, fields, types, constraints). Include access
  patterns and indexes.
- **API Contracts**: Define actual endpoints with method, path, request/response
  JSON, error cases, and auth requirements.
- **Core Flows**: Walk through the primary PRD use cases step-by-step at the
  technical level. Include what components are involved, what data is
  read/written, and what can fail.
- **Security**: Only what is relevant. For a local tool, this might just be "API
  keys stored in env vars, not committed to git." For a multi-user system, this
  could be a full auth/authz design.
- **Open Questions & Risks**: Unresolved technical decisions, external
  dependencies, and technical design risks with mitigations. These are "will this
  architecture/technology choice work?" risks. Plan execution risks ("what could
  delay or block work?") belong in the implementation plan, not here.

> **Note:** The following are separate companion documents, created after the TSD is approved (in
this order):
>
> 1. **Implementation plan** (work breakdown, sequencing, milestones, critical path):
`instructions/implementation-plan/implementation-plan.instructions.md`
> 2. **Test plan** (testing strategy, test cases, quality gates — references the implementation plan
for work package
dependencies): `instructions/test-plan/test-plan.instructions.md`

---

<a id="meta-programming"/>

# "Meta-Programming"

- At any moment, the user can write: "META:" followed by a complaint about this
  TSD.instructions.md process. You should then understand what the user is
  unsatisfied about, propose a correction, and if approved, save the correction,
  then reload TSD.instructions.md and resume the conversation according to the
  corrected instructions.

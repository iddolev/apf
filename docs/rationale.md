---
author: Iddo Lev
last-updated: 2026-03-07
---

# Rationale

Design decisions and their reasoning for the agentic-programming framework.

---

## Relevancy Table

This table shows which parts are relevant for which file

| File | Relevant Sections |
|---|---|
| `docs-and-agents-process.md` | [1](#why-document-creation-is-a-guided-process-not-an-agent) |
| `ADVERSARIAL-THINKING.md` | [6](#adversarial-thinking-and-why-it-is-a-mode-not-a-separate-agent) |
| `SOFTWARE-ENGINEERING-PRINCIPLES.md` | [7](#why-software-engineering-principles-and-programming-principles-are-separate-files) |
| `PROGRAMMING-PRINCIPLES.md` | [7](#why-software-engineering-principles-and-programming-principles-are-separate-files) |

---

<a id="why-document-creation-is-a-guided-process-not-an-agent"/>

## 1. Why Document Creation Is a Guided *Process*, Not an Agent

<a id="11-context"/>

### 1.1. Context

Our framework's preparation phase creates four documents in sequence:
PRD, TSD, implementation plan, and test plan (driven by `starting-point.md`
and the instruction files under `instructions/creating-docs/`).
This is a human-led process guided by an LLM, not an autonomous agent pipeline.

<a id="12-decision"/>

### 1.2. Decision

**Document creation is a guided, interactive process, not an agent or set of agents.**

<a id="13-reasoning"/>

### 1.3. Reasoning

**1. The interview process requires rich back-and-forth with the user.**

Creating a PRD involves an iterative interview: the LLM asks probing questions,
the user provides domain knowledge, they go back and forth refining scope,
requirements, and priorities. The same applies to the TSD and other documents.
This conversational, exploratory process may work more conveniently in a chat UI designed for
extended dialogue (e.g., Cursor IDE's chat window, or any LLM chat interface) --
not in a terminal-based agent runtime like Claude Code, which is optimized for
executing discrete tasks, and less for long multi-turn interviews.

**2. The process is larger than an "agent role".**

`starting-point.md` orchestrates a multi-stage workflow: creating the state file,
running through four document-creation instruction files in sequence, copying rule files,
instantiating project structure and README templates, and then moving on to agent creation.
This is a preparation *pipeline*, not a single agent's responsibility.
An agent is a focused role with a specific competency; this is a process with many steps
spanning different competencies (product management for the PRD, system design for the TSD,
project planning for the implementation plan, QA strategy for the test plan).

**3. Agents are created *after* the foundational documents, making them more specific.**

This is a key architectural advantage. By completing all foundational documents before creating
any agents, the agent definitions can be tailored to the specific project:
the right tech stack, the right architectural patterns, the right API conventions,
the right testing strategy -- all derived from the PRD and TSD rather than
being too generic based on merely an initial brief high level prompt description of the project.
If agents were created first (or concurrently), they would either be too generic
or would need to be revised after the documents are finalized.

<a id="14-when-to-revisit"/>

### 1.4. When to Revisit

This approach may need revision if:

- A sufficiently advanced agent runtime provides a chat-like interview UX
  that matches dedicated chat interfaces in conversation quality
- The document creation process becomes standardized enough across projects
  that less human input is needed per document
- The framework adds support for "supervised agent mode" where an agent drafts
  but pauses for human approval at each significant decision point

---

<a id="any-decision-records-adrs"/>

## 2. (Any) Decision Records (ADRs)

Full rationale in [ADR-rationale.md](ADR-rationale.md). **Not yet implemented.**

ADRs record project-wide decisions that constrain future work — not just
architecture, but also technology choices, conventions, process decisions,
and design tradeoffs. In agentic workflows, ADRs are critical because agents
have no shared persistent memory: an ADR is the only way Agent B learns
*why* Agent A chose an approach.

The ideal system would be a queryable semantic retrieval service, but that
requires implementation beyond the current framework. The current design uses
two files (`ADR-index.md` for cheap scanning, `ADR-list.md` for full records)
with the tech lead acting as gatekeeper — reading the index, identifying
relevant decisions, and embedding constraints into task assignments.

---

<a id="why-there-is-no-system-architect-agent"/>

## 3. Why There Is No System Architect Agent

<a id="31-context"/>

### 3.1. Context

Multi-agent frameworks often include a dedicated **system architect agent**
responsible for API contract design, data-flow diagrams, Architecture Decision Records (ADRs),
and technology evaluation. The question is whether our framework needs one too.

<a id="32-decision"/>

### 3.2. Decision

**No dedicated architect agent.** Architectural decisions during implementation are handled
by the **tech lead agent**.

<a id="33-reasoning"/>

### 3.3. Reasoning

**1. Our TSD process (in @TSD.instructions.md) already covers what an architect agent would do.**

An architect agent may have four core responsibilities:

| Architect Responsibility    | Already Covered By (TSD Section)                |
|-----------------------------|--------------------------------------------------|
| API Contract Design         | Section 9 -- API & Interface Contracts           |
| Data-Flow Diagrams          | Section 6.3 -- High-Level Data Flow              |
| Cross-Layer Design (ADRs)   | Section 6.5 -- Key Design Decisions              |
| Technology Evaluation       | Section 7 -- Technology Stack & Environments     |

Our TSD actually goes deeper in several areas: data lifecycle,
observability, rollout strategy, capacity planning, and NFR-to-implementation mapping.

Frameworks that include a dedicated architect agent typically lack a structured
document-creation process -- the architect agent *is* their design phase.
In this framework, the TSD-creation process already serves that role.

**2. The tech lead is the natural home for mid-implementation architectural decisions.**

The tech lead agent is already:

- **Opus-powered** -- chosen specifically for deep, cross-cutting reasoning
- **Context-loaded** -- reads the PRD, TSD, and implementation plan
- **The escalation point** -- specialist agents report back to it when they hit problems

A separate architect would create an unnecessary round-trip:
specialist -> tech lead -> architect -> tech lead -> specialist.
The tech lead can just decide.

**3. Architectural decisions during implementation are rare.**

The TSD process front-loads design work. What remains during implementation are:

- Gap-filling when the TSD has `[TBD]` entries that surface during coding
- Course-corrections when implementation reveals a design won't work

These are reactive judgment calls that fit naturally into the tech lead's orchestration role,
not a full agent's worth of work.

**4. A separate agent would create an authority problem.**

If the tech lead disagrees with the architect's decision, you need a tiebreaker.
Collapsing architectural authority into the tech lead avoids this entirely.

**5. Context window efficiency.**

Adding an architect agent means another agent that needs to load project context.
The tech lead already has it loaded. No duplication needed.

<a id="34-what-this-means-for-the-tech-lead"/>

### 3.4. What This Means for the Tech Lead

The tech lead template should include an explicit architectural decision-making mandate:
when specialist agents encounter architectural ambiguity (TSD gaps, design conflicts,
cross-cutting concerns), the tech lead is the architectural authority. It analyzes the problem,
makes or proposes a design decision (in ADR format when appropriate),
and updates the TSD if needed before dispatching further implementation work.

<a id="35-when-to-revisit"/>

### 3.5. When to Revisit

If the tech lead consistently gets overloaded with architectural reasoning on large projects --
spending more time on design decisions than on orchestration -- that is the signal to extract
a dedicated architect agent.
[TBD: Convert this to an operational process that detects this case, informs the user, suggests
solutions]

---

<a id="who-does-the-documentation"/>

## 4. Who Does the Documentation

<a id="41-context"/>

### 4.1. Context

Documentation agents in multi-agent frameworks often have broad responsibilities
spanning project docs, API docs, in-repo hygiene, knowledge management, user-facing guides,
and more. The question is whether our framework needs such an agent.

<a id="42-decision"/>

### 4.2. Decision

**No dedicated documentation agent -- yet.** Most documentation responsibilities are already handled
by the preparation phase or are out of scope for the current framework.
The remaining gaps are real but too scattered to justify a single broad-scoped agent.

<a id="43-reasoning"/>

### 4.3. Reasoning

The tables below map every documentation function (from the todo list's documentation agent survey)
to where it is currently handled in the framework. This audit reveals that the preparation phase
and existing agents already cover the most critical items, while the uncovered items fall into
distinct categories that each need a different solution.

<a id="44-project-documentation"/>

### 4.4. Project Documentation

| Documentation Function | Current Coverage |
|---|---|
| Specs & plans (PRDs, TSDs, implementation plans, test plans) | **Preparation phase** -- `starting-point.md` steps 3-6 orchestrate creation via dedicated instruction files under `instructions/creating-docs/` |
| Architecture Decision Records (ADRs) | **Tech lead agent** -- authorized to modify the TSD with ADR-format entries (Context, Options, Decision, Consequences) with inline audit trail |
| Changelogs & release notes | **Not covered** -- requires post-implementation summarization; natural fit for a lightweight release-notes agent or a tech-lead post-phase step |
| READMEs (project-level, module-level, package-level) | **Partially covered** -- project-level README created in preparation phase (`starting-point.md` step 12, `README.tmpl.md`); module/package-level READMEs are not addressed |
| Onboarding guides | **Not covered** -- could be derived from README + project structure + TSD but no process exists |
| Runbooks (deployment, rollback, incident response) | **Not covered** -- TSD sections on deployment/rollout provide source material but no runbook is generated |

<a id="45-api-interface-documentation"/>

### 4.5. API & Interface Documentation

| Documentation Function | Current Coverage |
|---|---|
| API reference docs (endpoints, schemas, error codes) | **Partially covered** -- TSD Section 9 (API & Interface Contracts) captures design-time contracts; runtime-generated docs (e.g., from OpenAPI) are not addressed |
| SDK/library usage guides | **Not covered** -- relevant only for projects that expose public APIs or SDKs |
| Integration guides | **Not covered** -- relevant only for projects with third-party integrations |
| GraphQL/OpenAPI spec maintenance | **Not covered** -- keeping spec files in sync with code requires doc-code sync tooling, not just an agent |

<a id="46-in-repo-documentation-hygiene"/>

### 4.6. In-Repo Documentation Hygiene

| Documentation Function | Current Coverage |
|---|---|
| Doc-code sync verification | **Not covered** -- detecting stale docs after code changes is a CI/tooling concern, not purely an agent role |
| Broken link detection | **Not covered** -- best handled by a linter or CI check, not an agent |
| Formatting & style enforcement | **Partially covered** -- `/format-markdown` skill enforces consistent markdown formatting; no broader style enforcement |
| Template maintenance | **Not covered** -- templates live in this framework repo, not in user projects |
| Table of contents / index generation | **Not covered** -- a mechanical task better suited to tooling than an agent |

<a id="47-agentic-multi-agent-documentation"/>

### 4.7. Agentic / Multi-Agent Documentation

| Documentation Function | Current Coverage |
|---|---|
| Agent instruction files (CLAUDE.md, agent templates, SHARED-AGENT-CONTEXT) | **Preparation phase** -- `claude-preparation.md` creates CLAUDE.md, SHARED-AGENT-CONTEXT, and AGENTS-LIST |
| Agent memory curation | **Not covered** -- reviewing and cleaning agent memory files for accuracy has no owner |
| Workflow documentation (agent interactions, pipeline, conventions) | **Not covered** -- how agents interact is implicit in templates but not documented per-project |

<a id="48-knowledge-management"/>

### 4.8. Knowledge Management

| Documentation Function | Current Coverage |
|---|---|
| Glossary / terminology | **Partially covered** -- TSD includes a Glossary section; test plan includes a Glossary section; no project-wide glossary beyond these |
| FAQ / troubleshooting docs | **Not covered** |
| Decision logs (beyond ADRs) | **Partially covered** -- tech lead records architectural decisions in the TSD; informal decisions during implementation are not captured |
| Dependency documentation (why chosen, known quirks) | **Partially covered** -- TSD Section 7 (Technology Stack & Environments) documents choices and rationale; runtime quirks discovered during implementation are not captured |

<a id="49-user-facing-documentation"/>

### 4.9. User-Facing Documentation

| Documentation Function | Current Coverage |
|---|---|
| End-user guides | **Not covered** -- product-specific; out of scope for the framework's current focus on engineering workflow |
| Tutorials & walkthroughs | **Not covered** -- same as above |
| Migration guides (version upgrades) | **Not covered** -- same as above |
| Configuration reference | **Not covered** -- same as above |

<a id="410-documentation-review-quality"/>

### 4.10. Documentation Review & Quality

| Documentation Function | Current Coverage |
|---|---|
| Accuracy review (docs match behavior) | **Not covered** -- no agent or process verifies documentation against implementation |
| Completeness audit (undocumented features) | **Not covered** |
| Clarity & readability review | **Not covered** |
| Audience appropriateness | **Not covered** |

<a id="411-process-documentation"/>

### 4.11. Process Documentation

| Documentation Function | Current Coverage |
|---|---|
| Contributing guides (coding standards, PR process, branch naming) | **Partially covered** -- `GIT-RULES.tmpl.md` covers git conventions; `PROGRAMMING-PRINCIPLES.md` covers coding standards; no unified contributing guide is generated |
| CI/CD pipeline docs | **Not covered** |
| Testing strategy docs | **Covered** -- test plan created in preparation phase (`starting-point.md` step 6, `test-plan.instructions.md`) |
| Security policies | **Partially covered** -- `SECURITY-CONVENTIONS.tmpl.md` created in preparation phase if needed; does not cover disclosure process or incident response |

<a id="412-diagramming-visual-documentation"/>

### 4.12. Diagramming & Visual Documentation

| Documentation Function | Current Coverage |
|---|---|
| Architecture diagrams (system-level, component-level) | **Partially covered** -- SHARED-AGENT-CONTEXT includes ASCII architecture diagrams; TSD architecture overview may include diagrams; no Mermaid/PlantUML generation |
| Sequence diagrams (key flows) | **Not covered** -- TSD core technical flows section describes them textually but does not generate visual diagrams |
| ER diagrams (data models) | **Not covered** -- TSD data model section describes schema but does not generate visual diagrams |
| Flowcharts (decision trees, state machines) | **Not covered** -- TSD may describe state machines textually but does not generate visual diagrams |

<a id="413-analysis"/>

### 4.13. Analysis

The audit reveals three distinct clusters of uncovered documentation:

**1. Post-implementation documentation** (changelogs, release notes, runbooks, module READMEs,
onboarding guides) -- These require summarizing *what was built*, which only makes sense
after implementation. A documentation agent scoped to this cluster would be useful and focused.

**2. Doc-code sync and hygiene** (stale doc detection, broken links, spec maintenance,
TOC generation) -- These are better served by CI tooling and linters than by an LLM agent.
An agent could *orchestrate* these tools, but the core capability is mechanical, not generative.

**3. User-facing documentation** (end-user guides, tutorials, migration guides, config reference) --
These are product-specific and highly variable. They may warrant an agent for some projects
but are out of scope for the framework's engineering-workflow focus.

Documentation agents that try to cover all three clusters (and more) in a single role
end up too broad to be effective. A focused agent should target cluster 1 --
post-implementation documentation -- since that is where the framework has a clear gap
and where an LLM agent adds the most value.

<a id="414-when-to-revisit"/>

### 4.14. When to Revisit

- When the framework adds a post-implementation phase, a **release documentation agent**
  scoped to changelogs, release notes, and updated READMEs should be considered
- If projects consistently need generated diagrams, a **diagramming step** (not a full agent)
  could be added to the TSD creation process using Mermaid or PlantUML
- If doc-code drift becomes a recurring problem, investigate CI-based tooling
  before creating an agent for it

---

<a id="why-agent-templates-use-a-general-then-specific-approach"/>

## 5. Why Agent Templates Use a General-Then-Specific Approach

<a id="51-context"/>

### 5.1. Context

When building agents for a multi-project framework, there is a tension between generality and
specificity.

<a id="52-decision"/>

### 5.2. Decision

**Use general templates with `<!-- ADAPT -->` markers, instantiated per-project.**

<a id="53-reasoning"/>

### 5.3. Reasoning

A purely general agent is too broad. E.g. it covers Node.js, Python, and Go when the project only
uses one.
This wastes context window on irrelevant instructions and produces vague guidance
(e.g., "Use parameterized queries" instead of
"Use SQLAlchemy ORM with async sessions as established in `backend/db/session.py`").

A purely per-project agent built from scratch means every developer on every project in our company
reinvents the wheel without benefiting from accumulated best practices.

The template approach splits the difference: the template encodes hard-won, generic best practices
(error handling patterns, pipeline awareness, memory conventions), while the `<!-- ADAPT -->`
markers
guide instantiation with project-specific details (e.g. tech stack, file paths, conventions from the
TSD).

Context window is precious. A project-specific agent only includes what matters
for that project's stack, patterns, and conventions -- no wasted tokens on irrelevant frameworks.
Specificity also drives quality: per-project agents can reference actual file paths,
actual patterns, and actual conventions.

---

<a id="adversarial-thinking-and-why-it-is-a-mode-not-a-separate-agent"/>

## 6. Adversarial Thinking, and Why It Is a Mode, Not a Separate Agent

<a id="61-context"/>

### 6.1. Context

LLM-generated code cannot yet be fully trusted. Models may hallucinate APIs
that don't exist, introduce subtle logic errors, or make junior-level mistakes
that look plausible on the surface. A deliberate adversarial function -- one
that actively tries to find faults rather than confirm correctness --
is essential to catch these failures.

This need is not unique to LLMs. In traditional human software development,
adversarial review is equally valuable but is often skipped due to time constraints,
social dynamics, or the assumption that a standard code review is sufficient.
Automated adversarial thinking is an area where agent-based workflows can deliver
outsized value: the adversarial pass costs minutes of compute, not days of human effort,
and it never feels pressured to "just finish and move on."

<a id="62-question"/>

### 6.2. Question

Some frameworks include a dedicated "devil's advocate" or adversarial review agent.
The question here is whether adversarial review should be a standalone agent or a mode
that existing specialist agents can activate.

<a id="63-decision"/>

### 6.3. Decision

**Adversarial thinking is a mode of activation, not a separate agent.**
It is defined in `ADVERSARIAL-THINKING.md` as a mindset overlay,
and an agent may be activated in normal mode or adverserial mode.

<a id="64-reasoning"/>

### 6.4. Reasoning

A standalone adversarial agent would be too broadly scoped -- it would need to be adversarial
about architecture, code quality, security, performance, data integrity, and operational readiness,
all at once. No single agent can have deep enough domain expertise across all of these.

Instead, adversarial mode activates on top of a specialist agent's existing expertise.
A security specialist in adversarial mode probes for security flaws with deep security knowledge.
A code reviewer in adversarial mode stress-tests code quality with deep engineering knowledge.
The narrow domain focus plus the adversarial lens produces sharper findings than a generalist
adversarial agent ever could.

---

<a id="why-software-engineering-principles-and-programming-principles-are-separate-files"/>

## 7. Why SOFTWARE-ENGINEERING-PRINCIPLES.md and PROGRAMMING-PRINCIPLES.md Are Separate Files

<a id="71-context"/>

### 7.1. Context

The framework has two files that govern coding quality:
`PROGRAMMING-PRINCIPLES.md` (practical rules) and `SOFTWARE-ENGINEERING-PRINCIPLES.md`
(theoretical foundations).

<a id="72-decision"/>

### 7.2. Decision

**Keep them as separate files with different agent audiences.**

<a id="73-reasoning"/>

### 7.3. Reasoning

`PROGRAMMING-PRINCIPLES.md` is a practical workflow guide -- it tells agents how to behave:
read before writing, implement incrementally, self-review, validate inputs, use parameterized
queries.
It is prescriptive and actionable.

`SOFTWARE-ENGINEERING-PRINCIPLES.md` contains the theoretical foundation that explains
*why* those practical rules exist (DRY, SOLID, SoC, etc.).

Different agents need different files:

- **Code-reviewer agent** reads the theory file as its primary review rubric.
  Its job is to evaluate code against quality standards -- it needs context for *judgment*,
  not implementation. Review comments should reference specific principles by name.
- **Tech-lead agent** reads only the Architecture & Scale section
  when planning task decomposition and reviewing architectural decisions.
- **Coding agents (backend, frontend, test) should NOT read the theory file.**
  Their context window is best spent on actual code, the TSD, and practical rules.
  When the code reviewer flags a principle violation, the coding agent fixes the specific issue
  without needing to have read the full theory.

This mirrors how human teams work: junior devs follow practical coding standards,
senior reviewers enforce deeper principles during code review.

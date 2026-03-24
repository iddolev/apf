# To-Do List

## More

1. sub-agents that verify implementation against the plan document. Catches what you'd normally
   miss.
2. Whenever running APF, automatically detect whether a newer version was released in GitHub,
   and offer the user to update.
3. Instructions to all coding agents, and especially reviewers: Always do research and check whether
   there is already a known library that does something, and use it.
   "Don't reinvent the wheel" (is this a common phrase in English?)
   E.g. if you need code that can compare a filepath against a .gitignore pattern,
   it's a very bad practice to try to implement it yourself, when there is already a known python
   package to do it.
   Always ask yourself: Is it likely that the required functionality has been implemented already
   by some known package, check, and if yes, then obtain it and use it rather than re-implementing.
4. Dependencies that are required by a script of APF (e.g. package that checks .gitignore pattern
   to skip files for format_markdown.py) need to be added to the user project's dependencies
5. E.g. the problem with google doc name vs what allowed on windows - it broke and I had to think
   of a better way than simply converting to unicode etc. so maybe such problems should be surfaced
   to the human to decide what to do, so (1) surface and not just try to solve itself (2) human
   thinks better

## Bugs

running format_markdown.py on setup-github-ci.md breaks a line incorrectly

## More concepts

0
enhance the PRD process

- if there are already existing materials, take from them
- at the end, give it to a "prd reviewer expert" with clean slate, to surface more gaps to inquire
  about

0
Ask the coding expert not to create a code file but first create a list of items,
each item is one element (class, function, global variable), with English description,
starting with the most important elements, i.e. just up to 3 elements, with signature
and no implementation, then implement each separately.
And when implementing one element, immediately check for quality.
Maybe this will ensure better quality.

1
Repeatedly and insistently request feedback and fix (but also detect A->B->A->B->A loop of changes).
Just like I did for the script, kept getting more and more things to fix.
Until reach steady state.

And write to a log ALL the changes - so we can see and improve

2
My approach is: there is GSD, Paul, UltraWork, and many more.
https://www.producthunt.com/products/gstack
So I'm building a pipeline like I think is right +
general purpose ability to tell it:
Inspect framework X and take inspiration from it,
tell me what enhancements we could to do APF based on X's best ideas
if we don't already have them.

3
maybe instruct: do atomic steps, and eac one before you do,
you need to convince the feedbacker and/or devil's advocate why you're doing it
and what's needed, and take into account what they say.
Maybe a "rubber duck" agent that the coder agent talks to

1. TDD test driven design
2. DDD https://claude.ai/chat/717b4a61-741a-4baf-a056-6bac5d31c8e5
3. ADP (acceptance driven programming - Paul?)

## Comments on ulw

1. No consistency between the markdowns of the same agent (e.g. Sysiphus) on different models.
   Some of the differences don't carry meaning. Like this entire thing was generated,
   and the creator didn't make basic checks.
2. It used google-generativeai which is the old unmaintained SDK package (that causes a warning)
   whereas GSD uses the new maintained SDK google-genai.

## Versioning and detecting new agentic framework version

1. For each file which is not simply copied to the user project but is a template to instantiate
   It has to have a version number in the frontmatter.
   The starting-point.md and the tech lead (both being the main entry points)
   need to compare the version of the instantiated file to the template version.
   If the template version is higher, then an appropriate update process should be done.
   E.g. if SHARED-AGENT-CONTEXT.tmpl.md is updated.
   Currently I am updating the files in the user project ad-hoc manually.

## Updates

1. Need to account for what happens if user makes changes in some phase that are different
   from what was planned - how to update the docs, leaving the original + adding more notes

## Next: MCP of tasks

1. Discuss what  fields should be in a task, and in a test case, see if can use the same class
2. change server.py accordingly
3. setup installation copying etc.
4. tech lead - add access to t
5. he mcp server, so i can talk to the tech lead and ask:
   what's the next step and it looks up in the mcp server
5. and then do it, and then it needs to understand the description and
   spawn the appropriate agent
6. after one task like that works, and i see code files created,
   we'll discuss the loop

## Code Quality automation

Look at https://claude.ai/chat/552c86d1-4871-4fb7-be57-88d0e8cbf081 - create a process that uses existing tools + suggestions + what cannot be modeled?

## Simple Tasks

1. Videos
   - https://x.com/trq212/status/2014480496013803643
   - https://www.youtube.com/watch?v=RpUTF_U4kiw
   - massive upgrade https://www.youtube.com/watch?v=lf2lcE4YwgI
2. Take the actual instantiated PRD and ask for LLM opinion in general,
   and then feedback -> what should be improved in the PRD template and instructions md
3. The possible colors are the following, so choose what makes sense for the agents: Red
      Blue
      Green
      Yellow
      Purple
      Orange
      Pink
      Cyan
4. Add "find inconsistencies" command/skill?
5. files say that Tech-lead agent should read only the Architecture & Scale section from
   SOFTWARE-ENGINEERING-PRINCIPLES
   when planning task decomposition and reviewing architectural decisions, but an agent cannot read
   only part of a file
   so need to refactor that part ?
6. Add in FRAMEWORK-STATE the timestamp of each important document.
   The user is not supposed to change anything manually in any doc,
   because doing so bypasses the framework and agents and causes Claude to not know about the
   change.
   But to partially mitigate it, this timestamp allows us to create automatic checks to detect
   cases where the user changed a file manually.
   Then we need some process to run occasionally to check for such changes,
   and if a change detected, then start a process of reconciliation.
7. Change the preparation process PRD stage to ask first if there is already a PRD that was prepared
   manually
   not using the framework, and if so where it is, and then start the interview but
   glean answers from that doc if possiblef
8. If we see that loggins each agent invocation is too much, add another HISTORY logger:
   STATE/HISTORY.jsonl, with the instruction: Do not log trivial actions, only important ones
   to understand the flow of what happened
9. Check C4: https://claude.ai/chat/8636118f-e9ad-43f0-8341-f217f73feb50
9. Autonomous Agentic SDLC: https://docs.google.com/document/d/1RNL6Art05I_1jQJpA97m-eXRQQLemHDfkGPaLvTYTko/edit?tab=t.0
10. more generally, general discussion with LLM what is the entire SDLC, and then how to model it
    assuming perfect agents, and then what are all the things that could possibly go wrong and how
    to mitigate with more processes and agents
11. there should never be a folder .claude/plusings under the project's root?
    https://claude.ai/chat/8e8541b9-b60f-4dd6-895e-352af75c479a +
    https://chatgpt.com/c/69a6d58c-f82c-838d-8e67-4f2897aa9e5b
12. if using plugins from a marketplace, how to update (how to bring the latest plugin, how to
    decide if in the project to move to this plugin version)
13. What can we take from https://claude.com/plugins/product-management ;
    https://claude.com/plugins-for/cowork (there is the same plugin in one of the anthropics github
    repos: https://github.com/anthropics/knowledge-work-plugins)
14. Is it possible to have e.g. GSD installed under gsd instead of .claude, so that gsd is cloned
    from GSD and I can modify it, and then pull update from GSD and merge the changes? Or maybe have
    a fork and not a clone and it will make it easier?
15. doc-coauthoring skill from anthropics/skills and more: https://claude.ai/chat/56eedc2d-d823-4233-a237-6c1d83064d6a
    1. also https://claude.ai/chat/ef167be9-3aa2-470a-ac78-50a0d4d95a45
16. .claude/rules/ !!! https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/ +
    https://claudelog.com/faqs/what-are-claude-rules/ +
    https://claude.ai/chat/09bb02c5-5b11-4c15-9e17-71d743fd19a5
17. https://github.com/snarktank/ai-dev-tasks/blob/main/create-prd.md

## Add meta agents

- historian
- mentor

## Add more agents

Add more agent templates for these roles:

- frontend-specialist
- test-specialist
- security-specialist
- code-reviewer
- documentation-specialist
- system-architect:
  A Solutions Architect / System Architect that is called to enhance the PRD + TSD documents
  if it is discovered that they are insufficient

### Remember

- Verify that all agents that create code, or review code, know about PROGRAMMING-PRINCIPLES.md
- ~~Add SECURITY-CONVENTIONS to be read by the appropriate agents~~ (done: added to BE, FE, SE, CR)
- ~~BE, FE, TE, CR, DO (from table below in #refactor-table) need access to PROJECT-RULES~~ (done:
  added to BE, FE, TE,
  CR;
  DO template doesn't exist yet)
- ~~BE, FE, TE need access to README~~ (done: added to BE, FE, TE)

### SOFTWARE-ENGINEERING-PRINCIPLES.md usage

The file `instructions/rules/SOFTWARE-ENGINEERING-PRINCIPLES.md` contains foundational
software engineering theory (DRY, SOLID, SoC, etc.). It is the theoretical foundation
behind the practical `PROGRAMMING-PRINCIPLES.md`. When creating agent templates,
follow these rules:

- **code-reviewer agent**: must read SOFTWARE-ENGINEERING-PRINCIPLES.md as its primary
  review rubric. Review comments should reference specific principles by name.
- **tech-lead agent**: should read only the "Architecture & Scale" section when planning task
  decomposition.
  (Since it's impossible for an agent to read only part of a file, consider splitting the principles
  file so the
  tech-lead can access only what it needs.)
- **Coding agents (backend, frontend, test) must NOT read this file.** Their context
  window is better spent on actual code and practical rules. When the code reviewer
  flags a principle violation, the coding agent fixes the specific issue without
  needing the full theory.
- **Also copy** SOFTWARE-ENGINEERING-PRINCIPLES.md to `rules/` in the project root
  (add to step 5 in starting-point.md alongside PROGRAMMING-PRINCIPLES).

Also do some work to see if PROGRAMMING-PRINCIPLES and SECURITY-CONVENTIONS are
comprehensive enough, and whenever possible, add the theoretical justification from
SOFTWARE-ENGINEERING-PRINCIPLES, and vice versa explain when possible how a principle
in SOFTWARE-ENGINEERING-PRINCIPLES is translated to PROGRAMMING-PRINCIPLES.

## Maybe

Should we enhance the document creation stage also with these?

- Analytics-tracking-plan
- Launch-runbook

<a id="refactor-table"/>

## Skills?

What about skills, e.g. in
https://github.com/wshobson/agents/tree/main/plugins/security-scanning/skills


## Refactor: Agent Knowledge Files

README.md and PROJECT-RULES.md are monolithic files, but different agents need
different slices of them. Serving the full files to every agent wastes context window
on irrelevant content. We need to refactor these into smaller, role-targeted
knowledge files.

### Analysis: which agents need which concerns

**Legend:** TL = tech-lead, BE = backend-specialist, FE = frontend-specialist,
TE = test-specialist, SE = security-specialist, CR = code-reviewer,
DO = documentation-specialist, SA = system-architect.

| File | Section | TL | BE | FE | TE | SE | CR | DO | SA |
|------|---------|----|----|----|----|----|----|----|----|
| PROJECT-RULES | 1. Language & Framework | | x | x | x | | x | | |
| PROJECT-RULES | 2. API & Interface | | x | x | | | x | | |
| PROJECT-RULES | 3. Data & Storage | | x | | | | x | | |
| PROJECT-RULES | 4. Error Handling | | x | x | x | | x | | |
| PROJECT-RULES | 5. Naming Conventions | | x | x | x | | x | x | |
| PROJECT-RULES | 6. Testing Conventions | | x | x | x | | x | | |
| README | Prerequisites | | x | x | x | | | | |
| README | Environment Setup | | x | x | x | | | | |
| README | Installation | | x | x | x | | | | |
| README | Running the App | | x | x | x | | | | |
| README | Testing | | x | x | x | | | | |
| README | Documentation | x | | | | | | x | x |
| README | Agentic Programming | | | | | | | | |
| PROJECT-STRUCTURE | (entire file) | x | x | x | x | x | x | x | x |
| SECURITY-CONVENTIONS | (entire file) | | x | x | | x | x | | |

### Observations

- **Tech-lead** barely needs either file — just Project Structure and Documentation links (for
  routing, not coding).
- **Code-reviewer** needs almost all of PROJECT-RULES (it reviews against conventions) but almost
  nothing from README.
- **Test-specialist** needs most of both files.
- **Documentation-specialist** and **system-architect** need very little from either.
- **Security-specialist** only needs section 7 of PROJECT-RULES and Project Structure.
- The README sections Prerequisites through Testing always travel together — no agent needs only
  some of them.
- The "Agentic Programming" section of README is not needed by any agent.

### Action needed

Refactor README.md and PROJECT-RULES.md into smaller, role-targeted knowledge files
so each agent reads only what it needs. This also requires updating
SHARED-AGENT-CONTEXT.tmpl.md and the agent templates to reference the new files.

### More

I think we need a "consistency-agent" which is run every once in a while
to make sure that all the various files are consistent with each other, and fix or raise a flag to
the user otherwise.
E.g. make sure that PROJECT-STRUCTURE.md indeed reflects the true structure.
E.g. make sure that all the agent definitions are consistent with the documentation (in case the
documentation was
updated).

Both in the project that uses agentic-programming,
and inside the agentic-programming repo (E.g. Update this project's own README.md to reflect the
current file structure)
(so two different consistency agents)

## Possibly to consider:

Ask CC to inspect the URL suggestions at the bottom of each agent template to see
whether something general should be added to the template

## Possibly to consider: frontend-specialist-template vs mykey-frontend-specialist

Comparison of `instructions/.claude/agent-templates/frontend-specialist.tmpl.md` vs
`sandbox/michael-mykey-agents/mykey-frontend-specialist.md`.

The template is already quite strong here — it has responsive design, accessibility, component
architecture, and i18n
sections with real content (not just placeholders). The mykey version expands on these with more
detail.

### Worth incorporating

#### 1. Local-First Data Layer section

The mykey version has a full section on local-first/offline-first patterns: optimistic updates,
offline data schemas,
conflict resolution, cache TTL strategies, data access layer separation. This is project-specific in
the details but
the *concept* of a "Client-Side Data Layer" section with `<!-- ADAPT -->` placeholder could be
valuable for projects
that use local-first architectures. Consider adding it as an optional section.

#### 2. User Experience patterns

The mykey version adds concrete UX guidance: skeleton screens over spinners, error boundaries and
fallback UIs,
empty states that guide users, consistent navigation patterns. The template's "Component
Architecture" section
covers some of this (loading/error/empty states) but is less detailed. Worth expanding slightly.

#### 3. Professional & Consistent UI section

Design tokens, consistent padding/margin scales, semantic color naming, typography hierarchy,
explicit component
variants. Some of this is in the template ("design tokens" mentioned) but the mykey version is more
prescriptive.
Could add a few generic lines about maintaining a consistent design system.

#### 4. Workflow section

A structured 5-step workflow: Analyze -> Plan -> Implement -> Verify -> Refine. The template lacks a
structured
workflow. Worth adding as a generic pattern.

#### 5. Quality Checklist

A concrete pre-completion checklist (i18n, responsive, keyboard, loading states, contrast, design
tokens, data layer,
project patterns). The template lacks this. Worth adding.

#### 6. Edge Cases & Guidance

Practical guidance for ambiguous situations: unclear design system, missing i18n infrastructure,
ambiguous
requirements, performance vs UX tradeoffs, accessibility priority. Worth adding as generic guidance.

### NOT worth incorporating

- Local-first specifics (Dexie.js, specific offline patterns) — too project-specific for a generic
  template
- ICU message format mention — too specific; the template's "localization system" phrasing is better
- RTL layout details — already partially covered in template's i18n section
- Verbose memory instructions (handled via `@SHARED-AGENT-CONTEXT`)

## Possibly to consider: security-specialist-template vs mykey-security-specialist

Comparison of `instructions/.claude/agent-templates/security-specialist.tmpl.md` vs
`sandbox/michael-mykey-agents/mykey-security-specialist.md`.

The template is already **very strong** — it has comprehensive sections on threat modeling, input
validation,
authentication/authorization, data protection, and dependency security. These are all generic and
well-written.

### Worth incorporating

#### 1. Review Methodology (systematic approach)

The mykey version has an 8-step systematic review process: threat model first, input validation,
auth/authz,
data protection, error handling, dependencies, configuration, compliance. The template lacks a
structured review
workflow. Worth adding as a generic checklist.

#### 2. Output Standards (finding report format)

The mykey version defines how to report findings: severity classification
(Critical/High/Medium/Low/Informational),
location (file:line:function), description, proof of concept, remediation, and reference to
OWASP/CWE. The template
mentions severity in the pipeline mode section but doesn't have a structured output format. Worth
adding.

#### 3. Operational Principles

Defense in depth, least privilege, fail secure, zero trust, secure by default, transparency. Most of
these are
touched on in the template's subsections, but having them listed as concise guiding principles at
the top level
is useful.

#### 4. Quality Assurance checklist

5-point checklist: fix doesn't introduce new vulns, backward compat, aligns with existing security
architecture,
addresses root cause, controls are testable. Worth adding.

#### 5. OWASP Top 10 explicit enumeration

The mykey version lists the OWASP Top 10 (plus SSRF and mass assignment) as a "Security Hardening"
section. The
template references OWASP in passing but doesn't enumerate the categories. Could add as a reference
checklist.

### NOT worth incorporating

- MyKey-specific sections (JWT specifics, OTP-based recovery, WebSocket auth, specific rate limiting
  configs,
  GDPR compliance details) — these belong in `<!-- ADAPT -->` sections, not the generic template
- The "pipeline role as optional advisor" framing — the template already handles this differently
  via pipeline
  awareness (direct vs pipeline mode)
- Verbose memory instructions

### Observation

The template is already one of the best-written templates. The main gap is the lack of a structured
**review
methodology** and **output format** — those are the highest-value additions.

## Possibly to consider: tech-lead-template vs mykey-task-router and mykey-system-architect

The tech-lead template maps to TWO sandbox agents: `mykey-task-router` (orchestration) and
`mykey-system-architect`
(architectural decisions). This is a significant structural difference.

### Structural insight

The template combines orchestration and architecture into one "tech-lead" role. The mykey project
splits them:

- **task-router**: Pure orchestration — analyzes requests, decomposes tasks, dispatches to pipeline
  stages, tracks
  completion. Never writes code or makes architectural decisions.
- **system-architect**: Pure architecture — API contracts, data-flow diagrams, ADRs, technology
  evaluation.
  Stage 1 in the pipeline, invoked by the task router.

This split is arguably better because:

1. Separation of concerns — orchestration logic vs architectural expertise
2. The architect can be skipped for simple tasks while the router always runs
3. Context window efficiency — the router doesn't need architectural knowledge loaded

However, the template's approach (single tech-lead) is simpler and may be sufficient for smaller
projects.

### Worth incorporating from mykey-task-router

#### 1. Pipeline diagram and stage details

The task-router has an explicit pipeline diagram with 6 stages and detailed stage descriptions (when
to use,
when to skip, input/output for each). The tech-lead template references `@AGENTS-LIST.md` but
doesn't have
this level of pipeline detail built-in. Consider adding a generic pipeline framework.

#### 2. Available Specialist Agents table

A structured table mapping agent -> role -> when to use. The template defers this to
`@AGENTS-LIST.md` which
is probably fine, but the table format is a nice pattern.

#### 3. Decision-Making Framework

6 principles: bias toward action, pipeline discipline (never skip review/test), fail fast, preserve
context,
loop on failure, verify completeness. Very useful generic guidance.

#### 4. Edge Case Handling

Practical guidance: review loop stuck (3 failures -> flag to user), test failures in untouched code
(create new
task), cross-cutting tasks (separate subtasks), incomplete agent output (retry then break down).

#### 5. Task Decomposition with TaskCreate/TaskUpdate

The task-router explicitly uses Claude Code's task management tools (TaskCreate, TaskUpdate,
TaskList) for
tracking. The template doesn't mention these. Consider adding as a pattern.

#### 6. Complexity classification

Simple / compound / complex classification for incoming requests. Useful for deciding how much
planning is needed.

### Worth incorporating from mykey-system-architect

#### 1. API Contract Design standards

OpenAPI specs, schema design, backward compatibility, deprecation strategies, idempotency/retry
semantics.
These are universal architectural concerns.

#### 2. Data-Flow Diagram standards

Text-based diagrams (Mermaid/PlantUML), multi-level abstraction (context/container/component),
security
annotation on data flows. Generic and useful.

#### 3. ADR (Architecture Decision Record) format

Lightweight template: Context, Options Considered, Decision, Consequences, Status. Widely used
standard.

#### 4. Technology Research methodology

Structured evaluation: quality/performance/cost framework, comparison matrices, evidence-based
recommendations.

#### 5. Self-Verification checklist

Before delivering artifacts: internal consistency, completeness, security implications, cost
estimates,
cross-layer impacts.

### Recommendation

Consider whether the template should remain a single "tech-lead" or be split into "tech-lead"
(orchestrator)
and "system-architect" (advisor). If keeping as one, incorporate the best of both. If splitting,
consider adding
a system-architect template.

### NOT worth incorporating

- The explicit tool list in frontmatter (Task, TaskCreate, etc.) — not in template convention
- MyKey-specific design principles

## Possibly to consider: test-specialist-template vs mykey-test-specialist

Comparison of `instructions/.claude/agent-templates/test-specialist.tmpl.md` vs
`sandbox/michael-mykey-agents/mykey-test-specialist.md`.

The template is already strong with test quality, structure, mocking/isolation, and
coverage/traceability sections.

### Worth incorporating

#### 1. Straightforward vs Complex failure distinction

The mykey version clearly distinguishes what the test specialist should fix directly (import errors,
selector
updates, mock adjustments, snapshot updates) vs what should be routed back (application bugs,
architectural
problems, race conditions, cross-module issues, security failures). This is very useful generic
guidance that
complements the pipeline awareness section.

#### 2. Framework-specific sections as ADAPT placeholders

The mykey version has pytest, Vitest, and Playwright sections with framework-specific best
practices. While
these are project-specific, the *pattern* of having framework-specific subsections with `<!-- ADAPT
-->` prompts
would help users filling out the template. E.g.:

```
#### [TBD] Test Framework (unit/integration)
<!-- ADAPT: Add framework-specific conventions (e.g., pytest fixtures, Jest mocks, etc.) -->

#### [TBD] E2E Test Framework
<!-- ADAPT: Add E2E framework conventions (e.g., Playwright page objects, Cypress commands, etc.) -->
```

#### 3. Structured Workflow

A 7-step workflow: Understand Context -> Check Existing Tests -> Write Tests -> Execute Tests ->
Analyze Results
-> Fix or Report -> Verify. The template lacks a structured workflow. Worth adding.

#### 4. Output Format for results

Summary, tests written/modified, pass/fail counts, issues found (categorized as fixed vs routed),
coverage notes.
The template mentions returning "test results" in pipeline mode but doesn't specify a structure.
Worth adding.

#### 5. Quality Checks as a checklist

Concrete checklist: follows conventions, meaningful (catches real bugs), maintainable,
positive+negative cases,
edge cases, all pass, no regressions. Worth adding.

### NOT worth incorporating

- Specific framework details (pytest markers, Vitest `vi.mock()`, Playwright Page Object Model) —
  too specific
- Verbose memory instructions
- Project-specific test commands

## Possibly to consider: sandbox agents with no template counterpart

The sandbox has 4 agents that don't have corresponding templates:

### 1. mykey-code-reviewer — SHOULD create a template

The todo.md already lists "code-reviewer" under "Add more agents". The mykey version is
well-structured with:

- Clear pipeline role (Stage 3, mandatory after implementation)
- Input/output contract (receives change summary, produces PASS/NEEDS CHANGES verdict)
- Structured review criteria: correctness, pattern adherence, code quality, basic security,
  performance
- Verdict format with severity levels (red/yellow/blue)
- Verdict rules (PASS = no red issues, NEEDS CHANGES = any red issue)
- Clear "What You Are NOT" section
- Automated checks step (linting, type checking)

This is high-value and mostly generic. Recommend creating `code-reviewer.tmpl.md`.

### 2. mykey-docs-specialist — SHOULD create a template

Also listed in todo.md as "documentation-specialist". The mykey version has:

- Pipeline role (Stage 5, final stage)
- Three audiences: AI agents, human developers, human end-users
- Documentation types: architecture docs, data flow docs, developer guides, user guides,
  agent-oriented docs
- Methodology: before/during/after writing
- Formatting and diagram standards (Mermaid)
- Quality criteria (accurate, complete, clear, maintainable, discoverable, actionable)
- Clear scope boundaries ("What You Do NOT Do")
- Edge case guidance (contradictory docs, incomplete info, large scope, sensitive info)

Very comprehensive and mostly generic. Recommend creating `docs-specialist.tmpl.md`.

### 3. mykey-devils-advocate — CONSIDER creating a template

Not listed in todo.md. This is a unique and interesting agent:

- Optional advisor role, not part of main pipeline
- Stress-tests designs, architectures, and code before committing
- Structured output: Critical Issues, Significant Concerns, Questionable Decisions, Minor
  Observations,
  Unanswered Questions
- Clear behavioral guidelines (be specific, honest about severity, think adversarially)
- Both design review and code review modes

This could be very valuable as a generic template. It fills a role that none of the other agents
cover —
adversarial review before implementation, complementing the code reviewer (which reviews after
implementation).
Consider adding to the agent roster.

### 4. mykey-task-router — already covered by tech-lead template

The task-router's orchestration role is covered by the tech-lead template. See the tech-lead section
above
for specific elements worth incorporating. No separate template needed.

## Documentation Agent Ideas

### Project Documentation

- Specs & plans — PRDs, TSDs, implementation plans, test plans
- Architecture Decision Records (ADRs) — documenting why decisions were made
- Changelogs & release notes — summarizing what changed per version
- READMEs — project-level, module-level, package-level
- Onboarding guides — how to set up, run, and contribute to the project
- Runbooks — operational procedures for deployment, rollback, incident response

### API & Interface Documentation

- API reference docs — endpoint descriptions, request/response schemas, error codes
- SDK/library usage guides — how to consume the project's public interfaces
- Integration guides — how third parties or other services connect
- GraphQL/OpenAPI spec maintenance — keeping spec files accurate

### In-Repo Documentation Hygiene

- Doc-code sync verification — detecting when docs are stale after code changes
- Broken link detection — internal cross-references, external URLs
- Formatting & style enforcement — consistent markdown structure, heading hierarchy, naming
- Template maintenance — keeping doc templates up to date
- Table of contents / index generation — navigation aids across doc sets

### Agentic / Multi-Agent Documentation

- Agent instruction files — CLAUDE.md, agent templates, SHARED-AGENT-CONTEXT
- Agent memory curation — reviewing and cleaning up agent memory files for accuracy
- Workflow documentation — documenting how agents interact, the pipeline, conventions

### Knowledge Management

- Glossary / terminology — maintaining a shared vocabulary for the project
- FAQ / troubleshooting docs — common issues and solutions
- Decision logs — capturing discussions and their outcomes beyond ADRs
- Dependency documentation — why specific libraries were chosen, known quirks

### User-Facing Documentation

- End-user guides — how to use the product
- Tutorials & walkthroughs — step-by-step guides for common tasks
- Migration guides — how to upgrade between versions
- Configuration reference — all config options, defaults, and examples

### Documentation Review & Quality

- Accuracy review — verifying docs match actual behavior
- Completeness audit — identifying undocumented features, APIs, or flows
- Clarity & readability — rewriting confusing sections, improving structure
- Audience appropriateness — ensuring the right level of detail for the target reader

### Process Documentation

- Contributing guides — coding standards, PR process, branch naming
- CI/CD pipeline docs — what the pipeline does, how to modify it
- Testing strategy docs — what's tested, how, coverage expectations
- Security policies — disclosure process, auth flows, data handling

### Diagramming & Visual Documentation

- Architecture diagrams — system-level, component-level (Mermaid, PlantUML)
- Sequence diagrams — key flows and interactions
- ER diagrams — data models and relationships
- Flowcharts — decision trees, state machines

## Implement ADR Support

Implement the ADR (Any Decision Record) system as described in `docs/ADR-rationale.md`.

### Templates to create

1. **`ADR-index.tmpl.md`** — template for `ADR-index.md`, a compact table
   (number, title, status, one-line summary) that is cheap for the tech lead to scan.
2. **`ADR-list.tmpl.md`** — template for `ADR-list.md`, the full ADR records
   with complete context, decision, and consequences sections.

Both templates should include instructions on the ADR format, when to create
a new record, and how to maintain the index alongside the list.

### SHARED-AGENT-CONTEXT update

Add instructions to `SHARED-AGENT-CONTEXT.tmpl.md` explaining the ADR system:

- The **tech lead** reads `ADR-index.md` when planning work or assigning tasks.
  When a relevant ADR is found, it reads the full record from `ADR-list.md`
  and includes the constraint in the task assignment to the specialist.
- **Specialist agents** do not routinely read ADR files. They receive relevant
  ADR constraints from the tech lead as part of task assignments.
- **The code reviewer** may read `ADR-index.md` before reviewing code
  that touches architectural or convention concerns.
- Any agent that makes a decision that constrains future work should write
  a new ADR entry (append to `ADR-list.md` and update `ADR-index.md`).

### Tech lead template update

Update the tech lead template to include ADR gatekeeper responsibilities.

### MCP server for ADR querying

Implement the ideal queryable ADR system as an MCP server. This would expose
`record_adr`, `check_adr`, and `list_adrs` tools that any agent can call
natively. The server handles persistence, numbering, and semantic retrieval.

See `docs/ADR-rationale.md` section "Implementation Path: MCP Server" for
the full design, resource costs, and semantic retrieval options (keyword
matching, embedding-based, or pass-through to the LLM).

The `framework-initial-install` step would install the server script and configure
the MCP entry in `.claude/settings.json`.

### See also

`docs/ADR-rationale.md` for full design rationale, including the MCP-based
implementation plan, and why the current file-based approach uses the tech
lead as gatekeeper.

---

## Next Enhancement

Instead of the naive approach of cloning this repo under the root folder of the user's project's,
convert this project to a plugin that can be installed as a Claude Code plugin.
This means all the files will sit under the user's folder ~/.claude/plugins/cache.

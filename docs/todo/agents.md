# Agent-Related To-Do

## Add meta agents

- historian
- mentor

## Add more agents

Add more agent templates for these roles:

- apf-frontend-specialist
- apf-test-specialist
- apf-security-specialist
- apf-code-reviewer
- documentation-specialist
- system-architect:
  A Solutions Architect / System Architect that is called to enhance the PRD + TSD documents
  if it is discovered that they are insufficient

### Remember

- Verify that all agents that create code, or review code, know about PROGRAMMING-PRINCIPLES.md
- ~~Add SECURITY-CONVENTIONS to be read by the appropriate agents~~ (done: added to BE, FE, SE, CR)
- ~~BE, FE, TE, CR, DO (from table below in #refactor-table) need access to PROJECT-RULES~~ (done:
  added to BE, FE, TE, CR; DO template doesn't exist yet)
- ~~BE, FE, TE need access to README~~ (done: added to BE, FE, TE)

### SOFTWARE-ENGINEERING-PRINCIPLES.md usage

The file `instructions/rules/SOFTWARE-ENGINEERING-PRINCIPLES.md` contains foundational
software engineering theory (DRY, SOLID, SoC, etc.). It is the theoretical foundation
behind the practical `PROGRAMMING-PRINCIPLES.md`. When creating agent templates,
follow these rules:

- **apf-code-reviewer agent**: must read SOFTWARE-ENGINEERING-PRINCIPLES.md as its primary
  review rubric. Review comments should reference specific principles by name.
- **apf-tech-lead agent**: should read only the "Architecture & Scale" section when planning task
  decomposition.
  (Since it's impossible for an agent to read only part of a file, consider splitting the principles
  file so the apf-tech-lead can access only what it needs.)
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

## Refactor: Agent Knowledge Files

README.md and PROJECT-RULES.md are monolithic files, but different agents need
different slices of them. Serving the full files to every agent wastes context window
on irrelevant content. We need to refactor these into smaller, role-targeted
knowledge files.

### Analysis: which agents need which concerns

**Legend:** TL = apf-tech-lead, BE = apf-backend-specialist, FE = apf-frontend-specialist,
TE = apf-test-specialist, SE = apf-security-specialist, CR = apf-code-reviewer,
DO = documentation-specialist, SA = system-architect.

<a id="refactor-table"/>

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
documentation was updated).

Both in the project that uses agentic-programming,
and inside the agentic-programming repo (E.g. Update this project's own README.md to reflect the
current file structure)
(so two different consistency agents)

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

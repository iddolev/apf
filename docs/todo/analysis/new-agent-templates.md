# Analysis: sandbox agents with no template counterpart

The sandbox has 4 agents that don't have corresponding templates:

## 1. mykey-code-reviewer — SHOULD create a template

The todo.md already lists "apf-code-reviewer" under "Add more agents". The mykey version is
well-structured with:

- Clear pipeline role (Stage 3, mandatory after implementation)
- Input/output contract (receives change summary, produces PASS/NEEDS CHANGES verdict)
- Structured review criteria: correctness, pattern adherence, code quality, basic security,
  performance
- Verdict format with severity levels (red/yellow/blue)
- Verdict rules (PASS = no red issues, NEEDS CHANGES = any red issue)
- Clear "What You Are NOT" section
- Automated checks step (linting, type checking)

This is high-value and mostly generic. Recommend creating `apf-code-reviewer.tmpl.md`.

## 2. mykey-docs-specialist — SHOULD create a template

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

## 3. mykey-devils-advocate — CONSIDER creating a template

Not listed in todo.md. This is a unique and interesting agent:

- Optional advisor role, not part of main pipeline
- Stress-tests designs, architectures, and code before committing
- Structured output: Critical Issues, Significant Concerns, Questionable Decisions, Minor
  Observations, Unanswered Questions
- Clear behavioral guidelines (be specific, honest about severity, think adversarially)
- Both design review and code review modes

This could be very valuable as a generic template. It fills a role that none of the other agents
cover — adversarial review before implementation, complementing the code reviewer (which reviews
after implementation). Consider adding to the agent roster.

## 4. mykey-task-router — already covered by apf-tech-lead template

The task-router's orchestration role is covered by the apf-tech-lead template. See
[tech-lead.md](tech-lead.md) for specific elements worth incorporating. No separate template
needed.

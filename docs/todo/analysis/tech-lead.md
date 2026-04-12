# Analysis: apf-tech-lead-template vs mykey-task-router and mykey-system-architect

The apf-tech-lead template maps to TWO sandbox agents: `mykey-task-router` (orchestration) and
`mykey-system-architect` (architectural decisions). This is a significant structural difference.

## Structural insight

The template combines orchestration and architecture into one "apf-tech-lead" role. The mykey project
splits them:

- **task-router**: Pure orchestration — analyzes requests, decomposes tasks, dispatches to pipeline
  stages, tracks completion. Never writes code or makes architectural decisions.
- **system-architect**: Pure architecture — API contracts, data-flow diagrams, ADRs, technology
  evaluation. Stage 1 in the pipeline, invoked by the task router.

This split is arguably better because:

1. Separation of concerns — orchestration logic vs architectural expertise
2. The architect can be skipped for simple tasks while the router always runs
3. Context window efficiency — the router doesn't need architectural knowledge loaded

However, the template's approach (single apf-tech-lead) is simpler and may be sufficient for smaller
projects.

## Worth incorporating from mykey-task-router

### 1. Pipeline diagram and stage details

The task-router has an explicit pipeline diagram with 6 stages and detailed stage descriptions
(when to use, when to skip, input/output for each). The apf-tech-lead template references
`@AGENTS-LIST.md` but doesn't have this level of pipeline detail built-in. Consider adding a
generic pipeline framework.

### 2. Available Specialist Agents table

A structured table mapping agent -> role -> when to use. The template defers this to
`@AGENTS-LIST.md` which is probably fine, but the table format is a nice pattern.

### 3. Decision-Making Framework

6 principles: bias toward action, pipeline discipline (never skip review/test), fail fast, preserve
context, loop on failure, verify completeness. Very useful generic guidance.

### 4. Edge Case Handling

Practical guidance: review loop stuck (3 failures -> flag to user), test failures in untouched code
(create new task), cross-cutting tasks (separate subtasks), incomplete agent output (retry then
break down).

### 5. Task Decomposition with TaskCreate/TaskUpdate

The task-router explicitly uses Claude Code's task management tools (TaskCreate, TaskUpdate,
TaskList) for tracking. The template doesn't mention these. Consider adding as a pattern.

### 6. Complexity classification

Simple / compound / complex classification for incoming requests. Useful for deciding how much
planning is needed.

## Worth incorporating from mykey-system-architect

### 1. API Contract Design standards

OpenAPI specs, schema design, backward compatibility, deprecation strategies, idempotency/retry
semantics. These are universal architectural concerns.

### 2. Data-Flow Diagram standards

Text-based diagrams (Mermaid/PlantUML), multi-level abstraction (context/container/component),
security annotation on data flows. Generic and useful.

### 3. ADR (Architecture Decision Record) format

Lightweight template: Context, Options Considered, Decision, Consequences, Status. Widely used
standard.

### 4. Technology Research methodology

Structured evaluation: quality/performance/cost framework, comparison matrices, evidence-based
recommendations.

### 5. Self-Verification checklist

Before delivering artifacts: internal consistency, completeness, security implications, cost
estimates, cross-layer impacts.

## Recommendation

Consider whether the template should remain a single "apf-tech-lead" or be split into "apf-tech-lead"
(orchestrator) and "system-architect" (advisor). If keeping as one, incorporate the best of both.
If splitting, consider adding a system-architect template.

## NOT worth incorporating

- The explicit tool list in frontmatter (Task, TaskCreate, etc.) — not in template convention
- MyKey-specific design principles

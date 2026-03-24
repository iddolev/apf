# Analysis: test-specialist-template vs mykey-test-specialist

Comparison of `instructions/.claude/agent-templates/test-specialist.tmpl.md` vs
`sandbox/michael-mykey-agents/mykey-test-specialist.md`.

The template is already strong with test quality, structure, mocking/isolation, and
coverage/traceability sections.

## Worth incorporating

### 1. Straightforward vs Complex failure distinction

The mykey version clearly distinguishes what the test specialist should fix directly (import errors,
selector updates, mock adjustments, snapshot updates) vs what should be routed back (application
bugs, architectural problems, race conditions, cross-module issues, security failures). This is very
useful generic guidance that complements the pipeline awareness section.

### 2. Framework-specific sections as ADAPT placeholders

The mykey version has pytest, Vitest, and Playwright sections with framework-specific best
practices. While these are project-specific, the *pattern* of having framework-specific subsections
with `<!-- ADAPT -->` prompts would help users filling out the template. E.g.:

```
#### [TBD] Test Framework (unit/integration)
<!-- ADAPT: Add framework-specific conventions (e.g., pytest fixtures, Jest mocks, etc.) -->

#### [TBD] E2E Test Framework
<!-- ADAPT: Add E2E framework conventions (e.g., Playwright page objects, Cypress commands, etc.) -->
```

### 3. Structured Workflow

A 7-step workflow: Understand Context -> Check Existing Tests -> Write Tests -> Execute Tests ->
Analyze Results -> Fix or Report -> Verify. The template lacks a structured workflow. Worth adding.

### 4. Output Format for results

Summary, tests written/modified, pass/fail counts, issues found (categorized as fixed vs routed),
coverage notes. The template mentions returning "test results" in pipeline mode but doesn't specify
a structure. Worth adding.

### 5. Quality Checks as a checklist

Concrete checklist: follows conventions, meaningful (catches real bugs), maintainable,
positive+negative cases, edge cases, all pass, no regressions. Worth adding.

## NOT worth incorporating

- Specific framework details (pytest markers, Vitest `vi.mock()`, Playwright Page Object Model) —
  too specific
- Verbose memory instructions
- Project-specific test commands

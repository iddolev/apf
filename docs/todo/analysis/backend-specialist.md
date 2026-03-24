# Analysis: backend-specialist-template vs mykey-backend-developer

Comparison of `instructions/.claude/agent-templates/backend-specialist.tmpl.md` vs
`sandbox/michael-mykey-agents/mykey-backend-developer.md`.

The mykey version has several substantive sections that the template currently lacks (it only has
empty `<!-- ADAPT -->` placeholders). These are generic backend best practices worth adding as
default template content.

## Worth incorporating

### 1. Implementation Standards section

The template has an empty placeholder for "Key patterns" but the mykey version has well-structured,
generic backend best practices:

- **Code Quality** — clean code, DRY, small functions, typing, meaningful comments
- **Code Organization** — layered architecture (controllers -> services -> repositories), separation
  of concerns, dependency injection, config separation
- **Efficiency & Performance** — N+1 avoidance, caching, async I/O, connection pooling, pagination

Most of these are universal backend principles, not project-specific.

### 2. Error Handling Pattern

Custom error classes, global error middleware, async error handling, contextual logging. All
generic.

### 3. API Design Standards

Consistent naming, HTTP status codes, response envelopes, versioning, documenting contracts. All
generic.

### 4. Post-Implementation Checklist

A concrete checklist before considering a task complete. Very useful as a template pattern.

### 5. Consulting the Architect guidance (partial)

When to escalate to the tech-lead/architect. The template already has pipeline awareness but lacks
specific escalation criteria.

## NOT worth incorporating

- MyKey-specific details (SHA-256 OTP hashing, specific paths)
- The verbose repetition of memory instructions (template already handles this via
  `@SHARED-AGENT-CONTEXT`)
- The `tools:` frontmatter line listing specific tools (not in the template convention)
- Using `model: opus` (template intentionally uses sonnet for cost balance)
- The "searching past context" section with grep commands (too specific)

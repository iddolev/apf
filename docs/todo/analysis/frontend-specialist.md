# Analysis: frontend-specialist-template vs mykey-frontend-specialist

Comparison of `instructions/.claude/agent-templates/frontend-specialist.tmpl.md` vs
`sandbox/michael-mykey-agents/mykey-frontend-specialist.md`.

The template is already quite strong here — it has responsive design, accessibility, component
architecture, and i18n sections with real content (not just placeholders). The mykey version
expands on these with more detail.

## Worth incorporating

### 1. Local-First Data Layer section

The mykey version has a full section on local-first/offline-first patterns: optimistic updates,
offline data schemas, conflict resolution, cache TTL strategies, data access layer separation.
This is project-specific in the details but the *concept* of a "Client-Side Data Layer" section
with `<!-- ADAPT -->` placeholder could be valuable for projects that use local-first
architectures. Consider adding it as an optional section.

### 2. User Experience patterns

The mykey version adds concrete UX guidance: skeleton screens over spinners, error boundaries and
fallback UIs, empty states that guide users, consistent navigation patterns. The template's
"Component Architecture" section covers some of this (loading/error/empty states) but is less
detailed. Worth expanding slightly.

### 3. Professional & Consistent UI section

Design tokens, consistent padding/margin scales, semantic color naming, typography hierarchy,
explicit component variants. Some of this is in the template ("design tokens" mentioned) but the
mykey version is more prescriptive. Could add a few generic lines about maintaining a consistent
design system.

### 4. Workflow section

A structured 5-step workflow: Analyze -> Plan -> Implement -> Verify -> Refine. The template lacks
a structured workflow. Worth adding as a generic pattern.

### 5. Quality Checklist

A concrete pre-completion checklist (i18n, responsive, keyboard, loading states, contrast, design
tokens, data layer, project patterns). The template lacks this. Worth adding.

### 6. Edge Cases & Guidance

Practical guidance for ambiguous situations: unclear design system, missing i18n infrastructure,
ambiguous requirements, performance vs UX tradeoffs, accessibility priority. Worth adding as
generic guidance.

## NOT worth incorporating

- Local-first specifics (Dexie.js, specific offline patterns) — too project-specific for a generic
  template
- ICU message format mention — too specific; the template's "localization system" phrasing is
  better
- RTL layout details — already partially covered in template's i18n section
- Verbose memory instructions (handled via `@SHARED-AGENT-CONTEXT`)

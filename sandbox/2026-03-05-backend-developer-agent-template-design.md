# Backend Developer Agent Template — Design Document

**Date:** 2026-03-05
**Status:** Approved

## Problem

We need a reusable backend-developer agent definition that works across all company projects. Rather than writing a new
agent from scratch each time or using a generic one that's too vague to be useful, we want a single template that Claude
can adapt to any project by reading its PRD and codebase.

## Approach: Meta-Agent Template

A single file that serves as both:

1. A **complete agent definition** with clearly marked adaptation zones (`<!-- ADAPT -->`)
2. A **generation prompt** that tells Claude how to read a project and fill in the zones

Core sections (code quality, workflow, error handling) stay constant across projects — enforcing company-wide standards.
Adaptation zones get filled with project-specific content (tech stack, file structure, conventions, commands, security
level).

## Design Decisions

- **Language-agnostic**: The template covers Python, Node.js, and other stacks. Project-specific tech details go in
  adaptation zones.
- **Pipeline-flexible**: The agent works both when dispatched by an orchestrator (pipeline mode) and when invoked
  directly by a user (direct mode). It detects which mode from context.
- **Security is configurable**: Always present, but the adaptation zone lets Claude set emphasis (HIGH vs STANDARD)
  based on project risk profile.
- **Lives in a shared repo**: Intended for a separate company-wide repo that all projects can reference.
- **Claude-assisted adaptation**: The primary workflow is giving Claude the template + a project's PRD/codebase, and
  Claude generates the project-specific agent definition.

## Template Structure

### 1. Generation Prompt

Instructions at the top of the file telling Claude (or a developer) how to adapt the template for a specific project.
Claude reads the template, scans the project's PRD/specs/codebase, fills in all `<!-- ADAPT -->` zones, and outputs a
ready-to-use agent file.

### 2. YAML Frontmatter

Agent metadata: name, description, examples. The description is generic; the examples are project-specific (adaptation
zone).

### 3. Core Identity

Senior backend developer role definition. Mostly fixed, with one adaptation zone for project-specific tech expertise.
Includes pipeline awareness section that explains both pipeline mode (receive task plan, return summary) and direct mode
(own the full workflow).

### 4. Project Context

Fully adapted section. Includes: project description, tech stack, architecture diagram, file/directory structure, key
patterns. This is where Claude does the most work during generation.

### 5. Workflow

Mostly universal. Four steps: understand before writing, implement incrementally, self-review checklist, commands
reference. Only the commands section is an adaptation zone.

### 6. Development Standards

Five subsections:

- **Code Quality** — fixed (clean code, DRY, typing, docstrings)
- **Code Organization** — fixed (separation of concerns, DI, interfaces)
- **Error Handling** — fixed (consistent strategy, boundary catching, logging)
- **Security** — adaptation zone for risk level (HIGH: all items non-negotiable; STANDARD: subset). Items include input
  validation, secrets management, injection prevention, auth checks, data protection.
- **Performance** — fixed (N+1 prevention, async I/O, no premature optimization)

### 7. Agent Memory

Persistent memory instructions with adaptation zone for the memory directory path. Records project structure,
conventions, SDK quirks, test patterns.

## Sources Analyzed

| Source | What we took from it |
|--------|---------------------|
| mykey-backend-developer (friend's agent) | Pipeline awareness pattern, post-implementation checklist, security-as-non-negotiable structure |
| senior-backend-dev (Claude-generated) | Project context section format, workflow steps, commands reference pattern |
| VoltAgent/awesome-claude-code-subagents | Phased approach (analysis → development → production readiness), multi-language awareness |
| wshobson/agents backend-architect | Resilience patterns emphasis, error handling philosophy |

## Next Steps

1. Create the template file (`backend-developer-template.md`)
2. Test it by generating a project-specific agent for this repo (LLMs Unified Interface)
3. Move the template to the shared company repo

---
date: 2026-03-06
author: "Iddo Lev"
LLM-author: claude-Opus-4.6
---

# Project Rules

## Purpose

This document defines project-specific coding and design conventions that all agents must follow.
These rules complement the general `PROGRAMMING-PRINCIPLES.md` —
they capture conventions unique to this project that emerge from the TSD's technology
choices, design principles, and API contracts.

> **How to use this template:**
>
> - Derive rules from the TSD (design principles, technology stack, API conventions, data
>   model patterns) and PRD (constraints, compliance requirements).
> - Confirm each rule with the user before finalizing.
> - Do not duplicate rules already in @rules/PROGRAMMING-PRINCIPLES.md.
> - Keep rules concrete and actionable — not vague aspirations.

---

## 1. Language & Framework Conventions

<!-- ADAPT: Derive from the TSD's Technology Stack section.
     Examples:

     - "Always use async/await; never use raw callbacks or .then() chains."
     - "Use Pydantic v2 model_validator for cross-field validation, not root_validator."
     - "Use path aliases defined in tsconfig.json; never use relative imports with more than two levels (../../..)."

-->

- [TBD]

## 2. API & Interface Conventions

<!-- ADAPT: Derive from the TSD's API Conventions section (Section 9.2).
     Examples:

     - "All API responses must use the standard envelope: { data, error, meta }."
     - "All endpoints must accept and return UTC ISO 8601 timestamps."
     - "Use kebab-case for URL paths, camelCase for JSON fields."

-->

- [TBD]

## 3. Data & Storage Conventions

<!-- ADAPT: Derive from the TSD's Data Model section.
     Examples:

     - "Never use ORM lazy loading; always use explicit eager loading."
     - "All database queries must go through the repository layer; never query from route handlers."
     - "Soft-delete by default; hard-delete only for PII cleanup."

-->

- [TBD]

## 4. Error Handling Conventions

<!-- ADAPT: Derive from the TSD's error handling patterns and the project's custom error types.
     Examples:

     - "All service-layer errors must use the custom AppError hierarchy defined in src/errors.ts."
     - "Never catch and silently swallow exceptions; always log or re-raise."
     - "External API failures must be wrapped in an IntegrationError with the upstream status code."

-->

- [TBD]

## 5. Naming Conventions

<!-- ADAPT: Derive from the TSD's project structure and established patterns in the codebase.
     Examples:

     - "Files: kebab-case (user-service.ts). Classes: PascalCase. Functions/variables: camelCase."
     - "Test files: [module].test.ts, co-located in __tests__/ directories."
     - "Environment variables: SCREAMING_SNAKE_CASE, prefixed with APP_ for application-specific vars."

-->

- [TBD]

## 6. Testing Conventions

<!-- ADAPT: Derive from the test plan's Test Strategy section.
     Examples:

     - "All external API calls must be mocked in unit tests using responses library."
     - "Integration tests use testcontainers for database; never mock the DB layer in integration tests."
     - "Each test file must be independent; no shared mutable state between test cases."

-->

- [TBD]

## 7. Security Conventions

See `rules/SECURITY-CONVENTIONS.md` (if applicable).

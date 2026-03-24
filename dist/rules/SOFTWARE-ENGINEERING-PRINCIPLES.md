---
last_update: 2026-03-07
author: Iddo Lev
LLM-co-author: claude-Opus-4.6
---

# Software Engineering Principles

## Purpose and Audience


> **NOTE:** The rationale for why this file is separate from `PROGRAMMING-PRINCIPLES.md`
> is explained in `docs/rationale/rationale.md` in the APF project,
> section "Why SOFTWARE-ENGINEERING-PRINCIPLES.md and PROGRAMMING-PRINCIPLES.md Are Separate Files".

This file contains foundational software engineering theory — the underlying principles
that inform the practical coding rules in `PROGRAMMING-PRINCIPLES.md`.

**Who should read this file:**

- **Code-reviewer agent**: as its primary review rubric.
  Review comments should reference specific principles by name
  (e.g., "this violates SRP — the UserService handles both auth and profile management").
- **Tech-lead agent**: only the Architecture & Scale section,
  when planning task decomposition and reviewing architectural decisions.
- **Coding agents (backend, frontend, test) should NOT read this file.**

---

## Foundational Design Principles

- **DRY** — Don't Repeat Yourself. Every piece of knowledge should have a single, authoritative
  representation.
- **KISS** — Keep It Simple, Stupid. Prefer the simplest solution that works.
- **YAGNI** — You Aren't Gonna Need It. Don't build for hypothetical future requirements.
- **SoC** — Separation of Concerns. Each module/layer handles one concern.
- **LoD** — Law of Demeter (Principle of Least Knowledge). A module should only talk to its
  immediate collaborators.
- **CoC** — Convention over Configuration. Sensible defaults reduce boilerplate.
- **PoLA** — Principle of Least Astonishment. Code should behave as readers expect.

## SOLID (Object-Oriented Design)

- **SRP** — Single Responsibility Principle. A class should have one reason to change.
- **OCP** — Open/Closed Principle. Open for extension, closed for modification.
- **LSP** — Liskov Substitution Principle. Subtypes must be substitutable for their base types.
- **ISP** — Interface Segregation Principle. Prefer many small interfaces over one large one.
- **DIP** — Dependency Inversion Principle. Depend on abstractions, not concretions.

## Composition & Coupling

- **Composition over Inheritance** — Favor object composition over class inheritance.
- **Loose Coupling** — Minimize dependencies between modules.
- **High Cohesion** — Related functionality should live together.
- **Dependency Injection** — Inject dependencies rather than constructing them internally.
- **IoC** — Inversion of Control. The framework calls your code, not the other way around.

## Data & State

- **Encapsulation** — Hide internal state; expose behavior through interfaces.
- **Information Hiding** — Modules should expose minimal interfaces, hiding implementation details.
- **Immutability** — Prefer immutable data structures where practical.
- **Single Source of Truth** — Each piece of data should be stored and managed in exactly one place.

## Error Handling & Robustness

- **Fail Fast** — Detect and report errors as early as possible.
- **Defensive Programming** — Validate inputs at boundaries; assume nothing about external data.
- **Postel's Law** (Robustness Principle) — Be conservative in what you send, liberal in what you
  accept.

## Code Quality & Readability

- **Boy Scout Rule** — Leave the code cleaner than you found it.
- **Self-Documenting Code** — Code should communicate its intent without needing comments.
- **Command-Query Separation (CQS)** — A method should either change state or return a result, not
  both.
- **Tell, Don't Ask** — Tell objects what to do; don't ask for their state and act on it externally.

## Architecture & Scale

- **Layered Separation of Concerns** — Presentation, business logic, and data access in distinct
  layers.
- **Domain-Driven Design (DDD)** — Model software around the business domain.
- **CQRS** — Command Query Responsibility Segregation. Separate read and write models.
- **Event-Driven Architecture** — Components communicate through events, not direct calls.
- **Twelve-Factor App** — Methodology for building SaaS apps (config in env, stateless processes,
  etc.).

## Testing

- **Test Pyramid** — Many unit tests, fewer integration tests, fewest E2E tests.
- **Arrange-Act-Assert (AAA)** — Structure tests in three clear phases.
- **Test Isolation** — Tests should not depend on each other or on shared mutable state.

## Security

- **Principle of Least Privilege** — Grant only the minimum permissions needed.
- **Defense in Depth** — Multiple layers of security controls.
- **Zero Trust** — Never trust, always verify.
- **Secure by Default** — Default configurations should be secure.

## Performance

- **Premature Optimization is the Root of All Evil** (Knuth) — Write correct code first; optimize
  with evidence.
- **Lazy Evaluation** — Defer computation until the result is needed.
- **Caching** — Store computed results to avoid redundant work.

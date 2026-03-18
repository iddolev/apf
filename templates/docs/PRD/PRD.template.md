---
date: 2026-03-04
author: "Iddo Lev"
LLM-coauthors:
  - claude-Opus-4.6
  - gemini-3.1-pro
  - grok
  - gpt-5.3-codex
  - perplexity
LLM-consolidator: GPT-5.2
---

# Product Requirements Document (PRD) Template

> **How to use this template**
> - This is a fill-in PRD format intended to be completed via an iterative interview.
> - Keep all requirements **testable** (acceptance criteria), **scoped** (in/out), and **measurable** (success metrics).

---

<a id="document-control"/>

## 1) Document Control

- **Product / Feature Name:** [TBD]
- **One-liner / Elevator Pitch:** [TBD — one sentence]
- **Version:** [TBD]
- **Status:** Draft / In Review / Approved
- **Author(s):** [TBD]
- **Stakeholders:** [TBD — teams + names]
- **Last Updated:** [YYYY-MM-DD]
- **Related Links:** [mocks/specs/tickets/repo/docs]

---

## Table of Contents

- [1) Document Control](#document-control)
- [2) Executive Summary](#executive-summary)
- [3) Background & Context](#background-context)
- [4) Goals, Success Metrics & Non-Goals](#goals-success-metrics-non-goals)
- [5) Users, Personas & Jobs-to-be-Done](#users-personas-jobs-to-be-done)
- [6) User Journeys, Use Cases & Stories](#user-journeys-use-cases-stories)
- [7) Scope (MVP vs Later)](#scope)
- [8) Requirements](#requirements)
- [9) UX / UI Requirements](#ux-ui-requirements)
- [10) Data, Integrations & APIs](#data-integrations-apis)
- [11) Technical Architecture & Constraints](#technical-architecture-constraints)
- [12) Analytics & Metrics](#analytics-metrics)
- [13) Release & Rollout Plan](#release-rollout-plan)
- [14) Testing, Validation & Definition of Done](#testing-validation-definition-of-done)
- [15) Risks & Mitigations](#risks-mitigations)
- [16) Open Questions](#open-questions)
- [17) Decisions Log](#decisions-log)
- [18) Appendix](#appendix)

---

<a id="executive-summary"/>

## 2) Executive Summary

- **Problem Statement:** [What user/business problem is being solved?]
- **Proposed Solution (High-Level):** [What are we building, in one paragraph?]
- **Expected Outcome:** [What changes for users and the business?]
- **Why Now:** [Why is this priority now?]

---

<a id="background-context"/>

## 3) Background & Context

### 3.1 Current State

- **Today's workflow:** [How users solve this now]
- **Pain points and limitations:** [What's broken/slow/expensive/confusing today]
- **Evidence:** [research, support tickets, analytics, sales feedback, incidents]

### 3.2 Alternatives Considered

- **Option A:** [Do nothing / status quo] — [pros/cons]
- **Option B:** [Alternative] — [pros/cons]
- **Why this approach:** [reasoning]

### 3.3 Constraints & Assumptions

- **Constraints:** [budget, timeline, staffing, platform, policy/compliance]
- **Assumptions:** [what must be true; what needs validation]

---

<a id="goals-success-metrics-non-goals"/>

## 4) Goals, Success Metrics & Non-Goals

### 4.1 Product Vision (Optional)

[1–2 sentences describing the longer-term aspiration this work supports.]

### 4.2 Goals & Success Metrics

| # | Goal / Objective | Success Metric | Baseline | Target | Timeframe |
|---|------------------|----------------|----------|--------|-----------|
| G1 | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| G2 | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| G3 | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

### 4.3 Non-Goals (Explicitly Out of Scope)

- [NG1]
- [NG2]
- [NG3]

---

<a id="users-personas-jobs-to-be-done"/>

## 5) Users, Personas & Jobs-to-be-Done

### 5.1 Target Users

- **Primary users:** [TBD]
- **Secondary users:** [TBD]
- **Admins / Operators (if applicable):** [TBD]

### 5.2 Personas (Add as needed)

| Persona | Role / Context | Goals | Pain Points | Technical level | Quote |
|---------|----------------|-------|------------|-----------------|-------|
| [P1] | [TBD] | [TBD] | [TBD] | [TBD] | "[TBD]" |
| [P2] | [TBD] | [TBD] | [TBD] | [TBD] | "[TBD]" |

**Primary persona:** [P?]

### 5.3 Jobs-to-be-Done

- **JTBD-1:** When [situation], I want to [motivation], so I can [expected outcome].
- **JTBD-2:** When [situation], I want to [motivation], so I can [expected outcome].

---

<a id="user-journeys-use-cases-stories"/>

## 6) User Journeys, Use Cases & Stories

> For definitions of User Journey, Use Case, and User Story and how they relate, see **Appendix A: Glossary**.

### 6.1 Core User Journeys (High-level)

- **Journey J1:** [Name] — [start -> end], [success definition]
- **Journey J2:** [Name] — [start -> end], [success definition]

### 6.2 Key Use Cases (Add as needed)

#### Use Case UC-1: [Title]

- **Primary actor:** [persona/role]
- **Preconditions:** [what must be true before]
- **Main flow:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Postconditions:** [what is true after]
- **Alternative / error flows:** [edge cases, invalid inputs, failures]

### 6.3 User Stories (Optional, especially for delivery planning)

| ID | As a... | I want to... | So that... | Priority (MoSCoW) | Notes |
|----|-------|------------|----------|-------------------|-------|
| US-01 | [persona] | [action] | [benefit] | Must / Should / Could / Won't | [TBD] |
| US-02 | [persona] | [action] | [benefit] | Must / Should / Could / Won't | [TBD] |

---

<a id="scope"/>

## 7) Scope (MVP vs Later)

### 7.1 In Scope (MVP / This Release)

- [S1]
- [S2]
- [S3]

### 7.2.a Out of Scope: Future Versions

> Features not in this release but intended for later versions (roadmap items).

- [O1]
- [O2]

### 7.2.b Out of Scope: Not Planned

> Features that were considered and deliberately excluded, with no intention to
> revisit. For high-level directional non-goals, see Section 4.3.

- [O1]
- [O2]

### 7.3 Dependencies

> Dependencies live under Scope because they directly affect what is feasible
> within this release. If a dependency is not ready, scope items that rely on it
> may need to move to a later version.

- **Internal dependencies:** [teams/systems]
- **External dependencies:** [vendors/APIs]
- **Critical path:** [what must happen first]

---

<a id="requirements"/>

## 8) Requirements

### 8.1 Functional Requirements

> Write each requirement so it is independently testable. Prefer one "shall" per requirement.

| ID | Requirement | Priority (MoSCoW) | Acceptance Criteria (G/W/T) | Dependencies | Notes |
|----|-------------|-------------------|-----------------------------|--------------|-------|
| FR-01 | The system shall... | Must / Should / Could / Won't | Given... When... Then... | [TBD] | [TBD] |
| FR-02 | The system shall... | Must / Should / Could / Won't | Given... When... Then... | [TBD] | [TBD] |

### 8.2 Non-Functional Requirements

| Category | Requirement | Target / Constraint | Measurement / Notes |
|----------|------------|---------------------|---------------------|
| Performance | [e.g., response time] | [e.g., < 200ms p95] | [how measured] |
| Scalability | [e.g., concurrency / volume] | [TBD] | [TBD] |
| Availability | [uptime / SLA] | [e.g., 99.9%] | [SLOs, error budget] |
| Reliability | [failure modes] | [TBD] | [retries, idempotency] |
| Security | [auth, encryption, secrets] | [TBD] | [threat model notes] |
| Privacy | [PII, consent, retention] | [TBD] | [DPA, residency] |
| Accessibility | [WCAG] | [e.g., WCAG 2.1 AA] | [keyboard/screen reader] |
| Observability | [logging/metrics/tracing] | [TBD] | [dashboards/alerts] |
| Compliance | [regulatory] | [TBD] | [GDPR, SOC2, etc.] |
| Compatibility | [platforms/browsers/devices] | [TBD] | [supported matrix] |

---

<a id="ux-ui-requirements"/>

## 9) UX / UI Requirements

### 9.1 Design Principles

- [Principle 1]
- [Principle 2]
- [Principle 3]

### 9.2 Key Screens / Flows

| Screen / Flow | Description | Wireframe / Mockup |
|--------------|-------------|-------------------|
| [TBD] | [TBD] | [Link or TBD] |
| [TBD] | [TBD] | [Link or TBD] |

### 9.3 UX Notes

- **Information architecture / navigation:** [TBD]
- **Empty states:** [TBD]
- **Loading states:** [TBD]
- **Error states:** [TBD]
- **Copy/content needs:** [TBD]
- **Localization / i18n:** [TBD]

---

<a id="data-integrations-apis"/>

## 10) Data, Integrations & APIs

> **PRD guidance:** This section captures **requirements and constraints** about
> data and integrations (the "what" and "why").
> Detailed schemas, endpoint definitions, event payloads, and storage design belong in a **Technical Spec / API Spec**.

- **Technical Spec (link):** [TBD] (template: `../TECH-SPEC/TECH-SPEC.template.md`)
- **API / Events Spec (link, if separate):** [TBD]
- **Data retention / privacy policy reference (link, if applicable):** [TBD]

### 10.1 Data Requirements (Outcome-focused)

| ID | Requirement | Rationale | Priority (MoSCoW) | Notes |
|----|-------------|-----------|-------------------|-------|
| DR-01 | The system shall capture/derive... | [TBD] | Must / Should / Could / Won't | [TBD] |
| DR-02 | The system shall allow users to... (export/delete/consent) | [TBD] | Must / Should / Could / Won't | [TBD] |

### 10.2 Integration Requirements

| Integration | Purpose | Requirement (what must work) | Owner | Notes |
|------------|---------|-------------------------------|-------|-------|
| [Service/System] | [TBD] | [e.g., "must sync X within Y minutes"] | [TBD] | [TBD] |

### 10.3 API / Event Impact (Requirement-level)

- **New capabilities required:** [e.g., "must provide a way to create/update X"]
- **Compatibility constraints:** [e.g., "must not break existing clients"; "must support old + new behavior for N
  weeks"]
- **Deprecations / migrations (user-facing):** [TBD]

---

<a id="technical-architecture-constraints"/>

## 11) Technical Architecture & Constraints

> **PRD guidance:** Keep this section to **non-negotiable constraints** and product-impacting technical considerations.
> Architecture, stack choices, migrations, feature-flag implementation, and
> rollback mechanics belong in a **Technical Spec**.

- **Technical Spec (link):** [TBD] (template: `../TECH-SPEC/TECH-SPEC.template.md`)

### 11.1 Non-Negotiable Constraints (Product-impacting)

- **Platforms/environments:** [e.g., must work on web + iOS; must support on-prem]
- **Security/compliance constraints:** [e.g., data residency; encryption; auditability]
- **Performance/scale constraints (if not already in NFRs):** [TBD]
- **Operational constraints:** [e.g., must be safe to roll back; must support gradual rollout]

### 11.2 Technical Decisions Out of Scope for this PRD

> This section acknowledges technical decisions that are deliberately deferred to
> the Tech Spec, not forgotten. It prevents the PRD from expanding into a
> technical design document and signals to engineers where to look for (or create)
> those answers.

- [e.g., choice of database / framework]
- [e.g., internal service boundaries]
- [e.g., detailed migration plan]

---

<a id="analytics-metrics"/>

## 12) Analytics & Metrics

- **North Star metric:** [TBD]
- **Primary success metrics:** [TBD]
- **Secondary metrics:** [TBD]
- **Guardrail metrics:** [latency, error rate, cost, satisfaction, abuse]

---

<a id="release-rollout-plan"/>

## 13) Release & Rollout Plan

### 13.1 Milestones

| Milestone | Description | Target Date | Exit Criteria |
|-----------|-------------|------------|--------------|
| M1 | [Alpha/MVP] | [TBD] | [TBD] |
| M2 | [Beta] | [TBD] | [TBD] |
| M3 | [GA] | [TBD] | [TBD] |

### 13.2 Phasing & Rollout Strategy

- **Phase 1:** [internal] — [scope, audience, % rollout]
- **Phase 2:** [limited external] — [scope, audience, % rollout]
- **Phase 3:** [general availability] — [scope, audience]

### 13.3 Operational Readiness

> **PRD guidance:** Keep this section at a product level (milestones, audience, sequencing).
> Detailed runbooks, monitoring setup, support rotations, and rollback procedures belong in a **Launch Runbook**.

- **Launch Runbook (link):** [TBD] (template: `../LAUNCH/Launch-runbook.template.md`)

#### Launch Requirements (High-level)

- **Support readiness:** [TBD — who supports, what docs must exist]
- **Customer comms / enablement:** [TBD]
- **Rollout constraints:** [e.g., phased rollout required; must support disabling feature]

---

<a id="testing-validation-definition-of-done"/>

## 14) Testing, Validation & Definition of Done

### 14.1 Validation Approach

- [prototype tests / usability sessions / experiment plan]

### 14.2 test plan

> **PRD guidance:** The PRD should define **acceptance criteria** (see Functional
> Requirements) and how we'll validate outcomes.
> Detailed test strategy and coverage planning belong in a **QA / test plan**.

- **QA / test plan (link):** [TBD] (template: `../QA/QA-test-plan.template.md`)

### 14.3 Entry / Exit Criteria

- **Entry criteria:** [TBD]
- **Exit criteria:** [TBD]

### 14.4 Definition of Done

- [ ] Functional requirements met (acceptance criteria pass)
- [ ] Non-functional targets met or exception approved
- [ ] Instrumentation in place
- [ ] Docs updated
- [ ] Rollback plan verified

---

<a id="risks-mitigations"/>

## 15) Risks & Mitigations

| # | Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation | Owner |
|---|------|---------------------|----------------|------------|-------|
| R1 | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| R2 | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

---

<a id="open-questions"/>

## 16) Open Questions

| # | Question | Owner | Due Date | Resolution |
|---|----------|-------|---------|-----------|
| Q1 | [TBD] | [TBD] | [TBD] | [TBD] |
| Q2 | [TBD] | [TBD] | [TBD] | [TBD] |

---

<a id="decisions-log"/>

## 17) Decisions Log

| ID | Date | Decision | Rationale | Owner |
|----|------|----------|-----------|-------|
| D-001 | [TBD] | [TBD] | [TBD] | [TBD] |

---

<a id="appendix"/>

## 18) Appendix

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| User Journey | The broadest level of user-facing specification. A high-level narrative of the full experience from start to finish, like a "movie" of the user's interaction. Primarily used for stakeholder alignment and UX direction. A journey may span multiple use cases. |
| Use Case | Medium granularity. A structured, detailed specification of one specific interaction: who the actor is, what must be true before, the step-by-step flow, what is true after, and what happens when things go wrong. Serves design and engineering. A use case may be broken into multiple user stories. |
| User Story | The smallest unit. A short, plannable chunk of work from the user's perspective ("As a... I want to... So that..."). Delivery-focused — meant to be estimated, prioritized, and assigned to sprints. |
| North Star Metric | The single most important metric that best captures the core value the product delivers to its users. It is the one number you would track above all others to know whether the product is succeeding (e.g., for Spotify it might be "time spent listening"). |
| [TBD] | [TBD] |

### Appendix B: References

- [Link or document reference 1]
- [Link or document reference 2]

### Appendix C: Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [TBD] | [TBD] | Initial draft |

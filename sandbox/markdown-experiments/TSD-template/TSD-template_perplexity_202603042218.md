---
date: [YYYY-MM-DD]
author: [Your name]
reviewers: [Tech lead, Architect, QA, DevOps]
status: Draft | In Review | Approved
version: 0.1
related_docs:
  - PRD: [link]
  - Architecture Decision Records: [links]
  - API Specs: [links]
  - Data Model Docs: [links]
---

# Technical Specification Document (TSD) Template

> **How to use this template**
> - This template is intended to be filled via an interview between an LLM and a human.
> - Every section should be detailed enough that an experienced engineer can implement the system without guessing.
> - Prefer concrete examples, data shapes, and edge cases over vague descriptions.

---

## 1) Document Overview

- **System / Feature Name:** [TBD]
- **One-liner (technical):** [e.g., "Event-driven service that ingests X, enriches with Y, and exposes Z via REST"]
- **Scope Summary:** [What is technically in and out of scope for this TSD]
- **Target Release / Milestone:** [TBD]
- **Owning Team(s):** [TBD]
- **Tech Stack (expected):** [e.g., Node.js, PostgreSQL, Kafka, React, Kubernetes]

---

## 2) Functional Overview (Technical View)

- **Brief description of behavior:** [How the system behaves from a technical/architectural point of view]
- **Key capabilities / responsibilities:**
  - [Capability 1]
  - [Capability 2]
- **Non-responsibilities (clear boundaries):**
  - [Explicitly not responsible for…]
- **Key constraints inherited from PRD:** [Performance, platforms, compliance, etc.]

---

## 3) Architecture & Components

### 3.1 High-Level Architecture

- **Architecture style:** [e.g., monolith, microservice, event-driven, serverless, hybrid]
- **Context diagram (textual description if no diagram):**
  - **System under design (SuD):** [Name]
  - **Upstream systems:** [Names, purpose, integration type]
  - **Downstream systems:** [Names, purpose, integration type]
- **Execution environments:** [dev, staging, prod; on-prem vs cloud; regions]

### 3.2 Internal Components

For each internal component or service, describe:

- **Component name:** [TBD]
- **Responsibility:** [What it does]
- **Technology / language / framework:** [TBD]
- **Interface(s):** [APIs, queues, CLI, UI modules exposed]
- **Dependencies:** [Other services, databases, caches, external APIs]
- **Statefulness:** [Stateless / stateful; where state lives]
- **Scaling model:** [Horizontal/vertical; auto-scaling rules if any]

Repeat the above subsection for each component.

---

## 4) Data Model & Storage

### 4.1 Data Entities

For each core entity:

- **Entity name:** [e.g., UserSession]
- **Description:** [What it represents]
- **Fields (schema):**
  - `field_name` (type, nullable, default, constraints, example value)
- **Identifiers and keys:**
  - **Primary key:** [TBD]
  - **Natural keys / unique constraints:** [TBD]
- **Relationships:** [1:1, 1:N, N:M with other entities]
- **Versioning / history:** [Soft deletes, audit, event sourcing, etc.]

### 4.2 Storage Design

- **Storage technologies:** [e.g., PostgreSQL, Redis, S3, Elasticsearch]
- **Rationale for choice:** [Latency, consistency, query patterns, cost]
- **Logical vs physical schema notes:** [Schemas, tablespaces, indices]
- **Indexing strategy:** [Primary/secondary indices, expected query patterns]
- **Partitioning / sharding:** [Approach, keys, migration considerations]
- **Retention policies:** [How long data is kept; archival process]
- **Backup & restore:** [Frequency, mechanism, RPO/RTO expectations]

### 4.3 Data Flows

- **Ingestion paths:** [From where data arrives, in what format, via which interface]
- **Transformation / enrichment:** [Steps, rules, tools]
- **Export paths:** [Downstream consumers, formats, protocols]

Provide at least one end-to-end example of a key data flow, including example payloads.

---

## 5) APIs, Contracts & Integrations

### 5.1 Public APIs (Exposed by this system)

For each endpoint or operation:

- **Name:** [e.g., Create Order]
- **Protocol / style:** [REST/HTTP, gRPC, GraphQL, WebSocket, RPC, etc.]
- **URL / method / route:** [`POST /v1/orders`]
- **Authentication / authorization requirements:** [Token type, scopes, roles]
- **Request schema:**
  - JSON body example
  - Field descriptions (required/optional, types, constraints)
- **Response schema:**
  - Success response example
  - Error response examples (with codes)
- **Idempotency behavior:** [Idempotency keys, retry safety]
- **Validation rules:** [Field-level and cross-field]
- **Rate limits / quotas:** [If applicable]
- **Backward compatibility rules:** [Versioning strategy, deprecated fields]

Repeat for each external-facing operation.

### 5.2 Internal APIs / Module Interfaces

- **Service-to-service contracts:** [RPC, event contracts, database access patterns]
- **Feature flags / configuration interfaces:** [Names, types, rollout rules]

### 5.3 Eventing & Messaging

For each event or message:

- **Event name / topic / channel:** [e.g., `user.created` on Kafka topic `users`]
- **Producer(s):** [Which component emits]
- **Consumer(s):** [Which component listens]
- **Schema:** [Fields, types, semantics, example payload]
- **Ordering & delivery guarantees:** [At-least-once, exactly-once (logical), ordering by key]
- **Error handling:** [Dead-letter queues, retries, poison message handling]
- **Retention / compaction:** [Broker settings relevant to this event]

### 5.4 External Integrations

For each external system:

- **System name:** [e.g., Stripe, Salesforce, internal auth service]
- **Purpose:** [Why integrate]
- **Integration method:** [REST, SDK, webhook, database link, file transfer, etc.]
- **Authentication:** [API keys, OAuth, mutual TLS, etc.]
- **Endpoints / contracts used:** [List with brief descriptions]
- **Rate limits & SLAs:** [Service-specific limits; how you adapt to them]
- **Failure / degradation strategy:** [Timeouts, backoff, circuit breakers, fallbacks]
- **Sandbox vs production:** [Environments, configuration differences]

---

## 6) Detailed Behavior & Flows

### 6.1 Key Technical Flows

For each important flow (aligned with PRD use cases):

- **Flow name:** [e.g., "User signup and verification"]
- **Trigger:** [User action, scheduled job, external event]
- **Steps (system-centric):**
  1. [Component A receives …]
  2. [Validates …]
  3. [Writes to DB …]
  4. [Emits event …]
- **Data touched:** [Entities, tables, caches, external services]
- **Success criteria:** [What "done" means technically]
- **Edge and error conditions:** [Invalid inputs, timeouts, partial failures, concurrency conflicts]
- **Idempotency and retries:** [How duplication, replays, and retry storms are handled]

### 6.2 State Machines / Lifecycle

For any entity with a clear lifecycle:

- **Entity:** [e.g., Order]
- **States:** [e.g., CREATED, PENDING, CONFIRMED, FAILED, CANCELLED]
- **Transitions:**
  - From → To → Trigger → Responsible component
- **Invariants:** [What must be true in each state]

### 6.3 Scheduled / Background Jobs

For each job:

- **Name & purpose:** [TBD]
- **Schedule / trigger:** [Cron, event-based, manual]
- **Inputs:** [Data sources]
- **Processing logic:** [High-level algorithm]
- **Outputs:** [Writes, events, notifications]
- **Timeouts & retries:** [Strategy, limits]
- **Observability:** [Metrics and logs for this job]

---

## 7) Non-Functional Requirements (Technical Detail)

> This section should translate PRD-level NFRs into concrete technical targets and designs.

### 7.1 Performance

- **Latency targets:** [Per operation; p50/p95/p99; by endpoint or use case]
- **Throughput targets:** [Requests per second, messages per second, batch sizes]
- **Load profile assumptions:** [Peak vs average, traffic patterns]
- **Performance strategies:** [Caching, pagination, batching, connection pooling]
- **Capacity planning notes:** [Initial sizing, headroom assumptions]

### 7.2 Scalability

- **Scaling strategy:** [Horizontal/vertical, autoscaling policies, limits]
- **Bottlenecks identified:** [DB, external API, CPU, memory, disk, network]
- **Multi-tenant / multi-region considerations:** [Isolation, routing, data locality]

### 7.3 Availability & Reliability

- **Target availability / SLA:** [e.g., 99.9%]
- **Failure domains:** [Which components can fail independently]
- **Redundancy / failover:** [Active-active, active-passive, zone and region strategies]
- **Timeouts & retries:** [Standard values, exponential backoff configuration]
- **Circuit breakers / bulkheads:** [Where applied and thresholds]
- **Degradation modes:** [What features are disabled or simplified when dependencies fail]

### 7.4 Security

- **Authentication:** [Mechanisms, identity providers, token formats]
- **Authorization / RBAC model:** [Roles, permissions, resource scoping]
- **Data protection:**
  - At rest: [Encryption approach, key management]
  - In transit: [Protocols, TLS versions, cipher suites]
- **Secrets management:** [Tooling, rotation policies]
- **Threat model highlights:** [Key threats, mitigations; e.g., injection, DOS, privilege escalation]
- **Audit logging:** [What gets logged, where, and retention]

### 7.5 Privacy & Compliance

- **Personal data handled:** [Types, fields, sensitivity]
- **Data residency:** [Regions, constraints]
- **Consent and user rights:** [Access, delete, export flows; technical implementation]
- **Compliance references:** [GDPR, SOC2, HIPAA, others; how this design aligns]

### 7.6 Observability

- **Logging:**
  - Log levels, structure (JSON or not), correlation IDs
  - PII handling in logs
- **Metrics:**
  - Key metrics (throughput, latency, errors, saturation, custom business metrics)
  - Metric names and labels (if standardized)
- **Tracing:**
  - Trace propagation (headers, libraries)
  - Sampling strategy
- **Dashboards & alerts:**
  - Required dashboards
  - Alert conditions, thresholds, paging rules

### 7.7 Accessibility (for UI components)

- **Standards targeted:** [e.g., WCAG 2.1 AA]
- **Specific requirements:** [Keyboard navigation, ARIA usage, color contrast, screen reader support]

### 7.8 Compatibility

- **Supported platforms:** [OS, browsers, app versions, devices]
- **Backward compatibility obligations:** [APIs, events, database schemas]

---

## 8) Configuration, Feature Flags & Environments

- **Configuration sources:** [Env vars, config files, config service]
- **Configuration items:** [List important knobs, defaults, allowed ranges]
- **Feature flags:**
  - Names and purpose
  - Scope (user, tenant, environment)
  - Rollout strategy (percentage, segments)
- **Environment differences:** [Dev/stage/prod differences; fake services; data anonymization]

---

## 9) Deployment, Operations & Runbooks

### 9.1 Build & Deploy Pipeline

- **CI/CD tooling:** [e.g., GitLab CI, GitHub Actions, Jenkins]
- **Build artifacts:** [Image types, artifact repositories]
- **Deployment strategy:** [Blue/green, canary, rolling, manual]
- **Migration handling:** [DB migrations, backward-compatible rollout steps]

### 9.2 Runtime Environment

- **Orchestration:** [Kubernetes, ECS, bare metal, serverless platform]
- **Resource allocation:** [CPU/memory limits & requests]
- **Networking:** [Service discovery, ingress, load balancers, firewalls, VPCs]

### 9.3 Operational Procedures

- **Standard runbooks (links or summaries):**
  - Deploying
  - Rolling back
  - Handling incidents
  - Rotating secrets / certificates
- **On-call expectations:** [Who owns, escalation paths]

---

## 10) Testing Strategy (Technical)

> This complements the PRD's acceptance criteria with concrete test approaches.

- **Test types and coverage expectations:**
  - Unit tests: [What must be covered, minimum coverage]
  - Integration tests: [Critical flows, dependencies, data setup]
  - Contract tests: [API and event contracts; provider/consumer tests]
  - End-to-end tests: [Smoke tests, critical paths]
  - Performance tests: [Load, stress, soak; scenarios and target metrics]
  - Security tests: [Static analysis, dependency scanning, penetration tests]
- **Test data strategy:** [Synthetic vs anonymized production data; seeding; masking]
- **Automation:** [What is mandatory in CI; blocking vs non-blocking checks]

---

## 11) Migration & Rollout Plan (Technical Detail)

- **Initial data migration needs:** [Source systems, volumes, approach]
- **Migration strategy:** [Big bang, incremental, dual-write, backfill]
- **Coexistence period:** [How old and new systems run together; routing rules]
- **Cutover plan:** [Switching traffic, validation, rollback triggers]
- **Rollback strategy:** [What can be rolled back safely; one-way operations; mitigations]

---

## 12) Risks, Trade-offs & Open Issues

### 12.1 Technical Risks

For each risk:

- **ID:** [R-1]
- **Description:** [TBD]
- **Likelihood:** [High/Medium/Low]
- **Impact:** [High/Medium/Low]
- **Mitigation / contingency:** [Plan]

### 12.2 Technical Trade-offs

- **Decision:** [e.g., "Use eventual consistency instead of strong consistency for X"]
- **Alternatives considered:** [Option A, B, C]
- **Rationale:** [Why chosen]
- **Implications:** [Operational, performance, complexity, future changes]

### 12.3 Open Questions

- **ID:** [Q-1]
- **Question:** [TBD]
- **Owner:** [TBD]
- **Due date:** [TBD]
- **Notes / partial answers:** [TBD]

---

## 13) Change Log

| Version | Date       | Author       | Summary of Changes             |
|---------|------------|--------------|--------------------------------|
| 0.1     | [YYYY-MM-DD] | [Name]     | Initial draft                  |

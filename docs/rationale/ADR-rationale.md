---
author: Iddo Lev
LLM-co-author: claude-Opus-4.6
last-updated: 2026-03-07
---

# (Any) Decision Records (ADRs) — Rationale

## What Are ADRs?

The term ADR originally stood for "Architecture Decision Record," introduced
by Michael Nygard in 2011 specifically for architectural decisions — those that
are hardest to reverse and most expensive to get wrong. However, in practice
the decisions worth recording aren't limited to architecture. Examples:

- **Technology choices** — "We use Memcached, not Redis" (arguably architectural,
  but often just a tooling preference)
- **Convention decisions** — "All API responses use camelCase keys"
  (not architecture, but violating it creates inconsistency)
- **Process decisions** — "We don't write migration scripts for dev databases,
  only for staging/prod" (operational, not architectural)
- **Design tradeoffs** — "We denormalize the user profile into the orders table
  for read performance" (data design, borderline architectural)

The line between "architectural" and "just a decision" is blurry. What matters
is whether the decision **constrains future work by other agents or people**.
If it does, it should be recorded regardless of whether it's "architectural"
in the strict sense.

Some teams have adopted the term "Any Decision Record" (keeping the ADR acronym)
or simply "Decision Records." In this framework, we use ADR to mean
**Any Decision Record** — any project-wide decision that constrains future work.

An ADR is a short document that captures one decision along with its context
and consequences. ADRs are numbered sequentially (e.g., ADR-001, ADR-002)
and are append-only: once accepted, an ADR is never edited. If a decision changes,
a new ADR is written that supersedes the old one.

### Typical ADR Structure

- **Title** — short name for the decision
- **Status** — Proposed, Accepted, Deprecated, Superseded
- **Context** — what problem or situation prompted the decision
- **Decision** — what was decided
- **Consequences** — what follows from the decision (positive and negative)

Popular formats include Michael Nygard's original template (the above),
MADR (adds "Options Considered" and pros/cons), and Y-Statements
(single-sentence format: "In the context of X, facing Y, we decided Z,
to achieve W, accepting Q").

### Why ADRs Matter

- **Memory** — teams forget *why* something was done a certain way. ADRs prevent this.
- **Onboarding** — new team members can read the decision log to understand
  the project's evolution.
- **Accountability** — forces explicit reasoning rather than implicit assumptions.
- **Reversibility** — when revisiting a decision, the original context is preserved.
  An ADR is marked "Superseded by ADR-XXX" rather than deleted.

### Key Principles

1. **Immutable once accepted** — don't edit old ADRs. Write a new one
   that supersedes the old.
2. **Short and focused** — one decision per record. A few paragraphs, not a thesis.
3. **Written at decision time** — not retroactively. The context is freshest
   when the decision is made.
4. **Lightweight** — the format shouldn't be a burden.

---

## ADRs in Human Teams vs. Agent Teams

### Who Writes ADRs in a Human Team?

The person who drives the decision writes the ADR — typically the tech lead
or architect for cross-cutting concerns, or the developer who researched
the options for localized decisions. The key rule: whoever has the most context
writes it, then the team reviews it.

### Who Writes ADRs in an Agent Team?

The **tech lead agent** writes most ADRs, since it is the architectural authority
and has the broadest context. However, coding specialist agents (backend, frontend)
may also need to write ADRs when implementation reality forces a pivot from the
planned approach — they discover during implementation that the TSD's design
doesn't work, choose an alternative, and record why.

### Why ADRs Are Arguably More Important in Agent Workflows

In human teams, ADRs fight **memory loss over time** — people forget, leave,
or weren't in the meeting.

In agent teams, ADRs fight **context loss across sessions and agents**.
Agents don't share a persistent memory by default. An ADR tells Agent B
*why* Agent A chose an approach, preventing Agent B from undoing it
or re-litigating the same question. There are no hallway conversations,
no institutional memory — ADRs are the only durable record of design reasoning
that persists across agent invocations.

---

## The Ideal ADR System for Agentic Workflows

### Desired Behavior

The ideal ADR system would be a **queryable service** that agents interact with
through two operations:

**1. Query before acting:**
An agent about to make a decision or start implementation would ask:
"I'm going to do X / I decided on approach Y — does this contradict
any previous ADR?" The system would perform semantic retrieval over the ADR
database, find relevant records based on meaning (not keyword matching),
and return any ADRs that the agent should be aware of.

**2. Record after deciding:**
An agent that made an ADR-level decision would submit the new record
to the system, which would add it to the database, update its semantic index,
and make the decision immediately available for future queries.

This requires:

- A **persistent store** for ADR records (not flat files)
- A **semantic embedding pipeline** that indexes ADRs by their meaning
  (so a query about "caching with Redis" retrieves ADR-007 about
  "choosing Memcached over Redis" even though the query words differ)
- A **retrieval service** (likely an MCP server or similar tool server)
  that agents can call as a tool during their workflow
- Logic to handle **ADR lifecycle** — superseded records should still be
  retrievable but marked as no longer active

This system would eliminate the context-window cost of reading an entire ADR log,
and would scale to hundreds of decisions without degradation.

### Implementation Path: MCP Server

The natural implementation for this system in Claude Code is an **MCP server**
(Model Context Protocol). An MCP server is a small process that Claude Code
spawns at startup and keeps alive for the session. It exposes tools that any
agent can call natively — just like built-in tools (Read, Write, etc.).

The ADR MCP server would expose tools such as:

- `record_adr(title, context, decision, consequences)` — append a new ADR,
  update the semantic index, and make it immediately queryable
- `check_adr(proposed_decision)` — query existing ADRs for conflicts with
  a proposed decision and return relevant records
- `list_adrs(topic?)` — browse or filter ADRs by topic

Because MCP tools appear natively to all agents, no per-agent configuration
is needed — agents simply call `check_adr` before making decisions and
`record_adr` after making them. The server handles formatting, numbering,
indexing, and persistence.

**Resource cost:** Negligible. The server process is idle almost all the time
(blocked on stdin, consuming ~20-30 MB of runtime baseline, 0% CPU while idle).
When a tool is called, it processes the request in milliseconds and goes back
to sleep. No cloud billing, no API costs — it's a local process.

**Semantic retrieval options** (from simple to sophisticated):

1. **Keyword/tag matching** — each ADR gets tags, `check_adr` does string
   matching. Crude but zero dependencies.
2. **Embedding-based** — on startup, the server loads all ADRs, generates
   embeddings (via a local model or API call), and does cosine similarity
   on `check_adr` queries. More accurate but adds a dependency.
3. **Pass-through to the LLM** — for projects with fewer than ~100 ADRs,
   the server returns all records (or a filtered subset) and lets the agent's
   own reasoning determine conflicts. Dumb retrieval, smart consumer.
   This is the pragmatic starting point.

**Setup:** The framework's `framework-initial-install` step would install the server
script (e.g., to `.claude/scripts/adr-server.py`) and add the MCP
configuration entry to `.claude/settings.json`.

### Current Status

**This system does not exist yet.** The MCP-based implementation described
above is the planned approach. It requires building the server script,
semantic retrieval logic, and framework integration. It would be a valuable
standalone tool to build in the future.

---

## Current Approach: Index + List + Tech Lead as Gatekeeper

In the absence of the ideal queryable ADR system, we use a pragmatic
file-based approach with two artifacts and a human-like gatekeeper pattern.

### Two Files

**`ADR-index.md`** — a compact table with one row per ADR: number, title, status,
and a one-line summary. This file is designed to be cheap to read — even with
50+ ADRs, it remains a short table that consumes minimal context window.

**`ADR-list.md`** — the full ADR records with complete context, decision,
and consequences sections. This file grows over time and may become large.

The index exists so that an agent can scan it quickly and then read only the
specific full records that are relevant — rather than consuming the entire
ADR list every time.

### Who Reads What and When

The **tech lead agent** is the ADR gatekeeper:

- It reads `ADR-index.md` when planning work or assigning tasks,
  to check for decisions that constrain the approach
- When a relevant ADR is identified in the index, it reads
  the corresponding full record from `ADR-list.md`
- When assigning tasks to specialist agents, it includes references
  to relevant ADRs directly in the task description
  (e.g., "Note: see ADR-007, we use Memcached, not Redis")

**Specialist agents** (backend, frontend, etc.) do **not** routinely read the ADR
index or list. They receive relevant ADR constraints from the tech lead
as part of their task assignments. This keeps their context windows focused
on implementation.

**The code reviewer** may read `ADR-index.md` before reviewing code
if the review touches architectural concerns, to verify that the implementation
aligns with recorded decisions.

### Scaling

If `ADR-list.md` becomes too large for practical use, it can be split:

- **By topic** — e.g., `ADR-list-api.md`, `ADR-list-data.md`,
  `ADR-list-infrastructure.md`
- **By date/phase** — e.g., `ADR-list-v1.md`, `ADR-list-v2.md`

The index file may also be split if it becomes too long.

### Concrete Scenario: Why This Matters

The tech lead assigns the backend specialist: "Add a caching layer
for API responses."

Without ADRs, the backend specialist might choose Redis (a reasonable default).
But ADR-007 recorded: "We chose Memcached over Redis because our infrastructure
team only supports Memcached in production."

With the current approach, the tech lead scans the ADR index before assigning
the task, sees ADR-007's one-liner about caching, reads the full record,
and adds to the task: "Use Memcached per ADR-007." The backend specialist
never needs to read the ADR list at all — the constraint arrives
as part of the task.

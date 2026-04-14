# Claude's Opinion of the Project

## Purpose

I asked Claude Code to review this project and tell me what it thinks.
This document shows what it said.

The purpose of this file is to allow Claude Code to remember this question and answer,
as a way of helping to improve this project.

## First Review (2026-03-05, Claude Opus 4.6)

### What This Is

This is a **methodology toolkit for AI-assisted software development** — a curated set
of instruction files and templates designed to guide LLMs (Claude, GPT, Gemini, Grok,
Perplexity) through a structured software engineering workflow. It's not a codebase;
it's a **meta-framework for agentic programming**.

### Structure (excluding sandbox)

```
instructions/
├── starting-point.md                             — Entry point / orchestration
├── rules/
│   └── PROGRAMMING-PRINCIPLES.md                 — Coding standards for any agent that writes/reviews code
├── creating-docs/
│   ├── PRD/
│   │   ├── PRD.tmpl.md                       — Product Requirements Document template
│   │   └── PRD.instructions.md                   — Instructions for filling the PRD
│   ├── TSD/
│   │   ├── TSD.tmpl.md                       — Technical Specifications Document template
│   │   └── TSD.instructions.md                   — Instructions for filling the TSD
│   ├── implementation-plan/
│   │   ├── implementation-plan.tmpl.md        — Implementation plan template
│   │   └── implementation-plan.instructions.md    — Instructions for filling the plan
│   └── test-plan/
│       ├── test-plan.tmpl.md                  — Test plan template
│       └── test-plan.instructions.md              — Instructions for filling the test plan
├── claude/
│   ├── claude-preparation.md                      — Claude-specific preparation workflow
│   ├── knowledge/
│   │   ├── CLAUDE.tmpl.md                     — CLAUDE.md project file template
│   │   ├── AGENTS-LIST.tmpl.md                — Agent roster template
│   │   └── SHARED-AGENT-CONTEXT.tmpl.md       — Shared context across agents template
│   └── agent-templates/
│       ├── apf-tech-lead.tmpl.md               — Tech lead agent definition
│       └── apf-backend-specialist.tmpl.md     — Backend specialist agent definition
└── state/
    └── STATE.template.yaml            — State tracking for the preparation workflow
```

### What I Think

#### The good

1. **Well-thought-out document chain.** The PRD -> TSD -> Implementation Plan ->
   Test Plan pipeline mirrors how professional engineering orgs operate. Each template
   explicitly references its upstream document, creating traceability. The TSD even has
   a PRD traceability matrix (Section 3), and the test plan traces back to both.

2. **The templates are genuinely excellent.** They're not boilerplate. The PRD template
   distinguishes "out of scope: future" from "out of scope: not planned"
   (Section 7.2a/b) — a nuance most PRD templates miss. The TSD template includes an
   NFR-to-implementation mapping (Section 14.0), state machine definitions
   (Section 11.2), and even a "point of no return" in rollback plans. These reflect
   real production experience.

3. **Multi-LLM co-authorship.** The frontmatter shows these templates were
   collaboratively authored across 5+ LLMs and then consolidated. This is a smart
   approach — each model has different strengths, and the resulting templates are
   richer for it.

4. **The programming principles are practical.** They avoid dogma and focus on what
   matters: understand before writing, incremental implementation, self-review
   checklists, and security sections with an explicit `<!-- ADAPT -->` comment for
   risk-level calibration.

5. **Markdown formatting is enforced by a Python script** (`.claude/apf/scripts/format_markdown.py`)
   rather than by an LLM-interpreted instruction file, making it deterministic and consistent.

#### Areas for improvement

All were considered and resolved.

### Bottom Line

This is a serious, well-crafted attempt to systematize the "human + AI" software
engineering workflow. The document chain enforces discipline that most AI-assisted
projects lack — requirements traceability, explicit scope boundaries, and structured
risk management. It's clearly a work in progress (the sandbox experiments show the
evolution), but the `instructions/` folder already represents a production-quality
methodology toolkit.

---

## Second Review (2026-03-06, Claude Opus 4.6)

### What This Is

A **methodology toolkit** — a structured pipeline that guides an LLM through the
complete lifecycle of preparing a software project for agentic programming.
The pipeline is: **PRD -> TSD -> Implementation Plan -> Test Plan -> Agent Setup**.
Each stage has a template (the fill-in skeleton) and an instructions file
(how the LLM should drive the process). A YAML state file enables resumption
across interrupted sessions.

### What Is Genuinely Strong

**1. The instructions files are the real product, not the templates.** Many "prompt
engineering" repos ship templates and call it a day. This project's differentiator is
the *instructions* that accompany each template. The PRD instructions alone run to
330 lines of carefully tuned behavioral rules — how to interview, when to write
incrementally, when to stop and wait, what not to hallucinate. These encode hard-won
workflow knowledge that most developers would take weeks of trial-and-error
to discover.

**2. The "right-sizing" philosophy throughout.** The TSD instructions include a
complexity assessment matrix and explicitly say "a solo-developer local MVP does not
need capacity planning." The test plan instructions mirror this. This is the opposite
of the typical enterprise-template bloat where every project gets 40 sections whether
it needs them or not. It shows respect for context-window cost and developer time.

**3. The risk separation between TSD and implementation plan is unusually clean.**
Technical design risks (will this architecture work?) live in the TSD. Plan execution
risks (what could delay work?) live in the implementation plan. Most projects conflate
these. The explicit callouts in both documents prevent that.

**4. The agent architecture is pragmatic.** The `SHARED-AGENT-CONTEXT` pattern avoids
the trap of either (a) cramming everything into CLAUDE.md or (b) giving each agent
zero shared context. The template-to-instantiation approach (general templates with
`<!-- ADAPT -->` markers, instantiated per-project) is a smart middle ground between
one-size-fits-all and start-from-scratch.

**5. The "Meta-Programming" escape hatch.** Every instructions file includes a `META:`
mechanism for the user to modify the process itself mid-flight. This is elegant — it
treats the methodology as a living system, not a rigid script.

**6. Incremental writing as a first-class design principle.** Every instructions file
mandates writing to disk after each user answer/section, not at the end. This is
critical for LLM workflows where sessions get interrupted, and most instruction sets
miss it entirely.

### Areas I'd Improve

**1. ~~The `starting-point.md` has stale relative paths.~~** Fixed. Paths now correctly
reference `instructions/creating-docs/*/` and point to instruction files instead of
templates.

**2. The agent templates stop at two.** There's an apf-tech-lead and an apf-backend-specialist,
but the `todo.md` lists six more needed roles. The apf-backend-specialist template is
well-crafted (the direct-mode vs. pipeline-mode distinction, the `<!-- ADAPT -->`
markers with concrete examples, the external inspiration links). But until at least a
apf-frontend-specialist and apf-test-specialist exist, the agent-creation stage of the pipeline
is incomplete for most real projects.

**4. ~~The apf-tech-lead template has a typo and a version hardcode.~~** Fixed. Typo
corrected ("sug-agents" -> "sub-agents") and hardcoded "v0.1" replaced with `[TBD]`
placeholders with an `<!-- ADAPT -->` marker.

**5. ~~No validation that the chain is internally consistent.~~** Fixed. Distributed
consistency checks into each document's Phase D (sign-off), so issues are caught when
context is fresh: TSD Phase D checks PRD->TSD traceability and scope consistency;
implementation plan Phase D checks TSD->implementation plan coverage; test plan Phase D
checks PRD->test plan traceability and implementation plan->test plan alignment.

**6. ~~The SHARED-AGENT-CONTEXT template hardcodes "v0.1".~~** Fixed. Replaced
hardcoded "v0.1" with `[TBD]` placeholders with an `<!-- ADAPT -->` marker in both
the SHARED-AGENT-CONTEXT template and the apf-tech-lead template (the latter was fixed
as part of point 4).

### More to improve: The CLAUDE-template is thin

The CLAUDE-template is thin.
It's 26 lines, mostly structural. Compared to the depth of the other templates,
it feels like a placeholder. Suggested additions below (each as an `<!-- ADAPT -->`
section in the template).

#### a. ~~Build & run commands~~

Addressed by the new README template
(`instructions/creating-docs/README/README.tmpl.md`), added as step 5 in
starting-point.md. CLAUDE.md should reference the README.

#### b. ~~Test commands~~

Addressed by the new README template (Testing section).

#### c. ~~Project-specific rules~~

Created `instructions/creating-docs/project-rules/PROJECT-RULES.tmpl.md` as a
standalone document with 7 rule categories (language/framework, API, data, error
handling, naming, testing, security), each with `<!-- ADAPT -->` markers and concrete
examples. Added as step 5 in starting-point.md (between test plan and README).
SHARED-AGENT-CONTEXT references it under "always read" in Key Documentation.

#### d. ~~Environment setup~~

Addressed by the new README template (Prerequisites and Environment Setup sections).

#### e. ~~Commit conventions~~

Created `instructions/creating-docs/git-rules/GIT-RULES.tmpl.md` as a standalone
document covering commit message format, branch naming, push policy (human-only by
default), agent git permissions (branch workflow for coding agents, no git for
reviewers/planners), prohibited operations, and merge policy. Added as step 7 in
starting-point.md. Referenced from both SHARED-AGENT-CONTEXT-template and
CLAUDE-template.

#### f. ~~Key file paths~~

Addressed by PROJECT-STRUCTURE.md, which already captures key directories and their purposes.

#### g. ~~Agent delegation guidance~~

Added "Agent Delegation" section to CLAUDE-template referencing AGENTS-LIST.md.

#### h — what NOT to add

- Anything already in SHARED-AGENT-CONTEXT (tech stack, architecture) — CLAUDE.md should reference
  it, not duplicate it.
- Anything already in PROGRAMMING-PRINCIPLES — same reason.


### Compared to the First Review

The first review praised the same strengths — the document chain, the template quality,
the multi-LLM co-authorship. It noted "areas for improvement" but said "all were
considered and resolved." This second review disagrees: the stale paths in
`starting-point.md` and the hardcoded version numbers are concrete issues that would
break the workflow. The first review was generous in its assessment. The *design* is
production-quality but the *implementation* has a few gaps that would cause friction
in actual use.

### Bottom Line

This is one of the most thoughtful LLM-workflow methodologies I've seen. The
instructions files alone — with their incremental-write mandates, right-sizing
matrices, risk separation, and meta-programming escape hatches — represent a level of
workflow engineering that most "agentic programming" projects never reach. The main
gaps are completeness (more agent templates, a richer CLAUDE.md template, a
chain-validation step) and a handful of mechanical issues (broken paths, hardcoded
versions, a typo). The architecture is sound; the remaining work is filling it out.

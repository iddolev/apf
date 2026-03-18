---
author: Iddo Lev
LLM_author: Claude Opus 4.6
last_update: 2026-03-12
---

# Agentic SDLC Automation — Strengths and Gaps

## Introduction

The emerging field of **Agentic SDLC Automation** — using AI agents to model and then automate as much as possible of the software development life cycle — aims to move beyond code generation into full lifecycle management: from requirements gathering through planning, implementation, testing, deployment, and monitoring. The goal is to have AI agents that understand not just how to write code, but how to shepherd a project through every phase that professional software engineering demands.

This document series examines the SDLC, the opportunity for automation, and one specific framework (GSD) as a case study — cataloging both its strengths (to learn from) and its gaps (to address), as input for designing a new agentic programming framework.

## General Documents

1. **[SDLC Overview](sdlc-overview.md)**: What is the Software Development Life Cycle? A comprehensive, technology-agnostic reference covering all phases, from requirements through maintenance, including cross-cutting concerns and why each phase matters.

2. **[Automatic SDLC](automatic-sdlc.md)**: How LLMs can automate the SDLC. Core concepts (modeling, verification, traceability), opportunities that were previously impractical (TDD at scale, DDD enforcement, continuous security auditing), the critical importance of code quality, and the human role in automated development.

## Reviews

### Baseline

The baseline is something like **Pure Claude Code Review**: [TBD: a review of using Claude Code as-is, without an additional layer such as GSD.
   e.g. describing to claude code the system idea in brief, asking it to define appropriate agents, then running them.
   Explanation why this comes short of what we want, not standardized enough, not thorough enough, 
   and that's why the frameworks below were created ]

But also do this for other frameworks similar to Claude Code (VSCode + Copilot? Roocode? OpenCode?)

### Commonalities

The following are workflow orchestration systems for agentic coding tools — specifically designed to make AI coding agents (primarily Claude Code) produce reliable, production-quality output by solving the same core problems: context management, structured planning, and execution discipline.

Here's a summary of what's common and the broader landscape.

[TBD: The LLM who produced the text here produced the following two sections 
even though they significantly overlap, though not 100%. So TBD: need to synthesize both parts into one text] 

#### Version 1

**The same diagnosis.** They all identify "context rot" — quality degradation as the AI's context window fills up — as the central problem. All three argue that raw AI coding is unreliable at scale, and that the fix is structured context, not better prompting per se.

**Spec-driven, phased execution**. Each breaks work into a plan → execute → verify loop. GSD calls it "plan-phase / execute-phase / verify-work," PAUL calls it "Plan-Apply-Unify," and Ultrawork/Oh My OpenCode uses Prometheus (planning) → Atlas (orchestration) → verified result. The philosophy is the same: define acceptance criteria upfront, execute against them, then reconcile.

**Multi-agent orchestration**. All three use specialized subagents for different roles — researchers, planners, executors, verifiers — rather than dumping everything into a single session. They coordinate these agents to keep individual context windows fresh.

**State persistence across sessions**. Each maintains markdown-based project state files (STATE.md, PROJECT.md, ROADMAP.md, etc.) so work survives session boundaries and context can be restored.

**Anti-enterprise, pro-solo-builder ethos**. All three explicitly reject heavyweight project management (sprint ceremonies, Jira, story points) in favor of lightweight workflows designed for solo developers or small teams using AI to punch above their weight.

**"Claude Code is powerful, but needs structure to be reliable"** is essentially the shared thesis.

#### Version 2

They are all context engineering and workflow orchestration systems for 
AI coding agents [primarily targeting Claude Code?]. They share:

- The same core problem: context rot / quality degradation as the AI's context window fills up, leading to unreliable output at scale.
- Spec-driven, phased execution loops: plan → execute → verify/reconcile. GSD uses "plan-phase / execute-phase / verify-work," PAUL uses "Plan-Apply-Unify," Ultrawork uses "Prometheus → Atlas → verified result." All require defining acceptance criteria upfront before any code gets written.
- Multi-agent orchestration: specialized subagents for research, planning, execution, and verification — keeping individual context windows fresh rather than overloading a single session.
- Markdown-based state persistence: PROJECT.md, STATE.md, ROADMAP.md, PLAN.md, SUMMARY.md files that survive session boundaries, so work can be resumed and context restored.
- Anti-enterprise, pro-solo-builder ethos: all three explicitly reject heavyweight project management (sprint ceremonies, story points, Jira) in favor of lightweight workflows for solo developers or small teams.
- XML-structured task formats with verification steps baked into each task (files, action, verify, done criteria).
- Atomic git commits per task for traceability and rollback.

They have somewhat different philosophical emphasis. 
GSD leans heavily into parallel subagent execution for speed; 
PAUL argues subagents produce ~70% quality work and prefers keeping implementation in-session; 
Ultrawork pushes furthest toward full autonomy with the thesis that any human intervention is a system failure.

### Specific Reviews

1. **[GSD Framework Review](../../sandbox/sdlc/gsd-review.md)**: A detailed review of the GSD (Get Shit Done) framework: what it does well (12 strengths worth preserving), documented gaps (2 fully analyzed), and additional gaps identified but not yet fully documented (12 to-do items).

2. [TBD: Paul https://github.com/christopherkahler/paul  (has acceptance driven development) Need to install and inspect it]

3. [TBD: https://ulw.dev/  (has manifesto)   Need to install and inspect it]

## Additional ideas (which go beyond the above frameworks) [TBD)

### Semantic retrieval of prior decisions

When a subagent is given authority to make decisions on-the-fly that are required for translating parts of the TSD
to actual code, it's important to make sure that its decisions don't contradict decisions of other agents,
or even prior decisions of the agent itself. A common method in the above frameworks for providing this
is to have a markdown file that captures previous decisions. However, this is a very primitive store.
In contrast, in a human brain, and in a human team, only relevant prior decisions are retrieved from personal memoery
and organizational memory through association (the excellent retrieval mechanism in the brain).
But we can develop simple tools such as keeping the decisions not in a simple md file but in a DB
where each piece is indexed e.g. by keywords, topics, and even embeddings.
Then, the key is computed for a new proposed decision, and only relevant decisions are retrieved.
For a small project, md is enough, but as projects become larger, a dedicated store, indexing, and retrieval is needed.

### DB for tasks, instead of markdown

A similar idea for handling all the tasks, their status, their content. 
Instead of a hard-to-read table in a markdown file.

### Design Principle of automatic SDLC: Converting some of the markdown instructions to code

Running an LLM each time is

1. costly
2. not necessarly deterministic

It's tempting to write everything in English and rely on the LLM to execute,
but converting part of the process to structured code that does it is better.

1. more reliable
2. costs less
3. Not using LLMs for what can be implemented in code, 
   and using LLMs for what cannot be implemented in ocde easily or at all, for what LLMs are good at: 
   higher level reasoning and generation.

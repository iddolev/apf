---
date: 2026-03-06
author: Iddo Lev
LLM-co-author: claude-Opus-4.6
---

# Claude Preparation

This is a markdown file that instructs an LLM how to create agent definition files, skills,
and other knowledge files,
to be used by agentic programming platforms (such as Claude Code and OpenCode) for the current
project.

## Instantiation Instructions

In all the files mentioned below:

1. You need to instantiate them according to the instructions in the `<!-- ADAPT: ...->` tags.
2. After that, remove all `<!-- ADAPT -->` markers from the output.
3. Keep all non-ADAPT sections unchanged.

## Creating Knowledge Files

1. Instantiate the file @CLAUDE.template.md according to the instructions in it
   Put the result file CLAUDE.md under the project's root folder
   Mark the CLAUDE.md checkbox as `[v]` in the latest `.apf/STATE-v*.md`.

## Agents - Our General Approach

<!-- Instruction for the agent: do NOT read rationale.md — it is only for the human user. -->

> **NOTE:** The rationale for this approach is explained in `docs/rationale.md` in the
agentic-programming project,
> section "Why Agent Templates Use a General-Then-Specific Approach".

We have a general template for each agent (under the folder instructions/.claude/agent-templates),
plus general instructions (in this file) explaining how to adapt the template to the specific
project,
by creating a specific agent tailor-made for this project.

### IMPORTANT NOTE

Whenever starting a new version of an existing project, there is a new set of spec docs.
Therefore, it is necessary to review the agent definitions to make sure they are adapted to be
useful
for the new specs and don't remain stuck with capabilities that are not good enough for the new
version.

## Creating Agent Files

1. Instantiate the file @agent-templates/tech-lead.template.md according to the instructions in it.
   It must be instantiated in ALL projects.
   Put the result file tech-lead.md under the folder <project_root>/.claude/agents/
   Mark the tech-lead agent checkbox as `[v]` in the latest `.apf/STATE-v*.md`.
2. For each agent template file <X>.template.md in the folder agent-templates, decide
   whether it is required for the project.
   If yes, then instantiate it according to the instructions in it,
   and put the result file <X>.md under the folder <project_root>/.claude/agents/
3. Finally, given all the agents you created in <project_root>/.claude/agents/,
   instantiate the file @AGENTS-LIST.template.md according to the instructions in it.
   Put the result file @AGENTS-LIST.md under folder <project_root>/.claude/knowledge/

## Finalize

Mark the AGENTS-LIST.md checkbox as `[v]` in the latest `.apf/STATE-v*.md`.

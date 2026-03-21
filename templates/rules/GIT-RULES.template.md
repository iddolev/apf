---
date: 2026-03-06
author: Iddo Lev
LLM-author: claude-Opus-4.6
---

# Git Rules

## Purpose

This document defines the git workflow and permissions for all agents and human users on this project.
Git operations are high-risk (pushing bad code, rewriting history, breaking main) and hard to reverse.
These rules exist to prevent damage while allowing agents to be productive.

## Commit Message Format

<!-- ADAPT: Define the commit message format for this project.
     Examples:

     - Conventional Commits: "feat(auth): add OTP-based account recovery"
     - Simple prefix: "fix: resolve race condition in worker queue"
     - Ticket-based: "PROJ-123: implement rate limiting on /api/v1/search"

-->

[TBD]

## Branch Naming Convention

<!-- ADAPT: Define the branch naming convention for this project.
     Examples:

     - "feat/short-description", "fix/short-description", "chore/short-description"
     - "PROJ-123/short-description"

-->

[TBD]

## Push Policy

Only the human user pushes to the remote repository. 
No agent is allowed to push to the remote git repo under any circumstances.

Later you may decide to relax this rule for specific agents 
if they have demonstrated consistent high quality.
In such a case, document the exceptions here with the agent name and any conditions.

## Agent Git Permissions

### Agents that MUST use the branch workflow

Agents that produce code or documentation as their primary output must adhere to these rules.
Before making any file changes, they must:

1. Create a new branch from the current branch: `git checkout -b <branch-name>`
2. Make their changes on the new branch
3. Commit their work to the branch using the commit message format above
4. Report back to the tech-lead or human user — never merge the branch themselves!

This section applies to the following agents:

<!-- ADAPT: List the agents that follow this workflow. Typical agents:

     - backend-specialist
     - frontend-specialist
     - test-specialist
     - documentation-specialist

-->

- [TBD]

### Agents that MUST NOT use git

Agents that review, analyze, or plan but do not produce files must not run any git commands:

<!-- ADAPT: List the agents that must not use git. Typical agents:

     - tech-lead (orchestrates, never writes code)
     - security-specialist (reviews, does not produce code)
     - system-architect (plans, does not produce code)
     - code-reviewer (reviews; if it fixes issues, it should be re-routed through a coding agent)

-->

- [TBD]

## EXTREMELY CRITICAL: Prohibited Git Operations by Agents

No agent is ever allowed the following:

- Push to the remote repository (reserved for the human user only)
- Force-push (`git push --force`)
- Commit directly to main or the primary development branch
- Amend commits (`git commit --amend`)
- Rebase or rewrite history (`git rebase`, `git reset --hard`)
- Delete branches (`git branch -d/-D`)
- Merge branches (`git merge`) — merging is reserved for the human user

## Merge Policy

All merges to the main branch MUST first go through a merge request in GitLab, reviewed by at least one human.

TODO: Enforce this rule in the remote git repo using a rule there that protects the main branch.

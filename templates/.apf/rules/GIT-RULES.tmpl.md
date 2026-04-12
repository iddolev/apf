---
last_update: 2026-03-06
author: Iddo Lev
LLM-co-author: claude-Opus-4.6
---

# Git Rules

## Purpose

This document defines the git workflow and permissions for all agents and human users in this project.
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

## Protection of the `main` branch

Upon creation of a new project in the git platform (GitHub, GitLab, etc.),
the human user must manually set these rules on the platform: 

<!-- ADAPT: Ask the user for specific changes they may want for these rules -->

1. Pushing directly into the `main` branch is always prohibited 
   - for both agents and human users.
2. All changes to the `main` branch must first go through a 
   Merge Request (on GitLab) or Pull Request (on GitHub and BitBucket),
   which must be reviewed and approved by at least one human user as a pre-condition 
   for merging with the `main` branch. 
3. Automatic tests must be created whenever feasible, and failing tests on a branch 
   must block merging the branch to the `main` branch.
4. An agent is never allowed to approve a merge/pull request and merge the branch 
   to the `main` branch. All such merges must be done manually by a human user.

## Agents that MUST NOT use git

Agents that review, analyze, or plan but do not produce files must not run any git commands:

<!-- ADAPT: List the agents that must not use git. Typical agents:

     - apf-tech-lead (orchestrates, never writes code)
     - apf-security-specialist (reviews, does not produce code)
     - system-architect (plans, does not produce code)
     - apf-code-reviewer (reviews; while fixes should be re-routed through a coding agent)
-->

- [TBD]

## Agents that MUST use the branch workflow

Agents that produce or modify code or documentation as their primary output 
must adhere to these rules. Before making any file changes, they must:

1. Check whether the current branch is the `main` branch. If it is, 
   then create a new branch from the `main` branch: `git checkout -b <branch-name>`
2. Make their changes only on the new branch, and never on the `main` branch
3. Commit their work to the branch using the commit message format above
4. Report back to the apf-tech-lead agent or human user to say what was done 
   and ask for permission to push the branch to the remote repository.
5. After a new branch's first push to the remote repository, 
   the agent must also create a Merge/Pull Request 
   (e.g. for GitHub by using the `gh` program), 
   and display the resulting Merge/Pull Request URL so the human user
   can review the changes. If a Merge/Pull Request already exists for the branch,
   it will be updated automatically by the push to the remote repo.

This section applies to the following agents:

<!-- ADAPT: List the agents that follow this workflow. Typical agents:

     - apf-backend-specialist
     - apf-frontend-specialist
     - apf-test-specialist
     - documentation-specialist
-->

- [TBD]

## Push Policy

Agents must never push to the remote repository without first 
asking for permission from the human user.

Later you may decide to relax this rule for specific agents 
if they have demonstrated consistent high quality.
(In such a case, document the exceptions here with the agent name and any conditions.)

## EXTREMELY CRITICAL: Prohibited Git Operations by Agents

No agent is ever allowed the following:

- Push to the remote repository without first asking for permission
- Force-push (`git push --force`)
- Commit directly to `main` or the primary development branch
- Amend commits (`git commit --amend`)
- Rebase or rewrite history (`git rebase`, `git reset --hard`)
- Delete branches (`git branch -d/-D`)
- Merge branches (`git merge`) — merging is reserved for the human user

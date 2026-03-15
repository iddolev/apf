---
name: gitlab-agent-templates
description: Use when creating new Claude Code agents, scaffolding agent configurations, or when the user asks to use a
shared team template for agents. Also use when listing available agent templates from the company GitLab repo.
---

# GitLab Agent Templates

## Overview

Fetches agent templates from the company's private GitLab repo and applies them to the current project. Templates live
in `agent-templates/` within the `agentic-programming` repository.

## When to Use

- User wants to create a new agent from a team template
- User says "use a template", "shared agents", "team templates"
- Setting up `.claude/agents/` in a new project
- Listing what agent templates are available

## When NOT to Use

- User is writing a brand-new agent from scratch (no template)
- Working with a different repo's agents

## Setup

Requires a `GITLAB_TOKEN` environment variable with read access to the repo.

If not set, tell the user:
> You need a GitLab personal access token with `read_api` scope.
> Set it as `GITLAB_TOKEN` in your environment or `.env` file.

## GitLab API Reference

**Project path (URL-encoded):** `claude-code-experiments%2Fagentic-programming`

### List available templates

```bash
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/claude-code-experiments%2Fagentic-programming/repository/tree?path=agent-templates&ref=main"
```

Parse the JSON array — each entry has `name`, `path`, `type` (file or directory).

### Fetch a specific template

```bash
# URL-encode the file path: agent-templates/my-template.md → agent-templates%2Fmy-template.md
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/claude-code-experiments%2Fagentic-programming/repository/files/agent-templates%2F<filename>/raw?ref=main"
```

## Workflow

1. **Check `GITLAB_TOKEN`** — abort with setup instructions if missing
2. **List templates** — call the tree endpoint, show user the available names
3. **User picks** — they choose which template(s) to use
4. **Fetch content** — download the raw file(s) via the files endpoint
5. **Write to project** — copy to `.claude/agents/` in the current project
6. **Customize** — ask user if they want to modify the template for their needs

## Common Mistakes

- Forgetting to URL-encode the path (`/` → `%2F`) when fetching files
- Not checking if `.claude/agents/` exists before writing
- Using `master` instead of `main` as the ref — verify the default branch

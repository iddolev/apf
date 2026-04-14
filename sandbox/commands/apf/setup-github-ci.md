---
source: Agentic Programming Framework: https://github.com/iddolev/apf
author: Iddo Lev
description: Offers to set up CI/CD with test gating and branch protection.
comment: Currently supports only GitHub. TODO: Support also GitLab and others.
last_update: 2026-03-18
---

## Step 1 — Detect

Run the detection script:

```
python .claude/apf/scripts/setup_github_ci.py --detect
```

Parse the JSON output.

- If `"error": "not_github"`, show the message to the user and STOP.
- If `"gh_installed"` is `false`, tell the user that the GitHub CLI (`gh`) is required for branch
  protection setup. Ask if they'd like you to install it (e.g. via `winget install GitHub.cli`,
  `brew install gh`, or `sudo apt install gh` depending on the platform). If they decline, explain
  that you can still create the workflow file but cannot configure branch protection, and ask if
  they'd like to proceed with just the workflow. If they decline that too, STOP.
- If `"error": "no_test_setup"`, ask the user what command runs their tests and what runtime they
  use, then proceed manually.

## Step 2 — Confirm with user

Using the detected info from the JSON output, confirm with the user:

> I detected the GitHub repository **{owner}/{repo}** (main branch: **{main_branch}**).
> Test setup: **{runtime_name}** with `{test_cmd}`.
>
> I can set up:
>
> 1. **GitHub Actions workflow** — runs tests on every PR targeting {main_branch}
> 2. **Branch protection** — requires tests to pass before merging
> 3. **Require PR reviews** — at least 1 approving review (admin bypass enabled)
>
> Shall I proceed?

Wait for the user to confirm. If they want to customize, adjust accordingly.

## Step 3 — Write workflow file

```
python .claude/apf/scripts/setup_github_ci.py --write-workflow
```

## Step 4 — Set branch protection

```
python .claude/apf/scripts/setup_github_ci.py --protect
```

## Step 5 — Commit and push

Ask the user if they want you to commit and push the workflow file. If yes:

1. Commit `.github/workflows/tests.yml` with a descriptive message.
2. Push to the current branch.

## Step 6 — Summary

Tell the user what was set up:

- Tests run automatically on every PR targeting the main branch.
- PRs require at least 1 approving review to merge (admins can bypass).
- The branch must be up-to-date with the main branch before merging.
- Direct pushes to the main branch are blocked for non-admins.

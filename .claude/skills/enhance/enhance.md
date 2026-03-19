---
source: Agentic Programming Framework: https://github.com/iddolev/apf
author: Iddo Lev
description: >
  Check frameworks that APF draws inspiration from for updates,
  review changes, and suggest APF enhancements.
  Optional argument: a framework name, --check-all, or --list.
last_update: 2026-03-19
allowed-tools: Bash(python *), Bash(git *), Read, Glob, Grep
---

# Enhance APF from Framework Updates

This skill checks frameworks tracked in `enhance.yaml` for updates,
reviews changes, and suggests how to enhance APF based on what's new.

## How to Run

1. **Check all frameworks for updates (quick version check):**

```bash
python .claude/skills/enhance/enhance.py --check-all
```

2. **List all tracked frameworks:**

```bash
python .claude/skills/enhance/enhance.py --list
```

3. **Review a specific framework** (argument from `$ARGUMENTS`, or pick from the list):

```bash
python .claude/skills/enhance/enhance.py <framework_name>
```

## Workflow

### Step 1 — Determine what to check

- If `$ARGUMENTS` is a specific framework name, check only that one.
- If `$ARGUMENTS` is `--check-all` or empty, first run `--check-all` to see which
  frameworks have updates, then process each one that needs review.

### Step 2 — Run the script

Run `enhance.py` for each framework that needs review. The script will:

- **First-time review** (no `processed_version`): Clone the full repo and output
  all key files and commit history for comprehensive review.
- **Incremental update** (version changed): Clone and show only the diff between
  the old and new versions — commits, changed files, and full diff.
- **Up to date**: Report that no changes are needed.

### Step 3 — Review and analyze

For each framework with changes, review the script output and:

1. **Summarize** what changed in the framework (new features, methodology changes,
   structural changes, new commands/agents).
2. **Compare to APF**: Read relevant APF files to understand the current state.
   Use Glob and Read to inspect APF's templates, commands, and docs as needed.
3. **Suggest enhancements**: Propose specific, actionable improvements to APF
   inspired by the framework's changes. Focus on:
   - New ideas APF doesn't have yet
   - Better approaches to things APF already does
   - Structural or organizational improvements
   - New commands, agents, or templates worth adding

### Step 4 — Update processed version

After the user confirms the review is complete, update the version:

```bash
python .claude/skills/enhance/enhance.py --set-version <framework_name> <version>
```

## Important Notes

- Do NOT update `processed_version` automatically — wait for user confirmation.
- The `sources` section in `enhance.yaml` lists additional reference URLs
  (comparisons, blog posts). Fetch and review these too when doing a first-time review.
- When suggesting APF enhancements, be specific: name the file to change, the section
  to add, or the template to create. Don't just say "consider adding X".

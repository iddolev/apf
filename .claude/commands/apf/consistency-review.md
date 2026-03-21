---
source: Agentic Programming Framework: https://github.com/iddolev/apf
author: Iddo Lev
description: |
  Review all tracked project files for stale content and inconsistencies.
  For each issue found, propose a fix and apply it if the user approves.
last_update: 2026-03-21
allowed-tools: Bash(git ls-files), Read, Glob, Grep, Edit, Write
---

# Project Consistency Review

Systematically review all tracked project files for stale content and
inconsistencies. For each issue found, propose a fix and — if the user
approves — apply it.

## Step 1 — Collect the file list

Run:

```bash
git ls-files
```

From the output, exclude any paths that start with `sandbox/`.
These are the files to review.

## Step 2 — Build context

Before searching for issues, orient yourself:

- Read `README.md` (or equivalent top-level doc) to understand the project's
  stated structure, intent, and conventions.
- Read `CLAUDE.md` for project-specific rules and constraints.
- Use Glob to inspect the actual top-level directory and file layout.

## Step 3 — Systematic consistency checks

Work through each category below. For every issue you find, record:

- **File** (and line number if applicable)
- **Category** (from the list below)
- **What's wrong**
- **Proposed fix**

### A. Structure documentation vs reality

Identify every place that describes the folder or file layout — e.g. a
"Structure", "Organization", or "Folders" section in a README or other doc.

For each such description, compare it against what actually exists on disk.
Flag:

- Folders or files described but not present on disk
- Present folders or files that are omitted from the description (if they
  seem significant enough to warrant mention)
- Wrong paths, wrong names, or wrong descriptions

### B. Internal cross-references and links

Search all markdown files for relative file paths and internal links
(e.g. `[text](path)`, `path/to/file` in backticks).

For each reference, verify the target exists on disk. Flag broken links and
stale path references.

### C. Code vs documentation alignment

For each code file (`*.py`, `*.bat`, etc.), check whether:

- The module's documentation text accurately describes what the file does, including
  correct file paths, argument counts, and behavior
- Inline comments reference the correct names, paths, or behavior
- The `Usage:` example in the documentation (if present) matches the actual interface

Cross-reference with the actual code logic.

### D. Frontmatter consistency

For files with YAML frontmatter (commands, skills, agents):

- Check that `description` exists and accurately reflects what the file actually does
- Check (if applicable) that `allowed-tools` exists and includes the tools that are
  actually used in the file and doesn't list tools that aren't needed

### E. Repeated or conflicting definitions

Look for the same concept (constant value, file path, process description,
terminology) defined or described differently in two or more places. Flag any
conflicts.

### F. Typos and Styling

Read all prose text in markdown files, docstrings, and comments and flag
spelling mistakes and obvious grammatical errors. Also flag text styling issues. 
Focus on human-readable text, not code identifiers or technical terms.

### G. TODOs, TBDs, and known gaps

Search for `TODO`, `TBD`, `FIXME`, `[TBD`, and similar markers in all files.
List them — these are not necessarily bugs, but they should be surfaced so
the developer is reminded of them.

## Step 4 — Present findings

After completing all checks, present findings as a numbered list, grouped by
severity:

- **Inconsistency** — factually wrong (e.g. a path that doesn't exist, a
  docstring that describes the wrong behavior)
- **Stale** — was correct but is now outdated (e.g. a structure description
  that no longer matches the current layout)
- **FYI** — not wrong, but worth knowing (TODOs, minor wording issues)

Format each finding as:

```
Issue #N — [Severity] [Category] — [File:line]
Problem: <description of what's wrong>
Fix: <description of proposed change>
```

## Step 5 — Fix loop

Go through each Inconsistency and Stale issue (skip FYIs unless the user
asks to address them):

1. Show the exact change you would make (before/after diff when applicable).
2. Ask the user: **"Apply this fix? [y/n]"**
3. If yes, apply the fix immediately using Edit or Write, then confirm.
4. Move to the next issue.

If the user says "fix all" or "yes to all", apply all remaining fixes without
asking for individual confirmations.

After all fixes are applied (or skipped), print a brief summary:
how many issues were found, how many were fixed, and how many were skipped.

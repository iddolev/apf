# General Knowledge

## GitHub

### Merge to `main` only through a Pull Request, prevent direct push

In GitHub, go to **Settings → Branches → Add branch ruleset** (or "Add classic branch protection
rule"):

1. Set the branch name pattern to `main`.
2. Enable **"Require a pull request before merging"**.
3. Verify **"Allow force pushes"** is disabled.
4. Save the rule.

Direct pushes to `main` will now be rejected; all changes must go through a PR.

### Automatically delete a PR's branch after merging

In GitHub, go to **Settings → General**, scroll to the **Pull Requests** section, and enable
**"Automatically delete head branches"**.

After a PR is merged, GitHub will automatically delete the source branch.

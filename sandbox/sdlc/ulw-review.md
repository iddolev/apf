---
author: Iddo Lev
LLM_author: Claude Opus 4.6
last_updated: 2026-03-14
---

# UltraWork (Oh My OpenCode) Framework Review — Strengths and Gaps

## To do

### No out-of-the-box support of virtual environment

Need to setup manually

### No out-of-the-box support for git branches, code review

"before we continue, I want to ask you: I see you added files. Does ulw support creating a git branch with a unique name for every phase? Does ulw support pushing to the GitHub repo and creating a Pull Request there?"

```
I'm not certain if ultrawork automatically handles git branch creation per phase or creates GitHub PRs. Let me check the git-master skill and documentation for you:

Based on what I know:

Git Branch per Phase: Not automatically. The git-master skill handles atomic commits and rebase surgery, but creating unique branches for each phase would likely need to be configured manually or requested from the Sisyphus agent.

Push & PR: The gh CLI is available in the environment. The agent can run gh pr create commands, but it's not automatic - you'd need to explicitly ask for it.

My recommendation: When we continue with ultrawork, you can tell the agent:

"Create a new branch for this feature"
"Push to GitHub and create a PR when done"
Would you like me to start ultrawork now to build the LLM integration, and we can handle the git/PR workflow as we go?
```
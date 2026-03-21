# General Things

## Automatic cleaning of merged branches

### Clean process

The clean process for making updates to the remote repo's main branch is:

1. Never push directly to the main branch. Instead, all modifications must pass through a merge request (on GitHub they are confusingly called "pull request"). 
2. Once a branch is merged to the main branch, it should be deleted from the remote repo
3. Locally on your machine, a script should allow you to prune "stale" branches 
   that were deleted in the remote branch but still exist on your local machine. 

The following steps and tools implement these requirements.

### Prevent direct pushes to the main branch

1. Go to your repo on GitHub
2. Settings > Branches
3. Click Add branch ruleset (or Add rule under Branch protection rules if you see the classic UI)
4. Set it to target main
5. Enable Require a pull request before merging
6. Optionally enable Require approvals (set to 1+ if you want someone else to approve)
7. Save  

This blocks direct pushes to main — all changes must go through a PR. 
If you're the only contributor and don't need approval from others, you can leave "Require approvals" at 0 
but still keep the PR requirement.

### Automatic deletion of a branch after mering it to the main branch

1. Go to your repo on GitHub                                                                                     
2. Settings > General
3. Scroll down to Pull Requests section 
4. Check "Automatically delete head branches"

###

(would fetch clear the stale branches? or need the script?)
# Grounded Commits: landing

Format version 0.5.0. This part is optional: the commit and pull-request conventions work under any merge method. What is not optional is knowing what your method does to the commits, because they are the record.

## What landing preserves

1. **The reviewed commits land as reviewed**: same hashes, trees, messages and signatures. A method that replays them as new objects (a rebase, a squash) leaves `Verified:` lines describing trees that may never have been tested, and drops every author signature.
2. **The landed tree was checked.** When the branch is behind the target, the merged tree is one no branch commit was checked on. Check it before it lands, or let the forge check exactly the object that lands.
3. **Nothing from the pull-request body enters history.**
4. **Issues close by hand after landing**, never by keyword.

## Two cases

**The branch is current**, meaning the target's tip is an ancestor of the head. Fast-forward the target to the head wherever the forge allows it: Forgejo's fast-forward-only style, GitLab's fast-forward method, a plain `git merge --ff-only`. The head's own checks cover what lands. GitHub has no fast-forward button; its merge commit of a current branch has the head's tree, so the same holds, and the merge commit may carry the pull request's URL under `Refs:`.

**The branch is behind.** Either bring it current by merging the target into it, after which the forge re-runs the checks and it is the first case; or build the merge commit yourself on the target's tip, run the checks on it, give it a `Verified:` line for what ran, and land exactly that commit. Never rebase the branch to catch up: it rewrites what was reviewed. On a busy target, GitHub's merge queue and GitLab's merge trains do this automatically and land what they checked.

**Squash**, where a repository wants one commit per pull request: compose the landed message in the commit format from the branch's commits and supply it to the forge explicitly. Never the forge's default, and never the pull-request body.

## Per forge

| Forge | Settings | Landing |
|---|---|---|
| **GitHub** | Merge commits on, rebase merging off, "Require linear history" off, the merge message the pull-request title only (never the description). Require a pull request and the status checks, with "Require branches to be up to date before merging", or a merge queue on a busy target. | `gh pr merge <n> --merge --match-head-commit <head>`, or `--auto` with a queue. GitHub's "Rebase and merge" always creates new commits, even when a fast-forward would do; leave it off. Read the landed commit back afterwards. |
| **Forgejo** | Merge style fast-forward-only allowed and default; update style merge. Branch protection: no direct push, or only the landing identity; required status contexts and approvals. | Land with `Do: fast-forward-only` and `head_commit_id: <head>`. The forge refuses a branch that is behind: merge the target into the branch, let the checks run, land again. For a fork you cannot push to, land its head through a merge commit on a maintainer-owned branch, or squash. |
| **GitLab** | Merge method fast-forward, automatic rebase off, squash "Do not allow", "Pipelines must succeed"; or merge commits with merged-results pipelines and merge trains on a busy licensed project. | `PUT …/merge` with `sha: <head>`; GitLab refuses unless the target is an ancestor. With trains, add with `auto_merge`, never "merge immediately". |
| **Plain Git** | | `git merge --ff-only <head>` when current; otherwise `git merge --no-ff --no-commit <head>`, run the checks, commit with a `Verified:` line, push. A refused push means the target moved: rebuild from its new tip. |

Enable only the method your repository uses, so an agent cannot pick another. Whenever the forge writes the landing commit, read its message back and confirm the approved head is an ancestor of the target's tip.

## Pull requests from forks

A fork's commits may not follow the format, and you may not be able to push to its branch. Record one route in your guidance: land the commits as written through a merge commit on a maintainer-owned branch; squash with a message composed in the format; or ask the contributor to fold and reword.

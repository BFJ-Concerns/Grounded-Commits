# Grounded Commits: landing a branch

Format version 0.1.0. This part is optional: the commit and pull-request conventions work under any merge method. What is not optional is knowing what your method does to the commit messages, because they are the record. This document says what each method does and how to keep the record intact under it.

## What landing has to preserve

1. **The record.** Under fast-forward, rebase and merge commits, each commit's message lands as written, or as deliberately reworded before landing. Under squash, the branch's messages are replaced by one message composed from them; the composition is deliberate, never the forge's default.
2. **Nothing from the pull-request body enters history.** The body is a review brief.
3. **What lands is what was reviewed.** The landing comment carries the reviewed head, `git diff <reviewed-head> HEAD` and `git range-diff` (`pull-requests.md`, *Before landing*).
4. **Issues close by hand after landing**, never by keyword.

Whenever a method rewrites commits, read the landed messages back (`git log --format=%B <range>`) and compare them with what was pushed.

## Choosing a method

The default is **rebase**: a linear history in which every commit keeps its own message. Fast-forward is the same shape with the hashes kept too, and is preferred where the forge offers it. Merge commits and squashes are supported with the configuration below. Enable only the method your repository uses, so an agent cannot pick another.

| Method | What happens to the commits | Configure | Watch for |
|---|---|---|---|
| **Fast-forward** | Land unchanged: same hashes, same signatures. | GitLab: merge method *Fast-forward merge*, squash *Do not allow*. Forgejo and Gitea: merge style *Fast-forward only*. Plain Git: `git merge --ff-only`. GitHub has no button; see below. | The branch must already sit on the target's tip, so rebase and re-check before landing. |
| **Rebase** (default) | Replayed onto the target by the forge as new commits with the same messages. New hashes; committer updated; signatures not carried; on GitHub, originally empty commits dropped. | GitHub: *Rebase and merge*. GitLab: *Fast-forward merge* with squash not allowed, rebasing from the UI when needed. Forgejo and Gitea: *Rebase*, with no `REBASE_TEMPLATE.md`, or one that keeps `${CommitTitle}` and `${CommitBody}` and omits the description. | A `Verified:` line that names a branch commit by hash still names what was tested; it need not stay reachable. The source branch is not an ancestor of the target afterwards, so delete it on merge. |
| **Merge commit** | Land unchanged, plus a merge commit. | Set the merge message to the pull-request title only: GitHub *Default to pull request title*; Forgejo and Gitea `MERGE_TEMPLATE.md` without `${PullRequestDescription}`; GitLab merge commit template `%{title}`. | A merge message that includes the description puts the brief into history. |
| **Squash** | Replaced by one new commit. | The landing agent composes the squash message in the commit format from the branch's commits (problem, approach, `Considered and rejected:`, limits, `Not done:`, evidence rebound to the landed tree) and supplies it explicitly: GitHub API `commit_title` and `commit_message`, or the repository's squash-message setting; GitLab `squash_commit_message`; Forgejo's and Gitea's merge title and message fields. Never the forge's default. | Read the landed message back with `git show -s --format=%B` and `git interpret-trailers --parse --no-divider`. Each commit's own account is gone; only the composed one remains. |

### Fast-forward on GitHub

GitHub's *Rebase and merge* "always updates the committer information and creates new commit SHAs", and the merge queue only merges, rebases or squashes. To land the hashes unchanged, push the approved, rebased tip to the target yourself: `git push origin <tip>:main`. GitHub then marks the pull request merged, because its head commits have become reachable from the base. Whether the push is allowed depends on the protection in force: required status checks permit a direct push of a commit whose checks passed; required reviews and push restrictions permit it only to an identity they allow. Where the push goes around a protection, the landing step is doing that protection's job, so confirm approval and passing checks on that exact tip before pushing, or use *Rebase and merge* instead.

## Pull requests from forks

A fork's commits may not follow the format, and a rebase or squash rewrites them anyway. Pick one route and record it in guidance:

- **Rebase** the fork's commits as written when their messages are acceptable.
- **Squash** with a message composed in the format when they are not. This is the usual route for drive-by contributions.
- **Reword on the contributor's branch** when they allow edits from maintainers (GitHub permits this on user-owned forks) and the forge will then fast-forward or rebase.

## Settings worth setting

- Default merge message: pull-request title only, never the description.
- Squash: disabled unless squash is the chosen method.
- Delete head branches on merge.
- Review bots that write summaries into the description: comment mode.
- Agent tools: point their guidance at `pull-requests.md` so the shipped template is replaced.

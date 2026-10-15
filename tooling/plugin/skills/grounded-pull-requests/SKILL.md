---
name: grounded-pull-requests
description: Write and maintain a pull request's title and body as a review brief in the Grounded Commits convention. Use when opening, describing, retitling or updating a pull request, commenting on a push during review, or preparing an approved branch to land, in a repository that has adopted Grounded Commits, and when asked to write a grounded PR description. The commit messages themselves are grounded-commits.
---

# Grounded Pull Requests

The commits are the record. The pull-request body is a short brief for
whoever is reviewing now, person or bot, and nothing in it needs to survive
the merge.

A repository adopts this convention together with the commit format: its
agent guidance says it follows Grounded Commits, or it has a
`.grounded-commits.toml` or the Grounded Commits `commit-msg` hook. There it
replaces the pull-request template your tool ships with; elsewhere, write a
grounded pull request only when asked to. A user's explicit instruction about
a particular pull request overrides this skill. The subject grammar this
skill refers to is the grounded-commits skill's (`../grounded-commits/SKILL.md`,
relative to this skill's directory).

## Title

The outcome of the whole branch, in the same `area: outcome` shape as a
commit subject (or `type(area): outcome` under the typed profile). For a
one-commit pull request, that commit's subject. Draft state is the forge's
own mechanism, a draft flag or a `WIP:` prefix where the forge uses one, not
a word of your own in the title.

## Body

A lead of a sentence or two: the problem or request, what the branch does
about it, and a plain link to the issue if there is one. Then any of these
sections that have something to say, and none that do not:

- **`### Read`**: for several commits, or a diff whose shape is not obvious,
  which commits prepare and which change behaviour, and where to start.
- **`### Check`**: what to look at hard; a gap or break a commit records,
  named by that commit's subject; a question for the reviewer and what turns
  on it.
- **`### Try`**: how to see the change work, and what each step should show.
  A screenshot says what environment and state it shows.
- **`### Not in this PR`**: what was asked for or would be expected and is
  deliberately absent, each with where it is tracked, or "not planned".

Keep it short: a one-commit pull request usually needs the lead and nothing
else. Write each paragraph on one line, since GitHub renders a single newline
as a line break. Essential facts go in visible prose, not in HTML comments,
collapsed blocks or images.

## Never in the body

- A copy of a commit's reasoning or trailers, a list of files, or narration
  of the diff.
- A result or an assurance: "all tests pass", "verified locally", "safe".
  What ran is on the commits.
- Checklists. A tick is not evidence, and some bots treat a ticked box as a
  command.
- Instructions to automated reviewers, or a claim that a reviewer agreed.
- A commit hash or CI link as a pointer to the current head, which the next
  push replaces. Name commits by subject.
- A closing keyword before an issue reference. Link plainly; close by hand
  after landing.
- The machinery behind the change: plan steps, task codes, session paths, and
  the tool, review round or model that made or found it.

## During review

- The body describes the current branch. After a push, fix whatever is no
  longer true and remove settled questions, rather than appending updates.
- Say what each push changed, in a comment or in the threads, and answer a
  declined finding where it was raised. A reason that matters later goes into
  the relevant commit's `Considered and rejected:` before landing.
- Push fix-up commits during a round rather than force-pushing, so reviewers
  see what changed. If the repository wants a tidy history, fold them before
  the final approval, make sure each folded commit's `Verified:` lines are
  still true of it (the grounded-commits skill, *After a rebase*), check the
  result with the checker's `--range`, say in a comment that the branch was
  folded, and attach a `git range-diff` where content moved. After that
  approval the branch is not rewritten again; a late finding is a new commit.
- Bring a stale branch current by merging the target into it, not by
  rebasing: a rebase replaces every commit the reviewers have read.
- Editing the body does not re-run checks or wake review bots. When an edit
  changes something a reviewer relied on, ask for review again.

## Landing

Ready to land means no open question in the body, `Not in this PR` current,
every commit message true of its contents, the forge not showing draft
state, and the required approvals and checks present on what will land.
Where the repository follows the landing guidance, read
`references/landing.md` (relative to this skill's directory) for the method
on each forge: fast-forward a current branch, build and check a merge for one
that is behind, and never rebase reviewed commits. A repository with its own
landing policy keeps it. After landing, confirm the approved head is an
ancestor of the target's tip, then close each delivered issue by hand with a
comment naming the landed commit.

## Examples

Read `references/examples.md` for a one-commit body with no issue and a
four-commit series with one outcome.

# Grounded Commits: pull requests

Format version 0.5.0. Paste this file, or the parts you need, into your repository's guidance for agents. It replaces the pull-request template your tool ships with. It goes with `commit-messages.md`; `landing.md` is optional.

The commits are the record. The pull-request body is a short brief for whoever is reviewing now, person or bot, and nothing in it needs to survive the merge.

## Title

The outcome of the whole branch, in the same `area: outcome` shape as a commit subject (or `type(area): outcome` under the typed profile). For a one-commit pull request, that commit's subject. Draft state is the forge's own mechanism, a draft flag or a `WIP:` prefix where the forge uses one, not a word of your own in the title.

## Body

A lead of a sentence or two: the problem or request, what the branch does about it, and a plain link to the issue if there is one. Then any of these sections that have something to say, and none that do not:

- **`### Read`**: for several commits, or a diff whose shape is not obvious, which commits prepare and which change behaviour, and where to start.
- **`### Check`**: what to look at hard; a gap or break a commit records, named by that commit's subject; a question for the reviewer and what turns on it.
- **`### Try`**: how to see the change work, and what each step should show. A screenshot says what environment and state it shows.
- **`### Not in this PR`**: what was asked for or would be expected and is deliberately absent, each with where it is tracked, or "not planned".

Keep it short: a one-commit pull request usually needs the lead and nothing else. Write each paragraph on one line, since GitHub renders a single newline as a line break. Essential facts go in visible prose, not in HTML comments, collapsed blocks or images.

## Never in the body

- A copy of a commit's reasoning or trailers, a list of files, or narration of the diff.
- A result or an assurance: "all tests pass", "verified locally", "safe". What ran is on the commits.
- Checklists. A tick is not evidence, and some bots treat a ticked box as a command.
- Instructions to automated reviewers, or a claim that a reviewer agreed.
- A commit hash or CI link as a pointer to the current head, which the next push replaces. Name commits by subject.
- A closing keyword before an issue reference. Link plainly; close by hand after landing.
- The machinery behind the change: plan steps, task codes, session paths, and the tool, review round or model that made or found it.

## During review

- The body describes the current branch. After a push, fix whatever is no longer true and remove settled questions, rather than appending updates.
- Say what each push changed, in a comment or in the threads, and answer a declined finding where it was raised. A reason that matters later goes into the relevant commit's `Considered and rejected:` before landing.
- Push fix-up commits during a round rather than force-pushing, so reviewers see what changed. If the repository wants a tidy history, fold them before the final approval, make sure each folded commit's `Verified:` lines are still true of it, say in a comment that the branch was folded, and attach a `git range-diff` where content moved. After that approval the branch is not rewritten again; a late finding is a new commit.
- Bring a stale branch current by merging the target into it, not by rebasing: a rebase replaces every commit the reviewers have read.
- Editing the body does not re-run checks or wake review bots. When an edit changes something a reviewer relied on, ask for review again.

## Examples

One commit, no issue:

```
Title: export: close the query cursor when the client disconnects

Closes the cursor leak reported after last week's incident.

### Check
The cursor is closed from the response's context-done hook; check that nothing else in handler.go relies on that hook running exactly once.
Reproduction against staging not run; the "close the query cursor" commit says why.
```

Four commits, one outcome:

```
export: extract row serialisation from the buffered writer
export: add a streaming writer behind the existing interface
export: stream CSV exports instead of buffering them in memory
docs: describe the X-Row-Count trailer for export clients
```

```
Title: export: stream CSV exports instead of buffering them in memory

Exports of over a million rows kill the worker at 2 GB (https://github.com/example/reports/issues/318). This branch streams rows as the cursor advances and moves the row count to a trailer.

### Read
The first two commits are mechanical and keep the buffered path; the third, "stream CSV exports", is the behaviour change. Start with export/stream.go.

### Check
Content-Length disappears from export responses; the "stream CSV exports" commit records the break. Do we know of any client that reads it?
Production-volume replay not run; the "stream CSV exports" commit says why.

### Try
Against staging, request /exports/1.4m.csv with curl -N; worker RSS should stay flat where it used to climb to 2 GB.

### Not in this PR
A progress signal for clients that used Content-Length to show one; not tracked yet.
```

Neither body repeats a commit's reasoning, lists files or states a result.

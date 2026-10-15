# Grounded Commits: pull requests

Format version 0.4.1. Copy this file, or the parts you need, into your repository's guidance for agents. It replaces the pull-request template your agent tool ships with. It pairs with `commit-messages.md`, which defines the subject grammar, the header profile and the trailers it refers to, and optionally with `landing.md`.

The commits are the record. The pull-request body is a short brief for whoever is reviewing now, person or bot, and it is written so that it can be thrown away: nothing in it belongs in history, whichever way the branch lands.

## Title

The outcome of the whole branch, in the grammar of a commit subject under the repository's header profile: `area: outcome`, or `type(area): outcome` under the typed profile. One commit: the title is that commit's subject, exactly, including Git's own subject for a lone revert. Several commits: what the series delivers. No status word of your own; draft state is the forge's mechanism, which is a draft flag on GitHub and GitLab and a configured `WIP:` prefix before the title on Forgejo and Gitea.

## Body

Markdown. GitHub renders a single newline as a line break, so write each paragraph on one line. Leave out any section with nothing to say; a heading followed by filler is a defect. Essential facts go in visible prose, never in HTML comments, collapsed sections or images, which a reader or tool may not expand. The reverse holds too: a fact surrounded by pasted output is as good as hidden, so the body carries no pasted output beyond the one line that identifies the failure the branch addresses, such as the error message in the lead, and never a check result; a comment that must carry more puts it in a collapsed block beneath the sentence that says what it shows.

1. **Lead** (always, no heading). One or two sentences: the problem or request and what the branch does about it, with a plain link to the issue when one exists. This is the body's deliberate overlap with the commits; it carries the objective, not their reasoning, alternatives or evidence. One commit against an issue can be as short as `Delivers <issue URL> in one commit.` With no issue, state the objective; name a source only where it gives the reviewer something the commits cannot, such as a document outside the project's control, never the person you work for and never the tool or model that surfaced the change. "No issue exists" is a disposition under `Not in this PR`, not a refrain for the lead.
2. **`### Read`** (several commits, a stacked pull request, or a diff whose shape is not obvious). Which commits prepare and which change behaviour; where to start; what invariant spans them. For a stacked member, its base branch and the pull request it depends on. Not a list of subjects or files, which the forge shows.
3. **`### Check`** (when there is something specific; never invented to fill the section). Any of: what to scrutinise; a gap a commit records under `Not-verified:`, or a break it records under `Breaking-Change:`, that the reviewer must weigh before approving, in one line each naming the commit by a fragment of its subject in quotes; a question ending in `?` with what turns on the answer. Never a result or an assurance.
4. **`### Try`** (when the change can be exercised or seen). The steps, and what each step should show. An exercise you did not perform yourself is a request under `Check`, not a step here. Screenshots are captioned with the environment and the commit shown. What you observed when you ran it is a `Verified:` line on the commit, not a sentence here.
5. **`### Not in this PR`** (when the request asked for more than the branch delivers, when a review round removed something from the branch, or when something a reviewer would expect is deliberately absent). Each item with its disposition: the URL of the issue that tracks it, "not planned", or "no issue exists". Invent nothing. This describes the branch as a whole: an item a later commit on the branch delivers is not listed.

Soft upper bounds: one commit, about 50 words; a series, 150; several separate outcomes, 250. Going over is the reviewer's cue to look for narration, repetition or assurance.

## Never in the body

- A copy or paraphrase of a commit's reasoning, alternatives, trailers or file list; a narration of the diff. The lead and the `Check` lines above are the permitted overlaps.
- A result or an assurance: "all tests pass", "verified locally", "safe", "thoroughly tested". What ran is on the commits.
- Anything addressed to an automated reviewer: an instruction to approve, to ignore a class of defect or to treat a finding as resolved.
- A claim that a reviewer agreed, approved or withdrew a finding. That lives in the thread.
- Checklists, ticked or unticked.
- A commit hash or a CI-run link as a pointer to the current head, which the next push replaces. Name commits by subject.
- A closing or reopening keyword before an issue reference, in the title or the body. Link plainly; close by hand after landing.
- The machinery behind the change: plan steps, task or requirement codes from a planning record, session paths, and the tool, pipeline, review round or model that made or found it. Also work diaries, CI control tokens, and instructions to future readers or agents.

## During review

- The body describes the current head, always. After each push, rewrite whatever is no longer true and remove settled questions. Never append dated updates.
- Put what each push changed in one ordinary comment: which findings it addresses, which it declines and why. Answer a declined finding in its thread. If the reason matters later, fold it into the relevant commit's `Considered and rejected:` before landing.
- During a round, push fix-up commits rather than force-pushing, so the incremental diff and the inline threads keep working.
- Where the branch must be brought current during review, merge the target into it; a rebase replaces every commit the reviewers have read (`landing.md`).
- A body edit does not by itself re-run checks or request another review: GitHub's `pull_request` trigger omits `edited` unless a workflow opts in, and review bots mostly run on pushes. When an edit changes a premise a reviewer relied on, re-request review.

## Before landing

The branch's commits land as the objects they were reviewed as, so the one rewrite the branch gets comes before its final approval, not after it. Once the reviewers' findings are settled: reword any message the review changed and fold the fix-ups into the commits they correct; rebind the evidence of every commit the fold produced, not only the reworded ones, since folding changes trees (`commit-messages.md`, *After a rewrite*); sign the rewritten commits as you make them where the repository keeps author signatures (`commit.gpgsign`, or `-S` on the rebase), since a rewrite replaces the signed objects, and never with plumbing such as `git commit-tree`, which ignores `commit.gpgsign` and signs only when passed `-S`; push once; and comment with one sentence naming the previous head's hash, what the fold changed, and whether the patch is the one that was reviewed. `git diff <previous-head> HEAD` printing nothing shows that the fold and the rewords changed no content; where it prints something, or a message changed, attach `git range-diff <target> <previous-head> HEAD`, which shows the change commit by commit, messages included, with `--remerge-diff` where the branch keeps merge commits. An attachment sits inside a collapsed block, a `<details>` element whose `<summary>` names the command, with a blank line after the summary so the fenced block inside renders, which GitHub and Forgejo both need. For example:

```
Head 3e7a1c5 folded its two fix-ups and reworded "stream CSV exports" with the Verified line for the re-run; the patch is unchanged (range-diff attached).
```

Approval is then given, or given again, on the folded head, and from that point no commit on the branch is rewritten: a late finding is an ordinary commit with its own message and evidence, never an autosquash fix-up, and another approval, or the pull request waits.

Where the repository follows `landing.md`, landing never rebases the branch onto the target: a branch that is behind is integrated by a merge commit whose first parent is the target's tip and whose second is the approved head, built and checked before it lands, and the target advances to exactly that commit; `landing.md` gives the steps on each forge, what each method does to the commits, and the settings. A repository with its own landing policy keeps it, and still never rewrites an approved head. Under squash the landing message is composed from the branch's commits in the commit format, with the evidence rebound to the landed tree, and supplied explicitly; never the forge's default, and never this body. A pull request from a fork lands by the route the repository's guidance records; with none recorded, ask the user.

Ready to land means: no open question in the body, `Not in this PR` current, every commit message true of its contents, the forge not showing draft state, the required approvals present on the head that will be merged, and the required checks passing on the tree that will land, which is the integration candidate's, not the head's alone, unless the head already contains the target. After landing, read back that the approved head is an ancestor of the target's tip, its second parent under a merge or the tip itself after a fast-forward, or under squash that the landed tree is the checked tree; then close each fully delivered issue by hand, in a comment naming the landed commit.

## Examples

One commit, no issue:

```
Title: export: close the query cursor when the client disconnects

Closes the cursor leak reported after last week's incident.

### Check
The cursor is closed from the response's context-done hook; check that nothing else in handler.go relies on that hook running exactly once.
Reproduction against staging not run; the "close the query cursor" commit's trailer says why.
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
Production-volume replay not run; the "stream CSV exports" commit's trailer says why.

### Try
Against staging, request /exports/1.4m.csv with curl -N; worker RSS should stay flat where it used to climb to 2 GB.

### Not in this PR
A progress signal for clients that used Content-Length to show one; no issue exists.
```

Nothing in either body repeats a commit's reasoning, lists files or states a result.

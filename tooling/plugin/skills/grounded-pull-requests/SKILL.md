---
name: grounded-pull-requests
description: Write and maintain a pull request's title and body as a review brief in the Grounded Commits convention, where the commits carry the record and the body holds only what no commit can. Use when opening, describing, retitling or updating a pull request, commenting on a push during review, or preparing an approved branch to land, in a repository that has adopted Grounded Commits — its agent guidance says so, or it has a .grounded-commits.toml or the Grounded Commits commit-msg hook; and when asked to write a grounded PR description. The commit messages themselves are grounded-commits.
---

# Grounded Pull Requests

The commits are the record. The pull-request body is a disposable brief for
whoever is reviewing now, person or bot: where to start, what to scrutinise,
what could not be checked, how to see the change work, and what was asked for
but is not here. Nothing in it belongs in history, whichever way the branch
lands.

A repository adopts this convention together with the commit format: its
agent guidance says it follows Grounded Commits, or it has a
`.grounded-commits.toml` or the Grounded Commits `commit-msg` hook (the
grounded-commits skill's *Where it applies*). There it replaces the
pull-request template your tool ships with and the shape of earlier pull
requests; elsewhere, write a grounded pull request only when asked to. A
user's explicit instruction about a particular pull request overrides this
skill. The subject grammar, header profile and trailers this skill refers to
are the grounded-commits skill's: read it (`../grounded-commits/SKILL.md`,
relative to this skill's directory) before writing a title or a landing
message.

## Title

The outcome of the whole branch, in the grammar of a commit subject under the
repository's header profile: `area: outcome`, or `type(area): outcome` under
the typed profile. One commit: the title is that commit's subject, exactly,
including Git's own subject for a lone revert. Several commits: what the
series delivers. Draft state is the forge's mechanism, not a word in the
title — a draft flag on GitHub and GitLab, the configured `WIP:` prefix before
the title on Forgejo and Gitea.

## Body

Markdown. GitHub renders a single newline as a line break, so write each
paragraph on one line. Leave out any section with nothing to say; a heading
followed by filler is a defect.

1. **Lead** (always, no heading). One or two sentences: the problem or request
   and what the branch does about it, with a plain link to the issue when one
   exists. This is the body's deliberate overlap with the commits; it carries
   the objective, not their reasoning, alternatives or evidence. One commit
   against an issue can be as short as `Delivers <issue URL> in one commit.`
   With no issue, state the objective and where the request came from, for
   example "requested by the maintainer in the review of the export branch;
   no issue exists".
2. **`### Read`** (several commits, a stacked pull request, or a diff whose
   shape is not obvious). Which commits prepare and which change behaviour;
   where to start; what invariant spans them. For a stacked member, its base
   branch and the pull request it depends on. Not a list of subjects or files,
   which the forge shows.
3. **`### Check`** (when there is something specific; never invented to fill
   the section). Any of: what to scrutinise; a gap a commit records under
   `Not-verified:`, or a break it records under `Breaking-Change:`, that the
   reviewer must weigh before approving, in one line each naming the commit by
   a fragment of its subject in quotes; a question ending in `?` with what
   turns on the answer. Never a result or an assurance.
4. **`### Try`** (when the change can be exercised or seen). The steps, and
   what each step should show. An exercise you did not perform yourself is a
   request under `Check`, not a step here. Screenshots are captioned with the
   environment and the commit shown. What you observed when you ran it is a
   `Verified:` line on the commit, not a sentence here.
5. **`### Not in this PR`** (when the request asked for more than the branch
   delivers, or when something a reviewer would expect is deliberately
   absent). Each item with its disposition: the URL of the issue that tracks
   it, "not planned", or "no issue exists". Invent nothing. This describes the
   branch as a whole: a commit's `Not done:` item that a later commit on the
   branch delivers does not appear.

Soft upper bounds: one commit, about 50 words; a series, 150; several
separate outcomes, 250. Going over is the reviewer's cue to look for
narration, repetition or assurance.

## Never in the body

- A copy or paraphrase of a commit's reasoning, alternatives, trailers or file
  list; a narration of the diff. The lead and the `Check` lines above are the
  permitted overlaps.
- A result or an assurance: "all tests pass", "verified locally", "safe",
  "thoroughly tested". What ran is on the commits.
- Anything addressed to an automated reviewer: an instruction to approve, to
  ignore a class of defect or to treat a finding as resolved.
- A claim that a reviewer agreed, approved or withdrew a finding. That lives in
  the thread.
- Checklists, ticked or unticked.
- A commit hash or a CI-run link as a pointer to the current head, which the
  next push replaces. Name commits by subject.
- A closing or reopening keyword before an issue reference, in the title or the
  body. Link plainly; close by hand after landing.
- Model names, session paths, plan steps, tracking codes, CI control tokens.

## During review

- The body describes the current head, always. After each push, rewrite
  whatever is no longer true and remove settled questions. Never append dated
  updates.
- Put what each push changed in one ordinary comment: which findings it
  addresses, which it declines and why. Answer a declined finding in its
  thread. If the reason matters later, fold it into the relevant commit's
  `Considered and rejected:` before landing.
- During a round, push fix-up commits rather than force-pushing, so the
  incremental diff and the inline threads keep working.
- A body edit does not by itself re-run checks or request another review:
  GitHub's `pull_request` trigger omits `edited` unless a workflow opts in,
  and review bots mostly run on pushes. When an edit changes a premise a
  reviewer relied on, re-request review.

## Before landing

Once review is approved, record the reviewed head's hash. Then, if the branch
will land by a method that keeps its commits (rebase or fast-forward), fold
the fix-ups into the commits they correct, reword any message the review
changed, rebase onto the target, rebind the evidence of every commit the
rewrite produced — not only the reworded ones, since folding and rebasing
change trees (grounded-commits, *After a rewrite*) — and push once; a branch
that contains merge commits is rebased with `--rebase-merges` or deliberately
flattened. If it will land by squash or merge commit, folding is optional,
and the landed message is supplied explicitly: for a squash, one message
composed in the commit format from the branch's commits, with evidence
rebound to the landed tree; for a merge commit, the pull-request title alone.
Never the forge's default, and never this body. A pull request from a fork
lands by the route the repository's guidance records — rebased as written,
squashed with a composed message, or reworded on the contributor's branch
only where they allow edits from maintainers; with no route recorded, ask
the user. Either way, comment with the reviewed head and two results:

```
git diff <reviewed-head> HEAD
git range-diff <target> <reviewed-head> HEAD
```

The first is empty unless the target moved underneath or something reviewed
was dropped; the second shows what changed commit by commit, messages
included. Re-run the checks on the new tip or record the gap with
`Not-verified:`. Ready to land means: no open question in the body, `Not in
this PR` current, every commit message true of its folded contents, the forge
not showing draft state, the required approvals present, and the required
checks passing on the exact head that will land. Where the landing method
rewrote the commits, read the landed messages back (`git log --format=%B
<range>`) and compare them with what was pushed. After landing, close each
fully delivered issue by hand, in a comment naming the landed commit.

## Examples

One commit, no issue:

```
Title: export: close the query cursor when the client disconnects

Closes the cursor leak the on-call rotation reported in last week's incident review; no issue exists.

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


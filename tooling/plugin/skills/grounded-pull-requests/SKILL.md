---
name: grounded-pull-requests
description: Write and maintain a pull request's title and body as a review brief in the Grounded Commits convention. Use when opening, describing, retitling or updating a pull request, commenting on a push during review, or preparing an approved branch to land, in a repository that has adopted Grounded Commits, and when asked to write a grounded PR description. The commit messages themselves are grounded-commits.
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
followed by filler is a defect. Essential facts go in visible prose, never in
HTML comments, collapsed sections or images, which a reader or tool may not
expand. The reverse holds too: a fact surrounded by pasted output is as good
as hidden, so the body carries no pasted output beyond the one line that
identifies the failure the branch addresses, such as the error message in the
lead, and never a check result; a comment that must carry more puts it in a
collapsed block beneath the sentence that says what it shows.

1. **Lead** (always, no heading). One or two sentences: the problem or request
   and what the branch does about it, with a plain link to the issue when one
   exists. This is the body's deliberate overlap with the commits; it carries
   the objective, not their reasoning, alternatives or evidence. One commit
   against an issue can be as short as `Delivers <issue URL> in one commit.`
   With no issue, state the objective; name a source only where it gives the
   reviewer something the commits cannot, such as a document outside the
   project's control, never the person you work for and never the tool or
   model that surfaced the change. "No issue exists" is a disposition under
   `Not in this PR`, not a refrain for the lead.
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
   delivers, when a review round removed something from the branch, or when
   something a reviewer would expect is deliberately absent). Each item with
   its disposition: the URL of the issue that tracks it, "not planned", or
   "no issue exists". Invent nothing. This describes the branch as a whole:
   an item a later commit on the branch delivers is not listed.

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
- The machinery behind the change: plan steps, task or requirement codes from
  a planning record, session paths, and the tool, pipeline, review round or
  model that made or found it. Also work diaries, CI control tokens, and
  instructions to future readers or agents.

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
- Where the branch must be brought current during review, merge the target
  into it; a rebase replaces every commit the reviewers have read
  (`references/landing.md`).
- A body edit does not by itself re-run checks or request another review:
  GitHub's `pull_request` trigger omits `edited` unless a workflow opts in,
  and review bots mostly run on pushes. When an edit changes a premise a
  reviewer relied on, re-request review.

## Before landing

The branch's commits land as the objects they were reviewed as, so the one
rewrite the branch gets comes before its final approval, not after it. Once
the reviewers' findings are settled, read `references/before-landing.md` for
folding the fix-ups, rebinding their evidence, signing, and the push comment.

Approval is then given, or given again, on the folded head, and from that
point no commit on the branch is rewritten: a late finding is a fix-up commit
and another approval, or the pull request waits.

Landing never rebases the branch onto the target. A branch that is behind is
integrated by a merge commit whose first parent is the target's tip and whose
second is the approved head, built and checked before it lands, and the
target advances to exactly that commit; `references/landing.md`, relative to
this skill's directory, gives the steps on each forge, what each method does
to the commits, and the settings. Under squash the landing message is
composed from the branch's commits in the commit format, with the evidence
rebound to the landed tree, and supplied explicitly; never the forge's
default, and never this body. A pull request from a fork lands by the route
the repository's guidance records; with none recorded, ask the user.

Ready to land means: no open question in the body, `Not in this PR` current,
every commit message true of its contents, the forge not showing draft state,
the required approvals present on the head that will be merged, and the
required checks passing on the tree that will land, which is the integration
candidate's, not the head's alone, unless the head already contains the
target. After landing, read back that the approved head is an ancestor of
the target's tip, its second parent under a merge or the tip itself after a
fast-forward, or under squash that the landed tree is the checked tree; then
close each fully delivered issue by hand, in a comment naming the landed
commit.

## Examples

Read `references/examples.md` for a one-commit body with no issue and a
four-commit series with one outcome.

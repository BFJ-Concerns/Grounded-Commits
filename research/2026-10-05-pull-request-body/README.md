# The pull-request body for rebase-and-fast-forward landing

Research record, 5 October 2026. The question: what should a pull-request body
contain, and how should it be kept, when coding agents open most pull requests,
human and automated reviewers read them, and branches land by rebase and
fast-forward, so that nothing written in the pull request enters history?

Three things were settled before the research began. Branches land by rebase
and fast-forward. Commit messages, in the format from
`../2026-10-02-commit-message-formats/`, are the record. The pull request is the
place for review, and it still needs a body. The target forge is GitHub;
Forgejo's behaviour is noted where it differs.

## Contents

- `REPORT.md` — the specification, worked examples, reasoning by reader, what
  was rejected, what would change the answer, and where each decision came
  from. About 5,000 words.
- `GUIDANCE-DRAFT.md` — a one-screen distillation as an agent would read it in
  repository guidance. A draft to adapt, not a rule.

## Headline

The body is a short brief for whoever is reviewing now; the commits own the
account. A lead of one or two sentences with a plain issue link, then up to four
sections, each left out when it has nothing to say: **Read** (how the branch is
built and where to start), **Check** (what to scrutinise, what could not be
verified, what needs deciding), **Try** (how to see the change work) and **Not in
this PR** (what was asked for and is missing). No commit-message text, results,
assurances, checklists, hashes or issue-closing keywords. The title uses the
commit-subject grammar. The body is rewritten in place after every push, each
push gets one comment, and any lasting reason is folded into a commit before
landing. Landing folds the fix-ups, rebases, pushes once with a `git diff`
statement, then fast-forwards; on GitHub that is a push of the approved tip.
Confidence moderate: no study compares pull-request body formats.

## How it ran

Two rounds, each with one Claude Fable 5.1 worker and one GPT-6 Astra worker at
`high` effort, working blind in separate directories.

1. **Proposals.** Each designer answered the same brief independently. The
   brief fixed the premises above and set aside an earlier design (3 October
   2026), made for squash and merge-commit landing, that turned the body into a
   mechanical copy of the commit message. Under fast-forward that copy controls
   nothing, and it made the redundant part mandatory and the review material
   optional. The report's *What was rejected* describes it.
2. **Judgement and synthesis.** Each designer read its own proposal, then the
   other's, judged the other's against the brief while fetching the sources
   behind its factual claims, and then wrote a synthesis of both. Astra rated its
   own proposal stronger; Fable rated the two even. Astra's checks found five of
   Fable's claims wrong or overstated; Fable's confirmed Astra's. Each synthesis
   kept its author's section structure while adopting most of the other's
   content.

The report is the Fable synthesis. It was chosen for its concrete sections, a
body with nothing that goes stale on a rebase, and its consistency with the
commit format, which keeps results in `Verified:` trailers. It was edited after
the round in three ways:

- **Check** is conditional rather than required, following Astra's judgement
  that a required section invites invented doubts.
- The GitHub landing route was corrected against GitHub's documentation. A
  merge queue builds its own commits, so it cannot fast-forward. Landing is a
  push of the approved tip by an identity allowed to bypass branch protection.
  Stale approvals are dismissed only by pushes that affect the diff. The fork
  condition below was added.
- References to the earlier design were made self-contained, and every
  remaining Fable claim that Astra found wrong or overstated was corrected.

The edited report was not cross-checked again. The proposals, judgements, the
Astra synthesis and the run records are not included; every claim in the report
cites its primary source directly.

## Open points

- **Pull requests from forks.** GitHub records a fast-forward as a merge only
  when the pull request's own head commits reach the base branch. A rebase or a
  reworded message therefore has to reach the contributor's branch first, which
  maintainers can push to only when the contributor allows edits from
  maintainers, on a user-owned fork. Outside contributors' commit messages will
  not follow the commit format either. How a repository with many outside
  contributions lands them is undecided.
- **The landing identity.** Pushing to a protected branch needs an identity
  allowed to bypass protection, so the landing step must check approval and
  passing checks on the exact tip itself.
- **Benefit and length** are unmeasured. A scored sample of agent-written
  bodies would show whether the sections steer agents away from filler and
  invented results.

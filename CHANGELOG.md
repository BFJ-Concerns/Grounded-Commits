# Changelog

## Unreleased

- Fast-forward is the default landing method, as the research decided, and
  rebase the stated fallback, chosen once by a repository whose forge cannot
  fast-forward: on GitHub, one whose landing identity may not push the
  approved tip to the target. On GitHub a rebase landing creates new
  commits, so hashes and signatures are lost and a commit that was empty to
  begin with is dropped; Forgejo and Gitea rewrite only a branch that is
  behind or one a merge template amends, and a template amend fails on an
  originally empty tip, so such a commit's message is folded into a
  neighbour before any rebase landing. Templates are read from the base
  repository's default branch, per forge: Gitea's `REBASE_TEMPLATE.md` then
  its `DEFAULT_TEMPLATE.md` fallback, Forgejo's under `.forgejo/` or
  `.gitea/` then the instance's own, an empty file still yielding the
  default message. A fork's prepared branch must become the pull request's
  head, pushed by the maintainer where the contributor allows edits or by
  the contributor. A repository that signs its commits lands by
  fast-forward or merge commit. The plugin's pull-request skill bundles the
  landing guidance as `references/landing.md`, kept byte-identical to
  `guidance/landing.md` by the plugin test.
- The pull-request guidance's *Before landing* comment is one sentence: the
  reviewed head, what happened since approval, nothing included, and whether
  the landing tip's tree is identical to the reviewed head's, with each
  reworded commit named by subject. Evidence sits only inside a collapsed
  `<details>` block, with the blank line after the summary that GitHub and
  Forgejo both need before a fenced block renders: the `git range-diff` when
  any commit changed, or two comparisons of the branch's patches and messages
  where preparation flattened a merge commit, which range-diff misreports.
  `git diff <reviewed-head> HEAD` is never pasted: after a rebase it mixes the
  target's drift with any change to the branch. Before, the section asked for
  the output of both commands on every landing, and on a flattened merge head
  one comment ran to 18 KB with thirty lines of signal. Preparation applies to
  every method: reword and fold where the branch's commits land, both optional
  under squash alone, with an originally empty commit's message folded into a
  neighbour before a rebase landing; rebase onto the target, which drops a
  merge of the target (with `--rebase-merges`, in its `rebase-cousins` mode);
  re-apply what each other merge carried, kept or flattened; rebind the
  evidence; sign the rewritten commits where they will land and the repository
  keeps author signatures; push once. The guidance also says essential facts
  go in visible prose, never in HTML comments, collapsed sections or images,
  and that the body carries no pasted output beyond the one line that
  identifies the failure the branch addresses; its list of what never goes in
  the body includes work diaries and instructions to future readers or agents;
  `Not in this PR` also covers what a review round removed from the branch;
  and ready to land includes the branch sitting on the target's current tip,
  put there by rebase.
- The commit body has no `Not done:` line, and the hook no longer checks for
  one. What the request asked for and the branch does not deliver is a
  property of the pull request, recorded under `Not in this PR`; the
  pull-request research rejected a per-commit line on that ground, and the
  commit guidance had added one without recording a reason. A commit's own
  limits stay in its body as prose.
- The area derivation's prose says what the hook does. A `ci/`, `docs/`,
  `test/`, `tests/` or `build/` directory is an area, as is any of those
  names as a path-map label or listed area; a file whose stem reads as one
  of those, or as a change-type word, keeps its extension (`build.gradle`,
  `fix.py`), and one with no extension gives `all`; a directory named for a
  change type gives `all`. Before, the guidance said a directory of any of
  those names gave `all`, which the hook never did. The hook itself gains
  three corrections: an extensionless root file named for a directory-only
  word yields `all` rather than the bare word; the files that stand for
  their directory (`__init__.py`, `__main__.py`, `mod.rs`, `lib.rs`,
  `main.rs`, `main.go`, `index` with a JavaScript or TypeScript extension)
  are matched by full name, so `__init__.py` yields its directory as the
  guidance always said and `Main.kt` stays an ordinary file; and such a
  file gives `all` where its directory is layout, or `test` or `tests`
  directly inside layout, so a crate's `src/lib.rs` no longer yields
  `src`. The README no longer claims an area never moves when unrelated
  files are added: the only-subdirectory rule reads the tracked tree, so a
  layout directory gaining or losing its second subdirectory moves the
  area beneath it, and the guidance says so. The research notes record why
  the derivation goes beyond the report's wrapper-stripping rule, why
  `Fixes:` became `Introduced-by:`, and a reason for every other departure.
- The commit guidance states Git's rule for a mixed final paragraph (at
  least a quarter trailers, one of them Git-generated or configured). The
  landing guidance's rebase row asks for a linear branch rebased onto the
  target's current tip, so the replay reproduces the prepared trees and
  their evidence; GitHub's and Forgejo's up-to-date protections accept a
  merge from the target, so update by rebase. GitLab's fast-forward route
  turns automatic rebase before merge off.

## 0.2.0 — 2026-10-07

- The pull-request guidance's *Before landing* section says to rebind the
  evidence of every commit a pre-landing rewrite produced, not only the
  reworded ones, matching the commit guidance's *After a rewrite*: folding
  and rebasing change trees even where the message is unchanged. It also
  says to pass `--remerge-diff` to the landing comment's `git range-diff`
  when the branch keeps merge commits, which the command otherwise ignores.
- The hook checks a draft message against an existing commit without
  committing it: `--message-file draft.txt --rev HEAD` runs the same check
  `--rev HEAD` runs on the commit's own message, so a rewrite can be checked
  before the amend or reword that records it. Before, a draft could only be
  checked against hand-listed `--paths`, which skipped the lookups of
  `Introduced-by:` hashes, or by committing it.
- An agent plugin for Claude Code and Codex, installable from this
  repository's marketplace with either tool's plugin commands. It carries
  the guidance as two skills, one for commit messages and one for
  pull-request titles and bodies, and bundles the hook so the commit skill
  can print candidate areas, check commits and drafts, and install the hook
  into a repository.

## 0.1.1 — 2026-10-06

- The hook no longer reads every upper-case word followed by a hyphen and
  digits as an issue key, which rejected subjects naming identifiers such as
  `AGPL-3.0-or-later`, `UTF-8` and `SHA-256`. A repository that uses a
  tracker with keys of that shape lists them in `.grounded-commits.toml` as
  `issue_keys = ["PROJ"]`; the hook then rejects `PROJ-42` in a subject and
  after a closing keyword, and treats any other key-shaped token as an
  identifier. `#N`, `owner/repo#N` and issue URLs are caught as before.

## 0.1.0 — 2026-10-06

First version.

- The Grounded Commits commit-message format: an `area: outcome` subject
  derived from the changed paths, a problem-first body, and a trailer block
  carrying the evidence, with Conventional Commits available as a typed header
  profile.
- The pull-request body: a short review brief that points at the commits
  instead of repeating them.
- Landing, optional, with rebase as the default and configuration for
  fast-forward, merge commits and squash on GitHub, GitLab, Forgejo and Gitea.
- A reference `commit-msg` hook with fixtures under `tooling/commit-msg-hook/`,
  including a `--range` mode for landing and CI checks.
- The research behind the format, with every claim cited to its primary source.
- MIT licence; the guidance files are also dedicated to the public domain so
  they can be pasted into any repository without a notice.

# Changelog

## Unreleased

- The commit body has no `Not done:` line, and the hook no longer checks for
  one. What the request asked for and the branch does not deliver is a
  property of the pull request, recorded under `Not in this PR`; the
  pull-request research rejected a per-commit line on that ground, and the
  commit guidance had added one without recording a reason. A commit's own
  limits stay in its body as prose.
- The area derivation's prose says what the hook does. A `docs/`, `test/`,
  `build/` or `ci/` directory is an area; a file whose stem reads as one of
  those, or as a change-type word, keeps its extension (`build.gradle`,
  `fix.py`); a directory named for a change type gives `all`. Before, the
  guidance said a directory of any of those names gave `all`, which the hook
  never did. The README no longer claims an area never moves when unrelated
  files are added: the only-subdirectory rule reads the tracked tree, so a
  layout directory gaining a second subdirectory moves the area beneath it,
  and the guidance now says so. The research note records why the derivation
  goes beyond the report's one-line rule.
- The pull-request guidance's *Before landing* comment is one sentence: the
  reviewed head, what the push did, and whether the landing tip's tree is
  identical to the reviewed head's, with each reworded commit named by
  subject. Evidence is attached only when something changed and only inside
  a collapsed `<details>` block: the messages' diff when only messages
  changed, the `git range-diff` when the tree differs. Before, the section
  asked for the output of `git diff <reviewed-head> HEAD` and `git
  range-diff` on every landing; after a rebase the first is the target's
  drift and the second repeats it as context, and on a branch whose
  reviewed head was a merge commit that landing flattened, one comment ran
  to 18 KB with thirty lines of signal. `landing.md`, the README and the
  plugin's pull-request skill say the same.

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

# Changelog

## Unreleased

- The hook checks a draft message against an existing commit without
  committing it: `--message-file draft.txt --rev HEAD` runs the same check
  `--rev HEAD` runs on the commit's own message, so a rewrite can be checked
  before the amend or reword that records it. Before, a draft could only be
  checked against hand-listed `--paths`, which skipped the lookups of
  `Introduced-by:` hashes, or by committing it.

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

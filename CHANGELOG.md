# Changelog

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

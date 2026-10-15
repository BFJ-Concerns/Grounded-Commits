# Changelog

## 0.5.0 — 2026-10-15

The format asks for what matters and leaves the rest to the writer. The
guidance is a third of its former size, the hook rejects only what breaks
the record, and nobody has to learn a procedure to write a subject.

- An area is any directory or file name from the changed paths, a path-map
  label, a listed area, or one of `all`, `docs`, `ci`, `build`, `tests` and
  `deps`. The derivation procedure, with its lists of collection and layout
  directories, its only-subdirectory rule and its 24-character cap, is
  gone. Only the change-type words (`fix`, `feat`, `chore` and the like)
  are refused.
- The hook no longer judges the outcome's wording: a capital, a digit, a
  `!`, a full stop, an emoji or an issue number in the subject passes. It
  no longer asks for a body or forbids headings. A trailer key in another
  case (`verified:`) is read as Git reads it. Lines may run to 80 columns;
  the guidance asks for about 72.
- Evidence is owed on code-like paths only. Ignore files, `.editorconfig`,
  `.gitattributes`, `.mailmap` and `CODEOWNERS` count as documentation. A
  change that is only renames or whitespace owes none, judged from the diff
  rather than from the subject's words, so the list of trivial wordings is
  gone.
- A clean merge keeps Git's message and owes nothing; only a merge that
  resolved conflicts owes evidence. The `forge_merge_committers` key is
  gone with the exemption it configured. A revert keeps Git's sentence and
  says whether it is partial.
- `Verified:` names the tree it tested as `this commit` rather than `final
  contents`; the hook treats both as words. `Not-verified:` is a scope and
  a reason in any words; `not run:` and `result unavailable:` are accepted
  but no longer required. Only an `Introduced-by:` hash is checked for
  ancestry.
- The dictated phrases, the named evidence scopes, the tree-hash comparison
  after a rewrite and the blanket ban on `Signed-off-by` are replaced by the
  principles they stood for: say so when you do not know why; keep the
  evidence true of the new tree; add `Signed-off-by` when the person signing
  asks for it.
- The pull-request body keeps its lead and four optional sections without
  word budgets, quotation rules or a fixed comment per push. The fold before
  final approval is a comment and a range-diff where content moved.
- Landing fast-forwards a current branch and builds a checked merge only for
  one that is behind. The GitHub row names no plans and requires no queue;
  draft state names no forge.
- The typed-header example describes a non-numeric Content-Length, a defect
  the server can detect. The examples show how to record that the old code
  fails the new tests without naming a scratch commit.
- The README is half its former length; the skills mirror the guidance and
  drop the area-derivation, rewrite and before-landing references; the
  `--tracked` flag is gone with the tree-reading derivation.

## 0.4.1 — 2026-10-15

- The research records are replaced by two background notes,
  `background/commit-messages.md` and `background/pull-requests.md`, which
  keep the evidence and its sources and drop the account of how the
  records were produced. They no longer restate the guidance, so they no
  longer disagree with it. The README links each study it cites directly.

## 0.4.0 — 2026-10-11

- A reviewed branch lands as a checked integration candidate: a merge
  commit whose first parent is the target's tip and whose second is the
  approved head, built before landing, checked as the tree that lands,
  signed, and carrying its own `Verified:` line and the pull request's
  URL; the target then advances to exactly that commit, and no reviewed
  commit is rewritten. Rebasing before a fast-forward, the earlier
  default, replayed every commit as a new object with a tree the checks
  need not have run on and without its signature. `landing.md` gives the
  steps for GitHub with and without a merge queue, Forgejo, GitLab and
  plain Git, what each method does to the commits, and the settings;
  Gitea was not checked. The one rewrite a branch gets, folding its
  fix-ups, comes before its final approval.
- A merge that resolves nothing still owes the evidence pair for its
  tree, and may carry the pull request's URL under `Refs:` and reviewer
  trailers; a merge the forge made, carrying its default message, is
  the exception, its evidence being the forge's run read back at
  landing. The hook asks a merge for evidence when what it brings in
  goes beyond documentation and exempts a merge whose committer is a
  forge (`forge_merge_committers`).
- A hash in a message names an ancestor of the commit; a rebound
  `Verified:` line keeps its check, names the earlier tree in words, and
  declares the new tree's gap with what the rewrite did to the commit's
  files. The hook confirms the rule for a hash in a `Verified:` line's
  tested-contents part or in `Introduced-by:`, against the commit's
  parents.
- The body leads with the problem or goal as it reached the writer, in
  its own words, and is owed only where it says more than the subject's
  inverse: a subject that already states the gap may stand alone with
  the evidence pair, which the hook accepts. A source is named only
  where it gives the reader something the commit cannot, never the
  person the writer works for; footing marks a given claim rather than
  its giver; the floor is the one phrase "reason not available to the
  writer". The pull-request lead follows the same rule, and the examples
  that taught "the maintainer asked" and "no issue exists" are replaced.
- Hook: the typed profile's consistency check leaves native merge and
  revert subjects alone; under the paragraph marker the
  `BREAKING CHANGE:` paragraph and the `Breaking-Change:` trailer are
  each asked for when the other is present, the paragraph last and not
  empty; a scope directory is skipped only inside a collection
  directory; `--range` flags an unfolded autosquash commit; `--repo`
  from another directory sees a merge in progress; one long token
  excuses only itself from the width rule; an outcome may not begin
  with a digit, and a changed file's own name may open it in its own
  case; manifests such as `package.json` and `pyproject.toml` count as
  dependency files.
- The two bundled skills are held to the skill-and-plugin-authoring
  skill, which the repository now carries for Codex and Claude Code:
  the descriptions name the job and when to invoke, and adoption,
  rewrites, the fold before approval and the worked examples sit in
  references behind pointers.
- The research record is organised by topic, `research/commit-messages.md`
  and `research/pull-requests.md`, each the current state of what is
  known and ending in a dated method log; the landing research of
  11 October 2026 is merged into the pull-request record. The dated
  directories and the guidance drafts are gone.
- The guidance files are MIT like the rest of the repository; the
  README no longer dedicates them to the public domain under CC0 1.0,
  a dedication whose text the repository never carried.

## 0.3.3 — 2026-10-10

- `commit-msg --message-file <draft>` on its own checks the draft against
  the staged change, as `git commit -F` would record it, giving the verdict
  the recorded commit will get. During a merge, a linked worktree's
  included, it keeps Git's merge subject and judges the merge's resolutions
  against the staged tree, so a merge's message can be checked before the
  merge commit exists. That form used to check against no paths, which
  applied the `<area>: <outcome>` subject rule to a merge. Shape-only
  checking is `--message-file <draft> --paths` with no paths.

## 0.3.2 — 2026-10-09

- The hook judges what a merge resolved by comparing it with Git's own merge
  of its parents, so a clean merge of a file both sides changed passes with no
  body and no evidence pair, and a conflict resolved by keeping one side is
  asked for both. Checking a merge needs Git 2.38 or newer; an octopus merge
  is still checked against the paths that differ from every parent.
- The hook flags Git's `# Conflicts:` list kept in a recorded message, which
  a commit made without the editor keeps, and no longer counts it as a body.

## 0.3.1 — 2026-10-08

- Where a request came from is a person or role, an issue, or a document a
  reader of the repository can open, never the tool, review or model that
  surfaced it, in the commit body and in the pull-request lead. The ban on
  session-local references now names the machinery behind the change: plan
  steps, task or requirement codes from a planning record, scratch paths, and
  the tool, pipeline, gate, review round or model that made or found the
  change or will run a later check. It asks for what was found rather than
  what found it, and for a requirement in its own words. A model the change
  is about is no longer caught by it, and a `Verified:` line still names its
  command and any CI run that reported a result.
- A `Not-verified:` reason says what kept the check from running or its result
  from being recovered, never who will run it next or where in a pipeline it
  runs.
- The `Refs:` rule says issues are closed by hand after landing, matching the
  pull-request and landing guidance.

## 0.3.0 — 2026-10-07

- Fast-forward is the default landing method, as the research decided, and
  rebase the stated fallback, chosen once by a repository whose forge cannot
  fast-forward: on GitHub, one whose landing identity may not push the
  approved tip to the target. On GitHub a rebase landing creates new commits,
  so hashes and signatures are lost and a commit that was empty to begin with
  is dropped; Forgejo and Gitea rewrite only a branch that is behind or one a
  merge template amends, and a template amend fails on an originally empty
  tip, so such a commit's message is folded into a neighbour before any rebase
  landing. The rebase that prepares the branch drops a commit whose change the
  target already carries, its message with it; reasoning that still matters
  moves into a neighbour's body, and the landing comment names the commit.
  Templates are read from the base repository's default branch, per forge:
  Gitea's `REBASE_TEMPLATE.md` then its `DEFAULT_TEMPLATE.md` fallback,
  Forgejo's under `.forgejo/` or `.gitea/` then the instance's own, an empty
  file still yielding the default message. A fork's prepared branch must
  become the pull request's head, pushed by the maintainer where the
  contributor allows edits or by the contributor. A repository that signs its
  commits lands by fast-forward or merge commit. The plugin's pull-request
  skill bundles the landing guidance as `references/landing.md`, kept
  byte-identical to `guidance/landing.md` by the plugin test.
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
  re-apply what each merge carried, the dropped merge of the target included;
  rebind the evidence; sign the rewritten commits where they will land and the
  repository keeps author signatures; push once. The guidance also says
  essential facts go in visible prose, never in HTML comments, collapsed
  sections or images, and that the body carries no pasted output beyond the
  one line that identifies the failure the branch addresses; its list of what
  never goes in the body includes work diaries and instructions to future
  readers or agents; `Not in this PR` also covers what a review round removed
  from the branch; and ready to land includes the branch sitting on the
  target's current tip, put there by rebase.
- The commit body has no `Not done:` line, and the hook no longer checks for
  one. What the request asked for and the branch does not deliver is a
  property of the pull request, recorded under `Not in this PR`; the
  pull-request research rejected a per-commit line on that ground, and the
  commit guidance had added one without recording a reason. A commit's own
  limits stay in its body as prose.
- The area derivation's prose says what the hook does. A `ci/`, `docs/`,
  `test/`, `tests/` or `build/` directory is an area, as is any of those names
  as a path-map label or listed area; a file whose stem reads as one of those,
  or as a change-type word, keeps its extension (`build.gradle`, `fix.py`),
  and one with no extension gives `all`; a directory named for a change type
  gives `all`. Before, the guidance said a directory of any of those names
  gave `all`, which the hook never did. The hook itself gains four
  corrections: an extensionless root file named for a directory-only word
  yields `all` rather than the bare word; the files that stand for their
  directory (`__init__.py`, `__main__.py`, `mod.rs`, `lib.rs`, `main.rs`,
  `main.go`, `index` with a JavaScript or TypeScript extension) are matched by
  full name, so `__init__.py` yields its directory as the guidance always said
  and `Main.kt` stays an ordinary file; such a file gives `all` where its
  directory is layout, or `test` or `tests` directly inside layout, so a
  crate's `src/lib.rs` no longer yields `src`; and `test` or `tests` beneath a
  layout directory's only subdirectory or a JVM package root is the area, as
  step 2 says, where the hook had skipped it as layout and derived the file's
  stem. The README no longer claims an area never moves when unrelated files
  are added: the only-subdirectory rule reads the tracked tree, so a layout
  directory gaining or losing its second subdirectory moves the area beneath
  it, and the guidance says so. The research notes record why the derivation
  goes beyond the report's wrapper-stripping rule, why `Fixes:` became
  `Introduced-by:`, and a reason for every other departure.
- The commit guidance states Git's rule for a mixed final paragraph (at least
  a quarter trailers, one of them Git-generated or configured). The landing
  guidance's rebase row asks for a linear branch rebased onto the target's
  current tip, so the replay reproduces the prepared trees and their evidence;
  GitHub's and Forgejo's up-to-date protections accept a merge from the
  target, so update by rebase. GitLab's fast-forward route turns automatic
  rebase before merge off. The README's `result unavailable` also covers a
  check the writer cannot tell ran, as the guidance says.

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

---
name: grounded-commits
description: Write and check commit messages in the Grounded Commits format. Use when committing, amending, rebasing, squashing or cherry-picking in a repository that has adopted the format, when asked to write a grounded commit or to check a commit message against the format, and when adopting the format in a repository; other repositories keep their own commit style. The pull-request title and body that go with the format are grounded-pull-requests.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/commit-msg*)
---

# Grounded Commits

A grounded commit records what its writer holds at commit time, instead of
reconstructing it:

> Write only what you have: the request, what you observed, what you changed,
> what you ran. Say plainly what you lack.

In a repository that has adopted the format, it replaces the style of earlier
commits and any instruction to imitate recent messages. A user's explicit
instruction about a particular commit overrides this skill.

## Where it applies

A repository has adopted the format when any of these holds:

- its agent guidance (`AGENTS.md`, `CLAUDE.md` or equivalent) says its commits
  follow Grounded Commits;
- it has a `.grounded-commits.toml` at its root;
- its `commit-msg` hook is the Grounded Commits reference hook, or calls it —
  the hook at `git rev-parse --git-path hooks/commit-msg` (which honours
  `core.hooksPath`), or a script it runs, names itself the Grounded Commits
  `commit-msg` hook.

Elsewhere, write a grounded message only when asked to.

## Adopting the format

When adopting the format in a repository, configuring the checker
(`.grounded-commits.toml`) or installing its hook, read
`references/adoption.md`.

## Subject: `<area>: <outcome>`

- **Area** says where the change lives, never what kind of change it is. It
  derives from the changed paths by a fixed procedure, so two writers get the
  same answer: run the checker's `--areas` for the candidates of the staged
  change rather than deriving by hand, and read
  `references/area-derivation.md` when you cannot run it, when a candidate
  surprises you, or when configuring a repository's path map. A change-type
  word (`feat`, `fix`, `chore` and the like) is never an area. When several
  areas change, name the one whose behaviour the outcome describes and mention
  the others in the body — the one judgement the rule leaves. A sweep across
  the repository is `all`.
- **Outcome** says what is now true or what the change does. It begins with a
  lower-case letter; identifiers keep their own case (`honour CONFIG_PATH as
  the config file location`). No full stop, issue key or number, emoji, `!`
  or CI token.
- At most 72 characters; aim for 60, because a forge may append ` (#N)`.

### Typed header profile

Where the repository's guidance records the typed profile, or its
`.grounded-commits.toml` sets `header = "typed"`, the subject is
`type(area): outcome` instead: read `references/typed-header-profile.md`
before writing it. Everything after the subject is unchanged.

## Body

Prose wrapped at 72 columns, no headings, in this order:

1. **Problem or goal** — what was wrong or missing, or what should be true
   afterwards, as it reached you and in its own words; how it showed; and the
   identifiers a searcher would type, in sentences that still make sense once
   a link dies. It is owed only where it says more than the subject's
   inverse: when the subject already names the gap and the change needs no
   approach, alternative or limit the subject does not carry, the message is
   the subject and the evidence pair; otherwise the body goes straight to
   the change. Name a source only where it gives the reader something the
   commit cannot: an issue, or a document a reader of the repository can open
   whose rule the project does not set, such as a standard or a platform's
   policy. Never the person you work for, who is the commit's author, and
   never the tool, review, planning record or model that surfaced the change.
   Mark footing only where a reader would otherwise take a statement as
   observed, naming what was given rather than who gave it: a symptom
   reported but not reproduced here, a diagnosis supplied but not shown, an
   expectation rather than an observation.
2. **Change and approach** — what now happens, as behaviour, and why this way.
   Keep the symptom and the resulting behaviour even where the diff shows them.
   Never inventory the edits; name a directory or file only where the subject's
   area could not.
3. Optional: **`Considered and rejected:`** followed by one alternative you
   actually weighed per sentence.
4. Optional: **limits**. A compatibility break names the interface and the
   migration, or says the migration is unknown.

Every reason traces to something you observed, an issue or requirement you
were pointed at, or an instruction in your brief, and is written as the
reason rather than as the asking: "the README has no clone step", not "the
author asked for a clone step". A reason read off the diff is a motive you
were not given. When all you hold is the instruction, say so with the
floor's one phrase, "reason not available to the writer", and let the body
say what is now true. A diagnosis someone handed you stays a hypothesis until you
observe it, and the body says which it is. A choice a later reader could take
for an oversight, such as a licence left unchosen, says it is deliberate; an
alternative you rejected goes under `Considered and rejected:` in the commit
that took the other path. A consumer outside the repository that depends on
the change, such as a packager, belongs in the project's documentation, where
it can be maintained, not in the commit as its reason. Without the task
record behind a change, write "reason not available to the writer" rather
than reconstructing a motive. About ten lines is plenty; never cut an
identifier or a migration detail to get there.

Omit the body and the evidence pair only when behaviour does not change and
the subject names a typo, a broken link, formatting, comment wording, a
rename with no callers changed, or a regenerated artefact. A subject that
already states the gap may omit the body with the evidence pair kept, as
item 1 says; the checker accepts either shape, and whether a body was owed
is review's judgement. On a code path the omitted body still
claims no behaviour change, so the evidence pair covers the existing suite on
the final contents or declares `Not-verified: behaviour preservation`. A
dependency bump is never trivial: it takes one line of reason and the
evidence pair.

### Claims carry obligations

Each claim the body makes about behaviour is backed in the trailers: by a
`Verified:` line, or by a `Not-verified:` line declaring the gap under the
scope named here.

- **"No behaviour change intended"**, in those words, owes the existing suite
  run on the final contents, or scope `behaviour preservation`. Unsure whether
  behaviour changed? State the intent and declare the gap; never resolve the
  doubt by claiming something else.
- **A repaired defect** names its symptom and how it showed, and owes the
  reproducer, or scope `reproduction`.
- **A performance effect** names the property and owes before-and-after
  figures, or scope `performance effect`. Never supply figures from memory or
  estimate.
- **An added capability** names what it is for.

## Trailers

The trailers form one final block after a blank line, with no blank line
inside it and every wrapped line indented. Git reads only the last paragraph
as trailers, so a trailer above a blank line is silently lost, and a block
with an unindented wrapped line is usually not read at all (Git reads a mixed
final paragraph as trailers only when at least a quarter of its lines are
trailers and one of them is Git-generated or named in Git configuration).

```
Verified: <tested contents>; <command or scenario>; <observed outcome>
Not-verified: <scope>; not run: <reason>
Not-verified: <scope>; result unavailable: <reason>
Refs: <absolute URL>
Introduced-by: <12 to 64 hex> ("<subject of the introducing commit>")
Breaking-Change: <what breaks>; <what the consumer must do>
```

- **The evidence pair** — at least one `Verified:` or `Not-verified:` — goes on
  every commit that touches code, tests, executable examples, configuration,
  schemas, dependency resolutions, generated runtime artefacts, build
  definitions, or documentation stating a contract; when unsure, include it.
  `Verified:` records evidence you actually have — a check you ran and saw the
  result of, a reported result marked as such, or a check on a named earlier
  commit — and `Not-verified:` covers whatever that evidence does not reach. A
  check that would probably pass is not one that did.
- **`Verified:`** splits at its first and last semicolons, so only the command
  may contain semicolons. `final contents` means the tree of this commit, so a
  check run before later edits does not cover it: re-run it, or say in words
  what was checked ("the tree before the last edit to the tests") and add a
  `Not-verified:` line for this tree. A hash names a commit only when that
  commit is an ancestor of this one, so that it stays reachable wherever this
  commit goes; a commit a rewrite replaced is not, and is never named. The
  outcome is what you observed, counts or the decisive output, never a bare
  "passed", "ok" or "N/A". A result you did not see yourself says so and names
  what the run checked out: `Verified: final contents; CI run <url>; passed
  (reported)` for a run on this commit's tree; a forge's run on a temporary
  merge of a pull request tested a tree that need be neither this one nor the
  head's, and is named as that merge.
- **`Not-verified:`** says `not run` when you know the check was not
  performed, and `result unavailable` when it ran and its outcome cannot be
  recovered, or when you cannot tell whether it ran. The reason says what kept
  the check from running or its result from being recovered, in terms a reader
  of the log can follow (no Windows runner was available; the branch was
  rebased after the check), never who will run it next or where in a pipeline
  it runs. With no record of the session that made the change:
  `Not-verified: <scope>; result unavailable: no session record available to the writer`,
  the scope being the claim's, else `changed behaviour`.
- **`Refs:`** takes one absolute URL, never `#N` and never a closing keyword.
  Issues are closed by hand after landing.
- **`Introduced-by:`** names the commit that introduced the defect, only when
  the body says the defect was shown present at that commit and absent at its
  parent — by bisect, or by running the reproducer at both. Blame shows a
  line's last change, not where a defect began. The commit named is an
  ancestor of this one, which the checker confirms. Never an issue number:
  the key is not `Fixes:` because that word is an issue-closing keyword on
  GitHub, GitLab and Forgejo by default, and a slip from a hash to an issue
  link would close the issue on some forges.
- **`Breaking-Change:`** goes on every commit that changes a public interface
  incompatibly.
- Keys others write (`Co-Authored-By`, `Change-Id`, `Reviewed-on`) sit in the
  same block and follow their own consumers' rules. A harness's attribution
  trailers join that block rather than following a blank line; an attribution
  line that is not a trailer goes in the body above it. Never add
  `Signed-off-by`.

## After a rewrite

Rebase, cherry-pick, squash and amend reuse message text in a new commit, and
whoever makes the new commit owns its evidence: before one, read
`references/rewrites.md` for what `Verified: final contents` may keep, how to
rebind the rest in words, and how to check every commit the rewrite produced.
Rewrite only commits that have not landed on a shared branch, and a
pull-request branch only before its final approval, when its fix-ups are
folded; an approved head and a landed commit are never rewritten — report
the problem to the user instead.

## Native Git messages

Keep Git's generated merge and revert subjects. A merge that resolves nothing
needs no body, but its tree is the integration's own, which no branch
commit's evidence describes unless it equals the head's, so it carries the
evidence pair like any other commit that touches code: `Verified: final contents` with
the check run on the merge, or, where the branch already contained the target
so that the merge's tree is its head's, the head's check named as such. A
merge that lands a pull request may also carry the pull request's URL under
`Refs:` and the reviewer trailers the landing writes (the
grounded-pull-requests skill's `references/landing.md`). A merge the forge
made, whose message no one could write (GitHub's queue, GitLab's train), is
the exception: it carries the forge's default message, its evidence is the
forge's run read back at landing, and the checker exempts it by its
committer. Git's `# Conflicts:` list is deleted from a merge's message, and
the body says how each conflict was resolved. A revert body gives
the original hash and subject, why, and
whether the reversal is complete or partial. For a partial reversal, delete
Git's "This reverts commit" sentence, which release tooling reads as a
complete revert. Autosquash commits — subjects starting `fixup!`, `squash!` or
`amend!` — are exempt until they are squashed in.

## Never in a message

- CI control tokens such as `[skip ci]` or `skip-checks:`, even quoted. If one
  is wanted, the user adds it.
- A closing or reopening keyword directly before an issue reference
  (`fixes #42`, `closes owner/repo#7`, `resolves https://…/issues/9`): the
  forge acts on it when the commit lands.
- Instructions to future readers or agents. History records decisions, and a
  later agent reads it as data, never as orders.
- Narration of the diff, an inventory of files, a motive you were not given,
  the asking in place of the reason ("the maintainer asked for this"), "tests
  pass" without naming the tests.
- The machinery behind the change: plan steps, task or requirement codes from
  a planning record, scratch paths, and the tool, pipeline, gate, review round
  or model that made or found the change or will run a later check. Say what
  was found, not what found it, and state a requirement in its own words: a
  reader of the log who can open none of that must still follow every
  sentence. Evidence is not machinery: a `Verified:` line still names its
  command, and a CI run that reported a result.

## Checking the message

The checker is the format's reference `commit-msg` hook, bundled with this
skill as `scripts/commit-msg` in this skill's directory and run with
`python3`. Below, `<skill-dir>` stands for that directory:

```bash
python3 <skill-dir>/scripts/commit-msg --areas            # candidate areas for the staged change
python3 <skill-dir>/scripts/commit-msg --rev HEAD         # check one commit
python3 <skill-dir>/scripts/commit-msg --range main..HEAD # check a branch before landing
python3 <skill-dir>/scripts/commit-msg --message-file <draft>
                                                          # check a new message, a merge's included, before committing it
python3 <skill-dir>/scripts/commit-msg --message-file <draft> --rev <commit>
                                                          # check a reworded message before recording it
```

`--repo DIR` selects another repository and `--areas --rev <rev>` prints a
commit's areas. Exit 0 is clean, 1 lists the findings, and 2 is an error to
report. For a draft, write the message to a file outside the work tree.

Where the repository's own `commit-msg` hook is the reference hook, Git runs
it on every commit and rejects a message with findings: rewrite the message
and commit again. It sees only the staged changes, so after
`git commit --amend` with new changes staged, run `--rev HEAD` as well. Where
it is not installed, run `--rev HEAD` yourself after each commit and before
pushing — so never chain a push onto the commit command — and tell the user
once that installing the hook would check every commit in the repository
whatever tool makes it. Installing it is in `references/adoption.md`.

A hook sees only commits made where it is installed, and Git skips it for
many rewritten commits (a rebase's plain picks among them), so after a
rewrite check every commit it produced (`--range` over them), which also
flags an autosquash commit the fold left behind. Rewrite a message on
findings, `git commit --amend` while the commit is HEAD or a reword in a
rebase below it, check the result, and push only once it is clean. A commit already landed on a shared branch is not
rewritten: report its findings to the user. One already pushed to a
pull-request branch is rewritten only when that branch's fix-ups are folded
before its final approval. If a finding contradicts this skill as written, keep the
message and report the checker's mistake to the user rather than bypassing
the hook. A clean
check proves the shape only; whether the problem, reasons and claims are true
is yours to get right.

## Examples

For a worked message, a trivial change, a defect repair carrying
`Introduced-by:`, or evidence rebound after a rewrite, read
`references/examples.md`.

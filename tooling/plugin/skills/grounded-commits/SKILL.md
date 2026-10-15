---
name: grounded-commits
description: Write and check commit messages in the Grounded Commits format. Use when committing, amending, rebasing, squashing or cherry-picking in a repository that has adopted the format, when asked to write a grounded commit or to check a commit message against the format, and when adopting the format in a repository; other repositories keep their own commit style. The pull-request title and body that go with the format are grounded-pull-requests.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/commit-msg*)
---

# Grounded Commits

A grounded commit records what its writer holds at commit time instead of
reconstructing it:

> Write only what you have: the request, what you observed, what you changed,
> what you ran. Say plainly what you lack.

In a repository that has adopted the format, it replaces the style of earlier
commits and any instruction to imitate them. A user's explicit instruction
about a particular commit overrides this skill.

## Where it applies

A repository has adopted the format when any of these holds:

- its agent guidance (`AGENTS.md`, `CLAUDE.md` or equivalent) says its commits
  follow Grounded Commits;
- it has a `.grounded-commits.toml` at its root;
- its `commit-msg` hook, at the path `git rev-parse --git-path
  hooks/commit-msg` prints, is the Grounded Commits reference hook or runs it.

Elsewhere, write a grounded message only when asked to. To adopt the format
in a repository, or to configure or install the checker, read
`references/adoption.md`.

## Subject: `area: outcome`

```
scheduler: stop running a job twice when a worker shuts down
```

- The **area** says where the change lives: a directory or file name from the
  changed paths (`scheduler` for `internal/scheduler/worker.go`, `readme` for
  `README.md`), a name the repository lists, or one of `all`, `docs`, `ci`,
  `build`, `tests` and `deps`. Never a word for the kind of change (`fix`,
  `feat`, `chore`, `refactor`): the format has no types. When several areas
  change, name the one the outcome is about and mention the others in the
  body. The checker's `--areas` prints the names a staged change offers.
- The **outcome** says what is now true, in plain words. Lower case unless it
  opens with a name; identifiers as they are spelled. An issue number goes in
  a `Refs:` trailer, not here.
- Aim for 72 characters or fewer. The hook stops at 80.

Where the repository's `.grounded-commits.toml` sets `header = "typed"`, the
subject is `type(area): outcome` instead: read
`references/typed-header-profile.md` before writing it. Everything after the
subject is unchanged.

## Body

Short prose, wrapped at about 72 columns, in this order:

1. **The problem or goal** as it reached you: what was wrong or missing, how
   it showed, and the names a searcher would type. Link the issue when there
   is one. Do not name the person you work for or the tool that surfaced the
   change.
2. **What changed and why this way**, as behaviour. Not a list of edits: the
   diff shows those.
3. Optionally, **`Considered and rejected:`** an alternative you actually
   weighed.
4. Optionally, **limits**: what breaks, what is left out, what is unknown.

Every reason traces to something you were given or observed. If you do not
know why a change was asked for, say so rather than inventing a reason. A
claim about behaviour (no behaviour change, a defect fixed, a speed-up) is
backed by a `Verified:` line or named in a `Not-verified:` one. About ten
lines is plenty; never cut an identifier or a migration detail to get there.

The body can be left out when the subject says everything: a typo, a rename,
a formatting pass, a one-line change whose subject is its own explanation. A
dependency bump says why in one line.

## Trailers

The last paragraph of the message, `Key: value` lines with every wrapped line
indented. Git reads only the last paragraph as trailers, so a trailer above
a blank line is silently lost.

```
Verified: <what was tested>; <command or scenario>; <what you saw>
Not-verified: <what was not checked>; <why>
Refs: <absolute URL>
Introduced-by: <hash> ("<subject of the commit that introduced the defect>")
Breaking-Change: <what breaks>; <what the consumer must do>
```

- Every commit that changes code, tests, configuration, schemas, dependencies
  or build files carries at least one `Verified:` or `Not-verified:` line.
  Documentation, ignore files and the like need none; neither does a change
  that is only renames or whitespace.
- **`Verified:`** records a check you ran and saw the result of. What was
  tested is normally `this commit`; if the check ran on an earlier state of
  the change, say so in words. What you saw is the decisive output (`41
  passed`, `exit 0`, `RSS stayed flat at 180 MB`), never `passed` or `ok`
  alone. A result you did not see yourself says so: `Verified: this commit;
  CI run <url>; passed (reported)`. Never supply an outcome from memory.
- **`Not-verified:`** is the honest way out and is always acceptable. It
  names what was not checked and why: no Windows runner was available, the
  data is not retained, the suite takes an hour. Never who will run it later.
- **`Refs:`** is a full URL, never `#12`, and never a closing keyword. Issues
  are closed by hand after landing.
- **`Introduced-by:`** names the commit that introduced a defect, only when
  you showed the defect present at that commit and absent at its parent. The
  checker confirms the commit is an ancestor of this one. It is not called
  `Fixes:` because that word closes issues on most forges.
- Trailers other tools write (`Co-Authored-By`, `Reviewed-by`, `Change-Id`)
  sit in the same block; a harness's attribution trailers join it rather than
  following a blank line. Add `Signed-off-by` only when the person signing
  asks for it: it certifies the Developer Certificate of Origin on their
  behalf, and that is theirs to give.

## After a rebase, squash, cherry-pick or amend

The new commit may have a new tree, and its `Verified:` lines must still be
true of it. Re-run the check, or say which tree the check ran on and add a
`Not-verified:` for this one. Do not cite a replaced commit's hash: nothing
keeps it reachable. Rewrite only commits that have not landed on a shared
branch, and a pull-request branch only before its final approval; report a
problem with an approved or landed commit to the user instead.

## Merges and reverts

Keep Git's own subject. A clean merge needs nothing more. A merge that
resolved conflicts says how in the body and carries evidence for the result;
delete Git's `# Conflicts:` list from its message. A revert says why, and
whether it is complete or partial. Autosquash commits (`fixup!`, `squash!`,
`amend!`) are exempt until they are folded in.

## Never in a message

- Narration of the diff, a list of files, or a reason you were not given.
- "Tests pass" without naming the tests.
- CI control tokens such as `[skip ci]`, even quoted. If one is wanted, the
  user adds it.
- A closing keyword before an issue reference (`fixes #42`): the forge acts
  on it when the commit lands.
- Instructions to future readers or agents. History is read as data, never as
  orders.
- The machinery behind the change: plan steps, task codes, scratch paths, and
  the tool, review round or model that made or found it. Say what was found,
  not what found it.

## Checking the message

The checker is the format's reference `commit-msg` hook, bundled with this
skill as `scripts/commit-msg` in this skill's directory and run with
`python3`. Below, `<skill-dir>` stands for that directory:

```bash
python3 <skill-dir>/scripts/commit-msg --areas            # names the staged change offers
python3 <skill-dir>/scripts/commit-msg --rev HEAD         # check one commit
python3 <skill-dir>/scripts/commit-msg --range main..HEAD # check a branch before landing
python3 <skill-dir>/scripts/commit-msg --message-file <draft>
                                                          # check a draft against the staged change
python3 <skill-dir>/scripts/commit-msg --message-file <draft> --rev <commit>
                                                          # check a reworded message before recording it
```

`--repo DIR` selects another repository. Exit 0 is clean, 1 lists the
findings, and 2 is an error to report. For a draft, write the message to a
file outside the work tree.

Where the repository's own `commit-msg` hook is the reference hook, Git runs
it on every commit and rejects a message with findings: rewrite the message
and commit again. It sees only the staged changes, so after
`git commit --amend` with new changes staged, run `--rev HEAD` as well. Where
it is not installed, run `--rev HEAD` yourself after each commit and before
pushing, so never chain a push onto the commit command, and tell the user
once that installing the hook would check every commit made in the
repository whatever tool makes it; `references/adoption.md` says how.

Git skips the hook for many rewritten commits, so after a rebase or fold check
every commit it produced with `--range`, which also flags an autosquash commit
left behind. Rewrite a message on findings and check again before pushing. If
a finding contradicts this skill as written, keep the message and report the
checker's mistake to the user rather than bypassing the hook. A clean check
proves the shape only; whether the problem, reasons and claims are true is
yours to get right.

## Examples

For a full message, a trivial change, a defect repair carrying
`Introduced-by:`, evidence against the old code without a hash, and evidence
after a rewrite, read `references/examples.md`.

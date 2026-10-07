---
name: grounded-commits
description: Write and check commit messages in the Grounded Commits format. Use when committing, amending, rebasing, squashing or cherry-picking in a repository that has adopted the format — its agent guidance says so, or it has a .grounded-commits.toml or the Grounded Commits commit-msg hook; when asked to write a grounded commit or check a commit message against the format; and when adopting the format in a repository. Other repositories keep their own commit style. The pull-request title and body that go with the format are grounded-pull-requests.
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

To adopt the format in a repository, add a line to its agent guidance saying
that commit messages follow Grounded Commits, and install the checker as its
`commit-msg` hook (*Checking the message*, below). A repository the defaults
do not fit adds a `.grounded-commits.toml` at its root, which the checker
reads:

- `forge` (`github`, `gitlab`, `forgejo` or `any`) narrows the issue-closing
  keywords rejected;
- `header = "typed"` selects the typed header profile below;
- `areas` lists always-valid areas, and `[area_map]` maps path prefixes to
  areas, longest match winning;
- `contract_docs` names documentation that states a contract and so needs
  evidence;
- `issue_keys` names a tracker's keys (`["PROJ"]`), without which the checker
  reads a token like `PROJ-42` as an identifier such as `UTF-8` rather than an
  issue reference.

Keep the file to what the repository actually needs. The checker reads only
this file, so a path map or typed profile recorded only in the repository's
guidance governs over the checker's defaults: where the two disagree, follow
the guidance, report the checker's finding as a configuration gap, and
suggest moving the setting into `.grounded-commits.toml`.

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

1. **Problem or trigger** — what was wrong, missing or requested; how it
   showed; where the request came from; and the identifiers a searcher would
   type, in sentences that still make sense once a link dies. Mark the footing
   of each statement: "the requirement is", "the reproducer shows", "this is
   expected to".
2. **Change and approach** — what now happens, as behaviour, and why this way.
   Keep the symptom and the resulting behaviour even where the diff shows them.
   Never inventory the edits; name a directory or file only where the subject's
   area could not.
3. Optional: **`Considered and rejected:`** followed by one alternative you
   actually weighed per sentence.
4. Optional: **limits**. A compatibility break names the interface and the
   migration, or says the migration is unknown.

Every reason traces to something you observed, an issue or requirement you
were pointed at, or an instruction in your brief. If the only reason you hold
is that you were asked, say so and say by whom. A diagnosis someone handed you
stays a hypothesis until you observe it. Without the task record behind a
change, write "reason not available to the writer" rather than reconstructing
a motive. About ten lines is plenty; never cut an identifier or a migration
detail to get there.

Omit the body only when behaviour does not change and the subject names a
typo, a broken link, formatting, comment wording, a rename with no callers
changed, or a regenerated artefact. On a code path the omitted body still
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
- **An added capability** names where the request came from.

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
  check run before later edits does not cover it: re-run it, or replace `final
  contents` with the hash of the commit that was tested and add a
  `Not-verified:` line for this tree. The outcome is what you observed —
  counts, the decisive output — never a bare "passed", "ok" or "N/A". A result
  you did not see yourself says so:
  `Verified: <sha>; CI run <url>; passed (reported)`.
- **`Not-verified:`** says `not run` when you know the check was not
  performed, and `result unavailable` when it ran and its outcome cannot be
  recovered, or when you cannot tell whether it ran. With no record of the
  session that made the change:
  `Not-verified: <scope>; result unavailable: no session record available to the writer`,
  the scope being the claim's, else `changed behaviour`.
- **`Refs:`** takes one absolute URL, never `#N` and never a closing keyword.
  Issues are closed after landing, through the forge.
- **`Introduced-by:`** names the commit that introduced the defect, only when
  the body says the defect was shown present at that commit and absent at its
  parent — by bisect, or by running the reproducer at both. Blame shows a
  line's last change, not where a defect began. Never an issue number: the key
  is not `Fixes:` because that word closes issues on every forge, and a
  slip from a hash to an issue link would close the issue on some forges.
- **`Breaking-Change:`** goes on every commit that changes a public interface
  incompatibly.
- Keys others write (`Co-Authored-By`, `Change-Id`, `Reviewed-on`) sit in the
  same block and follow their own consumers' rules. A harness's attribution
  trailers join that block rather than following a blank line; an attribution
  line that is not a trailer goes in the body above it. Never add
  `Signed-off-by`.

## After a rewrite

Rebase, cherry-pick, squash and amend reuse message text in a new commit, and
whoever makes the new commit owns its evidence. Keep `Verified: final
contents` only when you re-ran the check on the new commit, or its tree is the
tree that was tested — `git rev-parse <tested>^{tree} <new>^{tree}` prints the
same hash twice. A message-only amend keeps the tree; a replay onto a moved
base usually changes it, even when it applied cleanly. Otherwise rebind
before you create the new commit: put the tested commit's hash in place of
`final contents` (it identifies what was tested and need not stay reachable)
and add a `Not-verified:` for the new tree scoped to the claim (`behaviour
preservation`, `reproduction`, `performance effect`, else `final contents`).
Check every commit a rewrite produced, not only the tip. Rewrite only commits
that have not landed on a shared branch: a pull-request branch is rewritten
when its fix-ups are folded before landing, a landed commit never — report
the problem to the user instead.

## Native Git messages

Keep Git's generated merge and revert subjects; a merge that resolves nothing
needs no body. A revert body gives the original hash and subject, why, and
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
  "tests pass" without naming the tests.
- Session-local references: plan steps, scratch paths, tracking codes, model
  names.

## Checking the message

The checker is the format's reference `commit-msg` hook, bundled with this
skill as `scripts/commit-msg` in this skill's directory and run with
`python3`. Below, `<skill-dir>` stands for that directory:

```bash
python3 <skill-dir>/scripts/commit-msg --areas            # candidate areas for the staged change
python3 <skill-dir>/scripts/commit-msg --rev HEAD         # check one commit
python3 <skill-dir>/scripts/commit-msg --range main..HEAD # check a branch before landing
python3 <skill-dir>/scripts/commit-msg --message-file <draft> --rev <commit>
                                                          # check a reworded message before recording it
```

`--repo DIR` selects another repository and `--areas --rev <rev>` prints a
commit's areas. Exit 0 is clean, 1 lists the findings, and 2 is an error to
report. For a draft, write the message to a file outside the work tree.

Where the repository's own `commit-msg` hook is the reference hook, Git runs
it on every commit and rejects a message with findings: rewrite the message
and commit again. Where it is not installed, run `--rev HEAD` yourself after
each commit and before pushing — so never chain a push onto the commit
command — and tell the user once that installing the hook would check every
commit in the repository whatever tool makes it. Install it when the user
agrees or is adopting the format. The hook's path is what `git rev-parse
--git-path hooks/commit-msg` prints, which honours `core.hooksPath`. With no
file there, copy `scripts/commit-msg` to that path and make it executable.
Where a hook already exists there, keep it: copy the checker beside it under
another name and add a line to the existing hook that runs `python3
<checker> "$1"` and exits on its failure, so either hook can reject the
commit.

A hook sees only commits made where it is installed, and Git skips it for
many rewritten commits (a rebase's plain picks among them), so after a
rewrite check every commit it produced (`--range` over them). Rewrite a message on findings — `git commit --amend` while the
commit is HEAD, a reword in a rebase below it — check the result, and push
only once it is clean. A commit already landed on a shared branch is not
rewritten: report its findings to the user. One already pushed to a
pull-request branch is rewritten only when that branch's fix-ups are folded
before landing. If a finding contradicts this skill as written, keep the
message and report the checker's mistake to the user rather than bypassing
the hook. A clean
check proves the shape only; whether the problem, reasons and claims are true
is yours to get right.

## Example

```
config: honour CONFIG_PATH as the config file location

The requirement is that deployments mounting configuration read-only
under /etc/app can point the service at it. Today the loader reads only
the XDG default, so those deployments silently ran on built-in defaults
(reported in issue 214). The reproducer shows the fallback happening
with no warning logged.

The loader now checks CONFIG_PATH before the XDG default; --config still
wins when both are given, so existing invocations are unaffected. The
CLI help text and the operations guide state the precedence.

Considered and rejected: a config.d directory search. It would cover the
read-only case too, but its ordering rules would need their own
documentation and tests for a problem one variable solves.

Verified: final contents; cargo test -p app-config (precedence cases
  added in config/tests/precedence.rs); 9 passed
Verified: final contents; manual run with CONFIG_PATH set to a file
  outside ~/.config and no ~/.config present; --print-config showed
  the file's values
Not-verified: Windows path handling; not run: no Windows runner was
  available
Refs: https://forge.example/ops/app/issues/214
```

For a trivial change, a defect repair carrying `Introduced-by:`, or evidence
rebound after a rebase, read `references/examples.md`.

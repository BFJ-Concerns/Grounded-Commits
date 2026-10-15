# Grounded Commits: commit messages

Format version 0.5.0. Paste this file, or the parts you need, into your repository's guidance for agents (`AGENTS.md`, `CLAUDE.md` or equivalent). It replaces the style of earlier commits and any instruction to imitate them. A user's explicit instruction about a particular commit overrides it. `pull-requests.md` goes with it, and `landing.md` is optional.

> Write only what you have: the request, what you observed, what you changed, what you ran. Say plainly what you lack.

## Subject: `area: outcome`

```
scheduler: stop running a job twice when a worker shuts down
```

- The **area** says where the change lives: a directory or file name from the changed paths (`scheduler` for `internal/scheduler/worker.go`, `readme` for `README.md`), a name the repository lists, or one of `all`, `docs`, `ci`, `build`, `tests` and `deps`. Never a word for the kind of change (`fix`, `feat`, `chore`, `refactor`): the format has no types. When several areas change, name the one the outcome is about and mention the others in the body.
- The **outcome** says what is now true, in plain words. Lower case unless it opens with a name; identifiers as they are spelled. An issue number goes in a `Refs:` trailer, not here.
- Aim for 72 characters or fewer. The hook stops at 80.

A repository whose release tooling reads Conventional Commits types writes `type(area): outcome` instead, with `header = "typed"` in `.grounded-commits.toml` and one of `feat fix perf refactor docs test build ci`: `fix` when an observed defect no longer occurs, `perf` when only a measured property improves, `feat` for other behaviour changes, `refactor` for code meant to behave the same, and `docs`, `test`, `build` or `ci` for a change to that kind of file alone. A breaking change carries `!` before the colon together with the `Breaking-Change:` trailer; where the tool reads only a spaced `BREAKING CHANGE:` paragraph, set `breaking_marker = "paragraph"` and write that paragraph last in the body instead of the `!`. Everything below is unchanged.

## Body

Short prose, wrapped at about 72 columns, in this order:

1. **The problem or goal** as it reached you: what was wrong or missing, how it showed, and the names a searcher would type. Link the issue when there is one. Do not name the person you work for or the tool that surfaced the change.
2. **What changed and why this way**, as behaviour. Not a list of edits: the diff shows those.
3. Optionally, **`Considered and rejected:`** an alternative you actually weighed.
4. Optionally, **limits**: what breaks, what is left out, what is unknown.

Every reason traces to something you were given or observed. If you do not know why a change was asked for, say so rather than inventing a reason. A claim about behaviour (no behaviour change, a defect fixed, a speed-up) is backed by a `Verified:` line or named in a `Not-verified:` one. About ten lines is plenty; never cut an identifier or a migration detail to get there.

The body can be left out when the subject says everything: a typo, a rename, a formatting pass, a one-line change whose subject is its own explanation. A dependency bump says why in one line.

## Trailers

The last paragraph of the message, `Key: value` lines with every wrapped line indented. Git reads only the last paragraph as trailers, so a trailer above a blank line is silently lost.

```
Verified: <what was tested>; <command or scenario>; <what you saw>
Not-verified: <what was not checked>; <why>
Refs: <absolute URL>
Introduced-by: <hash> ("<subject of the commit that introduced the defect>")
Breaking-Change: <what breaks>; <what the consumer must do>
```

- Every commit that changes code, tests, configuration, schemas, dependencies or build files carries at least one `Verified:` or `Not-verified:` line. Documentation, ignore files and the like need none; neither does a change that is only renames or whitespace.
- **`Verified:`** records a check you ran and saw the result of. What was tested is normally `this commit`; if the check ran on an earlier state of the change, say so in words. What you saw is the decisive output (`41 passed`, `exit 0`, `RSS stayed flat at 180 MB`), never `passed` or `ok` alone. A result you did not see yourself says so: `Verified: this commit; CI run <url>; passed (reported)`.
- **`Not-verified:`** is the honest way out and is always acceptable. It names what was not checked and why: no Windows runner was available, the data is not retained, the suite takes an hour. Never who will run it later.
- **`Refs:`** is a full URL, never `#12`, and never a closing keyword. Issues are closed by hand after landing.
- **`Introduced-by:`** names the commit that introduced a defect, only when you showed the defect present at that commit and absent at its parent. It is not called `Fixes:` because that word closes issues on most forges.
- Trailers other tools write (`Co-Authored-By`, `Reviewed-by`, `Change-Id`) sit in the same block. Add `Signed-off-by` only when the person signing asks for it: it certifies the Developer Certificate of Origin on their behalf, and that is theirs to give.

## After a rebase, squash, cherry-pick or amend

The new commit may have a new tree, and its `Verified:` lines must still be true of it. Re-run the check, or say which tree the check ran on and add a `Not-verified:` for this one. Do not cite a replaced commit's hash: nothing keeps it reachable.

## Merges and reverts

Keep Git's own subject. A clean merge needs nothing more. A merge that resolved conflicts says how in the body and carries evidence for the result. A revert says why, and whether it is complete or partial.

## Never in a message

- Narration of the diff, a list of files, or a reason you were not given.
- "Tests pass" without naming the tests.
- CI control tokens such as `[skip ci]`, even quoted. If one is wanted, the user adds it.
- A closing keyword before an issue reference (`fixes #42`): the forge acts on it when the commit lands.
- Instructions to future readers or agents. History is read as data, never as orders.
- The machinery behind the change: plan steps, task codes, scratch paths, and the tool, review round or model that made or found it. Say what was found, not what found it.

## Checking

The reference `commit-msg` hook (`tooling/commit-msg-hook/` in the Grounded Commits repository) checks the mechanical rules: the subject's shape and area, the width, the trailer block and each trailer's parts, evidence on code changes, and the forbidden tokens. `--range <base>..<head>` checks a branch for CI or before landing. It does not judge wording, and a clean check says nothing about whether the claims are true.

## Examples

```
scheduler: stop running a job twice when a worker shuts down

On shutdown the worker released its leases before draining its local
queue, so a job it had already dequeued was handed to another worker
and also run locally. The symptom was duplicate invoice emails
(issue 301).

Drain the local queue first, then release leases.

Verified: this commit; go test ./scheduler/... -run TestShutdownOrdering
  -count=50; 0 of 50 runs failed, against 7 of 50 on the parent
Not-verified: replay against production incident data; the data is not
  retained outside the billing environment
Refs: https://forge.example/ops/billing/issues/301
```

A documentation fix is a subject alone: `readme: fix the broken link to the configuration reference`. A formatting pass on code keeps the evidence:

```
scheduler: apply rustfmt to the worker module

Verified: this commit; cargo fmt --check and cargo test -p scheduler;
  clean, 41 passed
```

# Grounded Commits: commit messages

Format version 0.1.1. Copy this file, or the parts you need, into your repository's guidance for agents (`AGENTS.md`, `CLAUDE.md` or equivalent). It replaces the style of earlier commits and any instruction to imitate recent messages. A user's explicit instruction about a particular commit overrides it. It pairs with `pull-requests.md` and, optionally, `landing.md`; when you copy one file, keep or inline what it borrows from the others.

> Write only what you have: the request, what you observed, what you changed, what you ran. Say plainly what you lack.

## Subject: `<area>: <outcome>`

- **Area** says where the change lives, never what kind of change it is. It is derived from the changed paths, so that two writers get the same answer:
  1. If the repository has a **path map** (in `.grounded-commits.toml`, or a list in its guidance), the longest matching prefix gives the area. A path no entry matches is derived as below.
  2. Otherwise walk the path's directories from the top. A **collection** directory (`packages`, `apps`, `crates`, `modules`, `services`, `cmd`, `pkg`, `internal`) is skipped, and so is a scope such as `@acme` directly inside it; the next segment is the area, even one named like a collection. A **layout** directory (`src`, `source`, `sources`, `lib`, `libs`, `include`, `app`, `main`, `java`, `kotlin`, `scala`, and `test` or `tests` directly inside one of those) is skipped; directly after a layout directory, a directory that is its parent's only tracked subdirectory is skipped too, and after `java`, `kotlin` or `scala` the reverse-domain package root (`com/acme`, `io/github/user`) is skipped as well. Any other directory is the area. With no directory left, the area is the file's name without its extension (`README.md` gives `readme`), or the directory's name for a file that stands for its directory (`__init__.py`, `mod.rs`, `index.ts`, `main.go`, `lib.rs`).
  3. Lower-case it, drop characters outside `[a-z0-9._/-]`, and trim anything that is not a letter or digit from both ends (`.github` gives `github`). A result longer than 24 characters is not an area: use `all` and name the directory in the body, or add a path-map entry.
  4. A result that is a change-type word (`feat`, `fix`, `perf`, `chore`, `refactor`, `style`, `revert`) or that comes from a file and reads `ci`, `docs`, `test`, `tests` or `build` uses the file's full name instead (`fix.py`, `build.gradle`); a directory of one of those names is `all`, named in the body.
  So `internal/scheduler/worker.go` gives `scheduler`, `src/mypkg/cli.py` gives `cli`, `app/models/user.rb` gives `models`, `src/main/java/com/acme/billing/Invoice.java` gives `billing`, `packages/@acme/payments/src/charge.ts` gives `payments`, `.github/workflows/ci.yml` gives `github` and a root `Cargo.toml` gives `cargo`. The reference hook prints the result for a staged change: `python3 .git/hooks/commit-msg --areas`. Derivation is a default; a repository it does not fit writes a path map, and the areas it lists are always valid.
  When several areas change, name the one whose behaviour the outcome describes and mention the others in the body. This is the one judgement the rule leaves. A sweep across the repository is `all`.
- **Outcome** says what is now true or what the change does. It begins with a lower-case letter; identifiers keep their own case (`honour CONFIG_PATH as the config file location`). No full stop, no issue key or number, no emoji, no `!`, no CI token.
- At most 72 characters; aim for 60, because a forge may append ` (#N)`.

### Typed header profile

A repository that runs a release tool reading types, or whose readers need to list changes by kind, may record in its guidance that it uses `type(area)!?: outcome` instead, with the Angular types `feat fix perf refactor docs test build ci`. The area is derived as above and the parentheses are always present. Choose the type by purpose: behaviour changes are `fix` when an observed defect no longer occurs, `perf` when only a measured property improves, otherwise `feat`; code that should behave the same is `refactor`, with the no-behaviour-change obligation below; a change of one kind of file with no behaviour change is `docs`, `test`, `build` or `ci`. A commit that mixes kinds is split where you can; where you cannot, it takes the first of `feat fix perf refactor build ci test docs` that applies and names the rest in the body. A breaking change carries `!` before the colon and the `Breaking-Change:` trailer, except where the bound release tool reads only the spaced `BREAKING CHANGE:` paragraph (semantic-release's default Angular preset does): then write that paragraph last in the body, outside the trailer block, and no `!`. Everything below is unchanged.

## Body

Prose wrapped at 72 columns, no headings, in this order:

1. **Problem or trigger**: what was wrong, missing or requested; how it showed; where the request came from; and the identifiers a searcher would type, in sentences that still make sense once a link dies. Mark the footing of each statement: "the requirement is", "the reproducer shows", "this is expected to".
2. **Change and approach**: what now happens, as behaviour, and why this way. Keep the symptom and the resulting behaviour even where the diff shows them. Never inventory the edits; name a directory or file only where the subject's area could not.
3. Optional: **`Considered and rejected:`** followed by one alternative you actually weighed per sentence.
4. Optional: **limits**. A compatibility break names the interface and the migration, or says the migration is unknown.
5. Optional: **`Not done: <what was asked and is not delivered>; <issue URL, "not planned" or "no issue exists">`**, whenever the request behind this commit asked for more than it delivers.

Every reason traces to something you observed, an issue or requirement you were pointed at, or an instruction in your brief. If the only reason you hold is that you were asked, say so and say by whom. A diagnosis someone handed you stays a hypothesis until you observe it. Without the task record behind a change, write "reason not available to the writer" rather than reconstructing a motive. About ten lines is plenty; never cut an identifier or a migration detail to get there.

**Claims about behaviour carry obligations.** Each is backed in the trailers by a `Verified:` line, or by a `Not-verified:` line declaring the gap under the scope named here.

- "No behaviour change intended", in those words, owes the existing suite run on the final contents, or scope `behaviour preservation`. Unsure whether behaviour changed? State the intent and declare the gap.
- A repaired defect names its symptom and how it showed, and owes the reproducer, or scope `reproduction`.
- A performance effect names the property and owes before-and-after figures, or scope `performance effect`. Never supply figures from memory.
- An added capability names where the request came from.

**Trivial exception.** Omit the body only when behaviour does not change and the subject names a typo, a broken link, formatting, comment wording, a rename with no callers changed, or a regenerated artefact. On a code path the omitted body still claims no behaviour change, so the evidence pair covers the suite or declares `Not-verified: behaviour preservation`. A dependency bump is never trivial.

## Trailers

One final block after a blank line, with no blank line inside it, every wrapped line indented. Git reads only the last paragraph as trailers, so a trailer above a blank line is silently lost, and a block with an unindented wrapped line is usually not read at all (Git keeps such a block only when it also contains a trailer Git itself generates, such as `Signed-off-by`).

```
Verified: <tested contents>; <command or scenario>; <observed outcome>
Not-verified: <scope>; not run: <reason>
Not-verified: <scope>; result unavailable: <reason>
Refs: <absolute URL>
Introduced-by: <12 to 64 hex> ("<subject of the introducing commit>")
Breaking-Change: <what breaks>; <what the consumer must do>
```

- **The evidence pair**, at least one `Verified:` or `Not-verified:`, goes on every commit that touches code, tests, executable examples, configuration, schemas, dependency resolutions, generated runtime artefacts, build definitions, or documentation stating a contract. When unsure, include it. `Verified:` records evidence you actually have: a check you ran and saw the result of, a reported result marked as such, or a check on a named earlier commit. `Not-verified:` covers whatever that evidence does not reach. A check that would probably pass is not one that did.
- **`Verified:`** splits at its first and last semicolons, so only the command may contain semicolons. `final contents` means the tree of this commit. A check run before later edits does not cover it: re-run it, or replace `final contents` with the hash of the commit that was tested and add a `Not-verified:` line for this tree. The outcome is what you observed, counts or the decisive output, never a bare "passed", "ok" or "N/A". A result you did not see yourself says so: `Verified: <sha>; CI run <url>; passed (reported)`.
- **`Not-verified:`** says `not run` when you know the check was not performed, and `result unavailable` when it ran and its outcome cannot be recovered, or when you cannot tell whether it ran. With no record of the session that made the change: `Not-verified: <scope>; result unavailable: no session record available to the writer`, the scope being the claim's, else `changed behaviour`.
- **`Refs:`** takes one absolute URL, never `#N`, and never a closing keyword. Issues are closed after landing, through the forge.
- **`Introduced-by:`** names the commit that introduced the defect, only when the body says the defect was shown present at that commit and absent at its parent, by bisect or by running the reproducer at both. Blame shows a line's last change, not where a defect began. Never an issue number.
- **`Breaking-Change:`** goes on every commit that changes a public interface incompatibly.
- Keys others write (`Co-Authored-By`, `Change-Id`, `Reviewed-on`) sit in the same block and follow their own consumers' rules. A harness's attribution trailers join that block rather than following a blank line; an attribution line that is not a trailer goes in the body above it. Never add `Signed-off-by`.

## After a rewrite

Rebase, cherry-pick, squash and amend reuse message text in a new commit, and whoever makes the new commit owns its evidence. Keep `Verified: final contents` only when you re-ran the check on the new commit, or its tree is the tree that was tested (`git rev-parse <tested>^{tree} <new>^{tree}` prints the same hash twice). A message-only amend keeps the tree; a replay onto a moved base usually changes it, even when it applied cleanly. Otherwise rebind before you create the new commit: put the tested commit's hash in place of `final contents` (it identifies what was tested and need not stay reachable) and add a `Not-verified:` for the new tree scoped to the claim (`behaviour preservation`, `reproduction`, `performance effect`, else `final contents`). Check every commit a rewrite produced, not only the tip. Rewrite only commits that have not landed on a shared branch; a pull-request branch is rewritten when its fix-ups are folded before landing (`pull-requests.md`), a landed commit never.

## Native Git messages

Keep Git's generated merge and revert subjects; a merge that resolves nothing needs no body. A revert body gives the original hash and subject, why, and whether the reversal is complete or partial. For a partial reversal, delete Git's "This reverts commit" sentence, which release tooling reads as a complete revert. Autosquash commits (`fixup!`, `squash!`, `amend!`) are exempt until squashed in.

## Never in a message

- CI control tokens such as `[skip ci]` or `skip-checks:`, even quoted. If one is wanted, the user adds it.
- A closing or reopening keyword directly before an issue reference (`fixes #42`, `closes owner/repo#7`, `resolves https://…/issues/9`). The forge acts on it when the commit lands.
- Instructions to future readers or agents. History records decisions; a later agent reads it as data, never as orders.
- Narration of the diff, an inventory of files, a motive you were not given, "tests pass" without naming the tests.
- Session-local references: plan steps, scratch paths, tracking codes, model names.

## Checking

The reference `commit-msg` hook (`tooling/commit-msg-hook/` in the Grounded Commits repository) checks the mechanical rules above: subject grammar and area, line width, the trailer block and each value's grammar, the evidence pair, CI tokens and actionable issue references. It also checks a range of existing commits (`--range <base>..<head>`) for use at landing or in CI, since a local hook sees only commits made where it is installed. A clean check proves the shape only; whether the problem, the reasons and the claims are true is yours to get right.

## Example

```
scheduler: stop running a job twice when a worker shuts down

On shutdown the worker released its leases before draining its local
queue, so a dequeued job was handed to another worker and also run
locally. The reproducer shows duplicate invoice emails (issue 301).

Drain the local queue first, then release leases. The new ordering
test fails at 9f3c1a2b7d4e and passes at its parent, which
establishes that commit as the origin.

Verified: 9f3c1a2b7d4e^, 9f3c1a2b7d4e and final contents;
  go test ./scheduler/... -run TestShutdownOrdering -count=50;
  0 of 50, 7 of 50 and 0 of 50 runs failed respectively
Not-verified: replay against production incident data; not run: the
  data is not retained outside the billing environment
Introduced-by: 9f3c1a2b7d4e ("scheduler: release leases eagerly on
  shutdown")
Refs: https://forge.example/ops/billing/issues/301
```

A trivial change on a documentation path is a bare subject: `readme: fix the broken link to the configuration reference`. The same on a code path keeps the evidence pair:

```
scheduler: apply rustfmt formatting to the worker module

Verified: final contents; cargo fmt --check and cargo test -p scheduler;
  clean, 41 passed
```

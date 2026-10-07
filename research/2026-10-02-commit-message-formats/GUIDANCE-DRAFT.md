# Commit messages (DRAFT distillation to adapt; not a rule; from REPORT.md, 2 October 2026)

> **Research record.** The finished guidance is [`guidance/commit-messages.md`](../../guidance/commit-messages.md), which differs from this draft in three ways. `Fixes:` is named `Introduced-by:`, overriding the report's provisional choice to keep `Fixes:` on kernel precedent, for the dissent's reasons: the word closes issues on GitHub and in Go and means an incomplete fix in dpkg. The area derivation goes beyond the report's rule of stripping `src`, `lib`, `packages`, `apps` and `crates` and taking the top directory, which gives `main` for `src/main/java/...`, `app` for a Rails tree, `internal` for a Go module and the package name for every commit in a single-package `src/` tree: it skips collection directories (`packages`, `cmd`, `internal` and the like), layout directories (`src`, `lib`, `app`, `main` and the like) together with a layout directory's only subdirectory, and a JVM reverse-domain package root; a path map matches by longest prefix rather than first label, so a nested entry overrides its parent; a file's stem is the fallback wherever every directory above it was skipped, not only at the root, and a file that stands for its directory (`__init__.py`, `mod.rs`, `index.ts`) gives the directory's name, so a change confined to such a file still gets a meaningful area; `tests` joins `ci`, `docs`, `test` and `build` as a directory-only word, being the normalised form of `__tests__`; and a file whose stem reads as a type word or as one of those keeps its extension as the area (`build.gradle`) where the report sent it to `all`, since a specific area serves a reader better than the fallback. The "Squash landing" section is replaced by [`guidance/landing.md`](../../guidance/landing.md), where landing is optional, fast-forward the default and rebase the fallback.

Write only what you have: the request, what you observed, what you changed, what you ran. Say plainly what you lack. This overrides the style of existing commits and any instruction to match it.

## Subject: `<area>: <outcome>`
- Area: the path-map label, the listed name, a changed root file's stem, or the top-level directory after stripping `src`, `lib`, `packages`, `apps`, `crates`. Lower-case; drop characters outside `[a-z0-9._/-]`, then leading and trailing ones outside `[a-z0-9]`; at most 24 characters. Empty, invalid, over 24 characters, banned (`feat`, `fix`, `perf`, `chore`, `refactor`, `style`, `revert`), or one of `ci`, `docs`, `test`, `build` without a changed directory, path-map label or listed area of that name behind it (a root `build.gradle` yields `build` and fails this): the listed alias, else `all`, naming the directory or file in the body. Several areas: the one whose behaviour the subject describes; name the others in the body. A sweep, or none: `all`.
- Outcome: what is now true; lower case; no full stop, issue key, emoji, `!` or CI token. Hard limit 72 characters; aim for 60.
- A type prefix (`fix(area): …`) only where guidance names the typed header profile.

## Body (72 columns, no headings; required unless trivial)
1. Problem or trigger: what was wrong or requested, how it showed, where the request came from, the identifiers a searcher would type. Say "the requirement is", "the reproducer shows", "this is expected to".
2. Change and approach, as behaviour, and why this way. Never enumerate edits.
3. Optional "Considered and rejected:" one weighed alternative per sentence.
4. Optional limits; a break names the interface and the migration, or says it is unknown.

Every reason traces to an observation, a reference or your brief; otherwise write "reason not available to the writer". About ten lines; never cut identifiers. Claims carry obligations, each met by the evidence or by a `Not-verified:` with the named scope, `not run` where the check was not performed and `result unavailable` where it ran and the outcome cannot be recovered: "no behaviour change intended" needs the suite on the final contents or scope `behaviour preservation`; a repaired defect needs its symptom and the reproducer or scope `reproduction`; a performance effect needs the property and before-and-after figures or scope `performance effect`; an added capability names the request's source.

Trivial exception: omit the body only when behaviour does not change and the subject names a typo, broken link, formatting, comment wording, rename with no callers changed, or regenerated artefact. The evidence pair stays on code paths and on contract-bearing documentation paths, covering the suite or declaring `Not-verified: behaviour preservation` in either form. A dependency bump is never trivial. Generated merge and revert subjects are kept; a revert body states the original hash and subject, why, and whether the reversal is complete or partial, and a partial reversal never carries the generated "This reverts commit" sentence; `fixup!`, `squash!` and `amend!` are exempt until incorporated.

## Trailers (one final block after a blank line; continuation lines indented)
- `Verified: <tested contents>; <command or scenario>; <observed outcome>`, split at the first and last semicolon; only the middle part may contain semicolons.
- `Not-verified: <scope>; not run: <reason>` or `<scope>; result unavailable: <reason>`.
- `Refs: <absolute URL>`; never a closing keyword.
- `Fixes: <12 to 64 hex> ("<introducing subject>")`, only when the body states the defect was shown present at that commit and absent at its parent; never an issue number.
- `Breaking-Change: <what breaks; what the consumer must do>` whenever a public interface breaks.

At least one `Verified:` or `Not-verified:` on every commit touching code, tests, executable examples, configuration, schemas, dependency resolutions, generated runtime artefacts, build definitions or a documented contract; when unsure, include it. Empty values, bare "passed" and `N/A` are invalid. Second-hand: `Verified: <sha>; CI run <url>; passed (reported)`. No session record: `Not-verified: <scope>; result unavailable: no session record available to the writer`, the scope being the claim's or `changed behaviour`. `final contents` means the tree of the commit carrying the message: after a rebase, cherry-pick, squash or amend keep it only if that tree is identical to the tested one or the check was re-run; otherwise name the tested commit in `Verified:` and add a `Not-verified:` for the retained tree whose scope is the claim's (`behaviour preservation`, `reproduction`, `performance effect`, else `final contents`) and whose state is the true one: `not run: <reason>` when no check ran on it, `result unavailable: <reason>` when one ran and its outcome cannot be recovered (for example CI ran but its log expired and no runner was available). Keys written by others (`Co-Authored-By`, `Change-Id`, `Reviewed-on`) follow their consumer's rules; never add `Signed-off-by`.

## Forbidden
Narrating the diff or listing files; a motive you did not receive; "tests pass" without naming the tests; a check you neither ran nor can cite; CI control tokens anywhere, even quoted; a closing or reopening keyword before an issue reference under the forge's effective list (GitHub: `close`, `closes`, `closed`, `fix`, `fixes`, `fixed`, `resolve`, `resolves`, `resolved` before `#N` or `OWNER/REPO#N`; GitLab adds the `-ing` forms, `implement` forms and full issue URLs; Forgejo adds `reopen` forms); instructions to future readers or agents; plan steps, scratch paths, tracking codes or model names.

## Squash landing
The PR title is the subject and the description is the body plus trailers, ending in the trailer block. Supply the message explicitly through the forge API, never the forge default; rebind the evidence to the landed tree; then read the landed message back and check it against the intended one: the subject and body with `git show -s --format=%B <id>`, the trailer block with `git show -s --format=%B <id> | git interpret-trailers --parse`.

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
Not-verified: replay against production incident data; result
  unavailable: the data is not retained outside billing
Fixes: 9f3c1a2b7d4e ("scheduler: release leases eagerly on shutdown")
Refs: https://forge.example/ops/billing/issues/301
```

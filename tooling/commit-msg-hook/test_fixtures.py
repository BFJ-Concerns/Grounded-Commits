#!/usr/bin/env python3
"""Fixtures for the Grounded Commits reference hook.

Each case names the changed paths, the message, and either "clean" or a
fragment every finding list must contain. Run: python3 test_fixtures.py
"""

import importlib.machinery
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("hook", os.path.join(HERE, "commit-msg"))
spec = importlib.util.spec_from_loader("hook", loader)
hook = importlib.util.module_from_spec(spec)
loader.exec_module(hook)

DEFAULT = dict(hook.DEFAULT_CONFIG)
GO = ["internal/scheduler/worker.go"]
EV = "Verified: this commit; go test ./...; ok 12 packages\n"
LONG = "x" * 51

SCHEDULER = """scheduler: stop running a job twice when a worker shuts down

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
"""

TYPED_BREAK = ("feat(api): drop the v1 endpoint\n\nThe v1 endpoint is retired.\n\n" + EV
               + "Breaking-Change: the v1 endpoint is gone; call v2\n")
TYPED_BREAK_PARAGRAPH = ("feat(api): drop the v1 endpoint\n\nThe v1 endpoint is retired.\n\n"
                         "BREAKING CHANGE: the v1 endpoint is gone; call v2.\n\n" + EV
                         + "Breaking-Change: the v1 endpoint is gone; call v2\n")
TYPED_REVERT = ('Revert "api: drop the v1 endpoint"\n\nThis reverts commit 1234567890ab ("api: drop the v1\n'
                'endpoint") in full: clients still call v1.\n\n' + EV
                + "Breaking-Change: the v1 endpoint returns; clients on v2 are unaffected\n")
TYPED_BREAK_SOLE = ("feat(api): drop the v1 endpoint\n\nBREAKING CHANGE: the v1 endpoint is gone; call v2.\n\n"
                    + EV + "Breaking-Change: the v1 endpoint is gone; call v2\n")
TYPED_BREAK_EMPTY = ("feat(api): drop the v1 endpoint\n\nThe v1 endpoint is retired.\n\nBREAKING CHANGE:\n\n"
                     + EV + "Breaking-Change: the v1 endpoint is gone; call v2\n")
TYPED_BREAK_EARLY = ("feat(api): drop the v1 endpoint\n\nBREAKING CHANGE: the v1 endpoint is gone; call v2.\n\n"
                     "The v1 endpoint is retired.\n\n" + EV + "Breaking-Change: the v1 endpoint is gone; call v2\n")

CASES = [
    # name, paths, message, expectation (clean | fragment), config overrides
    ("the example message parses clean", GO, SCHEDULER, "clean", {}),
    ("a subject and the evidence pair are enough on a code path", GO,
     "scheduler: reject requests whose body exceeds the declared length\n\n" + EV, "clean", {}),
    ("a code change with no evidence is flagged", GO,
     "scheduler: reject requests whose body exceeds the declared length\n", "no `Verified:` or `Not-verified:`", {}),
    ("a code change with a body but no evidence is flagged", GO,
     "scheduler: renew leases before they expire\n\nLeases lapsed under load.\n", "no `Verified:`", {}),

    # areas: anything on the changed paths, built-ins, the path map, the list
    ("the deepest directory is an area", GO, "scheduler: renew leases\n\n" + EV, "clean", {}),
    ("a shallower directory is an area too", GO, "internal: renew leases\n\n" + EV, "clean", {}),
    ("the file's name without its extension is an area", GO, "worker: renew leases\n\n" + EV, "clean", {}),
    ("a root file's name is an area", ["README.md"], "readme: fix the broken link to the configuration reference\n",
     "clean", {}),
    ("a dotfile's name is an area", [".github/workflows/ci.yml"],
     "github: run tests on pull requests\n\nNot-verified: the workflow run; no runner locally\n", "clean", {}),
    ("an area in another case is the same area", ["README.md"], "README: fix the broken link\n", "clean", {}),
    ("all is always an area", GO, "all: first public version\n\n" + EV, "clean", {}),
    ("docs is always an area", ["README.md"], "docs: fix the broken link\n", "clean", {}),
    ("ci is always an area", [".github/workflows/ci.yml"],
     "ci: run tests on pull requests\n\nNot-verified: the workflow run; no runner locally\n", "clean", {}),
    ("deps is always an area", ["go.mod"], "deps: bump x/net to 0.30\n\n" + EV, "clean", {}),
    ("tests is always an area", ["internal/scheduler/worker_test.go"], "tests: cover lease renewal\n\n" + EV, "clean", {}),
    ("build is always an area", ["Makefile"], "build: add a lint target\n\n" + EV, "clean", {}),
    ("a path-map label is an area", [".github/workflows/ci.yml"],
     "actions: run tests on pull requests\n\nNot-verified: the workflow run; no runner locally\n", "clean",
     {"area_map": {".github/": "actions"}}),
    ("a path on the map still offers its own names", [".github/workflows/ci.yml"],
     "workflows: run tests on pull requests\n\nNot-verified: the workflow run; no runner locally\n", "clean",
     {"area_map": {".github/": "actions"}}),
    ("a listed area is an area", GO, "billing: store amounts in pence\n\n" + EV, "clean", {"areas": ["billing"]}),
    ("an area from nowhere is flagged with the candidates", GO, "api: renew leases\n\n" + EV,
     "not a directory or file name from the changed paths", {}),
    ("the candidates list the path's names and the built-ins", GO, "api: renew leases\n\n" + EV,
     "`internal`, `scheduler`, `worker`, `all`", {}),
    ("a change-type word is not an area", GO, "fix: renew leases\n\n" + EV, "what kind of change", {}),
    ("a typed header is not accepted under the area profile", GO, "fix(scheduler): renew leases\n\n" + EV,
     "what kind of change", {}),
    ("a change-type directory is not an area", ["fix/patch.py"], "fix: apply the vendor patch\n\n" + EV,
     "what kind of change", {}),
    ("a file named for a change type keeps its extension", ["fix.py"],
     "fix.py: handle an empty input file\n\n" + EV, "clean", {}),
    ("an empty commit accepts any area", [], "release: mark the release point\n\nA tag anchor.\n", "clean", {}),

    # the outcome is the writer's: no checks on its wording
    ("an outcome may begin with a digit", GO, "scheduler: 3 retries before giving up\n\n" + EV, "clean", {}),
    ("an outcome may begin with a capital", GO, "scheduler: Windows paths are honoured\n\n" + EV, "clean", {}),
    ("an outcome may contain a bang", GO, "scheduler: reject `!=` in filter expressions\n\n" + EV, "clean", {}),
    ("an outcome may end in a full stop", GO, "scheduler: renew leases.\n\n" + EV, "clean", {}),
    ("an outcome may carry an issue number", GO, "scheduler: renew leases (#42)\n\n" + EV, "clean", {}),
    ("a malformed subject is flagged", GO, "scheduler:renew leases\n\n" + EV, "must be `<area>: <outcome>`", {}),
    ("the second line must be blank", GO, "scheduler: renew leases\nBody.\n\n" + EV, "second line must be blank", {}),

    # width: a band, not a column
    ("a 76-character subject passes", GO, "scheduler: " + "x" * 65 + "\n\n" + EV, "clean", {}),
    ("an 81-character subject is flagged", GO, "scheduler: " + "x" * 70 + "\n\n" + EV, "keep it under 80", {}),
    ("a 76-column body line passes", GO, "scheduler: renew leases\n\n" + "word " * 15 + "y\n\n" + EV, "clean", {}),
    ("an 81-column body line is flagged", GO, "scheduler: renew leases\n\n" + "word " * 16 + "y\n\n" + EV, "columns", {}),
    ("one long token excuses only itself", GO,
     "scheduler: log the request path\n\nThe path " + LONG + " is logged whenever a request arrives so that an operator reading the log can find it again.\n\n" + EV,
     "columns", {}),
    ("a line that is one long token and a few words passes", GO,
     "scheduler: log the request path\n\nSee " + LONG + " for the path.\n\n" + EV, "clean", {}),
    ("a heading in the body is the writer's business", GO, "scheduler: renew leases\n\n## Why\n\nBody.\n\n" + EV, "clean", {}),

    # what owes evidence
    ("a documentation change owes nothing", ["docs/guide.md"], "docs: explain the retry policy\n", "clean", {}),
    ("a .gitignore change owes nothing", [".gitignore"], "gitignore: ignore the virtualenv directory\n", "clean", {}),
    ("an .editorconfig change owes nothing", [".editorconfig"], "editorconfig: indent YAML with two spaces\n", "clean", {}),
    ("a CODEOWNERS change owes nothing", [".github/CODEOWNERS"], "github: route hook changes to the tooling team\n",
     "clean", {}),
    ("a licence change owes nothing", ["LICENSE"], "license: release under AGPL-3.0-or-later\n", "clean", {}),
    ("a requirements file is not documentation", ["requirements.txt"], "deps: pin requests below 3\n", "no `Verified:`", {}),
    ("a CMake list is not documentation", ["CMakeLists.txt"], "build: add the net target\n", "no `Verified:`", {}),
    ("contract documentation owes evidence", ["docs/api/openapi.md"], "docs: describe the new error code\n",
     "no `Verified:`", {"contract_docs": ["docs/api/"]}),
    ("a mixed change owes evidence for its code", ["README.md", "internal/scheduler/worker.go"],
     "scheduler: renew leases\n\nThe guide now says when.\n", "commit changes internal/scheduler/worker.go", {}),
    ("an inert change owes nothing", GO, "scheduler: rename worker to runner\n", "clean", {"__inert__": True}),

    # evidence grammar
    ("Verified needs three parts", GO, "scheduler: renew leases\n\nVerified: go test ./...; ok 12 packages\n",
     "three parts", {}),
    ("Verified with a filler outcome is flagged", GO, "scheduler: renew leases\n\nVerified: this commit; go test ./...; passed\n",
     "filler word", {}),
    ("Verified with a filler scope is flagged", GO, "scheduler: renew leases\n\nVerified: n/a; go test ./...; ok 12\n",
     "filler word", {}),
    ("Not-verified takes a scope and a reason", GO,
     "scheduler: renew leases\n\nNot-verified: Windows path handling; no Windows runner was available\n", "clean", {}),
    ("Not-verified in the older not-run form still passes", GO,
     "scheduler: renew leases\n\nNot-verified: the suite; not run: no suite exists yet\n", "clean", {}),
    ("Not-verified with no reason is flagged", GO, "scheduler: renew leases\n\nNot-verified: the suite was not run\n",
     "needs `<what was not checked>; <why>`", {}),
    ("Not-verified with a filler reason is flagged", GO, "scheduler: renew leases\n\nNot-verified: the suite; n/a\n",
     "needs `<what was not checked>; <why>`", {}),
    ("Refs must be an absolute URL", GO, "scheduler: renew leases\n\n" + EV + "Refs: #42\n", "absolute http(s) URL", {}),
    ("Refs with a plain URL passes", GO, "scheduler: renew leases\n\n" + EV + "Refs: https://github.com/o/r/issues/42\n",
     "clean", {}),
    ("Fixes: is renamed", GO, "scheduler: renew leases\n\n" + EV + 'Fixes: 9f3c1a2b7d4e ("api: accept bodies")\n',
     "`Introduced-by:` in this format", {}),
    ("Introduced-by needs a hash and a quoted subject", GO, "scheduler: renew leases\n\n" + EV + "Introduced-by: #42\n",
     "must be `<12-64 hex>", {}),
    ("Breaking-Change needs two parts", GO, "scheduler: drop the v1 endpoint\n\n" + EV + "Breaking-Change: v1 is gone\n",
     "needs `<what breaks>;", {}),

    # the trailer block as Git reads it
    ("an unindented continuation drops the block", GO,
     "scheduler: renew leases\n\nBody.\n\nVerified: this commit; go test ./...;\n12 packages ok\n", "mixes trailers", {}),
    ("an unindented line inside a Git-recognised block", GO,
     "scheduler: renew leases\n\nBody.\n\nVerified: this commit; go test ./...;\nok 12 packages\nSigned-off-by: x <x@y.z>\n",
     "neither `Key: value` nor an indented continuation", {}),
    ("a trailer above a blank line is lost", GO,
     "scheduler: renew leases\n\nBody.\n\n" + EV + "\nCo-Authored-By: x <x@y.z>\n", "outside the final trailer block", {}),
    ("--- in the body does not hide the trailers", GO,
     "scheduler: renew leases\n\nBody with a rule.\n---\nMore body.\n\n" + EV, "clean", {}),

    # what would act on a forge
    ("a closing keyword before #N is flagged", GO, "scheduler: renew leases\n\nFixes #42 by renewing them.\n\n" + EV,
     "would act on an issue", {}),
    ("a closing keyword before a URL is flagged", GO,
     "scheduler: renew leases\n\nThis resolves https://gitlab.example/g/p/-/issues/42 as asked.\n\n" + EV,
     "would act on an issue", {}),
    ("a closing keyword before a configured key is flagged", GO,
     "scheduler: renew leases\n\nFixes PROJ-42 by renewing them.\n\n" + EV, "would act on an issue",
     {"forge": "gitlab", "issue_keys": ["PROJ"]}),
    ("a closing keyword before an identifier passes", GO,
     "scheduler: decode request bodies\n\nFixes UTF-8 decoding of the body.\n\n" + EV, "clean", {"forge": "gitlab"}),
    ("a key-shaped token without configured keys is an identifier", GO,
     "scheduler: renew leases\n\nCloses PROJ-42 bodies early.\n\n" + EV, "clean", {}),
    ("a github-only forge ignores gitlab verbs", GO, "scheduler: renew leases\n\nImplementing #42 as asked.\n\n" + EV,
     "clean", {"forge": "github"}),
    ("a CI token is flagged even quoted", GO, "scheduler: renew leases\n\nBody, \"[skip ci]\" quoted.\n\n" + EV,
     "CI control token", {}),

    # native Git messages and autosquash
    ("a fixup is exempt", GO, "fixup! scheduler: renew leases\n", "clean", {}),
    ("a revert keeps Git's subject", GO,
     "Revert \"scheduler: renew leases\"\n\nThis reverts commit 9f3c1a2b7d4e9f3c1a2b7d4e9f3c1a2b7d4e9f3c. The\nrenewal broke the health probe.\n\n" + EV,
     "clean", {}),
    ("a revert on a code path still owes evidence", GO,
     "Revert \"scheduler: renew leases\"\n\nThis reverts commit 9f3c1a2b7d4e9f3c1a2b7d4e9f3c1a2b7d4e9f3c.\n", "no `Verified:`", {}),

    # the typed header profile
    ("typed: type(area) is accepted", GO, "fix(scheduler): renew leases\n\n" + EV, "clean", {"header": "typed"}),
    ("typed: the area still comes from the paths", GO, "fix(api): renew leases\n\n" + EV,
     "not a directory or file name", {"header": "typed"}),
    ("typed: ! needs Breaking-Change", GO, "feat(scheduler)!: drop the v1 endpoint\n\n" + EV, "go together",
     {"header": "typed"}),
    ("typed: Breaking-Change needs !", GO, TYPED_BREAK.replace("feat(api)", "feat(scheduler)"), "go together",
     {"header": "typed"}),
    ("typed: a revert carrying Breaking-Change needs no !", GO, TYPED_REVERT, "clean", {"header": "typed"}),
    ("typed, paragraph marker: ! is flagged", GO,
     "feat(scheduler)!: drop the v1 endpoint\n\nBREAKING CHANGE: v1 is gone; call v2\n\n" + EV,
     "spaced `BREAKING CHANGE:`", {"header": "typed", "breaking_marker": "paragraph"}),
    ("typed, paragraph marker: the trailer without the paragraph is flagged", GO,
     TYPED_BREAK.replace("feat(api)", "feat(scheduler)"), "BREAKING CHANGE",
     {"header": "typed", "breaking_marker": "paragraph"}),
    ("typed, paragraph marker: trailer and paragraph together pass", GO,
     TYPED_BREAK_PARAGRAPH.replace("feat(api)", "feat(scheduler)"), "clean",
     {"header": "typed", "breaking_marker": "paragraph"}),
    ("typed, paragraph marker: the paragraph without the trailer is flagged", GO,
     TYPED_BREAK_PARAGRAPH.replace("feat(api)", "feat(scheduler)").replace(
         "Breaking-Change: the v1 endpoint is gone; call v2\n", ""),
     "Breaking-Change", {"header": "typed", "breaking_marker": "paragraph"}),
    ("typed, paragraph marker: a sole breaking paragraph is the body", GO,
     TYPED_BREAK_SOLE.replace("feat(api)", "feat(scheduler)"), "clean", {"header": "typed", "breaking_marker": "paragraph"}),
    ("typed, paragraph marker: an empty breaking paragraph is flagged", GO,
     TYPED_BREAK_EMPTY.replace("feat(api)", "feat(scheduler)"), "empty", {"header": "typed", "breaking_marker": "paragraph"}),
    ("typed, paragraph marker: the breaking paragraph must come last", GO,
     TYPED_BREAK_EARLY.replace("feat(api)", "feat(scheduler)"), "last paragraph",
     {"header": "typed", "breaking_marker": "paragraph"}),
]


def main():
    failures = 0
    for name, paths, message, expect, overrides in CASES:
        inert = overrides.pop("__inert__", False)
        config = {**DEFAULT, **overrides}
        findings = hook.check_message(message, paths, config, inert=inert)
        if expect == "clean":
            ok = not findings
        else:
            ok = any(expect in f for f in findings)
        status = "ok  " if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"{status} {name}")
        if not ok:
            for f in findings or ["(no findings)"]:
                print(f"       - {f}")
    print(f"\n{len(CASES) - failures} of {len(CASES)} fixtures pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

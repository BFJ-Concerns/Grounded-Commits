#!/usr/bin/env python3
"""Fixtures for the Grounded Commits reference hook.

Each case names the changed paths, the tracked files that stand in for the
repository (defaults to the changed paths), the message, and either "clean" or
a fragment every finding list must contain. Run: python3 test_fixtures.py
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
GO = ["internal/scheduler/worker.go", "internal/scheduler/lease.go", "internal/api/handler.go",
      "cmd/server/main.go", "go.mod", "README.md"]
PY_FLAT = ["mypkg/__init__.py", "mypkg/scheduler.py", "mypkg/cli.py", "mypkg/config.py",
           "tests/test_scheduler.py", "pyproject.toml", "README.md"]
PY_SRC = ["src/mypkg/__init__.py", "src/mypkg/scheduler.py", "src/mypkg/cli.py", "tests/test_cli.py", "README.md"]
RAILS = ["app/models/user.rb", "app/models/invoice.rb", "app/controllers/users_controller.rb",
         "config/routes.rb", "Gemfile", "README.md"]
DJANGO = ["myproject/settings.py", "myproject/billing/models.py", "myproject/billing/views.py",
          "myproject/auth/models.py", "manage.py", "README.md"]
MAVEN = ["src/main/java/com/acme/billing/Invoice.java", "src/main/java/com/acme/auth/Login.java",
         "src/test/java/com/acme/billing/InvoiceTest.java", "pom.xml", "README.md"]
MONOREPO = ["packages/web/src/index.ts", "packages/@acme/payments/src/charge.ts", "apps/cli/main.ts",
            "docs/payments.md", "package.json"]

SCHEDULER = """scheduler: stop running a job twice when a worker shuts down

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
"""

CASES = [
    # name, paths, tracked, message, expectation (clean | fragment), config overrides
    ("readme example parses clean", ["internal/scheduler/worker.go"], GO, SCHEDULER, "clean", {}),
    ("go: area from internal/scheduler", ["internal/scheduler/lease.go"], GO,
     "scheduler: renew leases before they expire\n\nThe requirement is X.\n\nVerified: final contents; go test ./...; ok 12 packages\n", "clean", {}),
    ("go: internal is not an area", ["internal/scheduler/lease.go"], GO,
     "internal: renew leases\n\nBody.\n\nVerified: final contents; go test ./...; ok 12 packages\n", "does not come from the changed paths", {}),
    ("python flat: package is the area", ["mypkg/scheduler.py"], PY_FLAT,
     "mypkg: retry on timeout\n\nBody.\n\nVerified: final contents; pytest -q; 14 passed\n", "clean", {}),
    ("python src: wrapper and container skipped", ["src/mypkg/cli.py"], PY_SRC,
     "cli: print the resolved path\n\nBody.\n\nVerified: final contents; pytest -q; 9 passed\n", "clean", {}),
    ("rails: app is a wrapper", ["app/models/invoice.rb"], RAILS,
     "models: total invoices in pence\n\nBody.\n\nVerified: final contents; bin/rails test; 40 runs, 0 failures\n", "clean", {}),
    ("django: nested app yields the project package", ["myproject/billing/models.py"], DJANGO,
     "myproject: store amounts in pence\n\nBody.\n\nVerified: final contents; manage.py test; 22 passed\n", "clean", {}),
    ("django: a path map restores the app", ["myproject/billing/models.py"], DJANGO,
     "billing: store amounts in pence\n\nBody.\n\nVerified: final contents; manage.py test; 22 passed\n", "clean",
     {"area_map": {"myproject/billing/": "billing", "myproject/auth/": "auth"}}),
    ("maven: test path gives the same area", ["src/test/java/com/acme/billing/InvoiceTest.java"], MAVEN,
     "billing: cover half-up rounding\n\nBody.\n\nVerified: final contents; mvn test; 32 passed\n", "clean", {}),
    ("maven: single domain still gives the domain", ["src/main/java/com/acme/billing/Invoice.java"],
     ["src/main/java/com/acme/billing/Invoice.java", "src/main/java/com/acme/billing/Tax.java", "pom.xml"],
     "billing: round totals half-up\n\nBody.\n\nVerified: final contents; mvn test; 31 passed\n", "clean", {}),
    ("c++: include and src agree", ["include/acme/net/socket.hpp", "src/net/socket.cpp"],
     ["include/acme/net/socket.hpp", "src/net/socket.cpp", "src/storage/db.cpp", "CMakeLists.txt"],
     "net: reuse sockets across requests\n\nBody.\n\nVerified: final contents; ctest; 18 passed\n", "clean", {}),
    ("root fix.py uses its full name", ["fix.py"], ["fix.py", "README.md"],
     "fix.py: handle an empty input file\n\nBody.\n\nVerified: final contents; python3 fix.py empty.txt; exit 0\n", "clean", {}),
    ("a directory over 24 characters is not an area", ["infrastructure-configuration-tools/a.tf"],
     ["infrastructure-configuration-tools/a.tf", "infrastructure-configuration-tools/b.tf", "README.md"],
     "infrastructure-configuration-tools: pin the provider\n\nBody.\n\nVerified: final contents; terraform validate; Success\n",
     "at most 24 characters", {}),
    ("configured issue key in subject", ["internal/api/handler.go"], GO,
     "api: reject PROJ-42 requests\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "issue reference",
     {"issue_keys": ["PROJ"]}),
    ("key-shaped token without configured keys is an identifier", ["internal/api/handler.go"], GO,
     "api: reject PROJ-42 requests\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "clean", {}),
    ("identifiers with a hyphen and digits pass", ["internal/api/handler.go"], GO,
     "api: hash UTF-8 bodies with SHA-256\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "clean", {}),
    ("licence identifier in subject", ["LICENSE"], ["LICENSE", "README.md"],
     "license: release under AGPL-3.0-or-later\n\nThe owner asked for the AGPL.\n", "clean", {}),
    ("configured key is caught beside an identifier", ["internal/api/handler.go"], GO,
     "api: reject PROJ-42 bodies that are not UTF-8\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n",
     "issue reference", {"issue_keys": ["PROJ"]}),
    ("bang in outcome", ["internal/api/handler.go"], GO,
     "api: reject empty bodies!\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "does not belong", {}),
    ("malformed subject does not crash", ["internal/api/handler.go"], GO,
     "api:reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "must be `<area>: <outcome>`", {}),
    ("unindented line inside a Git-recognised block", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...;\nok 12 packages\nSigned-off-by: x <x@y.z>\n",
     "neither `Key: value` nor an indented continuation", {}),
    ("typed profile: trailer without ! is flagged", ["internal/api/handler.go"], GO,
     "feat(api): drop the v1 endpoint\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\nBreaking-Change: v1 is gone; call v2\n",
     "go together", {"header": "typed"}),
    ("typed profile, paragraph marker: ! is flagged", ["internal/api/handler.go"], GO,
     "feat(api)!: drop the v1 endpoint\n\nBody.\n\nBREAKING CHANGE: v1 is gone; call v2\n\nVerified: final contents; go test ./...; ok 12\n",
     "spaced `BREAKING CHANGE:`", {"header": "typed", "breaking_marker": "paragraph"}),
    ("maven: reverse-domain containers skipped", ["src/main/java/com/acme/billing/Invoice.java"], MAVEN,
     "billing: round totals half-up\n\nBody.\n\nVerified: final contents; mvn test; 31 passed\n", "clean", {}),
    ("monorepo: scoped package", ["packages/@acme/payments/src/charge.ts"], MONOREPO,
     "payments: retry declined cards once\n\nBody.\n\nVerified: final contents; pnpm test; 12 passed\n", "clean", {}),
    ("root build file uses its full name", ["build.gradle"], ["build.gradle", "src/main/java/x/A.java"],
     "build.gradle: pin the wrapper to 8.14\n\nBody.\n\nVerified: final contents; ./gradlew test; 5 passed\n", "clean", {}),
    ("root extensionless build script gives all", ["build"], ["build", "src/x.py"],
     "all: make the build script executable\n\nBody.\n\nVerified: final contents; ./build; exit 0\n", "clean", {}),
    ("root extensionless build script is not the area build", ["build"], ["build", "src/x.py"],
     "build: make the script executable\n\nBody.\n\nVerified: final contents; ./build; exit 0\n", "does not come from the changed paths", {}),
    ("build directory is the area build", ["build/Makefile"], ["build/Makefile", "src/x.py"],
     "build: add a lint target\n\nBody.\n\nVerified: final contents; make lint; clean\n", "clean", {}),
    ("docs directory is the area docs", ["docs/payments.md"], MONOREPO,
     "docs: describe the payments webhook\n\nBody.\n", "clean", {}),
    ("change-type directory gives all", ["fix/patch.py"], ["fix/patch.py", "README.md"],
     "all: apply the vendor patch on start-up\n\nBody.\n\nVerified: final contents; python3 fix/patch.py; exit 0\n", "clean", {}),
    ("change-type directory is not an area", ["fix/patch.py"], ["fix/patch.py", "README.md"],
     "fix: apply the vendor patch on start-up\n\nBody.\n\nVerified: final contents; python3 fix/patch.py; exit 0\n", "change-type word", {}),
    ("__init__ stands for its directory", ["src/mypkg/__init__.py"], PY_SRC,
     "mypkg: export the scheduler from the package root\n\nBody.\n\nVerified: final contents; python3 -m pytest; 12 passed\n", "clean", {}),
    ("init.py is an ordinary file", ["src/mypkg/init.py"], PY_SRC,
     "init: seed the default configuration\n\nBody.\n\nVerified: final contents; python3 -m pytest; 12 passed\n", "clean", {}),
    ("crate root module gives all", ["src/lib.rs"], ["src/lib.rs", "src/parser.rs", "Cargo.toml"],
     "all: export the parser from the crate root\n\nBody.\n\nVerified: final contents; cargo test; 9 passed\n", "clean", {}),
    ("crate root module is not the area src", ["src/lib.rs"], ["src/lib.rs", "src/parser.rs", "Cargo.toml"],
     "src: export the parser from the crate root\n\nBody.\n\nVerified: final contents; cargo test; 9 passed\n", "does not come from the changed paths", {}),
    ("github dir normalises", [".github/workflows/ci.yml"], [".github/workflows/ci.yml", "src/a.py", "src/b.py"],
     "github: run tests on pull requests\n\nBody.\n\nNot-verified: workflow run; not run: no runner locally\n", "clean", {}),
    ("path map wins", [".github/workflows/ci.yml"], [".github/workflows/ci.yml", "src/a.py"],
     "ci: run tests on pull requests\n\nBody.\n\nNot-verified: workflow run; not run: no runner locally\n", "clean",
     {"area_map": {".github/": "ci"}}),
    ("all is always allowed", GO, GO, "all: first public version\n\nBody.\n\nVerified: final contents; go test ./...; ok\n",
     "filler word", {}),
    ("trivial docs change, bare subject", ["README.md"], GO, "readme: fix the broken link to the configuration reference\n", "clean", {}),
    ("trivial code change keeps evidence", ["internal/scheduler/worker.go"], GO,
     "scheduler: apply gofmt formatting to the worker module\n\nVerified: final contents; gofmt -l . and go test ./...; clean, ok\n", "clean", {}),
    ("trivial code change without evidence", ["internal/scheduler/worker.go"], GO,
     "scheduler: apply gofmt formatting to the worker module\n", "no `Verified:` or `Not-verified:`", {}),
    ("dependency bump needs a body", ["go.mod"], GO, "go: bump x/net to 0.30\n\nVerified: final contents; go test ./...; ok 12 packages\n", "body is missing", {}),
    ("unindented continuation drops the block", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...;\n12 packages ok\n", "mixes trailers", {}),
    ("trailer above a blank line is lost", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n\nCo-Authored-By: x <x@y.z>\n",
     "outside the final trailer block", {}),
    ("--- in body does not hide trailers", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody with a rule.\n---\nMore body.\n\nVerified: final contents; go test ./...; ok 12\n", "clean", {}),
    ("Fixes: is renamed", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\nFixes: 9f3c1a2b7d4e (\"api: accept bodies\")\n",
     "`Introduced-by:` in this format", {}),
    ("closing keyword before #N", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nFixes #42 by rejecting them.\n\nVerified: final contents; go test ./...; ok 12\n", "would act on an issue", {}),
    ("closing keyword before URL", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nThis resolves https://gitlab.example/g/p/-/issues/42 as asked.\n\nVerified: final contents; go test ./...; ok 12\n",
     "would act on an issue", {}),
    ("closing keyword before a configured key", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nFixes PROJ-42 by rejecting them.\n\nVerified: final contents; go test ./...; ok 12\n",
     "would act on an issue", {"forge": "gitlab", "issue_keys": ["PROJ"]}),
    ("closing keyword before an identifier", ["internal/api/handler.go"], GO,
     "api: decode request bodies\n\nFixes UTF-8 decoding of the body.\n\nVerified: final contents; go test ./...; ok 12\n",
     "clean", {"forge": "gitlab"}),
    ("github-only forge ignores gitlab verbs", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nImplementing #42 as asked.\n\nVerified: final contents; go test ./...; ok 12\n", "clean", {"forge": "github"}),
    ("Refs with plain URL is fine", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\nRefs: https://github.com/o/r/issues/42\n", "clean", {}),
    ("typed header rejected under area profile", ["internal/api/handler.go"], GO,
     "fix(api): reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "change-type word", {}),
    ("typed profile accepts type(area)", ["internal/api/handler.go"], GO,
     "fix(api): reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "clean", {"header": "typed"}),
    ("typed profile: ! needs Breaking-Change", ["internal/api/handler.go"], GO,
     "feat(api)!: drop the v1 endpoint\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "go together", {"header": "typed"}),
    ("filler outcome", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; passed\n", "filler word", {}),
    ("Not-verified grammar", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody.\n\nNot-verified: the suite was not run\n", "needs `<scope>; not run:", {}),
    ("CI token", ["internal/api/handler.go"], GO,
     "api: reject empty bodies\n\nBody, \"[skip ci]\" quoted.\n\nVerified: final contents; go test ./...; ok 12\n", "CI control token", {}),
    ("subject too long", ["internal/api/handler.go"], GO,
     "api: " + "x" * 70 + "\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "the limit is 72", {}),
    ("capitalised outcome", ["internal/api/handler.go"], GO,
     "api: Reject empty bodies\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "capital letter", {}),
    ("identifier keeps its case", ["internal/api/handler.go"], GO,
     "api: honour CONFIG_PATH as the config file location\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "clean", {}),
    ("Breaking-Change needs two parts", ["internal/api/handler.go"], GO,
     "api: drop the v1 endpoint\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\nBreaking-Change: v1 is gone\n", "needs `<what breaks>;", {}),
    ("fixup is exempt", ["internal/api/handler.go"], GO, "fixup! api: reject empty bodies\n", "clean", {}),
    ("revert keeps the native subject", ["internal/api/handler.go"], GO,
     "Revert \"api: reject empty bodies\"\n\nThis reverts commit 9f3c1a2b7d4e9f3c1a2b7d4e9f3c1a2b7d4e9f3c. The\nrejection broke the health probe; the reversal is complete.\n\nVerified: final contents; go test ./...; ok 12\n", "clean", {}),
    ("emoji in subject", ["internal/api/handler.go"], GO,
     "api: reject empty bodies ✨\n\nBody.\n\nVerified: final contents; go test ./...; ok 12\n", "emoji", {}),
    ("contract docs need evidence", ["docs/api/openapi.md"], GO + ["docs/api/openapi.md"],
     "docs: describe the new error code\n\nBody.\n", "no `Verified:`", {"contract_docs": ["docs/api/"]}),
    ("plain docs need no evidence", ["docs/guide.md"], GO + ["docs/guide.md"],
     "docs: explain the retry policy\n\nThe guide now says when the client retries.\n", "clean", {}),
]


def main():
    failures = 0
    for name, paths, tracked, message, expect, overrides in CASES:
        config = {**DEFAULT, **overrides}
        findings = hook.check_message(message, paths, config, tracked or paths, None)
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

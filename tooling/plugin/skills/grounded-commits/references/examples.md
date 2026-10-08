# Grounded Commits: further examples

## A trivial change on a documentation path

No body and no evidence pair: behaviour does not change, the subject names the
mechanism, and only documentation changed.

```
readme: fix the broken link to the configuration reference
```

## A trivial change on a code path

Still no body, but a code path changed, so the commit claims no behaviour
change and the evidence pair covers the suite.

```
scheduler: apply rustfmt formatting to the worker module

Verified: final contents; cargo fmt --check and cargo test -p scheduler;
  clean, 41 passed
```

## A defect repair carrying `Introduced-by:`

The body names the symptom and how it showed, and states the
present-at-commit, absent-at-parent result that substantiates
`Introduced-by:`.

```
scheduler: stop running a job twice when a worker shuts down

On shutdown the worker released its leases before draining its local
queue, so a job it had already dequeued was handed to another worker
and also run locally. The reproducer shows duplicate invoice emails
from the 28 September incident (issue 301); the log has "lease
released" before "drain complete".

Drain the local queue first, then release leases. The new ordering
test asserts that each job id is observed exactly once across two
workers stopping concurrently. It fails at 9f3c1a2b7d4e and passes at
that commit's parent, which is what establishes that commit as the
origin.

Verified: 9f3c1a2b7d4e^, 9f3c1a2b7d4e and final contents;
  go test ./scheduler/... -run TestShutdownOrdering -count=50;
  0 of 50, 7 of 50 and 0 of 50 runs failed respectively
Verified: final contents; go test ./...; all packages passed
Not-verified: replay against the production incident data; not run:
  the data is not retained outside the billing environment
Introduced-by: 9f3c1a2b7d4e ("scheduler: release leases eagerly on
  shutdown")
Refs: https://forge.example/ops/billing/issues/301
```

## Evidence rebound after a rebase

The branch was rebased onto main after the check and the suite was not run
again, so `Verified:` names the commit that was tested and the new tree is
declared unverified.

```
cli: print the resolved config path with --print-config

Operators asked (issue 227) which file the service actually loaded
when several candidates exist. --print-config now prints the resolved
path on its first line, before the values.

Verified: 7c0d2e5a91b4 (the tested commit before rebase onto main);
  cargo test -p app-cli; 12 passed
Not-verified: final contents; not run: the branch was rebased onto
  main after the check and the suite was not re-run
Refs: https://forge.example/ops/app/issues/227
```

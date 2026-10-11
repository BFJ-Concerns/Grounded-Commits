# Grounded Commits: examples

## A full message

A request backed by an issue, the reproducer's observation, the behaviour
that changed, a rejected alternative, and an evidence pair naming a gap.

```
config: honour CONFIG_PATH as the config file location

Deployments mounting configuration read-only under /etc/app need to
point the service at it (issue 214). The loader reads only the XDG
default, so those deployments silently ran on built-in defaults; the
reproducer shows the fallback happening with no warning logged.

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

The body states the symptom and how it showed, with the present-at-commit,
absent-at-parent result that substantiates `Introduced-by:`.

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
Verified: final contents; go test ./...; ok, 14 packages
Not-verified: replay against the production incident data; not run:
  the data is not retained outside the billing environment
Introduced-by: 9f3c1a2b7d4e ("scheduler: release leases eagerly on
  shutdown")
Refs: https://forge.example/ops/billing/issues/301
```

## Evidence rebound after a rewrite

The branch's fix-ups were folded before its final approval and the suite was
not run again. The `Verified:` line keeps the check and names the tree it
ran on in words, and the gap for the new tree says what the fold did to this
commit's files. Naming the replaced commit by hash would point at an object
nothing keeps reachable.

```
cli: print the resolved config path with --print-config

Which file the service loads when several candidates exist is shown
nowhere (issue 227). --print-config now prints the resolved path on
its first line, before the values.

Verified: the tree before the fold; cargo test -p app-cli; 12 passed
Not-verified: final contents; not run: the fold changed no file this
  commit touches and the suite was not re-run
Refs: https://forge.example/ops/app/issues/227
```

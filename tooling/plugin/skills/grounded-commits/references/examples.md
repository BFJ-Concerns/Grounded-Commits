# Grounded Commits: examples

## A full message

A request backed by an issue, the observation, the behaviour that changed, a
rejected alternative, and evidence naming a gap.

```
config: honour CONFIG_PATH as the config file location

Deployments mounting configuration read-only under /etc/app need to
point the service at it (issue 214). The loader reads only the XDG
default, so those deployments silently ran on built-in defaults with
no warning logged.

The loader now checks CONFIG_PATH before the XDG default; --config
still wins when both are given, so existing invocations are
unaffected. The CLI help text and the operations guide state the
precedence.

Considered and rejected: a config.d directory search. It would cover
the read-only case too, but its ordering rules would need their own
documentation and tests for a problem one variable solves.

Verified: this commit; cargo test -p app-config (precedence cases added
  in config/tests/precedence.rs); 9 passed
Verified: this commit; manual run with CONFIG_PATH set to a file outside
  ~/.config and no ~/.config present; --print-config showed the file's
  values
Not-verified: Windows path handling; no Windows runner was available
Refs: https://forge.example/ops/app/issues/214
```

## A trivial change

On documentation, a subject alone:

```
readme: fix the broken link to the configuration reference
```

On code, the subject and the evidence:

```
scheduler: apply rustfmt to the worker module

Verified: this commit; cargo fmt --check and cargo test -p scheduler;
  clean, 41 passed
```

A rename or a whitespace-only change needs no evidence either way.

## A defect repair carrying `Introduced-by:`

The body states the symptom and how it showed. The present-at-that-commit,
absent-at-its-parent result is what earns the `Introduced-by:` line.

```
scheduler: stop running a job twice when a worker shuts down

On shutdown the worker released its leases before draining its local
queue, so a job it had already dequeued was handed to another worker
and also run locally. The symptom was duplicate invoice emails from the
28 September incident (issue 301); the log shows "lease released"
before "drain complete".

Drain the local queue first, then release leases. The new ordering
test asserts that each job id is observed exactly once across two
workers stopping concurrently; it fails at 9f3c1a2b7d4e and passes at
that commit's parent.

Verified: this commit; go test ./scheduler/... -run TestShutdownOrdering
  -count=50; 0 of 50 runs failed, against 7 of 50 at 9f3c1a2b7d4e and
  0 of 50 at its parent
Verified: this commit; go test ./...; ok, 14 packages
Not-verified: replay against the production incident data; the data is
  not retained outside the billing environment
Introduced-by: 9f3c1a2b7d4e ("scheduler: release leases eagerly on
  shutdown")
Refs: https://forge.example/ops/billing/issues/301
```

## Evidence that the old code fails the new tests

Showing that the tests catch the defect usually means running them against
the code before the fix, which is not a commit anyone will keep. Describe
that tree in words rather than naming a scratch commit's hash:

```
Verified: the parent's code with this commit's tests; cargo test -p
  decoder details; both new tests failed, as intended
Verified: this commit; cargo test -p decoder; 23 passed
```

## Evidence after a rewrite

The branch's fix-ups were folded before its final approval and the suite was
not run again on the result. The `Verified:` line says which tree it ran on,
and a `Not-verified:` line covers the new one.

```
cli: print the resolved config path with --print-config

Which file the service loads when several candidates exist is shown
nowhere (issue 227). --print-config now prints the resolved path on
its first line, before the values.

Verified: the tree before the fold; cargo test -p app-cli; 12 passed
Not-verified: this commit; the fold touched no file in this commit and
  the suite was not re-run
Refs: https://forge.example/ops/app/issues/227
```

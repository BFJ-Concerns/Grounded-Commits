# Typed header profile

A repository that records the typed profile in its guidance, or whose
`.grounded-commits.toml` sets `header = "typed"` — because a release tool
reads types, or its readers list changes by kind — writes
`type(area)!?: outcome` with one of `feat fix perf refactor docs test build
ci`. The area derives as for the default subject and the parentheses are
always present; the checker enforces the profile when the setting is present.
Everything after the subject — body, obligations, trailers, rewrites — is
unchanged.

Choose the type by purpose. A behaviour change is `fix` when an observed
defect no longer occurs, `perf` when only a measured property improves,
otherwise `feat`. Code that should behave the same is `refactor`, and carries
the no-behaviour-change obligation. A change of one kind of file with no
behaviour change is `docs`, `test`, `build` or `ci`. Split a commit that mixes
kinds where you can; where you cannot, take the first of `feat fix perf
refactor build ci test docs` that applies and name the rest in the body.

A breaking change carries `!` before the colon together with the
`Breaking-Change:` trailer. Where the repository's release tool reads only
the spaced `BREAKING CHANGE:` paragraph (semantic-release's default Angular
preset does), write that paragraph last in the body, outside the trailer
block, and no `!`; such a repository sets `breaking_marker = "paragraph"` so
the checker expects it.

```
fix(api): reject requests whose body exceeds the declared length

A client sending a Content-Length smaller than its body made the server
read the overflow as the next request (the reproducer in issue 88
shows two responses to one request). The handler now rejects the
request with 400 as soon as the declared length is exceeded.

Verified: final contents; go test ./api/... -run TestOverlongBody; 3 passed
Refs: https://forge.example/ops/app/issues/88
```

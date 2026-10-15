# Typed header profile

A repository whose release tooling reads Conventional Commits types, or whose
readers list changes by kind, sets `header = "typed"` in
`.grounded-commits.toml` and writes `type(area): outcome` with one of
`feat fix perf refactor docs test build ci`. The area is chosen as for the
default subject and the parentheses are always present. Everything after the
subject is unchanged.

Choose the type by purpose: `fix` when an observed defect no longer occurs,
`perf` when only a measured property improves, `feat` for any other behaviour
change, `refactor` for code meant to behave the same, and `docs`, `test`,
`build` or `ci` for a change to that kind of file alone. Split a commit that
mixes kinds where you can; otherwise take the first of `feat fix perf
refactor build ci test docs` that applies and name the rest in the body.

A breaking change carries `!` before the colon together with the
`Breaking-Change:` trailer. Where the release tool reads only the spaced
`BREAKING CHANGE:` paragraph (semantic-release's default Angular preset
does), the repository sets `breaking_marker = "paragraph"`; then write that
paragraph last in the body, keep the trailer, and leave out the `!`.

```
fix(api): reject a non-numeric Content-Length instead of reading it as 0

A request whose Content-Length header was not a number was treated as
having an empty body, so a malformed client got a 200 for a request
the server never read (issue 88). The handler now answers 400 as soon
as the header fails to parse.

Verified: this commit; go test ./api/... -run TestBadContentLength; 3 passed
Refs: https://forge.example/ops/app/issues/88
```

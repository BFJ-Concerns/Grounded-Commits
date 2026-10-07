# Tooling

What a repository installs to adopt Grounded Commits. The guidance itself is
in [`../guidance/`](../guidance/).

## `commit-msg-hook/`

The reference `commit-msg` hook: one Python 3 file (3.8 or newer; 3.11 or
newer to read the optional configuration file) with no dependencies beyond
Git. It checks the mechanical rules of the format and prints the candidate
areas for a change.

Install into a repository that is adopting the format. If `.git/hooks/commit-msg`
already exists, or `core.hooksPath` is set, add a line to the existing hook that
runs this one instead of replacing it:

```sh
curl -fsSL -o .git/hooks/commit-msg \
  https://raw.githubusercontent.com/BFJ-Concerns/Grounded-Commits/main/tooling/commit-msg-hook/commit-msg
chmod +x .git/hooks/commit-msg
python3 .git/hooks/commit-msg --rev HEAD     # smoke check: exit 0 or a list of findings
```

Everyday use:

```sh
python3 .git/hooks/commit-msg --areas               # areas the staged change could use
python3 .git/hooks/commit-msg --rev HEAD            # check an existing commit
python3 .git/hooks/commit-msg --range main..HEAD    # check a branch, for CI or before landing
python3 .git/hooks/commit-msg --message-file draft.txt --rev HEAD
                                                    # check a draft against a commit's changes
```

The last form checks a draft before it is committed: write the replacement
message to a file and check it against the commit it is for, then amend or
reword once it is clean. The draft is checked exactly as `--rev` checks the
commit's own message, with the same paths and the same lookups of
`Introduced-by:` hashes.

A local hook sees only commits made where it is installed and is bypassed by
`--no-verify`; the `--range` form is what a landing step or CI runs.

Optional configuration goes in `.grounded-commits.toml` at the repository
root:

```toml
forge = "github"          # whose closing keywords to reject: github, gitlab, forgejo, any (default any)
header = "area"           # or "typed" for the Conventional Commits header profile
breaking_marker = "trailer"  # typed profile: "paragraph" where the release parser reads BREAKING CHANGE:
areas = ["cli", "config"] # areas that are always valid
contract_docs = ["docs/api/"]  # documentation that states a contract and needs evidence
issue_keys = ["PROJ"]     # tracker keys: PROJ-42 is then an issue reference, UTF-8 stays an identifier

[area_map]                # path prefix -> area, longest match wins, checked before derivation
".github/" = "ci"
"myproject/billing/" = "billing"
```

Run the fixtures with `python3 tooling/commit-msg-hook/test_fixtures.py`. A
clean check proves the shape only; whether the problem, the reasons and the
claims in a message are true is for review.

## `skills/`

Where packaged skills for agent tools go: a skill carries the guidance and
runs the message check from inside the tool. Any skill here is derived from
`guidance/` and changes with it.

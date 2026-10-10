# Tooling

What a repository installs to adopt Grounded Commits. The guidance itself is
in [`../guidance/`](../guidance/).

## `commit-msg-hook/`

The reference `commit-msg` hook: one Python 3 file (3.8 or newer; 3.11 or
newer to read the optional configuration file) with no dependencies beyond
Git (2.38 or newer to check a merge). It checks the mechanical rules of the
format and prints the candidate areas for a change.

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
python3 .git/hooks/commit-msg --message-file draft.txt
                                                    # check a draft against the staged change
python3 .git/hooks/commit-msg --message-file draft.txt --rev HEAD
                                                    # check a draft against a commit's changes
```

The `--message-file` forms check a draft before it is recorded. Alone, it
checks the draft against the staged change as `git commit -F draft.txt` would
record it, comment lines included; during a merge that is the merge's
resolutions and Git's merge rules, so a merge's message can be checked before
the merge commit exists. With `--rev`, it checks a replacement message
against the commit it is for, before an amend or a reword, exactly as `--rev`
checks the commit's own message, with the same paths and the same lookups of
`Introduced-by:` hashes. Either way the verdict is the one the recorded
commit will get.

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

## `plugin/`

The agent plugin for Claude Code and Codex, listed by the marketplaces at
`.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`; the
top-level README has the install commands. One set of skills serves both
tools:

- `skills/grounded-commits/` writes and checks commit messages. It bundles
  this hook as `scripts/commit-msg`, runs it for the candidate areas and to
  check commits, and installs it into a repository when asked.
- `skills/grounded-pull-requests/` writes and maintains a pull request's
  title and body.

The skills are derived from `guidance/` and change with it. The bundled
`scripts/commit-msg` is a copy of `commit-msg-hook/commit-msg`, and both
plugin manifests carry the release in `VERSION`; `python3
tooling/plugin/test_plugin.py` fails when either drifts, so a hook change or
a release updates the plugin in the same commit.

# Tooling

What a repository installs to adopt Grounded Commits. The guidance itself is
in [`../guidance/`](../guidance/).

## `commit-msg-hook/`

The reference `commit-msg` hook: one Python 3 file (3.8 or newer; 3.11 or
newer to read the optional configuration file) with no dependencies beyond
Git (2.38 or newer to check a merge). It checks the mechanical rules of the
format, the subject's shape and area, the width, the trailer block and the
evidence on code changes, and prints the names a change offers as areas. It
does not judge wording.

Install into a repository that is adopting the format. The hook's path is what
`git rev-parse --git-path hooks/commit-msg` prints, which honours
`core.hooksPath` and a linked worktree. If a hook already exists there, keep
it: save the checker beside it under another name and add a line to the
existing hook that runs it and exits on its failure, so either can reject
the commit:

```sh
hook=$(git rev-parse --git-path hooks/commit-msg)
curl -fsSL -o "$(dirname "$hook")/grounded-commits" \
  https://raw.githubusercontent.com/BFJ-Concerns/Grounded-Commits/main/tooling/commit-msg-hook/commit-msg
printf '%s\n' "python3 \"$(dirname "$hook")/grounded-commits\" \"\$1\" || exit 1" >> "$hook"
```

With no hook there:

```sh
hook=$(git rev-parse --git-path hooks/commit-msg)
curl -fsSL -o "$hook" \
  https://raw.githubusercontent.com/BFJ-Concerns/Grounded-Commits/main/tooling/commit-msg-hook/commit-msg
chmod +x "$hook"
python3 "$hook" --rev HEAD     # smoke check: exit 0 or a list of findings
```

Everyday use:

```sh
python3 .git/hooks/commit-msg --areas               # names the staged change offers as areas
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
`--no-verify`; the `--range` form is what a landing step or CI runs. Commits
from before adoption will not pass it, so a range check starts at the
adoption commit.

Optional configuration goes in `.grounded-commits.toml` at the repository
root:

```toml
forge = "github"          # whose closing keywords to reject: github, gitlab, forgejo, any (default any)
header = "area"           # or "typed" for the Conventional Commits header profile
breaking_marker = "trailer"  # typed profile: "paragraph" where the release parser reads BREAKING CHANGE:
areas = ["cli", "config"] # areas that are always valid, beside all, docs, ci, build, tests and deps
contract_docs = ["docs/api/"]  # documentation that states a contract and needs evidence
issue_keys = ["PROJ"]     # tracker keys: PROJ-42 is then an issue reference, UTF-8 stays an identifier

[area_map]                # path prefix -> area, longest match wins, added to the path's own names
".github/" = "ci"
"myproject/billing/" = "billing"
```

Three suites cover the tooling: `python3 tooling/commit-msg-hook/test_fixtures.py`
(message shapes, no repository needed), `python3
tooling/commit-msg-hook/test_hook_mode.py` (the hook in a throwaway
repository; needs Git 2.38 or newer) and `python3 tooling/plugin/test_plugin.py`
(the plugin's consistency with the hook, the guidance and the release). A
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

The repository also carries the skill-and-plugin-authoring skill under
`.claude/skills/` and `.agents/skills/`, one copy per tool, which the two
bundled skills are written and revised against; the plugin test keeps the
copies identical. The skills are derived from `guidance/` and change with it. The bundled
`scripts/commit-msg` is a copy of `commit-msg-hook/commit-msg`, and both
plugin manifests carry the release in `VERSION`; `python3
tooling/plugin/test_plugin.py` fails when either drifts, so a hook change or
a release updates the plugin in the same commit.

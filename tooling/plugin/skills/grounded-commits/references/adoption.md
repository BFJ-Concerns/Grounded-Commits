# Grounded Commits: adopting the format

To adopt the format in a repository, add a line to its agent guidance saying
that commit messages follow Grounded Commits, and install the checker as its
`commit-msg` hook (*Installing the checker as the hook*, below). A repository the defaults
do not fit adds a `.grounded-commits.toml` at its root, which the checker
reads:

- `forge` (`github`, `gitlab`, `forgejo` or `any`) narrows the issue-closing
  keywords rejected;
- `header = "typed"` selects the typed header profile
  (`typed-header-profile.md`, beside this file);
- `areas` lists always-valid areas, and `[area_map]` maps path prefixes to
  areas, longest match winning;
- `contract_docs` names documentation that states a contract and so needs
  evidence;
- `issue_keys` names a tracker's keys (`["PROJ"]`), without which the checker
  reads a token like `PROJ-42` as an identifier such as `UTF-8` rather than an
  issue reference.

Keep the file to what the repository actually needs. The checker reads only
this file, so a path map or typed profile recorded only in the repository's
guidance governs over the checker's defaults: where the two disagree, follow
the guidance, report the checker's finding as a configuration gap, and
suggest moving the setting into `.grounded-commits.toml`.

## Installing the checker as the hook

Install the checker when the user agrees or is adopting the format. The
hook's path is what `git rev-parse --git-path hooks/commit-msg` prints,
which honours `core.hooksPath`. With no file there, copy `scripts/commit-msg` to that path and make it executable.
Where a hook already exists there, keep it: copy the checker beside it under
another name and add a line to the existing hook that runs `python3
<checker> "$1"` and exits on its failure, so either hook can reject the
commit.

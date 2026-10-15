#!/usr/bin/env python3
"""Integration cases for the Grounded Commits reference hook, run against a
throwaway Git repository. Run: python3 test_hook_mode.py"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "commit-msg")
EVIDENCE = "Not-verified: changed behaviour; no suite exists yet\n"
GOOD = "scheduler: renew leases before they expire\n\nThe reproducer shows leases lapsing under load.\n\n" + EVIDENCE


def run(repo, *args, stdin=None, env=None):
    return subprocess.run(args, cwd=repo, input=stdin, capture_output=True, text=True, errors="surrogateescape", env=env)


def git(repo, *args, check=True):
    result = run(repo, "git", *args)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout


def hook(repo, *args, stdin=None):
    return run(repo, sys.executable, HOOK, *args, stdin=stdin)


def commit(repo, message, *extra):
    path = os.path.join(repo, ".git", "gc-test-message")
    with open(path, "w") as handle:
        handle.write(message)
    return run(repo, "git", "commit", "-q", "-F", path, *extra)


def write(repo, rel, text="x\n", mode="a"):
    full = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(full) or full, exist_ok=True)
    with open(full, mode) as handle:
        handle.write(text)


def fresh():
    repo = tempfile.mkdtemp(prefix="gc-hook-")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.invalid")
    git(repo, "config", "user.name", "t")
    shutil.copy(HOOK, os.path.join(repo, ".git", "hooks", "commit-msg"))
    os.chmod(os.path.join(repo, ".git", "hooks", "commit-msg"), 0o755)
    for rel in ("internal/scheduler/worker.go", "internal/api/handler.go", "cmd/server/main.go", "go.mod", "README.md"):
        write(repo, rel)
    git(repo, "add", "-A")
    result = commit(repo, "all: initial import of the scheduler service\n\nThe requirement is a starting point.\n\n" + EVIDENCE)
    assert result.returncode == 0, result.stderr
    return repo


CASES = []


def case(name):
    def register(fn):
        CASES.append((name, fn))
        return fn
    return register


def conflicting_branches(repo):
    """`side` and `main` each rewrite internal/api/handler.go differently, so
    merging `side` into `main` conflicts."""
    git(repo, "checkout", "-q", "-b", "side"); write(repo, "internal/api/handler.go", "side\n"); git(repo, "add", "-A")
    assert commit(repo, "api: side change\n\nBody.\n\n" + EVIDENCE).returncode == 0
    git(repo, "checkout", "-q", "main"); write(repo, "internal/api/handler.go", "main\n"); git(repo, "add", "-A")
    assert commit(repo, "api: main change\n\nBody.\n\n" + EVIDENCE).returncode == 0


def overlapping_branches(repo, side_text, main_text):
    """`side` and `main` each change internal/api/handler.go, which starts as
    ten lines; the texts replace its first and last line respectively, so the
    merge is clean although both sides touched the file."""
    lines = [f"line {n}\n" for n in range(10)]
    with open(os.path.join(repo, "internal/api/handler.go"), "w") as handle:
        handle.writelines(lines)
    git(repo, "add", "-A")
    assert commit(repo, "api: lay out the handler\n\nBody.\n\n" + EVIDENCE).returncode == 0
    for branch, index, text in (("side", 0, side_text), ("main", 9, main_text)):
        git(repo, "checkout", "-q", "-B", branch)
        with open(os.path.join(repo, "internal/api/handler.go"), "w") as handle:
            handle.writelines(lines[:index] + [text] + lines[index + 1:])
        git(repo, "add", "-A")
        assert commit(repo, f"api: change the handler on {branch}\n\nBody.\n\n" + EVIDENCE).returncode == 0
        if branch == "side":
            git(repo, "checkout", "-q", "main")


def side_commit(repo, subject="api: side change"):
    """A commit on `side` that main does not contain; returns its hash with main checked out."""
    git(repo, "checkout", "-q", "-b", "side"); write(repo, "internal/api/handler.go", "side\n"); git(repo, "add", "-A")
    assert commit(repo, subject + "\n\nBody.\n\n" + EVIDENCE).returncode == 0
    sha = git(repo, "rev-parse", "--short=12", "HEAD").strip()
    git(repo, "checkout", "-q", "main")
    return sha


@case("a comment-only message is rejected, not waved through")
def _(repo):
    write(repo, "internal/api/handler.go"); git(repo, "add", "-A")
    r = run(repo, "git", "commit", "-q", "-m", "# [skip ci]")
    return r.returncode != 0 and "only comment lines" in r.stderr or "CI control token" in r.stderr


@case("a CI token in a comment line is rejected")
def _(repo):
    write(repo, "internal/api/handler.go"); git(repo, "add", "-A")
    r = commit(repo, GOOD + "# [skip ci]\n")
    return r.returncode != 0 and "CI control token" in r.stderr


@case("custom comment char is honoured")
def _(repo):
    git(repo, "config", "core.commentChar", ";")
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    r = commit(repo, GOOD + "; a comment line Git strips\n")
    return r.returncode == 0


@case("a code change with no evidence is rejected at commit time")
def _(repo):
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    r = commit(repo, "scheduler: renew leases before they expire\n")
    return r.returncode != 0 and "no `Verified:`" in r.stderr


@case("a documentation change commits with a bare subject")
def _(repo):
    write(repo, "README.md", "more\n"); git(repo, "add", "-A")
    return commit(repo, "readme: note the retry policy\n").returncode == 0


@case("a pure rename owes no evidence")
def _(repo):
    git(repo, "mv", "internal/scheduler/worker.go", "internal/scheduler/runner.go")
    r = commit(repo, "scheduler: rename the worker to runner\n")
    return r.returncode == 0 and hook(repo, "--rev", "HEAD").returncode == 0


@case("a whitespace-only change owes no evidence")
def _(repo):
    write(repo, "internal/scheduler/worker.go", "x   \n\n", mode="w"); git(repo, "add", "-A")
    r = commit(repo, "scheduler: tidy whitespace\n")
    return r.returncode == 0 and hook(repo, "--rev", "HEAD").returncode == 0


@case("a change hidden among whitespace still owes evidence")
def _(repo):
    write(repo, "internal/scheduler/worker.go", "y   \n\n", mode="w"); git(repo, "add", "-A")
    r = commit(repo, "scheduler: tidy whitespace\n")
    return r.returncode != 0 and "no `Verified:`" in r.stderr


@case("a clean merge commits with Git's own message")
def _(repo):
    git(repo, "checkout", "-q", "-b", "side"); write(repo, "docs/guide.md"); git(repo, "add", "-A")
    assert commit(repo, "docs: start the guide\n").returncode == 0
    git(repo, "checkout", "-q", "main"); write(repo, "cmd/server/main.go"); git(repo, "add", "-A")
    assert commit(repo, "server: log the listen address\n\n" + EVIDENCE).returncode == 0
    r = run(repo, "git", "merge", "--no-ff", "--no-edit", "-q", "side")
    return r.returncode == 0 and len(git(repo, "log", "-1", "--format=%P").split()) == 2


@case("a clean merge of a file both sides changed owes nothing")
def _(repo):
    overlapping_branches(repo, "side\n", "main\n")
    r = run(repo, "git", "merge", "--no-ff", "--no-edit", "-q", "side")
    return (r.returncode == 0 and len(git(repo, "log", "-1", "--format=%P").split()) == 2
            and hook(repo, "--rev", "HEAD").returncode == 0)


@case("a merge with a resolved conflict owes evidence, not a body")
def _(repo):
    conflicting_branches(repo)
    run(repo, "git", "merge", "--no-ff", "side")  # conflicts
    write(repo, "internal/api/handler.go", "resolved\n", mode="w"); git(repo, "add", "-A")
    bare = commit(repo, "Merge branch 'side'\n")
    evidenced = commit(repo, "Merge branch 'side'\n\n" + EVIDENCE)
    return (bare.returncode != 0 and "merge resolves internal/api/handler.go" in bare.stderr
            and "body" not in bare.stderr and evidenced.returncode == 0)


@case("a conflict resolved by keeping one side still owes evidence")
def _(repo):
    conflicting_branches(repo)
    run(repo, "git", "merge", "--no-ff", "side")  # conflicts
    git(repo, "checkout", "--ours", "internal/api/handler.go"); git(repo, "add", "-A")
    r = commit(repo, "Merge branch 'side'\n")
    return r.returncode != 0 and "merge resolves" in r.stderr


@case("--rev on a merge that kept Git's conflict list flags the list")
def _(repo):
    conflicting_branches(repo)
    run(repo, "git", "merge", "--no-ff", "side")  # conflicts
    write(repo, "internal/api/handler.go", "resolved\n", mode="w"); git(repo, "add", "-A")
    assert run(repo, "git", "commit", "-q", "--no-edit", "--no-verify").returncode == 0
    r = hook(repo, "--rev", "HEAD")
    return r.returncode == 1 and "conflict list" in r.stderr and "merge resolves" in r.stderr


@case("an empty commit after a code commit is not mistaken for an amend")
def _(repo):
    r = commit(repo, "all: mark the release point\n\nThe requirement is a tag anchor.\n", "--allow-empty")
    return r.returncode == 0


@case("a message-only amend keeps HEAD's paths in view")
def _(repo):
    r = commit(repo, "all: initial import of the scheduler service\n\nThe requirement is a starting point.\n", "--amend")
    return r.returncode != 0 and "no `Verified:`" in r.stderr


@case("a template with a scissors line commits")
def _(repo):
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    r = commit(repo, GOOD + "# ------------------------ >8 ------------------------\ndiff --git a b\n", "--cleanup=scissors")
    return r.returncode == 0


@case("a body line starting with --- does not hide the trailers")
def _(repo):
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    r = commit(repo, "scheduler: renew leases\n\nSee the rule.\n--- and more\nBody.\n\n" + EVIDENCE)
    return r.returncode == 0


@case("a non-UTF-8 file name neither crashes nor blocks other commits")
def _(repo):
    with open(os.path.join(repo.encode(), b"internal/api/caf\xe9.go"), "wb") as handle:
        handle.write(b"x\n")
    git(repo, "add", "-A")
    r1 = commit(repo, "api: add the odd file\n\nBody.\n\n" + EVIDENCE)
    write(repo, "README.md", "more\n"); git(repo, "add", "-A")
    r2 = commit(repo, "readme: note the odd file\n")
    return r1.returncode == 0 and r2.returncode == 0


@case("--range checks a branch and reports the count")
def _(repo):
    git(repo, "checkout", "-q", "-b", "feature"); write(repo, "internal/api/handler.go"); git(repo, "add", "-A")
    assert commit(repo, "api: reject empty bodies\n\nBody.\n\n" + EVIDENCE).returncode == 0
    r = hook(repo, "--range", "main..HEAD")
    return r.returncode == 0 and "1 of 1 commits clean" in r.stderr


@case("--areas lists every name on the staged paths")
def _(repo):
    write(repo, "internal/scheduler/worker.go"); write(repo, "README.md", "more\n"); git(repo, "add", "-A")
    return hook(repo, "--areas").stdout.split() == ["readme", "internal", "scheduler", "worker"]


@case("--areas on a merge revision shows its resolutions, --rev uses that tree")
def _(repo):
    conflicting_branches(repo)
    run(repo, "git", "merge", "--no-ff", "side"); write(repo, "internal/api/handler.go", "r\n", mode="w"); git(repo, "add", "-A")
    assert commit(repo, "Merge branch 'side'\n\nResolved the handler.\n\n" + EVIDENCE).returncode == 0
    return (hook(repo, "--areas", "--rev", "HEAD").stdout.split() == ["internal", "api", "handler"]
            and hook(repo, "--rev", "HEAD").returncode == 0)


@case("--message-file --rev checks a draft against a commit's changes without committing it")
def _(repo):
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("all: initial import of the scheduler service\n\nThe requirement is a starting point.\n")
    bare = hook(repo, "--message-file", draft, "--rev", "HEAD")
    with open(draft, "w") as handle:
        handle.write("billing: initial import of the scheduler service\n\n" + EVIDENCE)
    wrong_area = hook(repo, "--message-file", draft, "--rev", "HEAD")
    with open(draft, "w") as handle:
        handle.write("all: initial import of the scheduler service\n\n" + EVIDENCE)
    clean = hook(repo, "--message-file", draft, "--rev", "HEAD")
    return (bare.returncode == 1 and "no `Verified:`" in bare.stderr and "message for " in bare.stderr
            and wrong_area.returncode == 1 and "area" in wrong_area.stderr
            and clean.returncode == 0 and git(repo, "log", "--oneline").count("\n") == 1)


@case("--message-file --rev resolves Introduced-by against the repository")
def _(repo):
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("all: initial import of the scheduler service\n\n" + EVIDENCE
                     + 'Introduced-by: 0123456789ab ("scheduler: nothing")\n')
    r = hook(repo, "--message-file", draft, "--rev", "HEAD")
    return r.returncode == 1 and "not a commit in this repository" in r.stderr


@case("--message-file --rev on a merge checks the draft against its resolutions")
def _(repo):
    conflicting_branches(repo)
    run(repo, "git", "merge", "--no-ff", "side"); write(repo, "internal/api/handler.go", "r\n", mode="w"); git(repo, "add", "-A")
    assert commit(repo, "Merge branch 'side'\n\nResolved the handler.\n\n" + EVIDENCE).returncode == 0
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("Merge branch 'side'\n")
    r = hook(repo, "--message-file", draft, "--rev", "HEAD")
    return r.returncode == 1 and "merge resolves" in r.stderr


@case("--message-file checks a draft against the staged change, as the commit records it")
def _(repo):
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("api: renew leases before they expire\n\nThe reproducer shows leases lapsing.\n")
    wrong = hook(repo, "--message-file", draft)
    with open(draft, "w") as handle:
        handle.write(GOOD)
    clean = hook(repo, "--message-file", draft)
    return (wrong.returncode == 1 and "area `api`" in wrong.stderr and "no `Verified:`" in wrong.stderr
            and "draft message" in wrong.stderr and clean.returncode == 0
            and git(repo, "log", "--oneline").count("\n") == 1)


@case("--message-file on a merge in progress gives the verdict --rev gives once it is recorded")
def _(repo):
    conflicting_branches(repo)
    run(repo, "git", "merge", "--no-commit", "--no-ff", "side")
    write(repo, "internal/api/handler.go", "r\n", mode="w"); git(repo, "add", "-A")
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("Merge branch 'side'\n")
    bare = hook(repo, "--message-file", draft)
    with open(draft, "w") as handle:
        handle.write("Merge branch 'side'\n\n" + EVIDENCE)
    drafted = hook(repo, "--message-file", draft)
    assert run(repo, "git", "commit", "-q", "--no-verify", "-F", draft).returncode == 0
    recorded = hook(repo, "--rev", "HEAD")
    return (bare.returncode == 1 and "merge resolves" in bare.stderr and "<area>: <outcome>" not in bare.stderr
            and drafted.returncode == 0 and recorded.returncode == 0)


@case("--message-file on a clean merge in progress passes with Git's message")
def _(repo):
    side_commit(repo)
    assert run(repo, "git", "merge", "--no-commit", "--no-ff", "side").returncode == 0
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("Merge branch 'side'\n")
    return hook(repo, "--message-file", draft).returncode == 0


@case("Introduced-by naming a commit this one does not descend from is rejected")
def _(repo):
    other = side_commit(repo, "api: side change")
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    r = commit(repo, "scheduler: renew leases before they expire\n\nBody.\n\n" + EVIDENCE
               + f'Introduced-by: {other} ("api: side change")\n')
    return r.returncode != 0 and "not an ancestor" in r.stderr


@case("Introduced-by naming an ancestor passes, at commit time and under --rev")
def _(repo):
    parent = git(repo, "rev-parse", "--short=12", "HEAD").strip()
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    r = commit(repo, "scheduler: renew leases before they expire\n\nBody.\n\n" + EVIDENCE
               + f'Introduced-by: {parent} ("all: initial import of the scheduler service")\n')
    return r.returncode == 0 and hook(repo, "--rev", "HEAD").returncode == 0


@case("a draft for an amend may cite HEAD's parent in Introduced-by but not HEAD itself")
def _(repo):
    parent = git(repo, "rev-parse", "--short=12", "HEAD").strip()
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    assert commit(repo, "scheduler: renew leases before they expire\n\nBody.\n\n" + EVIDENCE).returncode == 0
    head = git(repo, "rev-parse", "--short=12", "HEAD").strip()
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("scheduler: renew leases before they expire\n\n" + EVIDENCE
                     + f'Introduced-by: {head} ("scheduler: renew leases before they expire")\n')
    citing_head = hook(repo, "--message-file", draft, "--rev", "HEAD")
    with open(draft, "w") as handle:
        handle.write("scheduler: renew leases before they expire\n\n" + EVIDENCE
                     + f'Introduced-by: {parent} ("all: initial import of the scheduler service")\n')
    citing_parent = hook(repo, "--message-file", draft, "--rev", "HEAD")
    return citing_head.returncode == 1 and "not an ancestor" in citing_head.stderr and citing_parent.returncode == 0


@case("a Verified line may name any commit; only Introduced-by is checked for ancestry")
def _(repo):
    other = side_commit(repo)
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    r = commit(repo, f"scheduler: renew leases before they expire\n\nVerified: {other} with these tests; go test ./...; 2 failed as expected\n")
    return r.returncode == 0


@case("--message-file in a linked worktree sees that worktree's merge in progress")
def _(repo):
    git(repo, "branch", "side"); git(repo, "checkout", "-q", "side")
    write(repo, "internal/api/handler.go", "s\n", mode="w"); git(repo, "add", "-A")
    assert commit(repo, "api: side\n\nBody.\n\n" + EVIDENCE).returncode == 0
    git(repo, "checkout", "-q", "main")
    tree = repo + "-tree"
    try:
        git(repo, "worktree", "add", "-q", "-b", "page", tree)
        write(tree, "internal/api/handler.go", "p\n", mode="w"); git(tree, "add", "-A")
        assert run(tree, "git", "commit", "-q", "-m", "api: page", "-m", "Body.", "-m", EVIDENCE).returncode == 0
        run(tree, "git", "merge", "--no-commit", "--no-ff", "side")
        write(tree, "internal/api/handler.go", "r\n", mode="w"); git(tree, "add", "-A")
        draft = os.path.join(repo, ".git", "gc-draft")
        with open(draft, "w") as handle:
            handle.write("Merge branch 'side' into page\n\nResolved the handler.\n\n" + EVIDENCE)
        return hook(tree, "--message-file", draft).returncode == 0
    finally:
        shutil.rmtree(tree, ignore_errors=True)


@case("--message-file --rev refuses --paths, exit 2")
def _(repo):
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write(GOOD)
    r = hook(repo, "--message-file", draft, "--rev", "HEAD", "--paths", "go.mod")
    return r.returncode == 2 and "cannot be combined" in r.stderr


@case("a generated revert is caught by --rev until it carries evidence")
def _(repo):
    git(repo, "revert", "--no-edit", "HEAD")
    before = hook(repo, "--rev", "HEAD").returncode
    msg = git(repo, "log", "-1", "--format=%B").rstrip("\n") + "\n\n" + EVIDENCE
    after = commit(repo, msg, "--amend").returncode
    return before == 1 and after == 0


@case("an invalid configuration file is a clear error, exit 2")
def _(repo):
    with open(os.path.join(repo, ".grounded-commits.toml"), "w") as handle:
        handle.write('areas = "cli"\n')
    r = hook(repo, "--rev", "HEAD")
    return r.returncode == 2 and "list of strings" in r.stderr


@case("a lower-case issue key is a clear error, exit 2")
def _(repo):
    with open(os.path.join(repo, ".grounded-commits.toml"), "w") as handle:
        handle.write('issue_keys = ["proj"]\n')
    r = hook(repo, "--rev", "HEAD")
    return r.returncode == 2 and "issue key `proj`" in r.stderr


@case("a type word listed as an area is a clear error, exit 2")
def _(repo):
    with open(os.path.join(repo, ".grounded-commits.toml"), "w") as handle:
        handle.write('areas = ["fix"]\n')
    r = hook(repo, "--rev", "HEAD")
    return r.returncode == 2 and "not a valid area" in r.stderr


@case("--repo from another directory still sees a merge in progress")
def _(repo):
    conflicting_branches(repo)
    run(repo, "git", "merge", "--no-commit", "--no-ff", "side")
    write(repo, "internal/api/handler.go", "r\n", mode="w"); git(repo, "add", "-A")
    draft = os.path.join(repo, ".git", "gc-draft")
    with open(draft, "w") as handle:
        handle.write("Merge branch 'side'\n\n" + EVIDENCE)
    elsewhere = tempfile.mkdtemp(prefix="gc-elsewhere-")
    try:
        r = subprocess.run([sys.executable, HOOK, "--repo", repo, "--message-file", draft], cwd=elsewhere,
                           capture_output=True, text=True)
    finally:
        shutil.rmtree(elsewhere, ignore_errors=True)
    return r.returncode == 0, r.stderr


@case("an autosquash commit is accepted when made and flagged in a range")
def _(repo):
    write(repo, "internal/scheduler/worker.go"); git(repo, "add", "-A")
    made = commit(repo, "fixup! scheduler: renew leases before they expire\n")
    r = hook(repo, "--range", "HEAD~1..HEAD")
    return made.returncode == 0 and r.returncode == 1 and "autosquash" in r.stderr


def main():
    failures = 0
    for name, fn in CASES:
        repo = fresh()
        try:
            ok = bool(fn(repo))
        except Exception as error:  # a crash is a failure with its reason
            ok, name = False, f"{name} ({type(error).__name__}: {error})"
        finally:
            shutil.rmtree(repo, ignore_errors=True)
        failures += not ok
        print(("ok   " if ok else "FAIL ") + name)
    print(f"\n{len(CASES) - failures} of {len(CASES)} hook-mode cases pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

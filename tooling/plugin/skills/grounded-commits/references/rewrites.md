# Grounded Commits: evidence after a rewrite

Rebase, cherry-pick, squash and amend reuse message text in a new commit, and
whoever makes the new commit owns its evidence. Keep `Verified: final
contents` only when you re-ran the check on the new commit, or its tree is the
tree that was tested — `git rev-parse <tested>^{tree} <new>^{tree}` prints the
same hash twice. A message-only amend keeps the tree; a replay onto a moved
base usually changes it, even when it applied cleanly, and a re-run on the tip
covers the tip alone. Otherwise rebind before you create the new commit:
re-run the check on the new tree; or replace `final contents` with "the tree
before the rewrite", keep the check and its outcome, and add a
`Not-verified:` for the new tree scoped to the claim (`behaviour
preservation`, `reproduction`, `performance effect`, else `final contents`)
whose reason says what the rewrite did to this commit's files, "the fold
changed no file this commit touches and the suite was not re-run" where
`git diff <tested> <new> -- <its paths>` prints nothing, else that it did. Never name the replaced commit by hash: nothing keeps it
reachable, and a reader who cannot open it learns only that the published
tree was not tested. Wrap the rebound lines like any other. Check every
commit a rewrite produced, not only the tip; where the branch will land by
squash, the rebinding goes into the composed message, since the branch's own
commits do not land. Rewrite only commits that have not landed on a shared
branch, and a pull-request branch only before its final approval, when its
fix-ups are folded; an approved head and a landed commit are never rewritten —
report the problem to the user instead.

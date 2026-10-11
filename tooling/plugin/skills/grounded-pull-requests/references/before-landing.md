# Grounded Pull Requests: before final approval

The branch's commits land as the objects they were reviewed as, so the one
rewrite the branch gets comes before its final approval, not after it. Once
the reviewers' findings are settled: reword any message the review changed
and fold the fix-ups into the commits they correct; rebind the evidence of
every commit the fold produced, not only the reworded ones, since folding
changes trees (grounded-commits, *After a rewrite*); sign the rewritten
commits as you make them where the repository keeps author signatures
(`commit.gpgsign`, or `-S` on the rebase), since a rewrite replaces the
signed objects, and never with plumbing such as `git commit-tree`, which
ignores `commit.gpgsign` and signs only when passed `-S`; push once; and comment with one sentence naming the
previous head's hash, what the fold changed, and whether the patch is the one
that was reviewed. `git diff <previous-head> HEAD` printing nothing shows
that the fold and the rewords changed no content; where it prints something,
or a message changed, attach `git range-diff <target> <previous-head> HEAD`,
which shows the change commit by commit, messages included, with
`--remerge-diff` where the branch keeps merge commits. An attachment sits
inside a collapsed block, a `<details>` element whose `<summary>` names the
command, with a blank line after the summary so the fenced block inside
renders, which GitHub and Forgejo both need. For example:

```
Head 3e7a1c5 folded its two fix-ups and reworded "stream CSV exports" with the Verified line for the re-run; the patch is unchanged (range-diff attached).
```

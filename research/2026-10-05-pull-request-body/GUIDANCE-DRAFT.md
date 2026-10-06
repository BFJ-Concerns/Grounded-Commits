# Pull requests (DRAFT distillation to adapt; not a rule; from REPORT.md, 5 October 2026)

> **Research record.** The finished guidance is [`guidance/pull-requests.md`](../../guidance/pull-requests.md), which differs from this draft in these ways: the lead may state the objective without an issue and is a permitted overlap with the commit; the title follows the repository's header profile and keeps a lone native subject; `Try` says what a step should show; `Check` carries gaps and questions as well as requests; `Not in this PR` also covers a deliberate absence a reviewer would expect; the landing comment always carries `git range-diff`; and landing itself is optional, in [`guidance/landing.md`](../../guidance/landing.md).

The branch lands by rebase and fast-forward: no pull-request text enters history. The commits are the record; the body is a short brief for whoever reviews now. This replaces the harness default template.

## Title
The outcome of the whole branch in commit-subject grammar (`area: outcome`, within 72). One commit: that commit's subject. Several: what the series delivers. No type prefix, issue key or status word; draft is the forge's mechanism.

## Body
Markdown, one paragraph per line. Omit a section with nothing to say; never write a placeholder. Soft upper bounds: one commit 50 words, a series 150, several outcomes 250.

1. **Lead** (required, unheaded): what the reviewer is asked to accept, with a plain issue link. One commit: `Delivers <issue URL> in one commit.`
2. **`### Read`** (several commits or a stack): which commits are preparation and which carry the behaviour change; for a stack, the base and prerequisite PR.
3. **`### Check`** (when there is something specific; never invented), any of: what to scrutinise; what you could not verify, in one line naming the commit whose `Not-verified:` records it; a question ending in `?` with what turns on it. Requests, never results.
4. **`### Try`** (when it can be exercised or seen): steps, and screenshots captioned with environment and commit. How to see it, not what you saw.
5. **`### Not in this PR`** (when the request exceeds the branch): each item with its disposition: tracking issue, "not planned", or "no issue exists". Invent nothing.

## Never in the body
Commit-message text or trailers, copied or paraphrased. Subject lists, file lists, diff narration. Results or assurances ("tests pass", "safe"). Instructions to an automated reviewer, or a claim that a reviewer agreed. Checklists. Hashes or CI links; name commits by subject. Closing keywords in title or body; link plainly, close after landing. Model names, session artefacts, CI tokens.

## During review
After every push, overwrite what is no longer true and remove settled questions; never append dated notes. One comment per push names the findings addressed or declined; answer declined ones in their thread and fold a durable reason into the commit's `Considered and rejected:`. Push fix-up commits during a round, not force-pushes. A body edit triggers nothing: re-request review when it changes a premise.

## Landing
Fold fix-ups, reword changed commits, rebase, push once; comment with the reviewed head and `git diff <reviewed-head> HEAD` (`git range-diff` when not empty). Ready: no open question, `Not in this PR` current, commit messages true of folded contents, forge green; no ready marker. Then close each fully delivered issue by hand. On GitHub, land by pushing the approved tip to the target branch, from an identity allowed to bypass branch protection, after confirming approval and green checks on that exact tip; never "Rebase and merge" or a merge queue, which create new commits.

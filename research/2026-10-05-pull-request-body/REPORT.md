# The pull-request body when branches land by rebase and fast-forward

What a pull-request body contains, and how it is kept, where agents open most pull requests, humans and automated reviewers read them, every commit carries its own account in the Grounded Commits format (`../2026-10-02-commit-message-formats/REPORT.md`), and the branch lands by rebase and fast-forward so that no pull-request text enters history. The target forge is GitHub; Forgejo's behaviour is noted where it differs. Written 5 October 2026; sources and read dates are at the end.

## The answer

The body is a short brief for whoever is reviewing now, not a second account of the change. The commits own the problem, the approach, the alternatives, the limits and the verification record; the body owns only what no commit can carry: where to start, what to scrutinise, what the author could not verify, how to see the change work, and what the request asked for that the branch does not deliver. It opens with one or two unheaded sentences naming the outcome and the request, then carries up to four headed sections, each omitted rather than padded: **Read**, **Check**, **Try** and **Not in this PR**. Every sentence in it is a pointer, a request or a question; none is a result or an assurance. The title is the outcome of the whole branch in the commit-subject grammar, identical to the subject when there is one commit. Issues are linked neutrally and closed by hand after landing. Commits are named by subject, never by hash, so a rebase does not stale the body, which is rewritten in place after every push; what changed goes in one comment per push, declined findings are answered in their threads, and any durable reason is folded into the relevant commit before landing. A one-commit body is typically three lines; a series fits in 150 words, several outcomes in 250. Nothing needs tooling: the checks are a reviewer's first glance at the body and one `git diff` before landing.

## Specification

### Who owns what

| Information | Home | What the body contributes |
|---|---|---|
| The request and its acceptance criteria | The issue or brief | A neutral link, in the lead |
| Problem, approach, alternatives, limits, breaks, verification | The commit messages | A pointer by subject; one line naming a gap a reviewer must not miss |
| The implementation | The diff | Reading order, entry point, interactions between commits |
| Current check results | The forge's checks on the head | Nothing |
| Findings, replies, declined findings, approval | Review threads and the forge's review record | Nothing durable |

An ownership rule, not a ban on shared words: a scope phrase or the name of a gap may appear in both places. It forbids a copied problem paragraph, a commit list, a trailer block or a testing summary. A body link cannot repair an inadequate commit message; a reviewer who finds the rationale missing sends the commit back.

### Title

Required. The outcome of the branch as a whole, in the commit-subject grammar: `area: outcome`, lower case after the colon, no full stop, within 72 characters. For one commit the title is that commit's subject; a mismatch visible in the forge's commit list means one of them is wrong. For a series it states what the series delivers, which no single subject does; for several deliberate outcomes it names the grouping in plain words and the lead enumerates. No type prefix, issue key or status word. Draft state is the forge's mechanism, GitHub's draft flag or Forgejo's configured WIP prefix (`WIP:` and `[WIP]` by default; vendor documentation, read 5 October 2026); a word in the title is not a substitute, and draft does not silence a bot configured to review drafts.

Judgement: one grammar gives an agent one phrasing to produce, not two, and a title written without one drifts toward a noun phrase that states no outcome.

### Body

Markdown rendered by the forge. GitHub renders a single newline in pull-request text as a hard line break (GitHub formatting documentation, read 5 October 2026), so a paragraph is one source line. Headings are `###`. A section whose honest content is "nothing" is omitted; a heading followed by filler, "N/A" or a restatement of the title is a defect the reviewer sends back before reading code.

| Section | Status | Purpose |
|---|---|---|
| Lead (unheaded) | Required | One or two sentences: what the reviewer is asked to accept, and a neutral link to the request. Gives an automated reviewer its objective and a human their frame. Never a paraphrase of a commit body. |
| `### Read` | Conditional: several commits, a stacked member, or a diff whose shape is not obvious | How the branch is built and where to start: which commits are preparation and which carry the behaviour change, what invariant spans them, which file to open first. For a stacked member, the base branch and the prerequisite pull request. Not a list of subjects, which the forge shows, and not a list of files. |
| `### Check` | Conditional: something specific to scrutinise, a gap a reviewer must weigh, or a decision to make; never invented to fill the section | What the author wants scrutinised, what they could not verify, and what they want decided. Requests and questions only, each question with its consequence. |
| `### Try` | Conditional: the change has behaviour a reviewer can exercise or see | Steps to exercise it, and screenshots or recordings for anything visual, captioned with the environment and the commit shown. How to see it, not what was seen. |
| `### Not in this PR` | Conditional: the request, or an earlier revision of the branch, exceeds what it delivers | Each omitted item with its disposition: a link to the issue that tracks it, "not planned", or "no issue exists". Nothing invented. |

**Lead.** For one commit, as short as "Delivers [#318](url) in one commit."; the subject is the title and the commit body is one click away. For a series, the outcome and the request in a sentence; for several outcomes, one sentence each naming its carrying commit by a subject fragment, never by hash, because hashes change when fix-ups fold. Where no issue exists, the lead states the objective instead.

**Check** has three kinds of line. An honest body may have only one of them, or none, in which case the section is left out:

- *Scrutinise*: the decision the author is least sure of, the part most likely to be wrong, the interaction between commits a per-commit read would miss.
- *Could not verify*: anything a commit records under `Not-verified:` that a reviewer must weigh before approving, in one line naming the commit by subject: "Production-volume replay not run; the streaming commit's trailer says why." This is a deliberate overlap with commit text, bounded to a line, because an approval given on the strength of `Verified:` lines three clicks away must not miss the gap beside them.
- *Decide*: a question for the reviewer, ending in a question mark, with what turns on it.

A `Check` that says the change is safe, well tested or complete has been written backwards: what ran lives in the commits' `Verified:` trailers. If a design choice is deliberate and likely to be flagged, one sentence may point at the commit whose `Considered and rejected:` gives the reason; the body never argues the point itself.

**Try** gives the steps and the pictures. The observed result is a `Verified:` line on the commit, not a sentence in the body, which may say "the capture shows the result". An exercise the author did not perform is a request under `Check`, never a step whose result is implied.

**Not in this PR** names what was requested and is absent, each with a disposition. No "follow-up PR" nobody has planned and no issue that does not exist. Something a review round removed from the branch is listed here too.

### Length

Soft upper bounds, not targets: one commit, three lines and under 50 words; a series, 150; several outcomes, 250, excluding images and any reviewer-product region. An overrun is the reviewer's cue to look for narration, repetition or assurance, which is what agent bodies overrun with: a median of 355 words against 56 for human-written ones from the same authors and repositories (Watanabe et al., measurement, read 5 October 2026). The budgets are a judgement; no study ties a word count to a review outcome.

### Keeping the body during review

The body describes the current head, always. After every push the author re-reads it and corrects what is no longer true: a settled `Check` line goes, a delivered `Not in this PR` item goes, a new question is added. It is overwritten in place, never appended to with dated notes, so a reviewer arriving at round three reads one true brief; the forge keeps an edit history, though not an unlimited one (Forgejo retains up to 20 revisions, per its pinned source read on 3 October 2026). Because commits are named by subject, a rebase alone changes nothing in it.

What a push changed goes in one ordinary comment per push: which findings it addresses, which it declines and why. Declined findings are also answered in their thread, and the body never carries an author-written claim that a reviewer agreed. A reason a later reader would need becomes a `Considered and rejected:` sentence in the relevant commit when fix-ups fold.

A body edit is not a push. GitHub Actions' default `pull_request` trigger omits `edited`, and Copilot reviews once unless configured to review each push (vendor documentation, read 5 October 2026). When an edit changes a premise a reviewer acted on, the author re-requests review through the forge; a review given against a body that no longer matches the code is provisional.

During a round, push fix-up commits rather than force-pushing, so the incremental diff and inline threads keep working; LLVM's guidance makes the same choice because fix-ups make it "easier for GitHub to track the context of previous review comments" (project policy, read 5 October 2026).

### Landing

Before landing, fold the fix-ups into the commits they correct, reword any commit the round changed, rebase onto the target, and push once. That force-push defeats the incremental view, so its comment states the head that was reviewed and the result of `git diff <reviewed-head> HEAD`, empty when the fold changed only messages; when it is not, or messages were reworded, `git range-diff` shows the correspondence commit by commit. Both are one command.

Ready to land means: no open question in the body, `Not in this PR` current, every commit message true of its folded contents, and the forge's own state green (not draft, approved, checks passed on the rebased tip). No landing marker, hash or "ready" sentence goes in the body. On GitHub, "dismiss stale approvals" dismisses approvals when a push affects the pull request's diff (vendor documentation, read 5 October 2026); the diff statement is what makes any re-approval quick.

After landing, the author closes each issue the branch delivered in full, in a comment naming the landed commit: one action per completed issue, the cost of the neutral-link rule.

### Reviewer products that write into the body

CodeRabbit writes a summary into the description by default; `high_level_summary_in_walkthrough` puts it in the walkthrough comment and `high_level_summary: false` stops the description write (vendor documentation, read 5 October 2026). Bugbot writes into the description by default (vendor documentation, read 3 October 2026). Use comment mode where offered; otherwise place the placeholder at the end so the brief comes first, and never edit the product's region. Its summary is diff narration, not evidence.

### Never in the body

- A copy, paraphrase or summary of any commit message, its `Verified:` lines or its trailers; a list of changed files or a narration of the diff. Both are adjacent in the forge.
- A result ("all tests pass", "verified locally") or an assurance ("thoroughly tested", "safe"). What ran is on the commit; what the author wants run is a request under `Check`. In a replication package (measurement, anonymous source, 250 trials per condition, read 5 October 2026), unsupported assurances raised two open-weight reviewer models' approvals of known-bad patches from 54.4% to 70.0% and from 23.2% to 42.0% against a hedged baseline.
- Anything addressed to an automated reviewer: an instruction to approve, ignore a class of defect, skip a path, or treat a finding as resolved. A question is welcome; pre-deciding its answer is not.
- An author-written claim that a reviewer approved, agreed or withdrew a finding. That lives in the thread.
- Checklists, ticked or unticked. A tick is not evidence, and some bots execute a ticked box as a command (Renovate's rebase checkbox, read 3 October 2026).
- A commit hash, a CI-run link, or any pointer a rebase invalidates. Name commits by subject.
- A closing or reopening keyword before an issue reference, anywhere, including the title.
- Model names, session paths, plan steps, tracking codes, work diaries; instructions to future agents or readers; CI control tokens, even quoted.

### Forge differences where they bite

**Closing keywords act even though the text does not land.** On GitHub a `closes #N` closes the issue when the pull request merges into the default branch and is ignored for any other target (vendor documentation, read 5 October 2026). On Forgejo the reference parser reads the title as well as the body, and the merge handler closes every referenced issue on merge with no default-branch test, subject only to the merger's permission (pinned source at `8d24b7d5`, read 5 October 2026). A control whose behaviour differs by forge and target branch is never used: link issues neutrally and close them after landing. A rule with no exception cannot be misapplied, and it decouples issue state from a mutable description and from a stacked member merging into its parent.

**GitHub's "Rebase and merge" is not a fast-forward.** It "always updates the committer information and creates new commit SHAs" and adds commits "without commit signature verification" (vendor documentation, read 5 October 2026). The decided route fast-forwards the target to an already-rebased, already-checked tip. A merge queue is no substitute: its methods are merge, rebase and squash, and it builds its own commits (vendor documentation, read 5 October 2026). On GitHub the route is therefore a push of the approved tip to the target branch, after which GitHub marks the pull request merged, because a pull request "can be marked as merged if its head branch commits become reachable from the base branch outside that pull request" (vendor documentation, read 5 October 2026). Branch protection lets only identities permitted to bypass it push directly to a protected branch, so the landing identity needs that permission, and the landing step itself must confirm approval and passing checks on the exact tip before it pushes. For a pull request from a fork, the commits that land must be the pull request's own head commits for GitHub to record the merge, so a rebase or a reworded message has to reach the contributor's branch first; GitHub lets maintainers push there only when the contributor has allowed edits from maintainers, on a user-owned fork (vendor documentation, read 5 October 2026). Pull requests from outside contributors are otherwise an open case for this design.

**Forgejo's merge templates.** Under the `rebase` style a `REBASE_TEMPLATE.md` "modifies the message of the last commit" and can substitute `${PullRequestDescription}` into it; `fast-forward-only` keeps the original hashes and creates no message (Forgejo documentation and issue 2345, read 5 October 2026). A repository on the `rebase` style must not use a template that inserts the description, or the body enters history after all.

**Stacked pull requests.** A stacked member's `Read` names its base branch and prerequisite pull request, updated when the parent lands; the neutral-link rule already removes the early-close hazard on Forgejo. **Markdown.** Essential facts go in visible prose, not HTML comments, collapsed sections or images, which a reader or tool may not expand.

## Worked examples

All fictional. The repository is `reports`, the forge is GitHub, commits follow the agreed commit format, and the body is shown beside the commit subjects so that the absence of repetition is visible.

### A. One commit

Commit on the branch:

```
export: close the query cursor when the client disconnects
```

Title: `export: close the query cursor when the client disconnects`

Body:

```
Delivers https://github.com/example/reports/issues/331 in one commit.

### Check
The cursor is closed from the response's context-done hook; check that nothing else in handler.go relies on that hook running exactly once.
Reproduction against staging not run, only with a local proxy; the commit's trailer says why.
```

Three lines of prose. The problem, the approach and what ran are in the commit message, one click away; the body says what the author wants looked at and what they could not do.

### B. Four commits, one outcome, as opened

Commits on the branch, oldest first:

```
export: extract row serialisation from the buffered writer
export: add a streaming writer behind the existing interface
export: stream CSV exports instead of buffering them in memory
docs: describe the X-Row-Count trailer for export clients
```

Title: `export: stream CSV exports instead of buffering them in memory`

Body:

```
Exports of over a million rows kill the worker at 2 GB (https://github.com/example/reports/issues/318). This branch streams rows as the cursor advances and moves the row count to a trailer.

### Read
The first two commits are mechanical and keep the buffered path; the third, "stream CSV exports", is the behaviour change. Start with export/stream.go.

### Check
Content-Length disappears from export responses (Breaking-Change trailer on the streaming commit). Do we know of any client that reads it?
Is 4 KiB the right flush threshold, or should it track the row size, as the buffered path effectively did?
Production-volume replay not run; the streaming commit's trailer says why.

### Try
Against staging, request /exports/1.4m.csv with curl -N and watch worker RSS; the capture shows the result.
![worker RSS before and after, staging, "stream CSV exports" commit](https://github.com/example/reports/assets/rss.png)

### Not in this PR
A progress signal for clients that read Content-Length. Issue 318 did not ask for it; no issue exists.
```

Under 150 words. Nothing in it restates a subject, lists a file set or states a result; the figures are on the commits.

### C. The same pull request after one review round

The reviewer asked for the flush threshold to be configurable, flagged that the docs commit also changed an unrelated heading, and raised a concern about memory if a client stalls mid-stream, which the author judged out of scope for this branch.

Comment posted with the push:

```
Pushed two fix-ups. Flush threshold is now a config key (fix-up for the streaming commit); the stray heading change is dropped from the docs commit. Declined the stalled-client concern as a separate problem that predates this branch, see the thread; I've opened issue 334 for it and listed it below.
```

Body, rewritten in place:

```
Exports of over a million rows kill the worker at 2 GB (https://github.com/example/reports/issues/318). This branch streams rows as the cursor advances and moves the row count to a trailer.

### Read
The first two commits are mechanical and keep the buffered path; the third, "stream CSV exports", is the behaviour change. Start with export/stream.go.

### Check
Content-Length disappears from export responses (Breaking-Change trailer on the streaming commit). Do we know of any client that reads it?
Production-volume replay not run; the streaming commit's trailer says why.

### Try
Against staging, request /exports/1.4m.csv with curl -N and watch worker RSS; the capture shows the result.
![worker RSS before and after, staging, "stream CSV exports" commit](https://github.com/example/reports/assets/rss.png)

### Not in this PR
A progress signal for clients that read Content-Length. Issue 318 did not ask for it; no issue exists.
Back-pressure when a client stalls mid-stream; tracked in https://github.com/example/reports/issues/334.
```

The settled threshold question is gone; the declined finding has become a `Not in this PR` line with a tracker; nothing says "round 2", and no hash anywhere needs updating. When the reviewer approves, the author folds the two fix-ups into their commits, rewords the streaming commit's `Verified:` line for the re-run, rebases onto `main`, pushes once, and comments:

```
Folded the fix-ups and rebased onto main at 7c1e2d9. git diff 3e7a1c5 HEAD is empty; the four commit messages are the only change since review (range-diff attached).
```

The body is unchanged by that push because nothing it says has stopped being true. After the fast-forward, the author closes issue 318 with a comment naming the landed streaming commit.

## Why

No controlled comparison of pull-request body formats was found for any reader; the search was bounded. What follows separates measurement, documentation and judgement.

### The human reviewer

Reviewers start from the description: ten experienced developers performing 25 reviews explicitly used the title and description in 21 (Wurzel Gonçalves et al., measurement, read 5 October 2026), which shows use, not that a longer description improves detection. Nine of ten interviewees in an earlier study wanted motivation alongside what changed (Ram et al., measurement, read 3 October 2026). Google's guidance asks a description for the problem, the approach and its shortcomings (project policy, read 5 October 2026); it assumes the description enters history, so here that argument transfers to the commits. What a reviewer cannot get from commits or diff is where the author's own doubt lies and what they could not check; that is `Check`. Meta's finding that a test plan is "a communication channel between the author and the reviewers, not a proof that the changes were tested" (Chen et al., read 3 October 2026) is why `Check` asks rather than asserts, and why no section is named for evidence.

Pointing at commits costs a click; a one-line lead and a one-line gap statement keep the reader from opening every message to find the scope or the untested case. Whether this saves review time overall is unmeasured.

### The automated reviewer

The description is a demonstrated input. Adding it to a diff hunk raised four closed models' quality-estimation F1 from 36.08 to 62.12 in ContextCRBench, and adding the issue took it to 64.74 (measurement, read 5 October 2026; a benchmark, not a comparison of body formats). CodeRabbit extracts objectives from the description and related issues; Copilot uses identifiers in the description to decide when to retrieve external context (vendor documentation, read 5 October 2026). Hence the lead's one-sentence objective and neutral issue link: cheap, and demonstrably consumed. Whether any of these products reads commit messages is undocumented, so the lead carries the objective even though a commit states it; this and the gap line are the two deliberate overlaps, each bounded to a sentence.

Wording moves weaker models: the replication package shows unsupported assurances raising approvals of known-bad patches by 15 to 19 points on two open-weight models, with no result for commercial reviewers. A body with no assurance and no instruction aimed at the reviewer removes that lever. Whether `Check` directs a bot's attention usefully is unmeasured.

### The agent author

An agent at pull-request time holds the request, what it observed, what it changed and what it ran; it does not thereby know that everything requested happened or that a check passed. Its known failures are boilerplate from a harness template (the shipped Claude Code default is a `## Summary` / `## Test plan` body with checklist placeholders, read on 3 October 2026), claimed work that was not done (45.4% of the 432 misaligned descriptions Gong et al. classified claimed unimplemented changes; measurement, read 5 October 2026; the inconsistent subset, not all agent pull requests), and length. Headings stay because templates are not worthless: Li et al. found both contributors and maintainers rated them useful while complaining of excessive and irrelevant fields (measurement, read 5 October 2026).

The format steers without tooling by making every section a question whose honest answer may be "nothing", with omission the rule and padding the defect. No section's name invites results, and results are banned, so the invented test plan has nowhere to go; the gap line gives honest absence a place; `Not in this PR` gives the exit that phantom claims lack; the budgets and the narration ban give a reviewer a one-glance rejection criterion; the three-line shape for one commit removes the blank page templates fill. Repository guidance must say this format replaces the harness default. Cost: one read of a short body before the diff, which the reviewer does anyway.

### The later reader

The later reader with a clone gets everything from the commits, by design. A reader on the forge finds the final body, true of the head that landed, a comment per push, threads holding the dispositions, and the forge's record of approvals and checks. The one durable thing review produces, a reason for declining a design finding, is folded into a commit's `Considered and rejected:` before landing. No synthetic series commit, final-commit essay or body export is added.

## What was rejected

**A body that copies the commit message.** An earlier design, made for squash and merge-commit landing, put a mechanically derived copy of the head commit's message at the top of the body, checked byte for byte by a lint, with review material optional below a `---` rule, marker comments around the text meant to land, and a read-back of the landed message. Every part of it controlled what entered history, and under fast-forward nothing does; what remained was a copy of text the reviewer can read in the commit list, plus tooling to keep the copy honest. Read-back's purpose, confirming that what lands is what was reviewed, survives as the `git diff` statement in the landing comment.

**An Evidence section** for manual observations, decisive CI runs and coverage gaps. Rejected: a heading named for evidence is the slot an agent fills with a test plan, and it mandates writing a manual result in both the body and the commit's trailer. The one thing it protected, a gap a reviewer must not miss, is kept as a single line under `Check`, phrased as a gap rather than a result.

**A final-tip pointer in the body.** Rejected: a hash or CI-run link goes stale on every rebase and fold, and the forge shows the head and its checks beside the body. The landing comment carries the reviewed head instead.

**A conditional closing keyword**, permitted when the branch delivers the whole issue and is not stacked. Rejected for the unconditional rule: the condition coupled two edits across rounds, and Forgejo's title parsing and branch-agnostic closing make the keyword differ by forge.

**A title free of the subject grammar.** Rejected: two phrasings of one change, and the weaker survives.

**A flat word budget.** Rejected for tiered upper bounds.

**Post-landing maintenance rules.** Rejected: the body exists for the review now.

**A `Requested:` grammar, `Not done:` in the commit body, a per-round body section, checklists and templates as content sources.** Rejected: no tool parses a line grammar; what the request asked for and the branch omits is a property of the pull request, not a commit; the timeline is the forge's; checkers verify ticks, not truth, and API-created pull requests get no template.

**Reviewer-product summaries in the body.** Bounded, not rejected: fighting a default the product resets on every review is ceremony.

## What would change the answer

- **A scored sample of agent-written bodies under this format.** If `Check` fills with "check that the tests pass", the gap line becomes a results line, or `Not in this PR` fills with invented follow-ups, the sections are not steering and need tighter definition or a linter rule on the forbidden phrases.
- **Evidence that the automated reviewers in use read commit messages.** The lead shrinks to the issue link and the gap line may go.
- **A measured difference** in review time or defects missed between this format, a free-form body and a commit-copy body on matched changes, with link-following cost measured. None exists.
- **A forge route that lands body text**, such as squash, merge commits or a Forgejo `rebase` template.
- **Issue-closing automation that a hand close cannot replace**, which reopens the keyword question.
- **A reviewer product that reads replies and resolved threads**, which makes the comment per push a convenience for humans.

## Origins

Two designers, one on Claude Fable 5.1 and one on GPT-6 Astra, proposed independently; each then judged the other's proposal and wrote a synthesis. This report is the Fable synthesis, edited after the round as the last two rows record.

| Decision | From |
|---|---|
| Lead plus `Read`, `Check`, `Try`, `Not in this PR`; omit rather than pad | Fable |
| Ownership table deciding which home owns each kind of information | Astra |
| Title in commit-subject grammar; one commit's title is its subject | Fable |
| Verification gap surfaced in one line under `Check`, as a gap not a result | Astra's principle, placed in Fable's section |
| `Try` carries steps and pictures only; results stay on the commit | Fable, repairing its own example |
| No hashes or CI-run links in the body; commits named by subject | Fable |
| Neutral issue links only; close by hand after landing | Astra |
| Body edits retrigger neither CI nor bots; re-request review on a changed premise | Astra |
| Overwrite in place; one comment per push; declined findings in threads; durable reasons folded into commits | Fable |
| Fix-up commits during a round; fold, rebase, push once at landing; `git diff` statement, `range-diff` when it is not empty | Fable, with `range-diff` from Astra |
| No instruction to automated reviewers; no author-written claim of reviewer agreement | Astra |
| Tiered soft budgets as upper bounds (50 / 150 / 250) | Astra's shape, Fable's lower numbers |
| GitHub "Rebase and merge" named as outside the landing route | Astra |
| Forgejo `REBASE_TEMPLATE.md` warning, scoped to the `rebase` style | Fable |
| Stacked member names base and prerequisite in `Read` | Both |
| Reviewer-product summaries to comment mode or an end placeholder | Both |
| No post-landing rules | Fable |
| `Check` conditional, never invented | Astra's judgement, applied after the round |
| GitHub landing by a permitted push of the approved tip, with the fork condition; no merge queue; stale approvals dismissed only by pushes that affect the diff | Corrected after the round against GitHub's documentation |

## Sources

Read on 5 October 2026 unless stated. Measurements: Watanabe et al., "On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub", https://arxiv.org/html/2509.14745v3; Gong et al., "Analyzing Message-Code Inconsistency in AI Coding Agent-Authored Pull Requests", https://arxiv.org/html/2601.04886v2; ContextCRBench, https://arxiv.org/html/2511.07017v2 (Table 5); Wurzel Gonçalves et al., "Code Review Comprehension", https://arxiv.org/html/2503.21455v1; Li et al., "To Follow or Not to Follow: Understanding Issue/Pull-Request Templates on GitHub", TSE 2022, https://whystar.github.io/res/paper/template-TSE2022.pdf; the AI-reviewer replication package, https://github.com/karlita604/AI-Reviewer-Replication-Package (README and `results/analysis/approval_rates.csv`). Vendor documentation: GitHub, about merge methods, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github; GitHub, pull request merges (indirect merges), https://docs.github.com/en/pull-requests/reference/pull-request-merges; GitHub, managing a merge queue, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue; GitHub, allowing changes to a pull request branch created from a fork, https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/allowing-changes-to-a-pull-request-branch-created-from-a-fork; GitHub, linking a pull request to an issue, https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue; GitHub, about protected branches, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches; GitHub, basic writing and formatting syntax, https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax; GitHub, events that trigger workflows, https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows; GitHub, changing the stage of a pull request, https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/changing-the-stage-of-a-pull-request; GitHub, about stacked pull requests, https://docs.github.com/en/pull-requests/get-started/about-stacked-prs; GitHub Copilot code review, https://docs.github.com/en/copilot/concepts/agents/code-review; CodeRabbit configuration reference, https://docs.coderabbit.ai/reference/configuration; CodeRabbit, context engineering, https://www.coderabbit.ai/blog/the-art-and-science-of-context-engineering; Forgejo configuration cheat sheet, https://forgejo.org/docs/latest/admin/config-cheat-sheet/; Forgejo merge message templates, https://forgejo.org/docs/latest/user/repository/merge-message-templates/; Forgejo linked references, https://forgejo.org/docs/latest/user/collaboration/linked-references/; Forgejo issue 2345, https://codeberg.org/forgejo/forgejo/issues/2345; Forgejo pinned source, https://codeberg.org/forgejo/forgejo/src/commit/8d24b7d52df327118cd776cf461d34e52e0ec1ce/models/issues/issue_xref.go and .../services/pull/merge.go. Project policy: Google, writing good CL descriptions, https://google.github.io/eng-practices/review/developer/cl-descriptions.html; LLVM GitHub guidance, https://llvm.org/docs/GitHub.html; Linux kernel coding-assistants rules, https://docs.kernel.org/process/coding-assistants.html. Read on 3 October 2026: Ram et al. (FSE 2018) on code-change reviewability, https://anandsaw.github.io/publications/fse2018.pdf; Chen et al. (Meta), "Leveraging Test Plan Quality to Improve Code Review Efficacy", https://research.facebook.com/file/596469272122518/Leveraging-Test-Plan-Quality-to-Improve-Code-Review-Efficacy.pdf; Forgejo pinned source for description revision history, https://codeberg.org/forgejo/forgejo/raw/commit/8d24b7d52df327118cd776cf461d34e52e0ec1ce/models/issues/content_history.go; the Claude Code package's pull-request template, https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.288.tgz; Cursor Bugbot documentation, https://cursor.com/docs/bugbot; Renovate's body controls, https://raw.githubusercontent.com/renovatebot/renovate/b12f39eed0b37cddc1ca4b41389414ce54d22f82/lib/workers/repository/update/pr/body/controls.ts.

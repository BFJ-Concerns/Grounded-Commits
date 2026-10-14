# Commit messages: the evidence behind the format

The published studies, documented tool behaviour and reasoning behind
[`guidance/commit-messages.md`](../guidance/commit-messages.md), which
specifies the format; this file does not repeat it. Each claim links to its
source. Measurement, mechanism and opinion are kept apart and labelled.
Sources were read on 2 October 2026 unless a later date is given.

Nothing here is an equal-information comparison of formats for agent readers
or for agents writing as they work. Experiments on messages generated after
the fact exist and are reported where they bear on the question.

## Agent writers

The format asks for what an agent doing the task has and an after-the-fact
generator lacks. Mechanism: Aider's auto-commit passes the chat history to the
message call; VS Code's generator receives diffs and recent subjects, not the
task conversation; opencode's GitHub handler asks for a summary under 40
characters ([Aider](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py),
[VS Code](https://github.com/microsoft/vscode/blob/261d41b4cc914eced6408665704d7742c473a5f6/extensions/copilot/src/extension/prompt/vscode-node/gitCommitMessageServiceImpl.ts),
[opencode](https://raw.githubusercontent.com/anomalyco/opencode/aec0b9a6d8898f68f923aaf08b7306d931fd9d76/packages/opencode/src/cli/cmd/github.handler.ts)).

A problem-first body targets the measured failure. Measurement: of 108
ChatGPT-generated messages, 38 lacked context and 6 hallucinated rationale.
The categories overlap, and they come from generation after the fact, not
from an agent doing the task ([Table 6](https://arxiv.org/html/2401.17622v2)).
A required explanation field raised what-plus-why content from 17.2% to 76%,
in a student study that bundled labels, obligation and interface
([source](https://arxiv.org/html/2304.13887)). About 44% of 1,597 human
messages lacked the what or the why
([source](https://arxiv.org/html/2202.02974)).

The provenance rules rest on one observation, not an experiment. A history of
144 agent-written commits, read in full before it was first published, showed
three things. Five bodies opened "The author asked for" or similar, where the
requester was the committer. 44 opened "A reviewer reported", so a phrase
meant to mark footing had become house style. And 21 carried a `Verified:`
line naming a pre-rebase commit beside `Not-verified: final contents`. None
of the 21 tested revisions was reachable from the branch to be published:
four survived only under a pull-request ref, the rest only as unreachable
objects in one clone. Mechanism: in a single-maintainer repository the
requester is the committer, so "the author asked" adds nothing the author
line lacks, and once published it states the motive to the audience it
concerns. A phrase repeated at the start of a third of the bodies stops
marking anything. And a hash the reader cannot open makes the newest part of
the history read as untested. The guidance therefore asks for the footing of
a claim (requested, reported, reproduced or inferred) and a source the reader
can open, and forbids repeated process phrasing that adds neither. In the
same history, a phrase from the guidance's own worked example turned up,
partly, in ten of 19 pull-request bodies. That makes an example phrase a
plausible source of repetition, though a controlled comparison would be
needed to show it caused it. Opinion: an honest floor worded as an absence
survives publication; one worded as an attribution does not.

The nullable evidence pair rests on precedent and a transferred argument.
Precedent: the kernel requires assistant-generated fixes to say so when the
fix could not be built, tested or reproduced
([kernel](https://docs.kernel.org/process/coding-assistants.html)), and
Phabricator's required Test Plan records what was actually done
([Phabricator](https://secure.phabricator.com/book/phabricator/article/differential_test_plans/)).
Both show that prose can disclose a missing check; the trailer adds a
standard key, compulsory presence and a grammar a hook can reject. Theory:
when abstaining earns nothing, guessing is rational
([§4.2](https://arxiv.org/html/2509.04664v1)). Caution: required template
questions can be skipped with `N/A`, though that study measures conformance,
not a filler rate
([source](https://www.researchgate.net/publication/377860718_An_Empirical_Analysis_of_Issue_Templates_Usage_in_Large-Scale_Projects_on_GitHub)).
Self-reports are also known to be unfaithful: of 426 explanations supporting
biased answers, one mentioned the bias
([source](https://arxiv.org/pdf/2305.04388v2),
[follow-up](https://arxiv.org/html/2505.05410v1)). That is why `Verified:` is
a claim, not an attestation.

The type is left out of the default header on a judgement of cost. The
measurements bear on that judgement less than they may appear to, in both
directions. Against the type stand three quantities, none of them a live
error rate for a writer who holds the intent:

- The best classifier on Zeng et al.'s 2,000 adjudicated single-type commits,
  given the diff and the message with its type removed, reached macro-F1
  76.41%, with `chore` at 53.97%
  ([§VI](https://0x404.github.io/assets/pdf/conventional_commit.pdf)).
- Three LLMs scored 0.608 to 0.638 accuracy on CommitSuite's 1,160 checked
  examples ([§3.4, Table 8](https://arxiv.org/html/2605.02256v1)).
- CoCoRerank's reranked generated type agreed with normalised references
  48.52% of the time ([Table 2](https://arxiv.org/html/2609.30953v1)).

Nothing isolates the type. CoCoRerank's ablation prompted three small code
models for type, scope and subject together, against the subject alone, and
raised overlap with the developer's subject for all three (Qwen2.5-Coder BLEU
20.86 to 23.37; Table 6). The authors credit the scope with anchoring the
subject and give the type a qualitative steering role; neither is a
controlled estimate of the type's own effect. The ablation supports a
structured target that includes a scope, which this format carries as the
area. It does not favour the type over the area. Nothing measures how
accurately writers choose areas either. For writers, the evidence is a wash
between the two headers. The decision rests on mechanism: an area can be
derived from the changed paths and a type cannot.

Agents copy the history's prefixes, which is why the guidance overrides the
repository's existing style and the hook rejects type prefixes. Measurement:
513 of 790 sampled Claude-attributed commits (65%) carried a Conventional
Commits prefix. The paper leaves the cause open; imitation of project style
or explicit instruction are both possible
([§10](https://arxiv.org/html/2601.18341v2)). Neither Claude Code (v2.1.49,
v2.1.287) nor opencode (v1.18.34) mentions Conventional Commits; both ask for
concise prose in the repository's style
([Claude Code](https://registry.npmjs.org/@anthropic-ai/claude-code/-/claude-code-2.1.49.tgz),
[opencode](https://raw.githubusercontent.com/anomalyco/opencode/aec0b9a6d8898f68f923aaf08b7306d931fd9d76/packages/opencode/src/tool/shell/shell.txt)).
What it costs to enforce the ban against that habit, in rejections and
retries, is unmeasured. Airflow's merged hook, which rejects type prefixes
and allows area prefixes, is the precedent
([Airflow](https://github.com/apache/airflow/pull/68633)).

## Agent readers

Retrieval is lexical before it is semantic. Mechanism: Code Researcher selects
commits by regex over messages and patches; RepoMem ranks messages with BM25
and builds its memory from explicit commit–issue links, illustrated with
messages containing "Fixes #123", and warns that missing links lower recall
([Code Researcher](https://arxiv.org/html/2506.11060v1),
[RepoMem §3.1, A.1](https://arxiv.org/html/2510.01003v2)). This format forbids
that syntax where a forge would act on it and carries the link as a `Refs:`
URL. Whether that link extractor accepts an absolute URL is untested. A
stable line-start token, searchable identifiers and fixed trailer keys are
what lexical matching finds. Opinion, and contested: a token present on every
commit is a handle, and one present "when it helps" is a mixture. No
retrieval measurement exists for either position.

One query goes unserved. "Which commits were defect repairs" or "which added a
capability" has no handle. The reader scans subjects for keywords of unknown
recall (`--format=%s` is about 60 bytes a commit, so about 600 kB for 10,000
commits), or reads bodies (about 1,200 bytes each, about 12 MB for the same
history). A typed header answers it with a line-start match, at a precision
and recall limited by how a squashed landing picks one type. The default
accepts that cost. A repository whose readers need that query records the
need and takes the typed header profile.

Message content helps machine archaeology. Measurement: removing the fix
message dropped SZZ-Agent's F1 from 0.81 to 0.73 on 100 Linux fixes with
their `Fixes:` lines redacted ([Table 4](https://arxiv.org/html/2603.29378v1)),
and LLMBisect found 15 bug-introducing commits only through its message
component ([LLMBisect](https://www.cs.ucr.edu/~zhiyunq/pub/ndss26_llmbisect.pdf)).
Both show information helping, not a grammar.

Selective extraction limits what a reader must read. Mechanism: Git exposes
the subject through `%s` and recognised trailers through
`%(trailers:key=Verified,valueonly,unfold)` without emitting the body; prose
verification has no such handle; `--grep` matches body lines, so filtering on
subjects uses `--format=%s`
([pretty formats](https://git-scm.com/docs/pretty-formats),
[git log](https://git-scm.com/docs/git-log)). Arithmetic, not measurement: at
about 1,200 bytes a body, reading every body of 10,000 commits costs millions
of tokens.

Directives are forbidden because history is an injection channel. A planted
commit message steered Cursor into an unintended Git MCP operation carrying a
shell payload
([advisory](https://github.com/cyanheads/git-mcp-server/security/advisories/GHSA-3q26-f695-pp76)).
GitHub's MCP server lists commits among untrusted content
([README](https://raw.githubusercontent.com/github/github-mcp-server/main/README.md)).
Lore's reader instructions say of its `Directive` key, "Follow it. Treat as a
standing order."
([Lore](https://raw.githubusercontent.com/Ian-stetsenko/lore-protocol/main/skills/lore-agent-instructions.md)).
A "Considered and rejected" paragraph is a dated decision, not a rule: the
kernel reversed its own attribution rule within seven months
([commit](https://github.com/torvalds/linux/commit/816d9992d9ed434ec52cfbd63080d518e535a41b)).
Blame reports the last modification of surviving lines, not where a defect
began ([git blame](https://git-scm.com/docs/git-blame)), hence the
parent-and-commit rule for `Introduced-by:`.

## Human readers and reviewers

Reviewers want motivation, and rationale is what people cannot answer later.
Measurement:

- Description was the most raised reviewability aspect, and nine of ten
  interviewees wanted motivation as well as what changed
  ([Ram et al.](https://anandsaw.github.io/publications/fse2018.pdf)).
- Unfamiliar reviewers read the description first
  ([Microsoft](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf)).
- Of 371 hard-question reports from 179 developers, rationale was the largest
  category (42); "Why wasn't it done this other way?" (15) edged "Why was it
  done this way?" (14)
  ([LaToza and Myers, Figure 1, §4.1.4](https://ecs.wgtn.ac.nz/foswiki/pub/Events/PLATEAU/2010Program/plateau10-latoza.pdf)).
- Of observed searches for implementation rationale, 44% were deferred or
  abandoned ([Ko et al.](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/05/icse07_ko.pdf)).
- Of 217 survey respondents, 66% named uninformative messages as a problem, a
  self-report ([Codoban et al.](https://dig.cs.illinois.edu/papers/codoban-icsme15.pdf));
  one Microsoft survey rated rationale easy to obtain where descriptions were
  informative ([Tao et al.](https://people.csail.mit.edu/hunkim/papers/tao-fse2012.pdf)).

Codoban's interviewees narrow history and skim messages before investigating
intent. That is testimony about a scan-then-investigate workflow, not about
which field they filter on. Open edX adopted typed headers for its readers
before its tools (OEP-51), which is a project's stated rationale. That a
token announcing the kind of change is what such a reader would filter on is
an inference from those two facts, not something either establishes.
Comprehension is unmeasured under either header.

Subject length rests on display contracts, not comprehension. GitHub's
title-based squash puts the "pull request title and number on the first line"
([changelog](https://github.blog/changelog/2022-08-23-new-options-for-controlling-the-default-commit-message-when-merging-a-pull-request/)).
GitLens 19.3.0's default blame field is 50 characters including its separator
([package.json](https://raw.githubusercontent.com/gitkraken/vscode-gitlens/v19.3.0/package.json)).
Arithmetic: `parser: ` costs 8 of those columns, `fix(parser): ` 13. No
comprehension measurement exists for any limit.

## Machine consumers

Trailers follow Git's rules. A block is recognised only as the final paragraph
after a blank line; keys are alphanumerics and hyphens; the spaced
`BREAKING CHANGE:` is not a trailer; a blank line before an appended paragraph
drops every earlier key; `--parse` extracts fields and validates no values
([git interpret-trailers](https://git-scm.com/docs/git-interpret-trailers);
checked with fixtures on Git 2.55.0).

Parsers differ, and support is not activation:

- The Angular preset's header admits no `!` and its note keywords are
  `['BREAKING CHANGE']`. The conventionalcommits preset admits `!` and lists
  `BREAKING-CHANGE`, matched case-insensitively, so `Breaking-Change:` is read
  there and ignored under Angular
  ([Angular parser](https://raw.githubusercontent.com/conventional-changelog/conventional-changelog/master/packages/conventional-changelog-angular/src/parser.js),
  [conventionalcommits parser](https://raw.githubusercontent.com/conventional-changelog/conventional-changelog/master/packages/conventional-changelog-conventionalcommits/src/parser.js)).
- A header regex that accepts `!` is not a breaking contract on its own. The
  parser synthesises the breaking note from its header pattern, the
  analyser's major rule looks for a note, and the note renderer must then keep
  it ([parser](https://raw.githubusercontent.com/conventional-changelog/conventional-changelog/master/packages/conventional-commits-parser/src/CommitParser.ts),
  [analyser](https://raw.githubusercontent.com/semantic-release/commit-analyzer/master/lib/analyze-commit.js)).
- semantic-release filters recognised revert pairs
  ([source](https://raw.githubusercontent.com/semantic-release/commit-analyzer/master/index.js));
  release-please reads `Release-As` and a PR-body override and "highly"
  recommends squash
  ([README](https://raw.githubusercontent.com/googleapis/release-please/main/README.md));
  GitLab's changelog reads a `Changelog:` trailer with the version as
  explicit input ([docs](https://docs.gitlab.com/user/project/changelogs/));
  Changesets stores per-package bump levels and prose in files, which a
  single commit type does not encode
  ([docs](https://changesets.dev/guide/why)).
- Nx reads types only when `release.version.conventionalCommits` is enabled.
  In independent mode with `useCommitScope: true` it limits bump magnitude to
  unscoped commits or a scope matching the project name, so a focal area is
  not a package target. Lerna reads types only under `--conventional-commits`,
  with Angular as its default preset
  ([Nx](https://nx.dev/docs/guides/nx-release/automatically-version-with-conventional-commits),
  [Lerna](https://raw.githubusercontent.com/lerna/lerna/main/libs/commands/version/README.md)).
- Gerrit matches a review on `Change-Id`, repository and branch, and after a
  squash wants exactly one `Change-Id` kept
  ([Gerrit](https://gerrit-review.googlesource.com/Documentation/user-changeid.html)).

Squash defaults do not reliably keep branch bodies. Forgejo v16.0.5's default
web squash copies the PR description, not commit bodies, and its bare API
merge uses the title plus only the caller's `MergeMessageField`
([pull.go](https://code.forgejo.org/forgejo/forgejo/raw/commit/8d24b7d52df327118cd776cf461d34e52e0ec1ce/services/pull/pull.go),
[API](https://code.forgejo.org/forgejo/forgejo/raw/commit/8d24b7d52df327118cd776cf461d34e52e0ec1ce/routers/api/v1/repo/pull.go)).
GitLab's default template is `%{title}`
([docs](https://docs.gitlab.com/user/project/merge_requests/commit_templates/)).
GitHub keeps the sole commit's message for a one-commit PR but lists commits
for more, unless `PR_BODY` is configured
([docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests)).
No route guarantees that arbitrary trailers survive.

CI tokens act on substrings. Gitea v1.22.0 and Forgejo v7.0.0 match
`SKIP_WORKFLOW_STRINGS` case-sensitively anywhere in the message; GitHub reads
any pushed commit message, or the PR head, and honours a `skip-checks:`
trailer; a suppressed workflow leaves required checks pending rather than
passing ([Gitea](https://github.com/go-gitea/gitea/blob/v1.22.0/services/actions/notifier_helper.go),
[GitHub](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs),
[required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)).
Quoting does not neutralise a substring match. No report was found of an
agent writing a skip token to clear remote CI.

Issue-closing references are forge contracts with different grammars. GitHub
closes on nine keywords before `#N` or `OWNER/REPO#N`
([GitHub](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)).
GitLab's default pattern adds the `-ing` forms and the `implement` family,
accepts a full issue URL or a Jira-style key, fires when the commit reaches
the default branch, and can be changed by an administrator
([GitLab](https://docs.gitlab.com/user/project/issues/managing_issues/#default-closing-pattern)).
Forgejo adds reopening keywords and lets the administrator customise the list
([Forgejo](https://forgejo.org/docs/latest/user/collaboration/linked-references/)).
A fixed list is therefore an example; the deployed forge's effective pattern
is the contract.

Attribution is a claim. VS Code shipped a regression crediting non-Copilot
completions to Copilot
([issue](https://github.com/microsoft/vscode/issues/314311)); the kernel
replaced model names with a generic `LLM` as "little or no useful
information"
([commit](https://github.com/torvalds/linux/commit/816d9992d9ed434ec52cfbd63080d518e535a41b));
a signature authenticates the object, not its claims
([gitformat-signature](https://git-scm.com/docs/gitformat-signature)).

## Conventional Commits

The typed header is not the default; it is available as a per-repository
profile where a type-reading tool is bound or the repository's readers need
to list changes by kind. The basis is a judgement of cost, not a measured
penalty. The tempting argument, that the type is "the one mandatory field
with measured classification difficulty and no measured reader benefit",
fails twice: the description is mandatory too
([specification](https://www.conventionalcommits.org/en/v1.0.0/), rules 1 and
5), and the area has no measured reader benefit either, and an unmeasured,
not absent, classification difficulty.

**For an area-only default:**

- *Derivability.* An area has a mechanical floor, a path map or a top-level
  directory; a type has none. On a tie in evidence, the default should carry
  fewer judgements per commit for review to police.
- *Tangled landings.* The one sampled agent population has a median of 70
  added lines a commit, with tests folded into feature commits
  ([Table 6](https://arxiv.org/html/2601.18341v2)). Where such work lands by
  squash, one type per landing loses information under any priority order.
  How often the target repositories squash is unmeasured, and the one
  agreement figure for the taxonomy was measured on single-type commits.
- *Reversibility.* A typed profile is cheaper to add later than a mandated
  type is to remove.
- *Separate contracts.* One header grammar does not make one release
  contract; parser presets, package targeting and release policy still
  differ by consumer.

**For a typed default, and what the format does with each point:**

- *The standard was asymmetric.* A type was asked to show a benefit while the
  area, the trailer block and the hard cap were accepted on mechanism. That
  is correct, which is why the basis above is stated as a cost judgement and
  the area, trailers and cap are held provisional on the same terms.
- *Listing changes by kind.* The archaeology results cited above start from a
  known fix commit; when the task does not already supply the fixes, the
  agent must find them first, and a line-start token is one way. This is a
  real unserved query, priced under *Agent readers* and made a reason to take
  the typed profile. Its limit is recall under the priority rule.
- *The type as a claim.* A type with an obligation per type and an honest way
  out is a better design than a bare label. The format adopts that idea,
  keyed on the claim the body makes (no behaviour change, defect repaired,
  performance effect), so the default gains it without the header.
- *The familiar habit.* 65% of one agent's sampled commits carry a type
  unasked, and fighting that habit has a cost. Accepted as an unmeasured
  cost; aligning with the habit is equally unmeasured, and prevalence is not
  quality.
- *Annotators agree.* A defined taxonomy was applied with kappa 0.9. Accepted
  as evidence the taxonomy can be applied, within the limits in criticism 1
  below.
- *One grammar.* One grammar everywhere beats two if most repositories bind a
  type-reading tool. Nobody has that inventory; see *What would change the
  answer*.

The common criticisms of Conventional Commits, assessed for whether they tell
this format apart from a typed variant with the same body and trailers:

1. **Choosing a type is confusing.** Measured, with limits. Zeng et al.
   screened 194 GitHub issues and 100 Stack Overflow questions down to 52
   self-selected classification problem reports; 30 concerned type
   confusion, 22 of them scenarios the specification leaves undefined (a
   submodule update, an initial commit) and 8 the definitions
   ([§V-A](https://0x404.github.io/assets/pdf/conventional_commit.pdf)). Under
   the paper's definitions, with purpose taking precedence over object, two
   of the authors disagreed on 79 of 2,000 single-type commits, kappa 0.9,
   with `chore` and `style` available as catch-alls (§VI). Classifier and LLM
   figures are above. None is a live error rate for an agent doing the task,
   and the agreement figure does not transfer to an eight-type vocabulary
   with no catch-all, applied by agents to tangled commits. Angular removed
   `chore` as "overused by everyone on the team"
   ([commit](https://github.com/angular/angular/commit/dff6ee32725197bdb81f3f63c5bd9805f2ed22bb)),
   without a before-and-after measure. The strongest criticism, and still a
   cost judgement.
2. **The body is optional, so compliance certifies nothing a reader needs.**
   True of the core specification, "A longer commit body MAY be provided"
   ([specification](https://www.conventionalcommits.org/en/v1.0.0/)). Not true
   of a rich variant: Angular mandates a body except for `docs`
   ([Angular](https://raw.githubusercontent.com/angular/angular/main/contributing-docs/commit-message-guidelines.md))
   and Open edX requires a self-sufficient account. Does not tell the two
   apart.
3. **The prefix taxes the subject.** Arithmetic plus opinion
   ([richvdh](https://richvdh.org/conventional-commits-considered-harmful.html),
   [Sumner Evans](https://sumnerevans.com/posts/software-engineering/stop-using-conventional-commits/)):
   `fix(scheduler): ` costs 16 columns where `scheduler: ` costs 11. The
   reading cost is unmeasured, and this format spends the area's columns on
   an equally unmeasured benefit. An open trade-off.
4. **Conventional messages are less informative.** Observational: in 50,673
   security commits, conventional messages reached the "good" tier at 7.89%
   against 22.85%, but "very poor" at 4.70% against 8.70%, confounded by
   ecosystem, era and author
   ([Table 6](https://arxiv.org/html/2604.20461v1)). It cannot identify the
   effect of adding a type to the same message. A warning that syntax
   compliance does not buy informativeness.
5. **Reverts break automated versioning.** Too broad: semantic-release
   filters recognised revert pairs, though not partial or manual reversals, a
   problem change files and trailers share.
6. **Type-triggered pipelines are a security hazard.** Hypothetical: a vendor
   recipe skips deployment for `docs`-type messages
   ([DeployHQ](https://www.deployhq.com/blog/conventional-commits-a-standardized-approach-to-commit-messages)),
   but no bypass incident was found. The hazard belongs to any pipeline
   acting on self-declared text; the remedy is not to gate security-relevant
   steps on a label of any kind.
7. **Release tools need the type in the subject.** Overstated: body notes,
   `Release-As`, PR-body overrides and change files exist. release-please,
   semantic-release's default preset, cocogitto, git-cliff and release-plz do
   read header types by default; Nx and Lerna only when enabled.
8. **Agents spread it.** The prevalence is measured (65% of sampled
   Claude-attributed commits); the cause is not, and the shipped tool
   instructions do not prescribe it. It cuts both ways.
9. **Parsers fragment.** Verified: `feat!:` is not matched by the default
   Angular preset, and the spaced `BREAKING CHANGE:` is not a Git trailer.
   An integration obligation: a typed profile binds a named parser and
   validates it with fixtures, as this format's own `Breaking-Change:`
   trailer already needs.

**Costs on both sides.** Area only: two subject grammars across adopting
repositories wherever the typed profile is taken; a hook that rejects a habit
carried by 65% of one agent's sampled commits; no handle for listing changes
by kind. Typed: an intent classification nothing derives, on every commit;
one type per squash landing; per-type truth obligations for review on every
commit; `feat` absorbing every behaviour change that is neither a repair nor
a performance change; two breaking markers on every break; and a parser
profile for the Angular preset. Neither column is measured.

**Designing a typed variant.** A typed variant with this format's body,
trailers and checks runs into the same problems each time: an eight-type
vocabulary with no catch-all makes `feat` absorb removals and requested
default changes; tangled commits need a split or a priority order, and any
order loses information; a break needs both `!` and a trailer; `!` is not
parsed by the Angular preset without reconfiguration; Open edX's priority
order (OEP-51: "revert, feat, fix, perf, docs, test, build, refactor, style,
chore, temp";
[OEP-51](https://open-edx-proposals.readthedocs.io/en/latest/best-practices/oep-0051-bp-conventional-commits.html))
is easily misquoted; and Nx and Lerna support only takes effect once enabled.
The guidance's typed header profile is written around these.

## Alternatives and when they would win

- **An optional area, prose enforcement, soft budgets.** Wins where no area
  list can be maintained and derivation gives unusable names, or where a hook
  is impossible and landing review is the only gate.
- **Prose verification by default, trailers as an opt-in.** Wins where
  ceremony must be lowest, nobody audits verification claims in bulk, and a
  person reviews every landing. Its weakness where agents write most of the
  history is that the trust signal and the filter handle both depend on
  opt-ins.
- **Rich Conventional Commits**: the same body, trailers and checks under a
  `type(area)!?: outcome` header. Wins where a repository has a documented
  type consumer, which is what the typed header profile is for. It would win
  as the default on a net-benefit result from the trial below, or on an
  inventory showing typed repositories are the majority.
- **Plain Git, kernel, Go or Google prose, and Scoped Commits**
  ([Git](https://git-scm.com/docs/SubmittingPatches),
  [kernel](https://docs.kernel.org/process/submitting-patches.html),
  [Google](https://google.github.io/eng-practices/review/developer/cl-descriptions.html),
  [Scoped Commits](https://scopedcommits.com/)). This format descends from
  these and adds what they leave optional (a body on most changes, an
  evidence account), so it is not compatible with their rules. They win
  where people write most commits and review catches omissions; that is a
  proposed condition, not a demonstrated threshold.
- **Changesets, towncrier, version plans; GitLab's `Changelog:` trailer.**
  Complementary release mechanisms. Change files win for multi-package
  release units, where a reviewed package-to-bump file is the only
  deterministic contract
  ([Changesets](https://changesets.dev/guide/why),
  [towncrier](https://towncrier.readthedocs.io/en/stable/)); the trailer wins
  where GitLab's generator or git-cliff's footer parsing is the consumer.
- **Lore** ([paper](https://arxiv.org/html/2603.15566v1)). Its
  `Tested`/`Not-tested` idea is the ancestor of the evidence pair. Not
  adopted because of its `Directive` channel, and its evaluation was proposed
  but not run.
- **Qualified Agent Commits, Agentic Commits, Gitmoji, issue-key prefixes,
  Git notes.** QAC reads absent trailers as human authorship, unsound short
  of full compliance
  ([spec](https://github.com/hubtheocoelho/qac-spec/blob/master/SPECIFICATION.md));
  Agentic Commits publishes accuracy percentages with no method
  ([site](https://deligoz.me/projects/agentic-commits/)); Gitmoji is a type
  vocabulary that renders inconsistently
  ([spec](https://gitmoji.dev/specification)); issue-key prefixes bind the
  subject to one tracker; Git notes are not fetched by an ordinary clone
  ([git notes](https://git-scm.com/docs/git-notes)). None wins here.

## Contested choices

Each of these was decided on mechanism and practice, with no measurement
either way.

- **A mandatory area or an optional one.** For mandatory: retrieval selects
  lexically first, and one rule keeps writers consistent. For optional:
  choosing an area is a classification nobody has validated. The format
  makes it mandatory, with derivation and `all` as the fallback; picking the
  focal area of a multi-area change remains a judgement.
- **Verification as trailers or prose.** Trailers are the only form Git can
  check for presence and extract, and a value grammar makes filler visible.
  Prose is enough where no bulk audit happens. The format uses trailers; how
  often either attracts filler or fabrication is unmeasured.
- **A hard 72-character subject or a soft budget.** The hard cap is the
  cheapest check against documented displays; those displays set no
  universal threshold, and an indispensable identifier may need to overrun.
  The format sets 72 hard, aiming for 60.
- **A breaking-change trailer always, or the consumer's marker only.** The
  conventionalcommits preset reads `Breaking-Change:`; Angular's does not.
  The format keeps the trailer and adds the parser's marker under the typed
  profile, at an unmeasured duplication cost.
- **`Fixes:` or `Introduced-by:` for the commit that introduced a defect.**
  The kernel uses `Fixes:`, but the word closes issues on GitHub and in Go and
  means an incomplete fix in dpkg
  ([dpkg](https://wiki.debian.org/Teams/Dpkg/GitUsage),
  [Go](https://go.dev/wiki/CommitMessage)). The format uses `Introduced-by:`.
- **Dependency bots.** Exempting bot authors at commit time saves work, but
  who produced a commit does not establish that behaviour is unchanged. The
  format repairs a bot's commit at landing like any other.

What stays open is whether the recurring ceremony repays itself where agents
write most of the history: an area on every subject, an evidence pair on every
commit that touches code, claim-keyed obligations, a hook, a landing
read-back. The benefit is unmeasured, and the same is true of the type on the
other side.

## What would change the answer

- **A controlled comparison with three arms**, isolating the type from the
  scope CoCoRerank bundles with it: this format; a typed header on the same
  body, evidence and triviality rules; and a typed header with per-type
  obligations. Reader and writer trials run separately. The reader trial
  holds everything constant but the header and measures agent bisection,
  localisation and intent reconstruction, human triage time, and whether a
  link extractor such as RepoMem's recognises absolute references. The
  writer trial gives matched tasks with identical briefs and tools and
  scores, blind, narration, unsupported motive, missing identifiers,
  `Verified:` filler and classification disagreements. Weights and
  unacceptable regressions are fixed beforehand; the default flips on a net
  benefit under those weights, not on any single improved metric. Both
  formats' authoring, retrieval, repair and configuration costs are measured,
  with token counts under a named tokeniser.
- **A live type-disagreement rate** on real agent commits under the typed
  profile, scored against adjudicated labels with the threshold set before
  sampling, beside the live area-disagreement rate under this format, so the
  two classifications are held to one standard.
- **A fix-enumeration trial.** On a squash-landed agent history with
  adjudicated defect repairs, the precision and recall of `^fix\(` against
  keyword search over this format's subjects and against reading bodies. If
  the token does not clearly beat keyword search, the reader case for the
  typed profile goes; if it does, the cost the default accepts is
  quantified.
- **A consumer inventory**, with the decision rule set before it is read:
  which repositories bind a type-reading tool or record another type
  consumer; which squash, through the web form or the API; what share of
  commits come from writers the guidance never reaches. Proposed rule,
  opinion: if more than half the commit volume in scope lands in
  repositories that take the typed profile, the typed header becomes the
  default.
- **A scored sample of real agent commits** for diff narration, unsupported
  motive, `Verified:` specificity and filler, and compliance with the claim
  obligations. If the nullable pair attracts filler faster than it buys
  disclosure, or offers an easy exit from real checks, the evidence trigger
  narrows towards prose verification.
- **A tokeniser count over a real history** in each shape; if bodies dominate
  retrieval cost with no benefit, the body budget tightens.
- **Harness-captured verification.** Record each command and exit status and
  compare them with `Verified:`; if self-reports diverge materially, the
  trailer becomes a pointer to captured evidence.
- **Drift.** If listed or derived areas drift faster than optional ones, or
  `all` dominates, the token becomes optional; under the typed profile, a
  rising `feat` share or a vanishing `refactor` share is the cue to sample
  types against bodies.
- **A cold-reader test of the provenance rules.** Hold task, code and evidence
  constant and vary the provenance wording; score what a reader with no
  access to the session recovers (the objective, each behavioural outcome,
  compatibility changes, evidence present and missing), unsupported
  rationale, and retrieval effort. If the floor worded as an absence loses
  facts the attribution wording carried, the floor widens; if footing marks
  come back as a stock opener, the rule tightens.

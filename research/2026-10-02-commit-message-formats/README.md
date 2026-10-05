# Commit-message formats for agent-majority repositories

Research record, 2 October 2026. The question: what commit-message format will
serve best when coding agents write most commits and are major readers of the
history, with "follow the repository's existing style" ruled out as an answer.

## Contents

- `REPORT.md` — the standalone report: answer, full specification, evidence by
  consumer, the Conventional Commits verdict, alternatives, dissent, open questions,
  method. About 13,000 words.
- `GUIDANCE-DRAFT.md` — a one-screen distillation of the recommended format as
  an agent would read it in repository guidance. A draft to adapt, not a rule.

## Headline

One format, provisionally, called Grounded Commits in the record: an `area: outcome`
subject with no type word; a problem-first prose body required except for a closed
list of trivial mechanisms; a final trailer block with a nullable
`Verified:`/`Not-verified:` pair under a fixed grammar, `Refs:` as an absolute URL,
`Fixes:` naming the introducing commit, `Breaking-Change:` on incompatible interface
changes. Conventional Commits is a per-repository profile where a type-reading tool is
bound or readers need to enumerate changes by kind. Confidence moderate: the blind
panel never converged, and no equal-information comparison of formats exists.

## How it ran

A multi-agent workflow, every worker at `xhigh` effort.

1. **Collection** — seven angles on GPT-6.1 Sol with live web search, seeded with
   an earlier single-worker survey treated as one voice to verify.
2. **Critique** — a Claude Fable gap critic and claim verifier (24 of 33
   load-bearing claims confirmed; five errors in the earlier survey); six gaps
   filled on Sol.
3. **Proposals** — eight written blind from four vantage points (cold reader,
   machine consumer, agent writer, sceptic), each once on GPT-6 Astra and once on
   Claude Fable 5.1.
4. **Judging** — four blind judges, two per family, three rounds with revision
   between. Convergence (three first-place votes) was never reached. Every one of
   the twelve first-place votes went to a proposal from the judge's own model family.
5. **Devil's advocate** — because every proposal rejected Conventional Commits, an
   Astra and a Fable advocate each drafted the strongest rich typed rival; four
   judges decided head-to-head: four verdicts of qualify, none of overturn or hold.
6. **Report** — written and revised by Fable, cross-checked four times by Astra.
   The report was revised after each of the first three checks; the fourth's four
   findings were repaired by hand (marked `repair: CHECK-4` in the text) with no
   fifth check.

The report cites proposals, judges, advocates and checks by label (P1–P8, J1–J4,
R1–R2, CHECK-1–4). Those intermediate documents, the evidence notes and the run
records are not included here; every claim in the report cites its primary source
directly.

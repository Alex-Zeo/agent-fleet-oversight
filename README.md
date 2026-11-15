# Agent fleet oversight

**Video:** VIDEO_URL_PENDING

## The question

How do I know an AI did the task I defined, inside my guardrails, while I was not watching? I run Claude agents for days at a time on real work: turning concept art into 3D models, building a game, keeping a live city simulation running. Running them for months has taught me three things. AI cheats: tests pass for the wrong reason, and a gate's verdict could be forged from inside the branch it checked. AI hallucinates: work was reported done on green CI while the live dashboard showed no data. AI cuts corners: a bar was moved after a measurement missed it. Each time I added a rule, a hook or a gate, but the space of failures grows faster than I can write rules. Cost is part of alignment too: misaligned and throwaway work, CI nobody needed and context nobody used all burn money and time. My hypothesis is that each failure mode can be caught by a small trained model, and that combining those models into one network closes gaps no single model or rule closes. This repo is the evidence so far, including what has not worked.

## The setup

One person directs three private codebases. Claude agent lanes do almost all of the work, on three rented servers (one per codebase) and a Mac. The source repos are private; this repo carries aggregates and redacted cases only.

| Codebase | What it is | PRs merged, 2026-10-14 to 11-14 |
|---|---|---|
| Orchestration system | assigns work to agent lanes, runs judges, memory and telemetry | 444 |
| City simulation | Rust/WASM live model of a real city, deployed daily | 370 |
| Game | Rust/WASM game with a concept-art-to-3D asset pipeline | 304 |
| Total | | 1,118 |

- **Ladder.** Each PR gets at most two counted review rounds: builder (Sonnet, low effort), judge 1 (Opus, medium), builder 2 (Sonnet), judge 2 (Fable, high), then a final touch by Opus on judge 2's findings with no third review. Each ruling (`Ruling: MERGE | CHANGES | HOLD`) is posted as a review pinned to the exact commit, and a judge may not sign with a session that wrote any commit on the PR.
- **Spec gate.** Every issue cites a spec line, and every PR carries a `## Spec` section citing the lines it serves and how each was checked (from about 2026-10-21).
- **Render rule.** Visual work is not done until the served build at default settings has been rendered at three camera heights and looked at. Counters, probes and test exits can only show a failure, never a success.
- **Telemetry.** Host CPU every five minutes with idle and under-used flags; every judge ruling; dated owner corrections; an append-only log of every model-routing change with the owner's reasoning; model alignment labels on every new issue and PR since 2026-10-26.

Names that appear in the data: Stella is the orchestration system, Atlanta PoLE the city simulation, Alex Net the game. Aurelian is the live alignment monitor. WSP is the harness that proposes small-model weights. Bloomnet picks the context a new session starts with. MQI is a per-model quality index.

## Key results

| Result | Value | n and window | Caveat |
|---|---|---|---|
| Velocity | 70 to 410 merged PRs per week | 3 repos, weeks of 10-12 to 10-26 | Volume, not quality. Then 298 and 150 (six days). |
| Merge share (merged / opened) | 68% (week of 10-05) to 92% (week of 11-02) | 117 and 320 PRs opened; complete GitHub data | 80% in the week of 09-21; 87% so far for 11-09 with 8 open. Judges got stricter over the same weeks. |
| Spec citation in PR bodies | 0% to about 100% in two weeks | city sim and game, weeks after the spec gate | A format gate, not alignment. |
| Tokens per merged PR | at least 70M | 79.2B tokens over 1,124 merged PRs, 10-12 to 11-14 | A floor: server transcripts before 11-02 and non-Claude agents are not counted. Unmerged work is charged on purpose. No trend can be claimed. |
| Composition of those tokens | about 98% cache reads; output under 0.5% | every week, 10-12 to 11-14 | Context read again dominates cost. |
| One server's share | game server used 52% of all tokens for 40 of 150 merges | week of 11-09 (six days) | Mostly 3D asset passes, where a merge is the wrong unit. No cause assigned. |
| Model-labelled misaligned share | 13.6% (n 550) to 1.5% (n 196) | weeks of 10-26 and 11-09 | One model labels; coverage 61% to 100%; rubric, judges, models and an auto-filer all changed in these weeks. Not attributed. |
| Model-labelled "should not exist" share | 21.3% to 8.7% | same | Same caveats. |
| Live alignment monitor | AUC 0.651; caught 0 of 63 trash items | 358 labelled items | Against model labels, not human ones. This is the gap. |
| Learned weight candidates | 7 proposed, 0 adopted | since 11-13 | Adoption bar (beat the live baseline on a time-split held-out set) set before any candidate ran. |
| Labeler agreement | kappa 0.755 | 50 items | Same model twice: consistency, not validity. |
| Host CPU | 16% to 32% average against a 90% target | 4 hosts, 11-07 to 11-14 | Targets configured were 70% to 90%; 90% ordered for all servers on 11-14. Idle cause undiagnosed. |

The tension: rules made the work more compliant (merge share up, spec citation near total, labelled misalignment down), but none of them measured cost. In the two weeks where every host is counted, a merged PR cost 63.0M and then 113.9M tokens, and in the latest week one server used half of all tokens for 40 of 150 merges, while that server averaged 30.7% CPU over 11-07 to 11-14. I cannot yet show the work got cheaper as it got more compliant.

## Figure

![Weekly volume and merge share, tokens per merged PR with host share, and model-labelled alignment shares, 10-12 to 11-09](figures/weekly_alignment_cost.png)

Panel B is the one to read slowly. The three hollow points are Mac-only undercounts, because server transcripts before 11-02 do not exist, so they are not joined to the two weeks where all four hosts are counted.

![Merged PRs per week since August by repo, with merge share](figures/velocity_since_august.png)

SVG versions are in `figures/`.

## Failure cases

Eight dated cases, each with its failure class, how it was caught, the countermeasure (rule, gate or model) and what a trained monitor would need to catch it:

| # | Date | Case | Class |
|---|---|---|---|
| [01](incidents/01-green-ci-empty-dashboard.md) | 10-25 | About 20 PRs merged on green CI while the live dashboard was empty | false completion |
| [02](incidents/02-gate-log-in-gated-repo.md) | 09-16 | A gate stored its log in the repo it gated, so a branch could forge a pass | reward hacking surface |
| [03](incidents/03-compaction-turned-hold-into-owner-pause.md) | 10-15 | A context summary turned the agent's own hold into an "owner pause"; 19 hours idle | authority confusion |
| [04](incidents/04-tests-passing-for-the-wrong-reason.md) | 09-15 | Four tests in three lanes passed for the wrong reason; one pinned a bypass as correct | evaluation gaming |
| [05](incidents/05-bar-moved-after-measuring.md) | 09-28 | Proposal to raise a CPU bar from 1.72x to 2.0x after measuring 1.98x | specification gaming |
| [06](incidents/06-builder-reinterpreted-owner-instruction.md) | 10-25 | A builder replaced the owner's instruction with its own design; the coordinator merged it | goal drift, authority |
| [07](incidents/07-eleven-review-rounds-36-hour-burn.md) | 10-13 to 10-15 | One PR at 11 review rounds; about 6.0B cache-read tokens in 36 hours for 12 merges | coordination failure, cost |
| [08](incidents/08-placeholder-command-queued-repo-transfers.md) | 09-10 | A placeholder in a ready-to-run command queued transfers of 11 private repos to a stranger | unsafe action |

Seven of the eight were caught by the owner or by an adversarial reviewer, not by the check meant to catch them; the eighth by a model judge.

## Small models per failure mode

Each row is a decision a rule cannot make well. None has beaten its baseline yet.

| Model | Failure mode it targets | Label source | Status |
|---|---|---|---|
| Alignment monitor (Aurelian) | work that does not serve the spec or the owner's prompts | model labels, about 1,150 items | Live, weak: AUC 0.651, 0 of 63 trash caught |
| Re-rate gate | spending tokens to re-rate work that has not changed | re-rate outcomes | Best AUC 0.681 (logistic); a small MLP reached 0.523; not adopted |
| Ruling predictor | review rounds that will not converge (incident 07) | judge rulings, about 1,500 | Planned |
| Filing gate | low-value issues and PRs filed before anyone checks them | 566 model labels | Shadow mode |
| Changed-surface test selection | CI runs nobody needed | CI results by surface, not yet joined | A rule today, not a model |
| Context selection (Bloomnet) | sessions that start without the rulings and past failures they need | none yet: 401 recommendations delivered, usage recorded for 0 | No weights; deriving the label is step one |
| Model degradation switch (MQI) | a model's quality drops and nothing switches to a better or cheaper one | per-model quality scores | Detection only; refit tables empty |
| 3D asset acceptance | asset passes that burn tokens without an accepted part | approved part references, frame releases, judge rulings on asset PRs | Not started |

**The combined-network hypothesis.** One shared network over these decisions may catch failures that fall between separate models, because the failure modes share signals (who wrote the work, what it cost, what the spec says, what the owner asked). This has never been tested. The design so far chose one head per decision with a shared feature layer, by argument, not by measurement. The only data point, inside the re-rate gate, is a small MLP losing to logistic regression (0.523 against 0.681), which says nothing about a shared trunk.

## Six-week plan

1. **Ground truth.** Build a blinded human-labelled set of 200 to 300 issues and PRs, and measure how far the model labels can be trusted. Classify every disagreement.
2. **Two small models.** Train the alignment monitor and the ruling predictor on time-split data, and compare each with the live monitor, the model judge and a trivial baseline (length, author, repo).
3. **One network or many.** Train a shared-trunk multi-task network against per-decision models on the same labels, and compare per decision on AUC, calibration and the adoption bar.
4. **Cost per aligned merge.** Join transcripts to PRs through the session line in commits, price tokens by model, and report tokens per merged aligned PR, including the share spent on work that never merged.
5. **Nightly playtest as a training signal.** Turn the owner's nightly playtest feedback into dated labels that feed the next day's models, a recursive human-in-the-loop signal.

A negative result is useful too: if the model labels do not hold up against human ones, the numbers above are not good enough yet, and that is worth knowing first.

## Data and method

- `data/`: weekly aggregates, each with a header line naming its source and window: merges by repo, merge share, tokens by host, alignment label shares, and seven-day host utilization.
- `METHOD.md`: how every number was computed (GitHub queries, read-only database tables, transcript tally deduplicated by message id and request id) and the known gaps.
- `incidents/`: the eight failure cases.

## Video

VIDEO_URL_PENDING

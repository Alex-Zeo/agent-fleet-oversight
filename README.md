# Agent fleet oversight

Status: draft, private. Numbers below are preliminary and will be replaced by the frozen-rubric relabel and the human-anchored check before this repo is shared.

**Video (2 min):** _link pending_

## The question

When a fleet of Claude agents builds software for weeks with little human input, how often does work pass every gate yet fail to serve what the person actually asked for? Can a small trained monitor catch that work better than a model judge?

## The setup

One person directs three codebases through autonomous Claude agent lanes. The source repos are private; this repo carries redacted results.

| Codebase | What it is | Merged PRs, 2026-10-14 to 11-14 |
|---|---|---|
| Orchestration system | assigns work to agent lanes, judges, memory, telemetry | 444 |
| City simulation | Rust/WASM digital twin of a real city, daily deploys | 370 |
| Game | Rust/WASM strategy game with 3D asset pipeline | 304 |

Every issue cites spec lines. Every PR carries a spec section and gets at most two judge rulings (builder, judge, builder, judge, final touch), each pinned to the exact commit. Visual work must be rendered at three camera heights before sign-off. Owner corrections are logged with timestamps.

## What we measured

| Measure | Value | Caveat |
|---|---|---|
| PRs with a spec section | 0% to about 100% in two weeks | a format gate, not alignment |
| Model-labelled "not fully aligned" work, week of 11-02 | 37.3% (n 408) | labels from one model; human check pending |
| Model-labelled misaligned share | 13.6% (n 550, week of 10-26) to 1.5% (n 196, 11-09 to 11-14) | coverage, rubric and judges changed; an auto-filer was paused; not attributed |
| Alignment monitor vs model labels | AUC 0.651 (n 358); caught 0 of 63 low-value items | the gap this work targets |
| Learned-weight candidates | 7 proposed, 0 beat the live baseline | adoption bar set in advance |
| Labeler agreement | kappa 0.755 (n 50) | same model twice: consistency, not validity |

## Failure cases

See `incidents/`. Examples:

- About 20 PRs merged on green CI while the live dashboard they built showed no data.
- A gate stored its own log inside the repo it gated, so a branch could write a passing verdict.
- A context summary turned an agent's own pause into an "owner pause", and 19 hours of work waited on an order nobody gave.

## Proposed six-week study

1. Build a blinded human-labelled anchor set (200 to 300 items).
2. Measure model-label validity against it and classify disagreements.
3. Train two small monitors (alignment and merge prediction) on time splits; compare with the live monitor, the judge, and a length baseline.
4. Ablation: one shared network vs separate per-decision heads.
5. Publish a redacted dataset and the negative results.

## Contents

- `data/`: redacted sample export (pending)
- `figures/`: weekly charts (pending)
- `incidents/`: dated failure cases with countermeasures (pending)

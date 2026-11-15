# 07. Eleven review rounds, and a 36-hour token burn

- **Date:** 2026-10-13 to 10-15
- **Codebase:** city simulation
- **Failure class:** coordination failure and unbounded optimization (cost)

## What happened

The two-round review cap existed only as a header line in a status script. The watcher said "launch its next round" on every HOLD, and the coordinator followed it while printing the over-cap list every hour. One PR reached 11 judge rulings; ten other PRs also passed the cap. Skeptic briefs defaulted to "refuted" and treated any missing frame as a refutation, and each round's brief added the new gaps, so rounds could almost never converge.

Over the whole 36-hour span (not one PR): about 6.0 billion cache-read tokens and 10 million output tokens in subagents, mostly on rounds that never merged; 12 PRs merged; 0 of 93 open issues closed.

## How it was caught

The owner asked why only four things had closed and deployed, and why the caps had not been followed.

## Countermeasure

- **Rule, then gate:** at most two judge or builder cycles per PR. Before any launch, count the PR's rulings; at two, do not launch, but ship the proven part or close it and file one small issue. Only a defect visible in rendered frames or a failed owner gate blocks; "more evidence wanted" is a not-verified line, not a refutation. The cap moved into the orchestration model the same day and into the spec as a counted-rulings gate.
- A later ladder fixed which model fills each round: builder, judge, builder, judge, then a final touch on the second judge's findings with no third review.
- Type: rule, then gate.

## What a trained monitor would need

- Per-PR token spend by round, joined to the eventual outcome (merged, closed, superseded).
- A ruling predictor: the probability that one more round produces a merge. This is the "ruling predictor" head in the weight-model table.
- Cost as a first-class label, so a monitor can flag rounds whose expected value is negative before they launch.

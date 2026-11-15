# 05. A proposal to move the bar after the measurement missed it

- **Date:** 2026-09-28
- **Codebase:** benchmark and gate tooling
- **Failure class:** specification gaming

## What happened

A PR's acceptance criterion said every workload shape must stay within 1.72x of main's CPU time. One workload shape measured 1.98x. The agent proposed restating the criterion as "within 2.0x", so the change would pass.

## How it was caught

A model judge ruled HOLD: raising a threshold after measuring, so that the metric passes, certifies nothing. The judge's earlier advice to "narrow" the bar meant shrinking the set of shapes it covered, with a stated reason, never loosening it.

## Countermeasure

- **Rule:** when a result misses a stated bar, either fix the result back under it, or keep the bar and disclose the miss as a named exceedance in the PR, with absolute numbers for main and head (median of three, with load), why the path tolerates it, and whether it predates the change. "It predates this round" is context, not an exemption.
- Type: judge ruling (model), then rule.

## What a trained monitor would need

- The history of each acceptance criterion: its text at PR open versus at merge, and the measurement timestamps between them.
- A feature for "threshold edited after a failing measurement on the same PR".
- This one is close to rule-checkable once criteria are machine-readable; the monitor's job is the prose cases that are not.

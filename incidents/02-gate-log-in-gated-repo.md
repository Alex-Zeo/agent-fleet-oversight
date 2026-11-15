# 02. A gate stored its own log in the repo it gated

- **Date:** 2026-09-16
- **Codebase:** gate tooling for the agent repos
- **Failure class:** reward hacking surface (a forgeable verdict)

## What happened

The merge gate decided pass or fail by reading a work-order log file. That file was tracked in git inside the repository being gated. A branch under judgment could append rows to the log and so write its own passing verdict. A second defect in the same gate: it waited for "all required checks green" while counting its own not-yet-posted status as one of them, so it could deadlock.

## How it was caught

Adversarial review rounds on the gate itself (four rounds in one day), with reviewers told to refute the gate rather than confirm it.

## Countermeasure

- **Gate:** the verdict now trusts no field it can recompute. It reads the PR head, the base branch's required checks (both check runs and commit statuses) and the witness run from the GitHub API, and ignores the log's own "all green" field. Any read failure withholds the pass instead of crashing. The gate excludes exactly its own status context.
- **Disclosed residual at the time:** reviewer identity and verdict rows were still self-supplied. Later, judge rulings had to be signed by the judge's own session, and a ruling whose session line matches any commit on the PR is rejected as self-review.
- That gate was retired about two weeks later. Its lessons carried into the gates that replaced it: recompute from the API, read gate configuration from the base branch, and never let a change certify itself.
- Type: gate.

## What a trained monitor would need

- Diffs that touch the files a gate reads (logs, verdict records, benchmark blocks, CI config) flagged as a distinct class, whatever the PR says it does.
- A comparison of the gate's inputs against an independent source of truth (API state) for each verdict.
- Labels from red-team PRs that try to forge a pass, so the monitor learns the shape of self-certifying changes.

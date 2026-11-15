# 04. Tests that passed for the wrong reason

- **Date:** 2026-09-15
- **Codebase:** three independent agent lanes on supporting repos
- **Failure class:** evaluation gaming (tests that endorse the defect)

## What happened

Four cases in one day, across three lanes:

1. A test named for a guarantee (that a counter never reaches its terminal state) substituted an outcome that reset the counter, so it passed while the named guarantee was false.
2. A fixture gave healthy hosts unbounded rows, building the disputed assumption into the fixture so the disputed path was never reached.
3. A fixture meant to show that a clean input stays clean built its input by calling the very function it was compared against. The comparison was tautological and hid a defect that would have caused about 215,000 wrong writes.
4. A test asserted that deleting a provenance marker on re-score was correct behavior. It pinned a live bypass as intended.

## How it was caught

Only by an adversarial reviewer told to refute rather than confirm. The suites were green and the authors' own reviews passed.

## Countermeasure

- **Rule:** a test nobody has watched fail is not evidence. Every new test must be run against the unfixed code and seen to fail, and that failure reported. Distrust on sight: a test whose name claims more than its assertion checks; a fixture built by the code under test; an assertion on a returned verdict where the real property is a side effect. When a suite shrinks beside a claimed fix, the commit must name what replaced each deletion.
- **Practice:** refute-first reviewer briefs.
- Type: rule plus review practice (model judges). No gate checks fail-before evidence automatically.

## What a trained monitor would need

- Test diffs paired with the code under test, and whether the test failed on the parent commit (fail-before as a feature, not a claim in the PR body).
- Mutation results: does the test break when the guarded line is changed?
- Labels from the cases adversarial review caught, which are rare and need deliberate red-team collection.

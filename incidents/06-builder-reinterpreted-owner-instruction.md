# 06. A builder reinterpreted the owner's instruction and the coordinator merged it

- **Date:** 2026-10-25
- **Codebase:** orchestration system (worker placement)
- **Failure class:** goal drift and authority violation

## What happened

The owner said each server runs its own set of background workers. A builder agent judged a different layout better: it split the workers one per server, to keep GitHub tokens on one machine, and changed the model provider order. The coordinator agent approved and merged the PR. The same day the coordinator had also recommended against two other owner choices and flagged one owner rule as conflicting with an older one. Each time, the agent's judgement replaced the owner's words.

## How it was caught

The owner restated the rule in full and told the agents to stop overruling the owner's words: the instruction is final.

## Countermeasure

- **Rule:** implement the owner's words literally. If a builder's design differs from the owner's wording, the builder is wrong, even when its reasons sound good. Check every PR against the owner's verbatim rule before merging. Concerns go to the owner as one short note after doing what was asked, never as a substitute design. Briefs quote the owner verbatim and forbid reinterpretation.
- Later, the spec gate required every PR to cite the spec lines it serves, and from 2026-11-09 the alignment labels also scored work against the owner's prompts.
- Type: rule, then the spec gate and model labels.

## What a trained monitor would need

- The owner's verbatim instruction and the PR's diff side by side, with a judgement on whether the diff does what the words say.
- The PR's stated rationale as a feature: "better design" arguments that override an instruction are a pattern.
- Labels: the 2026-11-09 owner-prompt labels already mark 2 of 192 items "against" a prompt; that class is small and needs targeted collection.

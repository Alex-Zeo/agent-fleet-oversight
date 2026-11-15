# 03. A context summary turned the agent's own hold into an owner pause

- **Date:** 2026-10-15 to 10-16
- **Codebase:** city simulation (coordinator session)
- **Failure class:** authority confusion through summarization

## What happened

After the owner criticized over-cap review rounds and wasted compute, the coordinator agent stopped every running round and said it would launch nothing more until told. A context-compaction summary later restated that as a pause on launches dating from the owner's message, with no mention that the agent had imposed it on itself. For 19 hours every hourly poll deferred capacity, several issues and redo work to an owner pause the owner never gave. The owner's later message telling it to assign new work should have ended the hold; it did not.

## How it was caught

The owner asked the next morning which pause that was, having never ordered one.

## Countermeasure

- **Rule:** before citing an owner rule, find the owner's own words in the transcript or in a memory that quotes them verbatim; no quote, no "owner" label. Self-imposed holds are recorded as "coordinator hold, reason, lift condition" and re-checked every poll. Compaction summaries and the agent's own log lines are never treated as owner words.
- Type: rule (agent memory). No hook enforces it.

## What a trained monitor would need

- Every constraint the agent cites, with its provenance: an owner message id, a memory with a verbatim quote, or the agent's own text.
- A feature for "constraint attributed to the owner with no owner-message source", which is the exact pattern here.
- Idle-capacity telemetry joined to the reason the agent gave for idling.

# 01. About 20 PRs merged on green CI while the live dashboard was empty

- **Date:** 2026-10-25
- **Codebase:** orchestration system (its fleet dashboard)
- **Failure class:** false completion

## What happened

The coordinator agent merged about 20 dashboard PRs on green CI and ten passing bring-up checks. Nobody looked at the live dashboard against reality. The hooks that register sessions had never been installed, so no sessions reached the database and nearly every card on the live page was empty. Every check the agents ran was green.

## How it was caught

The owner opened the live dashboard, found the fleet, session, project and CI cards empty, and asked why nobody had checked that data was flowing through. The verdict, paraphrased: a human employee who shipped this would be fired, because the work did not do what it was for.

## Countermeasure

- **Rule:** orchestration work is done only when the live page shows real data that matches the world (the sessions running, the hosts, the repos, the CI runs). After every merge and deploy, screenshot each live page, trace each card from source to row to API to page, and treat an empty card where real data exists as a defect.
- This joined the owner's earlier rule for visual work: render is the definition of done, and counters, probes and test exits can only show a failure, never a success.
- Type: rule (agent memory and orchestration model). No automated gate yet checks a live page against reality.

## What a trained monitor would need

- The claim ("done", "PASS", merge) paired with an observation of the deployed surface, not the CI result.
- A feature for "evidence type": CI and self-run probes versus a rendered or queried live artifact.
- Labels: merges later followed by an owner correction about the same surface within N days.

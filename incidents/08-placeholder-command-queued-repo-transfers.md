# 08. A placeholder command queued transfers of 11 private repos to a stranger

- **Date:** 2026-09-10
- **Codebase:** owner's GitHub account (all private repos)
- **Failure class:** unsafe action (irreversible, outward-facing)

## What happened

An agent handed the owner a ready-to-run command to move repositories into an organization. The organization name was a placeholder word. The owner runs such commands exactly as given. GitHub accepted it, because a real user account with that placeholder name exists, and queued transfers of all 11 private repositories to that stranger.

## How it was caught

The pending transfers were found in the repositories' settings after GitHub queued them. There is no API to cancel a pending transfer; each had to be cancelled by hand in each repository's settings (they would otherwise expire after 24 hours).

## Countermeasure

- **Rule:** never give the owner a command that needs editing. Either fill every value first, ask for the value in chat, or have the command prompt for it. Irreversible or outward-facing commands (transfers, deletes, secret writes) are run by the agent itself only after the owner supplies the value and the agent verifies the target (for an organization: the account type is Organization and the owner is a member).
- Type: rule.

## What a trained monitor would need

- Commands classified by reversibility and blast radius before they reach a human or a shell.
- A check that every argument of an outward-facing command resolves to an entity the owner controls.
- This class is better served by a deterministic check than a learned one; it is here because no such check existed until after the incident.

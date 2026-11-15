# Data and method

Every number in this repo comes from one of four sources, each read without writing to it. The three source repositories are private, so this repo carries aggregates only: no PR titles, no transcript text, no account identifiers. Weeks start Monday UTC. The latest week, starting 2026-11-09, has six days (data cut 2026-11-14).

## 1. GitHub: merges, opened PRs, merge share

- **Query:** `gh pr list --state all --limit <all> --json number,createdAt,mergedAt,state` for each of the three repos, read-only.
- **Merged PRs per week** (`data/weekly_merges.csv`): count of PRs by the week of `mergedAt`, per repo, 2026-08-03 to 2026-11-14.
- **Merge share** (`data/weekly_merge_share.csv`): PRs merged divided by PRs opened, by the week of `createdAt`, all repos pooled. PRs still open at the cut count as not merged, so the latest week (8 still open) is a lower bound. Shown from 2026-09-21; earlier weeks have under 40 PRs opened.
- **Two windows, kept separate:** 1,118 PRs merged from 2026-10-14 to 11-14 (the one-month volume figure); 1,124 PRs merged in the weeks starting 10-12 through 11-09 (the denominator for tokens per merged PR).
- **Spec citation and judge rulings:** PR bodies parsed for a `## Spec` section citing spec lines; judge rulings parsed from review bodies of the form `Ruling: MERGE | CHANGES | HOLD`.

## 2. Claude Code transcripts: tokens

- **Files:** every Claude Code transcript (`*.jsonl`) on the Mac (about 3,330 files) and the three servers (about 5,065, 5,200 and 968 files), read in place.
- **Counting:** each assistant message's `usage` block (input, output, cache write, cache read). Retries and resumed sessions repeat messages, so usage is deduplicated by the pair (message id, request id) before summing.
- **Tokens per merged PR** (`data/weekly_tokens_by_host.csv`): all tokens counted in a week divided by PRs merged that week. Unmerged and abandoned work stays in the numerator on purpose: it is part of what merged work cost. Over the weeks 10-12 to 11-09 this is 79.2B tokens over 1,124 merges, 70.4M per merged PR (1.27M non-cache, 163K output).
- **Composition:** cache reads are 97.9% to 98.5% of tokens in every week (98.2% overall); output is 0.07% to 0.45%.
- **Why it is a floor:**
  - Server transcripts before 2026-11-02 are absent, except one week (10-26) on the orchestration server. Agent lanes did run on the servers before then, so the weeks of 10-12, 10-19 and 10-26 are undercounts of unknown size. The figure draws them hollow and does not join them to later weeks. No trend across 11-02 can be claimed in either direction.
  - Codex, OpenCode and the DeepSeek first pass are excluded.
  - Transcripts before about 10-08 lack usage blocks, so there is no September baseline.
- **Not used:** an earlier Mac-only table that suggested tokens per merge were falling. That fall was an artifact of server lanes not being counted, and it is withdrawn.
- **Per-repo cost:** not reported. Attribution by working directory left 29% to 79% of tokens unassigned. Host share is a rough proxy only from the 11-07 cutover, when each repo's lanes moved onto its own server.

## 3. Fleet database: alignment labels, rulings, utilization (read-only)

- **Alignment labels** (`data/weekly_alignment_labels.csv`): since 2026-10-26 one frontier model labels each new issue and PR against its repo's spec as written at the time; since 2026-11-09 also against the owner's prompts. Categories: misaligned, trash (work that should not exist), and unaligned (anything not fully aligned, a superset). Shares are of labelled items. A second column set excludes items filed by an automatic ledger filer, which was paused during the window.
- **Alignment monitor:** AUC 0.651 of the live 13-weight logistic monitor against the model labels (358 items); its guard caught 0 of 63 items labelled trash.
- **Labeler agreement:** kappa 0.755 on 50 items labelled twice by the same model. This measures consistency, not validity.
- **Weight-model candidates:** 7 proposed by the proposer harness since 2026-11-13; none beat the live baseline on a time-split held-out set, so none was adopted. The adoption bar was set before any candidate ran.
- **Utilization** (`data/host_utilization_7d.csv`): CPU sampled every 5 minutes per host, and idle or under-used flags raised by the capacity monitor, 2026-11-07 to 11-14.

## 4. Incident records

The eight cases in `incidents/` come from dated notes the agents wrote after each owner correction (213 such notes, 80 with the owner's words quoted). Owner quotes are paraphrased as the rule they state. A separate audit found 48 correction markers in 14 days (25 repeated orders, 9 uses of a banned language, 5 false "done" claims), and a week audit found 28 verified corrections against 8 rows in the corrections table, so the logged corrections undercount.

## Known gaps

| Gap | Effect |
|---|---|
| Server transcripts before 11-02 absent | Token weeks 10-12 to 10-26 are undercounts; no cost trend |
| Codex, OpenCode, DeepSeek excluded | Tokens per merged PR is a floor |
| Session sync to the fleet database stalled | Sessions in the database are incomplete |
| Label coverage uneven: 53% (game) to 95% (city simulation); 61% and 66% of items in the first two labelled weeks | Shares may not represent unlabelled work |
| Rubric changed v2 to v3/v4 during the window | Weeks are not strictly comparable |
| One model labels, and the same model checks agreement | Labels are unvalidated against humans; this is the first thing the proposed study fixes |
| Judges, model ladder, server cutover and the auto-filer pause all changed in the same weeks | No change in any share is attributed to any single cause |
| CPU targets | Targets configured during the window were 90% (game server) and 70% (orchestration server, Mac); no target is recorded for the city simulation server in the source data. On 2026-11-14 the owner ordered 90% for all three servers. Both are in the CSV. |

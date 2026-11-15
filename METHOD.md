# Data and method

Every number in this repo comes from one of four sources, each read without writing to it. The three source repositories are private, so this repo carries aggregates only: no PR titles, no transcript text, no account identifiers. Weeks start Monday UTC. The latest week, starting 2026-11-09, has six days (data cut 2026-11-14).

## 1. GitHub: merges, opened PRs, merge share

- **Query:** `gh pr list --state all --limit 5000 --json number,createdAt,mergedAt,state` for each of the three repos, read-only. The data was cut on 2026-11-14.
- **Rerun check:** the same query was run again on 2026-11-15 and the weekly counts recomputed. Every weekly merge count from 2026-08-03 through the week of 11-02, and every merge share from 09-21 through 11-02, came out identical to the CSVs. Only the week of 11-09 has moved since the cut (150 merges then, 151 on the rerun). The CSVs keep the 11-14 cut, because the token figures use the same cut.
- **Merged PRs per week** (`data/weekly_merges.csv`): count of PRs by the week of `mergedAt`, per repo, 2026-08-03 to 2026-11-14.
- **Merge share** (`data/weekly_merge_share.csv`): PRs merged divided by PRs opened, by the week of `createdAt`, all repos pooled. PRs still open at the cut count as not merged. The latest week is provisional, not a lower bound: it was 132 of 152 (86.8%, 8 open) at the cut and 133 of 159 (83.6%) on the 11-15 rerun, because PRs opened late in a week have had no time to merge. Shown from 2026-09-21; earlier weeks have under 40 PRs opened.
- **Two windows, kept separate:** 1,118 PRs merged from 2026-10-14 to 11-14 (the one-month volume figure); 1,124 PRs merged in the weeks starting 10-12 through 11-09 (the denominator for tokens per merged PR).
- **Spec citation:** PR bodies parsed for a `## Spec` section citing spec lines. City simulation, by week from 10-14: 0 of 101, 8 of 107, 89 of 89, 105 of 105, 42 of 46. Game, by week from 10-21: 0 of 22, 53 of 98, 149 of 149, 86 of 86, 14 of 14. Orchestration: 392 of 493 over the month.
- **Judge rejection rate:** rulings parsed from review bodies of the form `Ruling: MERGE | CHANGES | HOLD`; the rate is rulings other than MERGE over all rulings. These weeks start on Wednesday 10-14, unlike the Monday weeks used everywhere else, so they are given here and not as a CSV.

  | Week starting | City simulation | Game | Orchestration |
  |---|---|---|---|
  | 10-14 | 0.24 | no rulings | no rulings |
  | 10-21 | 0.31 | 0.47 | 0.40 |
  | 10-28 | 0.21 | 0.39 | 0.38 |
  | 11-04 | 0.18 | 0.37 | 0.61 |
  | 11-11 (4 days) | 0.50 | 0.68 | 0.51 |

  The jump in the last four days follows the 11-09 model change. Whether it is a stricter judge or worse work has not been established. A HOLD is sometimes a request for more evidence, not a spec miss.

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

- **Alignment labels** (`data/weekly_alignment_labels.csv`): since 2026-10-26 one frontier model labels new issues and PRs against their repo's spec as written at the time; since 2026-11-09 also against the owner's prompts. It labelled 550 of 906 items created in the first week, 408 of 616 in the second and 196 of 196 in the third. Categories: misaligned (works against the spec), trash (work that should not exist), and unaligned (anything not fully aligned, a superset of the other two). Shares are of labelled items. The CSV holds the weekly summary figures, not label rows.
- **Auto-filer:** a second column set excludes items filed by an automatic ledger filer, which was paused during the window. Without those items the misaligned share is 13.6%, 7.4% and 0.6% (n 523, 350, 179) and the trash share 18.4%, 12.6% and 1.7%. So removing the filer's own items does not remove the fall. The pause may still have had indirect effects, and the rubric and model changes remain.
- **Owner-prompt labels:** of 192 items labelled against the owner's prompts from 11-09, 125 serve a prompt, 26 serve one in part, 26 are in the spec but unprompted, 13 are unclear and 2 work against a prompt.
- **Alignment monitor:** AUC 0.651 of the live 13-weight logistic monitor against the model labels (358 items); its guard caught 0 of 63 items labelled trash.
- **Labeler agreement:** kappa 0.755 on 50 items labelled twice by the same model. This measures consistency, not validity.
- **Weight-model candidates:** 7 proposed by the proposer harness since 2026-11-13; none beat the live baseline on a time-split held-out set, so none was adopted. That adoption bar is part of the harness design.
- **Utilization** (`data/host_utilization_7d.csv`): CPU sampled every 5 minutes per host, and idle or under-used flags raised by the capacity monitor, 2026-11-07 to 11-14. The CSV holds the summary figures of the utilization report, not sample rows.

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
| CPU targets | Targets configured during the window, checked against the utilization report: 90% on the game server, 70% on the orchestration server, none set on the city simulation server. The Mac's 70% is as stated by the owner. On 2026-11-14 the owner ordered 90% for all three servers. Both columns are in the CSV. |
| No code in this repo | The scripts that tally transcripts and draw the figures are kept outside it, so the figures cannot be rebuilt from this repo alone |
| Judge strictness | Rejection rates rose in the last four days; stricter judging and worse work are not separated |

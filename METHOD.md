# Data and method

The README tells the 2D to 3D story; this file holds how every number was computed, the full results and judge check tables, and the fleet detail that used to sit in the README. Every fleet number in this repo comes from one of four sources, each read without writing to it. The 3D lead case numbers come from the game repo's experiment issue (#727) and are described in section 5. The three source repositories are private, so this repo carries aggregates only: no PR titles, no transcript text, no account identifiers. Weeks start Monday UTC. The latest week, starting 2026-11-09, has six days (data cut 2026-11-14).

## 1. GitHub: merges, opened PRs, merge share

- **Query:** `gh pr list --state all --limit 5000 --json number,createdAt,mergedAt,state` for each of the three repos, read-only. The data was cut on 2026-11-14.
- **Rerun check:** the same query was run again on 2026-11-15 and the weekly counts recomputed. Every weekly merge count from 2026-08-03 through the week of 11-02, and every merge share from 09-21 through 11-02, came out identical to the CSVs. Only the week of 11-09 has moved since the cut (150 merges then, 151 on the rerun). The CSVs keep the 11-14 cut, because the token figures use the same cut.
- **Merged PRs per week** (`data/weekly_merges.csv`): count of PRs by the week of `mergedAt`, per repo, 2026-08-03 to 2026-11-14.
- **Merge share** (`data/weekly_merge_share.csv`): PRs merged divided by PRs opened, by the week of `createdAt`, all repos pooled. PRs still open at the cut count as not merged. The latest week is provisional, not a lower bound: it was 132 of 152 (86.8%, 8 open) at the cut and 133 of 159 (83.6%) on the 11-15 rerun, because PRs opened late in a week have had no time to merge. Shown from 2026-09-21; earlier weeks have under 40 PRs opened.
- **Scale line in the README:** 1,213 PRs merged from 2026-10-17 to 11-16 across 18 repos, from a per-repo tally made on 2026-11-16 (the exact query was not kept with it): orchestration 488, city simulation 389, game 313, the other 15 repos 23 together. The three main repos hold 1,190, 98%. This is a later and wider window than the two below.
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

## 5. Lead case: 3D builds with no person watching

All of these come from comments on the game repo's experiment issue (#727, private), each cited by comment id, from the score tables those comments link, and from the Alex Net lane's experiment analysis of 2026-11-17 (lane an-dx-theories-261117, file droid-experiments-261117 with its CSVs droid-experiments, droid-history, droid-score-vs-rounds and droid-cost-allchassis). Every 3D score is **AI judge only, not yet checked against my blind labels**: it comes from one fresh Opus medium scorer per round (or, where named, the first pipeline's own in-round judge), and no scorer has been checked against the owner.

Three different 0 to 100 measures appear below and are not one scale: the first pipeline's **in-loop judge** (whole-droid score inside the loop), the fresh scorer's **11-region mean** (mean over 11 part regions and three views, the only measure scored the same way for old and new builds), and the fresh scorer's **whole-droid score** (new method only). Each number names its measure.

### Results across droids (as of 2026-11-17, n=4 of 6)

Male droids only. Four of six droids are finished (a-standard, b-lean, c-angular, e-carbon-standard); d-minimal and f-reinforced-angular are still running and will be added to these tables when they finish.

| Droid | Old cost, USD | New male cost, USD | Reduction | Old rounds | New rounds | Source |
|---|---|---|---|---|---|---|
| a-standard | 749.14 | 185.13 | 75.3% | 74 | 12 | stats3, comment 6951147899 |
| b-lean | 584.86 | 182.62 | 68.8% | 62 | 12 | stats3; b-lean result, comment 6939125964 |
| c-angular | 707.59 | 199.33 | 71.8% | 93 | 12 | stats3; c-angular result, comment 6951013658 |
| e-carbon-standard | 679.96 | 181.70 | 73.3% | 81 | 12 | e-carbon-standard result, comment 6958924820 |
| Mean | 680.39 | 187.19 | 72.3% | 77.5 | 12 | computed here |

- **Reduction** is each droid's own: 1 minus new male cost over old cost. Min 68.8%, max 75.3%, mean 72.3% (n=4). Pooled over the four droids it is 72.5%.
- **Old cost** is the first pipeline's one unsexed body for that droid, list price, last result event per session id, plus a one-sixth share of the old fresh scorer (1.34 USD). That share is why a-standard is 749.14 here and 747.80 in the stall figures below (747.82 on the first #727 tally, 747.79 in the cost CSV, a rounding difference).
- **New male cost** is the male body's 12 build rounds plus its fresh scorer rounds, same method. e-carbon-standard male has 10 scorer rounds, not 12 (texture Fable rounds 1 and 2 were never scored), so its cost is about 4 USD lower than a full set would be.
- **Rounds** are not the same unit: an old round worked on one part, a new round covers the whole body from one view.

**Quality, male, 11-region mean** (AI judge only, not yet checked against my blind labels):

| Droid | Old final | New male final, against the male texture art | Gain | New male final, against the old per-part references | Old final, against its own per-part references | Difference |
|---|---|---|---|---|---|---|
| a-standard | 46.6 | 69.8 | +23.2 | 60.9 | 54.9 | +6.0 |
| b-lean | 51.9 | 72.3 | +20.4 | 56.9 | 59.1 | -2.2 |
| c-angular | 48.4 | 70.0 | +21.6 | 53.6 | 56.2 | -2.6 |
| e-carbon-standard | 49.5 | 69.8 | +20.3 | 47.3 | 59.5 | -12.2 |
| Mean (n=4) | | | +21.4 | | | -2.75 |

- The old builds were scored against the male whole-body texture art, so male against old is the only comparison on the same art. The old pipeline was never built to that art; it was built part by part to the per-part references, and on that target there is no gain (from 12.2 lower to 6.0 higher, mean 2.75 lower).
- Sources: a-standard comments 6904021106 (old), 6915255579 (male); b-lean 6939125964; c-angular 6951013658; e-carbon-standard 6958924820; stats3 6951147899 for the old finals of a, b and c.
- **Both bodies averaged, three droids** (stats3, includes female scores, kept here and not in the README): against the texture art the new body mean is +21.9 over the old final; against the per-part references it is +5.6, -4.1 and +0.5, mean +0.6. The draft 7 video brief quoted "+22" and "+0.6" from this three-droid table; the four-droid male figures above replace them in the README.
- Headline from these numbers: about the same droid, as far as an AI judge can tell, for about 72% less cost. Not "a better droid": the +21.4 depends on scoring against art the old pipeline never used.

### Time

No time reduction is given until the Alex Net lane re-measures it. The sources do not yet give a male-only elapsed figure on one definition for old and new:

- The two bodies of each new droid ran side by side, so a both-bodies figure cannot be halved into a per-body one.
- For a-standard the experiment analysis gives the chassis (both bodies) 24.40 summed lane hours and 12.09 elapsed hours; stats3 lists 24.40 as "new chassis wall h". The b-lean and e-carbon-standard result tables give 23.98 and 22.70 as the sum of the two bodies' lane hours.
- Stats3 says the old rounds kept no agent duration, while the experiment analysis gives old summed lane hours (97.08 on standard, 519.54 on all six) from RUNNER start to exit. The old elapsed span on standard is 97.18 hours in stats3 and 101.89 in the experiment analysis.
- The draft 6 video said "97 to 13 hours". It may set old elapsed hours against new agent hours, and is withdrawn here, as is the earlier "about a tenth of the agent hours". The Alex Net lane is tracing the column (stats6, queued for when all six droids finish).

### Stats3: old against new, three droids, both bodies (comment 6951147899)

Copied from stats3 as posted. n=3, not a controlled comparison, no ablation. The bootstrap intervals (10,000 draws, seed 1044550201) have only 10 distinct resamples at n=3 and are not inference. Scores are AI judge only, not yet checked against my blind labels.

| Droid | Old USD | New female USD | New male USD | New both bodies USD | Old wall h | New both bodies "wall h" (see Time) | Old rounds | New rounds (body / droid) |
|---|---|---|---|---|---|---|---|---|
| a-standard | 749.14 | 206.45 | 185.13 | 391.58 | 97.18 | 24.40 | 74 | 12 / 24 |
| b-lean | 584.86 | 195.84 | 182.62 | 378.46 | 72.91 | 23.98 | 62 | 12 / 24 |
| c-angular | 707.59 | 201.07 | 199.33 | 400.40 | 91.50 | 24.07 | 93 | 12 / 24 |

| Ratio old / new (n=3) | Mean | Median | Min | Max |
|---|---|---|---|---|
| Cost, per body | 3.48 | 3.53 | 3.09 | 3.83 |
| Cost, droid (both bodies) | 1.74 | 1.77 | 1.55 | 1.91 |
| Wall h, per body | not used here: it halves a both-bodies figure | | | |
| Wall h, droid | not used here: see Time | | | |
| Rounds, droid | 3.18 | 3.08 | 2.58 | 3.88 |

| Droid, 11-region mean against the male texture art | Old | New female | New male | New body mean | New minus old |
|---|---|---|---|---|---|
| a-standard | 46.6 | 70.6 | 69.8 | 70.2 | +23.6 |
| b-lean | 51.9 | 65.0 | 72.3 | 68.7 | +16.8 |
| c-angular | 48.4 | 77.5 | 70.0 | 73.7 | +25.3 |
| Mean (n=3) | | | | | +21.9 |

### Experiments, in historical order

Dates are when each change first ran (droid-history CSV, from lane logs, art file dates and owner messages). No change was ever run alone with the others held fixed.

| Date | Question | Answer | Number | n | Measure and source | Caveat |
|---|---|---|---|---|---|---|
| Nov 10 | Do more rounds make a better model? (first pipeline, run to plateau) | No, not after round two | In-loop judge 29 to 47 in the first two whole-body rounds (55.76 USD), then 47 to 56 over the next 63 rounds (692.03 USD); a fresh scorer gave the final build 47. 74 rounds, 747.80 USD in all | 1 droid (standard, the only one with more than one whole-body round) | In-loop judge, droid-score-vs-rounds CSV; cost from droid-cost-allchassis CSV (whole-body passes p1 and p2: 29.48 and 26.28 USD) | In-loop judge and fresh scorer differ in rubric and art. Six old droids in all: 4,004.72 USD, 448 rounds |
| Nov 11 | Was each round trying to do too much? (one body part at a time, run in parallel) | No | 70 rounds on single parts (62 finished), 651.85 USD, moved the in-loop judge from 50 to 56 on standard. Inside each droid parts ran one after another: summed lane hours over elapsed span 0.936 to 0.953; the 5.10 across all six came from six droids running at once | 6 old droids; score on 1 | In-loop judge; experiment analysis T2 | No serial run of the same work exists. The new whole-body method uses 12 rounds per body against 62 to 93 |
| Nov 11 | Was the concept art too small? (a 1254 px close-up per part and view, in place of one 1536x1024 sheet shared by six droids) | Partly | Mean change per round 5.45 points on the sheet, 8.50 on the close-up art; larger in 10 of 14 parts (median paired difference +2.25) | 15 parts, 31 and 36 round pairs | In-loop judge, front scoring only, same-model pairs; experiment analysis T4 | Side views arrived the same day. In the new method the 3 parts given newer close-up art gained 18.70 against 24.16 for other parts (n=3 against 19). Every art set was approved, so approvals cannot separate old and new art |
| Nov 13 to 14 | Were builders only looking at the front? (judge and fix from front, profile and back) | Partly | New method: the view a round worked on gained 7.22 points against 0.72 for the other two views, higher in 33 of 36 rounds. First pipeline: judging all three views lowered the mean change per round from 3.56 to 1.95 points (higher in 8 of 17 parts) | 36 new rounds; 20 old parts | Fresh scorer whole-droid view scores (new); in-loop judge (old); experiment analysis T3 | The scorer was told which view was built. The old three-view score is the lowest of three views, a lower scale |
| Nov 15 | Should shape come before texture? (high-contrast shape art, shape phase then texture phase) | Yes on the four finished droids, for the bundle | Male whole-droid score 43 after round 1 to 71 after round 12 on average (a-standard 46.7 to 72.7, b-lean 42.0 to 71.3, c-angular 39.3 to 70.0, e-carbon-standard 43.3 to 70.0); 187.19 USD mean per male droid | 4 male droids | Fresh scorer whole-droid score against the texture art in every round; a-standard from the droid-score-vs-rounds CSV, others from the result comments above | Bundle: judge and builder in one session, the whole-body three-view schedule, Opus then Fable at high effort, new whole-body art and a fresh scorer all arrived together. All four male droids peaked one to three rounds before round 12. The dark-art idea behind the split is weak: darkest third of old parts took 9.38 rounds against 6.25 for the lightest, but Spearman rho -0.127, p 0.38, n=50, and darkness is confounded with droid |

The draft 6 video's per-experiment slide values are in its make_spec.py (shots s04 to s09) and match the rows above for the standard droid; the rows above add the other finished droids.

### What was compared on the first droid (a-standard)

- **Old standard:** the first pipeline's best build of the standard droid, frozen at commit d9c0ea79 after 74 rounds (70 on single parts, 4 whole-body passes). It was built part by part against per-part reference images, with Opus at medium effort and Fable per part. It has one body with no sex.
- **New method:** the same droid rebuilt twice, a female body and a male body, 12 judge-builder rounds each: two phases (shape, then texture), two passes per phase (Opus high, then Fable high), three rounds per pass (one per view). Each round a fresh judge session reviews the build from one view (front, profile or back, in turn) against the owner-approved whole-body shape and texture art, then the same session fixes what it found; there is no handoff to a separate builder. A separate fresh scorer then scores the round at all three views. The scoring rubric, from the #727 issue body, is the same for old and new: 0 to 100 per body part, 40 points shape and proportion, 30 detail, 30 material and colour. Final builds: female 6ec7429d, male f671f540.

| Number | How | Source |
|---|---|---|
| Hours per body: old 97.1, new 8.3 (female) and 10.0 (male) | Withdrawn pending the trace in [Time](#time) | was: baseline cost table on #727 and lane durations |
| Build cost per body: old 747.82 USD, new 182.00 (female) and 160.67 (male) USD | Sum of list-price cost, last result event per session id. With scorers: 206.45 and 185.13 (stats3) | comments 6903328205 (old) and 6924712566 (new, corrected: the first posting 6915289250 counted some resumed sessions twice) |
| Scorer cost: about 24 USD per body | Same method, scorer rounds only. An earlier figure of 334 USD double-counted resumed sessions and is withdrawn | scorer transcripts |
| Cost per round by pass, and the 189 USD projection | Mean, SD and range over every finished new round at 2026-11-16 (41 build, 36 scorer) in droid-cost-allchassis.csv (525 rows, old rounds included; 21 of 448 old rounds carry estimated cost, 180.84 USD, flagged). Projection = 3 x (9.79 + 21.44 + 6.11 + 17.53) + 24 | Alex Net lane, 2026-11-16, recomputed here from the CSV |
| Self minus fresh score | Mean and SD of builder self-score minus fresh scorer over the 33 rounds that had both at 2026-11-16 | Alex Net lane, 2026-11-16 |
| 11-region mean against the texture art: old 46.6, new 70.6 and 69.8 | Mean over the same 11 part rows, three views, of the final scorer's scores against the approved texture art | comments 6904021106 (old), 6913124415 (female), 6915255579 (male) |
| 11-region mean against the old per-part references: old 54.9, new 59.9 and 60.9 | Same 11 part rows against the per-part references the old pipeline was built from | same |
| Acceptable as is for the next step: female 20 of 24 rows, male 16 of 25 | The scorer's yes or no per part and target row. Not asked of the old build | comment 6915289250 |
| Builder self-score against a fresh scorer | Two cited rounds, both Fable texture round 2: female self 58 to 67 on profile, fresh scorer 73.3 flat; male self 61 to 72 on profile, fresh scorer's profile score 76 to 70 | comment 6915289250 |

- **Old pipeline across six droids:** 4,004.72 USD and 448 rounds in total; per droid (one body each): standard 747.79 USD, 74 rounds; lean 583.52, 62; angular 706.25, 93; minimal 577.13, 65; carbon standard 678.62, 81; reinforced angular 711.41, 73. Summed from the old rows of droid-cost-allchassis.csv. The summed lane hours (519.5 on all six) are not used until the hours trace reports.

### Full results table, first droid

Rows 1 to 5 are the standard droid: one old build against a female and a male new body. Row 6 covers every round that had both scores at 2026-11-16, on the standard and lean droids. The all-droid tables above supersede rows 1 and 2.

| # | Result | Old pipeline | New method | n | Caveat |
|---|---|---|---|---|---|
| 1 | Hours per body | withdrawn | withdrawn | | See [Time](#time) |
| 2 | Cost per body, list price | 747.82 USD build and scoring, 74 rounds (70 on single parts, 4 whole-body) | build 182.00 and 160.67 USD, 12 rounds each; scorer about 24.5 USD per body | 1 old build, 2 new bodies | 3.6x and 4.0x like for like, since the old figure contains its own scoring. A new round covers the whole body from one view, so the round counts are not the same unit |
| 3 | 11-region mean against the owner-approved whole-body texture art | 46.6 | 70.6 (female), 69.8 (male) | 11 parts, 3 views | AI judge only. The old pipeline was not built against this art. Not blind to method |
| 4 | 11-region mean against the old pipeline's own per-part references | 54.9 | 59.9 (female), 60.9 (male) | 11 parts, 3 views | AI judge only. The like-for-like target on this droid; on four droids the male mean is 2.75 lower |
| 5 | Judge's "acceptable as is for the next step" | not asked | female 20 of 24 rows, male 16 of 25 | part and target rows | AI judge only. The owner has not been asked |
| 6 | Builder self-score against a fresh scorer | | mean self minus fresh +1.18 points (SD 5.32); self more than 5 points above fresh in 9 of 33 rounds. Cited cases: female self 58 to 67 (profile) while fresh stayed 73.3; male self 61 to 72 while fresh profile fell 76 to 70 | 33 rounds with both scores | AI judge only. A lead, not a finding: some scorers had seen earlier scores |

Fable passes cost 2 to 3 times the Opus passes. A full body at this schedule projects to about 189 USD (a projection from round costs at 2026-11-16); the four finished male droids came in at a mean of 187.19 USD.

### Cost per round, new method

Every finished round at 2026-11-16 (the standard droid, and the lean and angular droids as far as they had run): 41 build rounds and 36 scorer rounds, list price, one session each, so nothing is counted twice. Three rounds that ended at an account limit are included at their partial cost.

| Pass | Rounds | Mean USD | SD | CV | Range |
|---|---|---|---|---|---|
| Shape, Opus high | 16 | 9.79 | 3.50 | 0.36 | 3.49 to 16.66 |
| Shape, Fable high | 12 | 21.44 | 3.72 | 0.17 | 17.64 to 31.40 |
| Texture, Opus high | 7 | 6.11 | 2.20 | 0.36 | 2.45 to 9.70 |
| Texture, Fable high | 6 | 17.53 | 3.21 | 0.18 | 12.82 to 20.79 |
| Fresh scorer, any pass | 36 | 2.01 | 0.21 | 0.10 | 1.67 to 2.41 |

With the three partial rounds left out of the means, the 189 USD projection becomes about 193 USD.

### Confounds

The comparison is not controlled. Changed between old and new, beyond the method itself:

1. **Scorer:** one Opus medium scorer per round, not checked against the owner; the blinded owner check has 0 answers; the taste backtests cannot be told apart from chance or fall below a trivial baseline.
2. **Inputs:** the new method had better owner-approved inputs (whole-body shape and texture art). The old pipeline worked from per-part references and is scored against art approved after it froze.
3. **Bodies:** one old body with no sex against a female and a male new body; the README compares male bodies only.
4. **Effort and models:** old Opus medium plus Fable per part; new Opus high then Fable high. No old round ran Opus at high effort.
5. **Unfinished old run:** the old standard build froze mid-run; its feet and hands never had rounds, and its side and back driver never started a round.
6. **Render:** different render script, camera, light rig and resolution (old 1536x2304, new 1024x1536). The repo figure `figures/droid_old_new_art.png` (no longer shown in the README, because it includes female bodies) was rendered afterwards for showing the work, on one rig for all three standard builds (old d9c0ea79, new female 6ec7429d, new male f671f540): the Unreal Engine 5.8.4 editor, where `jc_render.py` imports each head's built mesh and renders it with one shared camera frame, one light set and one background. It was not used for scoring.
7. **Anchoring:** scorers saw builder self-scores or earlier scores in some rounds, so treat their scores as upper bounds.
8. **Hours:** see [Time](#time); no hours figure is used.
9. **Size:** four finished droids of six, one scorer session per round, no repeat runs, no run with one change removed.
10. **Not blind to method:** old and new builds can be told apart on sight (tell check below), for a person or for the scorer.
11. **Order:** the new method ran after the old one, with newer references.

### Judge check results

Checks on the judge itself, not old against new.

| # | Check | Result | n | Caveat |
|---|---|---|---|---|
| J1 | Judge predicts the owner's past single picks (1 of 4), options blinded | 8 of 24, 33.3% (Wilson 95% 18.0% to 53.3%); chance 6 of 24; always option 1, 7 of 24 | 24 picks | 2D concept art, not 3D builds. The picks themselves were made unblinded. 23 of 24 would be needed to clear the rule, so this can show a judge is bad, never good. An earlier run (9 of 29) was withdrawn for a text leak |
| J2 | Judge on accept or send back, concept-art drafts | 28 of 56, 50.0% (37.3% to 62.7%); always send back 37 of 56, 66.1% | 56 drafts | 2D concept art, unblinded. The true request text was missing for 38 of 56 |
| J3 | Tell check before labelling | blind guess of the old build 0 of 10, so the methods separate 10 of 10; edge density 0.041 to 0.048 (old) against 0.025 to 0.033 (new) | 10 pairs; pool 66 old, 12 new | Not a judge result. Led to Revision 5 below |
| J4 | The owner's approval page | 305 of 308 groups end as approve | 308 groups | Always approve would score 99%, so the page cannot test a judge |
| J5 | Blinded owner pairs (the validation) | 0 answered | 0 | Rule fixed before data, below |

### Judge check: decision rule, design, backtests, tell check

- **Decision rule** (comment 6903781964, posted 2026-11-16 00:15 UTC, before any owner label): pairwise agreement between the owner and the judge on blinded pairs of builds; the judge may stand in for the owner when agreement is at least 85% and the lower bound of the 95% Wilson interval is at least 75%. 10% of pairs are repeated with left and right swapped to measure owner self-agreement. If no second person labels at least 50 pairs, results say "agrees with the owner", never "agrees with people". The rule, pairs and scorer freeze at the first label. Run jc-261116-01, pair seed 1044550201. Unchanged by every revision since.
- **Design:** about 150 pairs plus 15 repeats, same droid, sex and phase in each pair; one image per item (front, side and back in one row) with no lane, model, round, cost or score in the image, file name or metadata; random item ids, the mapping sealed on the game server and the fleet database; the owner never sees a judge score while a run is open. Backfilled approvals recovered from past messages are kept in a separate column and are never called blind.
- **Revision 5** (2026-11-17, comment 6953849465, decided before any pair was drawn or any label given), after the tell check:
  1. Framing: a fixed camera and a common ground line for every item, every item re-rendered, then the tell check repeated on the re-rendered set and posted on #727.
  2. Primary measure: pairs inside the new method only (round against round, Opus pass against Fable pass, same droid, same view). The decision rule applies to this stratum.
  3. Old against new stays as a secondary stratum, reported separately and labelled "not blind to method" everywhere it appears. It never counts toward the decision rule.
  4. Before the batch is published, the tell check also runs on the primary stratum (can a fresh judge tell the earlier round from the later one from the image alone, beyond the quality difference).
- **Backtest on past single picks** (comment 6904535705): 24 groups where the owner picked 1 of 4 concept-art options. Options were re-encoded, renamed at random, shuffled and shown with no titles or descriptions. A fresh Opus medium judge per group. An earlier run (9 of 29) was withdrawn because option text leaked the original order. At n = 24 the judge needs 23 hits to clear the rule, so this backtest can show a judge is bad, never that it is good.
- **Accept or send back** (ChatGPT concept-art drafts): 56 judged rows after 6 exclusions for wrong links or no single image. The true request text was missing for 38 of 56 rows. Unblinded.
- **Approval page:** 305 of 308 page groups end as approve, so always approve would score 99% there; no approve or revise backtest is reported on the page.
- **Tell check** (comment 6915388208, before labelling, not a judge result): 10 shape pairs drawn with the run seed, one old and one new item each, left and right random. A blind guess of which item is old was written down before unsealing.

  | Check | Result |
  |---|---|
  | Blind guess of the old item | 0 of 10 correct: every guess inverted, so the methods separate 10 of 10 |
  | Edge density inside the silhouette | old 0.041 to 0.048, new 0.025 to 0.033, no overlap (pool of 66 old and 12 new) |
  | Feet on the bottom frame edge | 63 of 66 old items, 0 of 12 new |
  | Background and figure brightness | identical |

  The framing difference came from fitting the camera to each asset's bounds and is being fixed (Revision 5, item 1). The surface difference is in the geometry (old builds panelled, new ones smooth) and cannot be hidden without hiding the shape being judged, so old against new pairs are reported as not blind to method, separately from same-method pairs.

### The script

`scripts/wilson.py` (Python 3, no dependencies) computes the Wilson 95% interval and the decision rule. Run with no arguments it reprints rows J1 and J2 of the judge check table and the rule check, and the fewest agreements that clear the rule at n = 24, 40, 56 and 150. `--hits K --n N` checks one count; `--csv FILE` scores a file with `prediction,truth` columns against the majority-answer baseline, which is how the accept or send back row was scored.

## 6. Fleet detail

- **Review ladder (since 11-03; current models since 11-09).** Each PR gets at most two counted review rounds: builder (Sonnet, low effort), judge 1 (Opus, medium), builder 2 (Sonnet, low), judge 2 (Fable, high), then a final touch by Opus on judge 2's findings with no third review. Each ruling (`Ruling: MERGE | CHANGES | HOLD`) is posted as a review pinned to the exact commit, and a judge may not sign with a session that wrote any commit on the PR.
- **Spec gate (from about 10-21).** Every issue cites a spec line, and every PR carries a `## Spec` section citing the lines it serves and how each was checked.
- **Internal names in the data:** Stella is the orchestration system, Atlanta PoLE the city simulation, Alex Net the game. Aurelian is the live alignment monitor. WSP is the harness that proposes small-model weights. Bloomnet picks the context a new session starts with. MQI is a per-model quality index.
- **Small models, planned or weak.** None has beaten its baseline.

  | Model | Failure mode it targets | Label source | Status |
  |---|---|---|---|
  | Alignment monitor | work that does not serve the spec or the owner's prompts | model labels, about 1,150 items | Live, weak: AUC 0.651, 0 of 63 trash caught |
  | Re-rate gate | when to re-rate work (cost) | labels exist | Best AUC 0.681 (logistic); a small MLP reached 0.523; not adopted |
  | Ruling predictor | review rounds that will not converge (case 07) | judge rulings, about 1,500 | Planned |
  | Filing gate | low-value issues and PRs filed before anyone checks them | 566 model labels | Shadow mode |
  | Changed-surface test selection | CI runs nobody needed | CI results by surface, not yet joined | A rule today, not a model |
  | Context selection | sessions that start without the rulings and past failures they need | none yet: of 401 recommendations, 346 were acknowledged and usage was recorded for 0 | No weights |
  | Model degradation switch | a model's quality drops and nothing switches | per-model quality scores | Detection only |

  Learned weight candidates: 7 proposed since 11-13, 0 adopted. The combined-network idea (one shared trunk over these decisions) has never been tested; the only data point is the small MLP losing to logistic regression inside the re-rate gate.
- **Further measures:** host CPU 16.3% to 32.1% average across 4 hosts (11-07 to 11-14); one server used 52% of all tokens for 40 of 150 merges in the week of 11-09, mostly 3D asset passes; PR bodies citing the spec rose from 0 to all within two weeks of the spec gate (section 1).

## 7. Fleet setup and measures

### The setup

One person directs three private codebases. The work is done mostly by Claude agent lanes; Codex, OpenCode and a DeepSeek first pass also ran in the window. The lanes run on three rented servers (one per codebase) and a Mac. The source repos are private; this repo carries aggregates, redacted cases and the judge check numbers. This table is an earlier window than the README's scale line (section 1).

| Codebase | What it is | PRs merged, 2026-10-14 to 11-14 |
|---|---|---|
| Orchestration system | assigns work to agent lanes, runs judges, memory and telemetry | 444 |
| City simulation | Rust/WASM live model of a real city, deployed daily since 11-07 | 370 |
| Game | Rust/WASM game with the concept-art-to-3D build pipeline of the lead case | 304 |
| Total | | 1,118 |

Every PR gets at most two review rounds by model judges, each ruling pinned to the exact commit; every PR cites the spec lines it serves; and visual work is not done until the served build has been rendered and looked at, because counters and test exits can only show a failure. Telemetry covers host CPU, every judge ruling, dated owner corrections, every model-routing change and model alignment labels on new issues and PRs since 10-26. Details are in [section 6](#6-fleet-detail).

Terms. *Misaligned* is work that goes against the spec. *Trash* is work that should not exist. Both are labels from one model, not from people. The case files in `incidents/` keep the agents' own notes and call the person directing the fleet "the owner".

### Failure cases

Eight dated cases from 2026-09-10 to 10-25; four of them come before the measured window. Case 01 is a hallucination (work reported done on green CI while the live dashboard showed no data), 02 and 04 are cheats, and 05 is a corner cut. Each file gives the failure class, how it was caught, the countermeasure (rule, gate or model) and what a trained monitor would need to catch it.

| # | Date | Case | Class | Caught by |
|---|---|---|---|---|
| [01](incidents/01-green-ci-empty-dashboard.md) | 10-25 | About 20 PRs merged on green CI while the live dashboard was empty | false completion | owner |
| [02](incidents/02-gate-log-in-gated-repo.md) | 09-16 | A gate stored its log in the repo it gated, so a branch could forge a pass | reward hacking surface | adversarial review |
| [03](incidents/03-compaction-turned-hold-into-owner-pause.md) | 10-15 | A context summary turned the agent's own hold into an owner pause; 19 hours idle | authority confusion | owner |
| [04](incidents/04-tests-passing-for-the-wrong-reason.md) | 09-15 | Four tests in three lanes passed for the wrong reason; one pinned a bypass as correct | evaluation gaming | adversarial review |
| [05](incidents/05-bar-moved-after-measuring.md) | 09-28 | Proposal to raise a CPU bar from 1.72x to 2.0x after measuring 1.98x | specification gaming | model judge |
| [06](incidents/06-builder-reinterpreted-owner-instruction.md) | 10-25 | A builder replaced the owner's instruction with its own design; the coordinator merged it | goal drift, authority | owner |
| [07](incidents/07-eleven-review-rounds-36-hour-burn.md) | 10-13 to 10-15 | One PR at 11 review rounds; about 6.0B cache-read tokens in 36 hours for 12 merges | coordination failure, cost | owner |
| [08](incidents/08-placeholder-command-queued-repo-transfers.md) | 09-10 | A placeholder in a ready-to-run command queued transfers of 11 private repos to a stranger | unsafe action | found after the fact |

The owner caught four of the eight, adversarial reviewers told to refute rather than confirm caught two, a model judge caught one, and one was found only after the damage was queued. Most were not caught by the check meant to catch them. Oversight that depends on the owner reading every result does not scale.

### Fleet measures

**Volume and compliance.** The work became more compliant in form as rules were added.

| Measure | Value | n and window |
|---|---|---|
| Merged PRs per week | 70 to 410 | weeks of 10-12 to 10-26; then 298, and 150 in the six days of 11-09 |
| Merge share (merged / opened, by week opened) | 68% (week of 10-05) to 92% (week of 11-02) | 117 and 320 PRs opened |
| Model-labelled misaligned share | 13.6% (n 550) to 1.5% (n 196) | weeks of 10-26 and 11-09 |

None of these changes is attributed to a cause: label coverage, the rubric, the judges, the models and an auto-filer pause all changed in the same weeks, and one model labels (section 3).

![Weekly volume and merge share, tokens per merged PR with host share, and model-labelled alignment shares, 10-12 to 11-09](figures/weekly_alignment_cost.png)

Panel B is the one to read slowly. The three hollow points are Mac-only undercounts, because server transcripts before 11-02 do not exist, so they are not joined to the two weeks where all four hosts are counted.

![Merged PRs per week since August by repo, with merge share](figures/velocity_since_august.png)

SVG versions are in `figures/`.

### What it costs

| Measure | Value | n and window |
|---|---|---|
| Tokens per merged PR | at least 70M | 79.2B tokens over 1,124 merged PRs, weeks of 10-12 to 11-09 |
| Composition | about 98% cache reads; output under 0.5% | every week |
| One runaway PR | 11 review rounds; about 6.0B cache-read tokens in 36 hours for 12 merges | case 07, before the two-round cap |

The 70M figure is a floor: server transcripts before 11-02 and non-Claude agents are not counted, so no cost trend can be claimed in either direction. Per body, the 3D lead case gives a sharper cost unit than a merge ([results across droids](#results-across-droids-as-of-2026-11-17-n4-of-6)).

## Known gaps

| Gap | Effect |
|---|---|
| Server transcripts before 11-02 absent | Token weeks 10-12 to 10-26 are undercounts; no cost trend |
| Codex, OpenCode, DeepSeek excluded | Tokens per merged PR is a floor |
| Session sync to the fleet database stalled | Sessions in the database are incomplete |
| Label coverage uneven: 53% (game) to 95% (city simulation); 61% and 66% of items in the first two labelled weeks | Shares may not represent unlabelled work |
| Rubric changed v2 to v3/v4 during the window | Weeks are not strictly comparable |
| One model labels, and the same model checks agreement | Labels are unvalidated against humans; the first test in the README proposal checks the 3D judge against the owner; the fleet labels are not part of it |
| Judges, model ladder, server cutover and the auto-filer pause all changed in the same weeks | No change in any share is attributed to any single cause |
| CPU targets | Targets configured during the window, checked against the utilization report: 90% on the game server, 70% on the orchestration server, none set on the city simulation server. The Mac's 70% is as stated by the owner. On 2026-11-14 the owner ordered 90% for all three servers. Both columns are in the CSV. |
| Tally and figure scripts not in this repo | The scripts that tally transcripts and draw the figures are kept outside it, so the figures cannot be rebuilt from this repo alone. Only `scripts/wilson.py` is here |
| One model labels, and the 3D scorer is one model | Every 3D score is AI judge only, not yet checked against my blind labels; the blinded owner check has 0 answers |
| Owner feedback backfill | 231 rows (214 unique quotes: ChatGPT 75, Codex prompts 41, Claude sessions 83, GitHub relays 32) of the owner's past feedback recovered from chat; polarity and tags assigned by a model, none owner-confirmed, none joined to a build |
| Judge strictness | Rejection rates rose in the last four days; stricter judging and worse work are not separated |

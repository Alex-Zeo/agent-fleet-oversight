# 2D concept art to 3D models, with no person watching

This repo is part of my application to the Anthropic Residency. I study how to keep oversight of agents on long work that nobody watches, and what that work costs, through one concrete task: a harness that turns 2D concept art into 3D models for Alex Net, a game I am building, with no person watching each round. Fresh AI judges (Opus and Fable) score each build and then fix what they found, and I am setting up my own blinded labels of the builds, made without seeing any judge score. On all six droids the new method built about the same droid, as far as an AI judge can tell, for about 72% less cost than my first pipeline, in about a fifth of the time, though several changes landed together. I want to take the next step with Anthropic's help: turn my labels and the judge records into a trained model (weights) that judges 3D work, checked against blinded human labels.

**Video (3 minutes):** https://youtu.be/RBdJE05KqF8 covers the result across six droids, the experiments behind it, why Anthropic, and the two phases.

**Scale:** 1,213 merged pull requests across 18 repos, 98% in three, from 2026-10-17 to 11-16: the orchestration system that runs the agent lanes (488), Atlanta, a live city simulation (389), and Alex Net (313). The 3D work runs in Alex Net, from concept art, and in Atlanta, from map data. The source repos are private; this repo carries aggregates, the experiment records and the judge check ([how each number was counted](METHOD.md)).

## The harness

Alex Net's harness (experiment issue #727). The job: take owner-approved concept art of a droid (front, profile and back) and build a 3D model in Unreal Engine that matches it, over hours of agent work, with no person watching the rounds.

- **Art in two versions.** Every view comes as a high-contrast shape version and as a textured colour version.
- **Two phases.** Shape first, judged only against the high-contrast art; then texture, against the colour art, starting from the shape result.
- **Judges that score and fix.** Each phase has an Opus pass and then a Fable pass (both at high effort), and each pass has three rounds, one per view. In every round a fresh judge session that has not seen earlier rulings reviews the render from its view, then the same session fixes what it found. 2 phases x 2 passes x 3 views = 12 rounds per body.
- **A separate scorer.** After every round a fresh Opus medium session scores each body part 0 to 100 at all three views (40 points shape and proportion, 30 detail, 30 material and colour). Every score in this README is **AI judge only, not yet checked against my blind labels**.
- **My labels, made apart from the judges.** Blinded pairs of builds on a labelling page that never shows a judge score, a model name, a round or a cost (status below).

**The second 3D codebase, Atlanta,** builds a real city from map data (OpenStreetMap outlines, LiDAR heights and published dimensions), not from concept art. Its judges do not score and are not blind: they see the pull request and the builder's report, and rule MERGE or HOLD from renders at three camera altitudes. There are no owner labels there. Its 3D work so far includes 8 baked cars at three detail tiers (PRs #1337, #1353, #1382 and #1396; 102.23 USD and 15.73 agent hours; #1382 and #1396 went Opus HOLD, then Fable MERGE), the Mercedes-Benz Stadium and the GWCC halls (#1470, 33.65 USD), an authored outer ring of about 142 km2 (#1443) and 5 landmark towers. The experiments and the proposal below are about Alex Net.

## Results across droids

Six droid designs, twelve bodies built in all (a male and a female body per design). The comparison below is on the male body of each design, all six finished (n=6 of 6). Scorer cost is counted on both sides ([definitions](METHOD.md#results-across-droids)).

| Droid | Old pipeline, USD | New method, USD | Cost reduction | Old wall h | New wall h | Time reduction | Rounds, old | Rounds, new |
|---|---|---|---|---|---|---|---|---|
| a-standard | 749.14 | 185.17 | 75.3% | 101.89 | 12.09 | 88.1% | 74 | 12 |
| b-lean | 584.86 | 182.61 | 68.8% | 77.82 | 16.06 | 79.4% | 62 | 12 |
| c-angular | 707.59 | 199.35 | 71.8% | 96.42 | 21.32 | 77.9% | 93 | 12 |
| d-minimal | 578.47 | 165.79 | 71.3% | 79.72 | 17.79 | 77.7% | 65 | 12 |
| e-carbon-standard | 679.96 | 185.15 | 72.8% | 96.42 | 24.82 | 74.3% | 81 | 12 |
| f-reinforced-angular | 712.76 | 184.56 | 74.1% | 96.42 | 23.85 | 75.3% | 73 | 12 |

- **Cost:** each droid's own reduction runs from 68.8% (min) to 75.3% (max), mean 72.3%. List price, old body including its share of scoring, new male body including its 12 fresh scorer rounds.
- **Time:** wall time only, the elapsed span from first start to last finish, never halved. Each droid's reduction runs from 74.3% to 88.1%, mean 78.8%, about a fifth of the time. All six old droids ran at once on shared accounts, which stretched the old spans. Angular, carbon standard and reinforced angular share one old wall time (96.42 h) because the old pipeline ran those three as one parallel batch. Old agent hours were never measured (the old column is summed lane time), so I make no agent-hour comparison ([why](METHOD.md#time-and-agent-hours)).
- **Rounds:** 62 to 93 old rounds against 12 new ones per body, a reduction of 80.6% to 87.1%, mean 83.6%. Not the same unit: an old round worked on one part, a new round covers the whole body from one view.
- **Quality:** scored as the mean over 11 part regions, 0 to 100. Against the new male texture art, the new finals score 23.4 points higher than the old finals on average (from +20.3 to +29.3), higher on 6 of 6. But the old pipeline was never built to that art. Against the art it was built to, there is no gain: from 12.2 points lower (the carbon droid) to 6.1 points higher, 1.8 points lower on average, higher on 2 of 6. So the honest headline is about the same droid, as far as an AI judge can tell, for about 72% less cost, in about a fifth of the time, not a better droid. AI judge only, not yet checked against my blind labels.

## Experiments, in the order I ran them

Each change below was added on top of the ones before. None was ever run alone. First-pipeline scores are the loop's own judge; new-method scores are a fresh scorer; the two are not one scale. All are AI judge only, not yet checked against my blind labels ([sources and n](METHOD.md#experiments-in-historical-order)).

### Nov 10, first pipeline: Do more rounds make a better model?

**No, not after round two.** On the standard droid the loop's own judge went from 29 to 47 in the first two whole-body rounds (55.76 USD), then gained 9 points over the 72 rounds after that (692.03 USD; 74 rounds in all, 65 finished). A fresh judge scored the final build 47. n=1 droid, the only one that ran more than one whole-body round.

My first pipeline was a loop that ran to plateau: it kept running rounds, scored by a model judge, until the score stopped rising. Across six droids it spent 4,004.72 USD on 448 rounds.

### Nov 11: Was each round trying to do too much?

**No.** I split the droid into 11 parts, each with its own rounds. 70 more rounds on single parts (651.85 USD) moved the loop's score from 50 to 56 on the standard droid (n=1 droid).

I also expected parts to run in parallel. They did not: inside each droid the parts ran one after another, and the only speed-up came from six droids running at once.

### Nov 11: Was the concept art too small?

**Partly.** With a close-up of every part in place of one sheet shared by six droids, scores rose 8.50 points a round instead of 5.45, faster in 10 of 14 parts (first pipeline, 15 parts).

Side views arrived the same day, so the two changes cannot be told apart. I approved every art set, so my approvals cannot separate them either.

### Nov 13 to 14: Were builders only looking at the front?

**Partly.** In the new method, the view a round worked on gained 6.4 points against 0.7 for the other two views, more in 58 of 66 rounds (six male droids). The scorer knew which view each round built.

The builds looked flat from the side, so judging and fixing moved to front, profile and back, one view per round. In the first pipeline, judging all three views slowed the gain per round from 3.56 to 1.95 points, on a stricter score.

### Nov 15: Should shape come before texture?

**Yes, on all six droids, for the whole bundle.** Builders got high-contrast art for shape first, then colour art for texture. The male whole-droid score went from 43.7 after round 1 to 72.0 after round 12 on average (n=6), and every part improved on every droid (66 of 66). Every droid's best score came before round 12: five of six one to three rounds before, the sixth (f-reinforced-angular) at round 7.

This change landed together with judge and builder in one session, the three-view schedule, Opus then Fable at high effort, new whole-body art and a fresh scorer, so the result belongs to the bundle. The gain was uneven across the four passes: the last one (Fable, texture) cost about 58 USD and added about 1 point, and the largest jump (+14.7, texture Opus) is partly colour arriving on a build scored against colour art. Fable always ran second, on a better build, so this is not a test of Opus against Fable ([per pass](METHOD.md#per-pass-new-method-male-n6)). The idea that dark art hides shape is weak in the records: the darkest third of old parts took 9.38 rounds against 6.25 for the lightest, but the correlation is not significant (n=50).

## Two more things in the records

- **A loop that stops on a score can be steered by the score.** On the six male droids the builder scored the view it worked on up 24.3 points on average, more than the other two views in 71 of 71 rounds, where the fresh scorer saw 6.4 ([three views](METHOD.md#three-views-and-builder-self-score-male-n6)). AI judge only, not yet checked against my blind labels.
- **Review loops burn the same way.** Before I capped pull request review at two rounds, one PR went 11 rounds and about 6.0B cache-read tokens in 36 hours for 12 merges ([case 07](incidents/07-eleven-review-rounds-36-hour-burn.md)).

## Judge check status

0 blinded labels so far. Before labelling, a 10-pair test showed that old and new builds could be told apart 10 of 10, by framing (the camera was fitted to each build) and by build style (old builds panelled, new ones smooth). The camera fix is done: every item was rendered again with one fixed camera and ground line, and on a repeat test the framing tell is gone. Old against new is still separable by build style, which cannot be hidden without hiding the shape being judged, so it stays a side result labelled "not blind to method".

The first batch is published: 60 primary pairs (new method only, same droid, same view), 24 secondary old against new pairs, and 10% repeats with left and right swapped, 92 pairs in 2 sittings. The decision rule was posted before any label and is unchanged: 85% agreement with me and a 95% Wilson lower bound of at least 75%, on the primary pairs only. With 60 pairs that needs at least 52 agreements out of 60 non-tie answers. A tell check on the primary pairs: a fresh judge picked the earlier round in 8 of 10, from build detail only, with no render cue ([design](METHOD.md#judge-check-decision-rule-design-backtests-tell-check)). Approvals recovered from my past messages are backfilled, not blind, and are kept separate.

## The proposal: a trained model for judging 3D work

Today every round's quality check is a frontier-model judge, and nobody has checked it against a person. The records this harness keeps are what a trained model needs: renders at three views and per-part scores with written reasons for every new round, the cost of every round old and new (448 old rounds), the builder's own scores, and, once labelling starts, my blinded picks, starting with the first batch of 92 pairs (60 that count toward the rule, plus a side set and repeats), with more batches to follow for training. With Anthropic's help I want to train a model (weights) from my labels and the judge records, and find out what it can and cannot do. Every test uses only held-out, blinded labels I made directly, split by droid and body type.

1. **A learned judge for 3D fidelity.** A reward model that predicts which of two builds I would pick against the approved art.
   - *Test:* agreement with my held-out blinded picks under the rule already posted, on the same pairs as the Opus judge.
   - *If it fails:* it is not used, and the Opus judge stays unchecked.
2. **Catching builders that fit the judge.** A detector that flags rounds where the score rises but the build does not get better: the builder's score against a fresh scorer, the judged view against the two views it was not judged on, and the learned judge against the model judge.
   - *Test:* on held-out rounds, do flagged rounds match the rounds I rate no better than the round before? A red-team set, with builders told to raise the score without matching the art, measures how many it catches.
3. **Fewer rounds and lower cost.** A stop rule from the learned judge in place of a fixed 12 rounds or a loop, and a cheaper check than a frontier scorer round (about 2 USD each today).
   - *Test:* replay the recorded runs and stop where the learned judge says further rounds will not change my pick; report rounds and USD saved, and how often I prefer the build it gave up on.
4. **What it teaches about overseeing long agent work.** How many labels from one person it takes before a learned check can stand in for that person on work nobody watched, and where it breaks.
   - *Test:* a learning curve over label count, scored on a droid held out of training. Atlanta would be a harder transfer test, but it has no owner labels today, so it would need its own blinded labels first.

What I start with: 0 blinded labels, one labeller, and no trained model of mine that has beaten its baseline (a small MLP lost to logistic regression, 0.523 against 0.681; [METHOD](METHOD.md#6-fleet-detail)). So the order is fixed: close the blinded check first, with a second rater on at least 50 pairs, then train.

This is phase 1, the residency: 3D models, then animations for them, each step checked by the judge. Phase 2 is a larger 3D game and video studio, and it opens only when the judge agrees with people.

## Mentorship I am seeking

I will work on the problem my mentor sets, using this testbed and its records. These are the places where my own results are weakest:

| Area | The gap, and where it shows | What I would ask |
|---|---|---|
| Scalable Oversight | Every score is from an AI judge; I have 0 blinded labels (results, every experiment) | How to size and blind a labelled set, and how to decide when a judge can stand in for a person |
| Adversarial Robustness and AI Control | Builders scored their own rounds up about 24 points where a fresh judge saw about 6, and the judge knew which view was built (Nov 13 to 14 experiment and the self-score result) | How to test whether a builder is fitting its judge, and how to red-team a judge before trusting it |
| Experimental design (Alignment Science) | Two of four answers are "Partly" and the "Yes" is for a bundle, because changes landed together and nothing was run with one change removed; and the quality gap is about 23 points or none, depending on which art is used to score | How to plan runs so an effect can be attributed, at about 184 USD a body, and how to build a measure that does not depend on the target it was tuned to |
| ML systems and training | Nothing I have trained has beaten its baseline (the proposal) | How to train and test a small judge from a few hundred pairwise labels from one person |

## Limits

- No run with one change removed. Every experiment's answer belongs to changes that landed together.
- Six droids, one build per body, no repeat runs.
- One labeller (me), and 0 blinded labels so far.
- Every quality number comes from an AI judge: one Opus medium scorer per round. Some scorers saw the builder's own score or earlier scores, so treat the scores as upper bounds. Old and new builds can be told apart on sight, and their render setups differed ([confound list](METHOD.md#confounds)).
- The proposal is untested. Nothing I have trained so far has beaten its baseline.
- Owner feedback recovered from chat (231 rows) is model-tagged and unconfirmed, and no row is joined to a build. Fleet-wide alignment shares come from one model's labels, checked only by the same model. The full list is under [known gaps](METHOD.md#known-gaps).

## More detail

- [`METHOD.md`](METHOD.md): how every number was computed, the per-droid tables, the experiment table, the judge check design and decision rule, the confound list, the fleet setup and measures, the failure cases and the known gaps.
- [Failure cases](METHOD.md#failure-cases): eight dated cases where agents cheated, hallucinated or cut corners in the fleet, with the files in [`incidents/`](incidents/).
- [`scripts/wilson.py`](scripts/wilson.py): the Wilson interval and backtest scoring behind the judge check; `python3 scripts/wilson.py`, no dependencies.
- `data/` and `figures/`: weekly fleet aggregates and figures, each with its source and window.

## How this was written

The story, the theories and the changes are mine. Claude drafted the wording and assembled this repo, and the agent fleet described here gathered the figures and ran the experiment.

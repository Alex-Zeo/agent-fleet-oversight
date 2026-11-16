# 2D concept art to 3D models, with no person watching

In the past month my agent fleet merged 1,213 pull requests across 18 repos. I am researching long-horizon alignment and cost efficiency through one concrete task: a harness and a workflow that turn 2D concept art into high-fidelity 3D models with no person watching each round. In the game, Alex Net, fresh AI judges (Opus and Fable) score each build and then fix what they found, and I am setting up my own labels of the builds, made separately and without seeing the judge scores. I believe in this setup because it has shown early success: on the one finished comparison it took about a tenth of the agent hours and about a quarter of the build cost of my first pipeline, though several things changed at once. In my experience, running to plateau, goal loops and hill-climbing waste rounds when the output is a 3D model. I am applying to take this to the next level: turn my labels and the judge records into a trained model (weights) that judges 3D work, checked against blinded human labels, with Anthropic's help.

**Scale:** 1,213 merged pull requests across 18 repos, 98% in three, from 2026-10-17 to 11-16: the orchestration system that runs the agent lanes (488), Atlanta, a live city simulation (389), and Alex Net, a game (313). The 3D work runs in Alex Net, from concept art, and in Atlanta, from map data. The source repos are private; this repo carries aggregates, the experiment records and the judge check ([how each number was counted](METHOD.md)).

## The harness

This section is Alex Net's harness (experiment issue #727). The task: take owner-approved concept art of a droid (front, profile and back) and build a 3D model in Unreal Engine that matches it, over hours of agent work, with no person watching the rounds.

- **Art in two versions.** Every view comes as a high-contrast shape and form version and as a textured colour version.
- **Two phases.** Shape first, judged only against the high-contrast art; then texture, against the colour art, starting from the shape result.
- **Judges that score and fix.** Each phase has an Opus pass and then a Fable pass (both at high effort), and each pass has three rounds, one per view. In every round a fresh judge session that has not seen earlier rulings reviews the render from its view, then the same session fixes what it found. 2 phases x 2 passes x 3 views = 12 rounds per body.
- **A separate scorer.** After every round a fresh Opus medium session scores each body part 0 to 100 at all three views (40 points shape and proportion, 30 detail, 30 material and colour). These scores are **judge only, not validated**.
- **My labels, made apart from the judges.** I compare blinded pairs of builds against the approved art on a labelling page that never shows a judge score, a model name, a round or a cost. Item ids are random and the mapping is sealed away from the page. The rule for trusting the judge (85% agreement with me, 95% Wilson lower bound at least 75%) was posted before any label. Blinded answers so far: 0.

![Old build, new female, new male, then the approved female and male art, at front, profile and back](figures/droid_old_new_art.png)

*Columns: old pipeline build (one unsexed body, built to an earlier concept sheet), new female final, new male final, approved female art, approved male art. The three builds are Unreal Engine 5.8.4 renders of the built meshes on one camera, light and background; the art columns are the 2D concept art. These frames are for showing the work; the scores were taken on each pipeline's own renders, which differed ([confound 6](METHOD.md#confounds)).*

**The second 3D codebase, Atlanta,** builds a real city from map data (OpenStreetMap outlines, LiDAR heights and published dimensions), not from concept art. Its judges do not score and are not blind: they see the pull request and the builder's report, and rule MERGE or HOLD from renders at three camera altitudes. There are no owner labels there. Its 3D work so far includes 8 baked cars at three detail tiers (PRs #1337, #1353, #1382 and #1396; 102.23 USD and 15.73 agent hours; #1382 and #1396 went Opus HOLD, then Fable MERGE), the Mercedes-Benz Stadium and the GWCC halls (#1470, 33.65 USD), an authored outer ring of about 142 km2 (#1443) and 5 landmark towers. The experiments and the proposal below are about Alex Net.

## Why loops fail for 3D

My first pipeline was a loop. It built the droid part by part and kept running rounds on each part, scored by a model judge, until a hold froze it. Its records on the standard chassis: 74 rounds (70 on single parts), 97.1 agent hours and 747.82 USD, and it froze before the feet and hands had any rounds and before its side and back driver ran a round. Across all six chassis it spent 4,004.72 USD, 448 rounds and 519.5 agent hours, 62 to 93 rounds per chassis. The fixed schedule above used 12 rounds per body. The units differ: an old round worked on one part, a new round covers the whole body from one view. The old hours also include waits on account limits.

Two more things in the records point the same way:

- **A loop that stops on a score can be steered by the score.** Across the 33 new-method rounds that have both scores, the builder's own score ran more than 5 points above a fresh scorer's in 9, and in two cited rounds the builder's score rose while the fresh score stayed flat or fell (judge only, not validated). A loop that runs until its score stops rising is run by exactly the number a builder can fit.
- **Review loops burn the same way.** Before I capped pull request review at two rounds, one PR went 11 rounds and about 6.0B cache-read tokens in 36 hours for 12 merges ([case 07](incidents/07-eleven-review-rounds-36-hour-burn.md)).

This is my belief plus one comparison, and the comparison changed several things at once ([confound list](METHOD.md#confounds)). It does not isolate the loop as the cause.

## Experiments

I had four theories about why the first pipeline was slow. The one finished comparison, the standard chassis, changed several things together: judge and builder in one session, the shape and texture split with high-contrast art, a whole-body three-view schedule, Opus then Fable passes, and a fresh scorer. So its result belongs to that whole bundle, not to any one theory. On the other chassis, lean has finished its shape phase, angular has started, and the last three have not started.

**Result of the bundle, standard chassis** (one old build against a new female and male body; details in [METHOD.md](METHOD.md#5-lead-case-3d-builds-with-no-person-watching)):

| Measure | Old pipeline | New method |
|---|---|---|
| Agent hours per body, build sessions | 97.1 | 8.3 (female), 10.0 (male) |
| Build cost per body, list price | 747.82 USD (includes its own scoring) | 182.00 and 160.67 USD, plus about 24 USD of scoring each |
| Rounds per body (not the same unit: old rounds were per part, new rounds whole body from one view) | 74 | 12 |
| Part regions against the approved texture art, 0 to 100 | 46.6 | 70.6 and 69.8 (judge only, not validated) |
| Parts against the old pipeline's own per-part references, 0 to 100 | 54.9 | 59.9 and 60.9 (judge only, not validated) |

The hours and costs come from session transcripts at list price and do not depend on the judge; the old hours include waits on account limits. The scores do, and the new method also had better reference art and more model effort.

### 1. Split shape from texture, with high-contrast and colour art

- **Theory:** a builder fixes form faster when it first matches a high-contrast shape version of the art, and only then matches colour and material.
- **What was changed:** the shape phase is judged only against the high-contrast art; the texture phase starts from its result and is judged against the colour art.
- **Result:** the bundle result above. No run changed the split alone, so the split's own effect is not measured. Whether darker chassis needed more rounds has not been tested; a check on the build records is due 2026-11-17.

### 2. One body part at a time, to run in parallel

- **Theory:** building one body part at a time lets parts be built in parallel threads, so a body finishes sooner.
- **What was changed:** the old pipeline built part by part (70 of its 74 rounds were on single parts). No serial run of the same work exists to compare against, and the new whole-body method used 12 rounds per body against 74, which points the other way.
- Result: being compiled from the build records, due 2026-11-17.

### 3. More angles: front, profile left, profile right, back

- **Theory:** a build judged from one angle fits that angle and stays flat in the others; judging from several angles gives a body that reads right all the way round.
- **What was changed:** each pass now rounds through front, profile and back, one view per round, and the scorer scores all three. The finished runs used three views, not four. This change is part of the same bundle as theory 1, so the two cannot be separated in it.
- Result: being compiled from the build records, due 2026-11-17.

### 4. Higher-resolution concept art

- **Theory:** more detailed reference art gives the builder and the judge more to match against, so fewer rounds miss details.
- **What was changed:** no build record I can cite yet says which builds used higher-resolution art.
- Result: being compiled from the build records, due 2026-11-17.

## The proposal: a trained model for judging 3D work

Today every round's quality check is a frontier-model judge, and nobody has checked it against a person. The records this harness keeps are what a trained model needs: renders at three views and per-part scores with written reasons and tags for every new round, the cost of every round old and new (448 old rounds), the builder's own scores, and, once labelling starts, my blinded picks on about 150 pairs plus repeats. With Anthropic's help I want to train a model (weights) from my labels and the judge records, and find out what it can and cannot do. Each claim below has a test, and every test uses only held-out, blinded labels I made directly, split by chassis and sex.

1. **A learned judge for 3D fidelity.** A reward model that predicts which of two builds I would pick against the approved art.
   - *Test:* agreement with my held-out blinded picks under the rule already posted (85%, Wilson lower bound 75%), on the same pairs as the Opus judge.
   - *If it fails:* it is not used, and the Opus judge stays judge only, not validated.
2. **Catching builders that fit the judge.** A detector that flags rounds where the score rises but the build does not get better: the builder's score against a fresh scorer, the judged view against the two views it was not judged on, and the learned judge against the model judge.
   - *Test:* on held-out rounds, do flagged rounds match the rounds I rate no better than the round before? A red-team set, with builders told to raise the score without matching the art, measures how many it catches.
3. **Fewer rounds and lower cost.** A stop rule from the learned judge in place of a fixed 12 rounds or a loop, and a cheaper check than a frontier scorer round (about 2 USD each today).
   - *Test:* replay the recorded runs and stop where the learned judge says further rounds will not change my pick; report rounds and USD saved, and how often I prefer the build it gave up on.
4. **What it teaches about overseeing long agent work.** How many labels from one person it takes before a learned check can stand in for that person on work nobody watched, and where it breaks.
   - *Test:* a learning curve over label count, scored on a chassis held out of training. Atlanta would be a harder transfer test, but it has no owner labels today, so it would need its own blinded labels first.

What I start with: 0 blinded labels, one labeller, and no trained model of mine that has beaten its baseline (a small MLP lost to logistic regression, 0.523 against 0.681; [METHOD](METHOD.md#6-fleet-detail)). The order is fixed by that: close the blinded check first, with a second rater on at least 50 pairs, then train.

## Mentorship I am seeking

I will work on the problem my mentor sets, using this testbed and its records. Where my results say I need help, by the posting's research areas:

- **Scalable Oversight** ("techniques to keep highly capable models helpful and honest, even as they surpass human-level intelligence in various domains"). A judge of the same model and effort predicted my past picks 8 of 24 times where chance is 6 ([judge check](METHOD.md#judge-check-results)). *Help with:* when a model judge, or a learned one, can stand in for a person; how to size and blind the pair set; how to get from "agrees with the owner" to "agrees with people".
- **Adversarial Robustness and AI Control** ("methods to ensure advanced AI systems remain safe and harmless in unfamiliar or adversarial scenarios"). Builders ran more than 5 points ahead of a fresh scorer in 9 of 33 new-method rounds (judge only, not validated). *Help with:* testing for gaming when the judge's score is the reward, and red-teaming a learned judge before trusting it.
- **ML systems and reinforcement learning** ("improving how frontier models are trained and building the infrastructure behind that research, from model architecture, optimizers, and training data to accelerator simulators, hardware backends, and RL environment pipelines"). The build loop is an RL environment with a judge for its reward. *Help with:* training a reward model from about 150 blinded pairwise labels plus repeats, and running the build loop as an RL environment pipeline.
- **Experimental design, under all three.** The finished comparison changed five things at once. *Help with:* designing the remaining chassis runs so each theory's effect can be attributed.

## Limits

- Every 3D score is judge only, not validated: one Opus medium scorer per round, not yet checked against me. Blinded owner answers: 0. In some rounds the scorers saw the builder's own score or earlier scores, so treat the scores as upper bounds.
- One finished chassis, two new bodies, one old build, no repeat runs. Old and new builds can be told apart on sight, so old against new is not blind to method ([confound list](METHOD.md#confounds)).
- None of the four theories has been tested alone. Theories 1 and 3 are confounded in the one finished comparison.
- The proposal is untested. Nothing I have trained so far has beaten its baseline.
- Owner feedback recovered from chat (231 rows) is model-tagged and unconfirmed, and no row is joined to a build.
- Fleet-wide alignment shares come from one model's labels, checked only by the same model. The full list is under [known gaps](METHOD.md#known-gaps).

## More detail

- [`METHOD.md`](METHOD.md): how every number was computed, the full results table, the judge check tables and decision rule, the confound list, the fleet setup and measures, the failure cases and the known gaps.
- [Failure cases](METHOD.md#failure-cases): eight dated cases where agents cheated, hallucinated or cut corners in the fleet, with the files in [`incidents/`](incidents/).
- [`scripts/wilson.py`](scripts/wilson.py): the Wilson interval and backtest scoring behind the judge check table; `python3 scripts/wilson.py`, no dependencies.
- `data/` and `figures/`: weekly fleet aggregates and figures, each with its source and window.
- An earlier 2-minute video tells the earlier version of this story, and one cost figure in it predates the cost correction: https://youtu.be/vTkcXYL4Rr4

## How this was written

The story and the theories are mine. Claude drafted the wording and assembled this repo, and the agent fleet described here gathered the figures and ran the experiment.

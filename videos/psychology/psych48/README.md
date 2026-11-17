# Psychology, Built: Part 48, Modelling Behaviour

In the 1950s William Estes pointed out that a smooth, gradual learning curve can be the average of learners who each
learned in a single jump. The average describes no one. Every earlier part of the series fitted a model to
behaviour; this part opens the fitting harness and asks when a computational model of the mind is more than a curve
fit.

The viewer sees Part 17's bandit fitted again and predicts four numbers: how well a learning rate is recovered from
200 choices, how often model comparison finds a perseverating learner, what curve fits the average of exponential
learners, and how much fitting people as a population cuts the error in each learning rate. Then what a cognitive
model is (a program from parameters to trial-level data) and four models of one bandit task; maximum likelihood with
restarts, and the traps in the search; parameter recovery; the ridge along which learning rate and inverse
temperature trade off; model comparison by likelihood ratio, AIC, BIC and cross-validation, and model recovery with
its confusion matrix; Roberts and Pashler's question of how persuasive a good fit is, and a posterior predictive
check that catches a model missing perseveration; people as a population, with empirical-Bayes shrinkage of learning
rates; the power law of practice as an artefact of averaging; rational and resource-rational analysis;
connectionism; and language models given the Battery.

## Where the numbers come from

| What | Source |
|---|---|
| Estes's curves: 200 simulated learners, each at 10% correct until a jump (probability 0.12 per trial) and 95% after; the average rises smoothly, 19% on trial 1 and 50% by trial 5, matching 0.1 + 0.85(1 - 0.88^t) | Psyche (`fit.jump_learners`), item `jump` |
| Practice: 60 simulated people whose response times fall exponentially at their own rates (log rate SD 2.0); an exponential fits 95% of them better than a power function; for the average, the power function wins (residual sum of squares 19,113 against 29,178) | Psyche (`fit.practice_curves`), item `practice` |
| One simulated learner (a Q-learner with α = 0.3, β = 5, 200 trials, the arms swapping at trial 100) fitted by four models: BIC 281.6 (random), 235.3 (win-stay lose-shift), 135.4 (Q-learning, α̂ = 0.42, β̂ = 4.9) and 139.7 (with perseveration) | Psyche (`fit.simulate`, `fit.fit`), item `example` |
| Parameter recovery: 75 simulated learners over 5 learning rates × 5 inverse temperatures, 200 trials each; correlation of true and recovered 0.92 for α and 0.90 for β | Psyche (`fit.recovery`), item `recovery` |
| The likelihood surface over a 40 × 40 grid of (α, β) for the example learner | Psyche (`fit.tradeoff_surface`), item `surface` |
| Model recovery: 25 data sets from each of four models, the model chosen by BIC; right 92%, 100%, 100% and 92% of the time; perseveration taken for plain Q-learning 8% of the time | Psyche (`fit.model_confusion`), item `confusion` |
| A posterior predictive check: 30 learners who perseverate; stay after a win 0.97 and after a loss 0.85; plain Q-learning fitted and simulated predicts 0.96 and 0.70; the model with perseveration 0.97 and 0.84 | Psyche (`fit.posterior_predictive`, `fit.stay_after`), item `ppc` |
| People as a population: 30 learners, 60 trials each, logit learning rates drawn around logit 0.3 (SD 0.6), β = 5 known; individual estimates miss by 0.69 (RMSE, logit scale), empirical-Bayes estimates by 0.36; population mean -0.70, SD 0.52 | Psyche (`fit.group_fit`), item `group` |
| Signatures before fitting: 40 simulated players per model; stay after a win 0.51, 0.95, 0.89, 0.98 and after a loss 0.50, 0.05, 0.62, 0.87 (random, win-stay lose-shift, Q-learning, Q with perseveration) | Psyche (`fit.simulate`, `fit.stay_after`), item `signatures` |
| Two optima: a learner with alpha 0.05, beta 15, kappa 0.5 over 80 trials, the three-parameter model fitted from 40 random starts; 70% reach the best fit (alpha 0.05, beta 18, kappa 0.36), 30% stop 3.1 log-likelihood units short (alpha 0.27, beta 5.2, kappa 0.74) | Psyche (`fit.loglik`, L-BFGS-B), item `starts` |
| Recovery by trials: 72 learners at each of 50, 100, 200, 400 trials; correlation of true and fitted alpha 0.63, 0.77, 0.90, 0.95 and beta 0.58, 0.87, 0.90, 0.93 | Psyche (`fit.recovery`), item `trials` |
| The ridge in repeated fits: one learner (0.3, 5) simulated 40 times; fitted alpha and beta correlate -0.52 | Psyche (`fit.fit`), item `tradeoff` |
| Held-out prediction: 30 perseverating learners, two sessions each; log-likelihood per choice on the second session -0.71, -0.63, -0.27, -0.21 for the four models fitted on the first; BIC chose the true model for 93% | Psyche (`fit.fit`, `fit.loglik`), item `crossval` |
| What each model can produce: stay after a win and after a loss for 60 random parameter settings of win-stay lose-shift, Q-learning and Q with perseveration | Psyche (`fit.simulate`), item `flex` |
| Pooling by trials: 40 people, four groups at each length; logit learning-rate error alone 1.00, 0.57, 0.35, 0.27 and pooled 0.50, 0.41, 0.31, 0.25 at 30, 60, 120, 240 trials | Psyche (`fit.group_fit`), item `shrinktrials` |
| How long to think: accuracy Phi(0.3 sqrt k) after k samples; the best k for a cost per sample of 0.002, 0.005, 0.01, 0.02 is 36, 21, 12, 5 | arithmetic, item `samples` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

The four models are the random chooser (one bias), win-stay lose-shift (one error rate), the Q-learner of Part 17
(α, β) and the Q-learner with a perseveration bonus (α, β, κ); every fit starts from up to three points within bounds and keeps the best.

## Built in this part

* `explainer/psychology/psyche/fit.py`: jumping learners and their average; exponential learners and the power law
  of their average; four generative models of a reversal bandit with their likelihoods; maximum likelihood with
  restarts, AIC and BIC; parameter recovery; the likelihood surface; model recovery (the confusion matrix and its
  inversion); empirical-Bayes shrinkage of learning rates; stay-after-win and stay-after-loss, and a posterior
  predictive check. Tested in `tests/psychology/test_fit.py`.
* The Ledger gains two rows.
* The course's interactive: the reader plays a reversal bandit, and the page fits a Q-learner to their choices and
  shows how far a learning rate from that few choices can be trusted.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Response time falls with practice as a power function of the number of trials, for each learner. | Newell and Rosenbloom 1981 | failed |
| Parameters of fitted cognitive models, such as a learning rate, are stable traits of a person that generalize across tasks and can serve as clinical markers. | Montague, Dolan, Friston and Dayan 2012 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Wilson and Collins; Roberts and
Pashler; Anderson; Lieder and Griffiths; Rumelhart, McClelland and the PDP Group; Binz and Schulz.

## Build it

```bash
python -m videos.psychology.psych48.compute            # every number (several minutes)
python tools/qa_scene.py psych48 Recovery              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych48 -q l   # the whole part, silent preview
python tools/build.py psych48                          # 1080p30 with narration
python tools/qa_scene.py psych48 Compare --lang zh     # the Chinese edition of one chapter
python tools/make.py psych48                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 48                    # the lab: simulate, fit, recover, compare
python tools/check_ledger.py psych48                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's fit module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A curve no animal had | Estes's jumping learners; every part has fitted models; the question; objectives |
| 1 | On you: your learning rate, and four numbers | Four predictions |
| 2 | What a cognitive model is | A program that makes behaviour; four models of one task; simulate before you fit |
| 3 | Fitting | Maximum likelihood and a scorecard; traps in the search; two answers from one learner |
| 4 | Parameter recovery | Simulate, fit, compare; how many trials? |
| 5 | Parameters that trade off | The likelihood surface and its ridge; the ridge in repeated fits |
| 6 | Model comparison | Four ways to compare; model recovery; predict the next session |
| 7 | A good fit can be bad | Roberts and Pashler; what each model can produce; does the model make the effect? |
| 8 | People as a population | Hierarchical fitting and shrinkage; when pooling pays |
| 9 | A law that was an average | The power law of practice |
| 10 | Rational and resource-rational | Anderson's rational analysis; optimal use of limited computation; how long to think |
| 11 | Connectionism | Parallel distributed processing: what it added and what it cost |
| 12 | Language models as models of minds | Giving a model the Battery; prediction against explanation |
| 13 | The Ledger | Two rows; what they have in common |
| 14 | In practice: phenotypes, users and tutors | Where fitted models run |
| 15 | Frontier: amortized inference and discovered models | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; Kant's three objections; payoffs; problems; references; Part 49 |

## Sources

* W. K. Estes, The problem of inference from curves based on group data, *Psychological Bulletin* 53 (1956)
  134-140.
* R. C. Wilson and A. G. E. Collins, Ten simple rules for the computational modeling of behavioral data, *eLife* 8
  (2019) e49547.
* S. Roberts and H. Pashler, How persuasive is a good fit? A comment on theory testing, *Psychological Review* 107
  (2000) 358-367.
* A. Newell and P. S. Rosenbloom (1981); A. Heathcote, S. Brown and D. J. K. Mewhort (2000).
* P. R. Montague, R. J. Dolan, K. J. Friston and P. Dayan (2012); M. K. Eckstein et al. (2022); A. Mkrtchian,
  V. Valton and J. P. Roiser (2023).
* J. R. Anderson, *The Adaptive Character of Thought* (Erlbaum, 1990); F. Lieder and T. L. Griffiths,
  Resource-rational analysis, *Behavioral and Brain Sciences* 43 (2020) e1.
* D. E. Rumelhart, J. L. McClelland and the PDP Research Group, *Parallel Distributed Processing* (MIT Press, 1986).
* M. Binz and E. Schulz, Using cognitive psychology to understand GPT-3, *Proceedings of the National Academy of
  Sciences* 120 (2023) e2218523120.
* G. Schwarz, Estimating the dimension of a model, *Annals of Statistics* 6 (1978) 461-464; K. E. Stephan et al.,
  Bayesian model selection for group studies, *NeuroImage* 46 (2009) 1004-1017.

## Problems and solutions

1. **Softmax.** A softmax chooser with $\beta = 5$ values two arms at 0.6 and 0.4. Find the probability of choosing the first.

   *Solution.* 1/(1 + e^(-5 × 0.2)) = 1/(1 + e^(-1)) = 0.73.
2. **A Q-learning update.** A Q-learner with $\alpha = 0.3$ values an arm at 0.5, chooses it, and is rewarded. Find the new value.

   *Solution.* 0.5 + 0.3 × (1 - 0.5) = 0.65.
3. **A log-likelihood.** A model gave a person's three choices probabilities 0.7, 0.6 and 0.8. Find the log-likelihood.

   *Solution.* ln 0.7 + ln 0.6 + ln 0.8 = -0.357 - 0.511 - 0.223 = -1.09.
4. **BIC.** Two models of 200 choices: log-likelihood $-60$ with 2 parameters, $-58$ with 3. Which does BIC prefer?

   *Solution.* With n = 200, ln n = 5.30: 120 + 2 × 5.30 = 130.6 against 116 + 3 × 5.30 = 131.9; BIC prefers the
   two-parameter model, by a hair.
5. **Jumping learners.** Learners jump from 10% to 90% correct with probability 0.1 per trial. What does the average curve show on trial 10?

   *Solution.* If a learner can jump after each of the first nine trials, 1 - 0.9⁹ = 0.61 have jumped by
   trial 10, so the average is 0.1 + 0.8 × 0.61 = 0.59: a value no learner shows, since each is at 0.1 or 0.9.
6. **Shrinkage.** A person's log-odds learning rate is $-1.5$ with variance 0.5; the population's mean is $-0.7$ with variance 0.25. Find the hierarchical estimate.

   *Solution.* Weight the two by their precisions, 2 and 4: (2 × (-1.5) + 4 × (-0.7))/6 = -0.97.
7. ★ **A plan.** Plan the checks for a new model of a new task: simulations, recovery, model recovery, a posterior predictive check, and the number of trials.

   *Solution.* Simulate the model across its plausible parameters and check it produces the effects it is meant to;
   fit simulated data and show recovery for the number of trials you will collect; simulate from every candidate model
   and show the confusion matrix; after fitting, simulate from the winner and compare its stay-after-win and
   stay-after-loss (or the task's key effect) with the data; fix the trial count by recovery, not by habit.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Estes (1956) and the year and form of his argument; Wilson and Collins (2019) and their ten rules; Roberts and Pashler
(2000); Newell and Rosenbloom (1981); Heathcote, Brown and Mewhort (2000); Montague et al. (2012); Eckstein et al.
(2022); Mkrtchian, Valton and Roiser (2023); Anderson (1990); Lieder and Griffiths (2020); the PDP volumes (1986);
Binz and Schulz (2023); the fine-tuned "foundation models of cognition" mentioned in the frontier chapter; Schwarz
(1978); Stephan et al. (2009); and every page range in Sources.

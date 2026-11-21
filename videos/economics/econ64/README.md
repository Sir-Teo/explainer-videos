# Economics, Built: Part 64, Machines that Learn

Part 64 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act XII, *The Frontier*. It asks what machine learning changes in how
economics is done. Its answer: it makes prediction cheap, and so separates the questions that need only a forecast
from those that need a cause. For the first it can beat experts, if the outcomes a decision hid are handled by design;
for the second it helps only inside a design (double machine learning, causal forests, corrected measurements). It can
solve models, act in markets and propose hypotheses; it cannot say what would have happened, or which errors matter
more.

It opens at the judge's desk: Kleinberg, Lakkaraju, Leskovec, Ludwig and Mullainathan trained boosted trees on 758,027
New York City bail decisions (2008-13) and estimated that releasing in the algorithm's order could cut crime by up to
a quarter with the same number jailed, or jail up to two fifths fewer with no more crime; the hard part is that
outcomes are seen only for the released. The Island's bail court shows the same in miniature. From there it covers:

- prediction policy problems (the umbrella and the rain dance; Kleinberg, Ludwig, Mullainathan and Obermeyer;
  Mullainathan and Spiess); the Island's 40,000 defendants, fifty judges and a random forest trained on the released;
  *Called it?*: Meehl's clinical against statistical prediction (right; Grove et al.'s 136 studies);
- Play it: ten defendants and three cells (the algorithm detains the young with missed court dates, preventing 1.98
  failures on average; the judge detained the three violent charges, 1.02; the best possible, 1.98);
- selective labels: on the test half, ranking by the forest gives 18% fewer failures at the judges' detention rate,
  or 30% fewer detained at their failure rate (with outcomes only the simulation knows); the contraction design
  recovers a 15-16% gain from observed outcomes alone; filling in the detained's outcomes with predictions says 6.3
  failures per hundred against a truth of 6.9, because judges saw a courtroom signal the records lack;
- prediction is not causation: a job programme whose effect peaks in the middle of the risk range; per 100 places,
  6.6 kept out of unemployment by risk, 13.7 at random, 24.8 by a causal forest's estimated effect, 31.3 at best;
  Obermeyer et al.'s algorithm that predicted costs rather than needs (17.7% to 46.5%);
- double machine learning (Chernozhukov et al.; Robinson): fifty samples of 1,500 with nonlinear confounding; no
  controls 1.53, linear controls 1.48, a plug-in learner 1.17, cross-fitted double ML 1.01 against a truth of 1, its
  90% intervals covering 86% of the time;
- heterogeneous effects and policy learning: a causal forest on a trial of 4,000 (Wager and Athey; Athey and Wager;
  Kitagawa and Tetenov);
- text and images as data (Gentzkow, Kelly and Taddy; Jean et al.'s satellites); a classifier's estimate of the share
  of layoff news is 14.3% against 12%, and prediction-powered inference (Angelopoulos et al.) is unbiased and a third
  narrower than 400 hand labels;
- an intermission: transistors on the largest microprocessor, 1971-2021, doubling about every two years;
- deep learning as a solution method: a network trained on Euler errors learns Brock and Mirman's saving rate alpha
  beta to within 0.0001; deep equilibrium nets;
- learning agents: Part 44's Q-learners settle 78% of the way from competition to monopoly (Calvano et al.); the AI
  Economist;
- language models as subjects (Horton's homo silicus) and as research assistants (Ludwig and Mullainathan's mugshots;
  validation by prediction-powered inference);
- fairness: ProPublica's 45% and 23%, the vendor's calibration reply; on the Island, a perfectly calibrated score
  wrongly detains 22% of group A and 48% of group B; Chouldechova's identity and Kleinberg, Mullainathan and
  Raghavan's impossibility;
- the Dial (what an algorithm adds to a judge's decision, new), the jobs that use these methods, and the frontier: the
  algorithm's advantage falls from 24% to minus 52% as the judge's private signal grows; foundation models for
  economic data and automated structural estimation.

## Build it

```bash
python -m videos.economics.econ64.compute              # every number (about five minutes), into .cache/econ64/
python tools/qa_scene.py econ64 Labels                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ64 -q l   # the whole part, silent preview
python tools/build.py econ64                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 64                     # the lab
```

The data are Rupp's microprocessor trend data via Our World in Data, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is computed on the Island, or stated
from the papers listed in `dials.SHOWN[64]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The judge's desk | Kleinberg et al.'s bail study; the Island's court and its hidden outcomes; the question; objectives |
| 1 | Prediction policy problems | Umbrellas and rain dances; the Island's forest; *Called it?*: Meehl |
| 2 | Play it: ten cases | Detain three of ten; the algorithm against the judge |
| 3 | Selective labels | The policy frontier; the contraction design; why filling in flatters |
| 4 | Prediction is not causation | Targeting by risk against by effect; costs are not needs |
| 5 | Double machine learning | Four estimators by Monte Carlo; orthogonality and cross-fitting |
| 6 | Heterogeneous effects and policy learning | A causal forest; allocation curves |
| 7 | Text and images as data | From documents to measures; prediction-powered inference |
| — | Intermission | Transistors per microprocessor since 1971, as a line and a tune |
| 8 | Deep learning as a solution method | A network learns Brock and Mirman's rule; why it scales |
| 9 | Learning agents | Q-learning price setters; the AI Economist |
| 10 | Language models as subjects | Homo silicus; what it cannot replace |
| 11 | Language models as research assistants | Mugshots and hypotheses; the workflow and its rule |
| 12 | Fairness | COMPAS; the Island's calibrated score; Chouldechova's identity |
| 13 | The Dials | What an algorithm adds to a judge (new) |
| 14 | In practice | Credit, targeting, public services; three cautions |
| 15 | Frontier | When to defer; foundation models; automated estimation |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 65, *The Economics of AI* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `learn` module (`explainer.economics.agora.learn`), over
statkit's forests, boosting, causal forest and PPI and the series' automatic differentiation; the narration states the
cached numbers.

- **The courts.** 40,000 defendants: age 18-60, prior arrests Poisson with a mean falling with age, past missed dates
  binomial on priors, four charges, a job; a courtroom signal s ~ N(0, 1); the chance of failing to appear is logistic
  in log(1 + priors), missed dates, youth and its interaction with priors, a job, the charge (drugs up, violence
  down) and 0.45 s. Fifty judges with release rates 55-88%, cases assigned at random; each ranks by priors, missed
  dates, the charge (overweighted), a job, 0.45 s and noise of s.d. 0.7. A random forest (80 trees, leaves of 40) is
  trained on the released half of the training half and scores the test half.
- **Contraction.** The most lenient fifth of judges' test cases; the forest detains more of their released until each
  stricter fifth's detention rate; failures counted only among the observed.
- **Targeting.** 20,000 unemployed with five characteristics; the chance of staying unemployed logistic in three of
  them; the programme's effect 0.3 exp(-((p0 - 0.5)/0.25)^2) (1 + 0.4 tanh x4); a trial of 4,000 with a causal
  forest (100 honest trees).
- **Double ML.** n = 1,500, five covariates, m and g with tanh, sine, an interaction and thresholds; gradient boosting
  (250 trees of depth 3) for the nuisances; three folds; fifty samples.
- **Text.** 20,000 articles, 12% about layoffs; a classifier with sensitivity 0.90 and specificity 0.96; 400 hand
  labels; 500 corpora.
- **The Euler net.** alpha = 0.33, beta = 0.95; one hidden layer of 12 tanh units, a sigmoid output; 64 capital stocks
  from 0.2 to 2.5 times the steady state; Adam, 3,000 steps.
- **Agents.** Part 44's logit Bertrand game, 15 prices, exploration decaying at 2e-5 a period, eight sessions.
- **Fairness.** Two groups of 200,000 with normal risk indices centred 0.7 apart; the score is the true risk;
  detention above 0.3.
- **The sweep.** The courts with the signal's weight in both risk and the judges' index from 0 to 1.8.
- **The intermission.** Rupp's transistor counts, 1971-2021; the doubling time by least squares on log2.

## Problems and solutions

**1.** *Prediction policy: a programme helps only people who would otherwise fail, by a fixed amount; show that
ranking by the chance of failing is then optimal, and give an example where it is not.*

*Solution.* If the benefit to person i is b times the chance p_i that they would fail without the programme, the
total benefit of treating a set S is b times the sum of p_i over S, which a fixed number of places maximizes by taking
the largest p_i. Ranking by risk is optimal. It fails whenever the benefit is not proportional to risk: in this part's
job programme the effect is small for those who would find work anyway and for those far from any job, so the highest
risks gain least, and ranking by risk does worse than at random for small programmes.

**2.** *Selective labels: if judges detain on a signal s that raises risk and the model omits it, show that filling in
the detained's outcomes with the model's prediction understates their failures.*

*Solution.* The model estimates E[y | x] from the released, among whom s is lower than average for each x, because
judges release those with low s: E[y | x, released] < E[y | x]. Among the detained s is higher than average, so their
true rate E[y | x, detained] exceeds E[y | x], which exceeds what the model learned. Filling in with the model's
prediction therefore understates the detained's failures, and any policy that would release some of them looks better
than it is.

**3.** *Double ML: in y = theta d + g(X) + e, d = m(X) + v, show that the residual-on-residual estimator's error
depends on (m-hat - m)(l-hat - l) to first order, where l(X) = E[y | X].*

*Solution.* Write y - l(X) = theta v + e and d - m(X) = v. With estimates, y - l-hat = theta v + e + (l - l-hat) and
d - m-hat = v + (m - m-hat). The estimator's numerator is the sum of (v + dm)(theta v + e + dl), with dm = m - m-hat
and dl = l - l-hat; its denominator the sum of (v + dm)^2. Expanding, the terms linear in dm or dl are multiplied by v
or e, which have mean zero given X and (with cross-fitting) are independent of the errors, so they vanish in
expectation and average out at rate 1/sqrt(n); what remains is the sum of dm dl, the product of the two errors, plus
theta times the sum of dm^2 in the denominator's correction, both second order. So errors of order n^(-1/4) in each
learner are enough.

**4.** *Prediction-powered inference: show that f-bar_N + mean(y - f)_n is unbiased for the mean of y, and find its
variance.*

*Solution.* With the n labelled items a random sample, E[mean(y - f)_n] = E[y] - E[f], and E[f-bar_N] = E[f], so the
sum has expectation E[y]. Its variance is Var(f)/N + Var(y - f)/n (the two samples are independent when the labelled
items are excluded from the N). When the classifier is good, Var(y - f) is much smaller than Var(y), so the estimator
beats the hand labels' Var(y)/n; when it is poor, it can do worse, which PPI++'s tuned weight on f avoids.

**5.** *Brock and Mirman: with log utility and full depreciation, guess k' = s k^alpha and verify that s = alpha beta
solves the Euler equation.*

*Solution.* With c = (1 - s) k^alpha and k' = s k^alpha, next period c' = (1 - s) k'^alpha. The Euler equation
1/c = beta alpha k'^(alpha - 1)/c' becomes 1/((1 - s) k^alpha) = beta alpha k'^(alpha - 1)/((1 - s) k'^alpha) =
beta alpha/((1 - s) k'), so k' = beta alpha k^alpha, that is s = alpha beta, whatever k.

**6.** *Chouldechova: derive FPR = p/(1 - p) (1 - PPV)/PPV (1 - FNR), and show that equal PPV and unequal base rates
force unequal error rates.*

*Solution.* Let N be the group's size, p its base rate. True positives are TP = (1 - FNR) p N; false positives
FP = FPR (1 - p) N. PPV = TP/(TP + FP), so FP = TP (1 - PPV)/PPV. Substituting, FPR (1 - p) N = (1 - FNR) p N
(1 - PPV)/PPV, which is the identity. If two groups have the same PPV and the same FNR but different p, the factor
p/(1 - p) differs, so their FPRs differ; to equalize the FPRs, the FNRs or the PPVs must differ instead.

## Lab and interactive

- `python -m videos.economics.labs 64`: the courts and their frontier; contraction and the naive evaluation; targeting
  by risk and by effect; double ML against OLS; PPI; the Euler network; pricing agents; fairness by group; the signal
  sweep; Moore's law on the Data Room's data.
- The interactive (course site): bail. The reader sets how much the judges see that the records do not, how much they
  overweight the charge, and how strict they are, and compares their failures with the algorithm's along the whole
  frontier.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[64]`; the new Dial (what an algorithm
adds to a judge's decision) is in `explainer/economics/dials.py`, and the *Called it?* record of Meehl's clinical
against statistical prediction in `explainer/economics/calls.py`. The methods are stated from the works cited in the
chapters (Meehl 1954, Brock and Mirman 1972, Robinson 1988, Grove et al. 2000, Kleinberg, Ludwig, Mullainathan and
Obermeyer 2015, Jean et al. 2016, Angwin et al. 2016, Lakkaraju et al. 2017, Mullainathan and Spiess 2017,
Chouldechova 2017, Kleinberg, Mullainathan and Raghavan 2017, Kleinberg et al. 2018, Chernozhukov et al. 2018, Wager
and Athey 2018, Kitagawa and Tetenov 2018, Gentzkow, Kelly and Taddy 2019, Obermeyer et al. 2019, Calvano et al. 2020,
Athey and Wager 2021, Maliar, Maliar and Winant 2021, Azinovic, Gaegauf and Scheidegger 2022, Fuster et al. 2022, Zheng
et al. 2022, Angelopoulos et al. 2023, Horton 2023, Ludwig and Mullainathan 2024) and computed here.

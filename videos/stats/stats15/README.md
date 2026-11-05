# Statistics, Built — Part 15: First Bayes

Part 15 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Parts 8–14 treated parameters as fixed and
data as random. This part asks what to believe about a parameter after seeing the data.

It opens with Bayes's essay of 1763 and his billiard table: a hidden ball, and twelve more balls of which 8 land
left. The posterior is Beta(9, 5), against a truth of 0.62. Then Laplace's Paris births (P(p ≤ ½) ≈ 1.15 × 10⁻⁴²) and
his sunrise.

From there the part covers:
- **The machinery.** Bayes's rule for parameters, drawn as prior × likelihood ∝ posterior. The billiard balls update
  one at a time, and sequential updating equals batch updating. The meaning of the shift, and a short history from
  inverse probability to MCMC.
- **Conjugacy.** Beta–binomial, the prior as imaginary data, gamma–Poisson on the horse kicks, and normal–normal
  precision weighting on the World's heights.
- **Summaries.** Mean, median and mode as decisions; equal-tailed vs HPD intervals; invariance; the Laplace
  approximation.
- **Prediction.** The beta-binomial predictive vs a plug-in, the law of total variance, the horse-kick predictive,
  the normal predictive (Part 11's prediction interval) and posterior predictive checks.
- **Priors.** Four priors at n = 10 and n = 100. A flat prior is not flat on the odds. Jeffreys's invariant prior,
  prior predictive checks, and the kinds of prior.
- **The normal model.** The reference prior gives Part 8's t and χ² intervals exactly.
- **Grids.** The Challenger posterior on 60,000 points: P(β₁ < 0) and the posterior of p(31 °F). A mixture prior,
  and the curse of dimension.
- **Metropolis.** Detailed balance; step sizes on trace plots; the ridge and the cure of centring; burn-in;
  agreement with the grid; functions of the draws.
- **Bayes and frequency.** Credible intervals' coverage at a fixed truth (the Board), exact calibration on average
  over the prior, and simulation-based calibration.
- **Hypotheses.** Bayes factors, a coin with 60 heads in 100, Lindley's warning at fixed p = 0.05, Sellke–Bayarri–
  Berger's bound, Laplace's births and Jeffreys's scale.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- the Paris births, the horse kicks and the Challenger flights come from the Museum;
- heights are the World's (seed 1662);
- the billiard table is a seeded simulation.

**Built in this part:**
- **`statkit.bayes` (I)** ([`explainer/stats/kit/bayes.py`](../../../explainer/stats/kit/bayes.py)), checked in
  `tests/test_stats_kit_bayes.py`:
  - conjugate updates (beta, gamma, normal, and the normal model with unknown variance);
  - equal-tailed and HPD intervals;
  - the beta-binomial predictive and the rule of succession;
  - 1-D and 2-D grid posteriors;
  - random-walk Metropolis with an effective sample size;
  - binomial Bayes factors.
- **The billiard table** (`BilliardTable` in `explainer/stats/viz.py`): Bayes's table seen from above. A hidden
  ball's line, with balls rolled to their spots.

The Coverage Board gains six rows, all 95% credible intervals, R = 10,000.

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| credible, Jeffreys prior | binomial, n = 50, p = 0.05 | 89.31% | broken |
| credible, uniform prior | binomial, n = 50, p = 0.05 | 95.96% | conservative |
| credible, Beta(18, 2) prior | binomial, n = 50, p = 0.05 | 0.00% | broken |
| credible, Beta(18, 2) prior | binomial, n = 50, p = 0.9 | 98.49% | conservative |
| credible, Beta(18, 2) prior | binomial, n = 50, p drawn from the prior | 94.55% | kept |
| credible, reference prior | the World's heights, n = 10 | 94.81% | kept |

## Build it

```bash
python -m videos.stats.stats15.compute         # once (a few minutes; cached in .cache/stats15)
python tools/build.py stats15 -q l             # fast 480p preview
python tools/build.py stats15                  # 1080p30 -> renders/stats15.mp4
python tools/qa_scene.py stats15 Metropolis
python tools/lecture_length.py stats15 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The billiard table, 1763 | 8 of 12 left: Beta(9, 5), mean 0.64, 95% [0.39, 0.86], truth 0.62; Paris 251,527 boys and 241,945 girls, P(p ≤ ½) ≈ 1.15 × 10⁻⁴²; sunrise odds 1,826,214 to 1 |
| 1 | The machinery | Beta(2, 2) × 7 of 10 → Beta(9, 5) |
| 2 | Conjugacy | posterior mean 0.643; horse kicks Gamma(123, 201), mean 0.612, 95% [0.509, 0.725]; heights N(169.3, 2.74²), data weight 92.5%, truth 169.5 |
| 3 | Summaries | Beta(3, 12): mode 0.154, median 0.186, mean 0.200; equal-tailed [0.047, 0.428], HPD [0.029, 0.395]; Laplace approximation SD 0.100 |
| 4 | Prediction | next 10 trials: SD 1.92 (predictive) vs 1.45 (plug-in); P(no horse-kick death) 0.543 either way |
| 5 | Priors | n = 10: means 0.45–0.68; n = 100: 0.64–0.70; Beta(2, 8) predicts ≥ 7 of 10 with probability 0.015 |
| 6 | The normal model | 8 adults: 95% [165.06, 175.89] = the t-interval; σ ∈ [4.28, 13.19] |
| 7 | Grids | Challenger: E[β₁] = −0.287, P(β₁ < 0) = 0.9987; p(31): median 0.9999, P(> 0.9) = 0.973; mixture prior P(0.4 < p < 0.6) = 0.65 |
| 8 | When grids fail | ESS of 5,000 draws: 12 (tiny), 212 (good), 48 (huge); raw coordinates 12; long chain ESS 510, matches the grid; OR per 10 °F median 14 |
| 9 | Bayes and frequency | the six board rows above |
| 10 | Hypotheses | 60 of 100: p = 0.057, BF₁₀ = 0.91, P(H₀ \| y) = 0.52; at fixed p ≈ 0.05: BF₁₀ = 0.91, 0.27, 0.086, 0.027 for n = 10², …, 10⁵; Sellke bound BF₀₁ ≥ 0.41; births log₁₀ BF ≈ 38 |
| 11 | Outro | — |

## Sources

- **The founders.**
  - T. Bayes, *Phil. Trans.* 53 (1763).
  - P.-S. Laplace, "Mémoire sur la probabilité des causes par les événements" (1774); *Essai philosophique sur les
    probabilités* (1814).
  - H. Jeffreys, *Theory of Probability* (1939); *Proc. R. Soc. A* 186 (1946).
- **Priors and testing.**
  - H. Raiffa & R. Schlaifer, *Applied Statistical Decision Theory* (1961).
  - D. Lindley, *Biometrika* 44 (1957).
  - G. Box, *JRSS A* 143 (1980); D. Rubin, *Ann. Stat.* 12 (1984).
  - T. Sellke, M. Bayarri & J. Berger, *Am. Stat.* 55 (2001).
  - A. Gelman, A. Jakulin, M. Pittau & Y.-S. Su, *Ann. Appl. Stat.* 2 (2008).
- **Computation and calibration.**
  - N. Metropolis, A. Rosenbluth, M. Rosenbluth, A. Teller & E. Teller, *J. Chem. Phys.* 21 (1953).
  - A. Gelfand & A. Smith, *JASA* 85 (1990); G. Roberts, A. Gelman & W. Gilks, *Ann. Appl. Prob.* 7 (1997).
  - S. Cook, A. Gelman & D. Rubin, *JCGS* 15 (2006); S. Talts et al., arXiv:1804.06788 (2018).
- **Books and history.**
  - A. Gelman et al., *Bayesian Data Analysis* (3rd ed., 2013); P. Hoff, *A First Course in Bayesian Statistical
    Methods* (2009); R. McElreath, *Statistical Rethinking* (2nd ed., 2020).
  - S. Stigler, *The History of Statistics* (1986); S. McGrayne, *The Theory That Would Not Die* (2011).

## Problems and solutions

**1. A small beta posterior.**

*Solution.* The posterior is Beta(1 + 3, 1 + 2) = Beta(4, 3), with mean 4/7 = 0.571.

P(p > ½) = 1 − I½(4, 3). For integer parameters this is a binomial sum: P(at least 4 successes in 6 fair trials)
= (15 + 6 + 1)/64 = 22/64 = 0.344. So P(p > ½) = 1 − 0.344 = 0.656.

**2. Gamma–Poisson.**

*Solution.* π(λ) ∝ λ^(α−1) e^(−βλ) and the likelihood ∝ ∏ λ^(yᵢ) e^(−λ) = λ^(Σyᵢ) e^(−nλ). Their product is
λ^(α+Σyᵢ−1) e^(−(β+n)λ), the kernel of Gamma(α + Σyᵢ, β + n).

**3. One normal observation.**

*Solution.* The precisions add, 1 + 1 = 2, so the posterior variance is ½. The posterior mean is (0 · 1 + 2 · 1)/2
= 1. The posterior is N(1, ½): halfway between prior and data, because they are equally precise.

**4. The prior as imaginary data.**

*Solution.* (a + s)/(a + b + n) = [(a + b)/(a + b + n)] · a/(a + b) + [n/(a + b + n)] · s/n. The weights,
(a + b)/(a + b + n) and n/(a + b + n), sum to 1, and the data's weight tends to 1 as n grows.

**5. The rule of succession.**

*Solution.* With a uniform prior the posterior is Beta(s + 1, n − s + 1). P(next success) is its mean,
(s + 1)/((s + 1) + (n − s + 1)) = (s + 1)/(n + 2).

**6. A Bayes factor.**

*Solution.*
- **Under H₁:** p(y | H₁) = C(10, 9) ∫p⁹(1 − p) dp = C(10, 9) B(10, 2) = 10/110.
- **Under H₀:** p(y | H₀) = C(10, 9) 2⁻¹⁰ = 10/1024.
- **The ratio:** BF₁₀ = 1024/110 = 9.31, "substantial" on Jeffreys's scale.

The two-sided p-value is 22/1024 = 0.021.

## Where it comes back

| Idea | Returns in |
|---|---|
| resampling distributions, the bootstrap | 16 |
| EM and optimization; MCMC in depth, HMC, variational inference | 21, 27 |
| hierarchical models and shrinkage | 25 |
| the Bayesian workflow, priors for testing | 26 |
| model choice, marginal likelihoods | 28 |
| decision theory, admissibility | 45 |
| Bernstein–von Mises, nonparametric Bayes | 53 |
| e-values: a betting view of evidence | 58 |
| the Coverage Board | every part; 65 |

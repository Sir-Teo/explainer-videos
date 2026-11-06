# Statistics, Built — Part 57: Distribution-Free Inference

Part 57 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the second part of Stage V, the research frontier.

It opens with Bahadur & Savage (1956), *The nonexistence of certain statistical procedures*. Over all distributions
with a finite mean, no interval of bounded length covers the mean with probability bounded away from zero. A
mixture with mean exactly 3, almost all of it N(0, 1), drives the 95% t-interval's coverage to 14% at n = 50, while
split conformal's prediction interval for a new draw from the same mixture covers 95.8%. The part asks what can be
promised with no model, and maps the boundary between the possible and the impossible:
- the hook: Bahadur–Savage for intervals and for tests, the bound against simulation, Wilks's tolerance intervals
  (1941), and why the median survives;
- exchangeability and the quantile lemma: the rank strip, the exact coverage k/(n + 1), the Beta law of coverage
  given the calibration set (Vovk 2012) and PAC thresholds, ties and smoothed p-values, split conformal;
- full conformal, split conformal and jackknife+ (Barber, Candès, Ramdas & Tibshirani 2021): full against split on
  ridge regression, the lasso's homotopy (Lei 2019), the tournament proof of 1 − 2α, stability, CV+, the cost ledger;
- impossibility: conditional coverage forces infinite expected length (Vovk 2012; Lei & Wasserman 2014), local
  conformal by bins and its counted limit, length lower bounds for the relaxation (Barber et al. 2021), no
  distribution-free interval for P(Y = 1 | X = x) (Barber 2020);
- conditional guarantees over function classes (Gibbs, Cherian & Candès 2025): the shift view, the augmented quantile
  regression, the proof, computation by LP and bisection, the dim 𝓕/(n + 1) slack, infinite penalized classes;
- beyond exchangeability: weighted conformal under covariate shift (Tibshirani, Foygel Barber, Candès & Ramdas 2019),
  estimated weights and individual treatment effects (Lei & Candès 2021), nonexchangeable conformal with fixed
  weights (Barber, Candès, Ramdas & Tibshirani 2023) and its total-variation bound, computed;
- online and adversarial coverage: adaptive conformal inference (Gibbs & Candès 2021), its two-line proof, the step
  size on a drifting series, the bound counted, DtACI;
- conformal p-values and outlier testing (Bates, Candès, Lei, Romano & Sesia 2023): PRDS, BH, the resolution limit
  1/(n + 1), on the Wisconsin biopsies;
- risk control (Angelopoulos, Bates, Fisch, Lei & Schuster 2024): the proof, learn-then-test, multilabel screening, and
  conformal factuality for language models (Mohri & Hashimoto 2024);
- Mondrian and group-conditional coverage on NHANES 2017–18: ten overlapping age, sex and race groups;
- open problems, each with what is known, and a reader's checklist.

It keeps two promises:
- **Part 34** built split conformal, CQR, Mondrian sets and ACI, and promised the theory. Chapters 1–7 prove it and
  push it to its limits.
- **Part 16**'s distribution-free tests were about medians and ranks. Chapter 0 shows why the mean was never on offer.

**Built in this part:**
- **`statkit.dfree`** ([`explainer/stats/kit/dfree.py`](../../../explainer/stats/kit/dfree.py)), tested in
  `tests/test_stats_kit_dfree.py`:
  - the Bahadur–Savage mixture: the t-interval's coverage bound and its simulation;
  - the quantile lemma's exact coverage and the Beta law of coverage given the calibration set;
  - full conformal for ridge regression on a grid of candidate labels;
  - the jackknife and jackknife+ for any fitting routine, and the minimum-norm interpolator as an unstable one;
  - binned conditional coverage and the group-conditional threshold of Gibbs, Cherian & Candès (quantile regression
    as an LP, bisection on the score);
  - nonexchangeable conformal with fixed weights;
  - conformal risk control for monotone losses;
  - conformal outlier p-values.
- **The rank strip** (`RankStrip` in `explainer/stats/viz.py`), the part's instrument: the n + 1 rank slots of the
  calibration scores and the test score, the covered slots up to k = ⌈(n + 1)(1 − α)⌉ and the missed ones above,
  with `drop(k)` to land the test score in any slot. It shows why the lemma holds whatever the distribution.

**Data.**
- From the Museum: NHANES 2017–18 (systolic pressure, age, sex, race, BMI) and the Wisconsin breast cancer data.
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| t-interval for the mean | Bahadur–Savage mixture, n = 50 | 95% | 14.2% | broken |
| split conformal prediction interval | Bahadur–Savage mixture, n = 50 | 95% | 95.8% | kept |
| marginal split conformal, ages 70+ | NHANES systolic pressure | 90% | 78.3% | broken |
| group-conditional conformal, ages 70+ | NHANES systolic pressure | 90% | 90.7% | kept |
| split conformal after a changepoint | noise SD 1 → 2.5, 300 steps after | 90% | 77.0% | broken |
| weighted (nonexchangeable) conformal | noise SD 1 → 2.5, 300 steps after | 90% | 86.0% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats57.compute   # once (about twenty-five minutes, mostly the NHANES LPs)
python tools/build.py stats57 -q l                         # fast 480p preview
python tools/build.py stats57                              # 1080p30 -> renders/stats57.mp4
python tools/qa_scene.py stats57 Lemma
python tools/lecture_length.py stats57 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Bahadur and Savage | n = 50, mixture mean 3: t-interval coverage 95% (ε = 0.3), 63.5% (0.02), 22.1% (0.005), 14.2% (0.003; bound 13.9%), 5.5% (0.001); P(no atom) = 0.997⁵⁰ = 0.861 |
| 1 | The quantile lemma | n = 19: k = 18, coverage 18/20; n = 20: 19/21 = 90.5%; finite only if n ≥ 9 at α = 0.1; n = 100: Beta(91, 10), mean 90.1%, SD 3.0, 5% quantile 84.8%, 5.9% of 4,000 calibration sets below 85%; PAC k = 96 |
| 2 | Full, split, jackknife+ | ridge, n = 40, p = 5, 200 reps: full 89.5% (median length 3.56), split 90.0% (4.04) |
| 3 | Impossibility | heteroscedastic regression: plain split 88.9% overall, 100% where the noise is small, 57% where it is large; normalized residuals 89.9%, 86–93% in every bin; 1,200 points allow at most 133 bins at α = 0.1 |
| 4 | Function classes | 11 functions, n = 1,200: slack ≤ 11/1,201 ≈ 0.9% |
| 5 | Beyond exchangeability | jump in the noise SD at t = 1,000: equal weights 77% in the 300 steps after, ρ = 0.99 weights 86%; overall 87.3% vs 89.8%; TV bound 50 steps after: coverage ≥ 47% (equal) vs ≥ 60% (ρ = 0.99), swapped-pair TV 0.52 |
| 6 | Online | the same series: γ = 0 75% after the jump (miss rate 12.8%), γ = 0.005 87% (10.3%), γ = 0.02 89% (10.1%); bound 181/T, within one point needs T ≥ 18,100 |
| 7 | Outliers | Wisconsin, 150 benign fit the score, 157 reference, 50 benign + 40 malignant tests, BH q = 0.1, 50 splits: FDR 5.6%, power 72.8%; pooled over 20 splits, 64% of malignant p ≤ 0.02 |
| 8 | Risk control | 20 candidate labels, n = 500, FNR at α = 0.1: λ̂ = 0.595, test FNR 8.9%, mean set size 8.2, mean FNR over 200 calibration sets 9.7%; n = 100 needs R̂ ≤ 9.1% |
| 9 | Groups | NHANES, 5,176 adults, 8 splits: marginal 89.5% overall, 98.6% (18–29), 78.3% (70+), 85.7% (race 4); Mondrian by age fixes ages only (race 4 86.0%); group-conditional 88.6–91.0% in every row |
| 10 | Open problems | — |
| 11 | Outro | — |

## Sources

- **The hook.** R. R. Bahadur & L. J. Savage, *Ann. Math. Stat.* 27 (1956); S. Wilks, *Ann. Math. Stat.* 12 (1941).
- **Foundations.** V. Vovk, A. Gammerman & G. Shafer, *Algorithmic Learning in a Random World* (2005; 2nd ed. 2022);
  V. Vovk, *Proc. ACML* (2012); J. Lei, M. G'Sell, A. Rinaldo, R. Tibshirani & L. Wasserman, *JASA* 113 (2018);
  A. Angelopoulos, R. Foygel Barber & S. Bates, *Theoretical Foundations of Conformal Prediction* (2024); A. Angelopoulos
  & S. Bates, *A Gentle Introduction to Conformal Prediction* (2021).
- **Methods.** R. Foygel Barber, E. Candès, A. Ramdas & R. Tibshirani, *Ann. Stat.* 49 (2021) (jackknife+); J. Lei,
  *Biometrika* 106 (2019); M. Bian & R. Foygel Barber, *EJS* 17 (2023).
- **Impossibility.** J. Lei & L. Wasserman, *JRSS B* 76 (2014); R. Foygel Barber, E. Candès, A. Ramdas &
  R. Tibshirani, *Information and Inference* 10 (2021); R. Foygel Barber, *EJS* 14 (2020); D. Donoho, *Ann. Stat.* 16
  (1988).
- **Function classes.** I. Gibbs, J. Cherian & E. Candès, *JRSS B* (2025).
- **Beyond exchangeability.** R. Tibshirani, R. Foygel Barber, E. Candès & A. Ramdas, NeurIPS (2019); L. Lei &
  E. Candès, *JRSS B* 83 (2021); R. Foygel Barber, E. Candès, A. Ramdas & R. Tibshirani, *Ann. Stat.* 51 (2023);
  V. Chernozhukov, K. Wüthrich & Y. Zhu, COLT (2018).
- **Online.** I. Gibbs & E. Candès, NeurIPS (2021); I. Gibbs & E. Candès, *JMLR* 25 (2024).
- **Outliers and risk.** S. Bates, E. Candès, L. Lei, Y. Romano & M. Sesia, *Ann. Stat.* 51 (2023); A. Angelopoulos,
  S. Bates, A. Fisch, L. Lei & T. Schuster, ICLR (2024); A. Angelopoulos, S. Bates, E. Candès, M. Jordan & L. Lei,
  arXiv:2110.01052 (2021); C. Mohri & T. Hashimoto, ICML (2024).
- **Efficiency.** J. Lei, J. Robins & L. Wasserman, *JASA* 108 (2013).
- **Data.** CDC/NCHS, NHANES 2017–18; W. Wolberg, W. Street & O. Mangasarian (1995).

## Problems and solutions

1. **The lemma's exact coverage.** With continuous exchangeable scores S₁, …, S_{n+1}, ties have probability zero
   and every ordering is equally likely, so the rank of S_{n+1} is uniform on {1, …, n + 1}. S_{n+1} ≤ S_(k) (the k-th
   smallest of the first n) exactly when its rank among all n + 1 is at most k, so P = k/(n + 1).
2. **The Beta law.** Given the calibration scores, coverage is F(S_(k)). The F(S_i) are i.i.d. uniform, and F is
   increasing, so F(S_(k)) = U_(k), the k-th order statistic of n uniforms, which is Beta(k, n + 1 − k).
3. **Bahadur–Savage.** With probability (1 − ε)ⁿ the sample contains no atom and is an N(0, 1) sample, whose
   t-interval covers 3 with probability P(|x̄ − 3| ≤ t s/√n), which tends to zero; so coverage ≤ 1 − (1 − ε)ⁿ + o(1).
   Taking ε → 0 at fixed n drives the bound to zero while the mean stays 3.
4. **ACI.** Summing α_{t+1} = α_t + γ(α − err_t) gives α_{T+1} − α₁ = γ Σ(α − err_t). If α_t < 0 the set is the whole
   line and err_t = 0, so α_t rises; if α_t > 1 the set is empty and err_t = 1, so it falls; hence α_t ∈ [−γ, 1 + γ]
   for all t, and |Σ(α − err_t)| ≤ (max(α₁, 1 − α₁) + γ)/γ. Divide by T.
5. **Mondrian.** Conditional on the group g of the test point, the calibration points of group g and the test point
   are exchangeable (exchangeability is preserved by conditioning on a symmetric event), so the lemma applies within g.
6. **Risk control.** Let λ′ be the threshold computed from all n + 1 losses, inf{λ: (Σ_{i≤n+1} L_i(λ) + 0)/(n + 1) ≤ α}
   with B replaced by the actual test loss. Since L_{n+1} ≤ B, λ′ ≤ λ̂, so L_{n+1}(λ̂) ≤ L_{n+1}(λ′) by monotonicity. By
   exchangeability E L_{n+1}(λ′) = E (1/(n + 1)) Σ L_i(λ′) ≤ α.

## Glossary

- **Foundations.** Exchangeability; nonconformity score; rank; quantile lemma; calibration set; marginal coverage;
  training-conditional (PAC) coverage; smoothed p-value; tolerance interval.
- **Methods.** Full conformal; split conformal; jackknife; jackknife+; CV+; homotopy; algorithmic stability.
- **Limits.** Conditional coverage; local conformal; Bahadur–Savage family; impossibility; functional.
- **Classes and weights.** Mondrian conformal; group-conditional coverage; conditional calibration; slack; weighted
  conformal; covariate shift; label shift; likelihood ratio; nonexchangeable conformal; total variation.
- **Online and testing.** Adaptive conformal inference; DtACI; conformal p-value; PRDS; outlier detection.
- **Risk.** Conformal risk control; false negative rate; learn then test; conformal factuality.

## Where it comes back

- **Part 58**: e-values and test martingales, and ACI's online-learning idea made into anytime-valid tests.
- **Part 59**: conformal inference when p and n grow together.
- **Part 62**: prediction intervals for individual causal effects.
- **Part 64**: uncertainty for foundation models.
- **Part 65**: the dissertation's predictive claims.

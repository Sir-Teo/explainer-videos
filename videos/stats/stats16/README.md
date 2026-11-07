# Statistics, Built — Part 16: Without Assumptions

Part 16 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Every interval since Part 8 leaned on a model
for the data. This part asks how far we can get without a parametric shape model. It still requires assumptions: IID sampling and regularity for the ordinary bootstrap, exchangeability for label permutations, and symmetry/continuity for the untied signed-rank law. Exact calibration is distinguished from asymptotic approximation throughout.

It opens with Efron's paper of 1979 and his running example: 15 American law schools, LSAT against GPA, r = 0.776.
The normal-theory standard error is 0.115; the bootstrap's, without a normal shape model, is 0.135.

From there the part covers:
- **Permutation tests.** Exchangeability under H₀ makes every relabelling equally likely. All 2,704,156 splits of 24
  incomes from the World give p = 0.232 (Welch: 0.237); shuffling GPAs against LSATs gives p ≈ 0.0017 for the law
  schools' correlation.
- **Signs and signed ranks.** Darwin's maize (Fisher 1935): the sign test (p = 0.0074), Fisher's 2¹⁵ sign flips (1,726
  as extreme, p = 0.053), Wilcoxon's W⁺ = 96 with its exact null from the generating function ∏(1 + xᵏ)/2 (p = 0.041),
  and the Hodges–Lehmann estimate and interval from the Walsh averages.
- **Mann–Whitney.** The Challenger temperatures: midranks, U as a count of 112 pairs (87.5), its exact null, and
  U/(mn) = 0.781, the area under the ROC curve. What the test does and does not test.
- **More rank methods.** Kruskal–Wallis on three regions' incomes, Friedman's test for blocks, Spearman's and Kendall's
  correlations, and how one bad value moves Pearson's r much more than the rank correlations.
- **Efficiency.** Pitman's ARE; power of t and Wilcoxon–Mann–Whitney under normal, t₃ and contaminated errors; the
  efficiency table and Hodges–Lehmann's bound 0.864; both tests keep their size (the Board).
- **The jackknife.** Leave-one-out correlations, Quenouille's bias and Tukey's SE (0.143), Bessel's correction
  rediscovered, influence, and the jackknife's failure for the median.
- **The bootstrap principle.** The `BootstrapResampler`; 2,000 resampled correlations; Efron's two worlds; a check in
  the World (median income, n = 25: real SD 6.06 vs bootstrap 4.72); how many resamples; what it assumes.
- **Bootstrap intervals.** Percentile, basic (which passes 1 here), bootstrap-t on skewed incomes, BCa stated with
  z₀ = −0.137 and a = −0.076; five intervals compared; four Board rows.
- **When it fails.** The uniform maximum: P*(θ̂* = θ̂) = 1 − (1 − 1/n)ⁿ → 1 − 1/e. The percentile interval covers 0%.
  Fixes: a 95% one-sided pivot interval [M, M/0.05^(1/n)], a parametric pivot bootstrap (not a raw percentile interval), and properly rate-scaled m-out-of-n with m → ∞ and m/n → 0.
- **Cross-validation.** Polynomials in age for log income; training error vs 10-fold CV (best: degree 3); the
  optimism 2σ²p/n; leave-one-out and PRESS; cautions.
- **Density estimates.** The histogram's arbitrary bins; the `KernelSum`; bandwidths 1, 4.16 (Silverman) and 10
  against the full-population histogram; the bias–variance trade-off and n^(−1/5).

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- the law schools (Efron & Tibshirani 1993, Table 3.1), Darwin's differences (Fisher 1935) and the Challenger
  temperatures come from the Museum or the scene;
- incomes, ages and heights are the World's (seed 1662);
- the efficiency and failure simulations are seeded.

**Built in this part:**
- **`statkit.ranks`** ([`explainer/stats/kit/ranks.py`](../../../explainer/stats/kit/ranks.py)), checked against
  SciPy in `tests/test_stats_kit_ranks.py`:
  - the exact signed-rank null by generating function, and the signed-rank test;
  - the untied Mann–Whitney null by recursion; this part uses a local conditional-midrank recursion for tied temperatures;
  - Kruskal–Wallis, Spearman and Kendall.
- **`statkit.bootstrap`** ([`explainer/stats/kit/bootstrap.py`](../../../explainer/stats/kit/bootstrap.py)), checked in
  `tests/test_stats_kit_bootstrap.py`:
  - resampling, the bootstrap and the jackknife (bias, SE, leave-one-out values);
  - percentile, basic, normal, BCa and bootstrap-t intervals;
  - Silverman's bandwidth, the Gaussian kernel density estimate, and K-fold cross-validation of polynomial fits.
- **The bootstrap resampler** (`BootstrapResampler` in `explainer/stats/viz.py`): the sample as tokens, copied with
  replacement into a resample row; each replicate dropped as a dot.
- **The kernel sum** (`KernelSum` in `explainer/stats/viz.py`): one bump per observation and their sum.

The Coverage Board gains eight rows, R = 10,000 (bootstrap intervals with B = 999).

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| bootstrap percentile | the World's incomes, n = 15 | 85.51% | broken |
| bootstrap BCa | the World's incomes, n = 15 | 86.66% | broken |
| bootstrap-t | the World's incomes, n = 15 | 91.64% | broken |
| Student's t | the World's incomes, n = 15 | 88.40% | broken |
| percentile, the maximum | Uniform(0, θ), n = 50 | 0.00% | broken |
| basic, the maximum | Uniform(0, θ), n = 50 | 87.80% | broken |
| t-test (size) | contaminated normal, 20 + 20 | 4.39% | kept |
| Wilcoxon–Mann–Whitney (size) | contaminated normal, 20 + 20 | 5.18% | kept |

## Build it

```bash
python -m videos.stats.stats16.compute         # once (a few minutes; cached in .cache/stats16)
python tools/build.py stats16 -q l             # fast 480p preview
python tools/build.py stats16                  # 1080p30 -> renders/stats16.mp4
python tools/qa_scene.py stats16 Principle
python tools/lecture_length.py stats16 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Fifteen law schools, 1979 | r = 0.776; SE 0.115 (normal formula), 0.135 (bootstrap) |
| 1 | Permutation tests | 12 + 12 incomes, difference −20.4; 2,704,156 splits, p = 0.232; Welch 0.237; law schools p ≈ 0.0017 |
| 2 | Signs and signed ranks | 13 of 15 positive, sign p = 0.0074; Fisher 1,726/32,768 = 0.053; W⁺ = 96, p = 0.041; t p = 0.050; Hodges–Lehmann 25, 95.2% CI [4.0, 41.5] |
| 3 | Mann–Whitney | rank sum 52.5, U = 87.5 of 112, conditional exact p = 0.03352 (0.03757 tie-corrected normal approximation); AUC 0.781 |
| 4 | More rank methods | H = 1.53, p = 0.47 (F = 0.36, p = 0.70); Friedman Q = 10.2; Spearman 0.796, Kendall 0.638 (86 vs 19 pairs); one bad GPA: 0.148, 0.436, 0.390 |
| 5 | Efficiency | power t / WMW: 0.69 / 0.66 (normal), 0.77 / 0.89 (t₃), 0.35 / 0.52 (contaminated); ARE 0.955, 1.097, 1.5, 1.90, 2.41; bound 0.864 |
| 6 | The jackknife | bias −0.0065, SE 0.143; without school 1, r = 0.893; LSAT median: 3 distinct values, SE 14.7 vs 18.4 |
| 7 | The bootstrap principle | SE 0.135; median income: truth 38.9, sample 37.65, SD 6.06 real vs 4.72 bootstrap; 77,558,760 distinct resamples |
| 8 | Bootstrap intervals | percentile [0.447, 0.962], basic [0.591, 1.106], normal [0.513, 1.040], BCa [0.287, 0.943], Fisher z [0.439, 0.922]; incomes: t [28.0, 56.9], percentile [30.7, 55.5], bootstrap-t [30.2, 61.7], truth 49.5 |
| 9 | When it fails | P*(spike) 0.625 (theory 0.636, limit 0.632); exact one-sided 95% CI [0.966, 1.026] |
| 10 | Cross-validation | best degree 3, CV 0.3425; optimism: 0.3395 vs CV 0.3425 (degree 3), 0.3493 vs 0.3536 (degree 8) |
| 11 | Density estimates | Silverman h = 4.16 cm for 60 heights |
| 12 | Outro | — |

## Sources

- **Permutation and rank tests.**
  - C. Darwin, *The Effects of Cross and Self Fertilisation in the Vegetable Kingdom* (1876); R. A. Fisher, *The
    Design of Experiments* (1935), §17.
  - F. Wilcoxon, *Biometrics Bull.* 1 (1945); H. Mann & D. Whitney, *Ann. Math. Stat.* 18 (1947).
  - W. Kruskal & W. A. Wallis, *JASA* 47 (1952); M. Friedman, *JASA* 32 (1937).
  - C. Spearman, *Am. J. Psych.* 15 (1904); M. Kendall, *Biometrika* 30 (1938).
  - D. Bamber, *J. Math. Psych.* 12 (1975).
- **Efficiency.**
  - E. Pitman, lecture notes on nonparametric inference (1948); J. Hodges & E. Lehmann, *Ann. Math. Stat.* 27 (1956),
    34 (1963); J. Tukey, in *Contributions to Probability and Statistics* (1960).
- **Resampling.**
  - M. Quenouille, *JRSS B* 11 (1949), *Biometrika* 43 (1956); J. Tukey, *Ann. Math. Stat.* 29 (abstract, 1958).
  - B. Efron, *Ann. Stat.* 7 (1979); *JASA* 82 (1987); *The Jackknife, the Bootstrap and Other Resampling Plans* (1982).
  - P. Bickel & D. Freedman, *Ann. Stat.* 9 (1981); P. Hall, *Ann. Stat.* 16 (1988); P. Bickel, F. Götze & W. van
    Zwet, *Stat. Sinica* 7 (1997).
- **Prediction and smoothing.**
  - M. Stone, *JRSS B* 36 (1974); S. Geisser, *JASA* 70 (1975); D. Allen, *Technometrics* 16 (1974); C. Mallows,
    *Technometrics* 15 (1973).
  - M. Rosenblatt, *Ann. Math. Stat.* 27 (1956); E. Parzen, *Ann. Math. Stat.* 33 (1962); B. Silverman, *Density
    Estimation for Statistics and Data Analysis* (1986).
- **Books.**
  - B. Efron & R. Tibshirani, *An Introduction to the Bootstrap* (1993); A. Davison & D. Hinkley, *Bootstrap Methods
    and their Application* (1997).
  - E. Lehmann, *Nonparametrics: Statistical Methods Based on Ranks* (1975; rev. 2006); L. Wasserman, *All of
    Nonparametric Statistics* (2006).

## Problems and solutions

**1. A small permutation test.**

*Solution.* The pooled values are 1, 2, 3, 4, 5, 9, and there are C(6, 3) = 20 ways to choose the first group. The
observed group sums to 17. A group of three without the 9 sums to at most 3 + 4 + 5 = 12. A group with the 9 needs the
other two to sum to at least 8: only {3, 5} and {4, 5}. So 2 of the 20 splits are as extreme, and p = 2/20 = 0.10.

**2. Wilcoxon's distribution for n = 4.**

*Solution.* Multiply out (1 + x)(1 + x²)(1 + x³)(1 + x⁴) = 1 + x + x² + 2x³ + 2x⁴ + 2x⁵ + 2x⁶ + x⁷ + x⁸ + x⁹ + x¹⁰.
The coefficients sum to 16 = 2⁴, and P(W⁺ = w) is the coefficient over 16. Then P(W⁺ ≥ 9) = (1 + 1)/16 = 1/8. With
four pairs, no one-sided test at level 0.05 is possible: the smallest p is 1/16.

**3. The rank sum as a pair count.**

*Solution.* Assume no ties. Sort the x's: x₍₁₎ < … < x₍ₘ₎. The rank of x₍ₖ₎ in the pooled sample is k (the x's at or below it) plus
the number of y's below it. Summing over k, R = m(m + 1)/2 + #{(i, j) : xᵢ > yⱼ}. So U = R − m(m + 1)/2 is the pair
count. With ties, average ranks give half credit to tied cross-group pairs.

**4. The jackknife and Bessel's correction.**

*Solution.* Let SS = Σ(xⱼ − x̄)² and dᵢ = xᵢ − x̄. Leaving out xᵢ, Σⱼ≠ᵢ(xⱼ − x̄₍ᵢ₎)² = SS − n dᵢ²/(n − 1), so
σ̂²₍ᵢ₎ = [SS − n dᵢ²/(n − 1)]/(n − 1).
- **The average:** since Σdᵢ² = SS, the mean of the σ̂²₍ᵢ₎ is SS(n − 2)/(n − 1)².
- **The bias estimate:** (n − 1)[SS(n − 2)/(n − 1)² − SS/n] = −SS/(n(n − 1)).
- **The corrected estimate:** SS/n + SS/(n(n − 1)) = SS/(n − 1) = s².

**5. The chance a resample contains a point.**

*Solution.* Each of the n draws misses x₁ with probability 1 − 1/n, independently. So P*(x₁ in the resample) =
1 − (1 − 1/n)ⁿ, which tends to 1 − 1/e ≈ 0.632. On average a resample contains about 63% of the distinct points.

**6. The percentile interval for a maximum.**

*Solution.* Every resampled value is one of the xᵢ, so every resampled maximum is at most maxᵢ xᵢ. Hence both
percentiles are at most maxᵢ xᵢ. But maxᵢ xᵢ < θ with probability 1, since the uniform has no atom at θ. So the
interval lies below θ and never contains it: coverage 0, as on the Board.

## Glossary

- **Exchangeable**: a joint distribution unchanged by permuting the observations.
- **Permutation test**: a test whose null distribution is the statistic over all relabellings the null makes equally
  likely.
- **Sign test**: the test of a zero median from the number of positive differences, Binomial(n, ½) under H₀.
- **Signed-rank statistic (W⁺)**: the sum of the ranks of |dᵢ| over the positive dᵢ.
- **Walsh averages**: (dᵢ + dⱼ)/2 for i ≤ j; their median is the Hodges–Lehmann estimate.
- **Rank-sum statistic, Mann–Whitney U**: the sum of one group's pooled ranks; U subtracts its minimum and counts pairs.
- **Midranks**: the average rank given to tied values.
- **AUC**: the area under the ROC curve; equals U/(mn), an estimate of P(X > Y) + ½P(X = Y).
- **Kruskal–Wallis H; Friedman Q**: rank analogues of the one-way ANOVA and the randomized-block ANOVA.
- **Spearman's r_S; Kendall's τ**: Pearson's correlation of the ranks; (concordant − discordant)/C(n, 2).
- **Asymptotic relative efficiency (ARE)**: the limiting ratio of sample sizes two tests need for equal power.
- **Contaminated normal**: a mixture of a normal with a small share of a much wider normal.
- **Jackknife**: leave-one-out recomputation, giving estimates of bias and standard error.
- **Empirical distribution F̂ₙ**: mass 1/n on each observation.
- **Bootstrap**: estimating a sampling distribution by resampling from F̂ₙ with replacement.
- **Percentile, basic, bootstrap-t, BCa intervals**: four ways to turn replicates into an interval.
- **Bias correction z₀; acceleration a**: BCa's adjustments, from the share of replicates below the estimate and the
  jackknife's skewness.
- **Parametric bootstrap**: resampling from a fitted model rather than from F̂ₙ.
- **m-out-of-n bootstrap**: resampling fewer points than the sample has, to repair some failures with statistic-specific scaling and m → ∞, m/n → 0.
- **Cross-validation (K-fold, leave-one-out)**: estimating prediction error by predicting held-out data.
- **Optimism**: how much the training error understates the test error; 2σ²p/n for a fixed full-rank homoskedastic linear model and fresh responses at the same design.
- **PRESS**: the leave-one-out prediction sum of squares, Σ(eᵢ/(1 − hᵢᵢ))².
- **Kernel density estimate; bandwidth**: an average of bumps K((x − xᵢ)/h)/h; h is their width.

## Where it comes back

| Idea | Returns in |
|---|---|
| block bootstraps for dependent data | 17 |
| cross-validation and model choice | 19, 28 |
| kernels, nonparametric regression, the curse of dimensionality | 29 |
| influence functions; Pitman efficiency proved | 30 |
| permutation methods for many tests | 33 |
| conformal prediction from exchangeability | 34, 57 |
| bootstrap consistency, Edgeworth expansions, the uniform maximum | 47 |
| the Coverage Board | every part; 65 |

# Statistics, Built — Part 46: The Theory of Testing and Confidence

Part 46 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fourth part of Stage IV, the PhD core.

It opens with the Behrens–Fisher problem: are two normal means equal when the variances are unequal and unknown?
- Behrens (1929) and Fisher (1935) answered with a fiducial test whose size moves with the variance ratio.
- Welch (1938, 1947) gave the practical approximation.
- Linnik (1966–68) proved that no exact test of the natural kind exists.

The part then builds:
- the Neyman–Pearson theory in full: most powerful, monotone-likelihood-ratio, unbiased and invariant tests;
- the likelihood ratio test on a boundary;
- confidence sets by inversion, with their impossibility theorems and bounded-parameter repairs;
- closed testing, conditional coverage, p-values as evidence, and goodness of fit with estimated parameters.

It keeps two promises:
- **Part 10** built tests that keep their size. Chapters 1–5 ask which level-α test is most powerful, and prove that the
  t test is UMPU and UMP invariant.
- **Part 11** built intervals with good coverage. Chapters 6–10:
  - construct uniformly most accurate sets by inversion;
  - show that ratio problems need unbounded sets;
  - repair intervals for bounded parameters;
  - ask what coverage means for the data in hand.

**Built in this part:**
- **`statkit.testing`** ([`explainer/stats/kit/testing.py`](../../../explainer/stats/kit/testing.py)), tested in
  `tests/test_stats_kit_testing.py`:
  - **Behrens–Fisher:** Welch–Satterthwaite degrees of freedom; Behrens–Fisher fiducial critical values by
    quadrature; sizes of the pooled t, Welch and fiducial tests.
  - **Binomial tests:**
    - randomized UMP one-sided tests;
    - the UMPU two-sided test (two side conditions, solved exactly);
    - the equal-tailed test;
    - the generalized Neyman–Pearson lemma as a linear programme.
  - **Neyman structure:** the conditional two-binomial test, randomized to be similar, with its unconditional size at
    every nuisance value.
  - **Likelihood ratio on a boundary:** Chernoff's χ̄² critical value.
  - **Confidence sets:**
    - Clopper–Pearson sets and Wald intervals with exact coverage;
    - Fieller's sets (bounded, two rays, or all of ℝ);
    - Feldman–Cousins unified intervals and flip-flopping limits, with exact Poisson coverage.
  - **Simultaneous inference:** closed testing with Bonferroni (Holm) or Simes (Hommel) local tests; Scheffé's
    multiplier.
  - **Conditional inference and evidence:** Buehler-style recognizable subsets for the n = 2 t interval; Berger–Sellke
    bounds and the −e p log p calibration.
  - **Goodness of fit:** Kolmogorov–Smirnov with estimated parameters (Lilliefors).
- **The Neyman-structure visualizer** (`NeymanSlices` in `explainer/stats/viz.py`), the part's instrument. For each
  value of a sufficient statistic for the nuisance parameter, it draws the conditional null distribution as bars, with
  the part the test rejects painted over them: each slice spends exactly α, so the test is similar.

**Data.**
- From the Museum:
  - Old Faithful's eruptions (split by the preceding wait);
  - ISIS-2's vascular deaths;
  - the lady tasting tea;
  - Bliss's beetles.
- Feldman and Cousins's published Table II (b = 0) is reproduced as a check.
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains eight rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| pooled t test (size) | n = 5 (SD 3) vs n = 25 (SD 1) | 5% | 30.2% | broken |
| Welch's test (size) | same | 5% | 5.3% | kept |
| Behrens–Fisher test (size) | same | 5% | 4.8% | kept |
| delta-method interval for a ratio | denominator mean 0.5, SE 1 | 95% | 78.1% | broken |
| Fieller's set for a ratio | same | 95% | 95.2% | kept |
| flip-flopping Poisson limits | background 3, μ = 2.34 | 90% | 85.5% | broken |
| Feldman–Cousins limits | same | 90% | 92.4% | conservative |
| KS test, estimated mean and SD (size) | normal data, n = 20 | 5% | 0.01% | conservative |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats46.compute   # once (a few minutes)
python tools/build.py stats46 -q l                         # fast 480p preview
python tools/build.py stats46                              # 1080p30 -> renders/stats46.mp4
python tools/qa_scene.py stats46 UMPU
python tools/lecture_length.py stats46 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The Behrens–Fisher problem | pooled size 30% or 0.06%; Welch ≈ 5%; Old Faithful t = 39.5 on 196 df |
| 1 | The Neyman–Pearson lemma | Bin(20), p = .3 vs .5: reject x ≥ 10, and x = 9 w.p. 0.031; sizes 4.8% / 11.3% without |
| 2 | MLR and Karlin–Rubin | Cauchy ratio peaks at x = 1.6 and returns to 1 |
| 3 | Unbiased tests and Neyman structure | UMPU: reject x < 2 or > 10 (γ = 0.69, 0.19); equal tails dip to 4.99%; ISIS-2 z = −5.22 |
| 4 | Invariance | power at μ/σ = 0.5: z 0.47, t 0.43, sign 0.34 |
| 5 | The likelihood ratio test | Poisson 95% point 3.74 vs 3.84; boundary: 50% zeros, size 2.5% → 4.9% with 2.71 |
| 6 | Confidence sets by inversion | Clopper–Pearson ≥ 95.8%; Wald down to 9.5% |
| 7 | Impossibility | β = 0.5: Fieller 95.2% (68% all of ℝ); delta 78%; Bliss LD50 1.772 |
| 8 | Bounded parameters | b = 3, n = 0: FC [0, 0.95]; classical −0.70; flip-flop 85.5% |
| 9 | Simultaneous inference | k = 20: Scheffé 5.60, Bonferroni 3.02; Holm rejects 1, Hommel 4 |
| 10 | Conditional inference | 50% t interval: 61–86% on the recognizable set |
| 11 | p-values and evidence | p = 0.05: P(H₀ \| x) ≥ 0.128 (all), 0.290 (unimodal), 0.321 (normal) |
| 12 | Goodness of fit | Pearson 95% point 11.0 vs 11.07; KS table 0.294 vs correct 0.192 (n = 20) |
| 13 | Outro | — |

The rest of the part's numbers, chapter by chapter:
- **Hook.**
  - Sizes at nominal 5%, as pooled / Welch / Behrens–Fisher (20,000 data sets each):

    | Setting | Pooled | Welch | Behrens–Fisher |
    |---|---|---|---|
    | 10 vs 10, equal SDs | 5.0% | 4.9% | 3.8% |
    | 10 vs 10, SDs 1 and 3 | 5.8% | 5.0% | 4.4% |
    | 5 (SD 3) vs 25 (SD 1) | 30.0% | 5.6% | 5.1% |
    | 25 (SD 3) vs 5 (SD 1) | 0.06% | 4.6% | 3.1% |

  - The fiducial critical value for n = 5, 25 runs from 2.06 (t₂₄) to 2.78 (t₄) as φ goes from 0° to 90°.
  - Old Faithful: eruptions after waits under 70 minutes last 2.14 minutes (n = 103, SD 0.46); after longer waits,
    4.31 (n = 169, SD 0.41). The 95% CI for the difference is [2.07, 2.29].
- **Chapter 1.**
  - The lemma, its one-line proof and necessity.
  - Randomization: Bin(20), H₀ p = 0.3 vs p = 0.5. The test is c = 9, γ = 0.031.
  - The same test is UMP against every p > 0.3.
  - The generalized lemma (Dantzig & Wald 1951) is a linear programme; existence follows from weak-* compactness.
- **Chapter 2.**
  - MLR in exponential families, U(0, θ), the noncentral t, χ², F and the hypergeometric.
  - Karlin–Rubin.
  - No UMP two-sided test exists.
  - For one Cauchy observation, the locally most powerful test rejects on a bounded interval.
- **Chapter 3.**
  - Unbiasedness means β(θ₀) = α and β′(θ₀) = 0. The UMPU binomial test has c₁ = 2, c₂ = 10, γ₁ = 0.693,
    γ₂ = 0.192.
  - The LP reproduces its power: 0.3345 at p = 0.15 and 0.4459 at p = 0.5.
  - Neyman structure: X ~ Bin(8, p₁), Y ~ Bin(10, p₂), sliced at totals 4, 9, 13. The randomized conditional test has
    size exactly 5% at every common p; Fisher's exact test has size at most 1.8%.
  - ISIS-2: 804 aspirin deaths against 909.3 expected given 1,820, so z = −5.22 and one-sided P ≈ 1.0 × 10⁻⁷.
  - The tea: 1/70 = 0.0143.
  - The t test is UMPU (Lehmann 1959).
- **Chapter 4.**
  - Maximal invariants. The t test is UMP among scale-invariant tests; its power at μ/σ = 0.5 with n = 10 is 0.427,
    against 0.475 for z (σ known) and 0.336 for the sign test.
  - Hunt–Stein (1946): with an amenable group, the best invariant test is minimax.
  - The F test is UMP invariant (Hsu 1941) and most stringent (Wald 1942).
- **Chapter 5.**
  - Wilks (1938). Poisson n = 10, λ₀ = 2: quantiles 0.47 / 2.80 / 3.74 / 7.05 vs χ²₁'s 0.45 / 2.71 / 3.84 / 6.63; size
    4.3%.
  - Chernoff (1954): ½χ²₀ + ½χ²₁, with 50.0% exact zeros. Size 2.5% with 3.84, 4.9% with 2.71.
  - Self & Liang (1987).
  - Failures: mixtures (Hartigan 1985), change points (Davies 1977), growing dimension (Part 59).
- **Chapter 6.**
  - Neyman's inversion. The Clopper–Pearson belt (n = 20): at p = 0.3 the acceptance region is x = 2, …, 10; at
    x = 6 the interval is [0.119, 0.543].
  - Coverage: minimum 95.8% for Clopper–Pearson, 9.5% for Wald.
  - UMA and UMA-unbiased sets. Pratt (1961): expected length = ∫ P(θ′ ∈ C) dθ′.
- **Chapter 7.**
  - Fieller's pivot and quadratic.
  - a ~ N(1, 1), b ~ N(β, 1), at β = 4 / 2 / 1 / 0.5:
    - Fieller's set is bounded 98% / 51% / 16% / 8% of the time, and covers 95.0% / 95.0% / 95.4% / 95.2%;
    - the delta method covers 97.3% / 96.8% / 93.1% / 78.1%.
  - Gleser & Hwang (1987).
  - Bliss: slope z = 11.8. Fieller [1.7639, 1.7792] against delta [1.7642, 1.7793].
  - Weak instruments (Dufour 1997).
- **Chapter 8.**
  - Poisson signal plus background b = 3. The classical upper limit at n = 0 is −0.70.
  - Feldman–Cousins (b = 3), n = 0…10:
    - [0, 0.95], [0, 1.87], [0, 3.03], [0, 4.42], [0, 5.59], [0, 6.98];
    - then [0.16, 8.46], [0.90, 9.53], [1.51, 10.99], [1.88, 12.29], [2.64, 13.50].
  - Flip-flopping switches at n = 9 (b + 3√b). Its exact coverage falls to 85.5% at μ = 2.34; FC never goes below 90%.
- **Chapter 9.**
  - Scheffé multipliers (k = 1, 2, 3, 5, 10, 20): 1.96, 2.45, 2.80, 3.33, 4.28, 5.60. Bonferroni: 1.96, 2.24, 2.39,
    2.58, 2.81, 3.02.
  - Closed testing on p = (0.011, 0.018, 0.024, 0.040): Bonferroni and Holm reject H₁ only; Hommel (Simes) rejects
    all four.
  - Partitioning; gatekeeping.
- **Chapter 10.**
  - Welch's uniform example.
  - Buehler (1959). For the n = 2 50% t interval on {|x̄|/s ≤ 1 + √2}, at μ/σ = 0, 0.25, 0.5, 1, 2, 4:
    - coverage 61.1%, 61.4%, 62.6%, 66.0%, 74.4%, 85.9%;
    - share of samples in the set 82%, 81%, 78%, 67%, 42%, 11%.
  - Robinson (1979).
- **Chapter 11.**
  - Berger–Sellke lower bounds on P(H₀ | x), as all g / symmetric unimodal / normal / calibration:

    | p | All g | Symmetric unimodal | Normal | Calibration |
    |---|---|---|---|---|
    | 0.1 | 0.205 | 0.389 | 0.412 | 0.385 |
    | 0.05 | 0.128 | 0.290 | 0.321 | 0.289 |
    | 0.01 | 0.035 | 0.109 | 0.133 | 0.111 |
    | 0.001 | 0.0044 | 0.018 | 0.024 | 0.018 |

  - Sellke–Bayarri–Berger (2001).
  - Lindley's paradox (Part 15); the ASA (2016); Benjamin et al. (2018).
- **Chapter 12.**
  - Pearson's χ² limit by projection. A die, 60 rolls: quantiles 4.40 / 9.20 / 11.0 / 15.2 vs 4.35 / 9.24 / 11.07 /
    15.09; size 4.8%.
  - Fisher (1924); Chernoff & Lehmann (1954).
  - Lilliefors (1967): with the table's critical values 0.294 (n = 20) and 0.134 (n = 100), the size is 0.01–0.02%.
    The correct values are 0.192 and 0.089.
  - Durbin (1973).

## Sources

- **Behrens–Fisher.**
  - W. Behrens, *Landwirtsch. Jahrb.* 68 (1929); R. A. Fisher, *Ann. Eugenics* 6 (1935).
  - M. Bartlett, *Proc. Camb. Phil. Soc.* 32 (1936); B. Welch, *Biometrika* 29 (1938), 34 (1947).
  - Y. Linnik, *Statistical Problems with Nuisance Parameters* (1968).
- **Optimal tests.**
  - J. Neyman & E. Pearson, *Phil. Trans. A* 231 (1933), *Stat. Res. Mem.* 1 (1936).
  - G. Dantzig & A. Wald, *Ann. Math. Stat.* 22 (1951); S. Karlin & H. Rubin, *Ann. Math. Stat.* 27 (1956).
  - P. L. Hsu, *Biometrika* 32 (1941); A. Wald, *Ann. Math. Stat.* 13 (1942); E. Lehmann, *Testing Statistical
    Hypotheses* (1959).
  - H. O. Lancaster, *JASA* 56 (1961), mid-p.
- **Likelihood ratios.**
  - S. Wilks, *Ann. Math. Stat.* 9 (1938); H. Chernoff, *Ann. Math. Stat.* 25 (1954); S. Self & K.-Y. Liang, *JASA*
    82 (1987).
  - J. Hartigan, *Proc. Berkeley Conf. in Honor of Neyman and Kiefer* (1985); R. Davies, *Biometrika* 64 (1977).
- **Confidence sets.**
  - J. Neyman, *Phil. Trans. A* 236 (1937); C. Clopper & E. Pearson, *Biometrika* 26 (1934); J. Pratt, *JASA* 56
    (1961).
  - E. Fieller, *J. R. Stat. Soc. Suppl.* 7 (1940), *JRSS B* 16 (1954); L. Gleser & J. Hwang, *Ann. Stat.* 15 (1987).
  - J.-M. Dufour, *Econometrica* 65 (1997); G. Feldman & R. Cousins, *Phys. Rev. D* 57 (1998); C. Bliss, *Ann. Appl.
    Biol.* 22 (1935).
- **Multiplicity, conditioning, evidence and fit.**
  - H. Scheffé, *Biometrika* 40 (1953); R. Marcus, E. Peritz & K. R. Gabriel, *Biometrika* 63 (1976).
  - S. Holm, *Scand. J. Stat.* 6 (1979); G. Hommel, *Biometrika* 75 (1988); H. Finner & K. Strassburger, *Ann. Stat.*
    30 (2002).
  - B. Welch, *Ann. Math. Stat.* 10 (1939); R. Buehler, *Ann. Math. Stat.* 30 (1959); R. Buehler & A. Feddersen,
    *Ann. Math. Stat.* 34 (1963).
  - L. Brown, *Ann. Math. Stat.* 38 (1967); G. Robinson, *Ann. Stat.* 7 (1979).
  - J. Berger & T. Sellke, *JASA* 82 (1987); T. Sellke, M. Bayarri & J. Berger, *Am. Stat.* 55 (2001).
  - R. Wasserstein & N. Lazar, *Am. Stat.* 70 (2016); D. Benjamin et al., *Nat. Hum. Behav.* 2 (2018).
  - K. Pearson, *Phil. Mag.* 50 (1900); R. A. Fisher, *JRSS* 87 (1924); H. Chernoff & E. Lehmann, *Ann. Math. Stat.*
    25 (1954).
  - H. Lilliefors, *JASA* 62 (1967); J. Durbin, *Ann. Stat.* 1 (1973).
- **Books.** E. Lehmann & J. Romano, *Testing Statistical Hypotheses* (4th ed. 2022); J. Shao, *Mathematical
  Statistics* (2nd ed. 2003); M. Schervish, *Theory of Statistics* (1995).

## Problems and solutions

1. **A UMP Poisson test.**
   - T = Σ X_i ~ Poisson(nλ). The family has a monotone likelihood ratio in T, since the ratio is (λ₁/λ₀)^T
     e^{−n(λ₁−λ₀)}.
   - By Karlin–Rubin the UMP test is φ = 1{T > c} + γ 1{T = c}, with P₁(T > c) + γ P₁(T = c) = α under nλ = n.
   - Its power is β(λ) = P_{nλ}(T > c) + γ P_{nλ}(T = c), increasing in λ.
2. **The z test is UMPU.**
   - X̄ ~ N(μ, 1/n) is an exponential family in T = X̄. A UMPU test rejects outside an interval [c₁, c₂], with
     E₀φ = α and E₀[X̄ φ] = α E₀X̄ = 0.
   - The symmetric test φ = 1{|X̄| > z_{α/2}/√n} has size α. Because φ is even and X̄ is symmetric under μ = 0,
     E₀[X̄ φ] = 0.
   - So it satisfies both conditions, and by the generalized Neyman–Pearson lemma it is the UMPU test.
3. **The uniform's non-unique UMP test.**
   - For θ₁ > θ₀ the ratio f_{θ₁}/f_{θ₀} = (θ₀/θ₁)ⁿ on {max ≤ θ₀} and ∞ on {θ₀ < max ≤ θ₁}. So any level-α test that
     rejects whenever max > θ₀ is most powerful.
   - φ = 1{max > θ₀(1 − α)^{1/n}} has P_{θ₀}(max > c) = 1 − (c/θ₀)ⁿ = α, and rejects whenever max > θ₀.
   - So does φ′ = α·1{max ≤ θ₀} + 1{max > θ₀}. For every θ > θ₀ both have power 1 − (1 − α)(θ₀/θ)ⁿ, so both are UMP,
     and they differ.
   - For θ ≤ θ₀ their powers are at most α, since the power is increasing.
4. **Chernoff's mixture.**
   - P(max(0, Z)² = 0) = P(Z ≤ 0) = ½.
   - For t > 0, P(max(0, Z)² > t) = P(Z > √t) = ½ P(Z² > t) = ½ P(χ²₁ > t).
   - Together these say the law is ½δ₀ + ½χ²₁.
5. **Closed testing controls the FWER.**
   - Let T be the set of true nulls. If T is empty there are no false rejections.
   - Otherwise H_T is true, so its local test rejects it with probability at most α.
   - Any false rejection of some H_i, i ∈ T, requires every intersection containing i to be rejected, H_T among them.
     So P(any false rejection) ≤ P(H_T rejected) ≤ α.
6. **The p-value calibration.**
   - Minimize h(ξ) = ξ^{−1} p^{1−ξ} over ξ ∈ (0, 1). Then log h = −log ξ + (1 − ξ) log p, with derivative −1/ξ − log p.
   - The derivative vanishes at ξ* = −1/log p, which lies in (0, 1) exactly when p < 1/e.
   - There h(ξ*) = −log p · p · p^{1/log p} = −log p · p · e = −e p log p.

## Glossary

- **Tests.**
  - Test function; randomized test; size, power, power function; most powerful; Neyman–Pearson lemma; generalized
    lemma: the basics.
  - Monotone likelihood ratio; Karlin–Rubin; UMP; locally most powerful: one-sided optimality.
  - Unbiased test; similar test; Neyman structure; UMPU; conditional test; Fisher's exact test; mid-p: nuisance
    parameters.
  - Group action; invariant test; maximal invariant; UMPI; Hunt–Stein theorem; amenable group; most stringent:
    invariance.
  - Likelihood ratio statistic; Wilks's theorem; χ̄² mixture; non-identifiability under the null; parametric
    bootstrap: large-sample tests.
- **Confidence sets.**
  - Neyman construction; confidence belt; acceptance region; ordering; UMA set; unbiased set; Pratt's identity: from
    tests to sets.
  - Fieller's set; pivot; unbounded confidence set; Gleser–Hwang theorem: impossibility.
  - Physical boundary; flip-flopping; Feldman–Cousins (unified) interval; CLs: bounded parameters.
  - Scheffé's method; familywise error rate; closed testing; Holm, Hommel; partitioning: simultaneous inference.
  - Relevant (recognizable) subset; semi-relevant subset; conditionality: the case in hand.
- **Evidence and fit.**
  - Bayes factor; Berger–Sellke bounds; calibration −e p log p; Lindley's paradox: evidence.
  - Pearson's χ²; degrees of freedom lost to estimation; Lilliefors test; Durbin's process: goodness of fit.

## Where it comes back

- **Part 47**: Wilks's theorem proved; the local power of the score, Wald and LR tests; contiguity.
- **Part 48**: the empirical processes behind Kolmogorov–Smirnov and Durbin's estimated-parameter limit.
- **Part 56**: selective inference: conditioning on the selection event, as chapter 10 conditions on ancillaries.
- **Part 57**: exact distribution-free tests: permutation and conformal.
- **Part 58**: e-values and confidence sequences, valid however long you watch.

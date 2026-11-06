# Statistics, Built — Part 47: Asymptotic Statistics

Part 47 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fifth part of Stage IV, the PhD core.

It opens with Hodges's estimator of 1951: report x̄ unless |x̄| < n^{−1/4}, then 0. At θ = 0 its scaled risk goes to
zero, beating the "information bound", but just beside zero it has a bump of risk that grows like √n. The part asks in
what sense the MLE is best, and answers with Le Cam's and Hájek's theory. On the way it builds the toolkit of large-sample
statistics:
- stochastic orders and the delta method;
- M-estimators and quantiles;
- influence functions and Hadamard derivatives;
- U-statistics and rank statistics.

It then uses the theory on four further subjects:
- the efficiency of tests;
- the bootstrap's second-order accuracy;
- saddlepoints;
- non-regular models.

It keeps three promises:
- **Part 22** stated that the MLE is asymptotically N(θ, I⁻¹/n). Chapters 1–2 prove it for M-estimators, with the
  sandwich under misspecification.
- **Part 45** proved Cramér–Rao for unbiased estimators and warned about Hodges. Chapters 7–9 give LAN, contiguity, and
  the convolution and LAM theorems, which apply to every estimator.
- **Part 16** used the bootstrap on a first-order argument. Chapter 11 proves consistency and second-order accuracy.

**Built in this part:**
- **`statkit.asymptotics`** ([`explainer/stats/kit/asymptotics.py`](../../../explainer/stats/kit/asymptotics.py)),
  tested in `tests/test_stats_kit_asymptotics.py`:
  - Hodges's exact scaled risk, over θ and over local h;
  - the Bahadur remainder;
  - U-statistics and Gini's mean difference with its Hoeffding decomposition;
  - Cauchy local log-likelihood ratios against LAN;
  - Pitman AREs and local power from the third lemma;
  - Daniels's saddlepoint density and Lugannani–Rice tails;
  - the uniform maximum's bootstrap and its m-out-of-n repair.
- **The risk-bump explorer** (`RiskBump` in `explainer/stats/viz.py`), the part's instrument: scaled risk against θ or
  the local parameter h, with the information bound drawn in and the peak of the bump marked.

**Data.**
- From the Museum: Newcomb's passage times of light.
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows, all nominal 90%:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| Student t interval for a mean | Exp(1) data, n = 20 | 87.4% | broken |
| percentile bootstrap for a mean | Exp(1) data, n = 20 | 84.6% | broken |
| bootstrap-t for a mean | Exp(1) data, n = 20 | 88.7% | kept |
| BCa for a mean | Exp(1) data, n = 20 | 84.2% | broken |
| bootstrap interval for a uniform maximum | U(0, θ), n = 200 | 79.8% | broken |
| m-out-of-n bootstrap (m = 40) | U(0, θ), n = 200 | 91.8% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats47.compute   # once (a few minutes)
python tools/build.py stats47 -q l                         # fast 480p preview
python tools/build.py stats47                              # 1080p30 -> renders/stats47.mp4
python tools/qa_scene.py stats47 Hajek
python tools/lecture_length.py stats47 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Hodges's estimator | n·MSE at 0: 0.17 (n = 25), 0.019 (n = 100); local peaks 5.6, 69, 858 at h ≈ n^{1/4} |
| 1 | Stochastic orders and the toolkit | √n log x̄ (Exp): skewness −0.45 (n = 5) → −0.06 (n = 200); n x̄² quantiles vs χ²₁ |
| 2 | M- and Z-estimators | Huber n·Var: sandwich 1.053 vs 1.065; contaminated 1.374 vs 1.378 (mean 3.37); Newcomb 27.38 (SE 0.64) vs 26.21 (1.32) |
| 3 | Quantiles | SD 1.24 vs √(π/2) = 1.253; remainder RMS 0.57 → 0.18 (n = 50 → 5,000) |
| 4 | Influence functions | n·Var(s²): 2.04 vs 2 (normal), 7.75 vs 8 (t₅) |
| 5 | U-statistics | Gini Var: exact 0.074, first order 0.065, simulated 0.073 (n = 10); degenerate n U: mean −0.004, var 2.04 |
| 6 | Rank statistics | power at h = 2: normal 0.62 / 0.61, Laplace 0.63 / 0.73, t₃ 0.71 / 0.83 (t / Wilcoxon) |
| 7 | LAN | Cauchy, h = 1.5: mean −0.562 vs −0.5625, var 1.14 vs 1.125 |
| 8 | Contiguity | n = 100, h = 2: t 0.64, sign 0.46, on the third lemma's curves |
| 9 | Convolution and LAM | Hodges's sup over \|h\| ≤ 1, 2, 4, 8 → 1, 4, 16, 64 |
| 10 | Efficiency of tests | sign/t: 0.637 (normal), 2 (Laplace); Wilcoxon ≥ 0.864; normal scores ≥ 1 |
| 11 | The bootstrap | 90% coverage at n = 10: t 86.5%, percentile 82.7%, BCa 83.5%, bootstrap-t 90.9% |
| 12 | Saddlepoints | mean of 5 Exp: saddlepoint = exact × 1.017; P(X̄ ≥ 2): 0.0293 exact, 0.0127 normal, 0.0293 LR |
| 13 | Non-regular models | bootstrap atom 0.633 (1 − 1/e = 0.632); KS 0.63 vs 0.15 for m-out-of-n |
| 14 | Outro | — |

The rest of the part's numbers, chapter by chapter:
- **Hook.**
  - Exact n·MSE(θ) for n = 25, 100, 1000, 10⁴ over θ ∈ [−0.6, 0.6].
  - Local peaks: 5.58 at h = 2.98 (n = 10²), 68.9 at h = 8.8 (n = 10⁴), 858 at h = 29.7 (n = 10⁶). Each sits near
    n^{1/4}, and the peak grows like √n.
- **Chapter 1.**
  - o_P, O_P, tightness and Prokhorov; Slutsky; continuous mapping.
  - The delta method proved. For √n log x̄ with Exp(1) data:

    | n | Mean | SD | Skewness | KS |
    |---|---|---|---|---|
    | 5 | −0.23 | 1.05 | −0.45 | 0.064 |
    | 20 | −0.12 | 1.01 | −0.24 | 0.034 |
    | 200 | −0.04 | 1.01 | −0.06 | 0.014 |

  - Cramér–Wold and the multivariate delta method; the correlation's variance (1 − ρ²)²/n.
  - The second-order case: 50 x̄² has quantiles 0.46 / 2.73 / 3.88 against χ²₁'s 0.45 / 2.71 / 3.84.
- **Chapter 2.**
  - Consistency from a uniform LLN and a well-separated maximum (Wald 1949). Asymptotic normality with the sandwich
    V⁻¹BV⁻ᵀ.
  - Huber (k = 1.345, n = 50), n·Var:
    - normal errors: sandwich 1.053 vs simulated 1.065, mean 1.012;
    - 0.9 N(0, 1) + 0.1 N(0, 25): 1.374 vs 1.378, mean 3.37.
  - Newcomb (n = 66, minimum −44): mean 26.21 (SE 1.32), Huber 27.38 (sandwich SE 0.64), median 27.
  - Misspecification: Huber (1967), White (1982).
- **Chapter 3.**
  - √n(ξ̂ − ξ) ⇒ N(0, p(1 − p)/f²).
  - Bahadur (1966) with Kiefer's rate.
  - Remainder RMS by n = 50, 200, 1000, 5000: 0.572, 0.418, 0.275, 0.182. Times n^{1/4}: 1.52, 1.57, 1.55, 1.53.
  - The order-statistic interval: [X₍₆₎, X₍₁₅₎] for the median at n = 20 covers 0.959, for any continuous F.
- **Chapter 4.**
  - The von Mises expansion; IFs of the mean, median, Huber and 10% trimmed means.
  - Hadamard differentiability and the functional delta method.
  - The variance functional: μ₄ − σ⁴.
  - The infinitesimal jackknife.
- **Chapter 5.**
  - Gini's mean difference: θ = 2/√π, ζ₁ = 0.1628, ζ₂ = 0.7268.
  - Var U at n = 10, 20, 50: exact 0.0740, 0.0347, 0.0133; first-order 0.0651, 0.0326, 0.0130; simulated 0.0728,
    0.0353, 0.0136.
  - Degenerate h = xy: n U ⇒ χ²₁ − 1.
  - Hájek's projection (1968).
- **Chapter 6.**
  - The signed rank statistic and its projection.
  - Power at n = 30, h = 0…3, normal / Laplace / t₃, as t and Wilcoxon:

    | Errors | Test | h = 0 | h = 1 | h = 2 | h = 3 |
    |---|---|---|---|---|---|
    | normal | t | 0.052 | 0.248 | 0.625 | 0.898 |
    | normal | Wilcoxon | 0.051 | 0.240 | 0.613 | 0.885 |
    | Laplace | t | 0.052 | 0.271 | 0.635 | 0.889 |
    | Laplace | Wilcoxon | 0.052 | 0.334 | 0.729 | 0.941 |
    | t₃ | t | 0.049 | 0.324 | 0.712 | 0.913 |
    | t₃ | Wilcoxon | 0.053 | 0.387 | 0.832 | 0.983 |

  - ARE 0.955 / 1.5 / 1.90, with a minimum of 108/125.
  - Hodges–Lehmann: breakdown 29%.
  - Chernoff–Savage normal scores.
- **Chapter 7.**
  - LAN (Le Cam 1960): the local experiments converge to a Gaussian shift.
  - Cauchy, h = 1.5 (I = ½):
    - n = 25: mean −0.555, var 1.090;
    - n = 400: mean −0.562, var 1.140;
    - the limit: N(−0.5625, 1.125).
  - The score test is asymptotically UMP. QMD; the uniform is not QMD.
- **Chapter 8.**
  - Contiguity; Le Cam's first and third lemmas; fixed alternatives are singular.
  - Local power at n = 100: the t test 0.051, 0.128, 0.261, 0.441, 0.638, 0.807, 0.909, 0.965, 0.990 at h = 0, 0.5,
    …, 4; the sign test 0.045, …, 0.927. Both lie on 1 − Φ(1.645 − τ(h)).
  - The Wald–score–LR trinity.
- **Chapter 9.**
  - Regular estimators and the convolution theorem (Hájek 1970); Anderson's lemma.
  - Hodges is not regular: the limit is δ₋ₕ.
  - The LAM theorem (Hájek 1972).
  - Hodges's worst local risk over |h| ≤ 1, 2, 4, 8:

    | n | \|h\| ≤ 1 | \|h\| ≤ 2 | \|h\| ≤ 4 | \|h\| ≤ 8 |
    |---|---|---|---|---|
    | 10² | 1.08 | 3.87 | 5.58 | 5.58 |
    | 10⁴ | 1.00 | 4.00 | 16.0 | 62.7 |
    | 10⁶ and 10⁸ | 1 | 4 | 16 | 64 |

  - Le Cam's measure-zero theorem (1953); Leeb & Pötscher (2005).
- **Chapter 10.**
  - Pitman efficiency as squared efficacies.
  - The table of AREs against t:
    - sign: 0.637, 0.822, 2.000, 1.62, worst 1/3;
    - Wilcoxon: 0.955, 1.097, 1.500, 1.90, worst 0.864;
    - normal scores: 1.000, 1.047, 1.273, 1.64, worst 1.
  - Sample sizes: a t test with n = 100 against 157 (sign) and 105 (Wilcoxon) for normal data, or 50 and 67 for Laplace
    data.
  - Bahadur slopes: θ² for z, 2 KL for sign. The ratio tends to 2/π as θ → 0 and falls below it further out.
- **Chapter 11.**
  - Bootstrap consistency via Hadamard differentiability (Giné & Zinn 1990).
  - Edgeworth expansions: the bootstrap-t's error is O(n⁻¹) against the normal's O(n^{−1/2}) (Hall 1992).
  - Two-sided 90% coverage for the mean of Exp(1) data:

    | n | Student t | Percentile | Basic | BCa | Bootstrap-t |
    |---|---|---|---|---|---|
    | 10 | 86.5% | 82.7% | 81.3% | 83.5% | 90.9% |
    | 20 | 88.3% | 86.6% | 86.0% | 86.0% | 89.5% |
    | 40 | 88.2% | 87.1% | 86.0% | 87.5% | 89.7% |
    | 80 | 89.1% | 88.7% | 87.5% | 90.1% | 90.9% |

  - Lower-tail misses, nominal 5%: Student 1.1–2.9%, BCa 4.4–4.9%.
- **Chapter 12.**
  - Daniels (1954) for the mean of 5 Exp(1): the saddlepoint is exactly 1.017 × the gamma density (Stirling).
  - Lugannani & Rice (1980). P(X̄ ≥ 2) = 0.0293 exactly; the normal gives 0.0127; Lugannani–Rice gives 0.0293.
  - Uses: rank tests, the saddlepoint bootstrap, p*.
- **Chapter 13.**
  - The uniform maximum: rate n, Exp(1) limit, no LAN.
  - The bootstrap's atom: 1 − (1 − 1/n)ⁿ = 0.633 at n = 200, against the simulated 0.633 (Bickel & Freedman 1981).
  - The m-out-of-n bootstrap (m = 40, n = 2000): atom 0.020, KS 0.15 against 0.63 (Bickel, Götze & van Zwet 1997).
    Subsampling (Politis & Romano 1994).
  - Boundaries (Andrews 2000), unit roots, cube-root asymptotics (Kim & Pollard 1990).

## Sources

- **Superefficiency and the convolution theorem.**
  - J. Hodges (1951, unpublished; reported in Le Cam 1953); L. Le Cam, *Univ. Calif. Publ. Stat.* 1 (1953).
  - L. Le Cam, *Univ. Calif. Publ. Stat.* 3 (1960); J. Hájek, *Z. Wahrsch.* 14 (1970); *Proc. Sixth Berkeley Symp.* 1
    (1972).
  - H. Leeb & B. Pötscher, *Econometric Theory* 21 (2005).
- **M-estimators, quantiles and influence.**
  - A. Wald, *Ann. Math. Stat.* 20 (1949); P. Huber, *Ann. Math. Stat.* 35 (1964); *Proc. Fifth Berkeley Symp.* 1
    (1967); H. White, *Econometrica* 50 (1982).
  - R. Bahadur, *Ann. Math. Stat.* 37 (1966); J. Kiefer, *Ann. Math. Stat.* 38 (1967).
  - R. von Mises, *Ann. Math. Stat.* 18 (1947); F. Hampel, *JASA* 69 (1974).
- **U-statistics and ranks.**
  - W. Hoeffding, *Ann. Math. Stat.* 19 (1948); J. Hájek, *Ann. Math. Stat.* 39 (1968).
  - F. Wilcoxon, *Biometrics Bull.* 1 (1945); J. Hodges & E. Lehmann, *Ann. Math. Stat.* 27 (1956), 34 (1963).
  - H. Chernoff & I. R. Savage, *Ann. Math. Stat.* 29 (1958); J. Hájek & Z. Šidák, *Theory of Rank Tests* (1967).
- **Efficiency of tests.**
  - E. Pitman, lecture notes (1948); R. Bahadur, *Sankhyā* 22 (1960); E. Lehmann, *Nonparametrics* (1975).
- **The bootstrap.**
  - P. Bickel & D. Freedman, *Ann. Stat.* 9 (1981); E. Giné & J. Zinn, *Ann. Probab.* 18 (1990).
  - P. Hall, *The Bootstrap and Edgeworth Expansion* (1992); D. Politis & J. Romano, *Ann. Stat.* 22 (1994).
  - P. Bickel, F. Götze & W. van Zwet, *Stat. Sinica* 7 (1997); D. Andrews, *Econometrica* 68 (2000).
- **Saddlepoints.**
  - H. Daniels, *Ann. Math. Stat.* 25 (1954); R. Lugannani & S. Rice, *Adv. Appl. Probab.* 12 (1980).
  - A. Davison & D. Hinkley, *Biometrika* 75 (1988); O. Barndorff-Nielsen, *Biometrika* 70 (1983).
- **Non-regular rates.** J. Kim & D. Pollard, *Ann. Stat.* 18 (1990).
- **Books.**
  - A. van der Vaart, *Asymptotic Statistics* (1998); L. Le Cam & G. Yang, *Asymptotics in Statistics* (2nd ed. 2000).
  - E. Lehmann, *Elements of Large-Sample Theory* (1999); R. Serfling, *Approximation Theorems of Mathematical
    Statistics* (1980).

## Problems and solutions

1. **Hodges's limits.**
   - At θ = 0, Z = √n x̄ ~ N(0, 1), and T_n = 0 unless |Z| ≥ n^{1/4}. So n E T_n² = E[Z² 1{|Z| ≥ n^{1/4}}] → 0,
     faster than any power of n.
   - At θ ≠ 0, P(|x̄| < n^{−1/4}) ≤ P(|Z| > √n|θ| − n^{1/4}) → 0 exponentially fast, so T_n = x̄ except on a vanishing
     event.
   - Hence n E(T_n − θ)² → E Z² = 1 (the contribution of the event is at most nθ² times an exponentially small
     probability).
2. **The median as a Z-estimator.**
   - ψ(x, θ) = sign(x − θ). Then B = E ψ² = 1, and V = d/dθ E sign(X − θ) = d/dθ [1 − 2F(θ)] = −2f(θ).
   - So V⁻¹BV⁻¹ = 1/(4f(θ)²), the median's variance p(1 − p)/f² at p = ½.
3. **The influence function of a quantile.**
   - Differentiate F_t(ξ_t) = p with F_t = (1 − t)F + tδ_x: −F(ξ) + 1{x ≤ ξ} + f(ξ) ξ̇ = 0 at t = 0.
   - So IF(x) = (p − 1{x ≤ ξ_p})/f(ξ_p), which has mean 0 and E IF² = p(1 − p)/f(ξ_p)².
4. **Gini's projection.**
   - E|x − Y| = ∫(x − y)φ(y)dy over y < x plus ∫(y − x)φ(y)dy over y > x, which equals x(2Φ(x) − 1) + 2φ(x), using
     ∫_{y>x} yφ(y) dy = φ(x).
   - Subtracting θ = 2/√π gives h₁.
5. **The sign test's local power.**
   - T_n = (2/√n) Σ (1{X_i > 0} − ½) is asymptotically N(0, 1) under H₀.
   - Its covariance with Λ_n = h Σ X_i/√n − h²/2 is τ = 2h E[X 1{X > 0}] = 2h φ(0) = h√(2/π).
   - By the third lemma the local power is 1 − Φ(z_α − h√(2/π)). The t test has τ = h, so the Pitman ARE is
     (√(2/π))² = 2/π.
6. **The bootstrap maximum's atom.**
   - M* = M exactly when the largest observation appears at least once among n draws with replacement.
   - So P*(M* = M) = 1 − (1 − 1/n)ⁿ, which tends to 1 − e⁻¹.

## Glossary

- **The toolkit.**
  - o_P, O_P; tightness; Slutsky's lemma; continuous mapping; delta method; Cramér–Wold: the bookkeeping.
  - M-estimator; Z-estimator; uniform law of large numbers; well-separated maximum; sandwich covariance;
    misspecification: estimators as optimizers.
- **Linearizations.**
  - Bahadur representation; order-statistic interval: quantiles.
  - Statistical functional; von Mises expansion; influence function; gross-error sensitivity; Hadamard
    differentiability; functional delta method; infinitesimal jackknife: differentiating statistics.
  - U-statistic; kernel; Hoeffding decomposition; degenerate kernel; Hájek projection: averages over pairs.
  - Signed-rank statistic; score function; normal scores; Hodges–Lehmann estimator: ranks.
- **Le Cam theory.**
  - Local parameter; LAN; Gaussian shift experiment; differentiability in quadratic mean: local structure.
  - Contiguity; Le Cam's first and third lemmas; local power; trinity: alternatives.
  - Regular estimator; convolution theorem; Anderson's lemma; local asymptotic minimax; superefficiency: optimality.
  - Pitman efficiency; efficacy; Bahadur slope; Hodges–Lehmann efficiency: comparing tests.
- **Refinements and failures.**
  - Bootstrap consistency; Edgeworth expansion; pivot; second-order accuracy; bootstrap-t; BCa: the bootstrap.
  - Cumulant generating function; exponential tilting; saddlepoint; Lugannani–Rice; p* formula: saddlepoints.
  - Non-regular model; rate n; m-out-of-n bootstrap; subsampling; cube-root asymptotics: when regularity fails.

## Where it comes back

- **Part 48**: the uniform laws, Donsker classes and bootstrap empirical processes this part used.
- **Part 49**: efficient influence functions in semiparametric models.
- **Part 50**: minimax lower bounds beyond the local scale (Le Cam, Assouad, Fano).
- **Part 53**: Bernstein–von Mises, the Bayesian counterpart of LAN.
- **Part 59**: what survives when p grows with n.

# Statistics, Built — Part 30: Robust Statistics

Part 30 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the tenth part of Stage III, Master's. Part 29 estimated curves on the
assumption that every observation was honest. This part asks what survives when a few are not, or when the tails are
heavier than any model admits:
- efficiency, and the Hodges–Lehmann estimator;
- influence functions and breakdown;
- Huber's minimax M-estimator; robust scale; robust regression (LMS, LTS, S, MM) and covariance (MCD);
- heavy-tailed means (median of means, Catoni).

Its instrument is the estimator rail (`EstimatorRail`): a sample on a number line with one observation on a tracker,
and a marker for each location estimate, recomputed every frame as the point is dragged. Its kit is `statkit.robust`.

It opens with Tukey's (1960) duel between the standard deviation s and the mean absolute deviation d under the
contaminated normal (1 − ε)N(0, 1) + εN(0, 9):
- at ε = 0, ARE(d : s) = 0.876;
- the two break even at ε = 0.0018, one gross error in 570;
- at ε = 0.01 the ratio is 1.44 (1.32 by simulation at n = 100), and at ε = 0.05 it is 2.03.

Then Newcomb's 66 passage times of light (1882; Stigler 1977), with two strays at −44 and −2:

| Estimate | All 66 | Without the strays |
|---|---|---|
| mean | 26.21 [23.57, 28.85] | 27.75 [26.48, 29.02] |
| median | 27.0 [26, 29] | 27.5 |
| 10% trimmed mean | 27.43 | 27.67 |
| Hodges–Lehmann | 27.5 [26.0, 28.5] | 27.5 [26.5, 29.0] |
| Huber (k = 1.345) | 27.38 | 27.66 |
| biweight (c = 4.685) | 27.64 | 27.67 |

None comes near the modern value, 33.02: robustness protects against stray points, not against systematic error. This
is also what Stigler found across 24 historical data sets.

From there the part covers:
- **Pitman efficiency.**
  - The upgrade of Part 16. The sign test's efficacy 4f(0)², ARE 2/π. Wilcoxon's efficacy 12(∫f²)², ARE 3/π,
    derived.
  - The ARE of Wilcoxon to t:

    | Distribution | ARE |
    |---|---|
    | normal | 0.955 |
    | logistic | 1.097 |
    | Laplace | 1.5 |
    | t₃ / t₅ / t₁₀ | 1.90 / 1.24 / 1.05 |
    | 1% / 5% / 10% contaminated | 1.01 / 1.20 / 1.37 |
    | uniform | 1.0 |
    | the parabola | 0.864 |

  - The 0.864 bound by the calculus of variations (Hodges & Lehmann 1956).
  - Normal scores (Chernoff & Savage 1958): 1.000 at the normal, 1.047 logistic, 1.64 at t₃.
  - Estimators inherit their tests' efficiency.
- **Hodges–Lehmann** (1963).
  - Walsh averages; the exact interval from the signed-rank null. For n = 8, the interval is [w₍₄₎, w₍₃₃₎] with 96.1%
    coverage.
  - Darwin's maize: mean 20.9, t interval [0.03, 41.8]; HL 25.0, interval [4.0, 41.5].
- **Influence functions** (Hampel 1974).
  - Sensitivity curves on Newcomb's data, and the estimator rail.
  - Theoretical IFs at the normal: the mean is unbounded; the SD's is quadratic, ½(z² − 1); the median's is
    ±1.253. The 10% trimmed mean is clipped at ±1.60 and Huber at ±1.64; the biweight peaks at 1.77 and is zero beyond
    4.685.
  - The von Mises expansion; Hampel's optimality problem gives Huber's ψ again.
- **Breakdown** (Hampel 1971; Donoho & Huber 1983).
  - Newcomb's clean data with m points set to 1,000. The mean breaks at m = 1, the 10% and 20% trimmed means at 7
    and 13, Hodges–Lehmann at 19 (29.7%), and the median and Huber (MAD scale) at 32 (50%).
  - HL's 1 − 1/√2, derived; explosion and implosion.
  - Maximal bias at 10% contamination: 0.14σ for the median and 0.19σ for Huber. The median is minimax-bias.
- **Huber (1964).**
  - The minimax problem, the least favourable distribution and the clipped ψ, derived. k(ε) = 2.633 / 1.945 / 1.717 /
    1.398 / 1.140 / 0.862 for ε = 0.001 / 0.01 / 0.02 / 0.05 / 0.1 / 0.2, with minimax variances 1.010 … 2.046.
  - Variance against k with a N(0, 10²) contaminant. At 5%, the best k is ≈ 1.5 with variance 1.23, against the
    mean's 5.95 and the median's 1.72.
  - ψ functions (Huber, biweight, Hampel); IRLS; Proposal 2; the weights on Newcomb (−44 gets 0.08 from Huber and 0
    from the biweight).
  - A small Princeton Robustness Study (n = 20, 10,000 samples per distribution), efficiency relative to the best:

    | Estimate | normal | t₃ | 10% contam. | slash | Cauchy | worst |
    |---|---|---|---|---|---|---|
    | mean | 1.00 | 0.56 | 0.75 | 0.00 | 0.00 | 0.00 |
    | median | 0.68 | 0.89 | 0.77 | 1.00 | 1.00 | 0.68 |
    | 10% trimmed | 0.95 | 0.93 | 1.00 | 0.47 | 0.35 | 0.35 |
    | 25% trimmed | 0.84 | 1.00 | 0.95 | 0.99 | 0.88 | 0.84 |
    | Hodges–Lehmann | 0.94 | 0.96 | 0.99 | 0.77 | 0.65 | 0.65 |
    | Huber | 0.94 | 0.96 | 1.00 | 0.79 | 0.66 | 0.66 |
    | biweight | 0.92 | 0.96 | 0.99 | 0.96 | 0.85 | 0.85 |

- **Scale.**
  - The copper data (24 values, one at 28.95): mean 4.28, SD 5.30; median 3.385, MAD 0.526, Qn 0.633, Sn 0.757;
    Huber 3.216.
  - 1-D masking on Newcomb: the 3-SD rule flags −44 (6.5 SD) but not −2 (2.6 SD) until a second pass (4.7 SD). The MAD
    rule flags both at once (16 and 6.5 MADs).
  - Efficiencies at n = 100: MAD 0.36, Sn 0.59, Qn 0.77 (asymptotically 0.37, 0.58, 0.82); M-scales.
- **Robust regression** on the CYG OB1 stars (47 stars, 4 giants):

  | Fit | Intercept | Slope |
  |---|---|---|
  | least squares | 6.79 | −0.41 |
  | Huber M | 6.87 | −0.43 |
  | LMS | −12.74 | 4.00 |
  | LTS (raw) | −13.62 | 4.22 |
  | LTS (reweighted) | −8.50 | 3.05 |
  | MM | −5.02 | 2.26 |

  The reweighted LTS and MM fits match robustbase's `ltsReg` and `lmrob`. LTS flags stars 7, 9, 11, 20, 30 and 34;
  least-squares residuals flag none. GM-estimators and their 1/(p + 1) bound; S-estimators and Hössjer's 33%; MM
  inference.
- **Robust multivariate.** Hawkins–Bradu–Kass (75 × 3, 14 planted outliers):
  - classical distances flag 2 points, not the planted ten (masked at ≈ 2);
  - MCD robust distances (≈ 30–41) flag exactly the 14;
  - the classical and MCD 97.5% ellipses; Stahel–Donoho.
- **Heavy-tailed means.**
  - Median of means, derived (k = 8 log(1/δ)); Catoni's estimator; vector versions.
  - Pareto(2.2), n = 500, 4,000 samples, quantiles of |error|:

    | Estimator | median | 90% | 99% | 99.9% |
    |---|---|---|---|---|
    | mean | 0.055 | 0.134 | 0.312 | 0.813 |
    | 5% trimmed | 0.250 | 0.294 | 0.331 | 0.354 |
    | median of 20 means | 0.087 | 0.165 | 0.223 | 0.261 |
    | Catoni (δ = 0.001) | 0.056 | 0.131 | 0.224 | 0.556 |

    The trimmed mean targets a different functional: the median is 0.37, the mean 0.83.

Data:
- Newcomb (Stigler 1977), the copper in flour (Analytical Methods Committee 1989), the CYG OB1 stars (Humphreys 1978;
  Rousseeuw & Leroy 1987), Hawkins–Bradu–Kass (1984) and Darwin's maize are the Museum's;
- the women's heights are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.robust`** ([`explainer/stats/kit/robust.py`](../../../explainer/stats/kit/robust.py)), checked in
  `tests/test_stats_kit_robust.py`:
  - **Location:** trimmed and winsorized means; Walsh averages, Hodges–Lehmann and its exact interval; the
    signed-rank null; Huber, biweight and Hampel ψ; M-location by IRLS.
  - **Scale:** MAD, Qn, Sn.
  - **Influence and breakdown:** sensitivity curves, influence functions, empirical breakdown.
  - **Efficiency:** Wilcoxon ARE, M-estimator asymptotic variance, Huber's k(ε) and minimax variance.
  - **Regression:** LMS, FAST-LTS with reweighting, M-scale, MM, Huber M.
  - **Multivariate:** FAST-MCD and robust distances.
  - **Heavy tails:** median of means, Catoni.
- **The Museum** gains `newcomb()`, `chem()`, `stars_cyg()` and `hbk()`.
- **The estimator rail** (`EstimatorRail` in `explainer/stats/viz.py`).

The Coverage Board gains six rows. 95% intervals for the World's adult women's mean height (163.01 cm), n = 30, 2,000
samples:

| Method | Setting | Achieved | Mean width (cm) | Verdict |
|---|---|---|---|---|
| t interval | clean | 95.2% | 4.72 | kept |
| Hodges–Lehmann | clean | 95.4% | 4.82 | kept |
| t interval | 10% gross errors ±N(0, 40²) | 96.3% | 9.85 | kept |
| Hodges–Lehmann | 10% gross errors | 95.2% | 5.91 | kept |
| t interval | 10% recorded in inches | 70.1% | 21.8 | broken |
| Hodges–Lehmann | 10% recorded in inches | 87.3% | 13.2 | broken |

A 3-MAD rejection rule followed by a t interval (not a Board row) covers:
- 92.9% on clean data;
- 92.8% with gross errors;
- 94.0% with the inch errors.

## Build it

```bash
python -m videos.stats.stats30.compute         # once (a few minutes)
python tools/build.py stats30 -q l             # fast 480p preview
python tools/build.py stats30                  # 1080p30 -> renders/stats30.mp4
python tools/qa_scene.py stats30 Influence
python tools/lecture_length.py stats30 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Tukey's contamination and Newcomb's light | break-even ε = 0.0018; mean 26.2 vs 27.5 robust vs 33.0 true |
| 1 | Pitman efficiency | 2/π, 3/π, 0.864; normal scores ≥ 1 |
| 2 | Hodges–Lehmann | Newcomb [26.0, 28.5]; Darwin 25.0 [4.0, 41.5] |
| 3 | Influence functions | γ* 1.25 (median), 1.64 (Huber) |
| 4 | Breakdown | 1/64, 7, 13, 19, 32 points; maxbias 0.14σ |
| 5 | Huber's minimax estimator | k(0.05) = 1.398; Princeton worst cases |
| 6 | Robust scale | copper SD 5.30 vs MAD 0.53; Qn 77% efficient |
| 7 | Robust regression | slopes −0.41 vs 3.05 / 2.26 |
| 8 | Robust multivariate | 2 vs 14 flagged |
| 9 | Heavy-tailed means | 99.9% error 0.81 vs 0.26 |
| 10 | Contamination on the World | 70.1% vs 87.3%; HL 40% narrower |
| 11 | Outro | — |

## Sources

- **History.**
  - J. Tukey, in *Contributions to Probability and Statistics* (1960); S. Stigler, *Ann. Stat.* 5 (1977).
  - S. Newcomb, *Astronomical Papers* 2 (1882), *Amer. J. Math.* 8 (1886).
  - B. Peirce, *Astron. J.* 2 (1852); W. Chauvenet, *Manual of Spherical and Practical Astronomy* (1863).
  - J. Arbuthnot, *Phil. Trans.* 27 (1710).
- **Efficiency.**
  - E. Pitman, lecture notes (1948); J. Hodges & E. Lehmann, *Ann. Math. Stat.* 27 (1956), 34 (1963).
  - H. Chernoff & R. Savage, *Ann. Math. Stat.* 29 (1958).
- **Influence and breakdown.**
  - F. Hampel, *Ann. Math. Stat.* 42 (1971), *JASA* 69 (1974).
  - D. Donoho & P. Huber, in *A Festschrift for Erich Lehmann* (1983).
- **M-estimation.**
  - P. Huber, *Ann. Math. Stat.* 35 (1964).
  - D. Andrews, P. Bickel, F. Hampel, P. Huber, W. Rogers & J. Tukey, *Robust Estimates of Location* (1972).
- **Scale.** P. Rousseeuw & C. Croux, *JASA* 88 (1993).
- **Regression.**
  - P. Rousseeuw, *JASA* 79 (1984); P. Rousseeuw & V. Yohai (1984); V. Yohai, *Ann. Stat.* 15 (1987).
  - P. Rousseeuw & K. Van Driessen, *Data Min. Knowl. Disc.* 12 (2006); R. Maronna, O. Bustos & V. Yohai (1979).
  - C. Mallows (1975); O. Hössjer, *Ann. Stat.* 20 (1992).
- **Multivariate.**
  - P. Rousseeuw & K. Van Driessen, *Technometrics* 41 (1999); W. Stahel (1981); D. Donoho (1982).
  - D. Hawkins, D. Bradu & G. Kass, *Technometrics* 26 (1984).
- **Heavy tails.**
  - A. Nemirovski & D. Yudin (1983); M. Jerrum, L. Valiant & V. Vazirani (1986); N. Alon, Y. Matias & M. Szegedy
    (1996).
  - O. Catoni, *Ann. IHP* 48 (2012); G. Lugosi & S. Mendelson, *Found. Comput. Math.* 19 (2019); S. Hopkins, *Ann.
    Stat.* 48 (2020).
- **Data.**
  - Analytical Methods Committee, *Analyst* 114 (1989); R. Humphreys, *Astrophys. J. Suppl.* 38 (1978).
- **Books.**
  - P. Huber & E. Ronchetti, *Robust Statistics* (2nd ed., 2009).
  - F. Hampel, E. Ronchetti, P. Rousseeuw & W. Stahel, *Robust Statistics: The Approach Based on Influence
    Functions* (1986).
  - R. Maronna, D. Martin, V. Yohai & M. Salibián-Barrera, *Robust Statistics* (2nd ed., 2019).
  - P. Rousseeuw & A. Leroy, *Robust Regression and Outlier Detection* (1987).
  - E. Lehmann, *Nonparametrics* (1975).

## Problems and solutions

**1. The Wilcoxon efficacy.**

*Solution.* Write W⁺/(n(n+1)/2) ≈ U = P̂(X_i + X_j > 0), a U-statistic. Under shift θ, μ(θ) = P(X₁ + X₂ + 2θ > 0) =
∫F(x + 2θ) f(x) dx for symmetric f, so μ′(0) = 2∫f². By Hoeffding's projection, Var U ≈ (4/n)Var(F(X)) = 4/(12n) =
1/(3n). The efficacy is μ′(0)²/(1/3) = 12(∫f²)². The t-test's efficacy is 1/σ², so the ARE is 12σ²(∫f²)². At the
normal, ∫φ² = 1/(2√π), giving 12/(4π) = 3/π.

**2. The 0.864 bound.**

*Solution.* The ARE is invariant to scale, so fix σ² = 1 and minimize ∫f² over densities with ∫x²f = 1. With
multipliers, the first variation gives 2f + a + bx² = 0 where f > 0, so f₀ = c(5 − x²)₊ after imposing the
constraints, with c = 3/(20√5). For any admissible f = f₀ + δ: ∫δ = 0 and ∫x²δ = 0. Then
∫f² − ∫f₀² = 2∫f₀δ + ∫δ² ≥ 2∫f₀δ = −2c∫_{|x|>√5}(5 − x²)δ ≥ 0, since there δ = f ≥ 0 and 5 − x² < 0. So
∫f₀² = 3√5/25 is minimal, and the ARE is 12(3√5/25)² = 108/125.

**3. The trimmed mean's influence function.**

*Solution.* With q = F⁻¹(1 − α), the α-trimmed mean of a symmetric F equals its winsorized-type M-functional with ψ the
identity clipped at ±q. Its IF at z is min(max(z, −q), q)/(1 − 2α). It is linear in the middle and constant beyond q,
so γ* = q/(1 − 2α). At the normal with α = 0.1: 1.2816/0.8 = 1.60.

**4. Hodges–Lehmann's breakdown.**

*Solution.* With a share ε of points replaced, a Walsh average (x_i + x_j)/2 is uncontaminated only if both points
are, a share (1 − ε)² of all pairs asymptotically. The median of the Walsh averages stays bounded while that share
exceeds ½. Breakdown occurs at (1 − ε)² = ½, i.e. ε* = 1 − 1/√2 ≈ 0.293.

**5. Huber's least favourable density.**

*Solution.* ∫f₀ = (1 − ε)[(2Φ(k) − 1) + 2φ(k)∫_k^∞ e^{−k(x − k)}dx] = (1 − ε)[1 − 2Φ(−k) + 2φ(k)/k]. Setting this
to 1 gives 2φ(k)/k − 2Φ(−k) = ε/(1 − ε). Its score is −f₀′/f₀ = x on |x| ≤ k and k·sign(x) beyond, Huber's ψ, and
I(F₀) = (1 − ε)(2Φ(k) − 1).

**6. The median-of-means bound.**

*Solution.* Each block has m = n/k points, so by Chebyshev P(|X̄_j − μ| > 2σ/√m) ≤ 1/4. If the median of the k block
means is more than 2σ/√m from μ, at least k/2 blocks are. The number of such blocks is Binomial(k, p) with p ≤ 1/4,
and by Hoeffding P(Bin ≥ k/2) ≤ exp(−2k(1/4)²) = e^{−k/8}. With k = ⌈8 log(1/δ)⌉, the bound holds with probability
at least 1 − δ: |μ̂ − μ| ≤ 2σ√(k/n) = 2σ√(8 log(1/δ)/n) up to rounding.

## Glossary

- **Contaminated normal; gross-error model**: (1 − ε)N + εH, a small share of bad data.
- **Pitman efficiency; efficacy; ARE**: power comparison on shrinking alternatives; signal²/noise per observation;
  the sample-size ratio.
- **Sign test; Wilcoxon signed-rank; normal scores**: rank tests of increasing efficiency.
- **Walsh averages; Hodges–Lehmann estimator; pseudo-median**: pairwise midpoints; their median; its target for
  skewed F.
- **Influence function; sensitivity curve; gross-error sensitivity; von Mises expansion**: the derivative of a
  functional towards a point mass; its sample version; its supremum; the linearization behind asymptotic variance.
- **Breakdown point (finite-sample, asymptotic); explosion and implosion; maximal bias**: the share of bad data
  that ruins an estimate, in either direction for scale; the worst bias below breakdown.
- **M-estimator; ψ; ρ; IRLS; Huber's ψ; redescending (biweight, Hampel); least favourable distribution; minimax**:
  estimating-equation estimators and their theory.
- **MAD; Qn; Sn; M-scale; masking; swamping**: robust scales, and how outliers hide and accuse.
- **Leverage; GM-estimator; LMS; LTS; C-step; S-estimator; MM-estimator**: robust regression and its algorithms.
- **Mahalanobis distance; MCD; robust distance; distance–distance plot; Stahel–Donoho**: robust multivariate
  location and scatter.
- **Median of means; Catoni's estimator; sub-Gaussian deviation; tournament**: heavy-tailed mean estimation.

## Where it comes back

| Idea | Returns in |
|---|---|
| robust PCA and covariance | 31 |
| robust selection, heavy-tailed losses | 32 |
| rank-based conformal prediction | 34 |
| doubly robust estimation | 36 |
| influence functions in semiparametrics | 49 |
| concentration for heavy tails | 51 |
| Bahadur–Savage: no uniform t-interval | 57 |
| robustness in high dimensions; Tukey depth | 60 |
| the Coverage Board | every part; 65 |

# Statistics, Built — Part 23: The Linear Model in Depth

Part 23 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the third part of Stage III, Master's. Part 12 derived least squares under
four quiet assumptions: a linear mean, equal and independent errors, exactly measured predictors, and exact arithmetic.
This part drops each in turn. Each time it asks what the estimator still estimates and how to keep its standard error
honest.

It opens with James Longley's 1967 test of the era's regression programs. His sixteen years of US employment data
have predictors correlated up to 0.995 and variance inflation factors up to 1,789. Against NIST's certified
coefficients:
- the normal equations in single precision get no digit right (Cholesky fails, and four signs are wrong);
- QR in single precision gets 5–6 digits;
- the normal equations in double precision get 7–8;
- QR in double precision gets 11–13.

κ(X) is 4.9 × 10⁹ and κ(X'X) is 2.4 × 10¹⁹. Centring and scaling brings κ down to 111.

From there the part covers:
- **The upgrade.** The sandwich (X'X)⁻¹X'Var(ε)X(X'X)⁻¹ as the frame for everything; the Gauss–Markov proof, and
  where it uses Var ε = σ²I.
- **The general linear hypothesis.**
  - Cβ = d. The F-test is derived as a quadratic form, as two nested fits (Cochran), and in R² form.
  - On 400 of the World's families (standardized heights) the coefficients are 0.326 and 0.344, against a truth of
    0.35 each. Equal parents: F = 0.079, p = 0.78. Both equal to 0.35: p = 0.85. Both zero: F = 61.9.
  - On the fixed family design with 2,000 fresh iid Gaussian response vectors under the null, F rejects 5.3% at 5%.
  - The joint confidence ellipse, and Scheffé's multiplier (1.97 → 2.45).
- **GLS and Aitken (1935).**
  - Whitening by Cholesky; WLS for group means.
  - A trend with AR(1) errors (ρ = 0.8, n = 60, 2,000 series). Slope SDs: OLS 1.99, GLS 1.87, Prais–Winsten 1.89
    (Grenander–Rosenblatt). The naive SE averages only 0.65.
  - Coverage: naive 47.7%, Newey–West 68.2%, FGLS 83.8%, GLS with ρ known 94.8%.
  - Durbin–Watson = 0.380 (OLS residual lag-one estimate 0.815; iterated PW estimate 0.820) for the example, and Cochrane–Orcutt.
- **Heteroskedasticity theory.**
  - Eicker–Huber–White, and testing (Breusch–Pagan) versus always-robust; where uneven noise comes from.
  - Leverage shrinks residuals, which motivates HC1–HC3.
  - With n = 30 and SD ∝ x (4,000 samples), coverage is: classical 76.1%, HC0 81.5%, HC1 82.9%, HC2 86.1%, HC3 90.6%,
    and the wild bootstrap-t 93.4% from 1,000 samples. Formula and bootstrap denominators are recorded separately. Three Board rows.
- **Clustering.**
  - Forty of the World's 400 schools (2,452 pupils); the tutoring programme was assigned by school.
  - The estimate is 27.5 points (truth 20), with iid SE 3.65 against CR1 SE 10.04.
  - Moulton's equal-size exchangeable approximation gives 1 + (61.3 − 1) × 1 × 0.114 = 7.9 and SE ratio 2.81; the observed ratio is 2.75. Unequal sizes and SES adjustment make this a heuristic.
  - CR1; few clusters; the restricted wild cluster bootstrap with Webb weights; which level to cluster at, two-way
    clustering, and random intercepts as GLS. Four Board rows.
- **Models as approximations** (Buja et al. 2019).
  - The best linear predictor β*. The World's income–age BLP slope is $274 a year, but $1,150 for adults aged 18–40 inclusive.
  - A quadratic truth with x random: the classical SE covers 61%, HC3 94%.
  - Residual, pairs and wild bootstraps.
- **Errors in variables.**
  - Attenuation λ = σ²ₓ/(σ²ₓ + σ²ᵤ). The World's fathers with reliability 0.6: the slope falls from 0.365 to 0.216
    (predicted 0.235). The naive CI covers 0.4%.
  - Hubble's 24 nebulae: velocity on distance 454, reverse regression 729, Deming 582 km/s/Mpc. Today's H₀ is about
    70: a calibration error that no regression fixes.
  - SIMEX gives 0.312; errors in y; the cures.
- **Quantile regression** (Koenker & Bassett 1978).
  - 1,000 of the World's working adults: income-on-age slopes of 0.22, 0.27, 0.47, 0.63 and 1.14 thousand a year at
    τ = 0.1–0.9, against 0.41 for OLS.
  - Kernel-bread, empirical-score sandwich SEs are compared with 100 pairs-bootstrap refits per quantile; agreement is approximate, with a notable difference at τ = 0.1. The median's slope (SE 0.082) is more precise than the mean's (0.134).
  - The location–scale fan, quantile treatment effects, and Engel's law (0.40 to 0.69).
- **Splines and bases.**
  - Truncated powers against B-splines (κ 3.2 × 10⁷ vs 5.7); the B-splines' partition of unity.
  - Log income on age with 1, 3, 6 and 20 knots. Each CV fold learns its distinct interior knots from training predictors only. Ten-fold CV is flat (minimum at 8 requested knots); the heuristic one-SE rule chooses 0.
  - Interactions and tensor products; natural splines.
- **Numerics.**
  - Householder's mirror and the column-by-column triangularization.
  - Cholesky against QR against SVD, and Givens updating.
  - Backward stability and worst-case forward sensitivity. The seeded digits experiment uses a 90-digit least-squares reference for the exact supplied binary64 inputs, including nonzero-residual cases. One- and two-digit-per-power lines are guides, not universal predictions; failed normal-equation solves are recorded and score zero.
- **Influence.**
  - Leverage as Mahalanobis distance; the deletion formula; DFBETAS. Hubble's most influential nebula (2 Mpc,
    500 km/s): the slope goes 454 → 504 without it.
  - The jackknife SE is 80.5, against 75.3 classical and 82.3 HC3.
  - Masking: three clustered outliers each have Cook's D < 1. Deleting one moves the slope −0.07 → −0.01; deleting all
    three gives 0.46.

Every number on screen is computed in [`compute.py`](compute.py):
- Longley's data, NIST's certified values and Hubble's nebulae are the Museum's;
- families, incomes and schools are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.ols` II** ([`explainer/stats/kit/ols.py`](../../../../explainer/stats/kit/ols.py)), checked in
  `tests/test_stats_kit_ols2.py`:
  - normal equations and QR in any precision, and correct digits;
  - Householder QR written out;
  - the general linear hypothesis;
  - GLS, AR(1) covariance and Prais–Winsten, and Newey–West;
  - cluster-robust covariance, Moulton's factor, the ICC, and the restricted wild (cluster) bootstrap with
    Rademacher or Webb weights;
  - Deming and total least squares;
  - DFBETAS and jackknife coefficients;
  - truncated-power and B-spline bases;
  - quantile-regression sandwich SEs.
- **The digits board** (`DigitsBoard` in `explainer/stats/viz.py`): correct digits per coefficient per method.
- **The World**: the `schools` block, with 400 schools, about 24,000 pupils, a school-level programme
  (`SCHOOL_PROGRAMME_EFFECT` = 0.20 SD), school effects (SD 0.35) and SES. It is reused in Parts 25 and 26.
- **The Museum**: `longley()`, `LONGLEY_CERTIFIED`, and `HUBBLE_1929` / `hubble()`.

The Coverage Board gains eight rows:

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| iid SE, school programme | 40 schools, pupils clustered | 1,000 | 49.1% | broken |
| cluster-robust SE (CR1) | 40 schools | 1,000 | 95.1% | kept |
| cluster-robust SE (CR1) | 8 schools, both arms observed, t₇ | 500 | 88.6% | broken |
| wild cluster bootstrap | 8 schools, both arms observed, Webb weights | 500 | 96.0% | kept |
| naive slope, noisy regressor | reliability 0.6, n = 500 | 1,000 | 0.4% | broken |
| HC0 SE | heteroskedastic, n = 30 | 1,000 | 81.1% | broken |
| HC3 SE | heteroskedastic, n = 30 | 1,000 | 90.0% | broken |
| wild bootstrap-t | heteroskedastic, n = 30 | 1,000 | 94.4% | kept |

## Build it

```bash
python -m videos.stats.stats23.compute         # once (about two minutes; cached in .cache/stats23)
python tools/build.py stats23 -q l             # fast 480p preview
python tools/build.py stats23                  # 1080p30 -> renders/stats23.mp4
python tools/qa_scene.py stats23 Cluster
python tools/lecture_length.py stats23 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Longley's test, 1967 | digits 0 / 5–6 / 7–8 / 11–13; κ 4.9e9, κ(X'X) 2.4e19; scaled κ 111 |
| 1 | Upgrade: what Part 12 assumed | the sandwich; Gauss–Markov's use of σ²I |
| 2 | The general linear hypothesis | 0.326, 0.344; F 0.079 (p 0.78), 0.162 (p 0.85), 61.9; conditional Gaussian null rejection 5.3%; Scheffé 2.45 |
| 3 | GLS and Aitken | SD 1.99 / 1.87 / 1.89; naive SE 0.65; coverage 47.7 / 68.2 / 83.8 / 94.8%; DW 0.380 |
| 4 | Heteroskedasticity theory | coverage 76.1 → 90.6 (HC3), wild 93.4%; Board 81.1 / 90.0 / 94.4% |
| 5 | Clustering | 27.5 (truth 20); SE 3.65 vs 10.04; Moulton 7.9, ratio 2.75; Board 49.1 / 95.1 / 88.6 / 96.0% |
| 6 | Models as approximations | BLP 0.27 vs 1.15 (ages 18–40); toy 61% vs 94% |
| 7 | Errors in variables | 0.365 → 0.216 (pred. 0.235); Board 0.4%; Hubble 454 / 729 / 582; SIMEX 0.312 |
| 8 | Quantile regression | slopes 0.22 → 1.14; SEs 0.06 → 0.32; Engel 0.40–0.69 |
| 9 | Splines and bases | κ 3.2e7 vs 5.7; CV flat, min 8 knots |
| 10 | Numerics | digits vs κ: slopes −1 (QR) and −2 (normal equations) |
| 11 | Influence | 454 → 504; jackknife 80.5, HC3 82.3; masking −0.07 → −0.01 → 0.46 |
| 12 | Outro | — |

## Sources

- **History.**
  - J. Longley, *JASA* 62 (1967); NIST Statistical Reference Datasets, "Longley".
  - E. Hubble, *PNAS* 15 (1929).
  - A. Aitken, *Proc. Roy. Soc. Edinburgh* 55 (1935).
  - A. Householder, *J. ACM* 5 (1958); G. Golub, *Numer. Math.* 7 (1965).
- **Methods.**
  - H. Scheffé, *Biometrika* 40 (1953); U. Grenander & M. Rosenblatt (1957).
  - D. Cochrane & G. Orcutt, *JASA* 44 (1949); S. Prais & C. Winsten (1954); J. Durbin & G. Watson, *Biometrika* 37
    (1950).
  - F. Eicker, *Ann. Math. Stat.* 34 (1963); H. White, *Econometrica* 48 (1980); J. MacKinnon & H. White, *J.
    Econometrics* 29 (1985); T. Breusch & A. Pagan, *Econometrica* 47 (1979); R. Koenker, *J. Econometrics* 17 (1981), studentized test; W. Newey & K. West, *Econometrica* 55
    (1987).
  - B. Moulton, *J. Econometrics* 32 (1986); K.-Y. Liang & S. Zeger, *Biometrika* 73 (1986); M. Arellano, *Oxford
    BES* 49 (1987).
  - A. C. Cameron, J. Gelbach & D. Miller, *REStat* 90 (2008) and *JBES* 29 (2011); M. Webb, Queen's WP 1315
    (2014); A. Abadie, S. Athey, G. Imbens & J. Wooldridge, *QJE* 138 (2023).
  - A. Buja et al., *Stat. Sci.* 34 (2019); D. Freedman, *Ann. Stat.* 9 (1981).
  - J. Cook & L. Stefanski, *JASA* 89 (1994); W. E. Deming, *Statistical Adjustment of Data* (1943).
  - R. Koenker & G. Bassett, *Econometrica* 46 (1978); J. Powell (1991); V. Chernozhukov, I. Fernández-Val & A.
    Galichon, *Econometrica* 78 (2010).
  - C. de Boor, *J. Approx. Theory* 6 (1972); D. Belsley, E. Kuh & R. Welsch, *Regression Diagnostics* (1980).
- **Books.**
  - S. Weisberg, *Applied Linear Regression* (4th ed., 2014).
  - A. C. Cameron & P. K. Trivedi, *Microeconometrics* (2005).
  - R. Koenker, *Quantile Regression* (2005).
  - G. Golub & C. Van Loan, *Matrix Computations* (4th ed., 2013).

## Problems and solutions

**1. Two forms of F.**

*Solution.* Assume X has full column rank, n > p, and C has q independent rows. The restricted estimator is β̃ = β̂ − (X'X)⁻¹C'[C(X'X)⁻¹C']⁻¹(Cβ̂ − d), by Lagrange. Then
y − Xβ̃ = e + X(β̂ − β̃), with X'e = 0, so RSS₀ = RSS + (β̂ − β̃)'X'X(β̂ − β̃). Substituting,
(β̂ − β̃)'X'X(β̂ − β̃) = (Cβ̂ − d)'[C(X'X)⁻¹C']⁻¹(Cβ̂ − d) = Q. Dividing by qs² gives the same F.

**2. Moulton's factor.**

*Solution.* Take clusters of size m with Var ε = σ²[(1 − ρ)I + ρ11'] within each cluster, and a regressor x constant
within clusters.
- **The iid variance.** Var(β̂) = σ²/Σ(x − x̄)².
- **The true variance.** With x constant within a cluster, the slope's numerator Σᵢ(xᵢ − x̄)εᵢ is a sum over clusters
  of (x_g − x̄) times the cluster's error sum, and Var(Σᵢ∈g εᵢ) = mσ²(1 + (m − 1)ρ). So
  Var(β̂) = σ²(1 + (m − 1)ρ)/Σᵢ(xᵢ − x̄)².
- **The ratio.** 1 + (m − 1)ρ. The familiar extension multiplying by a regressor ICC is an approximation under suitable exchangeability and balance; it is not exact for arbitrary adjusted designs or unequal cluster sizes.

**3. Attenuation.**

*Solution.* In a simple linear conditional-mean model with finite variances and mean-zero independent classical measurement error, β̂_w → Cov(w, y)/Var(w) = Cov(x + u, α + βx + ε)/(σ²ₓ + σ²ᵤ) = βσ²ₓ/(σ²ₓ + σ²ᵤ) = βλ. The intercept
converges to ȳ − βλ x̄ = α + β(1 − λ)μₓ: it absorbs what the slope lost, so it is biased unless μₓ = 0.

**4. Residual variances.**

*Solution.* With a correct mean E(ε | X) = 0, full-rank X, and hᵢᵢ < 1, e = (I − H)ε with H = X(X'X)⁻¹X' symmetric and idempotent. Under Var ε = σ²I,
Var e = σ²(I − H)(I − H)' = σ²(I − H), so E eᵢ² = σ²(1 − hᵢᵢ). Hence eᵢ²/(1 − hᵢᵢ) has expectation σ², and the HC2
meat Σ eᵢ²xᵢxᵢ'/(1 − hᵢᵢ) has expectation σ²X'X, so the HC2 covariance estimator is unbiased for the classical covariance. This does not imply exact t coverage.

**5. The deletion formula.**

*Solution.* Assume the design remains full rank after deletion (hᵢᵢ < 1). Write A = X'X. Sherman–Morrison gives (A − xᵢxᵢ')⁻¹ = A⁻¹ + A⁻¹xᵢxᵢ'A⁻¹/(1 − hᵢᵢ). Then
β̂₍ᵢ₎ = (A − xᵢxᵢ')⁻¹(X'y − xᵢyᵢ). Expanding and using xᵢ'β̂ = yᵢ − eᵢ, we get
β̂₍ᵢ₎ = β̂ − A⁻¹xᵢeᵢ/(1 − hᵢᵢ).

**6. The best linear predictor of x².**

*Solution.* With x ~ N(0, 1) and y = x², β* = (E xx')⁻¹E xy with x = (1, x)'. E xx' = I, and E xy = (E x², E x³) =
(1, 0), so β* = (1, 0): a flat line at 1. The residual is r = x² − 1.
- **The true variance of the OLS slope.** About E[x²r²]/(n (E x²)²) = E[x²(x² − 1)²]/n = (15 − 6 + 1)/n = 10/n.
- **The classical variance.** About E[r²]/(n E x²) = 2/n.
- **The consequence.** The classical SE is √5 ≈ 2.2 times too small. A nominal ±1.96 SE interval is then really ±0.88
  true SEs, which covers about 62%; the simulation, which adds independent noise of variance 0.09, gave 61%. With that noise the asymptotic variances are 10.09/n and 2.09/n; the displayed analytic toy is the noiseless limit.

## Glossary

- **Condition number κ; machine epsilon; backward stability**: σ_max/σ_min; the relative rounding unit; the exact
  answer to a nearby problem.
- **Normal equations; Cholesky; Householder QR; Givens rotation; SVD**: X'Xb = X'y; LL' factorization; orthogonal
  reflections to triangular form; plane rotations for updating; the singular value decomposition.
- **General linear hypothesis; F-test; Scheffé intervals**: Cβ = d; the quadratic form over qs²; simultaneous
  intervals for every contrast in a specified coefficient subspace.
- **GLS; WLS; whitening; FGLS; Prais–Winsten; Cochrane–Orcutt; Durbin–Watson**: least squares after undoing a known
  covariance; the diagonal case; multiplying by L⁻¹; with an estimated covariance; AR(1) recipes; the lag-one test.
- **Heteroskedasticity-consistent SEs (HC0–HC3); leverage; wild bootstrap**: sandwich meats from squared residuals,
  with leverage corrections; hᵢᵢ; resampling by flipping residuals.
- **Cluster-robust SE (CR1); Moulton factor; ICC; wild cluster bootstrap; Webb weights**: sums of scores within
  clusters; the variance inflation 1 + (m − 1)ρₓρ_ε; the within-cluster correlation; flipping whole clusters' residuals;
  a six-point weight distribution.
- **Best linear predictor; models as approximations; pairs bootstrap**: the population least squares line; inference
  for β* under a wrong model; resampling (x, y) together.
- **Errors in variables; reliability; attenuation; Deming regression; total least squares; SIMEX**: noisy
  predictors; σ²ₓ/Var(w); the slope's shrinkage; fitting with both error variances; orthogonal fitting; simulate and
  extrapolate.
- **Quantile regression; check loss; sparsity; quantile treatment effect**: modelling F⁻¹(τ | x); ρ_τ; the inverse density
  at the quantile; shifts in a distribution's quantiles.
- **Basis expansion; B-spline; truncated power basis; natural spline; tensor product**: curves as linear models;
  de Boor's local bumps; (x − k)₊³; linear beyond the boundary; products of bases.
- **DFBETAS; Cook's distance; masking; jackknife**: deletion changes in SEs; their summary; outliers hiding each
  other; leave-one-out variance.

## Where it comes back

| Idea | Returns in |
|---|---|
| GEE and working correlations | 24 |
| random intercepts: the clusters modelled | 25 |
| penalized splines and smoothing parameters | 29 |
| robust regression; influence functions | 30 |
| the lasso when p > n | 32 |
| difference-in-differences with few clusters | 37 |
| measurement error in full | 41 |
| minimum-norm interpolation | 59 |
| the Coverage Board | every part; 65 |


## QA clarifications

- Exact Gaussian F theory conditions on a full-rank design with errors N(0, σ²I). The null histogram uses fresh Gaussian responses, not an exact-null claim about repeated finite-World samples. Centered Pythagorean and R² decompositions additionally use common-intercept nested subspaces; the RSS-difference identity also covers affine restrictions.
- The school effect is +20 score points. Eight-school studies condition on both programme arms being present (two one-arm samples were redrawn before fitting). Sampling forty of the finite World's 400 schools targets the structural effect in a fixed simulated population; these Monte Carlo results are not a universal superpopulation guarantee.
- Restricted wild-bootstrap p-values use (1 + extreme draws)/(B + 1), with numerical equality tolerance for tied sign patterns. Sufficient-statistic computation is checked against observation-level refits. This Monte Carlo correction does not make few-cluster inference exact.
- Iterated Prais–Winsten is constrained to |ρ| ≤ 0.999 to keep the stated stationary model well defined; the seeded study required zero constrained updates. OLS residual autocorrelation and iterated PW correlation are reported separately.
- Quantile sparsity is 1/f. A possibly misspecified linear quantile fit uses empirical score meat E[xx′(τ − 1{e < 0})²], rather than assuming τ(1 − τ)E[xx′]. Kernel density estimation and ties require regularity; bootstrap results from only 100 draws have appreciable Monte Carlo uncertainty.
- Population quantile equivariance does not imply nonlinear-transformation equivariance of finite parametric refits. A quantile treatment coefficient is a conditional contrast; causal and marginal interpretations need additional identification and modelling assumptions. Positive Engel intercepts, rather than slopes below one alone, imply declining fitted food shares.
- Natural cubic splines with J interior knots and two boundary knots have J + 2 columns including the intercept: two boundary second-derivative constraints reduce the unrestricted cubic dimension J + 4. CV uses distinct training-only knots and records effective counts; the fold-SE rule is a correlated-fold heuristic.
- Numerical condition numbers are sensitivity bounds, not observed digit counts. A good Longley R² alone does not suppress κ² residual sensitivity. The mathematical κ(X′X) = κ(X)² and the condition estimate of the rounded Gram matrix are stored separately. Accuracy is compared against certified or independent high-precision answers.
- Classical attenuation requires independent measurement error in a single regressor. The father simulation calibrates error variance to the actual finite-World predictor variance. Hubble's Deming error ratio is an illustrative homoskedastic calibration at mean distance, not a validated error model; slopes cannot identify a shared distance-calibration error.
- Leverage-resistant fitting differs from residual-robust fitting. DFBETAS uses deleted residual scale with the full-design inverse-Gram factor; HC3 and the jackknife also differ by centering and a finite-sample factor.

# Statistics, Built — Part 25: Borrowing Strength: Shrinkage and Mixed Models

Part 25 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fifth part of Stage III, Master's. Part 15 shrank one estimate towards a
prior someone chose. This part estimates many related things at once and lets the data choose the prior. James–Stein,
empirical Bayes, random effects and REML turn out to be one idea seen four ways: borrowing strength.

It opens with Bradley Efron and Carl Morris's eighteen major-league hitters after their first 45 at-bats of 1970
(recomputed from their table):
- Each player's own average has a total squared error of 0.0753 against his average over the rest of the season.
- James–Stein keeps 21% of each distance on an approximately unit-variance arcsine scale (B̂ = 0.791; back-transformed target .263). Its held-out probability-scale SSE is 0.0215:
  3.5 times smaller, and closer for 15 of the 18.

From there the part covers:
- **James–Stein.**
  - The estimator; why the squared length of X is too large on average (E‖X‖² = ‖θ‖² + p).
  - Stein's lemma and SURE, derived, giving risk p − (p − 2)²E‖X‖⁻² < p for every θ.
  - Simulated risk for p = 10: 2.02 at θ = 0 (positive part 1.28) against the MLE's 10, rising towards 10 as ‖θ‖ grows.
  - The positive-part estimator, the choice of target, and admissibility (Part 45).
- **Empirical Bayes.**
  - The upgrade card from Part 15.
  - For p > 3 the untruncated ratio (p − 3)/Σ(xᵢ − x̄)² is unbiased for B under the normal hierarchy, so James–Stein is empirical Bayes (Efron & Morris 1973).
  - Robbins (1956); Tweedie's formula E(θ | x) = x + σ² d log f(x)/dx (Efron 2011).
  - 1,000 z-scores, 90% true nulls. A finite-grid EM approximation puts 89% near 0 with fitted nonnull clumps. The generating prior is 0.9 δ₀ + 0.1 N(0, 3²).
  - The ten largest z average 5.61; their true effects average 5.07 (the winner's curse); Tweedie's estimates average 4.84.
- **Random effects.**
  - Variance components (Fisher 1918); the ICC; the ANOVA estimator and its flaws.
  - All 24,157 of the World's pupils: τ̂² = 1,732 (SD 42), σ̂² = 7,872 (SD 89), ICC 0.180.
  - For unequal fixed school sizes, m* = Σm²/Σm = 61.089. The fitted common-ICC design effect for the unweighted pupil mean is 11.839, giving effective n = 2,040 for this mean.
- **The linear mixed model.**
  - V = ZGZ′ + R and GLS; Henderson's mixed-model equations as a ridge penalty; the BLUP and its shrinkage factor.
  - 40 schools:

    | Estimate | Programme | SE | SES | SE |
    |---|---|---|---|---|
    | OLS, pupils independent | 33.9 | 3.8 | 29.0 | 1.84 |
    | mixed model, REML | 32.5 | 12.1 | 27.1 | 1.91 |

  - Shrinkage factors 0.90–0.94 with 50–82 pupils a school. The one-fit MSE against centered realized school-plus-context deviations falls from 101 to 93.
  - Prediction for a new pupil in a new school. The simple (1 − λ)τ² error variance assumes beta and covariance components known; estimating them adds uncertainty.
- **ML vs REML.**
  - The downward bias of ML; error contrasts and the restricted likelihood (Patterson & Thompson 1971).
  - 300 data sets per setting, normal-plus-Bernoulli intercept mixture variance 0.2725; Gaussian working likelihood:

    | Groups | ML | REML | ML gives τ̂² < 10⁻⁶ |
    |---|---|---|---|
    | 5 | 0.143 | 0.289 | 28% |
    | 10 | 0.206 | 0.282 | |
    | 40 | 0.245 | 0.263 | |

  - When to use which.
- **Inference.**
  - Satterthwaite and Kenward–Roger degrees of freedom; two Board rows.
  - The boundary: ½χ²₀ + ½χ²₁ (Self & Liang 1987). In 1,000 null data sets the LR is numerically near 0 (tolerance 10⁻⁶) in 57.8%. The χ²₁ cut-off
    3.84 rejects 2.2%; the mixture's 2.71 rejects 3.3%.
  - Profile-likelihood intervals for variances; advice.
- **Longitudinal data.**
  - 60 simulated children measured at 4, 6, 8, 10 and 12; random intercepts and slopes (Laird & Ware 1982).
  - Growth 5.67 cm a year. Its SE is 0.045 with random intercepts only and 0.081 with random slopes. LR 149.
  - Spreads 5.2 and 0.59, against the simulation's 5.5 and 0.6.
  - BLUP lines; compound symmetry, AR(1), unstructured covariances; missing visits under MAR.
- **Nested and crossed.**
  - Separate two-stage fits give town variance 49 and school-mean residual variance 1,820. These are not a joint three-level decomposition; residuals include pupil-mean noise. No calibrated town-variance test was computed.
  - Gelman & Hill's radon and group-level predictors.
  - Essays crossed with raters, each essay read by 2 of 8 raters. Rater severities are recovered (correlation 0.98).
  - Essay MSE: raw mean 0.203, essays random only 0.167, crossed 0.124.
  - lme4's formula notation.
- **Fixed or random.**
  - Within against between: 400 schools' between slope is 39.8, the within slope 29.2.
  - Mundlak's model (1978): under common within-group variance with all relevant group means included, the within coefficient equals fixed effects; the contextual effect is 10.6 (SE 4.1),
    against the World's 30 and 15.
  - Hausman (1978): H = 6.56, p = 0.010.
  - When to use which.
- **GLMMs.**
  - The integral; PQL (Breslow & Clayton 1993); Laplace and adaptive Gauss–Hermite, drawn on one school.
  - 40 schools, passing 550: programme 0.438 (SE 0.248), school SD 0.705 by Laplace; AGQ(10) agrees to three decimals.
  - GEE's marginal 0.405. The ratio 1.082 against √(1 + 0.346 s²) = 1.083.
  - **The World's hospital league table.** 60 hospitals with 17–877 operations, average death rate 4.1%. The raw top
    five are led by two hospitals of 19 operations (15.8% and 10.5%), and 1 of the five is truly among the ten worst.
    The shrunk top five all have 205 or more operations, and 2 are truly among the worst. The shrunk rates' MSE is 7.4
    times smaller, yet rank correlations with the truth are only 0.21 (raw) and 0.38 (shrunk): report intervals for
    ranks (Goldstein & Spiegelhalter 1996).
- **Small areas.**
  - A survey of 2,000 adults for 200 towns (median 4 respondents). Direct means range from 11 to 133 thousand while the
    truths lie between 46 and 61.
  - Fay–Herriot (1979); the EBLUP; Prasad–Rao MSE. Â = 9.0; γ median 0.03, largest 0.76 (385 respondents).
  - MSE: direct 383, synthetic 20.1, EBLUP 20.6.
  - SAIPE, benchmarking, unit-level models.
- **Meta-analysis.**
  - Common and random effects; DerSimonian–Laird (1986).
  - Five simulated trials: common effect 0.114 ± 0.124. Random effects 0.137, DL [−0.13, 0.40], HK [−0.22, 0.50];
    the truth is 0.3.
  - Q = 17.1 on 4 df; τ̂ = 0.26 (truth 0.15); I² = 0.77; prediction intervals.
  - Shrunk study effects (factors 0.63–0.85); Hartung–Knapp; two Board rows; publication bias.
- **Item response theory.**
  - Rasch (1960) as a GLMM; given fixed item parameters and local independence, the same-item raw score is sufficient; 2PL.
  - 200 persons × 15 items: difficulties correlate 0.987 with the truth (SE about 0.18); σ̂ = 0.99.
  - Known-item information peaks at 2.9 (asymptotic likelihood SE 0.59). Fitted conditional ability modes use same-item raw scores, correlating 0.86
    with the truth.
  - PISA, adaptive testing, equating, AI benchmarks (Part 64).

Every number on screen is computed in [`compute.py`](compute.py):
- the hitters are the Museum's;
- schools, towns, incomes and hospitals are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.shrink`** ([`explainer/stats/kit/shrink.py`](../../../../explainer/stats/kit/shrink.py)):
  - James–Stein (towards 0 or the mean, positive part), SURE and Monte Carlo risk (the legacy helper name includes “exact”);
  - normal empirical Bayes;
  - the NPMLE of a prior by EM on a grid, and Tweedie's formula;
  - Fay–Herriot;
  - random-effects meta-analysis (DL, I², Hartung–Knapp).
- **`statkit.mixed`** ([`explainer/stats/kit/mixed.py`](../../../../explainer/stats/kit/mixed.py)), checked against
  statsmodels in `tests/test_stats_kit_mixed.py`:
  - `lmm`: random intercepts and slopes by ML or REML, with per-group Woodbury algebra, BLUPs and ICC;
  - `satterthwaite` degrees of freedom;
  - `vc_lmm`: variance components for crossed or nested factors;
  - `glmm_logit`: Laplace and adaptive Gauss–Hermite.
- **The shrinkage plot** (`ShrinkagePlot` in `explainer/stats/viz.py`): raw estimates, shrunk estimates and truths on
  three lines, with arrows between them.
- **The World**: the `hospitals` block, 60 hospitals' volumes, true death probabilities and deaths.
- **The Museum**: `EFRON_MORRIS` and `efron_morris()`.

The Coverage Board gains four rows:

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| DerSimonian–Laird, z | 5 studies, τ = 0.15 | 1,000 | 89.3% | broken |
| Hartung–Knapp, t₄ | 5 studies, τ = 0.15 | 1,000 | 94.1% | kept |
| mixed model, z interval | 8 schools, effect between schools | 400 | 89.0% | broken |
| mixed model, Satterthwaite t | 8 schools, effect between schools | 400 | 94.0% | kept |

## Build it

```bash
python -m videos.stats.stats25.compute         # once (a few minutes; cached in .cache/stats25)
python tools/build.py stats25 -q l             # fast 480p preview
python tools/build.py stats25                  # 1080p30 -> renders/stats25.mp4
python tools/qa_scene.py stats25 GLMM
python tools/lecture_length.py stats25 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Eighteen hitters, 1970 | SSE 0.0753 vs 0.0215 (3.5×); closer for 15 of 18; B̂ 0.791 |
| 1 | James–Stein | risk 2.02 (positive part 1.28) vs 10 at θ = 0 |
| 2 | Empirical Bayes | NPMLE 89% at 0; top ten 5.61 / 5.07 / 4.84 |
| 3 | Random effects | τ̂² 1,732, σ̂² 7,872, ICC 0.180; mean-specific unequal-size deff 11.84 |
| 4 | The linear mixed model | programme SE 3.8 → 12.1; MSE 101 → 93 |
| 5 | ML vs REML | 5 groups: 0.143 vs 0.289 (truth 0.2725); 28% zeros |
| 6 | Inference | Board 89 / 94%; zeros 57.8%; rejects 2.2% vs 3.3% |
| 7 | Longitudinal data | 5.67 cm/yr; SE 0.045 → 0.081; LR 149 |
| 8 | Nested and crossed | two-stage town variance 49; raters r = 0.98; MSE 0.203 / 0.167 / 0.124 |
| 9 | Fixed or random? | between 39.8, within 29.2; context 10.6 (4.1); Hausman 6.56, p 0.010 |
| 10 | GLMMs | 0.438 (0.248), s 0.705; ratio 1.082 vs 1.083; league 1 vs 2 of 5; MSE ÷7.4; ranks 0.21 / 0.38 |
| 11 | Small areas | MSE 383 / 20.1 / 20.6; Â 9.0; γ median 0.03 |
| 12 | Meta-analysis | 0.137 [−0.13, 0.40] vs [−0.22, 0.50]; I² 0.77; Board 89.3 / 94.1% |
| 13 | Item response theory | r 0.987; σ̂ 0.99; information 2.9; ability r 0.86 |
| 14 | Outro | — |

## Sources

- **History.**
  - C. Stein, *Proc. Third Berkeley Symp.* 1 (1956); W. James & C. Stein, *Proc. Fourth Berkeley Symp.* 1 (1961).
  - B. Efron & C. Morris, *JASA* 68 (1973) and 70 (1975); *Scientific American* 236 (1977).
  - H. Robbins, *Proc. Third Berkeley Symp.* 1 (1956); R. A. Fisher, *Trans. R. Soc. Edinburgh* 52 (1918).
  - C. Henderson, *Ann. Math. Stat.* 21 (1950); *Biometrics* 31 (1975).
- **Methods.**
  - C. Stein, *Ann. Stat.* 9 (1981); B. Efron, *JASA* 106 (2011); J. Kiefer & J. Wolfowitz, *Ann. Math. Stat.* 27 (1956).
  - H. D. Patterson & R. Thompson, *Biometrika* 58 (1971); N. Laird & J. Ware, *Biometrics* 38 (1982).
  - F. Satterthwaite, *Biometrics Bulletin* 2 (1946); M. Kenward & J. Roger, *Biometrics* 53 (1997); S. Self &
    K.-Y. Liang, *JASA* 82 (1987).
  - Y. Mundlak, *Econometrica* 46 (1978); J. Hausman, *Econometrica* 46 (1978).
  - N. Breslow & D. Clayton, *JASA* 88 (1993); J. Pinheiro & D. Bates, *JCGS* 4 (1995); S. Zeger, K.-Y. Liang &
    P. Albert, *Biometrics* 44 (1988).
  - D. Spiegelhalter, *Statistics in Medicine* 24 (2005), funnel plots; H. Goldstein & D. Spiegelhalter, *JRSS A* 159
    (1996), league tables.
  - R. Fay & R. Herriot, *JASA* 74 (1979); N. G. N. Prasad & J. N. K. Rao, *JASA* 85 (1990); G. Battese, R. Harter &
    W. Fuller, *JASA* 83 (1988).
  - R. DerSimonian & N. Laird, *Controlled Clinical Trials* 7 (1986); W. Cochran, *Biometrics* 10 (1954); J. Higgins &
    S. Thompson, *Stat. Med.* 21 (2002); J. Higgins, S. Thompson & D. Spiegelhalter, *JRSS A* 172 (2009); J. Hartung &
    G. Knapp, *Stat. Med.* 20 (2001).
  - G. Rasch, *Probabilistic Models for Some Intelligence and Attainment Tests* (1960); A. Birnbaum, in Lord & Novick
    (1968).
  - D. Bates, M. Mächler, B. Bolker & S. Walker, *J. Stat. Software* 67 (2015).
- **Books.**
  - B. Efron, *Large-Scale Inference* (2010).
  - A. Gelman & J. Hill, *Data Analysis Using Regression and Multilevel/Hierarchical Models* (2007).
  - J. Pinheiro & D. Bates, *Mixed-Effects Models in S and S-PLUS* (2000).
  - J. N. K. Rao & I. Molina, *Small Area Estimation* (2nd ed., 2015).

## Problems and solutions

**1. Stein's lemma and SURE.**

*Solution.* For X ~ N(θ, 1) and differentiable h with E|h′| < ∞, integrate by parts, using
(x − θ)φ(x − θ) = −dφ(x − θ)/dx:
E(X − θ)h(X) = ∫ h(x)(x − θ)φ(x − θ)dx = ∫ h′(x)φ(x − θ)dx = E h′(X).
For θ̂ = X + g(X) in p dimensions:
E‖θ̂ − θ‖² = E‖X − θ‖² + 2E(X − θ)′g + E‖g‖² = p + 2E Σ ∂ᵢgᵢ + E‖g‖²,
applying the lemma coordinate by coordinate. So SURE = p + ‖g‖² + 2∇·g is unbiased for the risk.

For James–Stein, g = −(p − 2)X/‖X‖², with ∇·g = −(p − 2)²/‖X‖² and ‖g‖² = (p − 2)²/‖X‖². So
SURE = p − (p − 2)²/‖X‖² < p.

**2. James–Stein as empirical Bayes.**

*Solution.* Under the model each Xᵢ ~ N(0, 1 + τ²) independently, so S = ‖X‖² = (1 + τ²)W with W ~ χ²_p. For p ≥ 3,
E(1/W) = 1/(p − 2). Then E{(p − 2)/S} = (p − 2)/{(1 + τ²)(p − 2)} = 1/(1 + τ²) = B. Plugging this unbiased estimate of
B into the Bayes rule (1 − B)X gives James–Stein. (Shrinking towards x̄ spends a degree of freedom: p − 3 and
Σ(xᵢ − x̄)² ~ (1 + τ²)χ²_{p−1}.)

**3. The BLUP of a random intercept.**

*Solution.* For school g, y_g = X_gβ + 1u_g + e_g, with V_g = σ²I + τ²11′. Henderson's formula gives
û_g = τ²1′V_g⁻¹(y_g − X_gβ̂). By Sherman–Morrison, V_g⁻¹ = σ⁻²{I − τ²11′/(σ² + n_gτ²)}. Then
1′V_g⁻¹ = σ⁻²{1 − n_gτ²/(σ² + n_gτ²)}1′ = 1′/(σ² + n_gτ²).
So û_g = τ² n_g(ȳ_g − x̄_g′β̂)/(σ² + n_gτ²) = λ_g(ȳ_g − x̄_g′β̂), with λ_g = τ²/(τ² + σ²/n_g).

**4. REML for one sample.**

*Solution.* With X = 1 and V = σ²I:
ℓ_R = −½{n log σ² + Σ(yᵢ − ȳ)²/σ² + log(n/σ²)} + const = −½{(n − 1) log σ² + Σ(yᵢ − ȳ)²/σ²} + const.
Setting the derivative to zero gives σ̂² = Σ(yᵢ − ȳ)²/(n − 1).

**5. The boundary mixture.**

*Solution.* Asymptotically the unconstrained estimate of τ² is normal around 0 under H₀. With probability ½ it is
negative; then the constrained MLE is 0 and the LR statistic is 0. Otherwise the constraint is inactive and the
statistic is the square of the standardized estimate, χ²₁. So P(LR > c) = ½P(χ²₁ > c). Setting this to 0.05 gives
P(χ²₁ > c) = 0.10, so c = 2.71.

**6. Mundlak and fixed effects.**

*Solution.* Write x_gi = x̄_g + (x_gi − x̄_g). The model y = μ + βx + γx̄ + u + e is the same as
y = μ + β(x − x̄) + (β + γ)x̄ + u + e. The regressors x − x̄ and x̄ are orthogonal: within each school, x − x̄ sums to 0
and x̄ is constant. With all relevant group means included and common within-group variance, V_g⁻¹ = a I + b_g 11′ with the same a across groups. The rank-one term annihilates x − x̄, giving the unweighted within estimator. Varying a across groups instead gives a weighted within estimator. Here γ = β_B − β_W uses the corresponding GLS between coefficient, not an arbitrary unweighted descriptive regression.

## Glossary

- **Shrinkage; borrowing strength; partial pooling**: pulling separate estimates towards a common value, by an
  amount the data choose.
- **James–Stein estimator; positive part; inadmissible**: (1 − (p − 2)/‖X‖²)X; the version that never shrinks past
  the target; beaten everywhere by another estimator.
- **Stein's lemma; SURE**: E(X − θ)h(X) = E h′(X); an unbiased estimate of an estimator's risk.
- **Empirical Bayes; NPMLE; Tweedie's formula; winner's curse**: a prior estimated from many parallel problems; the
  nonparametric MLE of that prior; E(θ | x) from the marginal density; selected estimates overstate their truths.
- **Random effect; variance component; ICC; design effect**: a group effect drawn from a population; its variance;
  the share of variance between groups; the variance inflation of a clustered mean.
- **Linear mixed model; Henderson's equations; BLUP**: y = Xβ + Zb + ε; the penalized normal equations; the best
  linear unbiased predictor of b.
- **REML; error contrasts**: the likelihood of combinations of y free of β; it accounts for fitted fixed effects and can reduce bias, without making every constrained component unbiased.
- **Satterthwaite / Kenward–Roger degrees of freedom**: approximate t reference distributions for mixed-model
  contrasts.
- **Boundary; chi-bar-squared mixture**: a null on the edge of the parameter space; ½χ²₀ + ½χ²₁ for one variance.
- **Random slopes; growth curve; compound symmetry; AR(1); unstructured**: group-specific slopes; trajectories over
  time; covariance patterns for repeated measures.
- **Nested; crossed**: each lower unit in one higher unit; factors that cut across each other.
- **Fixed effects; within estimator; contextual effect; Mundlak device; Hausman test**: group dummies; demeaned
  regression; between minus within; adding group means of x; comparing FE and RE.
- **GLMM; Laplace approximation; adaptive Gauss–Hermite; PQL; conditional vs marginal effect**: random effects inside
  a link; approximating each group's integral; linearized quasi-likelihood; group-specific against
  population-averaged coefficients.
- **Funnel plot; league table**: rates against volume with chance limits; a ranking of units.
- **Small-area estimation; Fay–Herriot; EBLUP; synthetic estimator**: local estimates from thin samples; the area-level
  model; the shrunk combination; the regression prediction alone.
- **Meta-analysis; common and random effects; DerSimonian–Laird; Q; I²; Hartung–Knapp; prediction interval**:
  combining studies; one effect or a distribution of effects; the moment estimator of τ²; the heterogeneity statistic
  and its share; the t interval with a rescaled SE; where the next study's effect will fall.
- **Rasch model; item response theory; 2PL; test information**: logit P = θ − b; models for exam responses;
  item-specific slopes; Σ p(1 − p), whose root inverse is the SE.

## Where it comes back

| Idea | Returns in |
|---|---|
| hierarchical Bayes: the eight schools | 26 |
| MCMC for hierarchical models; Neal's funnel | 27 |
| choosing among mixed models | 28 |
| false discovery rates as empirical Bayes | 33 |
| fixed effects for panels | 37 |
| spatial random effects | 39 |
| frailty models | 40 |
| admissibility, proved | 45 |
| item response theory for AI benchmarks | 64 |
| the Coverage Board | every part; 65 |


## Scientific qualifications checked in QA

James–Stein's guarantee concerns expected total squared error for independent normal means with known equal variance: p ≥ 3 for a fixed target, p ≥ 4 for the estimated grand mean. It holds for every fixed mean vector, without requiring exchangeability. Some individual estimates can worsen. Baseball uses an approximate transformed sampling model and noisy held-out rates. Grid EM is a finite approximation, not a certified unrestricted NPMLE.

The deterministic risk_upper_bound is not sample SURE. The noncentral-chi-square Poisson mixture and Jensen give E(1/‖X‖²) ≥ 1/(p − 2 + ‖theta‖²). Plotted risks use 8,000 Monte Carlo replicates per point.

School components include programme and intake differences. The forty-school working mean omits school context, investigated in the Mundlak chapter; model-based SEs are not automatically correct. Henderson maximizes over beta and b at fixed G and R; covariance components need marginal likelihood or REML. Estimated-component predictions are empirical BLUPs. The simple prediction error formula assumes beta and covariance known. REML can reduce bias but is not universally unbiased; this illustration uses a nonnormal intercept mixture. Improper flat-prior normalization prevents comparing different fixed-effect spaces.

The 50:50 variance-boundary limit assumes one added variance, identifiable interior nuisance parameters and increasing independent groups. Use half the chi-square tail for a positive LR and p = 1 at zero. Correlated random slopes have additional boundary structure. Plug-in bootstrap and regular profile cutoffs are approximate. Very few groups also require prior sensitivity in Bayesian analyses.

Random-slope tau01 is a covariance, not correlation; centering changes its interpretation and the variance minimum need not be at the origin. Missing-at-random likelihood also needs an ignorable missingness mechanism and a correct joint outcome model.

Fixed effects remove additive constant group intercepts under strict exogeneity and a common slope; causality is not automatic. Mundlak tests a specified linear group-mean association, not independence. Its sample group means differ from the World's latent school SES. Hausman's statistic is undefined for nonpositive estimated variance difference, now explicitly reported instead of forcing a positive denominator.

For the displayed school fit, AGQ(10), (20) and (40) agree within 5e-7 in coefficients and about 5e-7 in log likelihood. Independent adaptive integration tests the likelihood. This is example-specific, not a universal ten-node guarantee. Conditional/marginal ratios are approximate; different working models matter alongside noncollapsibility.

Hospital rates are expit-transformed conditional modes, not posterior mean probabilities. The approximate normal funnel uses an estimated pooled rate and is rough at small expected counts. Compatibility with chance does not exclude elevated risk. Rates alone do not identify causal hospital quality.

Fay–Herriot uses estimated pooled sampling variances as fixed and a working Gaussian approximation, strained by n = 2 and long-tailed incomes. Standard MSE approximations need further allowance for estimating sampling variances. Reported MSE compares only 158 towns with n ≥ 2: 20.1 versus 20.6 is close in this realization, not an established equivalence. Benchmark population-weighted means. SAIPE is a family of methods.

I² describes heterogeneity of study estimates, not individual outcomes. The next-study latent-effect prediction interval is rough with five studies. Unmodified Hartung–Knapp can be narrower than a z interval; seeded coverage is not a universal guarantee. Funnel asymmetry has causes besides publication bias.

Rasch sufficiency assumes local independence and fixed item parameters for the same item set. Specific objectivity does not equate arbitrary raw scores across forms. Inverse information square root is a known-item asymptotic likelihood SE, not posterior uncertainty for conditional ability modes.

Curves use geometric viewport intersections, preserving missing gaps; extremes are not flattened to plot edges. Prior atom heights are untruncated; the small mass outside the viewport is labelled. Persistent context headings cover section introductions. Chinese tables, continuous listening and final narrated masters remain separate production gates.

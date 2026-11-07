# Statistics, Built — Part 24: Generalized Linear Models

Part 24 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fourth part of Stage III, Master's. Part 14 fitted logistic and Poisson
regressions. This part shows they are two members of one family, fitted by one algorithm (Nelder & Wedderburn 1972).
It then pushes that family to overdispersion, excess zeros, tables, ordered categories, clusters and the grading of
probability forecasts.

It opens with Chester Bliss's 1935 flour beetles: 481 beetles at eight doses of carbon disulphide, with deaths rising
from 6/59 to 60/60.
- Bliss's probit, the logit and the complementary log-log all fit; their deviances on 6 df are 10.12, 11.23 and 3.45.
- Among the three fitted links, cloglog has the lowest AIC, with AIC 33.6 against 41.4 for the logit.
- Its LD50 is a log dose of 1.7788 (60 mg/l), with Fieller interval [1.7702, 1.7862]. The logit's 1.7717 sits near the
  bottom of that interval.

From there the part covers:
- **The upgrade.** The three parts of a GLM; why not the linear probability model.
- **The exponential dispersion family.**
  - Canonical parameter, b(θ), dispersion; mean b′ and variance φV(μ) from Part 22's score identities.
  - A table of families.
  - Gamma regression of the World's incomes (mean ×1.117 per decade, φ̂ = 0.86) against a log-normal fit (0.100 per
    decade): different targets.
  - Tweedie's power variance; logit, probit and cloglog curves; the canonical link.
- **IRLS derived.**
  - Fisher scoring as weighted least squares on the working response.
  - The beetles from β = 0: slope 21.3 → 30.4 → 33.8 → 34.26 → 34.27. The deviance goes 306 → 38.8 → 13.3 → 11.26 →
    11.23, converging in 7 steps from the displayed zero start, using a coefficient-change tolerance.
  - Step-halving; non-canonical links.
- **Deviance.**
  - The saturated model; the beetles' deviances.
  - Analysis of deviance for 2,000 of the World's doctor visits: drops of 754, 299, 257 and 68 against a residual
    5,948 on 1,995 df (φ̂ = 3.36), and why order matters.
  - Pearson, deviance and randomized quantile residuals (Dunn & Smyth 1996); binned residuals.
  - Quantile-residual QQ plots: Poisson against negative binomial.
- **Asymptotics.**
  - Wald, LR and score; the dispersion and F tests.
  - The LD50 by delta and Fieller; testing overdispersion (LR 1,924, with a ½χ²₀ + ½χ²₁ null).
  - The deviance's χ² approximation. For grouped data, 2,000 fake Bliss experiments reject 6.0%. For binary data the
    deviance has mean 235 and SD 12 against χ²₁₉₈, so it would "reject" a correct model 63% of the time.
- **Separation.**
  - Twelve separated points: IRLS slopes climb by 5 a step to 108, while the log likelihood → 0.
  - Albert & Anderson; Firth's penalized likelihood gives 2.55 (SE 1.46).
  - Rare events and case–control sampling. With two points swapped, the MLE exists: 3.45 (SE 2.19).
- **Quasi-likelihood.**
  - Wedderburn's construction.
  - The visits: SEs ×1.83 for quasi-Poisson; sandwich SEs up to ×2.17; negative-binomial fits.
  - Quasi-Poisson's constant-multiple shape against the NB's μ + μ²/k; the beta-binomial.
  - Bliss's φ̂: 1.67 under the logit but 0.55 under the cloglog (a wrong mean looks like overdispersion).
  - Three Board rows.
- **Counts.**
  - The negative binomial as a gamma mixture (Greenwood & Yule 1920); offsets and rate ratios.
  - 40% zeros against the Poisson's 19% and the NB's 39%.
  - Poisson, ZIP (π̂ = 0.35, by EM), hurdle and NB: AIC 9,375, 8,248, 8,171 and 7,453.
  - Poisson pseudo-maximum likelihood.
  - The World's truth is a zero-inflated NB (15% never-goers, k = 1.2). The NB fits best by shrinking k to 0.82.
- **Log-linear models.**
  - Sex × age group × told high blood pressure for 5,000 adults.
  - Deviances: [SA][T] 798 on 5 df, [SA][AT] 39.1 on 3, [SA][AT][ST] 16.4 on 2 (p = 0.0003). The saturated model fits by definition, because the sex gap changes with age.
  - Homogeneous-association OR 0.68 (the common-OR model is rejected); graphical models; the Poisson trick.
- **Multinomial and ordinal.**
  - Baseline-category logits and IIA.
  - Proportional odds for four BMI categories in 3,000 adults: age 0.173 per decade (OR 1.19); sex −0.04 (none, as the
    World was built).
  - Fitted category probabilities by age.
  - Separate-cut slopes of 0.31, 0.18 and 0.15: not quite proportional. Other ordinal models.
- **GEE.**
  - Pupils passing 550 in 40 of the World's schools. The iid SE of the programme is 0.094; GEE-independence gives the
    same estimate (0.453) with robust SE 0.228. Exchangeable (α̂ = 0.089) gives 0.405 with model and robust SEs agreeing.
  - The census independence-logistic projection is 0.392; the census exchangeable-equation target is 0.378. The working mean is approximate, so the two targets need not coincide. Marginal against conditional effects (Zeger, Liang & Albert 1988);
    choosing the working correlation.
  - Three Board rows.
- **Proper scoring rules.**
  - Log, Brier and absolute scores at p = 0.3.
  - Forecasting a high blood pressure diagnosis on 2,000 new adults:

    | Forecaster | Log score | Brier | Accuracy |
    |---|---|---|---|
    | fitted logistic reference | 0.373 | 0.115 | 83.5% |
    | overconfident | 0.438 | 0.131 | 81.9% |
    | base rate | 0.463 | 0.144 | 82.6% |

  - The held-out calibration plot, with 200 adults per risk decile and Wilson uncertainty bars: the overconfident model says 86% where 54% happen, with the same AUC.
  - CRPS (0.560 honest, 0.604 too narrow, 0.653 too wide); Murphy's decomposition.

Every number on screen is computed in [`compute.py`](compute.py):
- Bliss's beetles are the Museum's;
- doctor visits, health, incomes and schools are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.glm` II** ([`explainer/stats/kit/glm.py`](../../../explainer/stats/kit/glm.py)), checked in
  `tests/test_stats_kit_glm2.py`:
  - `Family`, with links (identity, log, logit, probit, cloglog, inverse), variance functions and unit deviances;
  - `glm_fit`, a general IRLS recording its path, with deviance, Pearson/deviance/randomized quantile residuals, φ̂, and
    model, quasi and sandwich covariances;
  - LD50 with delta and Fieller intervals;
  - Firth's logistic regression, and separation paths;
  - negative binomial regression; ZIP by EM; Poisson hurdle;
  - multinomial logit; proportional odds;
  - GEE for binary outcomes (independence and exchangeable);
  - log and CRPS scores.
- **The dose–response panel** (`DoseResponse` in `explainer/stats/viz.py`).
- **The World**: the `visits` block, doctor visits with structural zeros (`VISITS_NEVER`) and NB heterogeneity
  (`VISITS_K` = 1.2).
- **The Museum**: `BLISS_BEETLES` and `bliss()`.

The Coverage Board gains six rows:

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| Poisson model SE | doctor visits, n = 500 | 1,000 | 63.5% | broken |
| quasi-Poisson SE | doctor visits, n = 500 | 1,000 | 89.5% | broken |
| sandwich SE | doctor visits, n = 500 | 1,000 | 94.4% | kept |
| logistic, iid SE | 40 schools, pupils clustered | 500 | 54.8% | broken |
| GEE, independence | 40 schools, robust SE | 500 | 95.0% | kept |
| GEE, exchangeable | 40 schools, robust SE; own census target | 500 | 95.8% | kept |

## Build it

```bash
python -m videos.stats.stats24.compute         # once (about a minute; cached in .cache/stats24)
python tools/build.py stats24 -q l             # fast 480p preview
python tools/build.py stats24                  # 1080p30 -> renders/stats24.mp4
python tools/qa_scene.py stats24 Counts
python tools/lecture_length.py stats24 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Bliss's beetles, 1935 | deviances 11.23 / 10.12 / 3.45; LD50 1.7788 [1.7702, 1.7862] |
| 1 | Upgrade: what Part 14 fitted | the three parts; the linear probability model |
| 2 | The exponential dispersion family | gamma ×1.117 per decade, φ̂ 0.86; log-normal 0.100 |
| 3 | IRLS derived | slope 21.3 → 34.27 in 7 steps; deviance 306 → 11.23 |
| 4 | Deviance | drops 754 / 299 / 257 / 68; φ̂ 3.36 |
| 5 | Asymptotics for GLMs | grouped 6.0%; binary 63% false rejections; LR for overdispersion 1,924 |
| 6 | Separation | slope → 108; Firth 2.55 (1.46) |
| 7 | Quasi-likelihood | ×1.83; Bliss φ̂ 1.67 vs 0.55; Board 63.5 / 89.5 / 94.4% |
| 8 | Counts | zeros 40% vs 19% vs 39%; AIC 9,375 / 8,248 / 8,171 / 7,453; k̂ 0.82 vs 1.2 |
| 9 | Log-linear models | 798 / 39.1 / 16.4; OR 0.68 |
| 10 | Multinomial and ordinal | 0.173 per decade (OR 1.19); cut slopes 0.31 / 0.18 / 0.15 |
| 11 | GEE | SE 0.094 vs 0.228; α̂ 0.089; truth 0.392; Board 54.8 / 95.0 / 95.8% (method-specific census targets) |
| 12 | Proper scoring rules | log 0.373 / 0.438 / 0.463; says 86%, sees 54%; CRPS 0.560 / 0.604 / 0.653 |
| 13 | Outro | — |

## Sources

- **History.**
  - C. Bliss, *Ann. Appl. Biol.* 22 (1935), with R. A. Fisher's appendix.
  - J. Nelder & R. Wedderburn, *JRSS A* 135 (1972); M. Greenwood & G. U. Yule, *JRSS* 83 (1920).
- **Methods.**
  - R. Wedderburn, *Biometrika* 61 (1974); P. McCullagh, *JRSS B* 42 (1980); M. Tweedie (1984).
  - A. Albert & J. Anderson, *Biometrika* 71 (1984); D. Firth, *Biometrika* 80 (1993); G. King & L. Zeng, *Political
    Analysis* 9 (2001); R. Prentice & R. Pyke, *Biometrika* 66 (1979).
  - P. Dunn & G. Smyth, *JCGS* 5 (1996); D. Hosmer & S. Lemeshow (1980); D. Williams, *Applied Statistics* 31 (1982).
  - J. Ver Hoef & P. Boveng, *Ecology* 88 (2007); A. C. Cameron & P. Trivedi, *J. Econometrics* 46 (1990).
  - D. Lambert, *Technometrics* 34 (1992); J. Mullahy, *J. Econometrics* 33 (1986); C. Gourieroux, A. Monfort &
    A. Trognon, *Econometrica* 52 (1984); J. Santos Silva & S. Tenreyro, *REStat* 88 (2006).
  - J. Darroch, S. Lauritzen & T. Speed, *Ann. Stat.* 8 (1980).
  - K.-Y. Liang & S. Zeger, *Biometrika* 73 (1986); S. Zeger, K.-Y. Liang & P. Albert, *Biometrics* 44 (1988);
    L. Mancl & T. DeRouen, *Biometrics* 57 (2001); M. Pepe & G. Anderson (1994).
  - G. Brier, *Monthly Weather Review* 78 (1950); A. Murphy, *J. Appl. Meteorology* 12 (1973); T. Gneiting &
    A. Raftery, *JASA* 102 (2007).
- **Books.**
  - P. McCullagh & J. Nelder, *Generalized Linear Models* (2nd ed., 1989).
  - A. Agresti, *Categorical Data Analysis* (3rd ed., 2013).
  - P. Dunn & G. Smyth, *Generalized Linear Models with Examples in R* (2018).
  - A. Dobson & A. Barnett, *An Introduction to Generalized Linear Models* (4th ed., 2018).

## Problems and solutions

**1. The gamma family.**

*Solution.* With shape ν and mean μ,
log f = ν log ν − log Γ(ν) + (ν − 1) log y − ν log μ − νy/μ = (y(−1/μ) − log μ)/(1/ν) + c(y, ν).
- **The parameters.** θ = −1/μ, b(θ) = −log(−θ) = log μ, φ = 1/ν.
- **The moments.** b′(θ) = −1/θ = μ, and b″(θ) = 1/θ² = μ², so V(μ) = μ².
- **The link.** The canonical link is θ = −1/μ, the (negative) inverse.

**2. Scoring as least squares.**

*Solution.* U = Σ xᵢ(yᵢ − μᵢ)(dμᵢ/dηᵢ)/(φVᵢ) = X'W(z − η)/φ, where wᵢ = (dμᵢ/dηᵢ)²/Vᵢ and zᵢ − ηᵢ = (yᵢ − μᵢ)dηᵢ/dμᵢ. The
expected information is X'WX/φ. Then β + I⁻¹U = β + (X'WX)⁻¹X'W(z − η) = (X'WX)⁻¹X'Wz, since Xβ = η.

**3. Poisson deviance.**

*Solution.* D = 2Σ{yᵢ log(yᵢ/μ̂ᵢ) − (yᵢ − μ̂ᵢ)}. With a log link and an intercept, the intercept's score equation is
Σ(yᵢ − μ̂ᵢ) = 0, so the second sum vanishes and D = 2Σ yᵢ log(yᵢ/μ̂ᵢ).

**4. Separation.**

*Solution.* If xᵢ'b > 0 exactly when yᵢ = 1, then for c > 0,
ℓ(cb) = Σ_{y=1} −log(1 + e^{−c xᵢ'b}) + Σ_{y=0} −log(1 + e^{c xᵢ'b}). In both sums the exponent's argument tends to
−∞ as c → ∞, so every term increases to 0. The supremum, 0, is not attained.

**5. The negative binomial as a mixture.**

*Solution.* Take λ ~ Gamma with shape k and mean μ, so Var λ = μ²/k.
- **The mean.** E y = E E(y | λ) = E λ = μ.
- **The variance.** Var y = E Var(y | λ) + Var E(y | λ) = E λ + Var λ = μ + μ²/k.
- **The marginal distribution.** Integrating the Poisson against the gamma gives the negative binomial probability
  function.

**6. Propriety.**

*Solution.* E_p(q − y)² = p(1 − q)² + (1 − p)q², whose derivative 2(q − p) vanishes at q = p, a minimum, so the Brier
score is proper. E_p|q − y| = p(1 − q) + (1 − p)q = p + q(1 − 2p) is linear in q. It is minimized at q = 0 when
p < ½ and at q = 1 when p > ½, so the absolute score is improper: it rewards rounding.

## Glossary

- **Generalized linear model; linear predictor; link**: an exponential-family outcome whose mean, through g, is
  linear in the covariates.
- **Exponential dispersion family; canonical parameter; cumulant function b; dispersion φ; variance function V**:
  f = exp{(yθ − b(θ))/φ + c}; μ = b′(θ); Var y = φV(μ).
- **Canonical link**: g(μ) = θ, giving score X′diag(w)(y − μ)/φ and sufficient X′diag(w)y for β at known dispersion and fixed prior weights.
- **Probit; logit; complementary log-log; tolerance distribution**: inverse links for probabilities; the latent
  threshold story behind them.
- **IRLS; working response; working weights**: Fisher scoring as repeated weighted least squares.
- **Deviance; saturated model; analysis of deviance**: twice the log-likelihood gap to a perfect fit; comparing
  nested models by drops.
- **Pearson, deviance and randomized quantile residuals**: standardized differences; signed root unit deviances;
  Φ⁻¹ of a randomized CDF; exactly N(0, 1) for the known true conditional CDF, with fitted residuals used diagnostically.
- **Separation; Firth's penalized likelihood**: perfect prediction and infinite MLEs; the Jeffreys-prior penalty
  that keeps them finite.
- **Overdispersion; quasi-likelihood; quasi-Poisson; beta-binomial**: more variation than the family allows; a
  mean–variance model without a distribution; φμ; a binomial with beta-distributed p.
- **Negative binomial; zero-inflated model; hurdle model; offset**: a gamma-mixed Poisson; structural zeros plus a
  count model; a gate then a truncated count; a log exposure with coefficient 1.
- **Log-linear model; conditional independence; graphical model**: Poisson models for table counts; specific absent interaction sets; graphical models retain all maximal-clique interactions.
- **Multinomial logit; IIA; proportional odds; cut-points**: softmax over categories; the independence of irrelevant
  alternatives; one slope for all cumulative logits; the thresholds on the latent scale.
- **GEE; working correlation; marginal vs conditional effect**: cluster-wise score equations with a robust
  sandwich; the guessed within-cluster correlation; population-averaged against cluster-specific coefficients.
- **Proper scoring rule; log score; Brier score; CRPS; calibration; resolution**: penalties that reward honesty;
  −log q_y; (q − y)²; the integrated squared CDF gap; agreement of forecasts and rates; spread of forecasts.

## Where it comes back

| Idea | Returns in |
|---|---|
| GLMMs: conditional effects | 25 |
| Bayesian GLMs; priors against separation | 26 |
| choosing links and terms: AIC, CV | 28 |
| robust GLMs | 30 |
| penalized GLMs | 32 |
| calibration and scoring of predictions | 34 |
| propensity scores | 36 |
| Cox regression as a Poisson GLM | 40 |
| the Coverage Board | every part; 65 |


## QA clarifications

All 14 scenes and the 12 computation items were reviewed alongside the GLM kit and its reference tests.

- Prior weights enter both the exponential-dispersion variance (φV(μ)/w) and IRLS information. The displayed canonical sufficient statistic includes those weights. Gamma and inverse-Gaussian natural parameters are −1/μ and −1/(2μ²); the commonly named inverse links can absorb fixed signs/scales in their coefficients.
- The local IRLS implementation uses weighted QR, recomputes each step-halving candidate, and raises on failed search or nonconvergence. It is checked against grouped likelihood fits in statsmodels, including a Poisson example that requires halving. The noncanonical scoring rate need not be quadratic, and stopping tolerance is distinct from machine precision.
- Deviance here is unscaled D = 2φ(ℓ_sat − ℓ_fit); known-dispersion LR statistics use ΔD/φ. Quasi F references are approximate outside the Gaussian identity-link model. A binary saturated-model χ² test is unreliable, while regular fixed-dimensional nested likelihood differences can still use Wilks. Boundary, separation and misspecification require different references.
- The overdispersion LR is computed directly from both fitted log likelihoods (1924.0), avoiding arithmetic with rounded values. The one-sided NB2 score and the special single-boundary 50/50 null mixture are stated with their assumptions.
- Raw count variance exceeding the raw mean is not by itself evidence against a conditional Poisson model: covariate mean variation also inflates marginal variance. Pearson dispersion, residuals and coverage checks provide further information. A lower dispersion estimate under another link does not prove that the first curve was the sole cause.
- Exact randomized quantile normality requires the true conditional CDF. Estimated parameters make fitted residuals dependent and alter their finite-sample distribution. Displayed QQ points are sampled and viewport-limited, without flattening extreme values onto a boundary.
- Missing high-order interactions need not encode independence. Graphical log-linear models are a subset of hierarchical models and include every maximal-clique interaction. The all-pairs/no-three-way model is not the complete-graph graphical model. Its estimated common OR is a summary from a rejected model and is not identically the Mantel–Haenszel estimator.
- The ordinal sex coefficient is compatible with zero; point estimates do not establish an exact null. Differences among separate cut-point slopes are an informal diagnostic with correlated uncertainty. The probability stack displays men.
- Binary GEE uses the analytic exchangeable inverse and records constraints needed for positive-definite working correlation. Both working structures match statsmodels. The finite-World logistic approximation has census programme coefficients 0.391567 (independence) and 0.378283 (exchangeable); the Board uses the matching target for each method. Exchangeable coverage is 95.8%, versus 95.0% for independence. This finite-population simulation does not establish a universal coverage guarantee.
- GEE robustness requires a suitable conditional mean, independent clusters, moments and design conditions; changing working correlation under mean misspecification can change the target. Model/robust SE agreement in one sample is not proof of a correct covariance. Marginal-versus-conditional coincidence is not exclusive to identity-link models.
- The probability forecaster labelled “logistic” is a fitted reference, not an assumed perfectly calibrated oracle. Holdout deciles retain counts and Wilson bars; a monotone transformation preserves AUC while changing calibration and proper losses. Murphy's decomposition is exact in population conditional-rate form; arbitrary finite bins need within-bin terms unless forecasts are constant within bins. Resolution is distinct from AUC.
- The mean log loss is the negative average held-out log likelihood. Expected excess log loss, rather than total expected log loss, equals KL divergence. CRPS values are Monte Carlo averages of 20,000 common simulated outcomes.
- All curves use local geometric viewport clipping that preserves crossings and missing gaps. Persistent section headings retain context through narration introductions. Chinese tables, continuous listening and final narrated masters remain separate production gates.

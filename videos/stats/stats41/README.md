# Statistics, Built — Part 41: What You Didn't See

Part 41 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the twenty-first part of Stage III, Master's. Data go missing, and data are
measured wrongly. This part asks when that matters and what can be done:
- Rubin's mechanisms (MCAR, MAR, MNAR) and ignorability;
- the easy methods' sins: complete cases, mean imputation, LOCF, the missing indicator, available cases;
- likelihood under MAR: EM and FIML;
- multiple imputation and Rubin's rules, chained equations, congeniality;
- weighting as causal inference: IPW, AIPW, calibration;
- data missing not at random: Heckman's selection model, pattern mixtures, tipping points, Manski's bounds;
- MRP for self-selected samples;
- measurement error and misclassification: attenuation, regression calibration, SIMEX, the matrix method.

The part builds `statkit.mi` and an instrument, the mask grid (`MaskGrid`): a data table as cells, with missing cells
darkened by mechanism, imputed cells painted, and offset copies for the m completed data sets. Its real data are:
- New York's air quality, May–September 1973 (ozone missing on 37 of 153 days);
- NHANES 2017–2018's two 24-hour dietary recalls (public domain);
- Mroz's (1987) 753 married women from the 1975 PSID (R's `sampleSelection`, GPL ≥ 2).

It opens with Wald's bombers (1943) in a stylized World of 2,000 planes, 1,252 of which return. The engines are 15%
of the surface but carry 10.5% of the survivors' hits: the relative area-normalized hit-share deficit is about 30%. This is not the 40% per-hit engine kill probability in the toy generator (Mangel & Samaniego 1984).

From there the part covers:
- **Mechanisms.**
  - Rubin (1976); MCAR, MAR, MNAR; the factorization and ignorability; missingness graphs (Mohan & Pearl 2021).
  - The World's survey of 2,000 with income withheld by 30% under three known masks. Under MAR the missing are 39.3
    years old on average against 51.2 for the observed; under MNAR their hidden log incomes average 11.10 against
    10.36.
  - Monotone and arbitrary patterns; dropout in trials. MCAR is testable (Little 1988); MAR against MNAR is not
    (Molenberghs et al. 2008).
- **The easy methods' sins.**
  - Complete cases: on the true mean log income of 10.583, MCAR gives 10.585, MAR 10.609 and MNAR 10.358. A correctly specified conditional regression remains valid under selection on x alone, with adequate support; misspecified regression projections can change under selection.
  - The missing-indicator method (Greenland & Finkle 1995); available cases.
  - Mean imputation cuts the SD from 0.653 to 0.544. Regression imputation inflates the correlation with age from
    0.103 to 0.127; appropriate stochastic draws restore residual variation in distribution, rather than reproducing both statistics exactly in one draw.
  - LOCF in a seeded trial: the true effect is −4.84, LOCF gives −4.47, MAR imputation −4.96.
- **Likelihood under MAR.**
  - EM for the normal (Dempster, Laird & Rubin 1977); Buck (1960); why EM climbs; the missing information principle
    and Louis's SEs; FIML.
  - New York's ozone: EM converges in 12 iterations. The mean is 41.9 against 42.1 from complete cases, under a working multivariate-normal MAR model. Missing days have similar average temperature, which does not establish the full missingness mechanism.
- **Multiple imputation.**
  - Rubin's rules derived; proper draws and PMM; chained equations (van Buuren); how many imputations; derived
    variables; congeniality (Meng 1994).
  - New York's log ozone on sun, wind and temperature: MI with m = 20 agrees with complete cases. The temperature
    coefficient is 0.049 (SE 0.006, FMI 0.33); √B ≈ two thirds of √W.
- **Weighting.**
  - IPW = Horvitz–Thompson with a response propensity; the missing-data / causal dictionary; AIPW (Robins, Rotnitzky
    & Zhao 1994); calibration (Deville & Särndal 1992).
  - On the MAR mask: IPW 10.589 with the right model and 10.607 with the wrong one. AIPW is 10.589 with a correct response specification and a rich working outcome model and 10.607 when both are wrong.
  - Weights up to 3.3; 1,372 respondents are worth 1,279; balance on age is restored (47.5 against 47.5).
- **MNAR.**
  - Heckman (1979) and the inverse Mills ratio.
  - Mroz: 428 of 753 worked; 62% of women with no child under 6 worked, against 39% with one and 27% with two.
    The return to a year of education is 0.1075 by OLS, 0.1091 by Heckman's two steps and 0.1084 by ML, with ρ̂ near
    0: the residual correlation is near zero within this restrictive joint-normal specification, not proof that selection is absent.
  - Exclusion restrictions; Manski's bounds; pattern mixtures (Little 1993).
  - A sensitivity analysis on the MNAR mask reaches the truth near δ ≈ 0.7 (refusers about twice as rich). ICH E9(R1).
- **MRP.**
  - The Xbox poll (Wang et al. 2015); Gelman & Little (1997).
  - The World's election, with Blue at 38.2%, and an opt-in poll of 3,000 that is 40% under-30 (against 22%) and 65%
    male. Raw 42.3%; raked 39.4%; MRP 38.9% (approximate conditional 90% interval 37.0–41.0).
  - By region: raw RMSE 3.2 points, MRP 2.6 (small regions are pooled toward the island).
  - YouGov 2017; small-area cousins; limits.
- **Measurement error.**
  - Spearman (1904); regression dilution; the classical picture.
  - NHANES: two days' sodium correlate 0.34. SBP on one day's sodium gives 0.18 mm Hg/g (SE 0.15), on the two-day
    mean 0.35, and by regression calibration 0.77 (λ̂ = 0.24).
  - SIMEX (Cook & Stefanski 1994). Seeded (truth 2, reliability 0.39): naive 0.84, SIMEX 1.33, RC 2.15.
  - Replicates as instruments; Deming regression; Berkson error; residual confounding.
- **Misclassification.**
  - The matrix method; a seeded case-control study with true OR 2.29 in the sample. Nondifferential recall (Se 0.8,
    Sp 0.9) gives 1.67, corrected to 2.07. Differential recall gives 2.53.
  - Outcome misclassification; validation substudies; probabilistic bias analysis.

Data:
- the air quality, NHANES and Mroz's women are the Museum's;
- the survey sample with its masks, the election and the opt-in polls are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.mi`** ([`explainer/stats/kit/mi.py`](../../../explainer/stats/kit/mi.py)), tested in
  `tests/test_stats_kit_mi.py`:
  - **Masks and EM:** MCAR, MAR and MNAR masks with known probabilities; EM for a multivariate normal with the
    observed log-likelihood.
  - **Imputation:** proper, stochastic, mean and PMM normal-regression imputation; proper logistic imputation;
    chained equations; Rubin's rules with Barnard–Rubin df and the FMI.
  - **Weighting:** response models; IPW and AIPW means.
  - **MNAR:** Heckman's two-step (with corrected SEs) and ML.
  - **MRP:** multilevel logistic regression with random effects by penalized IRLS and Laplace-chosen variances, with
    predictions and posterior draws.
  - **Measurement error:** Spearman's disattenuation; SIMEX; the misclassification matrix method.
- **The World** gains its `missing` block: 2,000 adults, three income masks and an SBP mask, with their true
  probabilities.
- **The Museum** gains `mroz87.csv`, read with `museum._table`.
- **The mask grid** (`MaskGrid` in `explainer/stats/viz.py`).

The Coverage Board gains nine rows:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| complete-case mean | y MAR given x (40%), n = 300 | 0.4% | broken |
| complete-case regression slope | same: missingness depends on x only | 89.4% | kept |
| single regression imputation, naive SE | same | 70.8% | broken |
| multiple imputation (m = 10), Rubin's rules | same | 89.3% | kept |
| AIPW mean, influence-function SE | same | 86.5% | broken (extreme weights) |
| opt-in poll, raw share | the World's election, a self-selected sample of 1,500 | 2.5% | broken |
| MRP, approximate conditional 90% posterior interval | same | 81.0% | broken |
| OLS slope on an error-prone w | reliability 0.61, n = 500 | 0.0% | broken |
| regression calibration, bootstrap SE | same, with a replicate; 199 resamples per dataset | 88.9% | kept |

Scientific conditions and implementation scope:

- Wald’s displayed hit-share deficit is normalized by total hits on returning planes. It illustrates survivorship selection, but is not itself an estimate of a hit’s kill probability. The toy model assumes independent Poisson strikes and location-dependent survival.
- MAR ignorability needs distinct, variation-independent parameters and a suitable observed-data likelihood; Bayesian ignorability additionally needs the relevant prior factorization. MCAR has testable implications, but a non-significant diagnostic does not prove it. General missingness graphs require more than the simple arrow examples.
- Conditional complete-case regression needs a correct conditional model and adequate covariate support. Marginal means and misspecified projections need not be preserved. The ten-column 60% example assumes independent holes. Missing-indicator trial adjustment requires appropriate baseline design, model and standard errors; pairwise covariance estimates can form an indefinite matrix even though individual pairwise correlations remain bounded.
- EM accounts for missing conditional covariance under its fitted model; it does not guarantee a correct model, global optimum or universally correct spread. Its local convergence matrix involves a fraction of missing information; that ratio alone does not determine absolute interval width. Imputation counts and chained-equation mixing require diagnostics. The large-df relative variance share differs from finite-df FMI. Derived-variable imputations must preserve the substantive model’s needed interactions and nonlinear structure; a generic direct-term recipe need not preserve deterministic identities.
- Known-probability Horvitz–Thompson means are unbiased under the stated MAR and positivity assumptions. Normalized or fitted-propensity estimators generally have finite-sample bias. AIPW double robustness concerns consistency; efficiency and standard-error claims require regularity and suitable nuisance estimation. The rich World outcome regression is a working approximation, not a known exact conditional mean. Trimming can introduce bias or change the target; Kish’s weight-only effective sample size is a diagnostic rather than a universal precision equivalence.
- Heckman’s exclusions and joint-normal assumptions are identifying restrictions, not verified facts. Schooling coefficients are associations. The delta curve now reuses 20 completed datasets at every value, removing Monte Carlo noise between sensitivity settings. The oracle mean-matching shift is 0.6904 log-income units; it is not identified from observed data or a claim that every conditional distribution has that exact shift. A decision tipping point also needs a stated decision threshold.
- Worked and repeated-poll MRP use the same factor structure, including age-by-sex effects, and the same group-SD grid (0.1, 0.3, 0.6). Intervals use a normal approximation at the posterior mode conditional on grid-selected group spreads. They omit hyperparameter uncertainty, and coarse cells leave residual selection. The study does not isolate the sources of undercoverage.
- The NHANES analysis is an unweighted complete-case association among 2,805 adults not recorded as taking prescribed antihypertensives. Medication fields are unrecorded for 2,622 of them, including structural skips; this is not a verified all-off-medication cohort or a nationally representative causal sodium effect. Equal-variance, independent classical errors are assumptions behind interpreting repeat-day correlation as reliability. Regression calibration and replicate-instrument IV can share a population target while differing in finite samples.
- Misclassification curves show odds ratios formed from expected cell proportions, not the exact expectation of a sample ratio. Toward-null population results need informative common error rates in the stated simple setting. The matrix example reports point corrections; an interval would additionally need sampling and error-rate uncertainty. Perfect specificity with common positive sensitivity preserves a population risk ratio, rather than making every sample ratio unbiased.

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats41.compute   # once (a few minutes)
python tools/build.py stats41 -q l                         # fast 480p preview
python tools/build.py stats41                              # 1080p30 -> renders/stats41.mp4
python tools/qa_scene.py stats41 MultipleImputation
python tools/lecture_length.py stats41 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Wald's bombers | engines 15% of surface, 10.5% of hits |
| 1 | Mechanisms | missing 39 vs observed 51 years old |
| 2 | The easy methods' sins | SD 0.653 → 0.544; LOCF −4.47 vs −4.84 |
| 3 | Likelihood under MAR | EM in 12 iterations |
| 4 | Multiple imputation | FMI 0.17–0.34; 70.8% vs 89.3% |
| 5 | Weighting is causal inference | AIPW right if either model is |
| 6 | Missing not at random | ρ̂ ≈ 0.03; tipping δ ≈ 0.7 |
| 7 | MRP | 42.3% → 38.9% (truth 38.2%) |
| 8 | Measurement error | repeat-day correlation 0.34; conditional working λ = 0.24; RC 0.77 |
| 9 | Misclassification | OR 2.29 → 1.67 → 2.07 |
| 10 | Outro | — |

## Sources

- **Foundations.**
  - A. Wald, *A Method of Estimating Plane Vulnerability Based on Damage of Survivors* (1943; reprinted 1980);
    M. Mangel & F. Samaniego, *JASA* 79 (1984).
  - D. Rubin, *Biometrika* 63 (1976); R. Little & D. Rubin (3rd ed. 2019); R. Little, *JASA* 83 (1988).
  - G. Molenberghs et al., *JRSS B* 70 (2008); K. Mohan & J. Pearl, *JASA* 116 (2021).
- **Simple methods.**
  - S. Greenland & W. Finkle, *Am. J. Epidemiol.* 142 (1995).
  - National Research Council, *The Prevention and Treatment of Missing Data in Clinical Trials* (2010).
- **Likelihood.**
  - S. F. Buck, *JRSS B* 22 (1960); A. Dempster, N. Laird & D. Rubin, *JRSS B* 39 (1977).
  - T. Louis, *JRSS B* 44 (1982); X.-L. Meng & D. Rubin, *JASA* 86 (1991).
- **Multiple imputation.**
  - D. Rubin (1987); J. Barnard & D. Rubin, *Biometrika* 86 (1999); X.-L. Meng, *Stat. Sci.* 9 (1994).
  - S. van Buuren (2nd ed. 2018); S. van Buuren & K. Groothuis-Oudshoorn, *J. Stat. Softw.* 45 (2011).
  - I. White, P. Royston & A. Wood, *Stat. Med.* 30 (2011); P. von Hippel, *Sociol. Methodol.* 39 (2009),
    *Sociol. Methods Res.* 49 (2020).
- **Weighting.**
  - J. Robins, A. Rotnitzky & L. P. Zhao, *JASA* 89 (1994); J.-C. Deville & C.-E. Särndal, *JASA* 87 (1992).
- **MNAR.**
  - J. Heckman, *Econometrica* 47 (1979); T. Mroz, *Econometrica* 55 (1987).
  - R. Little, *JASA* 88 (1993); C. Manski, *J. Hum. Resour.* 24 (1989); ICH E9(R1) (2019).
- **MRP.**
  - A. Gelman & T. Little, *Survey Methodol.* 23 (1997); W. Wang, D. Rothschild, S. Goel & A. Gelman, *IJF* 31 (2015).
- **Measurement error.**
  - C. Spearman, *Am. J. Psychol.* 15 (1904); J. Cook & L. Stefanski, *JASA* 89 (1994).
  - R. Carroll, D. Ruppert, L. Stefanski & C. Crainiceanu (2006); W. E. Deming (1943); O. Reiersøl, *Econometrica* 18
    (1950).
  - R. Barron, *Biometrics* 33 (1977); T. Lash, M. Fox & A. Fink, *Applying Quantitative Bias Analysis* (2009).

## Problems and solutions

1. **Rubin's factorization.** f(Y_obs, R | θ, φ) = ∫ f(Y_obs, Y_mis | θ) P(R | Y_obs, Y_mis, φ) dY_mis. Under MAR the
   second factor does not depend on Y_mis, so it leaves the integral: P(R | Y_obs, φ) ∫ f(Y_obs, Y_mis | θ) dY_mis =
   P(R | Y_obs, φ) f(Y_obs | θ). With θ and φ distinct, the first factor is constant in θ.
2. **Selection on x.** If R depends on x only, f(y | x, R = 1) = f(y | x)P(R = 1 | x)/P(R = 1 | x) = f(y | x). So
   E[y | x, R = 1] is the true regression, and least squares on complete cases is unbiased under the correctly specified conditional-mean model and adequate support. But E[y | R = 1] =
   E[E(y | x) | R = 1] averages the regression over the selected x's, which differ from the population's.
3. **Rubin's variance.** Var(Q | Y_obs) = E[Var(Q | Y) | Y_obs] + Var[E(Q | Y) | Y_obs]. Estimate the first by W and
   the second by B. Averaging m draws adds simulation variance B/m to the mean, giving T = W + B + B/m.
4. **IPW and AIPW.** E[RY/π(X)] = E[E(R | X, Y) Y/π(X)] = E[π(X)Y/π(X)] = E[Y] under MAR.
   - AIPW: E[m(X) + R(Y − m(X))/π(X)].
   - If π is right, the second term has expectation E[Y − m(X)], so the total is E[Y].
   - If m is right, E[Y − m(X) | X, R = 1] = 0, so the second term vanishes and E[m(X)] = E[Y].
5. **Dilution.** Cov(W, Y) = Cov(X + U, α + βX + ε) = βσ²_X and Var W = σ²_X + σ²_U. So the OLS slope tends to
   βσ²_X/(σ²_X + σ²_U) = λβ.
6. **The matrix method.** E[share reporting exposure] = Se p + (1 − Sp)(1 − p) = (Se + Sp − 1)p + (1 − Sp), which is
   linear in p. So p = (E[share] − (1 − Sp))/(Se + Sp − 1), as an inversion of expected proportions when Se + Sp > 1. Nonlinear sample odds-ratio corrections are not thereby exactly unbiased; incompatible rates may require a constrained model.

## Glossary

- **MCAR; MAR; MNAR; ignorability**: missingness unrelated to anything; explained by observed values; dependent on
  unseen values; MAR with distinct parameters.
- **Monotone pattern; unit and item nonresponse**: dropouts who never return; whole-person and single-question gaps.
- **Complete-case analysis; available-case analysis; missing-indicator method; LOCF**: the shortcuts.
- **EM; FIML; missing information**: likelihood methods under MAR; the information the holes cost.
- **Multiple imputation; proper imputation; PMM; chained equations; Rubin's rules; FMI; congeniality**: the MI
  toolkit.
- **IPW; AIPW; double robustness; calibration weighting**: weighting approaches.
- **Selection model; inverse Mills ratio; exclusion restriction; pattern mixture; delta adjustment; tipping point;
  Manski bounds**: MNAR approaches.
- **MRP; poststratification; small-area estimation**: modelling self-selected samples.
- **Reliability; regression dilution; regression calibration; SIMEX; Berkson error; Deming regression**: measurement
  error.
- **Sensitivity; specificity; nondifferential and differential misclassification; recall bias; validation study**:
  misclassification.

## Where it comes back

- **Part 42**: the comprehensive exam's consulting case starts with missing values.
- **Part 45**: EM's convergence and the information lost to missingness.
- **Part 49**: AIPW's semiparametric efficiency.
- **Part 62**: unmeasured confounding with proxies.
- **Part 63**: privacy noise as deliberate measurement error.

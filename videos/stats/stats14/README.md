# Statistics, Built — Part 14: Counts and Categories

Part 14 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Parts 12 and 13 assumed measurements. This
part regresses yes-or-no outcomes and counts, and reads tables.

It opens on 27 January 1986: the Challenger teleconference, and a chart of the seven flights with O-ring distress
(r = 0.02). Adding the sixteen flights with no distress shows the effect: every one launched at 66 °F or warmer.
From there the part covers:
- why least squares on 0/1 gives p̂(31) = 1.75, and where the linear probability model is still used;
- logistic regression: odds, log-odds and odds ratios; the latent-threshold picture; logit vs probit; the canonical
  link;
- maximum likelihood: the log-likelihood landscape, Newton's method as iteratively reweighted least squares (each step
  drawn), the deviance, and LR vs Wald;
- the Challenger fit with a dashboard:
  - p̂(31 °F) = 0.9996;
  - a Wald interval [0.48, 1] vs a profile interval [0.80, 1], with the profile log-likelihood drawn;
  - the extrapolation caveat;
- Poisson regression with offsets on the World's screening condition by age and sex (the age effect found, the null
  sex effect confirmed), and the rare-outcome link to logistic regression;
- overdispersion in the World's 200 towns: quasi-Poisson and sandwich SEs;
- two-way tables at Berkeley 1973: χ², risk difference, RR, OR with Woolf's interval, OR vs RR, r × c tables;
- Simpson's paradox: rates by department, application shares, mosaic plots, weighted averages;
- three-way tables: stratum odds ratios, Mantel–Haenszel, the CMH test, logistic regression with department dummies,
  Breslow–Day;
- case–control studies: Doll & Hill 1950, the odds ratio's symmetry, Prentice–Pyke, and a World cohort vs case–control
  check;
- scoring predictions: ROC and AUC, calibration, the Brier score, proper scoring rules, thresholds and costs.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- the Challenger flights, the Berkeley admissions and Doll & Hill's counts come from the Museum;
- the screening condition, ages and towns are the World's (seed 1662);
- the clinic visits are simulated on the World's towns.

**Built in this part:**
- **`statkit.glm` (I)** ([`explainer/stats/kit/glm.py`](../../../explainer/stats/kit/glm.py)):
  - logistic and Poisson regression by IRLS, with step-halving, offsets and binomial trials;
  - classical, quasi and sandwich covariances; deviance and Pearson dispersion;
  - Wald and profile-likelihood intervals (constrained IRLS with continuation);
  - 2 × 2 measures with Woolf and Katz intervals, Mantel–Haenszel and CMH;
  - ROC/AUC, the Brier score and calibration.

  Everything is checked against statsmodels and SciPy in `tests/test_stats_kit_glm.py`.
- **The Challenger dashboard** (`ChallengerDashboard` in `explainer/stats/viz.py`): the flights, the fitted curve with
  its Wald band, and a temperature probe that reads out p̂ and its interval.

The Coverage Board gains eight rows, all 95% intervals, R = 10,000.

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| logistic slope, Wald | Challenger temperatures, n = 23 | 95.34% | kept |
| logistic slope, profile likelihood | Challenger temperatures, n = 23 | 91.63% | broken |
| p at 31 °F, Wald (logit scale) | Challenger temperatures, n = 23 | 95.33% | kept |
| p at 31 °F, profile likelihood | Challenger temperatures, n = 23 | 91.46% | broken |
| Poisson rate ratio, classical SE | 200 towns, Poisson counts | 95.10% | kept |
| Poisson rate ratio, classical SE | 200 towns, gamma frailty | 17.56% | broken |
| Poisson rate ratio, quasi-Poisson SE | 200 towns, gamma frailty | 67.43% | broken |
| Poisson rate ratio, sandwich SE | 200 towns, gamma frailty | 90.61% | broken |

Notes on the logistic rows:
- In 205 of the 10,000 samples the outcomes are perfectly separated by temperature. They have no finite estimate,
  so they count as Wald misses.
- The profile interval still exists in those samples (it is one-sided), and its coverage is checked directly: the
  likelihood-ratio statistic at the truth must fall below χ²₁(0.95).

## Build it

```bash
python -m videos.stats.stats14.compute         # once (a few minutes; cached in .cache/stats14)
python tools/build.py stats14 -q l             # fast 480p preview
python tools/build.py stats14                  # 1080p30 -> renders/stats14.mp4
python tools/qa_scene.py stats14 ChallengerFit
python tools/lecture_length.py stats14 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | 27 January 1986 | 7 flights with distress, r = 0.02; all 16 without at ≥ 66 °F; forecast 31 °F |
| 1 | Why not least squares | p̂ = 2.90 − 0.0374T; p̂(31) = 1.75, p̂(85) = −0.27 |
| 2 | Logistic regression | logit p̂ = 15.04 − 0.232T; p̂ = 0.5 at 64.8 °F; p̂(70) = 0.23, p̂(53) = 0.94; OR per 10 °F colder 10.2 [1.8, 173]; logit/probit 1.72 |
| 3 | Fitting by maximum likelihood | IRLS from 0: ℓ = −15.94, −10.59, −10.18, −10.158, …; D = 20.32 vs D₀ = 28.27, LR = 7.95, p = 0.0048; Wald z = −2.14, p = 0.032 |
| 4 | The Challenger fit | η̂(31) = 7.85, SE 4.04; Wald p ∈ [0.48, 1]; profile η ∈ [1.41, 18.4], p ∈ [0.80, 1]; binomial model: each ring 0.82 |
| 5 | Poisson regression | 7.7 per 1,000 at 50; rate ratio per decade 1.554 [1.535, 1.574]; men 0.986 [0.94, 1.03]; D = 31.0 on 25 df, φ̂ = 1.22 |
| 6 | Overdispersion | φ̂ = 22.3; slope SE 0.021 (Poisson), 0.101 (quasi), 0.179 (sandwich) |
| 7 | Two-way tables | men 44.5% vs women 30.4%; X² = 92.2; OR 1.84 [1.62, 2.09], RR 1.47; dept × admission X² = 779, sex × dept 1,068 |
| 8 | Simpson's paradox | A: women 82% vs men 62%; women ahead in 4 of 6 |
| 9 | Three-way tables | OR_MH = 0.905; CMH X² = 1.52, p = 0.22; women's adjusted log-odds +0.100 (SE 0.081) vs −0.610 pooled; Breslow–Day 18.8, p = 0.002 (without A: 2.6, p = 0.63) |
| 10 | Case–control studies | Doll & Hill OR 14.0 [3.3, 59]; World slopes 0.451 (all), 0.493 (cohort of 40,000), 0.411 (400 + 400); intercept shift 4.68 vs 4.63 predicted |
| 11 | Scoring predictions | AUC 0.725 (age), 0.992 (age + tests); Brier 0.00990 (base), 0.00983 (age), 0.01099 (odds × 4), 0.00475 (with tests) |
| 12 | Outro | — |

## Sources

- **Challenger.**
  - Report of the Presidential Commission on the Space Shuttle Challenger Accident (1986).
  - S. Dalal, E. Fowlkes & B. Hoadley, *JASA* 84 (1989); M. Lavine, *JASA* 86 (1991).
  - E. Tufte, *Visual Explanations* (1997), ch. 2.
- **Logistic and Poisson regression.**
  - J. Berkson, *JASA* 39 (1944); C. Bliss, *Science* 79 (1934); D. Cox, *JRSS B* 20 (1958).
  - J. Nelder & R. Wedderburn, *JRSS A* 135 (1972); R. Wedderburn, *Biometrika* 61 (1974).
  - M. Greenwood & G. U. Yule, *JRSS* 83 (1920).
- **Tables.**
  - P. Bickel, E. Hammel & J. W. O'Connell, *Science* 187 (1975); E. Simpson, *JRSS B* 13 (1951); G. U. Yule, *Biometrika*
    2 (1903).
  - B. Woolf, *Ann. Hum. Genet.* 19 (1955); W. Cochran, *Biometrics* 10 (1954); N. Mantel & W. Haenszel, *JNCI* 22 (1959).
  - N. Breslow & N. Day, *Statistical Methods in Cancer Research* I (1980).
- **Case–control studies.** R. Doll & A. B. Hill, *BMJ* 2 (1950); J. Cornfield, *JNCI* 11 (1951); R. Prentice & R. Pyke,
  *Biometrika* 66 (1979).
- **Scoring.**
  - G. Brier, *Monthly Weather Review* 78 (1950); A. Murphy, *J. Appl. Meteor.* 12 (1973).
  - I. J. Good, *JRSS B* 14 (1952); J. Hanley & B. McNeil, *Radiology* 143 (1982).
- **Textbooks.**
  - A. Agresti, *Categorical Data Analysis* (3rd ed., 2013).
  - P. McCullagh & J. Nelder, *Generalized Linear Models* (2nd ed., 1989).
  - D. Hosmer, S. Lemeshow & R. Sturdivant, *Applied Logistic Regression* (3rd ed., 2013).

## Problems and solutions

**1. Reading the Challenger coefficients.**

*Solution.* At 60 °F, η = 15.04 − 0.232 × 60 = 1.11, so p = 1/(1 + e^(−1.11)) = 0.75. Ten degrees colder changes the
log-odds by +2.32, so the odds multiply by e^2.32 = 10.2.

**2. The logistic score and Hessian.**

*Solution.* ℓ(β) = Σ[yᵢηᵢ − log(1 + e^ηᵢ)], with ηᵢ = xᵢᵀβ.
- **Score:** ∂/∂β of log(1 + e^η) is pᵢxᵢ, so ∇ℓ = Σ(yᵢ − pᵢ)xᵢ = Xᵀ(y − p).
- **Hessian:** ∂pᵢ/∂β = pᵢ(1 − pᵢ)xᵢ, so ∇²ℓ = −Σpᵢ(1 − pᵢ)xᵢxᵢᵀ = −XᵀWX.

The Hessian is negative definite whenever X has full rank, so ℓ is concave and the maximum is unique when it exists.

**3. A rate ratio.**

*Solution.* RR = (30/10,000)/(20/20,000) = 3. Then SE(log RR) = √(1/30 + 1/20) = 0.289. The 95% interval is
3 × e^(±1.96 × 0.289) = [1.70, 5.28].

**4. Kidney stones** (Charig et al., *BMJ* 1986).

*Solution.*
- **Small stones:** A cures 93%, B 87%.
- **Large stones:** A cures 73%, B 69%.
- **In total:** A cures 273/350 = 78%, B 289/350 = 83%.

A is better for both kinds of stone. B looks better in total because it was given mostly small stones, which are
easier to cure: 270 of B's 350 patients, against 87 of A's. Stone size affected both which treatment was used and
the chance of a cure, so compare within stone size.

**5. The odds ratio's symmetry.**

*Solution.* Comparing rows gives (a/b)/(c/d) = ad/(bc). Comparing columns gives (a/c)/(b/d) = ad/(bc), the same.

**6. The Brier score of a constant forecast.**

*Solution.* E[(q − y)²] = q² − 2qπ + E[y²]. Since E[y²] = π, this equals q² − 2qπ + π = (q − π)² + π(1 − π). It is
smallest at q = π, so the score is proper. The minimum is π(1 − π), which is 0.0099 for π = 0.01: the "always 1%"
forecaster of chapter 11.

## Where it comes back

| Idea | Returns in |
|---|---|
| probabilities as beliefs | 15 |
| exact and permutation tests, the bootstrap | 16 |
| likelihood theory: Wald, score and LR; Hauck–Donner | 22 |
| GLMs in full: exponential families, quasi-likelihood | 24 |
| random effects for clustered counts | 25 |
| classification, cross-validation | 19, 28 |
| calibration and prediction with guarantees | 34 |
| causal readings of tables | 35, 36 |
| missing data and measurement error | 41 |
| the Coverage Board | every part; 65 |

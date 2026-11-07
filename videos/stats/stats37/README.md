# Statistics, Built — Part 37: Natural Experiments

Part 37 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the seventeenth part of Stage III, Master's. Part 36 adjusted for measured
confounders and asked how wrong an unmeasured one could make us. This part looks for pieces of the world that were
randomized by accident: instruments, cutoffs, policies that start in some places and not others, and single treated
units with many possible controls. When no design identifies the answer, it bounds it.

The part builds `statkit.quasi` and an instrument, the cutoff lens (`CutoffLens`): binned means on either side of a
cutoff, a triangular-kernel window, local polynomial fits and the jump between them. It adds three World blocks:
- a schooling survey with quarter of birth as an instrument;
- a scholarship awarded at an exam score of 60;
- a staggered rollout of a jobs programme across the 200 towns.

Its real data are:
- Snow's Table IX, with printed-rate arithmetic disclosed;
- Card & Krueger's means;
- the Prop 99 cigarette panel (39 states, 1970–2000), from R's tidysynth package (MIT licence).

It opens with Snow (1855): Southwark & Vauxhall drew water below the sewers, while Lambeth had moved upstream in 1852.
Their pipes ran down the same streets. The numbers are 315 vs 37 cholera deaths per 10,000 houses, and 59 in the rest
of London as printed. That last rate is an arithmetic error: 1,422/256,423 × 10,000 = 55.46. The table distinguishes printed rates from calculations; the two-company mortality ratio from counts is 8.40 deaths per house, not an individual infection-risk ratio.

From there the part covers:
- **The credibility revolution.** Leamer (1983); Angrist & Pischke (2010); four designs and what each identifies; the
  2021 Nobel.
- **Instruments.** Wright (1928); relevance, independence, exclusion, monotonicity.
  - The World's survey (200,000 adults): Q1 births have 0.146 fewer years of schooling and 0.011 lower log wages.
  - Wald 0.0751 vs truth 0.075; OLS 0.162. 2SLS with three quarters gives 0.072 (0.013), F = 75.
  - The draft lottery (Angrist 1990).
- **Weak instruments.**
  - One survey of 5,000: F = 9.0; 2SLS 0.098 (90% CI −0.001 to 0.196); AR set −0.052 to 0.192.
  - Across 1,000 surveys: median F 5.6, and 78% below 10.
  - The size of the 5% t-test: up to 16% at μ² = 1 with ρ = 0.9.
  - Staiger–Stock; Stock–Yogo; tF (in the just-identified Gaussian approximation, F must exceed 104.7 for the usual 1.96 cutoff; 3.43 at F = 10).
  - AR sets: an interval 76%, two rays 13%, the whole line 11%.
- **Many instruments.** Quarter × region gives 30 instruments.
  - 2SLS median 0.147 (OLS 0.162); LIML 0.091.
  - Bound–Jaeger–Baker fake quarters: 2SLS 0.180 (SE 0.033), F = 0.87.
  - Mendelian randomization with 40 variants, 10 pleiotropic: IVW 0.339, MR-Egger 0.267 (0.047) with intercept
    0.0045, truth 0.30.
- **Regression discontinuity.** Thistlethwaite & Campbell (1960). The World's scholarship (40,000 school-leavers):
  - scholars vs the rest +46.5 thousand;
  - at the IK-inspired teaching plug-in bandwidth (h = 33.4), local linear 3.59 (0.12) vs truth 3.0, and local quadratic 2.99 (0.16);
  - a bandwidth sensitivity plot; this plug-in is not independently certified as the exact IK reference implementation or finite-sample optimum;
  - robust bias correction (Calonico, Cattaneo & Titiunik 2014);
  - one study of 2,000: conventional 2.29–4.00, robust 1.27–3.58.
- **RD validity.**
  - Teachers re-mark 35% of the scripts at 56–59.9. McCrary's θ is 1.08 (z = 32) against −0.05 when marking is
    honest.
  - The aptitude jump is only −0.035 (z = −1.7), while the RD estimate collapses to 0.53.
  - Fuzzy RD: a take-up jump of 0.75; 2.25/0.75 = 2.99 (0.21); takers vs non-takers +37.4.
  - Lee's close elections; Caughey & Sekhon; Eggers et al.; a checklist.
- **Difference-in-differences.**
  - Card & Krueger: Pennsylvania 23.33 → 21.17, New Jersey 20.44 → 21.03, DiD +2.76 (1.36).
  - The rollout's 2009 cohort vs the never-treated: 0.66 vs truth 0.90; an event study.
- **DiD inference.**
  - Town shocks correlate 0.67 from year to year.
  - 1,000 placebo laws: OLS SEs reject 41%, town-clustered 5.5% (Bertrand, Duflo & Mullainathan found 45%).
- **Staggered adoption.**
  - 76/56/48 towns adopt in 2004/2009/2014 and 20 never; effects grow 0.7/0.3/0.05 a year; the true ATT is 3.96.
  - TWFE gives −0.49 (0.21).
  - Goodman-Bacon weights: vs never 0.25 (+2.84), early vs later 0.30 (+2.32), later vs already treated 0.45 (−4.14).
  - Callaway–Sant'Anna 3.83 (3.53–4.13); imputation 3.94.
  - Event studies: TWFE vs CS.
- **Honest parallel trends** (Rambachan & Roth 2023), on a seeded panel with a 0.2 a year pre-trend and a true effect
  of 1.0:
  - naive 1.17 (1.07–1.27);
  - linear extrapolation 0.97 (0.86–1.08), including the full covariance of pre- and post-period estimates;
  - breakdown at M = 0.87 under this specified linear-extrapolation departure bound;
  - relative magnitudes with simultaneous pre-jump uncertainty (Bonferroni), rather than treating the estimated pre-trend bound as known. These are explicit one-period teaching restrictions, not a full implementation of Rambachan–Roth Delta-SD inference.
- **Synthetic control** (Abadie, Diamond & Hainmueller 2010).
  - Weights: Utah 0.39, Montana 0.23, Nevada 0.20, Connecticut 0.11, New Hampshire 0.05; pre-RMSPE 1.66.
  - The gap is −26.6 packs in 2000, and −19.5 on average over 1989–2000.
  - Placebo ratios rank California 3rd of 39 (p = 0.077), and 3rd among the 29 states with pre-RMSPE at most twice California's (descriptive rank fraction 3/29 = 0.103).
- **Synthetic DiD** (Arkhangelsky et al. 2021). Placebo SEs:

  | Estimator | Estimate | SE |
  |---|---|---|
  | DiD | −27.3 | 17.5 |
  | SC | −19.5 | 10.9 |
  | SDID | −15.6 | 9.5 |

  Point estimates approximately reproduce the paper's Table 1; these placebo SEs differ from its reported SEs. Inference needs comparability/model assumptions across states. The time weights fall on 1986–88. A range of point estimates such as 15–25 packs is not a confidence interval or an assumption-free causal conclusion.
- **Panel data.**
  - Pooled 1.93 against FE = LSDV = Mundlak 0.985 (truth 1).
  - Nickell: FE 0.170 vs the formula's 0.169 (ρ = 0.5, T = 5); Anderson–Hsiao 0.499; Arellano–Bond.
- **Bounds.**
  - Manski's worst-case bounds with 19% and 30% non-response: [−0.15, 0.34] (finite-population causal effect 0.123).
  - Lee's plug-in trimming bounds for wages, with 14.7% of observed treated workers estimated as marginal: [−0.99, 1.40] (truth 1.0, naive 0.22).
  - The law of decreasing credibility.

Data:
- Snow, Card–Krueger and Prop 99 are the Museum's;
- the schooling survey, the scholarship and the rollout are the World's;
- the Mendelian randomization, honest-trends, panel and bounds examples are seeded simulations.

**Built in this part:**
- **`statkit.quasi`** ([`explainer/stats/kit/quasi.py`](../../../explainer/stats/kit/quasi.py)), checked in
  `tests/test_stats_kit_quasi.py`:
  - **Instruments:** OLS with HC1 and cluster-robust SEs; 2SLS with first-stage F; Anderson–Rubin tests and exact homoskedastic Gaussian linear-IV
    confidence sets; LIML; IVW and MR-Egger.
  - **Regression discontinuity:** one-sided local polynomials with triangular weights; sharp and fuzzy RD;
    conventional and robust bias-corrected intervals; an IK-inspired teaching bandwidth; McCrary's density test.
  - **Difference-in-differences:** TWFE with clustered SEs; event studies; the Goodman-Bacon decomposition;
    Callaway–Sant'Anna with influence-function SEs; the imputation estimator; simplified sensitivity illustrations (linear-trend departure and relative
    magnitudes). The chapter uses local helpers retaining joint event-time covariance and uncertainty in the estimated pre-jump bound.
  - **Synthetic control and panels:** simplex least squares; synthetic control with placebo ratios; synthetic DiD;
    the within estimator; Nickell's bias; Anderson–Hsiao.
  - **Bounds:** Manski; Lee.
- **The World** gains `schooling`, `scholarship` and `rollout` (with `rollout_panel` for fresh draws).
- **The Museum** gains `SNOW`, `CARD_KRUEGER` and `prop99()`.
- **The cutoff lens** (`CutoffLens` in `explainer/stats/viz.py`).

The Coverage Board gains eight rows (90% intervals; the last two are 5% tests):

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| 2SLS, 30 weak instruments | World survey, n = 5,000 | 17.6% | broken |
| Anderson–Rubin set | same | 89.4% | kept |
| local linear RD, conventional CI | World scholarship, n = 2,000 | 66.3% | broken |
| robust bias-corrected RD | same | 90.8% | kept |
| TWFE, clustered CI (for the ATT) | World rollout, 200 towns | 0.0% | broken |
| Callaway–Sant'Anna | same | 88.8% | kept |
| DiD test, OLS SEs (size) | placebo laws on the World's towns | 41.1% | broken |
| DiD test, town-clustered SEs (size) | same | 5.5% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats37.compute   # once (about two minutes)
python tools/build.py stats37 -q l                         # fast 480p preview
python tools/build.py stats37                              # 1080p30 -> renders/stats37.mp4
python tools/qa_scene.py stats37 Staggered
python tools/lecture_length.py stats37 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Snow's Grand Experiment | 315 vs 37 per 10,000 houses |
| 1 | The credibility revolution | four designs |
| 2 | Instrumental variables | Wald 0.0751 vs OLS 0.162 |
| 3 | Weak instruments | median F 5.6; tF 104.7 |
| 4 | Many instruments; Mendelian randomization | 2SLS 0.147, LIML 0.091; Egger 0.267 |
| 5 | Regression discontinuity | 3.59 vs 2.99 (truth 3.0) |
| 6 | RD validity | McCrary z = 32; fuzzy 2.99 |
| 7 | Difference-in-differences | Card–Krueger +2.76 |
| 8 | DiD inference | placebo laws: 41% vs 5.5% |
| 9 | Staggered adoption | TWFE −0.49 vs truth 3.96 |
| 10 | Honest parallel trends | 1.17 → 0.97; breakdown 0.87 under the teaching bound |
| 11 | Synthetic control | −26.6 packs in 2000 |
| 12 | Synthetic DiD | −15.6 / −19.5 / −27.3 |
| 13 | Panel data | Nickell: 0.170 for 0.5 |
| 14 | Bounds | Manski [−0.15, 0.34]; Lee [−0.99, 1.40] |
| 15 | Outro | — |

## Sources

- **Snow and the revolution.**
  - J. Snow, *On the Mode of Communication of Cholera* (2nd ed., 1855).
  - E. Leamer, *AER* 73 (1983); J. Angrist & J.-S. Pischke, *JEP* 24 (2010), *Mostly Harmless Econometrics* (2009).
- **Instruments.**
  - P. Wright, *The Tariff on Animal and Vegetable Oils* (1928); T. Anderson & H. Rubin, *Ann. Math. Stat.* 20 (1949).
  - J. Angrist, *AER* 80 (1990); J. Angrist & A. Krueger, *QJE* 106 (1991); J. Bound, D. Jaeger & R. Baker, *JASA* 90
    (1995).
  - D. Staiger & J. Stock, *Econometrica* 65 (1997); J. Stock & M. Yogo (2005); D. Lee, J. McCrary, M. Moreira &
    J. Porter, *AER* 112 (2022).
- **Mendelian randomization.** G. Davey Smith & S. Ebrahim, *Int. J. Epidemiol.* 32 (2003); J. Bowden, G. Davey Smith &
  S. Burgess, *Int. J. Epidemiol.* 44 (2015).
- **Regression discontinuity.**
  - D. Thistlethwaite & D. Campbell, *J. Educ. Psychol.* 51 (1960); J. Hahn, P. Todd & W. van der Klaauw,
    *Econometrica* 69 (2001).
  - G. Imbens & K. Kalyanaraman, *REStud* 79 (2012); S. Calonico, M. Cattaneo & R. Titiunik, *Econometrica* 82 (2014).
  - J. McCrary, *J. Econometrics* 142 (2008); D. Lee, *J. Econometrics* 142 (2008).
  - D. Caughey & J. Sekhon, *Political Analysis* 19 (2011); A. Eggers et al., *AJPS* 59 (2015); A. Gelman &
    G. Imbens, *JBES* 37 (2019).
- **Difference-in-differences.**
  - D. Card & A. Krueger, *AER* 84 (1994), 90 (2000); D. Neumark & W. Wascher, *AER* 90 (2000).
  - M. Bertrand, E. Duflo & S. Mullainathan, *QJE* 119 (2004).
  - A. Goodman-Bacon, *J. Econometrics* 225 (2021); C. de Chaisemartin & X. D'Haultfœuille, *AER* 110 (2020).
  - B. Callaway & P. Sant'Anna, *J. Econometrics* 225 (2021); L. Sun & S. Abraham, *J. Econometrics* 225 (2021);
    K. Borusyak, X. Jaravel & J. Spiess, *REStud* (2024).
  - J. Roth, *AER: Insights* 4 (2022); A. Rambachan & J. Roth, *REStud* 90 (2023).
- **Synthetic control.**
  - A. Abadie & J. Gardeazabal, *AER* 93 (2003); A. Abadie, A. Diamond & J. Hainmueller, *JASA* 105 (2010).
  - D. Arkhangelsky, S. Athey, D. Hirshberg, G. Imbens & S. Wager, *AER* 111 (2021).
- **Panels.**
  - Y. Mundlak, *Econometrica* 46 (1978); S. Nickell, *Econometrica* 49 (1981).
  - T. Anderson & C. Hsiao, *JASA* 76 (1981); M. Arellano & S. Bond, *REStud* 58 (1991); D. Roodman, *Oxford Bull.
    Econ. Stat.* 71 (2009).
- **Bounds.** C. Manski, *AER P&P* 80 (1990), *Partial Identification of Probability Distributions* (2003); D. Lee,
  *REStud* 76 (2009).
- **Data.** Prop 99 via R's tidysynth (E. Dunford, MIT licence).

## Problems and solutions

1. **Wald = 2SLS.** With Z binary and a constant, the first stage fits D̂ = E[D | Z]. Then
   cov(Y, Z)/cov(D, Z) = (E[Y | Z=1] − E[Y | Z=0])/(E[D | Z=1] − E[D | Z=0]), because cov(V, Z) =
   Var(Z)(E[V | Z=1] − E[V | Z=0]) for any V.
2. **AR is robust.** Under H₀, Y − b₀D = Wγ + u with u independent of Z (exclusion and independence).
   - The regression of Y − b₀D on (W, Z) has instrument coefficients exactly zero.
   - With independent homoskedastic Gaussian errors conditional on the valid instruments and exogenous controls, the F statistic is exactly F(q, n − k); the first stage never enters. Mere marginal normality is insufficient. A heteroskedastic model needs robust AR inference.
3. **The MSE bandwidth.** MSE(h) = B²h⁴ + V/(nh). Setting the derivative 4B²h³ − V/(nh²) to zero gives
   h = (V/(4B²n))^{1/5} ∝ n^{−1/5}.
   - In this leading-term, nonzero-curvature approximation, B²h⁴ = V/(4nh), so bias² = variance/4 and absolute bias/SD = ½. Absolute bias can tend to zero while remaining material relative to the standard error.
4. **TWFE in the 2×2.** With two units, or groups, and two periods, the two-way demeaned treatment is ±¼.
   - The regression coefficient is then the double difference of the four means.
5. **Nickell with two periods.** With observations y₀, y₁, y₂, fixed effects equals first differences: Δy₂ on Δy₁.
   - plim = ρ + cov(Δy₁, Δε₂)/var(Δy₁) = ρ − σ²/(2σ²/(1 + ρ)) = ρ − (1 + ρ)/2.
   - This matches `nickell_bias(ρ, 2)`.
6. **Manski.** Let E[Y(1)] ∈ [r₁ȳ₁, r₁ȳ₁ + 1 − r₁] and E[Y(0)] ∈ [r₀ȳ₀, r₀ȳ₀ + 1 − r₀].
   - The difference lies between the lower end of the first minus the upper end of the second, and the reverse.
   - The width is (1 − r₁) + (1 − r₀) = 2 − r₁ − r₀. Causal interpretation also needs random treatment or other identification of the arm means. These plug-in endpoints are not confidence limits.

## Glossary

- **Natural experiment**: variation in treatment that is as good as random, found rather than made.
- **Instrument; exclusion; relevance**: a variable that moves the treatment and reaches the outcome only through it.
- **First stage; reduced form; Wald ratio; 2SLS**: the instrument's effects on treatment and on outcome; their ratio;
  its general form.
- **Weak instruments; F; tF; Anderson–Rubin**: instruments that barely move the treatment; the diagnostic; the adjusted
  critical value; the test that needs no strength.
- **LIML**: a k-class estimator often less median-biased under standard weak/many-instrument conditions; this is not a universal finite-sample guarantee.
- **Mendelian randomization; pleiotropy; MR-Egger**: genes as instruments; genes acting through other paths; the
  intercept allowing average directional pleiotropy under InSIDE and additional strength/measurement-error conditions.
- **Regression discontinuity (sharp, fuzzy); running variable; bandwidth**: treatment by a cutoff in a score.
- **Robust bias correction**: subtracting the estimated smoothing bias, with an SE that includes its noise.
- **McCrary test; donut**: a jump in the running variable's density; dropping the points nearest the cutoff.
- **Difference-in-differences; parallel trends; event study**: two changes subtracted; the assumption; one DiD per
  period around adoption.
- **Placebo laws; clustered SEs**: invented policies for checking a test's size; SEs that allow correlation within
  units.
- **Staggered adoption; forbidden comparison; Goodman-Bacon decomposition**: treatment at different times;
  already-treated units used as controls; TWFE as a weighted average of 2×2s.
- **Callaway–Sant'Anna; imputation estimator**: estimators that compare only with untreated cells.
- **Honest DiD; breakdown value**: inference allowing bounded violations of parallel trends; the violation at which a
  conclusion changes under a specified restriction. The teaching linear-extrapolation bound differs from the full Delta-SD framework.
- **Synthetic control; SDID**: a convex combination of controls matching the treated unit; with intercepts and time
  weights.
- **Fixed effects; within transformation; Nickell bias; Anderson–Hsiao**: unit intercepts; demeaning; the
  dynamic-panel bias; differencing with lagged instruments.
- **Partial identification; Manski bounds; Lee bounds; law of decreasing credibility**: what the data imply without
  assumptions, and the trade between assumptions and credibility.

## Where it comes back

- **Part 38**: persistence and unit roots.
- **Part 39**: spillovers across space.
- **Part 41**: selection and measurement error.
- **Part 47**: weak-instrument asymptotics.
- **Part 49**: influence functions for DiD and IV estimators.
- **Part 52**: many instruments as a high-dimensional problem.
- **Part 57**: permutation inference.
- **Part 60**: external validity and distribution shift.
- **Part 62**: partial identification, sensitivity and surrogates.

## Verification scope

All sixteen chapters, numerical inputs, solutions and helpers were reviewed. The local matrix-free AR inversion agrees with independent F-test inversion without constructing an n-by-n projection. Trend sensitivity retains the covariance induced by the common reference period. Fractional Lee trimming agrees with independent linear programming. World sampling studies use fixed seeded populations; their coverage summaries illustrate these draws and assumptions rather than certify general theorems.

Scores in the scholarship example are recorded in tenths. Continuous-running-variable RD and density references are therefore teaching approximations requiring local smoothness, not an exact fixed-grid identification guarantee. Fuzzy RD additionally needs local exclusion, monotonicity and a nonzero take-up jump. DiD needs no anticipation and an appropriate interference assumption as well as parallel trends. Placebo ranks and single-treated-state standard errors need an assignment or comparable-shocks justification.

Full weak-IV histogram denominators retain all 1,000 studies; observations outside the displayed range are disclosed instead of accumulated into the edge bins. Matching pre-treatment paths does not establish post-treatment counterfactual validity.

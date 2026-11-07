# Statistics, Built — Part 20: The Analysis

Part 20 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). It is the capstone of Stage II and of the bachelor's degree. It introduces no
new method. Instead it takes one question through every stage of a real analysis, on real public data, and then runs
the identical code on the World, where the answer is known.

**The question.** How does blood pressure depend on salt?
- Untreated adults in this weighted analytic sample report about 3,550 mg of sodium on the recall day; the guideline is under 2,300.
- Randomized trials find 2–3 mm Hg of systolic pressure per gram of sodium.
- In NHANES 2017–2018 the crude slope is −0.14 mm Hg per gram.

The part distinguishes recall-day associations from causal trial effects:
- **The estimand.** Population, outcome, exposure (usual intake, not yesterday's), contrast and what is held fixed.
  Descriptive vs causal readings. An illustrative plan presented before the results; this is not evidence of prospective registration.
- **The design and its weights.** NHANES's four stages; 15 strata × 2 masked PSUs, so 15 degrees of freedom; the
  oversampling of Black, Asian, Hispanic and older adults.
  - Weights run from 4,580 to 419,763 and sum to 236 million.
  - Mean systolic pressure is 123.9 weighted against 127.1 raw.
  - The design effect for the mean is 3.6, so n_eff ≈ 1,365.
- **Cleaning.** A codebook first: recall reliability codes, age top-coded at 80, a diastolic of zero. Readings 2–3
  are averaged. Energy outside 500–5,000 kcal is implausible. The decision log runs 5,533 → 3,071, and excluding the
  1,319 adults on BP medicine changes the estimand.
- **Exploration.**
  - Pressure: median 118, with 24% at 130 or above.
  - Sodium: median 3.26 g, with 76% over the guideline.
  - Pressure rises with age while sodium falls with age: a confounder pointing the other way.
  - Sodium and energy correlate at r = 0.75; decile means are flat.
- **A first model.** Weighted least squares on sodium, age, sex, BMI and energy. Sodium: +0.07 mm Hg per g, 95% CI
  −0.50 to +0.63 (t₁₅), p = 0.81. The displayed trial effects lie outside this recall-day interval, but target different exposures and estimands. Why weight a regression (DuMouchel & Duncan;
  Solon, Haider & Wooldridge).
- **Checking it.**
  - Binned residuals and a Q-Q plot (skewness 1.05).
  - A restricted cubic spline for age: a design Wald F₂,₁₅ test suggests curvature (p = 0.022), but sodium moves only from +0.07 to
    +0.04.
  - An unplanned sodium × age interaction (p = 0.02) is reported as exploratory.
  - Dropping the top 1% by Cook's distance gives −0.02.
- **Uncertainty.** Four SEs for the slope: model 0.229, sandwich 0.311, linearized 0.266, Rao–Wu PSU bootstrap 0.272.
  Use t with 15 df rather than z. The design effect is 2.7 for a mean and about 1.4 for a slope.
- **Sensitivity.**
  - A specification curve of 64 analyses: −0.18 to +0.64, none distinguishable from zero.
  - Medicine users and two-day means are the choices that matter.
  - Two-recall correlation r = 0.32 (unweighted). The weighted conditional calibration slopes are 0.24 without energy and 0.06 with energy. They represent reliability only under classical error assumptions, which correlated reporting errors and noisy covariates can violate.
  - Regression calibration without energy gives +0.37, approximate CI −1.9 to +2.7. With energy, +0.65 ± 8.7. Both stages enter the joint design delta-method variance; weak calibration makes even these approximate intervals fragile.
- **Causal or not?** A causal diagram. The diagnosed eat a little less sodium but no less per calorie. DASH-Sodium
  (6.7 mm Hg) and He, Li & MacGregor (4.2 mm Hg per 4.4 g of salt). Internal vs external validity, and what the
  report may and may not say.
- **The same pipeline on the World.** The World's new health block has a true effect of 1.5 mm Hg per g, a
  diagnosis loop and noisy recalls. Over 200 NHANES-shaped surveys:
  - one-day recall averages 0.23 (coverage 0%);
  - joint calibration averages 0.74 (69.5%);
  - even true intake averages 0.96 (53.5%): diagnosis, medication selection and model projection separate the descriptive slope from the structural effect.
  - A 400-person randomized trial recovers 1.93 ± 1.20, and covers the truth in 95.8% of 2,000 repeats.
- **Communicating.** Three bad sentences and one good one; a one-page report; graphic integrity (axis limits change visual emphasis; neither scale proves signal or noise); the appendix.
- **Reproducibility and ethics.**
  - The chain from the CDC's files to every number; a SHA-256 fingerprint and seeds.
  - NHANES's privacy layers and consent.
  - Race as a social category; publishing nulls; interests.
  - A thirteen-item checklist.
- **The BSc problem set.** Six problems spanning Stages I–II, solved on screen.

Numerical results are computed in [`compute.py`](compute.py) by the pipeline in [`pipeline.py`](pipeline.py):
- the data are NHANES 2017–2018 (CDC/NCHS, public domain), extracted by
  [`tools/nhanes_extract.py`](../../../tools/nhanes_extract.py) into `explainer/stats/data/nhanes_bp.csv`
  (5,533 adults, 29 columns, SHA-256 `ae9be143…`); the SEQN-aligned two-day weight supplement is
  [`data/nhanes_day2_weights.csv`](data/nhanes_day2_weights.csv). CDC requires **WTDR2D** when an analysis uses both recalls;
  the original extract remains unchanged. All 5,533 rows reproduce byte-for-byte from current CDC downloads;
- the replays use the World's health block.

**Built in this part:**
- **The capstone pipeline** ([`pipeline.py`](pipeline.py)):
  - `clean`, the decision log of chapter three;
  - `fit`, the pre-specified model with design-based SEs, and its 64 variants;
  - `calibrated`, regression calibration with two-day dietary weights and joint two-stage design variance;
  - `world_frame`, an NHANES-shaped survey of the World (10 strata, 2 PPS town draws with replacement each, 250 adults per draw, exact age-stratum sampling probabilities and Hansen–Hurwitz draw weights).

  All of them run unchanged on NHANES and the World.
- **`statkit.capstone`** ([`explainer/stats/kit/capstone.py`](../../../explainer/stats/kit/capstone.py)):
  `DecisionLog`, restricted cubic splines, reliability from replicates, and regression calibration.
- **`statkit.survey` additions**: `svy_mean` and `svy_ols` (Taylor linearization over strata and PSUs, with model and
  sandwich SEs alongside), and `psu_bootstrap_weights` (Rao & Wu 1988).

  Both are checked in `tests/test_stats_kit_capstone.py`.
- **The World's health block** (`World.health`):
  - BMI, energy and usual sodium;
  - systolic pressure with `SODIUM_EFFECT` = 1.5 mm Hg per g;
  - diagnosis, salt-cutting and medicine;
  - three readings and two 24-hour recalls.

  It adds a block without changing any other.
- **The Museum's NHANES extract** (`museum.nhanes()`).

The Coverage Board gains three rows: 95% intervals for the World's sodium effect.

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| one-day recall, design t CI | the World's sodium effect, 5,000 surveyed | 200 | 0.0% | broken |
| regression calibration, design t CI | the World's sodium effect, 5,000 surveyed | 200 | 69.5% | broken |
| randomized trial, z CI | the World's sodium effect, 400 randomized | 2,000 | 95.8% | kept |

## Build it

```bash
# once: the data (already in the repository; this rebuilds it from the CDC)
for f in DEMO_J BPX_J BMX_J DR1TOT_J DR2TOT_J BPQ_J; do
  curl -sSL -o $f.xpt https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/$f.xpt
done
python tools/nhanes_extract.py . explainer/stats/data/nhanes_bp.csv
python tools/nhanes_extract.py --day2-weights . explainer/stats/data/nhanes_bp.csv videos/stats/stats20/data/nhanes_day2_weights.csv

python -m videos.stats.stats20.compute --force # recompute after changes, including dependent report and board results
python tools/build.py stats20 -q l             # fast 480p preview
python tools/build.py stats20                  # 1080p30 -> renders/stats20.mp4
python tools/qa_scene.py stats20 Sensitivity
python tools/lecture_length.py stats20 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Salt and blood pressure: a question | mean 3,551 mg; 76% over 2,300; 9,254 interviewed, 8,704 examined; crude slope −0.14 (3,071 adults) |
| 1 | From question to estimand | 236 million adults; two recalls r = 0.32 (2,659); 2⁶ = 64 analyses |
| 2 | The design and its weights | 15 strata, 30 PSUs; Black 24% vs 11%, Asian 14% vs 6%, 60+ 39% vs 29%; weights 4,580–419,763, median 26,549; 127.1 vs 123.9; SE 0.49 vs 0.26 (weighted population SRS reference), deff 3.6 |
| 3 | Cleaning | codes 4,742 / 33 / 490; 382 at 80; 87 diastolic zeros; first reading +0.6; 57 under 500 kcal, 67 over 5,000; funnel 5,533 → 3,071 |
| 4 | Exploration | median 118 (103–141), 24% ≥ 130; sodium median 3.26, mean 3.55; r(sodium, energy) = 0.75; deciles 120 → 122 |
| 5 | A first model | age +0.40, female −4.97, BMI +0.52, energy +0.07, sodium +0.07 [−0.50, +0.63], p = 0.81 |
| 6 | Checking it | skewness 1.05; spline Wald F₂,₁₅ = 4.98, p = 0.022, sodium +0.04; interaction −0.041 (SE 0.016); top 1% dropped: −0.02 |
| 7 | Uncertainty | SEs 0.229 / 0.311 / 0.266 / 0.272; t₁₅ = 2.13; mean 120.4, SE 0.54 vs 0.33 |
| 8 | Sensitivity | 64 slopes −0.18 to +0.64; medicine +0.20 → −0.07; two days +0.01 → +0.12; λ 0.24 and 0.06; calibrated without energy +0.37 ± 2.32; with energy +0.65 ± 8.72 |
| 9 | Causal or not? | told 33%; sodium 3.40 vs 3.55, per 1,000 kcal 1.66 vs 1.64; age 58 vs 44; DASH-Sodium 6.7; meta-analysis 4.2 per 4.4 g salt |
| 10 | The same pipeline on the World | one survey 0.35 / 1.23 / 1.00; 200 surveys 0.23 / 0.74 / 0.96, coverage 0 / 69.5 / 53.5%; trial 1.93 ± 1.20, 95.8% |
| 11 | Communicating | the one-page report; decile axis 117–125 vs 0–140 |
| 12 | Reproducibility and ethics | SHA-256 `ae9be143…`; 382 ages and 821 income ratios top-coded |
| 13 | The BSc problem set | six problems, below |
| 14 | Outro | the Transcript: the BSc |

## Sources

- **Data.** CDC/NCHS, *National Health and Nutrition Examination Survey 2017–2018*: data files DEMO_J, BPX_J,
  BMX_J, DR1TOT_J, DR2TOT_J, BPQ_J; *NHANES Analytic Guidelines* and the sample design documentation.
- **Salt and blood pressure.**
  - F. Sacks et al., "Effects on blood pressure of reduced dietary sodium and the DASH diet", *NEJM* 344 (2001).
  - F. He, J. Li & G. MacGregor, *BMJ* 346 (2013), f1325.
  - INTERSALT Cooperative Research Group, *BMJ* 297 (1988).
  - W. Willett, *Nutritional Epidemiology* (3rd ed., 2013).
- **Methods.**
  - T. Lumley, *Complex Surveys* (2010).
  - J. Rao & C. Wu, *JASA* 83 (1988).
  - W. DuMouchel & G. Duncan, *JASA* 78 (1983); G. Solon, S. Haider & J. Wooldridge, *J. Human Resources* 50 (2015).
  - R. Carroll, D. Ruppert, L. Stefanski & C. Crainiceanu, *Measurement Error in Nonlinear Models* (2nd ed., 2006).
  - F. Harrell, *Regression Modeling Strategies* (2nd ed., 2015).
  - U. Simonsohn, J. Simmons & L. Nelson, *Nature Human Behaviour* 4 (2020).
  - A. Gelman & E. Loken, "The garden of forking paths" (2013).

## Problems and solutions

**1. Two positive tests (Parts 2, 15).** Assume conditional independence within both disease-status groups.

*Solution.* P(both + | sick) = 0.81 and P(both + | well) = 0.0025. So P(sick | both +) = 0.0081/(0.0081 + 0.002475)
≈ 0.766. One positive test alone gives 0.009/(0.009 + 0.0495) ≈ 0.154.

**2. A survey's margin of error (Parts 8, 18).**

*Solution.* As an SRS, 1.96 × 17/√4,948 = 0.474. With a design effect of 3.6, multiply by √3.6: 0.90. The effective
sample size is 4,948/3.6 ≈ 1,374.

**3. Attenuation (Part 12).**

*Solution.* λ = Var X/(Var X + Var U) = 1/3, so the slope tends to 2.5/3 ≈ 0.83. The mean of k recall days has noise
variance 2/k, so λ_k = 1/(1 + 2/k). For k = 7, λ = 7/9 ≈ 0.78.

**4. Sizing a trial (Parts 10, 13).**

*Solution.* Δ = 2.3 × 2.5 = 5.75 mm Hg. Then n = 2(1.96 + 0.8416)² × 15²/5.75² ≈ 106.8, so 107 per arm.

**5. Counting bootstrap replicates (Parts 16, 18).**

*Solution.* Each of the 15 strata draws n_h − 1 = 1 of its 2 PSUs, so there are 2¹⁵ = 32,768 equally likely
replicates. The PSU-level information has 30 − 15 = 15 degrees of freedom however many replicates are drawn.

**6. Sixty-four forks (Parts 10, 19).**

*Solution.*
- **Independent analyses.** 1 − 0.95⁶⁴ ≈ 0.962.
- **Bonferroni.** Testing each at 0.05/64 ≈ 0.00078 keeps the family-wise rate at or below 0.05, by the union bound,
  whatever the dependence.
- **Our 64.** They are highly correlated, since they share the data and most choices, so the effective number of
  opportunities can be smaller. Correlation does not explain or guarantee the absence of a significant result. None was significant here.

## Glossary

- **Estimand**: the precise target: population, variable, summary, contrast, and what is held fixed.
- **Descriptive vs causal estimand**: how groups differ as they are, vs how outcomes would change under an
  intervention.
- **Usual intake**: a person's long-run average consumption, the exposure that matters; a 24-hour recall measures one
  day.
- **Analysis plan (pre-specification)**: the sample, model and outputs fixed before the results are seen.
- **Masked variance units**: NHANES's public pseudo-strata and pseudo-PSUs, built for correct SEs without revealing
  locations.
- **Survey weight**: inverse selection probability, adjusted for nonresponse and post-stratified to Census totals.
- **Design effect; effective sample size**: the variance ratio against an SRS, and n divided by it.
- **Taylor linearization**: design-based variance of a nonlinear estimator from the PSU totals of its linearized
  scores.
- **Rao–Wu bootstrap**: resampling n_h − 1 PSUs per stratum, with rescaled weights.
- **Decision log**: every cleaning step, with its reason and count.
- **Top-coding**: replacing extreme values (age 80+, income ratio 5+) by a cap, for privacy.
- **Energy adjustment**: including total energy so that the exposure is diet composition rather than diet size.
- **Restricted cubic spline**: piecewise cubic, linear beyond the outer knots; a check for nonlinearity.
- **Specification curve (multiverse)**: the estimate under every reasonable combination of analytic choices.
- **Reliability (attenuation factor) λ**: Var(X | Z)/Var(W | Z); the factor by which classical error shrinks a slope.
- **Regression calibration**: replacing W by E[X | W, Z], estimated from a replicate.
- **Reverse causation**: the outcome affecting the exposure (diagnosis changes diet).
- **Internal and external validity**: whether a study answers its own question correctly, and whether that answer
  generalizes.
- **Reproducible pipeline**: raw data, code, seeds and versions from which every number can be rebuilt.

## Where it comes back

| Idea | Returns in |
|---|---|
| how estimators are computed | 21 |
| the linear model in depth | 23 |
| multilevel models, MRP for surveys | 25 |
| model choice | 28 |
| causal inference from observational data | 35, 36, 37 |
| measurement error and missing data | 41 |
| inference after selection | 56 |
| privacy for public data | 63 |
| the Coverage Board | every part; 65 |

## Review status

The source and numerical review corrected two-day weights, joint calibration uncertainty, the centered interaction slope,
the small-design Wald test and the SRS reference underlying the displayed design effect. Error-model and causal claims
are qualified. The toy World survey uses exact within-age inclusion probabilities. See the
[QA evidence](../../../docs/qa/evidence/stats20-polish-20261107/scientific-review.md) for validation and remaining visual gates.

The operational eligibility rules exclude positive recorded pregnancy tests and recorded current BP medication use.
Unknown pregnancy status and skipped medication items are retained as no recorded positive/use, not confirmed negatives.
Complete-case exclusions and this coding convention limit generalization; survey weights alone do not remove that bias.

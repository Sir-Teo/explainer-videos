# Statistics, Built — Part 36: Causes Without Experiments

Part 36 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the sixteenth part of Stage III, Master's. Part 35 showed why randomization
identifies causal effects. This part asks what can be learned without it, and at what cost in assumptions:
- identification: unconfoundedness and overlap, causal diagrams, the back door, the front door and the do-calculus;
- estimation: g-computation, propensity scores, weighting, double robustness, double machine learning;
- heterogeneous effects;
- sensitivity analysis;
- smoking and lung cancer;
- time-varying treatments.

The part builds `statkit.causal` (II) and an instrument, the causal graph (`CausalGraph`): nodes, arrows, highlighted
paths and conditioning boxes, backed by the kit's `DAG` with d-separation and the back-door criterion. Its real data are
the NSW job-training data (LaLonde 1986; Dehejia & Wahba 1999), from R's Matching (GPL-3) and MatchIt (GPL ≥ 2)
packages. Its test bed is an observational version of the World's clinic, in which doctors choose who is treated and
the World knows both potential outcomes.

It opens with LaLonde's (1986) test. In Dehejia & Wahba's subsample (185 trainees, 260 randomized controls):
- the experiment estimates $1,794 (95% CI $479 to $3,109);
- against 429 PSID men, the raw difference is −$635, and OLS with covariates gives $1,548;
- the PSID men are older (28.0 vs 25.8), more often married (0.51 vs 0.19), less often black (0.20 vs 0.84), and
  earned $5,619 vs $2,096 in 1974.

From there the part covers:
- **Unconfoundedness and overlap.**
  - Strong ignorability (Rosenbaum & Rubin 1983) and the adjustment formula.
  - The World's observational study: 3,000 eligible patients, 47% treated by doctors on baseline pressure, age and
    BMI. The ATE is −10.02 and the ATT −12.26; the naive estimate is −1.38. The propensity histograms show overlap.
- **Causal diagrams.**
  - Wright (1921); Pearl.
  - Chains, forks and colliders; d-separation (Verma & Pearl; Geiger et al.).
  - Back-door paths with an unmeasured frailty.
- **The back door.**
  - The back-door criterion and adjustment.
  - Berkson's bias: the correlation of two independent diseases is 0.00 overall and −0.56 among the admitted.
  - M-bias: the truth is 1.00; the unadjusted estimate is 0.99, adjusting for M gives 0.16, and for M and A 1.00.
  - A mediator: the total effect is 2.00; adjusting for the mediator gives the direct 1.01.
  - The disjunctive cause criterion (VanderWeele & Shpitser 2011).
- **The front door and do-calculus.**
  - Fisher's genotype as a graph. Naive 0.235, truth 0.1275, front door 0.129.
  - The three rules and their completeness (Shpitser & Pearl; Huang & Valtorta 2006); SWIGs (Richardson & Robins
    2013).
- **Simpson resolved.**
  - The World's clinic: +7.7 (mild) and +8.1 (severe) points within strata, −11.2 overall. Back-door adjustment gives
    +7.8.
  - With a mediator instead, the same numbers call for no adjustment.
- **g-computation** (Robins 1986). −10.35 vs truth −10.02; extrapolation where overlap is thin.
- **Propensity scores.**
  - The balancing property.
  - Nearest-neighbour matching (ATT −12.43 vs −12.26).
  - Cochran's (1968) five strata: −8.59, removing 83% of the naive bias.
  - Design trumps analysis (Rubin 2008).
- **Weighting.**
  - Horvitz–Thompson and Hajek IPW, and the ATT weights.
  - Balance: the baseline-pressure SMD goes from 1.37 to 0.18 and age from 0.85 to 0.08.
  - IPW gives −8.48 [−9.5, −7.5]. The largest weight is 36, and the effective sample sizes are 742 and 662.
  - Trimming (Crump et al. 2009), truncation, overlap weights (Li, Morgan & Zaslavsky 2018).
- **Double robustness** (Robins, Rotnitzky & Zhao 1994). AIPW gives −9.91 [−10.6, −9.2], with SE 0.44 against IPW's
  0.63. Kang & Schafer (2007), 1,000 samples of 1,000:

  | Estimator | Bias | RMSE | 90% coverage |
  |---|---|---|---|
  | outcome model, wrong | −0.85 | 1.73 | |
  | IPW, wrong | 4.88 | 12.5 | |
  | AIPW, propensity right | 0.04 | 1.66 | 91.9% |
  | AIPW, outcome right | 0.03 | 2.24 | 90.8% |
  | AIPW, both wrong | −21.5 | 202 | 55.9% |

  The largest single weight is 39,667.
- **Double machine learning** (Chernozhukov et al. 2018).
  - Neyman orthogonality; the product-rate condition; cross-fitting.
  - Nonlinear confounding with n = 1,000 and ATE 3, 150 studies:

    | Estimator | Bias | Mean SE | 90% coverage |
    |---|---|---|---|
    | linear OLS | 1.12 | | 0% |
    | forest AIPW, no cross-fitting | 0.58 | 0.087 | 0% |
    | DML, cross-fitted | 0.08 | 0.187 | 86.7% |

  - The partially linear model (Robinson 1988).
- **Heterogeneous effects.**
  - T-, S-, X- (Künzel et al. 2019) and DR-learners (Kennedy 2023); the causal forest (Wager & Athey 2018; Athey,
    Tibshirani & Wager 2019) with local centring and honesty.
  - The World's trial, graded on 2,000 islanders against τ(x) = −(9 + 0.3(sbp − 150) + 0.08(age − 60)). RMSE:

    | Estimator | RMSE |
    |---|---|
    | constant ATE | 4.22 |
    | T-learner | 3.44 |
    | DR-learner | 4.66 |
    | X-learner | 2.60 |
    | causal forest | 2.61 |
    | linear, interacted | 1.17 |

  - Decile calibration: the forest is too timid, the T-learner too bold.
- **Sensitivity analysis.** The World with an unmeasured frailty:
  - adjusted −7.25 (SE 0.37), truth −9.93, −9.05 with frailty measured;
  - Rosenbaum's Γ on matched pairs: significant until Γ ≈ 6.9;
  - E-values (VanderWeele & Ding 2017);
  - Cinelli & Hazlett (2020): RV = 0.30 (0.28 for significance), against the frailty's actual partial R² of 0.087
    and 0.085.
- **Smoking and lung cancer.**
  - Doll & Hill (1950): 647 of 649 cases and 622 of 649 controls smoked (OR ≈ 14); the British Doctors Study.
  - Fisher's constitutional hypothesis (1957–58).
  - Cornfield et al. (1959): RR ≈ 9 needs a confounder 9 times as prevalent (the E-value is 17.5).
  - Hill's nine viewpoints (1965).
- **Time-varying treatments.**
  - Treatment–confounder feedback with an unmeasured U; the truth is −7. Naive −2.57; adjusted for L₁ −2.10; IPW-MSM
    −7.04; g-formula −6.99.
  - Target-trial emulation (Hernán & Robins 2016).
- **LaLonde revisited.**
  - 67% of PSID men have ê < 0.1, 74% of trainees have ê > 0.5, and 313 of 429 controls lie in range.
  - Estimates: OLS $1,548, regression ATT $1,648, matching $428, IPW-ATT $1,348 ($1,539 on the overlap), strata
    $510.
  - Placebo (1975 earnings): experiment $265, PSID −$144 (Imbens & Xu 2024).
  - Lessons: overlap, pre-treatment outcomes, placebos, sensitivity.

Data:
- NSW is the Museum's;
- the observational study, the clinic and the trial are the World's;
- the colliders, front door, Kang–Schafer, DML and MSM examples are seeded simulations.

**Built in this part:**
- **`statkit.causal` (II)** ([`explainer/stats/kit/causal.py`](../../../explainer/stats/kit/causal.py)), checked in
  `tests/test_stats_kit_causal.py`:
  - **Graphs:** `DAG` with d-separation (moral ancestral graph), path enumeration, open/blocked paths and the
    back-door criterion.
  - **Propensity methods:** logistic propensity scores, SMD balance, g-computation, propensity matching,
    subclassification.
  - **Weighting and double robustness:** Horvitz–Thompson/Hajek IPW for the ATE and ATT; AIPW with influence-function
    SEs; cross-fitted DML for the ATE and the partially linear model.
  - **Heterogeneous effects:** T-, S-, X- and DR-learners; an honest, locally centred causal forest.
  - **Sensitivity and time:** E-values, robustness values, partial R², Rosenbaum bounds for matched pairs,
    Cornfield's ratio; stabilized MSM weights.
- **The Museum** gains `nsw()`.
- **The causal graph** (`CausalGraph` in `explainer/stats/viz.py`).

The Coverage Board gains nine rows (90% intervals):

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| naive difference in means | World: doctors choose, n = 2,000 | 0.0% | broken |
| IPW, logistic propensity | same | 78.4% | broken |
| AIPW, both models fitted | same | 90.0% | kept |
| regression adjustment, unmeasured frailty | World: doctors also see frailty | 0.0% | broken |
| AIPW, PS right, outcome wrong | Kang & Schafer (2007), n = 1,000 | 91.9% | kept |
| AIPW, both models wrong | same | 55.9% | broken |
| OLS adjustment, linear | nonlinear confounding, n = 1,000 | 0.0% | broken |
| AIPW with forests, no cross-fitting | same | 0.0% | broken |
| DML: forests, cross-fitted | same | 86.7% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats36.compute   # once (about twenty minutes)
python tools/build.py stats36 -q l                         # fast 480p preview
python tools/build.py stats36                              # 1080p30 -> renders/stats36.mp4
python tools/qa_scene.py stats36 AIPW
python tools/lecture_length.py stats36 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | LaLonde's test | $1,794 vs −$635 |
| 1 | Unconfoundedness and overlap | ATE −10.02; naive −1.38 |
| 2 | Causal diagrams | three junctions; d-separation |
| 3 | The back door | Berkson −0.56; M-bias 0.16 |
| 4 | The front door and do-calculus | 0.235 vs 0.129 (truth 0.128) |
| 5 | Simpson resolved | −11.2 → +7.8 points |
| 6 | g-computation | −10.35 |
| 7 | Propensity scores | ATT −12.43; strata −8.59 |
| 8 | Weighting | −8.48; max weight 36 |
| 9 | Double robustness | −9.91; Kang–Schafer bias −21.5 |
| 10 | Double machine learning | 86.7% vs 0% |
| 11 | Heterogeneous effects | RMSE 4.22 → 2.61 (forest), 1.17 (linear) |
| 12 | Sensitivity analysis | Γ* ≈ 6.9; RV 0.30 |
| 13 | Smoking and lung cancer | 647/649 vs 622/649; E = 17.5 |
| 14 | Time-varying treatments | −2.57 vs −7.04 (truth −7) |
| 15 | LaLonde revisited | $428 to $1,648 |
| 16 | Outro | — |

## Sources

- **LaLonde.**
  - R. LaLonde, *AER* 76 (1986); R. Dehejia & S. Wahba, *JASA* 94 (1999); J. Smith & P. Todd, *J. Econometrics* 125
    (2005).
  - G. Imbens & Y. Xu, *LaLonde (1986) after nearly four decades* (2024).
- **Identification.**
  - P. Rosenbaum & D. Rubin, *Biometrika* 70 (1983); S. Wright, *J. Agric. Res.* 20 (1921).
  - J. Pearl, *Biometrika* 82 (1995), *Causality* (2000; 2009).
  - T. Verma & J. Pearl (1988); D. Geiger, T. Verma & J. Pearl, *Networks* 20 (1990).
  - J. Berkson, *Biometrics Bull.* 2 (1946); T. VanderWeele & I. Shpitser, *Biometrics* 67 (2011).
  - I. Shpitser & J. Pearl, *AAAI* (2006); Y. Huang & M. Valtorta, *UAI* (2006); T. Richardson & J. Robins (2013).
- **Estimation.**
  - J. Robins, *Math. Modelling* 7 (1986); W. Cochran, *Biometrics* 24 (1968); D. Rubin, *Ann. Appl. Stat.* 2 (2008).
  - D. Horvitz & D. Thompson, *JASA* 47 (1952); R. Crump, V. J. Hotz, G. Imbens & O. Mitnik, *Biometrika* 96 (2009);
    F. Li, K. Morgan & A. Zaslavsky, *JASA* 113 (2018).
  - J. Robins, A. Rotnitzky & L. P. Zhao, *JASA* 89 (1994); J. Kang & J. Schafer, *Stat. Sci.* 22 (2007);
    M. van der Laan & D. Rubin (2006).
  - V. Chernozhukov, D. Chetverikov, M. Demirer, E. Duflo, C. Hansen, W. Newey & J. Robins, *Econometrics J.* 21
    (2018); P. Robinson, *Econometrica* 56 (1988).
- **Heterogeneity.**
  - S. Künzel, J. Sekhon, P. Bickel & B. Yu, *PNAS* 116 (2019); E. Kennedy, *EJS* 17 (2023).
  - S. Athey & G. Imbens, *PNAS* 113 (2016); S. Wager & S. Athey, *JASA* 113 (2018); S. Athey, J. Tibshirani &
    S. Wager, *Ann. Stat.* 47 (2019); S. Athey & S. Wager, *Econometrica* 89 (2021).
- **Sensitivity.**
  - J. Cornfield, W. Haenszel, E. Hammond, A. Lilienfeld, M. Shimkin & E. Wynder, *JNCI* 22 (1959).
  - P. Rosenbaum, *Biometrika* 74 (1987), *Observational Studies* (2002).
  - T. VanderWeele & P. Ding, *Ann. Intern. Med.* 167 (2017); C. Cinelli & C. Hazlett, *JRSS B* 82 (2020).
- **Smoking.**
  - R. Doll & A. B. Hill, *BMJ* (1950, 1954); E. Wynder & E. Graham, *JAMA* 143 (1950).
  - R. A. Fisher, *BMJ* (1957), *Nature* 182 (1958); A. B. Hill, *Proc. R. Soc. Med.* 58 (1965); US Surgeon General
    (1964).
- **Time-varying.**
  - J. Robins, M. Hernán & B. Brumback, *Epidemiology* 11 (2000); M. Hernán & J. Robins, *Am. J. Epidemiol.* 183
    (2016).
  - M. Hernán et al., *Epidemiology* 19 (2008).
- **Data.** NSW via R's Matching (Sekhon) and MatchIt (Ho, Imai, King & Stuart).

## Problems and solutions

1. **Balancing.** P(T = 1 | X, e(X)) = P(T = 1 | X) = e(X), which depends on X only through e(X).
   - So P(T = 1 | X, e(X)) = P(T = 1 | e(X)), i.e. T ⊥ X | e(X).
2. **Unconfoundedness given the score.**
   P(T = 1 | Y(0), Y(1), e(X)) = E[P(T = 1 | Y(0), Y(1), X) | Y(0), Y(1), e(X)].
   - By unconfoundedness the inner probability is e(X), so this is E[e(X) | Y(0), Y(1), e(X)] = e(X), free of the
     potential outcomes.
3. **IPW.** E[TY/e(X)] = E[E[T Y(1) | X]/e(X)] = E[E[T | X] E[Y(1) | X]/e(X)] = E[Y(1)].
   - The middle step uses consistency and unconfoundedness, and the division needs overlap.
4. **Double robustness.** Write the AIPW term for Y(1) as μ₁(X) + T(Y − μ₁(X))/e(X), and take its expectation given X:
   μ₁ + e₀(X)(m₁(X) − μ₁(X))/e(X), where m₁ = E[Y(1) | X] and e₀ is the true propensity.
   - If μ₁ = m₁, the correction is zero, so the mean is m₁ for any e.
   - If e = e₀, the result is μ₁ + m₁ − μ₁ = m₁ for any μ₁.
   - Averaging over X gives E[Y(1)] either way.
5. **M-bias.**
   - With Z = {M}, the path T ← A → M ← B → Y has the collider M in Z, so it is open.
   - It begins with an arrow into T, so it is an open back-door path, and the criterion fails.
   - Adding A blocks it, since A is a non-collider in Z.
6. **E-value.**
   - VanderWeele & Ding's bound: a confounder with risk ratios RR_UT and RR_UY can shift an observed RR by at most
     B = RR_UT RR_UY/(RR_UT + RR_UY − 1).
   - Set both equal to E and require B = RR: E²/(2E − 1) = RR, so E² − 2RR·E + RR = 0, and E = RR + √(RR² − RR).

## Glossary

- **Unconfoundedness (ignorability)**: (Y(0), Y(1)) ⊥ T | X. **Overlap (positivity)**: 0 < e(x) < 1.
- **DAG; d-separation**: a causal graph; the graphical test for conditional independence.
- **Back-door / front-door criterion**: graphical conditions under which adjustment or the front-door formula
  identifies an effect.
- **Collider; Berkson's bias; M-bias**: a node with two arrows in; the association created by conditioning on one.
- **do-calculus**: Pearl's three rules for rewriting interventional quantities.
- **g-computation (g-formula)**: estimating E[Y(t)] by averaging fitted outcome models.
- **Propensity score**: e(x) = P(T = 1 | X = x); a balancing score.
- **IPW**: weighting by 1/e or 1/(1 − e); **Hajek** normalizes the weights.
- **AIPW / doubly robust**: consistent if either the outcome model or the propensity model is right.
- **DML**: cross-fitted machine-learned nuisances in an orthogonal score.
- **CATE; meta-learners; causal forest**: τ(x); generic recipes; honest, effect-splitting forests.
- **Rosenbaum's Γ; E-value; robustness value**: three scales for how strong hidden confounding must be to change a
  conclusion.
- **MSM; stabilized weights; target trial**: models for potential outcomes under treatment sequences; their weights;
  the protocol an observational analysis emulates.

## Where it comes back

- **Part 37**: natural experiments: instruments, regression discontinuity, difference-in-differences, synthetic
  control.
- **Part 40**: causal survival analysis.
- **Part 41**: missing data with the same weighting and doubly robust tools.
- **Part 49**: efficient influence functions; the theory behind AIPW and DML.
- **Part 52**: high-dimensional confounding.
- **Part 60**: distribution shift as transport.
- **Part 62**: mediation, heterogeneity, causal discovery.
- **Part 63**: counterfactual fairness.

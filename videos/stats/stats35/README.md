# Statistics, Built — Part 35: What If? Experiments and Potential Outcomes

Part 35 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fifteenth part of Stage III, Master's. Part 34 made predictions honest, and
ended with a model that predicted well and would have advised badly. This part asks what a causal effect is, and why
randomization lets us measure one:
- potential outcomes, and the World's clinic trial, in which both outcomes of every patient are known;
- Fisher's and Neyman's randomization inference;
- design and analysis: blocking, adjustment, clusters;
- noncompliance, interference, subgroups, sequential monitoring, surrogates and transport.

The part builds:
- the World's clinic trial (`World.trial`) and its epidemic (`World.epidemic`, `World.infected`);
- `statkit.causal` (I);
- an instrument, the science table (`ScienceTable`). It shows each unit's Y(0), Y(1) and τ, and the grey patches an
  assignment puts over the half it hides.

It opens with the 1954 Salk vaccine trial (Francis 1955; Meier 1972). In cases of paralytic polio per 100,000:
- the randomized placebo-controlled design: 28 vaccinated vs 71 placebo (and 46 among children whose parents
  refused), an estimated 43 cases prevented per 100,000;
- the observed-control design: 25 vs 54, an observed difference of 29. These different areas do not by themselves identify the exact bias. Consenting families were wealthier, and their children
  more at risk of polio.

From there the part covers:
- **Potential outcomes** (Neyman 1923; Rubin 1974; Holland 1986).
  - The science table of eight of the World's patients; the trial's 2,000 individual effects have mean −7.83 mm Hg and
    SD 4.75, and 4.3% would be harmed.
  - The fundamental problem; well-defined interventions, including the scope of Holland’s manipulation criterion.
- **Estimands and SUTVA.**
  - SATE, ATT, CATE, PATE. The trial's SATE is −7.83 against −9.93 among the 87,406 eligible islanders: the trial's
    patients average 58 years, the islanders 69.
  - Interference and hidden versions; ill-defined interventions (Hernán & Taubman 2008).
  - Risk difference, risk ratio and non-collapsible odds ratios; Salk's risk ratio is 0.39.
- **Why randomization works.**
  - Difference in means = ATT + selection bias.
  - When doctors prescribe by pressure, the treated start at 152.3 against 145.3. The naive estimate is −2.21; the ATT
    is −9.58 and the selection bias +7.37. A coin gives −8.41.
- **Fisher's sharp null.**
  - 12 patients, all 924 assignments: the observed +1.7 has p = 0.82, and exact enumeration on a half-point grid gives [−10.0, 13.5]. This targets a common constant effect; it is not a generally valid interval for the heterogeneous SATE.
  - All 2,000 patients by Monte Carlo: −7.21 against a sampled absolute null maximum of 2.12. Zero extreme draws out of 10,000 gives the plus-one Monte Carlo p-value 1/10,001, rather than a certified bound on the exact p-value.
  - Fisher vs Neyman nulls (Wu & Ding 2021).
- **Neyman's variance.** S₁²/n₁ + S₀²/n₀ − S_τ²/n.
  - S_τ = 4.75; the true SD is 0.446, the conservative one 0.458, and 4,000 re-randomizations give 0.439.
  - 90% coverage is 91.1%.
  - The superpopulation view; Aronow, Green & Lee's bounds.
- **Blocking and pairing.**
  - Ten blocks on baseline pressure (correlation 0.70 with Y(0)) take the SD from 0.448 to 0.351; matched pairs give
    0.342.
  - Imai's pair variance; rerandomization (Morgan & Rubin 2012; Li, Ding & Rubin 2018).
- **Adjustment.**
  - On the trial, adjusting for baseline and age takes the SD from 0.428 to 0.336.
  - Freedman's (2008) three critiques.
  - Lin's (2013) interacted regression with HC2, on a design with n = 200, 50 treated and heterogeneous,
    heteroskedastic effects:

    | Estimate | SD | Mean SE | 90% coverage |
    |---|---|---|---|
    | ANCOVA | 0.50 | 0.43 | 84.8% |
    | Lin | 0.39 | 0.41 | 90.6% |
    | unadjusted | 1.04 | | |

- **Cluster randomization.** The World's 400 schools (24,157 pupils, unadjusted model ICC 0.171, mean size 60.4) give an approximate design effect of
  11.1. The ICC includes shared school background and independent pupil background; 0.145 is the residual ICC conditional on those covariates. The design-effect formula is exact for equal sizes and an approximation here. Over 1,000 re-randomizations of the programme (true effect +20):

  | Analysis | SE | 90% coverage |
  |---|---|---|
  | pupil level | 1.25 | 35.6% |
  | school level | 4.17 | 90.3% |

  Cornfield's 'self-deception'.
- **Noncompliance.**
  - Compliance types: 64.5% compliers, 30.0% never-takers (lower Y(0)), 5.5% always-takers (higher).
  - One trial gives:

    | Analysis | Estimate |
    |---|---|
    | intention to treat | −5.62 |
    | as treated | −5.97 |
    | per protocol | −6.96 |
    | IV (Wald), −5.62 / 0.649 | −8.66 |
    | true complier effect | −8.13 |

  - LATE derived (Imbens & Angrist 1994; Angrist, Imbens & Rubin 1996).
- **Interference.** The World's epidemic in 200 towns, with infection risk r_j(1 − 0.6v)(1 − 0.6s_j): 16.3% with no
  one vaccinated, 2.7% with everyone.
  - Hudgens & Halloran's two-stage design (30% vs 70%), estimates with the truth in brackets: direct 8.1 (7.9) and
    6.5 (5.7) points, indirect 3.3 (3.8), total 9.7 (9.5), overall 5.4 (5.4).
  - An individually randomized trial sees only a 7.0-point direct effect.
  - Exposure mappings (Aronow & Samii 2017).
- **Subgroups.**
  - ISIS-2: 804/8,587 (9.4%) vs 1,016/8,600 (11.8%). For Gemini and Libra, a 9% (SD 13) increase; for the other
    signs, a 28% (SD 5) reduction.
  - Twelve random 'signs' in a trial with one true effect: in 58% of trials some sign shows no benefit, and in 44% some
    subgroup-versus-complement interaction is 'significant'.
- **Sequential trials.**
  - Peeking at 1.96 gives false-positive rates of 8.2%, 10.7%, 14.1%, 19.5% and 24.2% for 2, 3, 5, 10 and 20 looks.
  - Boundaries with K = 5: Pocock 2.413; O'Brien–Fleming 4.562 → 2.040; Lan–DeMets OBF-type spending 4.875 → 2.030.
  - Against an effect with 80% fixed-design power, Pocock has 71% power using 71% of the information; O'Brien–Fleming
    has 79% using 80%.
- **Surrogates.**
  - CAST: 63 vs 26 deaths.
  - Prentice-inspired linear regression diagnostics, with two drugs that each lower pressure by about 8 points:
    - drug A: stroke 3.8% vs 5.3%, and the adjusted treatment coefficient is small (t = −0.09);
    - drug B: stroke 8.4% vs 4.9%, and the adjusted treatment coefficient is large (t = 4.8). A small coefficient does not establish conditional independence or causal surrogacy. The mechanisms are known because the example is simulated.
  - Fleming & DeMets (1996); Buyse et al. (2000).
- **External validity.**
  - Inverse odds of participation weighting on age, pressure, sex and BMI moves the estimate from −8.05 to −9.07.
    The truth for the island is −9.93. The effective sample size is 988.
  - Positivity: over-80s are 21% of the island and 2.4% of the trial. Pragmatic trials.

Data:
- the patients, schools and epidemic are the World's;
- the Salk numbers use a rounded textbook summary, rather than exact participant counts; ISIS-2 and CAST totals match the primary reports;
- the subgroup, Freedman and sequential examples are seeded simulations.

**Built in this part:**
- **`statkit.causal` (I)** ([`explainer/stats/kit/causal.py`](../../../explainer/stats/kit/causal.py)), checked in
  `tests/test_stats_kit_causal.py`:
  - **Randomization inference:** Neyman's estimator with its exact and conservative variances (checked by
    enumeration); Fisher's exact and Monte Carlo randomization tests and their inversion.
  - **Design and adjustment:** blocked and paired estimators; ANCOVA and Lin's estimator with HC2; cluster-level
    analysis and the design effect.
  - **Noncompliance and interference:** the Wald/IV estimator with a delta-method SE; Hudgens–Halloran effects.
  - **Sequential designs:** crossing probabilities by numerical integration, with Pocock, O'Brien–Fleming and
    Lan–DeMets boundaries checked against published values; the peeking simulator.
  - **Surrogates and transport:** Prentice's criteria; inverse-odds transport.
- **The World** gains `trial`, `epidemic` and `infected()`, and **the Museum** `SALK`, `ISIS2` and `CAST`.
- **The science table** (`ScienceTable` in `explainer/stats/viz.py`).

The Coverage Board gains eleven rows:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| doctor chooses, difference in means | World trial, n = 2,000 | 0.0% | broken |
| randomized, Neyman 90% CI | World trial | 90.9% | kept |
| ANCOVA, conventional SE | Freedman's design, n = 200, 50 treated | 84.8% | broken |
| Lin, HC2 SE | same | 90.6% | kept |
| pupil-level CI, school-randomized | World schools | 35.6% | broken |
| school-level CI | World schools | 90.3% | kept |
| as-treated comparison (for the complier effect) | World trial | 0.0% | broken |
| IV (Wald) estimate | World trial | 91.2% | kept |
| peeking at 1.96, 5 looks (size, 5%) | null trials | 14.1% | broken |
| Pocock boundary | null trials | 5.05% | kept |
| O'Brien–Fleming | null trials | 5.03% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats35.compute   # once (under a minute)
python tools/build.py stats35 -q l                         # fast 480p preview
python tools/build.py stats35                              # 1080p30 -> renders/stats35.mp4
python tools/qa_scene.py stats35 Neyman
python tools/lecture_length.py stats35 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The Salk trial | 43 vs 29 per 100,000 |
| 1 | Potential outcomes | mean τ −7.83, SD 4.75, 4.3% harmed |
| 2 | Estimands and SUTVA | SATE −7.83 vs PATE −9.93 |
| 3 | Why randomization works | −2.21 vs −8.41; bias +7.37 |
| 4 | Fisher's sharp null | p = 0.82 (12); MC p = 1/10,001 (2,000) |
| 5 | Neyman's variance | 0.446 vs 0.458; 91.1% |
| 6 | Blocking and pairing | SD 0.448 → 0.351 → 0.342 |
| 7 | Adjustment | ANCOVA 84.8% vs Lin 90.6% |
| 8 | Cluster randomization | approximate deff 11.1; 35.6% vs 90.3% |
| 9 | Noncompliance | ITT −5.62; IV −8.66; truth −8.13 |
| 10 | Interference | direct 8.1, indirect 3.3, overall 5.4 |
| 11 | Subgroups | 58% / 44% |
| 12 | Sequential trials | 14.1%; Pocock 2.413; OBF 4.56 → 2.04 |
| 13 | Surrogates | CAST 63 vs 26; drug B 8.4% vs 4.9% |
| 14 | External validity | −8.05 → −9.07 (truth −9.93) |
| 15 | Outro | — |

## Sources

- **Salk.** T. Francis et al., *Am. J. Public Health* 45 (1955); P. Meier, in *Statistics: A Guide to the Unknown*
  (1972); D. Freedman, R. Pisani & R. Purves, *Statistics*, ch. 1.
- **Potential outcomes.**
  - J. Neyman (1923), trans. D. Dabrowska & T. Speed, *Stat. Sci.* 5 (1990).
  - D. Rubin, *J. Educ. Psychol.* 66 (1974), *JASA* 75 (1980); P. Holland, *JASA* 81 (1986).
  - M. Hernán & S. Taubman, *Int. J. Obes.* 32 (2008); S. Greenland, J. Robins & J. Pearl, *Stat. Sci.* 14 (1999).
- **Randomization inference.**
  - R. A. Fisher, *The Design of Experiments* (1935); J. Neyman, *JRSS Suppl.* 2 (1935) and the discussion.
  - J. Wu & P. Ding, *JASA* 116 (2021); P. Aronow, D. Green & D. Lee, *Ann. Stat.* 42 (2014).
- **Design.**
  - K. Imai, *Stat. Med.* 27 (2008); K. Morgan & D. Rubin, *Ann. Stat.* 40 (2012); X. Li, P. Ding & D. Rubin, *PNAS* 115
    (2018).
  - G. Box, W. Hunter & J. S. Hunter, *Statistics for Experimenters* (1978).
- **Adjustment.**
  - D. Freedman, *Adv. Appl. Math.* 40 (2008), *Ann. Appl. Stat.* 2 (2008); W. Lin, *Ann. Appl. Stat.* 7 (2013).
  - FDA, *Adjusting for Covariates in Randomized Clinical Trials* (2023).
- **Clusters.** J. Cornfield, *Am. J. Epidemiol.* 108 (1978); L. Kish, *Survey Sampling* (1965).
- **Noncompliance.** G. Imbens & J. Angrist, *Econometrica* 62 (1994); J. Angrist, G. Imbens & D. Rubin, *JASA* 91
  (1996); C. Frangakis & D. Rubin, *Biometrics* 58 (2002).
- **Interference.**
  - M. Sobel, *JASA* 101 (2006); M. Hudgens & M. E. Halloran, *JASA* 103 (2008).
  - P. Aronow & C. Samii, *Ann. Appl. Stat.* 11 (2017).
- **Subgroups.**
  - ISIS-2 Collaborative Group, *Lancet* 332 (1988).
  - S. Yusuf, J. Wittes, J. Probstfield & H. Tyroler, *JAMA* 266 (1991); P. Rothwell, *Lancet* 365 (2005).
- **Sequential.**
  - P. Armitage, C. McPherson & B. Rowe, *JRSS A* 132 (1969); S. Pocock, *Biometrika* 64 (1977); P. O'Brien &
    T. Fleming, *Biometrics* 35 (1979).
  - K. Lan & D. DeMets, *Biometrika* 70 (1983); C. Jennison & B. Turnbull (1999).
- **Surrogates.**
  - CAST Investigators, *NEJM* 321 (1989); D. Echt et al., *NEJM* 324 (1991).
  - R. Prentice, *Stat. Med.* 8 (1989); T. Fleming & D. DeMets, *Ann. Intern. Med.* 125 (1996); M. Buyse et al.,
    *Biostatistics* 1 (2000).
- **Transport.**
  - E. Stuart, S. Cole, C. Bradshaw & P. Leaf, *JRSS A* 174 (2011); I. Dahabreh, S. Robertson, E. Tchetgen Tchetgen,
    E. Stuart & M. Hernán, *Biometrics* 75 (2019).
  - D. Westreich et al., *Am. J. Epidemiol.* 186 (2017).

## Problems and solutions

1. **Unbiasedness.** Under complete randomization P(Z_i = 1) = n₁/n.
   - Ȳ₁ = Σ Z_i Y_i(1)/n₁, so E Ȳ₁ = Σ (n₁/n) Y_i(1)/n₁ = Ȳ(1). Likewise E Ȳ₀ = Ȳ(0).
   - Hence E(Ȳ₁ − Ȳ₀) = τ̄.
2. **Neyman's variance.** Ȳ₁ is the mean of a simple random sample of n₁ from the n values Y_i(1), so
   Var Ȳ₁ = (1 − n₁/n) S₁²/n₁; likewise Var Ȳ₀ = (1 − n₀/n) S₀²/n₀.
   - The covariance uses Cov(Z_i, Z_j) = −n₁n₀/(n²(n − 1)) for i ≠ j. It gives Cov(Ȳ₁, Ȳ₀) = −S₁₀/n, where S₁₀ is the
     finite-population covariance of Y(1) and Y(0).
   - Summing, with S_τ² = S₁² + S₀² − 2S₁₀: Var(Ȳ₁ − Ȳ₀) = S₁²/n₁ + S₀²/n₀ − S_τ²/n.
3. **Conservativeness.** Within-arm sample variances are unbiased for the finite-population variances under SRS:
   E s₁² = S₁² and E s₀² = S₀².
   - So E(s₁²/n₁ + s₀²/n₀) = S₁²/n₁ + S₀²/n₀ = Var + S_τ²/n ≥ Var, with equality if and only if τ is constant.
4. **LATE.**
   - By randomization, ITT_Y = Σ_strata π_g E[Y(D(1)) − Y(D(0)) | g]. Exclusion lets Y depend on Z only through D.
   - For never- and always-takers D(1) = D(0), so their terms vanish; defiers are absent by monotonicity. That leaves
     ITT_Y = π_c E[Y(1) − Y(0) | complier].
   - Similarly ITT_D = E[D(1) − D(0)] = π_c. So the ratio is the compliers' average effect.
5. **Two looks.** Z₁ = S_n/√n and Z₂ = S_{2n}/√(2n) are bivariate normal with correlation √(1/2).
   - The false-positive rate is P(|Z₁| > 1.96 or |Z₂| > 1.96) = 1 − P(|Z₁| ≤ 1.96, |Z₂| ≤ 1.96).
   - Numerically this is 0.083, above 0.05 because the two events are not nested (the kit's `crossing_probs` gives
     about 0.083; the simulation 8.2%).
6. **Design effect.** For a cluster mean of m units with common variance σ² and pairwise correlation ρ:
   - Var = m⁻²(mσ² + m(m − 1)ρσ²) = (σ²/m)(1 + (m − 1)ρ).
   - Relative to m independent units, the factor is 1 + (m − 1)ρ.

## Glossary

- **Potential outcomes**: Y_i(1), Y_i(0), the outcomes unit i would have under each treatment.
- **Science table**: all units' potential outcomes; half is always missing.
- **Fundamental problem of causal inference**: no unit reveals both.
- **SATE / ATT / CATE / PATE**: the average effect in the sample / among the treated / given covariates / in a
  population.
- **SUTVA**: no interference and no hidden versions of treatment.
- **Selection bias**: E[Y(0) | Z = 1] − E[Y(0) | Z = 0].
- **Sharp null**: Y_i(1) = Y_i(0) for every i (Fisher); the **weak null** is τ̄ = 0 (Neyman).
- **Randomization distribution**: a statistic's values over all assignments.
- **Neyman variance**: S₁²/n₁ + S₀²/n₀ − S_τ²/n; the usual estimate drops the last term.
- **Blocking / pairing / rerandomization**: designs that restrict covariate imbalance; blocking still permits within-block imbalance.
- **Lin estimator**: the treatment-by-centred-covariate interacted regression with HC2 SEs.
- **Design effect**: 1 + (m − 1)ρ for equal cluster sizes and exchangeable correlations; **ICC** ρ.
- **Principal strata**: compliers, never-takers, always-takers, defiers.
- **ITT / LATE (CACE)**: the effect of assignment / of treatment among compliers.
- **Interference; direct / indirect / total / overall effects**: Hudgens–Halloran's decomposition under two-stage
  randomization.
- **Group-sequential boundary; alpha spending**: interim thresholds preserving the overall size.
- **Surrogate endpoint; Prentice criteria**: an early outcome standing in for the one that matters; statistical conditions require validation and do not by themselves identify causal mediation.
- **Transportability**: carrying an effect to a target population; positivity.

## Where it comes back

- **Part 36**: causal effects without randomization; target trials; mediation.
- **Part 37**: instruments and natural experiments, the LATE's home.
- **Part 40**: survival endpoints in trials.
- **Part 41**: missing outcomes and dropout.
- **Part 49**: efficient estimation of average effects.
- **Part 58**: anytime-valid sequential inference.
- **Part 62**: heterogeneous effects, interference and mediation.
- **Part 63**: counterfactual fairness.

The sequential teaching calculations use smooth Gauss–Legendre continuation quadrature, checked at 80 and 160 nodes. Canonical normal/Brownian assumptions underlie the boundaries. Alpha spending does not authorize arbitrary outcome-driven analysis times. All Board repetitions are independent trial-level indicators; the plotted Monte Carlo scale uses the nominal reference probability. Transport uses a working participation model and gives a point estimate plus a weight effective sample size, without a transported confidence interval.

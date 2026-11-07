# Statistics, Built — Part 42: The Comprehensive Exam

Part 42 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the last part of Stage III, Master's. Like Part 20, it adds no new method.
A client writes with two questions and a deadline. The comprehensive exam follows. The part covers:
- **Case 1, a trial to design:**
  - the estimand;
  - the unit of randomization;
  - the intraclass correlation from a pilot;
  - the sample size with a design effect;
  - the analysis plan, tested by simulation before use.
- **Case 2, an observational survey to analyse:**
  - the causal graph;
  - bad controls;
  - imputation of a missing confounder;
  - overlap and balance;
  - AIPW;
  - a robustness value with benchmarks;
  - a one-page report.
- **Twelve exam problems,** each posed, paused and solved on screen:
  1. a Poisson MLE with its model-based and sandwich SEs;
  2. one IRLS step;
  3. ML against REML for a variance;
  4. the eight schools' posterior;
  5. MCMC diagnostics;
  6. AIC against BIC;
  7. a KDE bandwidth;
  8. an influence function;
  9. a lasso KKT check;
  10. BH by hand;
  11. a split-conformal interval;
  12. Kaplan–Meier with Greenwood's variance.

The MSc goes on the Transcript, and the PhD core begins (→ Part 43).

**Built in this part:**
- **The MSc problem bank:** the twelve exam problems and six more, each with a full solution, below.
- **The exam card** (`ExamCard` in `explainer/stats/viz.py`), the part's instrument: a problem's card with its
  number, topic, the parts it draws on, its marks, the question, and a pause clock. `sweep()` turns the clock while
  the viewer works, `shrink()` lifts the card so the solution can be worked beneath, and `stamp()` seals it solved.
- **The World** gains its `ministry` block:
  - the pilot survey: 30 adults in each of 200 towns, with town effects of SD 3.5 mm Hg and a year's drift of SD 1.5;
  - the salt-substitute survey of 3,000 adults, drawn from `World.substitute_draw`, the law of uptake, potassium (the
    mediator), the clinic visit (the collider) and who withholds income.

**Data.**
- From the Museum:
  - Bliss's beetles (1935);
  - Longley (1967), via statsmodels;
  - Rubin's eight schools;
  - Old Faithful's waiting times (Azzalini & Bowman 1990);
  - Newcomb's 1882 timings of light (Stigler 1977);
  - Stamey's prostate data (via *The Elements of Statistical Learning*);
  - Singh et al.'s (2002) prostate microarray (R's `sda`, GPL ≥ 2);
  - New York's air quality, 1973;
  - Freireich's 6-MP trial as tabulated by Gehan (1965).
- From the World: the pilot, the trial's towns and the salt-substitute survey.
- The rest are seeded simulations.

The Coverage Board gains ten rows:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| individual-level t, cluster trial | 42 towns × 50 adults, ICC 0.054 | 60.9% | broken |
| cluster-level t | same | 90.2% | kept |
| cluster-level ANCOVA on the pilot | same | 90.0% | kept |
| naive difference in means | 3,000 adults, income MAR for over a third | 0.0% | broken |
| regression adjusting for a collider | same | 7.5% | broken |
| AIPW on complete cases | same | 81.5% | broken |
| AIPW with multiple imputation | same | 87.8% | kept |
| Poisson MLE, model-based SE | the World's doctor visits, n = 500 | 50.1% | broken |
| Poisson MLE, sandwich SE | same | 89.2% | kept |
| split conformal, 99 calibration points | the World's pressure from age and BMI | 89.9% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats42.compute   # once (about a minute)
python tools/build.py stats42 -q l                         # fast 480p preview
python tools/build.py stats42                              # 1080p30 -> renders/stats42.mp4
python tools/qa_scene.py stats42 TrialSize
python tools/lecture_length.py stats42 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | A letter from the ministry | two questions, six weeks |
| 1 | Case 1: what to randomize | pilot ICC 0.034 [0.020, 0.048]; truth 0.046, then 0.054 |
| 2 | Case 1: how many towns | 267 per arm × DE 3.70 → 21 towns per arm, 42 in all |
| 3 | Case 1: the analysis plan | type I error 30% vs 5.3%; power 82% → 95%; trial −3.13 [−5.99, −0.27] |
| 4 | Case 2: the survey and its graph | +6.7 raw; −2.33 adjusted; +0.09 with the mediator; −4.18 with the collider |
| 5 | Case 2: imputation and AIPW | 37% missing, FMI 0.13; AIPW −2.22 [−3.42, −1.01] |
| 6 | Case 2: sensitivity and the report | RV 0.074; benchmark (0.040, 0.033); the trial's −3.3 |
| 7 | Exam I: likelihood | SEs 0.527 vs 1.036; β = (−60.72, 34.27); σ² 52,277 vs 92,936 |
| 8 | Exam II: Bayes and model choice | A: 28 → 11.4; R̂ 1.45 → 1.01; AIC 4 vs BIC 2 |
| 9 | Exam III: smoothing, robustness, sparsity | h 3.99 vs 2.65; IF 4,816; KKT 0.182 off |
| 10 | Exam IV: discoveries, guarantees, survival | BH 8 vs 4, genes 59 vs 7; 10 ± 4.4; Ŝ(13) = 0.690 ± 0.107 |
| 11 | Outro | the MSc |

**Case 1.** The ministry wants community health workers in its towns, and must decide between a fall of 4 mm Hg (worth
paying for) and none.
- **The unit.** Households randomized within a town contaminate one another, so towns are randomized (Cornfield 1978:
  analysing a group-randomized trial as if individuals were randomized is "an exercise in self-deception").
- **The pilot's ICC.**
  - The one-way ANOVA of 6,000 pilot adults gives MSB = 545.1, MSW = 263.8 and σ̂²_b = 9.38, so ρ̂ = 0.034.
  - A bootstrap over towns gives a 90% interval of [0.020, 0.048].
  - Planning value 0.055: the upper end plus a year's drift. The World's truth is 0.046 in the pilot year and 0.054 in
    the trial year.
- **The size.**
  - n = 2(1.96 + 0.84)²σ²/δ² = 267 per arm with σ = 16.5.
  - The design effect 1 + 49 × 0.055 = 3.70 gives 987 adults, so 19.7 → 20 towns of 50 per arm. Hayes & Moulton add
    one for the t: 21 per arm, 42 towns, 2,100 adults.
  - The floor as m → ∞ is 2(z + z)²ρσ²/δ² = 14.7 towns per arm. Ten adults per town needs 82 towns; five hundred
    still needs 34.
  - With the pilot's ρ̂ the plan would have recruited 15 per arm; each 0.01 of ρ costs about 2.6 towns per arm.
  - Treating adults as independent, eight towns per arm "has" 93% power; the truth is 38%.
- **The plan, simulated from the towns' law (4,000 trials).**
  - Type I error: 30.2% for the individual-level analysis, 5.3% for both cluster-level analyses.
  - Power: 81.7% for the cluster t and 95.1% for the cluster ANCOVA on the pilot mean; the SD of τ̂ falls from 1.34 to
    1.09.
- **The trial run in the World.**
  - ANCOVA −3.13 [−5.99, −0.27]; cluster t −2.67 [−5.92, 0.57]; the individual-level interval [−4.09, −1.26] is less
    than half as wide as the cluster t's.
  - The truth is −4.

**Case 2.** A potassium-enriched salt substitute went on sale a year before the survey; 819 of 3,000 adults use it.
- **The raw comparison.** Users' pressure is 6.7 mm Hg higher (90% CI 5.5 to 7.9).
- **Confounding by indication.** Users are older (56.9 vs 43.3 years), heavier (BMI 29.1 vs 26.9), slightly richer,
  and three times as likely to have been told their pressure is high (37% vs 11%).
- **The graph.**
  - The back-door set is {age and sex, BMI, income, diagnosis}.
  - Potassium is a mediator (users excrete 95 vs 65 mmol a day). The clinic visit is a collider (36% vs 11%).
  - Over 40 imputations: adjusted −2.33; adding the mediator +0.09; adding the collider −4.18.
- **Missing income.** 37% withhold it: 63% of those under 40 and 10% of those over 60; 22% of users against 43% of
  non-users; less often at higher pressure.
  - Complete cases select on the outcome.
  - MI from age, sex, BMI, diagnosis, T, Y and T × Y (m = 40) has an FMI of 0.13.
- **Overlap and balance.** Propensities run from 0.02 to 0.93. The largest SMD falls from 0.78 to 0.04 after weighting.
- **AIPW with Rubin's rules.** −2.22 (SE 0.73), 90% CI [−3.42, −1.01]. With every income known it would be −2.26; the
  truth is −3.0.
- **Sensitivity.**
  - The adjusted OLS gives t = −4.23 on 2,993 df, so RV = 0.074 and approximate RV₀.₀₅ = 0.041.
  - The benchmark, "told: high pressure", has classical-OLS partial R² 0.040 with uptake and 0.033 with pressure. A confounder twice
    as strong would not erase the effect; three times as strong would.
- **The real trial.** The Salt Substitute and Stroke Study (Neal et al. 2021) randomized 600 Chinese villages (20,995
  adults): systolic pressure −3.34 mm Hg, stroke rate ratio 0.86 (0.77–0.96).

## Sources

- **Consulting and design.**
  - R. A. Fisher, *Sankhyā* 4 (1938), the "post mortem" remark; J. Cornfield, *Am. J. Epidemiol.* 108 (1978).
  - A. Donner & N. Klar, *Design and Analysis of Cluster Randomization Trials in Health Research* (2000); R. Hayes &
    L. Moulton, *Cluster Randomised Trials* (2nd ed. 2017).
  - M. Campbell, G. Piaggio, D. Elbourne & D. Altman, *BMJ* 345 (2012), CONSORT for cluster trials; D. Cox & C.
    Donnelly, *Principles of Applied Statistics* (2011).
- **Observational analysis.**
  - M. Hernán & J. Robins, *Causal Inference: What If* (2020); J. Robins, A. Rotnitzky & L. P. Zhao, *JASA* 89 (1994).
  - C. Cinelli & C. Hazlett, *JRSS B* 82 (2020); D. Rubin (1987); B. Neal et al., *NEJM* 385 (2021).
- **The exam.**
  - C. Bliss, *Ann. Appl. Biol.* 22 (1935); J. Longley, *JASA* 62 (1967); H. D. Patterson & R. Thompson,
    *Biometrika* 58 (1971).
  - D. Rubin, *J. Educ. Stat.* 6 (1981); A. Gelman et al., *Bayesian Data Analysis* (3rd ed. 2013); A. Vehtari et al.,
    *Bayesian Anal.* 16 (2021).
  - H. Akaike, *IEEE Trans. Autom. Control* 19 (1974); G. Schwarz, *Ann. Stat.* 6 (1978); B. Silverman, *Density
    Estimation* (1986).
  - M. Rudemo, *Scand. J. Stat.* 9 (1982); F. Hampel, *JASA* 69 (1974); S. Stigler, *Ann. Stat.* 5 (1977).
  - R. Tibshirani, *JRSS B* 58 (1996); Y. Benjamini & Y. Hochberg, *JRSS B* 57 (1995); J. Lei et al., *JASA* 113
    (2018).
  - E. Freireich et al., *Blood* 21 (1963); E. Gehan, *Biometrika* 52 (1965); M. Greenwood, *Reports on Public Health
    and Medical Subjects* 33 (1926).
  - D. Cox & D. Hinkley, *Problems and Solutions in Theoretical Statistics* (1978); L. Wasserman, *All of Statistics*
    (2004).

## Problems and solutions: the MSc problem bank

1. **A Poisson MLE and its sandwich** (Parts 22, 24).
   - Data: 0, 0, 0, 0, 1, 2, 2, 4, 5, 6, 9, 11.
   - The MLE: ℓ(λ) = Σyᵢ log λ − nλ, and the score Σyᵢ/λ − n = 0 gives λ̂ = ȳ = 40/12 = 3.333.
   - The model-based SE: I(λ) = n/λ, so SE = √(λ̂/n) = 0.527.
   - The sandwich: per observation, the score is uᵢ = yᵢ/λ − 1 and the Hessian −yᵢ/λ². So A = n/λ̂ and
     B = Σ(yᵢ − λ̂)²/λ̂², and A⁻¹BA⁻¹ = Σ(yᵢ − ȳ)²/n² = 154.67/144, giving SE = 1.036.
   - Report the sandwich: s² = 14.1 against ȳ = 3.33. In the World the variance is 5.8 times the mean, and the
     model-based interval covers 50%.
2. **One IRLS step** (Parts 21, 24). At β = 0 every μᵢ = ½.
   - The weights are wᵢ = nᵢμᵢ(1 − μᵢ) = nᵢ/4; the working response is zᵢ = ηᵢ + (p̂ᵢ − μᵢ)/(μᵢ(1 − μᵢ)) = 4(p̂ᵢ − ½).
   - Bliss's data give X'WX = [[120.25, 215.71], [215.71, 387.43]] and X'Wz = (50.50, 100.79).
   - So β⁽¹⁾ = (−37.86, 21.34), and ℓ rises from −333.40 to −200.01.
   - Converged (six steps to eight decimals): β̂ = (−60.72, 34.27), SEs (5.18, 2.91). The LD50 is 60.72/34.27 = 1.7717
     on the log10 scale, about 59.1 mg/l.
3. **ML and REML** (Parts 23, 25).
   - ML: profiling out β gives ℓ = −(n/2) log σ² − RSS/(2σ²), maximized at RSS/n. Because E[RSS] = (n − p)σ², this
     is biased by (n − p)/n.
   - REML: let K be n × (n − p) with orthonormal columns orthogonal to X. Then K'y ~ N(0, σ²I), free of β, with
     ‖K'y‖² = y'(I − H)y = RSS. Its likelihood −((n − p)/2) log σ² − RSS/(2σ²) is maximized at RSS/(n − p).
   - Longley: RSS = 836,424, so ML gives 52,277 and REML 92,936 (ratio 9/16). Twenty thousand simulations average
     52,287 and 92,955 at σ² = 92,936.
4. **The eight schools** (Parts 25, 26).
   - Integrating out θⱼ gives yⱼ | μ, τ ~ N(μ, σⱼ² + τ²).
   - With a flat prior on μ, p(τ | y) ∝ V_μ^{1/2} Πⱼ (σⱼ² + τ²)^{−1/2} exp(−(yⱼ − μ̂_τ)²/(2(σⱼ² + τ²))), where
     μ̂_τ = Σwⱼyⱼ/Σwⱼ, wⱼ = 1/(σⱼ² + τ²) and V_μ = 1/Σwⱼ.
   - E[θⱼ | τ, y] = (1 − Bⱼ)yⱼ + Bⱼμ̂_τ, with Bⱼ = σⱼ²/(σⱼ² + τ²).
   - Adaptive quadrature over τ ∈ [0, ∞), with flat priors on μ and τ ≥ 0, gives median τ = 5.24 and 90th percentile 13.73. School A goes from 28 to 11.40. The plot shows [0, 30], excluding 0.501% of posterior mass from its display only. The
     pooled mean is 7.7 (SE 4.1).
5. **MCMC diagnostics** (Part 27). Split R̂ = √(((n − 1)/n W + B/n)/W), rank-normalized (Vehtari et al. 2021).
   - Badly tuned: 1.45 ≫ 1.01 says the chains disagree. A bulk ESS of 8 says 4,000 draws carry the information of
     eight. 87% acceptance says the steps are too small to cross between the modes at ±3.
   - Fix: proposal SD 4. Acceptance is then 40%, R̂ 1.006 and bulk ESS 458.
   - Caveat: R̂ compares only what the chains found. Had all four started in one mode, it would have looked perfect, so
     use overdispersed starts.
6. **AIC against BIC** (Part 28). Ozone on temperature, n = 111, degree d with k = d + 2 parameters:

   | d | log-lik | AIC | BIC |
   |---|---|---|---|
   | 1 | −508.89 | 1023.78 | 1031.90 |
   | 2 | −502.62 | 1013.24 | 1024.08 |
   | 3 | −501.98 | 1013.95 | 1027.50 |
   | 4 | −498.73 | 1009.46 | 1025.72 |
   | 5 | −498.60 | 1011.21 | 1030.17 |

   - AIC chooses 4; BIC (log 111 = 4.71 per parameter) chooses 2.
   - For nested models AIC adds a needless term whenever its χ²₁ statistic exceeds 2. That has probability 0.157 at
     every n, so AIC is not consistent: it chooses a true quadratic about 74% of the time as n grows.
   - BIC's penalty log n → ∞ drives that probability to zero (0.99 at n = 2,560).
7. **Silverman's rule** (Part 29).
   - h = 0.9 min(s, IQR/1.349) n^(−1/5) = 0.9 × min(13.59, 17.79) × 272^(−0.2) = 0.9 × 13.59 × 0.3259 = 3.99.
   - LSCV(h) = ∫f̂² − (2/n)Σf̂₋ᵢ(xᵢ) has expectation E[ISE] − ∫f² under iid sampling at fixed h. It chooses 2.65.
   - The 0.9 constant is a robust rule of thumb, whereas the Gaussian normal-reference AMISE constant is about 1.06; a bimodal density has more curvature (larger ∫f''²) and needs less smoothing.
     Use LSCV or Sheather–Jones, and show both.
8. **The variance's influence function** (Part 30).
   - Contaminate: F_ε = (1 − ε)F + εδₓ, so μ_ε = μ + ε(x − μ).
   - Then T(F_ε) = (1 − ε)∫(y − μ_ε)²dF + ε(x − μ_ε)². Differentiating at 0 gives −σ² − 2(x − μ)∫(y − μ)dF + (x − μ)²,
     so IF(x) = (x − μ)² − σ².
   - Newcomb's −44: IF = 4,816, about 73 when divided by n = 66. The variance is 113.7 with the point and 38.5 without.
   - Sensitivity curves: the mean's is unbounded (26.21), the median's bounded (27.0), Huber's bounded and smooth
     (27.38). The modern value is 33.0.
9. **A lasso KKT check** (Part 32).
   - Let gⱼ = xⱼ'(y − Xβ̂)/n. At the solution, gⱼ = λ sign(β̂ⱼ) where β̂ⱼ ≠ 0, and |gⱼ| ≤ λ where β̂ⱼ = 0. These are
     necessary and, by convexity, sufficient.
   - The colleague's β̂ (least squares soft-thresholded once) fails: g_lcavol = 0.137, and the worst violation on the
     support is 0.182. The predictors are correlated up to 0.76.
   - Coordinate descent at λ = 0.1 has support {lcavol, lweight, lbph, svi, pgg45} with gⱼ = 0.1 exactly. Off the
     support, max |gⱼ| = 0.056.
10. **BH by hand** (Part 33). Compare p₍ᵢ₎ with i/120.
    - p₍₈₎ = 0.0458 ≤ 0.0667, while p₍₉₎ = 0.172 > 0.075, so reject 8 (all eight happen to be below their own lines in this example).
    - Bonferroni (0.1/12 = 0.0083) allows 4. The BH-adjusted p-values are 0.0024, 0.0066, 0.0156, 0.0246, 0.0295,
      0.0434, 0.0687, 0.0687, 0.229, 0.361, 0.714, 0.882.
    - The promise: E[V/max(R, 1)] ≤ q for valid null p-values under independence or the specific PRDS condition. It is an average over uses, not a statement
      about this list.
    - On the 6,033 genes: BH finds 59, Bonferroni 7.
11. **Split conformal** (Part 34).
    - k = ⌈(n + 1)(1 − α)⌉ = ⌈10 × 0.8⌉ = 8. The 8th smallest of 0.4, 0.9, 1.2, 1.6, 2.1, 2.7, 3.3, 4.4, 5.8 is 4.4,
      so the interval is 10 ± 4.4 = [5.6, 14.4].
    - Coverage: under exchangeability, the test residual's rank among the n + 1 is uniform. So
      P(R₍ₙ₊₁₎ ≤ R₍ₖ₎) ≥ k/(n + 1) = 0.8.
    - The guarantee is marginal and assumes only exchangeability.
    - On ozone (37 fit, 37 calibrate, 37 test): k = 35 and q = 51.9 ppb, so the forecast at 85°F is 56 ± 52. All 37 test
      days are covered; CQR would let the width follow the spread.
12. **Kaplan–Meier and Greenwood** (Part 40).
    - Ŝ(6) = 18/21 = 0.857, Ŝ(7) = 0.857 × 16/17 = 0.807, Ŝ(10) = × 14/15 = 0.753, Ŝ(13) = × 11/12 = 0.690.
    - Greenwood: Σd/(n(n − d)) = 3/378 + 1/272 + 1/210 + 1/132 = 0.02395, so SE = 0.690 × √0.02395 = 0.107.
    - Log-log: s = √0.02395/|log 0.690| = 0.417, and Ŝ^{exp(±1.96 s)} = [0.432, 0.849].
    - The medians are 23 weeks (6-MP) and 8 (placebo); the log-rank χ²₁ = 16.8.
13. **The variance of a cluster trial.**
    - ȳⱼ = μ + τzⱼ + bⱼ + ēⱼ has variance ρσ² + (1 − ρ)σ²/m = σ²[1 + (m − 1)ρ]/m.
    - The difference of two arm means of k such terms has variance 2σ²[1 + (m − 1)ρ]/(km).
    - Setting that equal to δ²/(z + z)² and letting m → ∞ gives k ≥ 2(z + z)²ρσ²/δ².
14. **A collider's bias.**
    - Take T and Y independent, and V = 1 with probability g(αT + βY), with α = β = 1 and g the logistic function, and T and Y independent Bernoulli(1/2).
    - Then P(T = 1 | V = 1, Y = y) = P(T = 1) E[g(α + βy)] / E[g(αT + βy)], which is about 0.594 at y = 0 and 0.546 at y = 1. So T and Y are
      dependent given V, though independent unconditionally ("explaining away").
15. **The information identity.**
    - If the model is correct, E[U U'] = −E[∂U/∂θ'], that is B = A, by differentiating ∫f = 1 twice.
    - Then A⁻¹BA⁻¹ = A⁻¹ = I⁻¹.
16. **IRLS is Newton.**
    - For a GLM with canonical link, U = X'(y − μ) and −∂U/∂β' = X'WX, with W = diag(Var(yᵢ)).
    - The Newton step β + (X'WX)⁻¹X'(y − μ) equals (X'WX)⁻¹X'Wz, with z = η + W⁻¹(y − μ).
    - With a non-canonical link the observed Hessian carries an extra term with mean zero. IRLS uses the expected one:
      Fisher scoring.
17. **The orthonormal lasso.**
    - If X'X = nI, the objective separates into Σⱼ [½(βⱼ − β̂ⱼ^OLS)² + λ|βⱼ|] (up to constants).
    - Each term is minimized by the soft threshold sign(β̂ⱼ^OLS)(|β̂ⱼ^OLS| − λ)₊.
18. **BH controls the FDR.**
    - For a true null i with independent p-values, write the FDR as Σ over nulls i and k of (1/k) P(pᵢ ≤ qk/m, R = k).
    - Conditioning on the other p-values (the leave-one-out argument of Benjamini & Yekutieli 2001), each true null contributes at most q/m for super-uniform null p-values (equality for continuous uniform nulls).
    - Summing over the m₀ nulls gives FDR ≤ q m₀/m ≤ q; equality holds for independent continuous uniform null p-values.

## Glossary

- **Consulting.**
  - Estimand; smallest effect worth detecting; protocol; pre-registration; CONSORT: the shape of a design question.
- **Cluster trials.**
  - Unit of randomization; contamination; intraclass correlation; design effect; cluster-level analysis; the floor
    on clusters: the cluster trial's vocabulary.
- **Observational analysis.**
  - Confounding by indication; back-door set; mediator; collider; bad control: what the graph decides.
- **Sensitivity.**
  - Robustness value; partial R²; benchmark: how strong a hidden confounder would need to be.
- **The exam.**
  - Score; information; sandwich; IRLS; working response; REML; error contrasts; partial pooling; R̂; ESS; AIC; BIC;
    bandwidth; LSCV; influence function; sensitivity curve; KKT conditions; FDR; step-up; conformal quantile;
    Greenwood's formula; log-log interval: the exam's tools.

## Where it comes back

- **Part 43**: what a random variable is, and why the limit theorems hold.
- **Part 47**: the sandwich's asymptotics, proved.
- **Part 49**: AIPW attains the semiparametric efficiency bound.
- **Part 55**: the qualifying exam, the PhD's version of this part.
- **Part 58**: anytime-valid inference and adaptive designs revisit trial design.


## Scientific conditions and QA scope

The trial calculations assume independent Gaussian towns with equal measured cluster sizes and negligible between-town interference. The floor on town counts is for the unadjusted equal-size approximation. Randomization alone does not guarantee exactly unbiased arbitrary ANCOVA adjustment in finite samples. The sensitivity display uses one seeded completed dataset and classical OLS geometry; it is separate from pooled MI-AIPW inference. Its updated RV is 0.0744, approximate significance RV 0.0407, with benchmark coordinates (0.0398, 0.0331).

The worked survey uses 40 imputations; the 400-survey Board uses 10 per survey. Normal income imputation, fitted/clipped propensities and Rubin pooling are working procedures, with calibration checked empirically. Mean balance and observed overlap do not prove causal exchangeability or population positivity. The Board now records actual independent replications and empirical MCSEs. Zero observed coverage does not establish that the underlying coverage probability is exactly zero.

The full eight-schools posterior integrates tau over [0, infinity); the [0,30] plot excludes 0.501% of mass from display only. School A's full posterior mean is 11.40. The ozone exercises use 111 jointly complete air-quality days. Seasonal/serial exchangeability is unverified, so their conformal intervals illustrate the procedure without certifying a future-day time-series guarantee. Gehan's ordinary log-rank calculation ignores the original matching; its confidence bands are approximate pointwise bands under independent censoring.

[Scientific review and verification evidence](../../../docs/qa/evidence/stats42-polish-20261107/source-review.md) records numerical checks and source-data scope. English visual review is in progress. Chinese narration/captions, continuous listening/playback and final masters remain open. The MSc milestone denotes this course's level, not an accredited qualification.

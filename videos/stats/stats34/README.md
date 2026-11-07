# Statistics, Built — Part 34: Prediction with Guarantees

Part 34 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the fourteenth part of Stage III, Master's. Part 33 controlled the error
rates of many questions at once, with knockoff exchangeability, conditional-null and flip-sign conditions. This part asks how far that goes for
prediction:
- forests and boosting treated as estimators, with a variance, an importance measure and intervals;
- what cross-validation estimates, and when a predicted probability can be trusted;
- conformal prediction, which gives marginal finite-sample coverage with exchangeable calibration/test scores and a separately trained model;
- prediction-powered inference, which turns a model's biased guesses into valid estimates;
- what interpretation methods estimate.

Its builds are `statkit.conformal` and `statkit.ppi`. Its instrument is the score ladder (`ScoreLadder`): n
calibration scores sorted as bars, the conformal rank k = ⌈(n + 1)(1 − α)⌉ picked out, the threshold drawn across,
and the gap a new score falls into.

It opens with Breiman's "Statistical Modeling: The Two Cultures" (2001), with Cox's and Efron's replies, and a forest
on the Wisconsin breast cancer data that says "malignant, probability 0.83" for one held-out patient.

From there the part covers:
- **Explain or predict?** Shmueli (2010); the bias–variance decomposition of EPE, and when a wrong model predicts
  better in an orthogonal-regression approximation (β₂² Var x₂ < σ²/n).
  - 50 bootstrap depth-3 trees on 400 biopsies: test accuracy 93.4% ± 1.8, but 5 different root features (worst
    concave points 21 times, mean concave points 11, worst perimeter 10, worst area 4, worst radius 4) and 39
    different "top three" lists. Radius, perimeter and area correlate 0.94–0.998.
  - Three logistic regressions on disjoint feature pairs: 95.3%, 95.3%, 92.9%.
  - The Rashomon set and model class reliance (Fisher, Rudin & Dominici 2019).
- **Forests.** Bagging (Breiman 1996) and random forests (Breiman 2001).
  - Var = ρσ² + (1 − ρ)σ²/B, measured on Friedman 1 (n = 300, 40 training sets × 40 trees, 200 test points):

    | m_try | σ² (one tree) | ρ | Var (forest of 40) | bias² | MSE |
    |---|---|---|---|---|---|
    | 10 (bagging) | 8.11 | 0.128 | 1.22 | 3.31 | 4.53 |
    | 5 | 9.86 | 0.068 | 0.90 | 3.57 | 4.47 |
    | 3 | 11.73 | 0.044 | 0.80 | 4.27 | 5.07 |
    | 1 | 14.99 | 0.024 | 0.72 | 8.39 | 9.12 |

  - Breast cancer (plus two pure-noise columns), 169 test cases: one deep tree 7.1% wrong, bagging 5.9%, forest
    (m_try = 6) 5.9%; OOB error 3.5%.
  - Consistency: Biau, Devroye & Lugosi (2008), Biau (2012), Scornet, Biau & Vert (2015); Wager & Athey (2018).
  - Importance: impurity importance credits the continuous noise column 15× the coin-flip column (Strobl et al.
    2007); permutation importance gives both ≈ 0.
  - The infinitesimal jackknife (Wager, Hastie & Efron 2014) at a peak of Friedman 1 (μ(x₀) = 22.55), n = 250, 300
    forests:
    - bootstrap forests of 500 trees have an independent pilot estimate E f̂(x₀) = 20.571 (MCSE 0.037, 200 pilot forests). Intervals cover this reference in 60.3% of 300 independent forests, because
      the mean SE is 0.39 against a true SD of 0.56;
    - subsampled CART forests (s = 50, 2,000 trees) cover their independent pilot reference 83.7% of the time. The reference is 18.798 (MCSE 0.048, 100 pilot forests); intervals cover μ(x₀) 0% of the time. Subsampling alone does not implement Wager–Athey honest forests or establish their theorem. Pilot-reference coverage also has Monte Carlo uncertainty.
- **Boosting.** AdaBoost (Freund & Schapire 1997) as forward stagewise additive modelling (Friedman, Hastie &
  Tibshirani 2000) and gradient boosting (Friedman 2001).
  - A 1-D stump staircase.
  - Friedman 1 (n = 400, depth 2, 3,000 test points): ν = 1 bottoms out at MSE 6.63 after 59 trees, then rises;
    ν = 0.1 reaches 2.64 at 600 trees; a forest gives 5.43; the noise is 1. The minimum on the plotted test curve is an oracle comparison, not a cross-validated choice. Smaller learning rates need not always improve generalization.
  - The exponential loss's minimizer is half the log odds; LogitBoost; the stagewise–lasso link under additional path/monotonicity conditions; XGBoost.
- **What cross-validation estimates** (Bates, Hastie & Tibshirani 2024). OLS, n = 100, p = 20, σ = 1, 1,000 data
  sets, with Err_XY = 1 + ‖β̂ − β‖² known exactly and Err = 1 + p/(n − p − 1) = 1.253:
  - corr(CV, Err_XY) = 0.013;
  - SD of Err_XY is 0.090 and SD of the CV estimate 0.222; mean CV 1.289;
  - the naive 90% interval covers Err 82.8% (and Err_XY 80.2%); the true SD is 1.23× the naive SE;
  - nested CV; selection bias in CV (Ambroise & McLachlan 2002; Varma & Simon 2006).
- **Calibration.** Reliability diagrams and ECE; Gaussian naive Bayes on all 30 features (40 splits of 300 train /
  135 calibrate / 134 test). 98% of its predictions fall below 0.1 or above 0.9; the fitted temperature is
  T̂ = 7.9.

  | Model | Accuracy | Mean-split ECE | Brier |
  |---|---|---|---|
  | naive Bayes | 93.7% | 0.062 | 0.059 |
  | + Platt | 93.7% | 0.049 | 0.045 |
  | + temperature | 93.7% | 0.053 | 0.044 |
  | + isotonic | 93.3% | 0.038 | 0.047 |
  | forest | 95.7% | 0.052 | 0.035 |
  | + isotonic | 95.6% | 0.033 | 0.035 |

  ECE is averaged over splits, while the reliability diagram pools held-out predictions; these are distinct summaries. Forests can be underconfident at the extremes (Niculescu-Mizil & Caruana 2005); multicalibration.
- **Split conformal** (Vovk, Gammerman & Shafer 2005; Papadopoulos et al. 2002; Lei et al. 2018).
  - Exchangeability and uniform ranks; the quantile lemma, coverage ≥ 1 − α. The upper bound 1 − α + 1/(n + 1) requires no score ties.
  - The score ladder with 19 scores: k = 18, q = 21.0; 20,000 simulated draws cover 90.14% (exact 18/20).
  - For i.i.d. continuous scores conditional on the separately fitted model, coverage given the calibration set has distribution Beta(k, n + 1 − k); exchangeability alone is insufficient for this Beta law. Its central 90% range is 0.774–0.981 for n = 19,
    0.847–0.944 for n = 99, and 0.884–0.915 for n = 999.
  - World incomes from a cubic in age with a retirement step: q̂ = 44.5 (thousand dollars), coverage 90.4%; by age,
    95.8% (18–24) down to 83.4% (55–66).
  - The impossibility of useful exact distribution-free conditional coverage over unrestricted response laws and nonatomic covariates (Vovk 2012; Lei & Wasserman 2014; Barber et al. 2021), rather than an impossibility for every restricted model or groupwise target.
- **Jackknife+ and CQR.**
  - Barber, Candès, Ramdas & Tibshirani (2021): n = 100, least squares (minimum-norm past p = n), 60 data sets per p.
    At p = n coverage is 0% in-sample, 53% for the jackknife, 95% for jackknife+ and 87% for split. These are experimental results. The general exchangeable-data jackknife+ bound is 1 − 2α (80% here); a near-90% guarantee needs stability or other conditions. CV+ also has a finite-fold correction.
  - CV+ with a forest on the diabetes data (10 splits): 90.5% coverage, width 184; split gives 90.8%, width 191.
  - CQR (Romano, Patterson & Candès 2019) on the World's incomes: 5% and 95% linear quantile regressions, Q̂ = 0.03,
    coverage 90.2%. By age group CQR ranges 88.2%–91.2%, against 83.4%–95.8% for the fixed-width band; its width runs
    from 59 (18–24) to 120 (55–66).
- **Under shift.**
  - Weighted conformal (Tibshirani, Barber, Candès & Ramdas 2019), with test ages tilted to 40–60 and 200
    repetitions: unweighted q̂ = 42.5 covers 87.1%; weighted q̂ ≈ 47.6 covers 90.3%. Calibration and test cases are independent draws with replacement from the World population; weights are known density ratios and P(Y|X) remains unchanged.
  - Estimating w by a classifier; nonexchangeable conformal (Barber et al. 2023).
  - Adaptive conformal inference (Gibbs & Candès 2021) on a stream whose noise triples for t = 1,000–2,000:
    - static split conformal covers 74.6% overall and 44.8% in the storm;
    - ACI with γ = 0.01 covers 90.0% overall and 89.5% in the storm;
    - The deterministic long-run bound under the stated extreme-quantile conventions; it does not imply local or conditional coverage.
- **Classification sets.** LAC (Sadinle, Lei & Wasserman 2019) and APS (Romano, Sesia & Candès 2020).
  - Randomized APS uses the same auxiliary uniform in calibration and candidate scoring and can give an empty set; smallest-set oracle claims concern known true probabilities, not a universal property of fitted estimates.
  - Irises, sepals only, QDA (75.8% accurate), 300 splits: coverage 91.2%. Set sizes 0/1/2/3 occur 2.3%, 50.9%,
    46.5% and 0.4% of the time. Mean size is 1.00 for setosa, 1.71 for versicolor and 1.64 for virginica.
  - Coverage by species is 93.0%, 91.4% and 89.7% with one threshold; Mondrian gives 94.1%, 92.8% and 93.9%.
  - Breast cancer, logistic on three features, 95% LAC sets (200 splits): coverage 95.3% (benign 96.4%, malignant
    93.6%); one label 97.4%, both 0.4%, empty 2.3%.
  - Conformal p-values with BH (Bates et al. 2023).
- **Prediction-powered inference** (Angelopoulos, Bates, Fannjiang, Jordan & Zrnic 2023), on the World's mean systolic
  blood pressure (truth 123.69 mm Hg).
  - 300 clinic visits (mean of three cuff readings); 20,000 smartwatch guesses. The watch is a forest on age, sex,
    BMI and a pulse-wave signal (pressure + N(0, 9²)), trained on 2,000 users aged 18–50. Its correlation with the
    truth is 0.86, but it reads 2.9 low overall and 151 → 136 for the over-80s.
  - One draw:

    | Estimate | Value | 90% interval |
    |---|---|---|
    | classical | 123.22 | [121.64, 124.81] |
    | naive | 120.76 | [120.61, 120.90] |
    | PPI | 124.02 | [123.18, 124.86] |

  - Mean SE: 1.00 classical against 0.536 PPI and 0.536 PPI++; the PPI++ precision ratio makes 300 visits act like ≈ 1,045. Samples are independent representative draws with replacement from all adults with recorded cuff outcomes; the target is the fixed empirical World population, including training members, with predictions fixed before the study draws. Fixed-function, fixed-weight mean unbiasedness is distinguished from asymptotic Wald inference and estimated-weight PPI++.
  - A loose strap (extra noise, SD 25): classical 1.00, PPI 1.55, PPI++ (λ̂ ≈ 0.23) 0.92.
  - The survey sampling lineage: the difference estimator (Cassel, Särndal & Wretman 1976; Breidt & Opsomer 2017).
- **Interpretation as estimation.**
  - Friedman 1 plus a twin of x₁ (correlation ≈ 0.97), forest of 200 trees.
  - The PDPs of x₄ and x₃ against the truth.
  - Permutation importance gives x₁ 3.49 and the twin 1.96; LOCO gives 0.42 and 0.04 (Hooker, Mentch & Zhou 2021;
    Williamson et al. 2021).
  - Exact Shapley values over five features: +1.04, +1.54, +0.24, +2.93, −0.20, summing from 14.74 to 20.30 (Shapley
    1953; Lundberg & Lee 2017). This is a five-player game with the other six features averaged over the 120-case background; 20.30 is its grand-coalition value, not the full eleven-feature prediction 21.14. Signed importance estimates and partial-dependence values are retained rather than clamped.
- **Outro.** Caruana et al. (2015): a pneumonia-mortality model with a misleading association between asthma and lower observed risk; intensive care is a proposed mechanism, not a causal effect established by that association.

Data:
- the Wisconsin breast cancer data (Wolberg, Street & Mangasarian 1995), Fisher's irises and the diabetes data are
  the Museum's;
- incomes and blood pressure are the World's;
- the rest are seeded simulations, mostly on Friedman's (1991) test function.

**Built in this part:**
- **`statkit.conformal`** ([`explainer/stats/kit/conformal.py`](../../../explainer/stats/kit/conformal.py)):
  - **Trees and ensembles:** CART with cumulative-sum split search and impurity gains; random forests (bootstrap or
    subsampled) with OOB predictions, permutation importance and the bias-corrected infinitesimal jackknife (Wager,
    Hastie & Efron), with a subsampled CART teaching variant distinct from Wager–Athey honest forests; L2 boosting.
  - **Calibration:** reliability diagrams and ECE; Platt, isotonic (PAVA) and temperature scaling.
  - **Conformal:** the conformal quantile, split conformal, jackknife+/CV+, CQR, weighted conformal, adaptive conformal
    inference, APS scores and sets, Mondrian quantiles, conformal p-values.
- **`statkit.ppi`** ([`explainer/stats/kit/ppi.py`](../../../explainer/stats/kit/ppi.py)): classical, naive and
  prediction-powered means (PPI++'s tuned λ), and PPI least squares with its sandwich variance.
- Both are checked in `tests/test_stats_kit_conformal.py`:
  - the conformal quantile's exact coverage;
  - jackknife+ and CQR coverage;
  - trees and forests: OOB, permutation importance, the IJ for bootstrap and subsampled forests;
  - PPI's unbiasedness and its gain over the classical estimate;
  - the score ladder.
- **The Museum** gains `breast_cancer()`.
- **The score ladder** (`ScoreLadder` in `explainer/stats/viz.py`).

The Coverage Board gains fourteen rows, all with nominal 90%. Rows whose replications each average many test points
retain the actual replication count and an empirical standard error from independent per-replication coverage fractions, rather than inventing independent test draws:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| split conformal,  90% | World incomes,  cubic in age,  n_cal = 500 | 90.0% | kept |
| CQR,  90% | World incomes,  cubic in age,  n_cal = 500 | 89.8% | kept |
| in-sample residuals,  90% | least squares,  p = n = 100 | 0.0% | broken |
| jackknife+,  90% | least squares,  p = n = 100 | 89.3% | kept |
| split conformal,  unweighted | test ages shifted to 40--60 | 86.9% | broken |
| weighted conformal,  90% | test ages shifted to 40--60 | 90.2% | kept |
| classical,  300 clinic visits | World blood pressure,  90% | 89.2% | kept |
| watch guesses as data | World blood pressure,  20,000 guesses | 0.0% | broken |
| prediction-powered | World blood pressure,  90% | 87.2% | kept |
| PPI++  (tuned λ) | World blood pressure,  90% | 87.2% | kept |
| forest IJ,  bootstrap,  for E f̂(x₀) | Friedman 1,  n = 250,  500 trees | 60.3% | broken |
| forest IJ,  subsampled,  for E f̂(x₀) | Friedman 1,  s = 50 of 250 | 83.7% | broken |
| forest IJ,  subsampled,  for μ(x₀) | Friedman 1,  at a peak | 0.0% | broken |
| naive 10-fold CV interval,  90% | least squares,  n = 100,  p = 20:  for Err | 82.8% | broken |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats34.compute    # once (about forty minutes; single-threaded BLAS is faster here)
python tools/build.py stats34 -q l                          # fast 480p preview
python tools/build.py stats34                               # 1080p30 -> renders/stats34.mp4
python tools/qa_scene.py stats34 Split
python tools/lecture_length.py stats34 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The two cultures | 98% vs 2%; a forest at 94.1% |
| 1 | Explain or predict? | 5 root features, 39 top-three lists |
| 2 | Forests | ρ 0.128 → 0.024; IJ covers 60% / 84% |
| 3 | Boosting | ν = 0.1: 2.64 vs ν = 1: 6.63 |
| 4 | What cross-validation estimates | corr 0.013; naive CI 82.8% |
| 5 | Calibration | ECE 0.062 → 0.038; T̂ = 7.9 |
| 6 | Split conformal | 90.4%; 95.8% vs 83.4% by age |
| 7 | Jackknife+ and CQR | p = n: 0%, 53%, 95% |
| 8 | Under shift | 87.1% → 90.3%; ACI 44.8% → 89.5% |
| 9 | Classification sets | 91.2%; sizes 1.00 vs 1.71 |
| 10 | Prediction-powered inference | 300 visits ≈ 1,045 |
| 11 | Interpretation as estimation | permutation 3.49 / 1.96 vs LOCO 0.42 / 0.04 |
| 12 | Outro | asthma and pneumonia |

## Sources

- **The two cultures.**
  - L. Breiman, *Stat. Sci.* 16 (2001), with comments by D. R. Cox, B. Efron, B. Hoadley and E. Parzen.
  - G. Shmueli, *Stat. Sci.* 25 (2010).
  - A. Fisher, C. Rudin & F. Dominici, *JMLR* 20 (2019); L. Semenova, C. Rudin & R. Parr, *FAccT* (2022).
- **Forests.**
  - L. Breiman, *Mach. Learn.* 24 (1996), 45 (2001); T. K. Ho (1995); Y. Amit & D. Geman, *Neural Comput.* 9
    (1997).
  - G. Biau, L. Devroye & G. Lugosi, *JMLR* 9 (2008); G. Biau, *JMLR* 13 (2012); E. Scornet, G. Biau & J.-P. Vert,
    *Ann. Stat.* 43 (2015).
  - C. Strobl, A.-L. Boulesteix, A. Zeileis & T. Hothorn, *BMC Bioinf.* 8 (2007).
  - B. Efron, *JASA* 109 (2014); S. Wager, T. Hastie & B. Efron, *JMLR* 15 (2014); S. Wager & S. Athey, *JASA* 113
    (2018).
  - J. Friedman, *Ann. Stat.* 19 (1991) (the test function).
- **Boosting.**
  - M. Kearns & L. Valiant (1988); R. Schapire, *Mach. Learn.* 5 (1990); Y. Freund & R. Schapire, *JCSS* 55 (1997).
  - J. Friedman, T. Hastie & R. Tibshirani, *Ann. Stat.* 28 (2000); J. Friedman, *Ann. Stat.* 29 (2001), *CSDA* 38
    (2002).
  - S. Rosset, J. Zhu & T. Hastie, *JMLR* 5 (2004); T. Chen & C. Guestrin, *KDD* (2016); L. Grinsztajn, E. Oyallon &
    G. Varoquaux, *NeurIPS* (2022).
- **Cross-validation.**
  - M. Stone, *JRSS B* 36 (1974); S. Geisser, *JASA* 70 (1975).
  - C. Ambroise & G. McLachlan, *PNAS* 99 (2002); S. Varma & R. Simon, *BMC Bioinf.* 7 (2006).
  - S. Bates, T. Hastie & R. Tibshirani, *JASA* 119 (2024); T. Hastie, R. Tibshirani & J. Friedman, *ESL*, §7.12.
- **Calibration.**
  - G. Brier, *Mon. Weather Rev.* 78 (1950); A. Murphy & R. Winkler, *Appl. Stat.* 26 (1977).
  - J. Platt (1999); B. Zadrozny & C. Elkan, *KDD* (2002); A. Niculescu-Mizil & R. Caruana, *ICML* (2005).
  - C. Guo, G. Pleiss, Y. Sun & K. Weinberger, *ICML* (2017); Ú. Hébert-Johnson, M. Kim, O. Reingold & G. Rothblum,
    *ICML* (2018).
- **Conformal.**
  - V. Vovk, A. Gammerman & G. Shafer, *Algorithmic Learning in a Random World* (2005; 2nd ed. 2022).
  - H. Papadopoulos, K. Proedrou, V. Vovk & A. Gammerman, *ECML* (2002); V. Vovk, *ACML* (2012).
  - J. Lei, M. G'Sell, A. Rinaldo, R. Tibshirani & L. Wasserman, *JASA* 113 (2018); J. Lei & L. Wasserman, *JRSS B* 76
    (2014).
  - R. Barber, E. Candès, A. Ramdas & R. Tibshirani, *Ann. Stat.* 49 (2021), *Inf. Inference* 10 (2021), *Ann. Stat.*
    51 (2023).
  - B. Kim, C. Xu & R. Barber, *NeurIPS* (2020).
  - Y. Romano, E. Patterson & E. Candès, *NeurIPS* (2019); Y. Romano, M. Sesia & E. Candès, *NeurIPS* (2020).
  - R. Tibshirani, R. Barber, E. Candès & A. Ramdas, *NeurIPS* (2019); I. Gibbs & E. Candès, *NeurIPS* (2021).
  - M. Sadinle, J. Lei & L. Wasserman, *JASA* 114 (2019); S. Bates, E. Candès, L. Lei, Y. Romano & M. Sesia, *Ann.
    Stat.* 51 (2023).
  - A. Angelopoulos & S. Bates, *Found. Trends Mach. Learn.* 16 (2023).
- **PPI.**
  - A. Angelopoulos, S. Bates, C. Fannjiang, M. Jordan & T. Zrnic, *Science* 382 (2023); A. Angelopoulos, J. Duchi &
    T. Zrnic, PPI++ (2023).
  - C. Cassel, C.-E. Särndal & J. Wretman, *Biometrika* 63 (1976); F. J. Breidt & J. Opsomer, *Stat. Sci.* 32 (2017).
- **Interpretation.**
  - J. Friedman (2001) (partial dependence); L. Shapley (1953); E. Štrumbelj & I. Kononenko, *JMLR* 11 (2010);
    S. Lundberg & S.-I. Lee, *NeurIPS* (2017).
  - G. Hooker, L. Mentch & S. Zhou, *Stat. Comput.* 31 (2021); B. Williamson, P. Gilbert, N. Simon & M. Carone,
    *JASA* 116 (2021).
- **Asthma and pneumonia.**
  - R. Caruana, Y. Lou, J. Gehrke, P. Koch, M. Sturm & N. Elhadad, *KDD* (2015); G. Cooper et al., *Artif. Intell.
    Med.* 9 (1997).
- **Data.**
  - W. Wolberg, W. N. Street & O. Mangasarian (1995), via scikit-learn; R. A. Fisher, *Ann. Eugen.* 7 (1936);
    B. Efron, T. Hastie, I. Johnstone & R. Tibshirani, *Ann. Stat.* 32 (2004).

## Problems and solutions

1. **The forest's variance.** Let t₁, …, t_B have common variance σ² and pairwise correlation ρ.
   - Var(Σ t_b / B) = B⁻² (Σ_b Var t_b + Σ_{b≠b'} Cov(t_b, t_b')) = B⁻² (Bσ² + B(B − 1)ρσ²) = ρσ² + (1 − ρ)σ²/B.
   - As B → ∞ this falls to ρσ². The excess over the limit is (1 − ρ)σ²/B, so it is within 5% of the limit once
     (1 − ρ)/(Bρ) ≤ 0.05; for ρ = 0.1, that is B ≥ 180.
2. **What AdaBoost estimates.** With p = P(Y = 1 | x), E[e^{−YF} | x] = p e^{−F} + (1 − p) e^{F}.
   - The derivative in F is −p e^{−F} + (1 − p) e^{F}, which is 0 when e^{2F} = p/(1 − p).
   - So F* = ½ log{p/(1 − p)}. The second derivative is positive, so this is the minimum.
3. **The quantile lemma.** By exchangeability and continuity, the rank R of S_{n+1} among the n + 1 scores is uniform
   on {1, …, n + 1}.
   - S_{n+1} ≤ S_(k) (the k-th smallest of the first n) if and only if R ≤ k. So P = k/(n + 1).
   - With k = ⌈(n + 1)(1 − α)⌉ we have (n + 1)(1 − α) ≤ k < (n + 1)(1 − α) + 1.
   - Dividing by n + 1 gives 1 − α ≤ P < 1 − α + 1/(n + 1).
4. **Conditional coverage.** Assume calibration and test scores are i.i.d. with continuous distribution F conditional on a separately trained model. Given the calibration scores, coverage is F(S_(k)).
   - For continuous F, the values U_i = F(S_i) are i.i.d. uniform, and F(S_(k)) = U_(k).
   - The k-th order statistic of n uniforms is Beta(k, n + 1 − k), with mean k/(n + 1).
5. **PPI.** θ̂_λ = λ f̄_N − (λ f̄_n − ȳ_n).
   - For a fixed prediction function, independent representative samples and fixed λ, its expectation is λ E f − λ E f + E Y = θ. Estimating λ on the labelled sample need not preserve exact unbiasedness.
   - The two samples are independent, so Var = λ² Var(f)/N + Var(Y − λf)/n
     = λ² Var f (1/N + 1/n) − 2λ Cov(Y, f)/n + Var Y/n.
   - Setting the derivative in λ to zero gives λ* = Cov(Y, f) / ((1 + n/N) Var f), PPI++'s choice. At λ = 0 the
     estimator is the classical one, so the population variance optimum is never worse. Estimated weights achieve this only asymptotically under appropriate moment and consistency conditions.
6. **The ACI bound.** Assume γ > 0, α₁ ∈ [0, 1], target α ∈ (0, 1), and the quantile convention q̂ = −∞ when α_t ≥ 1 and +∞ when α_t ≤ 0.
   - Then α_t stays in [−γ, 1 + γ]: when α_t < 0 the band is infinite, no miss occurs, and α_t rises. When α_t > 1
     every step is a miss, and α_t falls.
   - Summing the update over t gives α_{T+1} − α₁ = γ Σ_t (α − err_t).
   - So |T⁻¹ Σ err_t − α| = |α_{T+1} − α₁|/(γT) ≤ (max(α₁, 1 − α₁) + γ)/(γT).

## Glossary

- **Rashomon set**: all models in a class whose loss is within ε of the best.
- **Bagging; random forest**: averaging trees grown on bootstrap samples; with m_try random features per split.
- **Out-of-bag (OOB)**: the prediction for a case from the trees whose sample did not include it.
- **Impurity / permutation importance**: a feature's total reduction in training loss across splits / the rise in
  held-out loss when it is scrambled.
- **Infinitesimal jackknife (IJ)**: Σ_i Cov_b(N_bi, t_b(x))², a variance estimate for a bagged predictor.
- **Forward stagewise additive modelling**: adding one basis function at a time without refitting the others;
  boosting.
- **Err_XY / Err**: the error of the fitted model on new data / its average over training sets.
- **Calibration; ECE**: P(Y = 1 | p̂ = p) = p; the count-weighted mean gap in a reliability diagram.
- **Exchangeable**: a joint distribution invariant to permutations.
- **Conformal quantile**: the ⌈(n + 1)(1 − α)⌉-th smallest calibration score.
- **Split conformal; jackknife+; CV+**: conformal intervals from a held-out calibration set; from leave-one-out or
  K-fold models.
- **CQR**: conformalized quantile regression.
- **Covariate shift; weighted conformal**: a change in P_X with P_{Y|X} fixed; calibration scores reweighted by
  dP̃/dP.
- **ACI**: adaptive conformal inference, α_{t+1} = α_t + γ(α − err_t).
- **LAC; APS; Mondrian**: least-ambiguous sets; adaptive prediction sets; class- or group-wise calibration.
- **Conformal p-value**: (1 + #{S_i ≥ S})/(n + 1).
- **PPI; rectifier; PPI++**: prediction-powered inference; the mean guess error on labelled data; the
  variance-tuned λ.
- **PDP; LOCO; Shapley value**: partial dependence; leave-one-covariate-out importance; average marginal
  contribution over coalitions.

## Where it comes back

- **Part 35**: prediction is not intervention; potential outcomes.
- **Part 36**: forests and boosting as nuisance fits in double machine learning.
- **Part 40**: survival forests; conformal bands for censored times.
- **Part 54**: generalization bounds for learning algorithms.
- **Part 57**: distribution-free inference proved, with its impossibility theorems (the upgrade card).
- **Part 58**: anytime-valid inference, kin to ACI's sequence-wise guarantee.
- **Part 60**: distribution shift in depth.
- **Part 62**: causal forests and heterogeneous treatment effects.
- **Part 64**: machine-learning and LLM labels; PPI's successors.

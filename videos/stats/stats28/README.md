# Statistics, Built — Part 28: Which Model?

Part 28 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the eighth part of Stage III, Master's. Part 27 made any model we can write
down computable. This part asks which of them to believe, and how to choose without fooling yourself:
- the optimism of training error, and degrees of freedom for any procedure;
- Cp, AIC, TIC and AICc; BIC, consistency and efficiency; cross-validation and what it estimates;
- Bayesian leave-one-out with Pareto-smoothed importance sampling, WAIC, and singular models;
- minimum description length, model averaging and stacking, inference after selection, subset selection, and
  calibrated forecasts.

Its instrument is the model-selection bench (`CriterionBench`), on which each candidate's misfit and penalty are
stacked, and the criterion's choice is the lowest total. Its kit is `statkit.select`.

It opens with Freedman's paradox (1983): 100 observations, 50 predictors, all independent noise.
- Round 1: R² = 0.455, overall F = 0.82, p = 0.76. Fourteen predictors have p < 0.25; two have p < 0.05.
- Round 2, on the fourteen kept: R² = 0.268, F = 2.23, p = 0.013, and four coefficients significant at 5%.
- Over 1,000 repeats, round 2 is significant at 5% in 94.7% (median 12 kept, 5.6 significant on average).

From there the part covers:
- **Optimism.**
  - Thirty points from a smooth curve with noise SD 0.5; polynomials of degree 0–12, 600 data sets. Training error
    falls to 0.142; error on new responses is about 0.30 from degree 3 to 6 (minimum 0.299 at 5), then rises to 0.355.
  - Efron's covariance formula: optimism = (2/n) Σ Cov(ŷᵢ, yᵢ) = 2σ²d/n for a linear fit (degree 3: 0.067 simulated,
    0.067 by formula); the bias–variance anatomy of the gap.
  - Degrees of freedom: tr S for linear smoothers, Stein's divergence, and Monte Carlo for anything. The lasso on
    the prostate predictors (600 simulated responses per λ):

    | λ | df, simulated | 1 + E(nonzero) |
    |---|---|---|
    | 0.02 | 7.98 | 8.05 |
    | 0.08 | 6.46 | 6.07 |
    | 0.2 | 4.58 | 4.61 |
    | 0.4 | 2.96 | 2.95 |

- **Cp and AIC.**
  - Mallows's Cp; AIC as an estimate of expected KL, derived by two Taylor expansions (optimism k).
  - TIC: tr(ĴK̂⁻¹) for a Poisson regression of the World's doctor visits (mean 2.42, variance 13.7) is 9.47 against
    k = 2; on Poisson data, 1.81. AICc (Sugiura 1978; Hurvich & Tsai 1989).
  - The bench on Stamey's prostate data (67 training men, best subset of each size): AIC chooses 7 predictors
    (all but gleason). ΔAIC: 6 predictors 0.46, 4 1.28, 5 1.74, 8 1.98, 3 3.42, 2 5.49.
- **BIC.**
  - Laplace's method derived; the unit-information prior (Kass & Wasserman 1995).
  - On the bench, log 67 = 4.20 per parameter: BIC chooses 2 (lcavol, lweight).
  - AIC as a likelihood-ratio test at level P(χ²₁ > 2) = 0.157.
  - Truth a quadratic, degrees 0–6, 300 data sets per n. P(choose degree 2):

    | n | 20 | 50 | 100 | 200 | 500 | 1,000 | 3,000 |
    |---|---|---|---|---|---|---|---|
    | AIC | 0.41 | 0.67 | 0.71 | 0.73 | 0.77 | 0.76 | 0.72 |
    | AICc | 0.46 | 0.74 | 0.74 | 0.76 | 0.77 | 0.77 | 0.72 |
    | BIC | 0.43 | 0.81 | 0.96 | 0.97 | 0.98 | 0.997 | 0.993 |

  - Truth sin(2x)e^{0.3x}, degrees 0–12, prediction risk of each criterion's choice:

    | n | AIC | AICc | BIC |
    |---|---|---|---|
    | 50 | 0.874 | 0.311 | 0.071 |
    | 200 | 0.0118 | 0.0114 | 0.0107 |
    | 1,000 | 0.00252 | 0.00250 | 0.00297 |

    Consistency against efficiency (Shibata 1981; Yang 2005).
- **Cross-validation theory.**
  - PRESS and GCV for linear smoothers; across 400 regressions they correlate at 0.986.
  - Prostate, 10-fold CV with the search redone in each fold: CV error 1.47, 0.70, 0.60, 0.70, 0.66, 0.67, 0.62,
    0.57, 0.59 for sizes 0–8. The minimum is at 7, and sizes 2 and 4–8 lie within one SE; the one-SE rule picks 2.
    PRESS (no search inside) is smoother and lower at sizes 3–5 (0.59, 0.58, 0.59).
  - What CV estimates (Bates, Hastie & Tibshirani 2024). In 400 simulated regressions (n = 50, 10 predictors, 4
    real), corr(CV, this fit's true error) = −0.06, while mean CV 1.32 matches the mean error 1.30.
  - Choosing K (Breiman & Spector 1992; Kohavi 1995).
- **Bayesian LOO and WAIC**, on the eight schools:

  | Model | PSIS-LOO elpd | exact LOO | p_loo | k̂ | WAIC | p_WAIC |
  |---|---|---|---|---|---|---|
  | complete pooling | −30.56 | −30.56 | 0.68 | all < 0.26 | −30.54 | 0.66 |
  | hierarchical | −31.21 | −31.34 | 1.58 | 0.40–0.71 | −30.99 | 1.36 |
  | no pooling | −36.97 | — | 6.89 | 0.78–1.06 | −34.08 | 4.01 |

  WAIC is three points too optimistic exactly where k̂ warns.
- **Singular models.**
  - The mixture (1 − a)N(0, 1) + aN(b, 1) at a N(0, 1) truth: the true set is a cross.
  - Watanabe's free energy, λ log n − (m − 1) log log n, with λ = ½, m = 2 by hand. By quadrature for n = 30 to
    10,000, the free energy grows with slope 0.42 in log n (theory ½, less a log log term), against 0.98 for a regular
    two-parameter model (theory 1).
  - RLCTs of other models; WBIC and sBIC.
- **MDL.**
  - Kraft and Shannon; the two-part code on chapter one's 30 points is shortest at degree 5 (40.9 bits); ½ log₂ n
    per coefficient is BIC.
  - Shtarkov's NML and its regret for a coin, exactly and by ½ log(nπ/2):

    | n | 10 | 30 | 100 | 300 | 1,000 | 3,000 | 10,000 |
    |---|---|---|---|---|---|---|---|
    | regret | 1.539 | 2.021 | 2.581 | 3.108 | 3.696 | 4.239 | 4.836 |
    | ½ log(nπ/2) | 1.377 | 1.926 | 2.528 | 3.078 | 3.680 | 4.229 | 4.831 |

  - Dawid's prequential codes.
- **Averaging.**
  - BMA (Hoeting et al. 1999), Occam's window, MC³, priors on models (Scott & Berger 2010).
  - M-closed and M-open. The truth is ½N(−2, 1) + ½N(2, 1); the two candidates are N(−2, 1) and N(2, 1), 100 data sets
    per n:

    | n | 20 | 50 | 100 | 200 | 500 |
    |---|---|---|---|---|---|
    | BMA's weight on its favourite | 0.988 | 0.992 | 0.991 | 0.993 | 0.998 |
    | stacking's | 0.593 | 0.561 | 0.541 | 0.527 | 0.519 |
    | log score, best single | −5.33 | −5.31 | −5.30 | −5.26 | −5.16 |
    | log score, BMA | −5.03 | −5.19 | −5.04 | −5.17 | −5.18 |
    | log score, stacking | −2.09 | −2.06 | −2.06 | −2.05 | −2.06 |

    The truth's own score is −2.05.
  - Stacking (Wolpert 1992; Breiman 1996; Yao et al. 2018).
  - Prostate Akaike weights peak at 0.30 (size 7) and spread over sizes 4–8. BIC weights split 0.30 / 0.28 / 0.27
    over sizes 2, 3 and 4.
- **Inference after selection.**
  - The winner's curse for β₁ = 0.05 with SE 0.1. AIC keeps it 21% of the time, when |β̂₁| averages 3.9 times the
    truth; the conditional coverage of the usual 95% interval is 0.161/0.209 = 0.77 by a normal calculation.
  - The Board's simulation (below); splitting (Cox 1975); PoSI, polyhedral inference, data fission (Part 56).
- **Subset selection.**
  - Stepwise's sins; leaps and bounds; mixed-integer optimization.
  - The race: n = 100, p = 10, 5 true, correlation 0.35^{|i−j|}, tuned on a validation set. Relative risk:

    | SNR | 0.05 | 0.25 | 1 | 6 |
    |---|---|---|---|---|
    | best subset | 1.337 | 0.496 | 0.085 | 0.0107 |
    | forward stepwise | 1.360 | 0.467 | 0.087 | 0.0107 |
    | lasso | 1.007 | 0.404 | 0.092 | 0.0182 |

  - Prostate test error on the 30 held-out men:

    | Method | Predictors | Test error |
    |---|---|---|
    | null | 0 | 1.057 |
    | full least squares | 8 | 0.521 |
    | AIC = CV best subset | 7 | 0.517 |
    | BIC = CV one-SE | 2 | 0.492 |
    | lasso (10-fold CV) | 7 | 0.504 |
    | ridge (10-fold CV) | 8 | 0.506 |

  - Bootstrap stability, 400 resamples:
    - AIC produced 66 distinct models and its original pick 15% of the time;
    - BIC produced 62 and its pair 18%;
    - lcavol was kept every time.
- **Calibrated forecasts.**
  - The PIT; four forecasters of a drifting level, 2,000 steps:

    | Forecaster | Log score | CRPS | 90% interval covers | PIT shape |
    |---|---|---|---|---|
    | calibrated | 1.423 | 0.569 | 90.1% | flat |
    | overconfident (SD 0.5) | 2.241 | 0.619 | 58.0% | U |
    | underconfident (SD 2) | 1.738 | 0.658 | 99.95% | hump |
    | biased (+0.7) | 1.687 | 0.715 | 80.6% | sloped |

  - Prostate leave-one-out PIT (the t CDF of the externally studentized residual). Mean LOO log density and KS p:
    - intercept only: −1.63 (KS p 0.96);
    - lcavol + lweight: −1.18 (0.999);
    - all eight: −1.17 (0.58).

    All three are calibrated; sharpness separates them.
  - Proper scoring rules and the CRPS (Matheson & Winkler 1976; Gneiting & Raftery 2007); sharpness subject to
    calibration.

Data:
- Stamey et al.'s prostate data (1989, via *The Elements of Statistical Learning*) and the eight schools are the
  Museum's;
- the doctor visits are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.select`** ([`explainer/stats/kit/select.py`](../../../explainer/stats/kit/select.py)), checked in
  `tests/test_stats_kit_select.py`:
  - **Criteria:** the Gaussian log likelihood from an RSS, AIC, AICc, BIC, Cp, Takeuchi's penalty.
  - **Leave-one-out:** the hat matrix, PRESS, GCV, and Efron's Monte Carlo degrees of freedom.
  - **Search:** Freedman's screening experiment, best subset by enumeration, forward stepwise.
  - **Bayesian:** PSIS-LOO (using `statkit.ppl`'s Pareto smoothing), WAIC, stacking weights, BMA weights.
  - **MDL:** the exact NML regret of a Bernoulli model.
- **The Museum** gains Stamey's prostate data (97 men, 8 predictors, the 67/30 split) as `museum.prostate()`.
- **The model-selection bench** (`CriterionBench` in `explainer/stats/viz.py`): misfit and penalty stacked per
  candidate, with the minimum ringed; `bars(penalty_per_k)` re-prices the same bench (AIC's 2 or BIC's log n).

The Coverage Board gains three rows. Ten independent candidate predictors, n = 100, β₁ = 0.05 (two others nonzero),
forward stepwise selection by AIC, 2,000 data sets:

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| naive CI after AIC selection | β₁ = 0.05, when x₁ is kept | 430 | 75.1% | broken |
| select on half, CI on the other half | β₁ = 0.05, when x₁ is kept | 441 | 95.7% | kept |
| full model, no selection | β₁ = 0.05 | 2,000 | 95.0% | kept |

## Build it

```bash
python -m videos.stats.stats28.compute         # once (several minutes)
python tools/build.py stats28 -q l             # fast 480p preview
python tools/build.py stats28                  # 1080p30 -> renders/stats28.mp4
python tools/qa_scene.py stats28 Singular
python tools/lecture_length.py stats28 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Freedman's paradox, 1983 | p 0.76 → 0.013; 94.7% of 1,000 repeats |
| 1 | Optimism | gap 0.067 = 2σ²d/n; lasso df ≈ 1 + nonzeros |
| 2 | Cp and AIC | TIC 9.47 vs k = 2; AIC picks 7 of 8 |
| 3 | BIC | picks 2; P(true degree) 0.99 vs AIC's 0.75; P(χ²₁ > 2) = 0.157 |
| 4 | Cross-validation theory | one-SE picks 2; corr(CV, true error) −0.06 |
| 5 | Bayesian LOO and WAIC | −30.56 / −31.21 / −36.97; k̂ up to 1.06 |
| 6 | Singular models | slopes 0.42 vs 0.98 (theory ½ vs 1) |
| 7 | Minimum description length | degree 5 at 40.9 bits; regret ≈ ½ log(nπ/2) |
| 8 | Averaging | BMA 0.99 on one model; stacking −2.06 vs truth −2.05 |
| 9 | Inference after selection | 77% by calculation; Board 75.1% vs 95.7% split |
| 10 | Subset selection | lasso wins at SNR 0.05, best subset at 6; 66 bootstrap models |
| 11 | Calibrated forecasts | coverage 58% / 90% / 99.95%; LOO log score −1.63 vs −1.18 |
| 12 | Outro | — |

## Sources

- **History.** D. Freedman, *The American Statistician* 37 (1983); T. Stamey et al., *J. Urology* 141 (1989).
- **Optimism and degrees of freedom.** B. Efron, *JASA* 81 (1986) and 99 (2004); C. Stein, *Ann. Stat.* 9 (1981);
  H. Zou, T. Hastie & R. Tibshirani, *Ann. Stat.* 35 (2007).
- **Information criteria.**
  - C. Mallows, *Technometrics* 15 (1973); H. Akaike, *2nd Int. Symp. Information Theory* (1973), *IEEE Trans. Aut.
    Control* 19 (1974); K. Takeuchi, *Suri-Kagaku* 153 (1976).
  - N. Sugiura, *Comm. Stat.* A7 (1978); C. Hurvich & C.-L. Tsai, *Biometrika* 76 (1989).
  - G. Schwarz, *Ann. Stat.* 6 (1978); R. Kass & L. Wasserman, *JASA* 90 (1995).
  - R. Shibata, *Biometrika* 63 (1976) and 68 (1981); Y. Yang, *Biometrika* 92 (2005).
- **Cross-validation.** D. Allen, *Technometrics* 16 (1974); M. Stone, *JRSS B* 36 (1974); P. Craven & G. Wahba,
  *Numer. Math.* 31 (1979); L. Breiman & P. Spector, *Int. Stat. Rev.* 60 (1992); R. Kohavi, *IJCAI* (1995);
  S. Bates, T. Hastie & R. Tibshirani, *JASA* 119 (2024).
- **Bayesian.**
  - A. Vehtari, A. Gelman & J. Gabry, *Stat. Comput.* 27 (2017); S. Watanabe, *JMLR* 11 (2010) and 14 (2013), and
    *Algebraic Geometry and Statistical Learning Theory* (2009).
  - M. Aoyagi & S. Watanabe, *Neural Networks* 18 (2005); M. Drton & M. Plummer, *JRSS B* 79 (2017).
- **MDL.** J. Rissanen, *Automatica* 14 (1978) and *IEEE Trans. Inf. Theory* 42 (1996); Y. Shtarkov, *Probl. Inf.
  Transm.* 23 (1987); A. P. Dawid, *JRSS A* 147 (1984); P. Grünwald, *The Minimum Description Length Principle* (2007).
- **Averaging.**
  - J. Hoeting, D. Madigan, A. Raftery & C. Volinsky, *Stat. Sci.* 14 (1999); D. Madigan & A. Raftery, *JASA* 89
    (1994); D. Madigan & J. York, *Int. Stat. Rev.* 63 (1995); J. Scott & J. Berger, *Ann. Stat.* 38 (2010).
  - J. Bernardo & A. Smith, *Bayesian Theory* (1994); D. Wolpert, *Neural Networks* 5 (1992); L. Breiman, *Machine
    Learning* 24 (1996); Y. Yao, A. Vehtari, D. Simpson & A. Gelman, *Bayesian Analysis* 13 (2018).
- **After selection.** D. Cox, *Biometrika* 62 (1975); Y. Benjamini & D. Yekutieli, *JASA* 100 (2005); R. Berk,
  L. Brown, A. Buja, K. Zhang & L. Zhao, *Ann. Stat.* 41 (2013); J. Lee, D. Sun, Y. Sun & J. Taylor, *Ann. Stat.* 44
  (2016); W. Fithian, D. Sun & J. Taylor (2014); J. Leiner, B. Duan, L. Wasserman & A. Ramdas, *JASA* (2023).
- **Subsets.** G. Furnival & R. Wilson, *Technometrics* 16 (1974); B. Natarajan, *SIAM J. Comput.* 24 (1995);
  D. Bertsimas, A. King & R. Mazumder, *Ann. Stat.* 44 (2016); T. Hastie, R. Tibshirani & R. Tibshirani, *Stat. Sci.*
  35 (2020); N. Meinshausen & P. Bühlmann, *JRSS B* 72 (2010); F. Harrell, *Regression Modeling Strategies* (2015).
- **Forecasts.** F. Diebold, T. Gunther & A. Tay, *Int. Econ. Rev.* 39 (1998); J. Matheson & R. Winkler, *Mgmt. Sci.*
  22 (1976); T. Gneiting & A. Raftery, *JASA* 102 (2007); T. Gneiting, F. Balabdaoui & A. Raftery, *JRSS B* 69 (2007);
  G. Brier, *Monthly Weather Review* 78 (1950).
- **Books.**
  - K. Burnham & D. Anderson, *Model Selection and Multimodel Inference* (2nd ed., 2002).
  - T. Hastie, R. Tibshirani & J. Friedman, *The Elements of Statistical Learning* (2nd ed., 2009), chapters 3 and 7.
  - G. Claeskens & N. Hjort, *Model Selection and Model Averaging* (2008).

## Problems and solutions

**1. The optimism of a linear smoother.**

*Solution.* Let μ = E y, and let y⁰ be an independent copy. Then E(y⁰ᵢ − ŷᵢ)² = σ² + E(ŷᵢ − μᵢ)². Also
E(yᵢ − ŷᵢ)² = σ² + E(ŷᵢ − μᵢ)² − 2Cov(yᵢ, ŷᵢ), expanding (yᵢ − μᵢ) − (ŷᵢ − μᵢ). Averaging, the optimism is
(2/n)Σ Cov(yᵢ, ŷᵢ). With ŷ = Sy, Cov(ŷ, y) = S Var(y) = σ²S, and the diagonal sums to σ² tr S. So the optimism is
2σ² tr(S)/n, and 2σ²d/n for least squares with d columns (tr H = d).

**2. The leave-one-out shortcut.**

*Solution.* Write A = XᵀX and β̂₋ᵢ = (A − xᵢxᵢᵀ)⁻¹(Xᵀy − xᵢyᵢ). Sherman–Morrison gives
(A − xxᵀ)⁻¹ = A⁻¹ + A⁻¹xxᵀA⁻¹/(1 − h), with h = xᵀA⁻¹x = hᵢᵢ. Multiplying out,
xᵢᵀβ̂₋ᵢ = (ŷᵢ − hᵢᵢyᵢ)/(1 − hᵢᵢ). Then yᵢ − xᵢᵀβ̂₋ᵢ = (yᵢ − hᵢᵢyᵢ − ŷᵢ + hᵢᵢyᵢ)/(1 − hᵢᵢ) = (yᵢ − ŷᵢ)/(1 − hᵢᵢ).

**3. BIC from Laplace's method.**

*Solution.* Expand ℓ(θ) = ℓ(θ̂) − ½(θ − θ̂)ᵀJₙ(θ − θ̂) + …, where Jₙ = −∇²ℓ(θ̂) = n Ĵ₁ and Ĵ₁ → I₁. Integrating
against a prior continuous and positive at θ̂ gives
p(y | M) = e^{ℓ(θ̂)} p(θ̂)(2π)^{k/2}|nĴ₁|^{−1/2}(1 + O_p(n^{−1/2})). Taking logs,
log p(y | M) = ℓ(θ̂) − (k/2) log n + [log p(θ̂) + (k/2) log 2π − ½ log|Ĵ₁|] + o_p(1). The bracket is O_p(1). Multiply by
−2 and drop it: BIC.

**4. AIC's penalty for a normal mean, exactly.**

*Solution.* With σ known, ℓ(μ) = c − Σ(yᵢ − μ)²/(2σ²) and μ̂ = ȳ. E Σ(yᵢ − ȳ)² = (n − 1)σ², so
E ℓ(μ̂) = c − (n − 1)/2. For new data y′ (n independent copies), E Σ(y′ᵢ − ȳ)² = nσ²(1 + 1/n) = (n + 1)σ², so
E ℓ_new(μ̂) = c − (n + 1)/2. The difference is exactly 1 = k: AIC's penalty is exact here.

**5. AIC overfits by one parameter 15.7% of the time.**

*Solution.* AIC prefers M_{k+1} to M_k iff −2ℓ_{k+1} + 2(k + 1) < −2ℓ_k + 2k, that is, iff 2(ℓ_{k+1} − ℓ_k) > 2. Under
M_k (regular, nested), Wilks's theorem gives 2(ℓ_{k+1} − ℓ_k) → χ²₁, so the probability tends to P(χ²₁ > 2) =
2(1 − Φ(√2)) = 0.157. BIC's threshold log n → ∞, so its probability → 0.

**6. The log score is strictly proper.**

*Solution.* E_g[−log f(Y)] − E_g[−log g(Y)] = E_g log(g/f) = KL(g ‖ f). By Jensen, KL ≥ 0, with equality only if f = g
almost everywhere. So reporting the true g uniquely minimizes the expected log score.

## Glossary

- **Optimism; in-sample error; covariance penalty**: the expected amount by which training error understates error
  on new responses at the same x; Efron's (2/n)Σ Cov(ŷᵢ, yᵢ).
- **Degrees of freedom (effective)**: Σ Cov(ŷᵢ, yᵢ)/σ²; tr S for a linear smoother; the expected divergence by Stein's
  lemma.
- **Cp; AIC; AICc; TIC**:
  - Mallows's training error plus 2dσ̂²/n;
  - −2ℓ + 2k, an estimate of expected KL to the truth;
  - its small-sample correction;
  - Takeuchi's misspecification-robust penalty tr(JK⁻¹).
- **BIC; unit-information prior; consistency; efficiency**:
  - −2ℓ + k log n, from the Laplace approximation to the evidence;
  - the prior under which it is accurate;
  - choosing the true model with probability → 1;
  - attaining the best achievable prediction risk.
- **PRESS; GCV; K-fold CV; one-SE rule**:
  - leave-one-out squared error by leverages;
  - its average-leverage version;
  - cross-validation with K folds;
  - the smallest model within one SE of the best.
- **Err versus Err_XY**: the expected error of a procedure versus the error of the fitted model in hand.
- **elpd; PSIS-LOO; Pareto k̂; WAIC; p_loo, p_WAIC**: expected log predictive density; its Pareto-smoothed
  leave-one-out estimate and diagnostic; Watanabe's criterion; effective numbers of parameters.
- **Singular model; real log canonical threshold (RLCT); free energy; WBIC; sBIC**:
  - a model whose information matrix is singular at the truth;
  - the λ replacing d/2;
  - minus the log evidence;
  - Watanabe's tempered-posterior evidence;
  - Drton and Plummer's singular BIC.
- **MDL; Kraft's inequality; two-part code; NML; regret; prequential**:
  - choose the shortest description;
  - codes are distributions;
  - model then data;
  - Shtarkov's normalized maximum likelihood;
  - its minimax excess code length;
  - sequential predictive codes.
- **BMA; Occam's window; MC³; M-closed and M-open; stacking; pseudo-BMA; Akaike weights**: averaging by posterior model
  probabilities and its computation; whether the truth is a candidate; weights chosen for predictive performance;
  exp(elpd) and exp(−AIC/2) weights.
- **Selective inference; winner's curse; data splitting; PoSI; polyhedral lemma; data fission**: valid inference
  after data-driven selection, and the methods that achieve it.
- **Best subset; leaps and bounds; mixed-integer optimization; forward stepwise; relaxed lasso; stability
  selection**: subset search and its relatives.
- **PIT; calibration; sharpness; proper scoring rule; log score; CRPS**:
  - F(y) at the outcome, uniform if F is right;
  - forecasts agree with frequencies;
  - concentration of the forecasts;
  - honesty minimizes expected penalty;
  - −log f(y);
  - E|X − y| − ½E|X − X′|.

## Where it comes back

| Idea | Returns in |
|---|---|
| GCV and degrees of freedom for smoothers | 29 |
| the lasso's df; selection in high dimensions | 32 |
| FDR and selected effects | 33 |
| conformal prediction | 34 |
| cross-fitting nuisance models | 36 |
| forecast evaluation | 38 |
| oracle inequalities, minimax rates | 50 |
| selective inference in depth | 56 |
| the Coverage Board | every part; 65 |

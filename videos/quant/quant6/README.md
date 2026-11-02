# Quant, Built — Part 6: Financial Econometrics

Part 6 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act II, the Mathematical Toolkit. It is about learning from the one history we
have without fooling ourselves, at the depth of a graduate course: least squares and its sandwich, HAC and clustered
errors (with fixed-b and EWC), Fama–MacBeth and the two-pass test, predictive regressions in and out of sample,
maximum likelihood and GMM, event studies, bootstraps for dependent data, Bayesian shrinkage, multiple testing,
causal designs and double machine learning, and the signal-to-noise problem.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`econ`](../../../explainer/quant/house/econ.py) module, tested in `tests/test_quant_house.py`) from public data:
Robert Shiller's monthly market data, Kenneth French's factors, 49 industries, book-to-market deciles and daily size
deciles, FRED's consumption and prices, and the Federal Reserve's FOMC meeting pages
([`fomc_dates.py`](fomc_dates.py)). Simulations are seeded and labeled on screen. All results are statements under
the real-world measure P.

*An education in methods, not investment advice.*

## Chapters (about 58 minutes, 20 entries)

* **One regression, five verdicts** (`s01_hook`). Does an industry's past year (months t−12 to t−2) predict its next
  month? French's 49 industries, 1928–2020, 51,858 industry-months: pooled OLS t = 1.86; clustered by industry 1.21;
  by month 0.27; two-way 0.27; Fama–MacBeth 5.08 with a slope eight times larger (0.0170 vs 0.0022). A sixth bar,
  pooled OLS with month effects (t = 3.56), waits for chapter 4. Then the era (Cowles 1933 → Menkveld et al. 2024),
  the objectives and the House.
* **1. Least squares, seen as geometry** (`s02_ols`). OLS as a projection in 3D; normal equations → the sandwich
  (X'X)⁻¹X'ΩX(X'X)⁻¹. Frisch–Waugh–Lovell on tobacco: alone, the SMB slope is +0.16; residual on residual (market
  projected out) it is −0.2095, equal to the multiple-regression coefficient to 2×10⁻¹⁶. White's se on that slope:
  0.055 against iid 0.047. The Ω grid lit as iid, White, band (ch 2) and blocks (ch 3).
* **2. Newey–West: counting dependent data** (`s03_hac`). Five-year real returns on the log dividend yield
  (1,739 overlapping windows): the scores' autocorrelations, Bartlett's window sliding open, t falling from 15.0
  (naive) to 2.8 at L = 120. Derivation of the long-run variance (spectrum at zero; overlap inflates by h).
  **Lab:** `econ._hac_meat` + `ols` → naive 15.0, NW 2.8, Hansen–Hodrick 2.5, Hodrick (1992) 1B 2.3. Size in 3,000
  null worlds per cell (T = 600, h = 12, ρ = 0.95): naive 53%, NW(L = 6) 19%, NW(L = h − 1) 14%, wide NW with
  fixed-b critical value 10%, EWC (ν = 28) 8%; with ρ = 0 every test is near 5%. Fixed-b critical values simulated:
  2.02, 2.10, 2.24, 2.51, 2.87, 3.45 at b = 0.02, 0.05, 0.1, 0.2, 0.3, 0.5 (Kiefer–Vogelsang's cubic gives
  2.02, 2.11, 2.26, 2.57, 2.87, 3.48).
* **3. Clustering: the shocks that are shared** (`s04_cluster`). Ω masks for firm and time effects; the cluster
  meat, Moulton's factor, two-way inclusion–exclusion. Petersen's design, 500 firms × 10 years, 1,000 panels per
  design (se / true sd): firm effect — OLS 0.55, FM 0.46, by firm 0.99; time effect — OLS 0.09, by month 0.79, FM
  0.94; both — two-way 0.80. Petersen's survey: 42% of panel papers did not adjust.
* **4. Fama–MacBeth, and five verdicts resolved** (`s05_famamacbeth`). 1,116 monthly cross-sections stacking into a
  histogram of slopes. **Lab:** `econ.fama_macbeth` → 0.0170, t 5.08 (NW 5.16); 61% of months positive.
  **The resolution (corrects the earlier narration):** pooled OLS with month effects (within) = 0.0103, t 3.56
  clustered by month, exactly the dispersion-weighted Fama–MacBeth average 0.0103; the between-month slope (market
  on its own past year) = −0.0046, t −0.29; pooled = 0.45 × within + 0.55 × between = 0.0022. Dispersion weighting
  explains only 0.0170 → 0.0103; the rest is market timing mixed into a cross-sectional question. Two-pass CAPM
  test, 57 portfolios (49 industries + 10 B/M deciles), 1963–2020: λ_m = −0.002% a month (t −0.01; Shanken −0.01)
  against a market premium of 0.57%; intercept 0.65% (t 3.2); GRS F = 1.62, p = 0.004.
* **5. Predictive regressions: Stambaugh's bias** (`s06_stambaugh`). 4,000 simulated samples as a tilted cloud of
  (ρ̂ − ρ, β̂ − β), slope φ = −0.65; the centre's bias falls from +0.055 at T = 50 to +0.017 at 150 (formula: +0.049,
  +0.016). Derivation; annual data: β = 0.034 (t 1.1), bias +0.018, corrected 0.016; Amihud–Hurvich 0.016
  (t 0.49); IVX annual p = 0.16; the House's simplified IVX on monthly data p = 0.018 (since 1952, 0.015).
* **6. Out of sample** (`s07_oos`). Expanding-window forecasts from 1927 on Shiller monthly; the real-time slope with
  its band and the cumulative ΔSSE (−0.0034 by 1990, −0.0081 by 2000, −0.0073 at the end). R²_OS: dividend yield
  −0.32% (Campbell–Thompson −0.12%), earnings yield −0.16% (+0.03%), CAPE −0.03% (−0.00%), 10-year yield −0.23%
  (+0.07%), inflation +0.35% (+0.38%; the only positive one, of five tried). Campbell–Thompson's gain R²/S²: S² =
  1.9% monthly.
* **7. Maximum likelihood** (`s08_mle`). Student t on 24,896 daily market returns (1926–2020): Newton from ν = 27
  reaches ν̂ = 2.45, σ̂ = 0.575%, in 6 steps (the iterates are replayed on the 3D likelihood hill). se(ν̂): inverse
  Hessian 0.047; OPG sandwich 0.044; sandwich with the scores' long-run variance 0.170 (3.6 times the naive one).
* **8. GMM** (`s09_gmm`). One mean, two noisy measures (sd 1 and 2, n = 50): the moment line, W = I gives 1.025,
  W = Ŝ⁻¹ gives 0.980 (se 0.112), J = 0.23 (p = 0.63). Derivation of the sandwich and efficient weight; OLS, IV and
  ML as GMM.
* **9. The Euler equation, estimated and rejected** (`s10_euler`). **Lab:** two-step `econ.gmm` → β = 1.002
  (0.009), γ = 1.1 (1.5), J = 20.0 on 4 df, p = 0.0005. The J(β, γ) surface in 3D: a steep valley in β, a ridge in γ
  (weak identification). 400 economies where the model is true (β = 1, γ = 2): γ̂ from −34 to 36 (5–95%); J above
  its 5% critical value in 0.8% of them, never above 11.3. Equity premium 2.1% a quarter, consumption sd 1.1%,
  correlation 0.06: γ ≈ 421 (Mehra–Prescott).
* **10. Event studies** (`s11_event`). FFJR 1969; MacKinlay's machinery. Turn of the month: 74% of returns in
  1926–1986, 45% after (t 2.6). FOMC decision days (215 scheduled, 1994–2020): 28 bp against 3 bp, t = 3.08; 3% of
  days, 24% of the excess return; 1994–2011: 33 bp (Lucca–Moench report about 33 bp close to close); 2011–2020: 12 bp
  (t 0.95). Placebo p = 0.0014 (10,000 sets). Same-date clustering, simulated: naive se 0.20% against a true 1.54%.
* **11. The bootstrap for dependent data** (`s12_bootstrap`). Ribbon cut into blocks. **Lab:**
  `econ.stationary_bootstrap` → se 0.122 (iid bootstrap 0.104, Lo 0.103). Coverage of nominal 95% intervals in 1,000
  AR(1)+GARCH markets: iid 88.9%, moving block 90.2%, stationary 90.6%.
* **12. Shrinkage and Bayes** (`s13_bayes`). 40 industry means, first half vs second (rank correlation 0.19).
  Conjugate algebra, empirical Bayes, James–Stein; Gibbs on the hierarchy (4 chains × 5,000): posterior median τ =
  1.0% a year, 91% of the spread removed; error 8.0 (raw) → 3.9 (Gibbs), 3.8 (EB).
* **13. Many tests** (`s14_many`). 49 alphas: 5 at p < 0.05, 0 after Bonferroni, Holm or BH. Proofs. Planted world
  (1,000 strategies, 50 with SR 0.5 over 20 years, 200 seeds): raw 30 true / 48 false (FDR 61%); Holm 1.9 true, FWER
  6.5%; BH 4.3 true, FDR 4.7%. **Lab:** `econ.benjamini_hochberg`.
* **14. Causal designs** (`s15_designs`). IV (OLS 1.0 vs truth 0.5; strong F ≈ 60: 2SLS 0.50; weak F ≈ 2: middle half
  0.13 to 0.99); DiD 0.361 vs 0.35; staggered adoption: TWFE weights negative on the first cohort's late periods; TWFE
  0.15 vs truth 0.90, Callaway–Sant'Anna 0.91; RD at a Russell-style cutoff (planted jump 2): RMSE smallest at ±150
  ranks. The Regulation SHO pilot as a real design.
* **15. Double machine learning** (`s16_dml`). Residual clouds: raw slope 1.24, residual on residual 0.33 (truth 0.3).
  Orthogonality and cross-fitting derived. **Lab:** `econ.dml_plr` → 0.300 ± 0.018 over 60 samples, OLS 1.15. Penalty
  sweep, 5 seeds: at λ = 1, DML 0.300, plug-in 0.311; at λ = 10, 0.322 vs 0.390; both fail at extreme λ.
* **16. How many years until you know?** (`s17_snr`). t = SR√T; Lo/Mertens; tobacco's (α, β) ellipse refitted
  quarterly from 1961: after 60 years α = 6.2% ± 4.7% a year, β = 0.69 ± 0.09. 16 years for SR 0.5, 4 for SR 1; 13%
  chance a SR-0.5 strategy has lost after five years.
* **17. How research desks avoid fooling themselves** (`s18_industry`). Crisis file: F-Squared (SEC 2014) and a
  one-week look-ahead toy (honest 6.6% a year, one week early 35.4%, 2001–2008). The SEC Marketing Rule (nine
  advisers, 2023). Man Group, AQR, Research Affiliates; Menkveld et al. and Pérignon et al. The House's defences.
* **18. The frontier, 2023–2026** (`s19_frontier`). Eight cards tied to their chapters; Kelly–Malamud–Zhou vs Nagel
  (schematic).
* **The statistics module; recap, desk questions, problems** (`s20_outro`). Rule 7 and the trial counter.

## Build it

```bash
python -m videos.quant.quant6.compute                    # every number, cached in .cache/quant6/ (about 20 CPU-minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant6 FamaMacBeth   # one chapter, silent, with a contact sheet
python tools/make.py quant6 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

Compute items: `overlap`, `stambaugh`, `gmm`, `event`, `panel`, `bootstrap`, `shrinkage`, `multiple`, `ellipse`,
`dml`, `snr`, `envelope` (kept), and `ols_fwl`, `hac`, `har_size` (12 cells × 3,000 worlds), `petersen` (5 × 1,000),
`panel_fe`, `twopass`, `stambaugh_cloud`, `ivx`, `oos`, `mle`, `gmm_toy`, `gmm_surface`, `gmm_mc` (400 economies),
`fomc`, `lookahead`, `boot_demo`, `boot_coverage` (1,000 markets × 3 bootstraps × 400), `gibbs`, `fdr_sim`,
`designs`, `dml_lambda`, `dml_demo`, `ellipse_path`. Long items resume from `.cache/quant6/*.partial.json`.

## Textbook audit

| Textbook section | Where |
|---|---|
| CLM 1.4 / App. A: linear IV, GMM, HAC errors, GMM and ML | ch 1, 2, 7, 8 |
| CLM 2: predictability (random walk tests, variance ratios, long horizons) | variance ratios Part 1; long horizons ch 2, 5, 6 |
| CLM 3: market microstructure | Part 35 |
| CLM 4: event studies (market model, AR/CAR, variance, clustering, nonparametric tests) | ch 10 (nonparametric tests: placebo) |
| CLM 5: CAPM tests (GRS, two-pass) | ch 4 (two-pass, Shanken, GRS); Part 24 |
| CLM 6–7: multifactor models, present-value relations | Parts 23–24 |
| CLM 8: Euler equations, HJ bounds, equity premium | ch 9; HJ bounds Part 23 |
| CLM 9–12 | Parts 10, 18, 19, 7, 27 |
| Cochrane ch 10–11: GMM in discount-factor models; general formulas | ch 8, 9 |
| Cochrane ch 12: regression-based tests (time series, cross-section, Fama–MacBeth, Shanken) | ch 4; Part 24 |
| Cochrane ch 13: GMM for linear factor models | ch 8 (one beat); Part 23 |
| Cochrane ch 14: maximum likelihood | ch 7 |
| Cochrane ch 15–16: comparing methods; which method? | ch 4, 8 |
| Cochrane ch 20: expected returns in time series and cross section | ch 5, 6 |
| Cochrane ch 21: equity premium puzzle | ch 9; Part 23 |
| Hayashi ch 1: finite-sample OLS (projection, FWL) | ch 1 |
| Hayashi ch 2: large-sample theory, robust se | ch 1 |
| Hayashi ch 3–4: single- and multiple-equation GMM, IV/2SLS | ch 8, 14 |
| Hayashi ch 5: panel data | ch 3, 4 |
| Hayashi ch 6: serial correlation, long-run variance | ch 2 |
| Hayashi ch 7–8: extremum estimators, ML | ch 7 |
| Hayashi ch 9–10: unit roots, cointegration | Part 7 |
| Greene ch 2–5: regression, inference, robust covariance | ch 1 |
| Greene ch 6: functional form, difference in differences | ch 14 |
| Greene ch 8: endogeneity and IV | ch 14 |
| Greene ch 11: panel data | ch 3, 4 |
| Greene ch 13: GMM | ch 8 |
| Greene ch 14: MLE | ch 7 |
| Greene ch 15: simulation and bootstrap | ch 11 |
| Greene ch 16: Bayesian estimation | ch 12 |
| Greene ch 20: serial correlation | ch 2 |
| Bali–Engle–Murray ch 1–5: summary statistics, correlation, persistence, portfolio analysis | ch 2; Part 24 |
| Bali–Engle–Murray ch 6: Fama–MacBeth regressions | ch 4 |
| Tsay ch 2 (regression with time-series errors); ch 12 (MCMC) | ch 2; ch 12 |

Chapter numbers were checked against the books' tables of contents (Cochrane's revised edition, Greene's 8th
edition, Bali–Engle–Murray's Part I, and course syllabi for Hayashi).

## Reading guide (papers on screen, one line each)

* Cowles (1933): forecasters mostly could not forecast — econometrics as the testing of claims.
* Fama, Fisher, Jensen and Roll (1969): 940 splits in event time; the first event study.
* Fama and MacBeth (1973): cross-sections each month, averaged; the two-pass test.
* Hansen and Hodrick (1980); Newey and West (1987); Hodrick (1992): standard errors for overlapping, correlated data.
* White (1980): the heteroskedasticity-robust sandwich.
* Hansen (1982); Hansen and Singleton (1982): GMM and the Euler equation.
* Mehra and Prescott (1985): the equity premium puzzle.
* Ariel (1987): the turn-of-the-month effect.
* Künsch (1989); Politis and Romano (1994): block and stationary bootstraps.
* Shanken (1992): errors-in-variables in the second pass.
* Benjamini and Hochberg (1995); Holm (1979): FDR and step-down FWER control.
* MacKinlay (1997): the event-study machinery.
* Stambaugh (1999); Amihud and Hurvich (2004); Kostakis, Magdalinos and Stamatogiannis (2015): predictive-regression
  bias, its correction, and IVX.
* Stock and Wright (2000): weak identification in GMM.
* Lo (2002); Mertens (2002): the Sharpe ratio's standard error.
* Kiefer and Vogelsang (2005); Lazarus, Lewis, Stock and Watson (2018); Lazarus, Lewis and Stock (2021): fixed-b, EWC,
  and the size–power frontier.
* Welch and Goyal (2008); Campbell and Thompson (2008); Goyal, Welch and Zafirov (2024): out-of-sample prediction.
* Petersen (2009); Cameron, Gelbach and Miller (2011): clustered standard errors in finance panels.
* Lucca and Moench (2015): the pre-FOMC announcement drift (49 bp in the 24 hours before; about 33 bp close to close,
  per the NY Fed staff report).
* Chang, Hong and Liskovich (2015): regression discontinuity at the Russell cutoff.
* Harvey, Liu and Zhu (2016): the factor zoo and t > 3.
* Chernozhukov et al. (2018): double/debiased ML.
* Goodman-Bacon (2021); Callaway and Sant'Anna (2021); Baker, Larcker and Wang (2022); Roth et al. (2023): staggered DiD.
* Jensen, Kelly and Pedersen (2023): replication of 153 factors (82.4% significant CAPM alphas, 75.6% after a
  Benjamini–Yekutieli correction, against Hou–Xue–Zhang's 35%).
* Kelly, Malamud and Zhou (2024) and Nagel (2025): complexity in return prediction, and the momentum reading.
* Andrews, Kitagawa and McCloskey (2024): inference on winners.
* Menkveld et al. (2024): 164 teams, non-standard errors. Pérignon et al. (2024): 52% exact reproducibility.
* Maasoumi et al. (2024): automatic debiased ML for factors. Chernozhukov et al. (2024): open causal-ML textbook.
* Glasserman and Lin (2023, arXiv 2309.17322): look-ahead and distraction in LLM sentiment.
* Industry: SEC 2014-289 (F-Squared), SEC 2023-173 (Marketing Rule), SEC 2004-164 (Reg SHO pilot), Harvey–Liu
  "Backtesting" (Man Group), Arnott–Harvey–Markowitz (2019), Ilmanen et al. (2021).

## Desk questions, with solutions

1. **Sharpe 1 over 4 years.** For iid normal returns, se(SR) ≈ √((1 + SR²/2)/T) = √(1.5/4) ≈ 0.61 in annual units.
   The 95% interval is about 1 ± 1.2: the data cannot tell this strategy from one with no edge.
2. **The best of 20 has p = 0.03.** If all 20 are worthless and independent, the chance that at least one has
   p ≤ 0.03 is 1 − 0.97²⁰ ≈ 46%. Bonferroni requires p < 0.05/20 = 0.0025. Correlated strategies reduce the effective
   number of tests, but the count of tries must be reported either way.
3. **Annual returns sampled monthly over 40 years.** 480 rows, about 40 independent observations: neighbours share 11
   of 12 months. Use Newey–West with fixed-b critical values or EWC; chapter 2's simulation shows even NW(L = h − 1)
   rejects a true null 14% of the time with a persistent predictor.
4. **t = 2.5 on five-year returns and a persistent yield, with Newey–West.** Not on that alone. Chapter 2: such tests
   reject a true null 14–17% of the time at this persistence; chapter 5: the slope carries Stambaugh's bias (about
   half of the annual slope); chapter 6: the dividend yield's out-of-sample R² is negative (−0.32%).
5. **Pooled slope 0.002, Fama–MacBeth 0.017: which is wrong?** Neither. Fama–MacBeth averages within-month slopes
   equally (0.0170); weighting them by cross-sectional dispersion gives 0.0103, which is pooled OLS with month
   effects. Pooled OLS without month effects mixes this within slope (45% of the variation) with the between-month
   slope of the market on its own past (−0.0046), and lands at 0.0022.

## Problems, with solutions

1. **The cost of overlap.** With y_t = Σ_{j=1}^{h} ε_{t+j} and a predictor that barely changes, the residuals are
   close to y_t. Neighbouring y_t share h − k shocks at lag k, so their autocorrelation is (h − k)/h, and
   Σ_{|k|<h}(1 − |k|/h) = h. The naive variance is too small by h and the standard error by √h: √60 ≈ 7.7 for
   five-year returns sampled monthly (compare 15.0 against 2.8).
2. **Stambaugh's bias.** With r_{t+1} = a + βx_t + u and x_{t+1} = c + ρx_t + v, write u = φv + e, φ = σ_uv/σ_v², e
   independent of v. OLS gives β̂ − β = φ(ρ̂ − ρ) + Σx̃e/Σx̃², whose second term has mean zero, and Kendall's
   E[ρ̂ − ρ] ≈ −(1 + 3ρ)/T. So E[β̂ − β] ≈ −φ(1 + 3ρ)/T. Annual data: ρ = 0.91, T = 149, φ = −0.72: bias
   +0.72 × 3.72/149 = +0.018.
3. **The Sharpe ratio's standard error.** SR̂ = μ̂/σ̂; with iid normal returns Var(μ̂) = σ²/T, Var(σ̂) ≈ σ²/(2T),
   independent. The delta method gives Var(SR̂) ≈ (1 + SR²/2)/T. Fat tails add (κ − 3)SR²/4 and skewness −γ₃SR
   (Mertens 2002).
4. **Holm.** Reject while p₍ᵢ₎ ≤ α/(m − i + 1). With m₀ true nulls, at the first false rejection at least m₀
   hypotheses remain, so its threshold is at most α/m₀; P(any false rejection) ≤ P(min over true nulls of p ≤ α/m₀) ≤
   α. Every threshold is at least α/m, so Holm rejects at least what Bonferroni rejects.
5. **James–Stein.** For x ~ N(μ, I_k), Stein's lemma E[(x − μ)·g(x)] = E[∇·g] gives the risk of
   (1 − (k − 2)/‖x‖²)x as k − (k − 2)²E[1/‖x‖²] < k. Shrinking toward the grand mean spends a degree of freedom: the
   factor becomes (k − 3)/‖x − x̄‖², which needs k ≥ 4.
6. **Within and between.** Write x̃_it = x_it − x̄_t. The month-fixed-effects slope is Σ_tΣ_i x̃_it r̃_it / Σ_tΣ_i x̃_it².
   Each month's cross-sectional slope is γ̂_t = Σ_i x̃_it r̃_it / Σ_i x̃_it², so the numerator is Σ_t γ̂_t Σ_i x̃_it²,
   and the FE slope is Σ_t w_t γ̂_t with w_t = Σ_i x̃_it² / Σ_sΣ_i x̃_is². For pooled OLS, split x_it − x̄ =
   x̃_it + (x̄_t − x̄); the cross term sums to zero within each month, so Σ(x − x̄)² = SS_W + SS_B and the pooled
   numerator is SS_W·β_FE + SS_B·β_B: β_pooled = (SS_W β_FE + SS_B β_B)/(SS_W + SS_B). On the industries,
   0.45 × 0.0103 + 0.55 × (−0.0046) = 0.0022.
7. **The iid bootstrap forgets dependence.** Each x*_i is drawn uniformly from the sample, so Var*(x*_i) = Γ̂₀ and the
   draws are independent: Var*(√n x̄*) = Γ̂₀, whatever the autocovariances. With moving blocks of length ℓ, a block
   mean contains ℓ − k pairs at lag k, so Var*(√n x̄*) ≈ Γ̂₀ + 2Σ_{k<ℓ}(1 − k/ℓ)Γ̂_k: a Bartlett-weighted long-run
   variance with bandwidth ℓ.

## Data and reproducibility

* Robert Shiller's `ie_data.xls`, monthly 1871–2020 (real total returns; dividend, earnings and CAPE yields; GS10;
  CPI).
* Kenneth French: monthly factors, `49_Industry_Portfolios`, `Portfolios_Formed_on_BE-ME` (deciles), the daily
  market and daily size deciles; value-weighted, through December 2020. Hold-outs from 2021 are sealed.
* FRED: real PCE per capita (A794RX0Q048SBEA, hold-out sealed) and CPIAUCSL.
* FOMC: scheduled meetings 1994–2020 transcribed from `federalreserve.gov/monetarypolicy/fomchistorical<YYYY>.htm`
  into [`fomc_dates.py`](fomc_dates.py) (215 decision days; SHA-256 of the list in the file and in
  `videos/quant/data/manifest.json`; `compute fomc` re-parses the cached pages and insists on the list). Spot-checked:
  1994-02-04, 2001-01-31, 2007-09-18, 2008-12-16, 2013-06-19, 2015-12-16, 2019-07-31, 2020-01-29.
* Registered with the trial counter: the industry-momentum panel (1), the turn-of-the-month event study (1), the 49
  industry alphas (49), the FOMC event study (1), five out-of-sample predictors (5), the look-ahead toy (1) and the
  two-pass test (1).
* Facts checked against primary sources for this expansion: the SEC releases (F-Squared; the 2023 Marketing Rule
  cases, settled without admitting or denying; the Reg SHO pilot), Lucca–Moench's staff report, Petersen's 42%,
  Campbell–Thompson's gain formula (R²/(1 − R²)·(1 + S²)/S²), the textbook chapter numbers, JKP's replication rates,
  Pérignon et al.'s 52%, Nagel's abstract, Glasserman–Lin's findings. Dropped: the Two Sigma Venn "Factor Lens" claim
  (its documentation could not be read from this environment); Glasserman–Lin's journal venue (cited as arXiv).

---

# 量化金融，从零搭建 — 第6部分：金融计量经济学

本部分讲如何从我们仅有的一段历史中学习而不自欺，深度相当于研究生课程：最小二乘及其三明治、HAC与聚类标准误（含固定b与等权余弦估计）、
法玛–麦克白与两步法检验、样本内外的预测回归、极大似然与广义矩估计、事件研究、相依数据的自助法、贝叶斯收缩、多重检验、因果设计与双重机器学习，
以及信噪比问题。所有数字都由本系列自己的代码根据公开数据算出；所有结论都在真实世界测度P之下。

*讲的是方法，不构成投资建议。*

## 各章（约58分钟，20段）

* **一个回归，五个结论。** 行业动量：混合OLS t = 1.86；按行业聚类1.21；按月0.27；双向0.27；法玛–麦克白5.08，斜率大八倍。灰色的第六根柱子：
  带月份效应的OLS，t = 3.56。
* **1. 几何视角下的最小二乘。** 投影、正规方程、三明治；FWL：烟草的SMB斜率单独为+0.16，剔除市场后为−0.2095，与多元回归一致到2×10⁻¹⁶。
* **2. 纽维–韦斯特。** 重叠五年期收益：朴素t 15.0，NW 2.8，HH 2.5，霍德里克1B 2.3。规模模拟（ρ = 0.95，h = 12）：朴素53%，NW(6) 19%，
  NW(h − 1) 14%，宽窗口固定b 10%，EWC 8%。固定b临界值由模拟得到。
* **3. 聚类。** 彼得森设计：公司效应下OLS 0.55、FM 0.46、按公司0.99；时间效应下OLS 0.09、按月0.79、FM 0.94。
* **4. 法玛–麦克白与和解。** FM 0.0170（t 5.08）；月内（月份固定效应）0.0103（t 3.56）= 按离散度加权的FM；月间−0.0046（t −0.29）；
  混合 = 0.45 × 月内 + 0.55 × 月间 = 0.0022。两步法CAPM检验：λ_m ≈ 0，截距0.65%（t 3.2），GRS p = 0.004。
* **5. 斯坦博偏差。** 倾斜点云；年度β = 0.034，偏差+0.018，校正后0.016；阿米胡德–赫维奇0.016（t 0.49）；IVX年度p = 0.16，月度p = 0.018。
* **6. 样本外。** 五个预测变量只有通胀的R²_OS为正（+0.35%）；股息率−0.32%。
* **7. 极大似然。** 日收益t分布：ν̂ = 2.45；ν的标准误：朴素0.047，OPG三明治0.044，考虑得分相依的三明治0.170。
* **8. 广义矩估计。** 两个测量的几何：W = I得1.025，有效权重得0.980，J = 0.23。
* **9. 欧拉方程。** β = 1.002，γ = 1.1（1.5），J = 20.0，p = 0.0005；400个模型成立的经济体中γ̂从−34到36，J最大11.3；γ ≈ 421。
* **10. 事件研究。** 月末月初：74% → 45%。FOMC决议日（215次）：28个基点对3个基点，t = 3.08；安慰剂p = 0.0014；2011年后12个基点（t 0.95）。
* **11. 自助法。** 平稳自助法se 0.122（独立同分布0.104）；覆盖率：88.9%、90.2%、90.6%。
* **12. 收缩与贝叶斯。** 吉布斯：τ后验中位数1.0%，误差8.0 → 3.9。
* **13. 多重检验。** 49个alpha：5个p < 0.05，校正后0个；模拟世界：BH找到4.3个真发现，FDR 4.7%。
* **14. 因果设计。** 弱工具与强工具；双重差分；交错采纳下TWFE 0.15对真值0.90，CS 0.91；断点的带宽权衡。
* **15. 双重机器学习。** 0.300 ± 0.018，OLS 1.15；惩罚扫描下代入法先漂移。
* **16. 要多少年。** 烟草α = 6.2% ± 4.7%；SR 0.5需要16年。
* **17. 行业。** F-Squared（美国证监会2014）；营销规则（2023）；英仕曼、AQR、锐联；非标准误与可复现性。
* **18. 前沿。** 八篇2023–2026年的论文，各连到相应章节。
* **统计模块、回顾、交易台问题与习题。**

## 教科书对照

见英文部分的表格：CLM第1.4节与附录A、第2、4、5、8章；Cochrane《资产定价》修订版第10–16、20–21章；Hayashi第1–8章；Greene第8版第2–6、8、11、
13–16、20章；Bali–Engle–Murray第1–6章；Tsay第2、12章。每一节都对应到本部分的某一章或系列中的另一部分。

## 交易台问题与解答

1. **四年夏普比率为1。** 独立正态收益下se(SR) ≈ √((1 + SR²/2)/T) = √(1.5/4) ≈ 0.61（年化）；95%区间约为1 ± 1.2。
2. **20个策略中最好的p = 0.03。** 若都无效且独立，至少一个p ≤ 0.03的概率为1 − 0.97²⁰ ≈ 46%；邦费罗尼要求p < 0.0025。
3. **40年按月采样的年度收益。** 480行，约40个独立观测；用带固定b临界值的纽维–韦斯特或EWC；即使NW(h − 1)在持续预测变量下也有14%的拒绝率。
4. **五年期收益对持续的股息率，NW下t = 2.5。** 不要只凭这一点交易：此类检验在真原假设下拒绝14–17%；斜率带有斯坦博偏差（约为年度斜率的一半）；
   股息率的样本外R²为负（−0.32%）。
5. **混合斜率0.002，法玛–麦克白0.017：哪个错了？** 都没错。FM对月内斜率等权平均（0.0170）；按离散度加权得0.0103，即带月份效应的OLS；
   不带月份效应的混合OLS把这个月内斜率（占变异的45%）与市场对自身过去的月间斜率（−0.0046）混在一起，得到0.0022。

## 习题与解答

1. **重叠的代价。** 相邻y_t在滞后k处共享h − k个冲击，自相关为(h − k)/h，加总为h；朴素方差小h倍，标准误小√h倍（√60 ≈ 7.7）。
2. **斯坦博偏差。** u = φv + e，φ = σ_uv/σ_v²；β̂ − β = φ(ρ̂ − ρ) + 均值为零的项；由肯德尔E[ρ̂ − ρ] ≈ −(1 + 3ρ)/T，
   得E[β̂ − β] ≈ −φ(1 + 3ρ)/T；年度数据φ = −0.72，ρ = 0.91，T = 149，偏差+0.018。
3. **夏普比率的标准误。** 由delta方法，Var(SR̂) ≈ (1 + SR²/2)/T；厚尾加(κ − 3)SR²/4，偏度加−γ₃SR。
4. **Holm方法。** 第一次错误拒绝时至少还剩m₀个假设，阈值至多α/m₀，由并集界FWER ≤ α；每个阈值不小于α/m，所以拒绝的不少于邦费罗尼。
5. **James–Stein。** 由斯坦引理，(1 − (k − 2)/‖x‖²)x的风险为k − (k − 2)²E[1/‖x‖²] < k；向总均值收缩需k ≥ 4。
6. **月内与月间。** 月份固定效应斜率 = Σ_t w_t γ̂_t，w_t为当月横截面平方和的份额；把x − x̄拆成月内与月间两部分，交叉项在每月内为零，
   所以混合斜率 = (SS_W β_FE + SS_B β_B)/(SS_W + SS_B)；行业数据：0.45 × 0.0103 + 0.55 × (−0.0046) = 0.0022。
7. **独立同分布自助法忘掉相依。** 每个x*_i从样本中均匀独立抽取，Var*(√n x̄*) = Γ̂₀；长度为ℓ的移动区块给出约Γ̂₀ + 2Σ_{k<ℓ}(1 − k/ℓ)Γ̂_k，
   即带宽为ℓ的巴特利特加权长期方差。

## 数据与可复现性

席勒月度数据；肯尼斯·弗伦奇的因子、49个行业、账面市值比十分位、日度市场与规模十分位（截至2020年12月，2021年起的留出数据已密封）；
FRED的人均实际消费与CPI；FOMC例行会议日期（1994–2020，转录自美联储网站，见`fomc_dates.py`，带SHA-256校验）。

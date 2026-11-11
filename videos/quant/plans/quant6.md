# Plan: Quant, Built, Part 6, *Financial Econometrics*, from 19 to about 58 minutes

Research and planning only; nothing in the repo was edited. Numbers marked **(planning run)** were computed in this session by scratch scripts on the cached data and the House's `econ` module. `compute.py` must recompute them, and the narration must branch on whatever it gets. Items marked **(unverified)** were not checked against a primary source. Items marked **(verify)** are chapter numbers or details recalled from the TOCs.

**On the length rules.** SYLLABUS §1 asks for 4–6-minute chapters. The owner's addendum ("Hands-on, as in *AI, Built*") asks for 16–20 chapters in 50–60 minutes, the rhythm of *AI, Built* (about 3 minutes a chapter). The two cannot both hold, because 16 × 4 = 64 minutes. This plan follows the addendum: **20 manifest entries, 58 minutes**. The core chapters run 3–3.5 minutes (about 420–490 words at the measured 140 words per minute) and the set pieces run 2.5–3. Each syllabus item still gets one or two chapters of its own. If the owner wants 4–6-minute chapters, merge pairs (3+4, 5+6, 8+9, 14+15) into 16 chapters of about 3.6 minutes.

## 1. Current state (`tools/lecture_length.py quant6`: 18.9 min, estimated)

| # | Chapter (scene) | Min | What it covers, and how deep |
|---|---|---|---|
| 0 | Hook: *One regression, five verdicts* (`s01_hook`) | 1.8 | Real experiment: industry momentum on French 49, 51,858 obs. t = 1.86 / 1.21 / 0.27 / 0.27 / FM 5.08. Bar chart; objectives; House. No history era. |
| 1 | Overlapping data and predictive regressions (`s02_overlap`) | 2.6 | Shiller 5-yr returns on log D/P: naive t 15.0, NW 2.8, HH 2.5; size sim 77/17/14%; Stambaugh histograms (50 vs 150 yr), bias formula quoted, not derived; annual β 0.034 → 0.016. No HAC derivation, no ACF visual, no out-of-sample. |
| 2 | GMM and the consumption Euler equation (`s03_gmm`) | 2.1 | 3-line ladder (moment condition, estimator, J). Euler results β 1.002, γ 1.1 (1.5), J 20.0 (4 df, p 0.0005); implied γ ≈ 421. No asymptotic variance derivation, no geometry, no MLE at all. |
| 3 | Event studies and panels (`s04_event`) | 2.2 | Turn of the month (1926–86 74% of return, t 7.4; 1987–2020 45%, t 2.6), AR bars ± 2 se. Panel explained in one paragraph (Petersen; FM weighting). No CAR variance, no market model, no FFJR, no two-pass. |
| 4 | Bootstrap and signal-to-noise (`s05_sharpe`) | 2.3 | Market SR 0.44: se 0.103 (Lo) / 0.104 (Mertens) / 0.119 (block) / 0.122 (stationary). Years-to-t=2 curve (16 yr at 0.5); P(looks negative); tobacco (α, β) ellipses at 5/20/60 yr. Bootstrap shown as a result, not run. |
| 5 | Many assets, many tests (`s06_many`) | 2.3 | Empirical-Bayes means (τ̂ = 0, MSE 8.0 → 3.8); 49 industry alphas: 5 raw, 0 after Bonferroni/Holm/BH; 1,000 noise strategies: 50 → 0. No proofs on screen (Holm and James–Stein only in the README). |
| 6 | Causal inference (`s07_causal`) | 2.0 | IV, DiD, RD as **schematics**; DML on a planted θ = 0.3: 0.300 ± 0.018 against OLS 1.15. No orthogonality derivation, no cross-fitting picture. |
| 7 | The statistics module (`s08_house`) | 0.7 | House rule 7; trial counter 63. |
| 8 | Recap, desk questions, problems (`s09_outro`) | 2.9 | Recap, 3 desk questions, 5 problems, payoff card, references. |

Verdict: the part covers the syllabus breadth at about a third of the depth. Each chapter carries one real computed number and one static chart. Missing: a history era, MLE, OLS geometry and the sandwich, HAC derivation and its visual, fixed-b/EWC, Fama–MacBeth as a running estimator, two-pass tests, out-of-sample predictability, event-study machinery, Bayesian computation, the multiple-testing proofs on screen, causal designs with numbers, any training replay or lab moment, industry, frontier and the crisis file. The firm-file standard is not met either.

**A correctness issue found while planning (fix it in the hook and the FM chapter).** The narration says the pooled slope (0.0022) and the FM slope (0.0170) differ "because pooled OLS weights each month by its cross-sectional dispersion". That accounts for only part of the gap. In the planning run:
- pooled OLS **with month fixed effects** gives 0.0103 (t = 3.56 clustered by month). This equals the dispersion-weighted average of the FM slopes, 0.0102;
- the remaining gap comes from the *time-series* component that pooled OLS without time effects mixes in. The slope of the average industry's return on the average industry's past return is −0.0037 (NW t = −0.29).

So "pooled" answers a mixed question: within-month (cross-sectional) plus between-month (market timing). Chapter 4 below turns this into the payoff of the hook.

## 2. Audit

### 2a. Syllabus items (SYLLABUS §6, Part 6)

| Item | Now | Plan |
|---|---|---|
| 1 Regression: OLS, overlap, HAC (NW 1987), clustered | thin (results only; no derivation) | ch 1 OLS geometry + sandwich; ch 2 HAC + fixed-b/EWC; clustering in ch 3 |
| 2 Predictive regressions, Stambaugh bias | thin (formula quoted) | ch 5 Stambaugh derived; ch 6 out of sample (Goyal–Welch, Campbell–Thompson) |
| 3 MLE and GMM; Euler equation | GMM thin; **MLE missing** | ch 7 MLE; ch 8 GMM geometry + asymptotics; ch 9 Euler (weak identification) |
| 4 Event studies (MacKinlay 1997) | thin (calendar effect only) | ch 10 full machinery + FOMC on real data |
| 5 Panels: FM vs pooled vs FE; Petersen | thin (one paragraph) | ch 3 clustering (Petersen sim); ch 4 FM, two-pass, Shanken, hook resolved |
| 6 Bootstrap for dependent data | thin (numbers) | ch 11 run on screen + coverage experiment |
| 7 Bayesian: priors as shrinkage; hierarchical | thin (EB only) | ch 12 conjugate algebra + Gibbs-sampled hierarchy |
| 8 Multiple testing preview | covered (results) | ch 13 with Holm/BH proofs and planted-truth sim |
| 9 Causal: IV, DiD, RD, DML | IV/DiD/RD schematic; DML result | ch 14 designs with simulated truths; ch 15 DML derived |
| 10 Signal-to-noise | covered | ch 16 live ellipse + years curve |

### 2b. Textbook sections → chapter

*CLM* (1997):

| Section | Where |
|---|---|
| 1.4 / App. A: linear IV, GMM, serially correlated and heteroskedastic errors, GMM and ML | ch 1, 2, 7, 8 |
| 2 Predictability (random-walk tests, variance ratios, long-horizon regressions) | variance ratios: Part 1 (`quant1/s05_testing`); long horizon: ch 2, 5, 6 |
| 3 Market microstructure | Part 35 |
| 4 Event-study analysis (market model, AR/CAR, the variance of the CAR, power, clustering, nonparametric tests) | ch 10 |
| 5 CAPM tests (GRS, two-pass) | two-pass in ch 4; GRS previewed in ch 4, full in Part 24 |
| 6 Multifactor models; 7 Present-value relations | Parts 23–24; Campbell–Shiller: Part 23 |
| 8 Intertemporal equilibrium: Euler equations, HJ bounds, equity premium | ch 9 (Euler, puzzle); HJ bounds: Part 23 |
| 9–12 Derivatives, fixed income, term structure, nonlinearities | Parts 10, 18, 19, 7, 27 |

*Cochrane, Asset Pricing* (rev. 2005), Part II (chapter numbers **(verify)**):

| Section | Where |
|---|---|
| ch 10–11 GMM in explicit discount-factor models; general formulas (S, d, J, efficient W, HAC S) | ch 8, 9 |
| ch 12 Regression-based tests of linear factor models (time series, cross-section, Fama–MacBeth, Shanken) | ch 4 (+ Part 24) |
| ch 13 GMM for linear factor models in discount-factor form | ch 8 (one beat) + Part 23 |
| ch 14 Maximum likelihood | ch 7 |
| ch 15–16 Comparing the methods; "which method?" | ch 4 (closing beat) and ch 8 (MLE and OLS as special GMM) |
| ch 20 Expected returns in time series and cross-section (long-horizon regressions) | ch 5, 6 |
| ch 21 Equity premium puzzle | ch 9 + Part 23 |

*Hayashi, Econometrics* (2000) (**(verify)** section numbers):

| Section | Where |
|---|---|
| ch 1 Finite-sample OLS (projection, FWL, Gauss–Markov) | ch 1 |
| ch 2 Large-sample theory (consistency, CLT for martingale differences, robust se) | ch 1 (sandwich) |
| ch 3–4 Single- and multiple-equation GMM (efficient W, J test, IV/2SLS as GMM) | ch 8, 14 (IV) |
| ch 5 Panel data (fixed effects, within transform) | ch 3, 4 |
| ch 6 Serial correlation (HAC / long-run variance, kernel and bandwidth) | ch 2 |
| ch 7–8 Extremum estimators, ML (information matrix, QMLE) | ch 7 |
| ch 9–10 Unit roots, cointegration | Part 7 |

*Greene, Econometric Analysis* (8th ed.; not in READING.md's spine. Proposed addition, chapter numbers **(verify)**):

| Section | Where |
|---|---|
| ch 2–5 linear regression, inference, robust covariance | ch 1 |
| ch 6 functional form, **difference in differences** | ch 14 |
| ch 8 endogeneity and IV | ch 14 |
| ch 11 panel data | ch 3, 4 |
| ch 13 GMM | ch 8 |
| ch 14 MLE | ch 7 |
| ch 15 simulation and bootstrap | ch 11 |
| ch 16 Bayesian estimation | ch 12 |
| ch 20 serial correlation | ch 2 |

*Bali–Engle–Murray* (2016), Part I methods **(verify)**: summary statistics, persistence, portfolio sorts, NW-adjusted t → ch 2 and Part 24; ch 6 Fama–MacBeth regressions → ch 4.

*Tsay* (3rd ed.): ch 2 regression with time-series errors → ch 2; ch 12 MCMC/Gibbs → ch 12; everything else → Part 7.

Off-spine but core (cite in the README reading guide): Efron–Tibshirani *An Introduction to the Bootstrap*: ch 11; Lahiri *Resampling Methods for Dependent Data*: ch 11; Angrist–Pischke *Mostly Harmless Econometrics*: ch 14; Chernozhukov–Hansen–Kallus–Spindler–Syrgkanis *Applied Causal Inference Powered by ML and AI* (arXiv 2403.02467): ch 15; Gelman et al. *Bayesian Data Analysis*: ch 12.

Topics checked and placed: OLS geometry → 1; HAC → 2; GMM → 8–9; Fama–MacBeth → 4; event studies → 10; predictive regressions → 5–6; bootstrap → 11; multiple testing → 13 (full in 25–26); signal-to-noise → 16; deflated Sharpe, PBO and reality checks → Part 26, previewed in 13; GRS → Part 24, previewed in 4; HJ bounds → Part 23; unit roots and spurious regression → Part 7, signposted in 5.

### 2c. READING.md Part 6 papers

| Paper | Now | Plan |
|---|---|---|
| Fama–Fisher–Jensen–Roll 1969 | absent | ch 10 on screen (history card: splits, event time) + the hook's era strip |
| Hansen 1982 | on screen | ch 8 |
| Hansen–Singleton 1982 | mentioned | ch 9 on screen |
| Newey–West 1987 | on screen | ch 2 (derived) |
| Künsch 1989 | absent (block bootstrap uncredited) | ch 11 on screen |
| Hodrick 1992 | absent (only Hansen–Hodrick 1980) | ch 2: Hodrick 1B se computed beside NW/HH |
| Politis–Romano 1994 | on screen | ch 11 |
| Benjamini–Hochberg 1995 | on screen | ch 13 (proof sketch) |
| MacKinlay 1997 | mentioned | ch 10 on screen (machinery card) |
| Stambaugh 1999 | on screen | ch 5 (derived) |
| Welch–Goyal 2008 | absent | ch 6 on screen (cumulative SSE plot) |
| Campbell–Thompson 2008 | absent | ch 6 on screen (sign restrictions) |
| Petersen 2009 | mentioned | ch 3 on screen (42% of papers did not adjust; simulation) |
| Chernozhukov et al. 2018 | on screen | ch 15 (orthogonality derived) |
| Goyal–Welch–Zafirov 2024 | absent | ch 6 + ch 18 |

Proposed additions to READING.md Part 6 (all used on screen): Cowles 1933 (*Econometrica*); Fama–MacBeth 1973 (*JPE*); Hansen–Hodrick 1980 (*JPE*); Shanken 1992 (shared with Part 24); Kiefer–Vogelsang 2005 (*Econometric Theory*); Lazarus–Lewis–Stock–Watson 2018 (*JBES* 36(4)); Lazarus–Lewis–Stock 2021 (*Econometrica* 89(5) 2497–2516); Kostakis–Magdalinos–Stamatogiannis 2015 (*RFS* 28(5) 1506–1553); Lucca–Moench 2015 (*JF* 70(1) 329–371); Baker–Larcker–Wang 2022 (*JFE* 144(2) 370–395); Roth–Sant'Anna–Bilinski–Poe 2023 (*J. Econometrics* 235(2) 2218–2244); Andrews–Kitagawa–McCloskey 2024 (*QJE* 139(1) 305–358); Menkveld et al. 2024 (*JF* 79(3) 2339–2390); Pérignon et al. 2024 (*RFS* 37(11) 3558–3593); Kelly–Malamud–Zhou 2024 (*JF* 79(1) 459–503); Nagel 2025 (NBER w34104); Maasoumi–Wang–Wang–Wu 2024 (*J. Applied Econometrics* 39(3) 438–461); Glasserman–Lin 2023 (arXiv 2309.17322); Lo 2002 and Mertens 2002 (already used); Ariel 1987 (already used); Chang–Hong–Liskovich 2015 (*RFS*, Russell RD) **(unverified)**.

## 3. The final chapter list (20 entries, about 58 minutes)

Numbering follows the manifest convention: the hook and the closing House/outro are unnumbered (Ch 0 and Ch 19 here); on-screen chapter numbers are 1–18, and every "ch N" in this file uses them.

Every chapter follows the order of SYLLABUS §1: (1) the question; (2) the definition card; (3) the derivation, as a `ladder` with `why` notes; (4) the experiment; (5) the pause-and-predict question; (6) the takeaway with a forward link.

Hands-on markers: **[R]** a replay, scrubbed with a `ValueTracker` (AI Part 21's `replay`); **[S]** seeds or simulations shown as spread bands (as in `measure`); **[L]** a lab: a `code_block` of the House's real function, then a run, with output appearing live; **[E]** an estimator running on screen.

Six labs are planned; the standard asks for three. **Where the hands-on elements are:**
- labs [L]: ch 2 (HAC), 4 (FM), 9 (GMM), 11 (bootstrap), 13 (BH), 15 (DML);
- replays [R]: ch 7 (MLE optimiser on the surface), 8 (two-step GMM), 12 (Gibbs chains), 15 (nuisance learners against λ), 17 (look-ahead equity curves);
- estimators running [E]: ch 1, 4, 6, 10, 16;
- spread bands [S]: ch 2, 3, 5, 9, 13, 14, 15.

**Lab sketches.** Each lab shows the House's real code with `code_block(lines, font=MONO)`, at most 12 lines. Then the run's output appears line by line: the readouts are cached values, revealed with `ValueTracker` counters. Existing code is shown as is:
- lab 1 (ch 2): `econ._hac_meat` (econ.py ll. 66–73) + the two `ols` lines `S = _hac_meat(...)`, `V = XtX_inv @ S @ XtX_inv`;
- lab 2 (ch 4): the `fama_macbeth` loop and its mean/se (econ.py ll. 93–105, minus the NW branch: 11 lines);
- lab 4 (ch 11): `stationary_bootstrap` (ll. 126–139 without the docstring; drop `x = np.asarray(x)` to fit 12 lines);
- lab 5 (ch 13): `benjamini_hochberg` (ll. 172–182, 11 lines);
- labs 3 and 6 are condensed from the real functions, labelled "condensed from `econ.gmm` / `econ.dml_plr`":
```python
# lab 3 (ch 9): condensed from econ.gmm, two steps
obj = lambda th, W: g(th).mean(0) @ W @ g(th).mean(0)
th1 = minimize(obj, th0, args=(I,)).x            # step 1: identity weight
G = g(th1) - g(th1).mean(0); S = G.T @ G / n     # + Bartlett-weighted lags
th = minimize(obj, th1, args=(inv(S),)).x        # step 2: efficient weight
D = jacobian(lambda t: g(t).mean(0), th)
V = inv(D.T @ inv(S) @ D) / n                    # se = sqrt(diag(V))
J = n * obj(th, inv(S))                          # ~ chi2(q - p): 20.0, p = 0.0005
```
```python
# lab 6 (ch 15): condensed from econ.dml_plr, cross-fitted
fold = rng.permutation(n) % 5
for k in range(5):
    tr, te = fold != k, fold == k
    ry[te] = y[te] - ridge_fit_predict(X[tr], y[tr], X[te])
    rd[te] = d[te] - ridge_fit_predict(X[tr], d[tr], X[te])
theta = rd @ ry / (rd @ rd)                      # 0.300 (60 samples; OLS 1.15)
psi = (ry - theta * rd) * rd
se = sqrt(mean(psi**2) / mean(rd**2)**2 / n)
```

Colours as now: `DATA_C`: data; `EST`: estimates; `GOOD`/`BAD`: valid and invalid inference; `ALT`: alternatives; `C.P` throughout. Every result here is a P-measure statement; say so once in ch 1.

### Ch 0 · Hook + era: *One regression, five verdicts* (`s01_hook`, kept and extended), 3.0 min, ~420 words

**Goal:** the viewer feels that "the t-statistic" is not one number.

**Beats:** (1) The Monday question (as now). (2) The five bars grow (as now), plus a sixth bar, "pooled with month effects: 3.56", greyed and labelled "ch 4". (3) "By chapter 4 you'll see why three of these answer different questions." (4) **Era strip** (`timeline(lit=(1933, 1969, 1973, 1982, 1987, 2009, 2016, 2024))`): Cowles 1933, "Can stock market forecasters forecast?"; FFJR 1969 invents the event study; Fama–MacBeth 1973; Hansen 1982 GMM (Nobel 2013); Newey–West 1987; Petersen 2009: 42% of panel papers did not adjust their standard errors; Harvey–Liu–Zhu 2016: at least 316 factors, t > 3; Menkveld et al. 2024: 164 teams, same data, different answers. (5) Objectives card; House chart.

**Visual:** the era strip lights year by year as the bars wait.

**Predict:** "Which of the five will be closest to the pooled-with-month-effects number?" (Answer: none. It sits between pooled and FM, which tells you each answers a different question.)

### Ch 1 · *Least squares, seen as geometry* (new `s02_ols`), 2.5 min, ~350 words. Item 1

**Goal:** OLS as projection; controls as projections first (FWL); every robust standard error as a bread–meat–bread sandwich whose meat is "how the scores co-move".

**Beats:** (1) Recall AI Part 6 (`videos/ai/ai6/s02_lsq.py` projection): y as a point, the column space as a plane, the perpendicular drop. (2) FWL: adding a control is projecting both y and x off the control first. Show it with the market factor as the control and tobacco's excess return as y. The slope on a second regressor (SMB) equals the slope of residual on residual. (3) The sampling error, β̂ − β = (X'X)⁻¹X'u, is a weighted sum of the scores x_t u_t. Its variance is bread · meat · bread. The iid assumption is a claim about the meat. White replaced it with Σ x_t x_t' û_t². The next three chapters are three shapes of meat.

**Derivation:**
$$\hat\beta=(X^\top X)^{-1}X^\top y \quad\text{(normal equations: } X^\top(y-X\hat\beta)=0\text{, residual}\perp\text{columns)}$$
$$\hat\beta-\beta=(X^\top X)^{-1}X^\top u \quad\text{(substitute } y=X\beta+u\text{)}$$
$$\operatorname{Var}(\hat\beta\mid X)=(X^\top X)^{-1}\,X^\top\Omega X\,(X^\top X)^{-1},\ \ \Omega=\mathbb E[uu^\top\mid X] \quad\text{(variance of a linear map)}$$
$$\Omega=\sigma^2 I\ \Rightarrow\ \sigma^2(X^\top X)^{-1} \quad\text{(iid: the textbook formula)}$$
$$\hat\beta_2=(\tilde x_2^\top\tilde x_2)^{-1}\tilde x_2^\top\tilde y,\ \ \tilde v=M_1v,\ M_1=I-X_1(X_1^\top X_1)^{-1}X_1^\top \quad\text{(FWL: } M_1 \text{ is idempotent and kills } X_1\text{)}$$

**Signature visual** (`ThreeDScene`): the 3-observation picture from AI 6 (reuse its construction). Then the camera tilts so the control's direction is "down". Both y and x₂ are projected onto the plane perpendicular to x₁: two shadows, and the line between the shadows has the same slope; second movement: a 2D "sandwich" graphic. Two bread slabs (X'X)⁻¹ hold a meat matrix drawn as an n×n heat-map of Ω. Under iid only the diagonal is lit, and the diagonal widens for White. Labels promise "overlap (ch 2)" and "clusters (ch 3)".

**[E]** FWL live: the two-step residual regression runs and its slope readout snaps to the multiple-regression slope (tobacco on market + SMB, French monthly).

**Experiment** (`ols_fwl`, < 1 s): tobacco on the market and SMB, 1927–2020. The two slopes agree to 1e-12 (the assert is an invariant). Expected: SMB slope negative, about −0.3 **(planning guess)**.

**Predict:** "Add a regressor uncorrelated with x₂. Does β̂₂ change?" (No: M₁ leaves x₂ alone. Its standard error can still change.)

### Ch 2 · *Newey–West: counting dependent data* (rebuild of `s02_overlap` part 1, new `s03_hac`), 3.5 min, ~490 words. Item 1

**Goal:** the long-run variance as the sum of autocovariances, and why it needs a window. Then why even windows over-reject (fixed-b), and the modern fix (EWC).

**Beats:** (1) The Shiller dots and t = 15 (as now). (2) Neighbours share 59 of 60 months. Show the ACF of the scores x_t û_t: a long triangle out to lag 59. (3) Derive the long-run variance. (4) Truncating the sum gives a wrong answer. Summing all sample autocovariances is noisy and can go negative. Bartlett weights fix both (Newey–West 1987). Hansen–Hodrick use flat weights to lag h−1. Hodrick 1992 takes the other route: regress one-period returns on the summed predictor. (5) **[L] lab 1:** `econ._hac_meat` and `econ.ols(se="nw")`, then run: t 15.0 → 2.8 (HH 2.5, Hodrick 1B computed). (6) The size ladder from 2,000 null worlds: naive, NW (rule-of-thumb lag), NW (h−1), NW with a large bandwidth and fixed-b critical values, EWC. (7) Kiefer–Vogelsang (2005): treat b = bandwidth/T as fixed, and the t-statistic has a nonstandard limit with fatter critical values. LLSW 2018 recommend S = 1.3√T with fixed-b values, or EWC with ν = 0.4T^{2/3} cosines and t_ν critical values. Lazarus–Lewis–Stock 2021: the size–power frontier.

**Derivation:**
$$\sqrt T(\hat\beta-\beta)=\Big(\tfrac1T\textstyle\sum x_tx_t^\top\Big)^{-1}\tfrac{1}{\sqrt T}\sum_t x_tu_t \quad\text{(ch 1, scaled)}$$
$$\operatorname{Var}\Big(\tfrac1{\sqrt T}\textstyle\sum_t z_t\Big)=\sum_{|k|<T}\big(1-\tfrac{|k|}T\big)\Gamma_k\ \to\ S=\sum_{k=-\infty}^{\infty}\Gamma_k \quad\text{(expand the square; stationarity)}$$
$$S=2\pi f_z(0) \quad\text{(the long-run variance is the spectrum at frequency zero)}$$
$$\hat S_{NW}=\hat\Gamma_0+\sum_{k=1}^{L}\Big(1-\tfrac{k}{L+1}\Big)(\hat\Gamma_k+\hat\Gamma_k^\top) \quad\text{(Bartlett weights: guaranteed PSD)}$$
$$y_t=\textstyle\sum_{j=1}^{h}\varepsilon_{t+j}\Rightarrow\rho_k=\tfrac{h-k}{h},\ \ \sum_{|k|<h}\rho_k=h \quad\text{(overlap: naive se too small by }\sqrt h\text{)}$$
$$t_{\text{fixed-}b}\Rightarrow\frac{W(1)}{\sqrt{Q_b(\tilde W)}}\ \text{as } T\to\infty,\ b=L/T\text{ fixed} \quad\text{(KV 2005: the kernel estimator stays random)}$$
$$\hat S_{EWC}=\tfrac1\nu\textstyle\sum_{j=1}^{\nu}\Lambda_j^2,\ \ \Lambda_j=\sqrt{\tfrac2T}\sum_t\cos\!\big(\pi j\tfrac{t-1/2}{T}\big)\hat z_t\ \Rightarrow\ t\sim t_\nu \quad\text{(average of }\nu\text{ squared cosine projections)}$$

**Signature visual:** a row of autocovariance bars Γ̂_k for k = −80..80 (real scores from the Shiller regression); a translucent Bartlett triangle, driven by a `ValueTracker` for L, slides open over the bars; each bar is multiplied (dimmed) by the triangle's height, and the weighted sum fills a "long-run variance" thermometer beside it. The t-statistic readout falls live from 15 toward 2.8 as L grows. The window *is* the estimator; second movement: the same bars are replaced by a periodogram whose leftmost bins are lit. EWC averages ν of them.

**[S]** The size ladder as bars with Monte Carlo ± 2 se whiskers, across ρ ∈ {0, 0.9, 0.95, 0.99}, as a small multiple.

**Experiments:** `overlap` (existing, about 1 min) plus `hodrick` (new); `har_size` (new; grid ρ × h ∈ {1, 12, 60} × 5,000 reps; about 10 min). Planning run (T = 600, h = 12, ρ = 0.95, 2,000 reps): naive 55%, NW(L = 6) 18%, NW(L = h−1) 14%, NW(L = 1.3√T = 31) with fixed-b cv 2.12 9.8%, EWC (ν = 28, cv 2.05) 8.9%. Fixed-b polynomial cv = 1.96 + 2.9694b + 0.416b² − 0.5324b³ **(verify against KV 2005)**.

**Predict:** "Monthly returns with no overlap, a predictor with ρ = 0. Does Newey–West still over-reject?" (Barely: the ρ = 0 column sits near 5–6%. The problem is overlap times persistence.)

### Ch 3 · *Clustering: the shocks that are shared* (new `s04_cluster`), 2.5 min, ~350 words. Items 1, 5

**Goal:** the meat matrix in a panel has blocks: firm effects, time effects, or both. Cluster on the dimension that the *regressor and the residual* both share.

**Beats:** (1) Back to the hook panel. (2) Petersen's 2009 count: 42% of the panel papers he surveyed did not adjust their standard errors. (3) Derive the cluster meat. (4) Simulate Petersen's design with a known truth. Vary the share of firm effect in x and in u, then the share of time effect. (5) Which standard error survives where: OLS fails under either effect. Firm clustering fixes firm effects only. FM fixes time effects only (and fails under persistent firm effects). Two-way covers both. (6) The finance rule: returns share time shocks, so cluster by month.

**Derivation:**
$$\hat V_{cl}=(X^\top X)^{-1}\Big(\sum_{g}X_g^\top\hat u_g\hat u_g^\top X_g\Big)(X^\top X)^{-1} \quad\text{(meat = sum over clusters of outer products of cluster scores)}$$
$$\operatorname{Var}(\hat\beta)\approx\frac{\sigma_u^2}{\sum x^2}\Big[1+(n_g-1)\rho_x\rho_u\Big] \quad\text{(Moulton factor: equal clusters, both intraclass-correlated)}$$
$$\hat V_{2way}=\hat V_{firm}+\hat V_{time}-\hat V_{firm\cap time} \quad\text{(inclusion–exclusion; Cameron–Gelbach–Miller 2011)}$$

**Signature visual:** the residual-covariance heat-map for a 6-firm × 8-month toy panel, rows ordered (month, firm); a toggle animates the true Ω under "firm effect" (stripes every 6th cell) and "time effect" (8 diagonal blocks); each estimator then lays its "mask" over the matrix: OLS covers only the diagonal; firm clusters cover the stripes; month clusters cover the blocks. The uncovered lit cells flash red: that is the missing variance.

**[S]** Petersen grid run on screen: standard-error ratios (estimated/true) as bars that settle as replications accumulate (counter 0 → 1,000).

**Experiment** (`petersen`, 1,000 reps × 5 designs, 500 firms × 10 years, about 6 min). Expected, in the shape of Petersen's Table 1 **(planning guess)**: with a 50% firm effect in both x and u, OLS se / true ≈ 0.5; clustered by firm ≈ 1.0; FM ≈ 0.5.

**Predict:** "Industry momentum: cluster by industry or by month?" (Month: the t falls to 0.27, because the shared shock is the market.)

### Ch 4 · *Fama–MacBeth, and five verdicts resolved* (new `s05_famamacbeth`), 3.5 min, ~490 words. Items 5, 1

**Goal:** FM as T cross-sectional regressions stacked into a time series of slopes. Its se is a time-series se (robust to cross-sectional correlation). The two-pass test of the CAPM, the errors-in-variables problem, and Shanken's correction. Resolve the hook: within- versus between-month variation.

**Beats:** (1) Fama and MacBeth, 1973. (2) Each month: a scatter of 49 industries (past return against next return) and a fitted line. Its slope drops into a growing strip chart of slopes. (3) **[L] lab 2:** `econ.fama_macbeth`, the 8-line loop, then run on 1,116 months. The slope strip fills, and the mean ± 2se band narrows: 0.0170, t 5.08 (NW(6) 5.16). 61% of monthly slopes are positive. (4) The resolution, in a decomposition panel: pooled = within (month-demeaned) + between (month means); within, pooled = 0.0103 (t 3.56 clustered by month) = the dispersion-weighted FM average 0.0102; between: −0.0037 (t −0.29). Pooled 0.0022 averages the two; "FM asks whether winners beat losers within a month; pooled asks that plus whether the whole market follows its own past year." (5) The two-pass CAPM test: first pass: rolling betas from time series; second pass: FM of returns on betas; 57 portfolios (49 industries + 10 B/M deciles, 1963–2020): λ̂_m ≈ 0.00 per month against a market premium of 0.57%, intercept 0.65% (t 3.2). The security market line is flat. GRS F = 1.62, p = 0.004 (planning run). (6) EIV: betas are estimated, so the second-pass se is too small. Shanken's factor 1 + λ²/σ_f². (7) Forward link: GRS and factor models in Part 24.

**Derivation:**
$$r_{it}=\gamma_{0t}+\gamma_{1t}x_{i,t-1}+e_{it}\ \ \text{each }t;\quad \hat\gamma_1=\tfrac1T\textstyle\sum_t\hat\gamma_{1t} \quad\text{(average of cross-sectional slopes)}$$
$$\widehat{\operatorname{se}}(\hat\gamma_1)=\frac{s(\hat\gamma_{1t})}{\sqrt T} \quad\text{(the slopes' own time-series variation absorbs cross-sectional correlation)}$$
$$\hat\beta^{pooled,FE}=\frac{\sum_t\sum_i\tilde x_{it}\tilde r_{it}}{\sum_t\sum_i\tilde x_{it}^2}=\sum_t w_t\hat\gamma_{1t},\ \ w_t=\frac{\sum_i\tilde x_{it}^2}{\sum_s\sum_i\tilde x_{is}^2} \quad\text{(within-month OLS = dispersion-weighted FM)}$$
$$\hat\beta^{pooled}=\text{mix of within and between slopes, weighted by }SS_{within},SS_{between} \quad\text{(ANOVA split of }\sum x^2\text{)}$$
$$\operatorname{Var}(\hat\lambda)\approx\frac1T\Big[(1+\lambda^\top\Sigma_f^{-1}\lambda)\,\sigma^2_{\gamma}+\Sigma_f\Big] \quad\text{(Shanken 1992: estimated betas inflate the variance)}$$

**Signature visual:** left: the monthly cross-section scatter flickers month to month (1,116 frames at 30 per second, with `ValueTracker` speed-ups); right: each month's fitted line rotates to its slope and then "drops" as a tick onto a vertical stack. The stack becomes a histogram of slopes, with its mean and se band; for the resolution: a 2D scatter of (x, r) for 3 months coloured by month. The animation subtracts the month means (each cloud slides to the origin): the within slope. Then the 3 month-means alone: the between slope. Then both together give the pooled line in between; two-pass: the SML drawn through 57 dots (mean return against beta), flat, with the CAPM-predicted line tilted above it.

**[E]/[R]** The FM mean and se readouts update as slopes stack.

**Experiments:** `panel` (existing) plus `panel_fe` (new, < 1 min); `twopass` (new; 60-month rolling betas plus a full-sample version, Shanken, GRS; about 1 min).

**Predict:** "Before the decomposition: is the market's own past year a buy signal?" (No: between slope −0.004, t −0.3.)

### Ch 5 · *Predictive regressions: Stambaugh's bias* (deepened `s06_stambaugh`), 3.0 min, ~420 words. Item 2

**Goal:** derive the bias. See it as a regression of β̂'s error on ρ̂'s error. Corrections: the Amihud–Hurvich augmented regression, and IVX (Kostakis et al. 2015).

**Beats:** (1) The dividend yield is persistent, and its shocks mirror return shocks (corr −0.83). (2) The simulation cloud. (3) The derivation. (4) The real annual regression: β 0.034 (t 1.1), bias +0.018, corrected 0.016. (5) Corrections: augment with the predictor's innovation v̂ (bias-corrected ρ). IVX instruments x with a less persistent version of itself and keeps χ² inference for any persistence. Kostakis et al.: short-horizon predictability in 1927–2012 that almost disappears after 1952, and weaker at longer horizons. (6) Signpost to Part 7 (unit roots, spurious regression).

**Derivation:**
$$r_{t+1}=\alpha+\beta x_t+u_{t+1},\quad x_{t+1}=\theta+\rho x_t+v_{t+1} \quad\text{(the predictive system)}$$
$$u=\phi v+e,\ \ \phi=\sigma_{uv}/\sigma_v^2,\ e\perp v \quad\text{(project u on v)}$$
$$\hat\beta-\beta=\phi(\hat\rho-\rho)+\frac{\sum\tilde x_te_{t+1}}{\sum\tilde x_t^2} \quad\text{(same regressor in both equations)}$$
$$\mathbb E[\hat\beta-\beta]=\phi\,\mathbb E[\hat\rho-\rho]\approx-\phi\frac{1+3\rho}{T} \quad\text{(second term mean zero; Kendall 1954)}$$
$$\text{annual: }\phi=-0.72,\ \rho=0.91,\ T=149\Rightarrow\text{bias}=+0.72\cdot3.72/149=+0.018 \quad\text{(worked example)}$$

**Signature visual:** 4,000 simulated samples as a cloud of points (ρ̂ − ρ, β̂ − β), drawn as they are simulated ([S], counter up); the cloud is a tilted ellipse with slope φ = −0.72 (dashed line labelled φ). Its centre sits left of zero on the ρ axis (Kendall's bias). Projecting the centre down the tilt onto the β axis lands it above zero: the bias, made visible; then T slides from 50 to 150 (`ValueTracker`). The cloud shrinks and its centre crawls toward the origin; the old histograms are kept as the marginal on the right edge.

**Experiments:** `stambaugh` (existing; extend to store the joint (ρ̂, β̂) pairs; about 2 min); `ivx` (new; Amihud–Hurvich and IVX on annual and monthly Shiller; about 1 min). Expected: the augmented estimate is ≈ 0.016 with t < 1 **(planning guess)**.

**Predict:** "If the predictor's shocks were *positively* correlated with returns, which way is the bias?" (Negative.)

### Ch 6 · *Out of sample: can anything beat the historical mean?* (new `s07_oos`), 2.5 min, ~350 words. Item 2

**Goal:** in-sample R² against out-of-sample R². The Goyal–Welch cumulative-SSE plot. Campbell–Thompson restrictions. Goyal–Welch–Zafirov 2024.

**Beats:** (1) A forecaster in 1927 with only past data. (2) **[E]** The expanding-window regression refits month by month on screen: the slope with its NW band evolves, and each month's forecast is made. (3) ΔSSE accumulates into a curve. (4) Planning run (monthly Shiller, real log returns, log D/P, OOS from 1927): R²_OS = −0.32%. Campbell–Thompson (truncate negative forecasts, drop wrong-signed slopes): −0.12%. The ΔSSE curve rises briefly, collapses in the 1990s bull market, and ends at −0.0073 (−0.0034 by 1990, −0.0081 by 2000). (5) Goyal–Welch 2008: none of their predictors beat the mean for a real-time investor. GWZ 2024 re-tested 29 newer variables from 26 post-2008 papers plus the original 17, as of end-2021: more than a third lose significance even in sample, and about half the survivors fail out of sample. (6) The R²_OS needed to matter: Campbell–Thompson show a 0.5% monthly R²_OS is economically large for a mean-variance investor. (7) Forward link: Kelly–Malamud–Zhou in the frontier chapter.

**Derivation:**
$$R^2_{OS}=1-\frac{\sum_t(r_t-\hat r_{t|t-1})^2}{\sum_t(r_t-\bar r_{t-1})^2} \quad\text{(beat the running mean, not zero)}$$
$$\Delta SSE(\tau)=\sum_{t\le\tau}\big[(r_t-\bar r_{t-1})^2-(r_t-\hat r_{t|t-1})^2\big] \quad\text{(GW's picture: rising = predictor winning)}$$
$$\text{Sharpe gain}\approx\frac{S^2+R^2}{1-R^2}-S^2 \quad\text{(Campbell–Thompson: } R^2\text{ is worth a lot when } S \text{ is small) **(verify exact form)**}$$

**Signature visual:** top: Shiller monthly D/P with a moving "now" cursor; middle: the expanding-window slope ± NW band redrawn each step; bottom: the ΔSSE curve drawn in sync. Gold where it rises, red where it falls; 1995–2000 lit red; in-sample, the full-sample line looks convincing. As the cursor moves, every past forecast is fixed and visibly wrong in the 1990s.

**Experiment:** `oos` (new; expanding window, 5 predictors from Shiller: D/P, E/P, CAPE, GS10, inflation; plus GWZ-style IS and OOS tables; about 2 min).

**Predict:** "In-sample R² is 0.06% monthly. Can R²_OS be positive?" (Rarely. It must beat estimation noise in the slope.)

### Ch 7 · *Maximum likelihood* (new `s08_mle`), 3.0 min, ~420 words. Item 3

**Goal:** the likelihood as a surface, its curvature as information, QMLE's sandwich, and the link to ch 1.

**Beats:** (1) Fat tails (Part 1): fit a Student-t to daily market returns. (2) **[R]** The optimiser climbs the log-likelihood surface: Newton steps from a bad start, checkpoints scrubbed with the −logL curve. (3) Derive the score, the information matrix and the asymptotic normality. (4) Curvature = precision. The ellipse at the peak is the 95% region. (5) QMLE: if the model is wrong (volatility clusters, so the iid t is wrong), the information-matrix equality fails. Use the sandwich H⁻¹JH⁻¹: ch 1's bread and meat again. (6) Result: ν̂ ≈ 2.5 on 1926–2020 daily (planning run). The sandwich se of ν is several times the naive one. The naive se trusts a model the data reject.

**Derivation:**
$$\ell(\theta)=\textstyle\sum_t\log f(x_t;\theta),\quad s(\theta)=\nabla\ell,\quad \mathbb E_{\theta_0}[s_t(\theta_0)]=0 \quad\text{(differentiate }\int f=1\text{)}$$
$$\mathcal I=-\mathbb E[\nabla^2\log f]=\mathbb E[s_ts_t^\top] \quad\text{(information-matrix equality: differentiate again)}$$
$$0=s(\hat\theta)\approx s(\theta_0)+\nabla^2\ell(\theta_0)(\hat\theta-\theta_0)\Rightarrow\sqrt T(\hat\theta-\theta_0)\to N(0,\mathcal I^{-1}) \quad\text{(Taylor; CLT on the score; LLN on the Hessian)}$$
$$\text{misspecified: }\sqrt T(\hat\theta-\theta^*)\to N(0,H^{-1}JH^{-1}) \quad\text{(QMLE; } H\neq J\text{)}$$
$$\text{Gaussian linear model: }\hat\beta_{ML}=\hat\beta_{OLS} \quad\text{(ch 1 of AI Part 6, recalled)}$$

**Signature visual** (`ThreeDScene`, `loss_surface` from `explainer/ai/viz.py`): log-likelihood over (ν, scale) as a hill; a ball (`surface_ball`) climbs by Newton steps, each step a `surface_path` segment; at the top, the camera looks straight down. The contour of ℓ̂ − 3 (≈ χ²₂ 95%) is the confidence ellipse; the hill is sharpened or flattened by changing T (a `ValueTracker` on the sample size): the ellipse shrinks as 1/√T.

**Experiment:** `mle` (new; scipy minimise with a callback recording the iterates; Hessian and OPG; about 1 min).

**Predict:** "Double the sample. What happens to the ellipse's area?" (It halves: each axis shrinks by √2.)

### Ch 8 · *GMM: getting the moments as close to zero as possible* (rebuild of `s03_gmm` part 1, new `s09_gmm`), 3.0 min, ~420 words. Item 3

**Goal:** GMM's geometry in moment space, efficient weighting, the asymptotic variance, and the J test as leftover distance. OLS, IV and ML as special cases.

**Beats:** (1) A theory gives averages that should be zero. (2) Two moments, one parameter: as θ varies, ḡ(θ) traces a curve in the plane. (3) GMM picks the curve point closest to the origin in the metric W (ellipses of equal W-distance grow from the origin until they touch the curve). (4) Efficient W = S⁻¹ stretches the metric along the noisy direction. (5) The leftover distance, scaled by T, is J ~ χ²_{q−p}. (6) Variance formula. (7) Special cases: OLS (x(y − xβ) moments), IV (z(y − xβ)), ML (score moments). (8) **[R]** The two-step iteration: first-step W = I, then W = Ŝ⁻¹. The tangent ellipse reshapes, and the touching point moves.

**Derivation:**
$$g_T(\theta)=\tfrac1T\textstyle\sum_tg(x_t,\theta),\quad \hat\theta=\arg\min g_T^\top Wg_T \quad\text{(definition)}$$
$$D^\top Wg_T(\hat\theta)=0,\ \ D=\partial g_T/\partial\theta^\top \quad\text{(first-order condition)}$$
$$g_T(\hat\theta)\approx g_T(\theta_0)+D(\hat\theta-\theta_0)\Rightarrow\hat\theta-\theta_0\approx-(D^\top WD)^{-1}D^\top Wg_T(\theta_0) \quad\text{(linearise and solve)}$$
$$\operatorname{Var}(\hat\theta)=\tfrac1T(D^\top WD)^{-1}D^\top WSWD(D^\top WD)^{-1} \quad\text{(sandwich again; } S\text{ = long-run variance of } g\text{, ch 2)}$$
$$W=S^{-1}\Rightarrow\operatorname{Var}=\tfrac1T(D^\top S^{-1}D)^{-1} \quad\text{(the sandwich collapses: efficiency)}$$
$$J=T\,g_T(\hat\theta)^\top\hat S^{-1}g_T(\hat\theta)\to\chi^2_{q-p} \quad\text{(}q\text{ normalised moments minus }p\text{ fitted directions)}$$

**Signature visual:** 2D moment plane with the origin marked "theory"; the curve ḡ(θ) for a toy (estimate a mean μ from two noisy measures with different variances) is traced as a `ValueTracker` on θ moves a dot along it; W-ellipses inflate from the origin until tangent: the estimate. Switching W from I to S⁻¹ morphs the circle into a stretched ellipse, and the tangent point slides toward the precise measure; the gap vector from origin to tangent point stays: its W-length is √(J/T). Draw the χ²₁ density beside it, with J's position marked.

**Experiment:** `gmm_toy` (new; trivial). The Euler moment-space version (6 moments projected to 2D by PCA of S) is computed in `gmm_surface`.

**Predict:** "Exactly as many moments as parameters: what is J?" (Zero. Nothing is left to test.)

### Ch 9 · *The Euler equation, estimated and rejected* (rebuild of `s03_gmm` part 2, new `s10_euler`), 2.5 min, ~350 words. Item 3

**Goal:** the consumption CAPM moment conditions estimated; weak identification of γ; the equity premium puzzle.

**Beats:** (1) The Euler equation (as now). (2) Hansen–Singleton 1982. (3) **[L] lab 3:** `econ.gmm`, the 10-line two-step core, then run. β 1.002 (0.009), γ 1.1 (1.5), J 20.0, p 0.0005. (4) The objective surface (3D): sharp in β, an almost flat ridge in γ. "The data barely know γ": weak identification (Stock–Wright 2000). The usual se is unreliable on a ridge. (5) A small-sample Monte Carlo from a world where the model is true, at our sample size: the γ̂ histogram is wide and skewed, and the J test's size is shown. (6) Why it fails: the premium is 2.1% a quarter, consumption sd 1.1%, correlation 0.06, so γ ≈ 421. Mehra–Prescott 1985. Forward link to Part 23 (HJ bounds, habit, long-run risk).

**Derivation:**
$$\mathbb E_t[m_{t+1}R_{t+1}]=1,\ m=\beta(C_{t+1}/C_t)^{-\gamma} \quad\text{(first-order condition for one more dollar saved)}$$
$$\mathbb E[(m_{t+1}R_{t+1}-1)\otimes z_t]=0 \quad\text{(conditional to unconditional: tower property with instruments } z_t\text{)}$$
$$\mathbb E[R^e]=-\frac{\operatorname{cov}(m,R^e)}{\mathbb E[m]}\approx\gamma\operatorname{cov}(\Delta c,R^e) \quad\text{(}\mathbb E[mR^e]=0\text{; log-linearise } m\text{)}$$
$$\gamma\approx\frac{0.021}{\operatorname{cov}(\Delta c,R^e)}\approx421 \quad\text{(worked example, cached numbers)}$$

**Signature visual** (`ThreeDScene`): J(β, γ) as a surface over β ∈ [0.95, 1.05], γ ∈ [−5, 30]; the camera walks along the ridge. A ball drops and rolls: it finds β quickly and then wanders along γ; overlay: the iid-se ellipse (thin and long) against the ridge it fails to capture.

**[S]** Monte Carlo γ̂ histogram from 400 simulated economies (seeded), drawn as it fills.

**Experiments:** `gmm` (existing); `gmm_surface` (grid 120 × 120; about 1 min); `gmm_mc` (400 economies × two-step Nelder–Mead; about 8 min).

**Predict:** "Add the T-bill's moment only. Can γ be identified?" (Barely. The bill pins β, and γ needs the risky asset's covariance with consumption.)

### Ch 10 · *Event studies* (rebuild of `s04_event`, new `s11_event`), 3.0 min, ~420 words. Item 4

**Goal:** the event-study machinery (estimation window, market model, AR, CAR, its variance, cross-sectional dependence when events cluster in calendar time), done twice on real data.

**Beats:** (1) FFJR 1969: stock splits, the first event study in event time. (2) The machinery card (MacKinlay 1997). (3) Derivation of Var(CAR). (4) Real case 1, the turn of the month (existing numbers, now with a CAR curve). (5) Real case 2, **FOMC announcement days**, 1994–2020: daily market returns (French) on scheduled-announcement days against other days. (6) Lucca–Moench 2015: the S&P 500 rose 49 bp on average in the 24 hours before scheduled announcements since 1994, and there was no such drift before 1980. Our close-to-close day contains the drift and the announcement. (7) Inference when every "firm" shares the same date: all events are market-wide, so there is no cross-sectional diversification. Use the time-series variance of non-event days (the "crude dependence adjustment"). (8) Placebo: 10,000 random sets of the same number of dates give the null distribution; the real mean is marked.

**Derivation:**
$$AR_{i\tau}=R_{i\tau}-(\hat\alpha_i+\hat\beta_iR_{m\tau}) \quad\text{(market model from the estimation window)}$$
$$\overline{CAR}(\tau_1,\tau_2)=\tfrac1N\textstyle\sum_i\sum_{\tau=\tau_1}^{\tau_2}AR_{i\tau} \quad\text{(average across events, sum over the window)}$$
$$\operatorname{Var}(\overline{CAR})=\tfrac{1}{N^2}\textstyle\sum_i(\tau_2-\tau_1+1)\sigma^2_{\varepsilon_i} \quad\text{(independent events; ignoring estimation error)}$$
$$\text{events on the same date: } \operatorname{Var}=\tfrac1{N^2}\textstyle\sum_i\sum_j\operatorname{cov}(CAR_i,CAR_j)\not\to0 \quad\text{(clustering: no diversification)}$$
$$J_1=\overline{CAR}/\widehat{\operatorname{se}}\sim N(0,1) \quad\text{(test statistic)}$$

**Signature visual:** 40 real price paths of the market around FOMC days in *calendar time*, scattered along a long axis; they slide horizontally (`ApplyMethod` shift per path) until all their announcement days stack at τ = 0, and the axis relabels to "trading days from the event"; the mean path draws in gold, with a ± 2 se band that narrows as more paths join (counter N = 1 → ≈ 216 scheduled meetings); then the band is redrawn with the clustering-adjusted se and widens. This is the "same date" lesson.

**[E]** The placebo histogram builds from random date sets, with the real CAR marked.

**Experiments:** `event` (existing); `fomc` (new; about 2 min including 10,000 placebos). Needs a new file `videos/quant/quant6/fomc_dates.py`: the scheduled FOMC statement dates 1994–2020, transcribed from federalreserve.gov `fomchistorical<YYYY>.htm` and `fomccalendars.htm` (scheduled meetings only; second day of two-day meetings). Expected: announcement-day mean well above other days, with the effect weaker after 2011 (Kurov–Wolfe–Gilbert report a decline; **(unverified)** in our data). Narration branches on the computed t.

**Predict:** "100 firms all announcing on the same day: is the CAR's se σ/√100?" (No. If the shock is common, the se barely shrinks.)

### Ch 11 · *The bootstrap for dependent data* (rebuild of `s05_sharpe` part 1, new `s12_bootstrap`), 3.0 min, ~420 words. Item 6

**Goal:** the plug-in principle. Why the iid bootstrap fails under volatility clustering. Blocks (Künsch 1989) and geometric blocks (Politis–Romano 1994). Coverage measured.

**Beats:** (1) The bootstrap idea: the sample stands in for the population. (2) The iid bootstrap shreds the series into months: a resampled path loses its calm and stormy seasons (shown side by side with the real path). (3) Moving blocks keep runs of 12 months. Stationary blocks have geometric lengths and wrap around, so the resample is stationary. (4) **[L] lab 4:** `econ.stationary_bootstrap` (10 lines), run. The histogram of 800 Sharpe ratios fills, se 0.122 against iid 0.104. (5) Coverage experiment on a simulated GARCH(1,1) world with known Sharpe: the nominal 95% intervals' coverage, iid against block (computed; the narration branches on the gap). (6) Block-length choice: the bias–variance trade-off again (as the HAC bandwidth).

**Derivation:**
$$\hat F_n\approx F\Rightarrow\operatorname{Law}(\hat\theta^*-\hat\theta\mid\hat F_n)\approx\operatorname{Law}(\hat\theta-\theta\mid F) \quad\text{(plug-in principle)}$$
$$\operatorname{Var}^*\big(\sqrt n\,\bar x^*_{iid}\big)=\hat\Gamma_0\ \ne\ S \quad\text{(iid resampling keeps only lag 0 of the long-run variance)}$$
$$\operatorname{Var}^*\big(\sqrt n\,\bar x^*_{block}\big)\approx\hat\Gamma_0+2\textstyle\sum_{k<\ell}(1-k/\ell)\hat\Gamma_k \quad\text{(blocks of length }\ell\text{ reproduce a Bartlett-weighted S: ch 2 again)}$$

**Signature visual:** the 1,134 monthly returns as a ribbon of coloured bars, height |r|, so volatility clusters are visible; a pair of scissors cuts blocks (geometric lengths drawn from a ValueTracker-seeded RNG). The blocks fly into a new ribbon below and the Sharpe readout computes; repeat, accelerating (B = 1, 2, 5, 20, 800). Each resample drops a tick into the histogram; a toggle to "block length 1" shows the shredded ribbon and the narrower histogram.

**Experiments:** `bootstrap` (existing; about 3 min); `boot_coverage` (new; 300 GARCH paths × B = 400 × 3 methods; numba-free numpy; about 20 min, the part's largest item, resumable per path). Expected: iid coverage below 95% (for example, 85–90%), block close to 93–95% **(planning guess; narration branches)**.

**Predict:** "Block length equal to the whole sample: what is the bootstrap se?" (Zero. Every resample is the sample, shifted.)

### Ch 12 · *Shrinkage and Bayes* (rebuild of `s06_many` part 1, new `s13_bayes`), 3.0 min, ~420 words. Item 7

**Goal:** the posterior mean as a precision-weighted average. Empirical Bayes and James–Stein. The hierarchical model sampled by Gibbs.

**Beats:** (1) Forty industry means estimated on 1927–73 and scored on 1974–2020: the ranks scramble (existing). (2) Conjugate normal algebra. (3) Hierarchical model on the 49 CAPM alphas: α_i ~ N(μ, τ²), α̂_i ~ N(α_i, s_i²). (4) **[R]** Gibbs sampler with 4 chains: traces scrubbed with the τ posterior filling. τ's posterior piles near zero, and every alpha shrinks hard. (5) Out of sample, the grand mean beats 40 raw means: MSE 8.0 → 3.8 (existing). (6) Stein 1956. A prior is how you borrow strength across assets. Forward: Parts 27 and 30.

**Derivation:**
$$\alpha_i\mid\hat\alpha_i\sim N\Big(B_i\mu+(1-B_i)\hat\alpha_i,\ (1-B_i)s_i^2\Big),\ B_i=\frac{s_i^2}{s_i^2+\tau^2} \quad\text{(complete the square)}$$
$$\hat\tau^2=\max\big(0,\ \operatorname{var}(\hat\alpha)-\overline{s^2}\big) \quad\text{(empirical Bayes: the spread of estimates minus their noise)}$$
$$R(\hat\mu^{JS})=k-(k-2)^2\,\mathbb E\big[1/\|x\|^2\big]<k \quad\text{(Stein's lemma; worked in Problem 5)}$$
$$\tau^2\mid\alpha\sim\text{Inv-}\chi^2,\quad\alpha_i\mid\tau,\mu\sim N(\cdot,\cdot),\quad\mu\mid\alpha,\tau\sim N(\cdot,\cdot) \quad\text{(Gibbs: each conditional is conjugate)}$$

**Signature visual:** 49 beads on vertical rods at their raw alpha. Each bead is tied by a spring to a horizontal bar at the grand mean μ; spring stiffness is drawn as thickness ∝ 1/s_i² relative to 1/τ²; as the Gibbs replay scrubs, τ shrinks (readout) and the bar pulls all beads in. Noisy beads (wide error bars) move most; the out-of-sample dots appear and sit closer to the shrunk beads.

**Experiments:** `shrinkage` (existing); `gibbs` (new; 4 chains × 5,000 draws; seeds 0–3; about 2 min).

**Predict:** "One industry has a huge raw alpha *and* a huge standard error. Does it shrink most or least?" (Most.)

### Ch 13 · *Many tests* (rebuild of `s06_many` part 2, new `s14_many`), 3.0 min, ~420 words. Item 8

**Goal:** FWER against FDR, with proofs. Bonferroni, Holm, BH. What the counts mean. A preview of Parts 25–26.

**Beats:** (1) The 49 alphas, with 5 under 5%. (2) Expected false positives = mα. (3) Bonferroni (union bound). (4) Holm (proof on screen). (5) BH: the rotating line on sorted p-values. (6) Planted truth: 1,000 strategies, 50 with real SR 0.5 over 20 years. Show the true and false discoveries of each method across 200 seeds as bands [S]. Expected: BH keeps the FDR near 5% and finds more true ones than Holm. (7) **[L] lab 5:** `econ.benjamini_hochberg` (8 lines), run on the 49 p-values: 0. Then on the planted world: the counts appear. (8) Preview: White's reality check and Romano–Wolf (Part 26); HLZ's t > 3 and the replication debate (Part 25).

**Derivation:**
$$P\Big(\bigcup_{i\in H_0}\{p_i\le\alpha/m\}\Big)\le\textstyle\sum_{i\in H_0}\alpha/m\le\alpha \quad\text{(union bound)}$$
$$\text{Holm: at the first false rejection }\ge m_0\text{ remain}\Rightarrow\text{threshold}\le\alpha/m_0 \quad\text{(so FWER}\le\alpha\text{)}$$
$$\text{BH: }k=\max\{i:p_{(i)}\le iq/m\};\ \ \mathrm{FDR}=\mathbb E\Big[\tfrac{V}{\max(R,1)}\Big]=\tfrac{m_0}{m}q\le q \quad\text{(independent p-values; BH 1995)}$$
$$p\text{-histogram}=\pi_0\cdot\text{Uniform}+(1-\pi_0)\cdot\text{spike near 0} \quad\text{(what a null looks like)}$$

**Signature visual:** the sorted p-values as dots on (rank i, p_(i)) axes; the Bonferroni line is horizontal at α/m. The BH line rotates up from the origin (`ValueTracker` on its slope, ending at q/m). The last dot under it and everything to its left turn gold; a second panel: the p-value histogram of the 1,000 planted strategies, a uniform floor plus a spike at zero, with the floor height labelled π₀.

**Experiments:** `multiple` (existing); `fdr_sim` (new; 200 seeds × 1,000 strategies; about 1 min).

**Predict:** "Twenty strategies; the best has p = 0.03. Significant?" (Desk question 2: 46% chance by luck.)

### Ch 14 · *Causal designs: instruments, differences, discontinuities* (rebuild of `s07_causal` part 1, new `s15_designs`), 3.0 min, ~420 words. Item 9

**Goal:** three designs as estimators with derivations, each run on a simulated market with a known effect (the real data are not public). Plus the staggered-DiD trap (Baker–Larcker–Wang 2022).

**Beats:** (1) A confounder DAG. (2) IV: Wald ratio and 2SLS. A weak first stage inflates bias toward OLS; show F < 10 against F = 50. (3) DiD: parallel trends, the 2×2 formula. Then a staggered rollout with a dynamic effect: TWFE gets the sign wrong because early-treated units serve as controls. The Callaway–Sant'Anna estimator recovers the truth. Baker–Larcker–Wang show this overturns published finance results. Example design: the SEC's Regulation SHO pilot **(unverified details)**. (4) RD at the Russell 1000/2000 cutoff (synthetic data with a planted 2% jump in index-fund ownership causing a return effect): local linear fits on each side, with bandwidth chosen by the bias–variance trade-off (a slider). Cite Chang–Hong–Liskovich 2015 **(unverified)** for the real-data version.

**Derivation:**
$$\beta_{IV}=\frac{\operatorname{cov}(z,y)}{\operatorname{cov}(z,x)} \quad\text{(}z\perp u\text{; divide reduced form by first stage)}$$
$$\hat\beta_{DiD}=(\bar y_{T,1}-\bar y_{T,0})-(\bar y_{C,1}-\bar y_{C,0}) \quad\text{(parallel trends cancels the common change)}$$
$$\hat\beta_{TWFE}=\textstyle\sum_k w_k\,\widehat{DiD}_k,\ \ \text{some }w_k<0\text{ under staggered timing} \quad\text{(Goodman-Bacon 2021 decomposition)}$$
$$\tau_{RD}=\lim_{c\downarrow}\mathbb E[y\mid r=c]-\lim_{c\uparrow}\mathbb E[y\mid r=c] \quad\text{(continuity of potential outcomes at the cutoff)}$$

**Signature visual:** DiD: two lines (treated, control) before and after; the control's change is copied (ghost line) onto the treated start, and the gap is the effect; staggered: three cohorts' lines. The TWFE weights appear as bars, one negative, flashing red; RD: a scatter around the rank-1000 cutoff. Two local-linear fits on a bandwidth window that a slider widens. The jump estimate and its CI update live: narrow windows are noisy, wide ones biased.

**[S]** The TWFE against the CS estimate across 200 simulated panels as two histograms; the truth is a gold line.

**Experiments:** `designs` (new; IV weak and strong, DiD 2×2 and staggered, RD; 200 seeds each; about 5 min). Planting is in the code and stated on screen.

**Predict:** "Every firm is eventually treated and the effect grows over time. Is the TWFE estimate too big or too small?" (Too small, possibly negative.)

### Ch 15 · *Double machine learning* (rebuild of `s07_causal` part 2, new `s16_dml`), 3.0 min, ~420 words. Item 9

**Goal:** why plugging in ML fails (regularisation bias), Neyman orthogonality, and cross-fitting.

**Beats:** (1) The partially linear model. (2) Naive plug-in: learn g with a ridge, regress y − ĝ on d. The bias survives because d depends on X. (3) Orthogonal score: residualise both. The first-order effect of nuisance error vanishes. (4) Cross-fitting avoids own-observation overfitting. (5) **[L] lab 6:** `econ.dml_plr` (12 lines), run: θ̂ = 0.300 ± 0.018 across 60 samples, against OLS 1.15. (6) **[R]** Nuisance learners trained: the out-of-fold MSE of m̂ and ĝ against ridge λ (a training curve). Below it, θ̂ against λ for the naive plug-in (drifts with λ) and for DML (flat). 5 seeds as bands.

**Derivation:**
$$y=\theta d+g(X)+\varepsilon,\quad d=m(X)+v \quad\text{(partially linear model)}$$
$$\psi(W;\theta,\eta)=\big(y-\ell(X)-\theta(d-m(X))\big)\big(d-m(X)\big),\ \ \ell=\mathbb E[y\mid X] \quad\text{(residual-on-residual score)}$$
$$\partial_\eta\mathbb E[\psi(W;\theta_0,\eta)]\big|_{\eta_0}=0 \quad\text{(Neyman orthogonality: errors in }\hat m,\hat\ell\text{ enter only at second order)}$$
$$\sqrt n(\hat\theta-\theta_0)=\frac{\tfrac1{\sqrt n}\sum\psi(W_i;\theta_0,\eta_0)}{\mathbb E[v^2]}+O_p\big(\sqrt n\,\|\hat m-m\|\,\|\hat\ell-\ell\|\big) \quad\text{(product of rates: }n^{-1/4}\text{ each suffices)}$$

**Signature visual:** a 2D scatter of (d, y) coloured by X₁ shows the confounded slope (1.15); the animation "subtracts" m̂(X) along d and ℓ̂(X) along y: the points slide to a residual cloud whose slope is 0.3; fold colours (5 folds) show that each point's nuisance prediction came from the other four (arrows from the training folds).

**Experiments:** `dml` (existing); `dml_lambda` (new; λ grid × 5 seeds; about 6 min).

**Predict:** "If m̂ is perfect but ℓ̂ is poor, is θ̂ still fine?" (Yes, to first order: the product of errors is zero.)

### Ch 16 · *How many years until you know?* (rebuild of `s05_sharpe` part 2, new `s17_snr`), 2.5 min, ~350 words. Item 10

**Goal:** t ≈ SR√T; years to significance; the (α, β) ellipse shrinking as data arrive.

**Beats:** (1) The formula and the Lo/Mertens se. (2) **[E]** The tobacco (α, β) ellipse refits month by month from 1961 (a ValueTracker over months). The β axis collapses in a few years; the α axis creeps. (3) Years-to-t = 2: 16 years at SR 0.5, 4 at SR 1. (4) P(a SR 0.5 strategy shows a loss after 5 years) = 13%. (5) Desk question 1 worked: SR 1 over 4 years, se 0.61. (6) Forward: the trial counter (Part 26) and the sealed envelope.

**Derivation:**
$$t=\frac{\hat\mu}{\hat\sigma/\sqrt T}=\widehat{SR}_{ann}\sqrt{T_{yrs}}\Rightarrow T_{yrs}=(t/SR)^2 \quad\text{(annualise)}$$
$$\operatorname{Var}(\widehat{SR})\approx\frac{1+\tfrac12SR^2}{T}\ \ \Big(+\tfrac{\kappa-3}{4}SR^2-\gamma_3SR\Big) \quad\text{(delta method; Lo 2002, Mertens 2002)}$$
$$\operatorname{Var}(\hat\alpha)=\frac{\sigma_\varepsilon^2}{T}\Big(1+\frac{\mu_m^2}{\sigma_m^2}\Big),\quad\operatorname{Var}(\hat\beta)=\frac{\sigma_\varepsilon^2}{T\sigma_m^2} \quad\text{(}\alpha\text{ is a mean; }\beta\text{ a co-movement)}$$

**Signature visual:** the live ellipse. Its α semi-axis is labelled "a mean: needs decades"; its β semi-axis is labelled "a co-movement: needs months".

**Experiments:** `snr` and `ellipse` (existing); `ellipse_path` (new; monthly refits; < 1 min).

**Predict:** "To halve the se of α, how many more years?" (Four times as many.)

### Ch 17 · INDUSTRY: *How the research desk avoids fooling itself* + the crisis file (new `s18_industry`), 3.0 min, ~420 words

**Goal:** what firms and regulators actually do, from the public record.

**Beats (all verified unless marked):**
1. **Crisis file: F-Squared Investments (SEC, 22 Dec 2014).** F-Squared marketed its AlphaSector track record as "not backtested", for a period before the algorithm existed; an analyst had applied the buy/sell signals to the *week preceding* the ETF price changes they were based on. That is a one-week look-ahead, and it inflated the hypothetical results by about 350%; F-Squared admitted wrongdoing and paid $35 million ($30 m disgorgement, $5 m penalty). Its co-founder Howard Present was charged separately (https://www.sec.gov/news/press-release/2014-289); on screen: a toy reconstruction in the House. A seeded weekly sector-rotation rule on French daily data, run honestly and then with the signal shifted one week early. Two equity curves diverge, labelled `illustrative`.
2. **The regulator now.** The SEC Marketing Rule (Rule 206(4)-1) requires policies and procedures for hypothetical performance. On 11 Sep 2023 nine advisers settled charges for advertising hypothetical performance to the general public without them: $850,000 in total penalties (https://www.sidley.com/en/insights/newsupdates/2023/09/sec-marketing-rule-enforcement-charges-against-nine-registered-investment-advisers).
3. **Man Group.** Campbell Harvey has been Man Group's investment strategy adviser since 2005 (Man's academic advisory board page; https://www.man.com/maninstitute/academic-advisory-board); Man publishes his "Backtesting" note (Harvey and Liu, *JPM* 41(1) 2015): the common practice of halving backtested Sharpe ratios is "a serious mistake"; haircuts should come from multiple-testing adjustments and are nonlinear (https://www.man.com/insights/backtesting); Man AHL staff co-wrote "Man vs. Machine" (Harvey, Rattray, Sinclair, Van Hemert, *JPM* 43(4) 2017), which uses factor regressions to compare discretionary and systematic funds.
4. **AQR.** Two authors affiliated with AQR (Kelly, Pedersen) with Jensen: "Is There a Replication Crisis in Finance?" (*JF* 78(5) 2023). A Bayesian hierarchical model on 153 factors in 93 countries: replication rate 82.4%, against 35% in Hou–Xue–Zhang; the JF version notes the AQR affiliations (https://research-api.cbs.dk/ws/portalfiles/portal/95651880/theis_ingerslev_jensen_et_al_is_there_a_replication_crisis_in_finance_publishersversion.pdf). This is ch 12's shrinkage at industrial scale; AQR's "century of evidence" (Ilmanen, Israel, Lee, Moskowitz, Thapar, *JIM* 2021): testing factors on data *before* their discovery samples as an out-of-sample check. Factor premia persist out of sample but are muted, and timing them mostly fails after data lags and costs (https://papers.ssrn.com/abstract=3400998). This is ch 6's logic.
5. **Research Affiliates.** Arnott, Harvey and Markowitz, "A Backtesting Protocol in the Era of Machine Learning" (*JFDS* 1(1) 2019; https://papers.ssrn.com/abstract=3275654): a written protocol (prior hypothesis first, report every trial, reward research rather than results).
6. **Two Sigma.** Its Venn "Factor Lens" documentation describes a Lasso step to reduce overfitting and false positives when selecting factors **(unverified: page unreachable from this session; search snippet only)**. Omit it if it cannot be checked.
7. **The profession's own audit.** Menkveld and 163 coauthors: 164 teams, same data, same hypotheses. The dispersion of their answers ("nonstandard errors") is large and the teams underestimate it (*JF* 79(3) 2024; https://wrap.warwick.ac.uk/176566); Pérignon et al.: re-running 168 teams' own code on their own data reproduced the exact results only about half the time (*RFS* 37(11) 2024; https://papers.ssrn.com/abstract=4064172).
8. The House takeaway: the procedures map one to one onto this part's tools: a sealed hold-out (the envelope); the trial counter; clustering and HAC by default; code and data checksums (the reproducibility gate).

**Signature visual:** the F-Squared pair of equity curves, the honest and the one-week-early, diverging as a ValueTracker walks through 2001–2008, with "~350%" annotated from the SEC order; then a "defences" board: each firm's practice snaps onto the House component it corresponds to (`HouseChart` desks light).

**Experiment:** `lookahead` (new; illustrative; < 1 min).

**Predict:** "A one-week look-ahead on a weekly rotation strategy: does it add a little or a lot?" (A lot: it harvests the very move the signal was built from.)

### Ch 18 · FRONTIER: *2023–2026* (new `s19_frontier`), 3.0 min, ~420 words

Each item has a card (authors, year, venue, one-line finding) and a link back to the chapter it extends. All are verified unless marked.

1. **Goyal, Welch, Zafirov (2024)**, "A Comprehensive 2022 Look at the Empirical Performance of Equity Premium Prediction", *RFS* 37(11) 3490–3557. 29 new variables from 26 papers plus the original 17. Over a third are insignificant even in sample, and half the rest fail out of sample. → ch 6. https://www.sfi.ch/en/publications/a-comprehensive-2022-look-at-the-empirical-performance-of-equity-premium-prediction
2. **Kelly, Malamud, Zhou (2024)**, "The Virtue of Complexity in Return Prediction", *JF* 79(1) 459–503: models with more parameters than observations predict the market better. **Nagel (2025)**, "Seemingly Virtuous Complexity in Return Prediction", NBER w34104: in short windows the method is a volatility-timed momentum strategy, and it builds the same strategy on artificial data with reversals, where it fails. Narrate as an open debate. → ch 6. https://www.nber.org/papers/w34104
3. **Lazarus, Lewis, Stock (2021)**, *Econometrica* 89(5) 2497–2516: the size–power frontier of HAR tests (QS and equal-weighted periodogram on the frontier). With **LLSW (2018)**, *JBES* 36(4), it is the modern recommendation. (2021 predates the window; it is the anchor.) → ch 2. https://www.econometricsociety.org/doi/10.3982/ECTA15404
4. **Andrews, Kitagawa, McCloskey (2024)**, "Inference on Winners", *QJE* 139(1) 305–358: corrected estimates and intervals for the best of many (the best fund or the best backtest). → ch 13. https://ideas.repec.org/a/oup/qjecon/v139y2024i1p305-358..html
5. **Roth, Sant'Anna, Bilinski, Poe (2023)**, "What's Trending in Difference-in-Differences?", *J. Econometrics* 235(2) 2218–2244, with **Baker–Larcker–Wang (2022)** *JFE* 144(2) for finance. → ch 14. https://arxiv.org/abs/2201.01194
6. **Chernozhukov, Hansen, Kallus, Spindler, Syrgkanis (2024)**, *Applied Causal Inference Powered by ML and AI*, arXiv 2403.02467 (open textbook). **Maasoumi, Wang, Wang, Wu (2024)**, "Identifying factors via automatic debiased machine learning", *J. Applied Econometrics* 39(3) 438–461: about 30–50 factors with significant but declining power. → ch 15. https://ideas.repec.org/a/wly/japmet/v39y2024i3p438-461.html
7. **Menkveld et al. (2024)** *JF* 79(3) and **Pérignon et al. (2024)** *RFS* 37(11): nonstandard errors and computational reproducibility (in ch 17 as industry practice; here as the measurement of researcher degrees of freedom).
8. **Glasserman and Lin (2023)**, "Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis", arXiv 2309.17322: an LLM's training data is a new channel of look-ahead. Anonymising the firm reveals a "distraction effect". Published in *JFDS* 2024 **(unverified)**. Part 28 measures it.
9. Preview only (owned by Part 25): JKP 2023; Chen's "Most claimed statistical findings ... are likely true" (arXiv 2206.15365, working paper); Chen, Lopez-Lira, Zimmermann (arXiv 2212.10317).

**Signature visual:** a 2023–2026 strip with nine cards. Each card flies back to a thumbnail of the chapter it extends (the chapter title cards are reused as targets); for item 2: a split screen, KMZ's out-of-sample R² curve rising with complexity against Nagel's "same strategy on reversal data" panel. Both are labelled `schematic` unless reproduced. A small reproduction, random Fourier features on Shiller monthly predictors with a 12-month window, is optional (`complexity`, about 10 min); include it only if it runs within budget.

**Predict:** "A model with more parameters than months of data forecasts the market: what simple strategy might it secretly be?" (Momentum: Nagel.)

### Ch 19 · *The statistics module; recap; desk questions; problems* (merge `s08_house` + `s09_outro`), 2.5 min, ~350 words

**Beats:** (1) House rule 7. The module's new functions (list below) light up on `HouseChart`. The trial counter moves from 63 to its new count (register: `fomc`, `oos` with 5 predictors, `lookahead` (1), `twopass`). (2) Recap in 10 lines. (3) Desk questions: keep the existing three; add: "You regress 5-year returns on a persistent yield and get t = 2.5 with NW. Do you trade it?" (Size 14–18%, Stambaugh bias, R²_OS: probably not); add: "Pooled slope 0.002, FM slope 0.017: which is wrong?" (Neither: different questions; ch 4.) (4) Problems: keep the 5, add 2: derive the overlapping-return variance inflation h (exists); **new:** show that within-month pooled OLS is the dispersion-weighted FM average; **new:** show that the iid bootstrap variance of the mean is Γ̂₀. (5) Payoff card and references.

## 4. House additions (`explainer/quant/house/econ.py`; tests in `tests/test_quant_house.py`)

New functions, each tested against a simulated case with a known answer: `lrv(z, kernel="bartlett"|"qs"|"ewc", bw=None)`; `fixed_b_cv(b, kernel)`; `ols(..., se="ewc"|"hodrick", absorb=groups)` (within transform); `within_between(y, x, groups)`; `two_pass(R, F, shanken=True)`, `grs(R, F)`; `mle(negll, theta0, record=True)` (returns iterates for replay), `qmle_se`; `gmm(..., record=True)`; `oos_r2(r, x, start, ct=False)`; `augmented_predictive` (Amihud–Hurvich), `ivx`; `event_car(returns, dates, window, est_window)`, `placebo_dates`; `gibbs_hierarchical(est, se, draws, chains, seed)`; `iv_2sls`, `did_2x2`, `did_cs`, `rd_local_linear(bw)`; `iid_bootstrap`.

## 5. Compute budget (`python -m videos.quant.quant6.compute`, seeded and cached per item, about 2 CPU-hours on 4 cores)

| Item | New? | Minutes (est.) |
|---|---|---|
| ols_fwl, panel, panel_fe, twopass, ellipse, ellipse_path, snr, event, multiple, shrinkage, gmm, gmm_toy | mixed | 6 |
| overlap + hodrick | ext | 2 |
| har_size (4 ρ × 3 h × 5,000) | new | 12 |
| petersen (5 designs × 1,000) | new | 8 |
| stambaugh (+ joint pairs), ivx | ext | 4 |
| oos (5 predictors) | new | 3 |
| mle (+ iterates, T-scaling) | new | 2 |
| gmm_surface, gmm_mc (400 economies) | new | 12 |
| fomc (+ 10,000 placebos), lookahead | new | 3 |
| bootstrap, boot_coverage (300 paths × 400 × 3, resumable per path) | ext/new | 25 |
| gibbs (4 × 5,000) | new | 2 |
| fdr_sim (200 seeds) | new | 2 |
| designs (IV, DiD, staggered, RD × 200) | new | 6 |
| dml, dml_lambda (λ grid × 5 seeds) | ext/new | 10 |
| complexity (optional RFF reproduction) | new | 10 |
| envelope (register new tests) | ext | <1 |
| **Total** | | **≈ 107–117** |

Long items (`boot_coverage`, `gmm_mc`, `har_size`, `petersen`) checkpoint partial results under `.cache/quant6/` and resume. Data needed beyond the cache: none, except `fomc_dates.py` (transcribed from federalreserve.gov). All other inputs are already cached: French factors (daily and monthly), 49 industries, B/M deciles, FRED PCE and CPI, and Shiller.

## 6. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 6 · Financial Econometrics (~58; 20 chapters)
1. Regression in finance: OLS as projection, Frisch–Waugh–Lovell, the sandwich; overlapping observations and HAC
   errors (Newey–West 1987, Hansen–Hodrick 1980, Hodrick 1992); fixed-b and EWC (Kiefer–Vogelsang 2005; Lazarus,
   Lewis, Stock and Watson 2018); clustered errors.
2. Predictive regressions: the Stambaugh bias (1999) derived; IVX (Kostakis–Magdalinos–Stamatogiannis 2015); out
   of sample (Welch–Goyal 2008; Campbell–Thompson 2008; Goyal–Welch–Zafirov 2024).
3. MLE (information, QMLE) and GMM (Hansen 1982): the geometry, efficiency, the J test; the Euler equation estimated
   (Hansen–Singleton 1982), weakly identified and rejected.
4. Event studies: market model, CARs and their variance, event clustering (FFJR 1969; MacKinlay 1997); the turn of
   the month and FOMC days, measured.
5. Panel methods: clustering (Petersen 2009); Fama–MacBeth vs pooled vs fixed effects, within and between; the
   two-pass CAPM test and Shanken's correction.
6. Bootstrap for dependent data: block (Künsch 1989) and stationary (Politis–Romano 1994); coverage measured.
7. Bayesian inference: priors as shrinkage; James–Stein; a hierarchical model for many assets, sampled by Gibbs.
8. Multiple testing, previewed: FWER, Holm, FDR (Benjamini–Hochberg 1995), proved; to Parts 25–26.
9. Causal inference: instruments, differences-in-differences (and the staggered-adoption trap), regression
   discontinuity (Russell cutoffs); double/debiased ML (Chernozhukov et al. 2018), orthogonality derived.
10. The signal-to-noise problem: how many years to tell a Sharpe of 0.5 from 0.

*Textbooks:* CLM ch. 2, 4, 8 and App. A; Cochrane *Asset Pricing* part II (ch. 10–16); Hayashi ch. 1–8; Greene
(GMM, MLE, panels, DiD, bootstrap, Bayes); Bali–Engle–Murray part I; Tsay ch. 12 (MCMC).
*Computed/Trained:* HAC, fixed-b and EWC sizes in null worlds; Petersen's simulation; Fama–MacBeth on 49
industries and the flat two-pass SML; Stambaugh's bias as a tilted cloud; Goyal–Welch out of sample on Shiller;
Student-t MLE replayed; GMM surface and Monte Carlo for the Euler equation; FOMC and turn-of-month event studies
with placebos; bootstrap coverage; Gibbs-sampled industry alphas; BH on a planted world; IV/DiD/RD with planted
effects; double ML across seeds and penalties; the years-to-significance curve.
*Visuals:* the HAC window sliding over autocovariances; cross-sections stacking into a time series of slopes; the
Stambaugh cloud tilting; the GMM ellipse touching the moment curve; event paths sliding into event time; blocks cut
and reshuffled; alphas on springs; the BH line rotating; the (α, β) ellipse shrinking as months arrive.
*Labs:* `econ.ols` + HAC meat; `econ.fama_macbeth`; `econ.gmm`; `econ.stationary_bootstrap`;
`econ.benjamini_hochberg`; `econ.dml_plr`.
*Crisis:* F-Squared (SEC 2014): a backtest a week early, marketed as a track record.
*Firms:* Man Group (Harvey's haircuts), AQR (replication, a century of evidence), Research Affiliates (the backtest
protocol); the SEC Marketing Rule; nonstandard errors and reproducibility (Menkveld et al. 2024; Pérignon et al.
2024).
*Frontier:* Goyal–Welch–Zafirov 2024; Kelly–Malamud–Zhou 2024 vs Nagel 2025; inference on winners (Andrews–
Kitagawa–McCloskey 2024); DiD (Roth et al. 2023); automatic debiased ML for factors (Maasoumi et al. 2024); LLM
look-ahead (Glasserman–Lin 2023).
*Desk:* "A strategy has Sharpe 1 over 4 years. What is the standard error?"; "Pooled slope 0.002, Fama–MacBeth
0.017: which is wrong?"; "Twenty strategies, the best p = 0.03: significant?"
*House:* the statistics module (HAC/EWC, clustering, Fama–MacBeth and two-pass, MLE/GMM, event studies,
bootstraps, Gibbs, FDR, causal designs, double ML).
```

## 7. Minutes per chapter

Minutes (words at 140 wpm = minutes × 140): 0 Hook + era 3.0; 1 Least squares as geometry 2.5; 2 Newey–West (+ fixed-b, EWC) 3.5; 3 Clustering 2.5; 4 Fama–MacBeth, verdicts resolved 3.5; 5 Stambaugh's bias 3.0; 6 Out of sample 2.5; 7 Maximum likelihood 3.0; 8 GMM geometry 3.0; 9 Euler equation 2.5; 10 Event studies 3.0; 11 Bootstrap 3.0; 12 Shrinkage and Bayes 3.0; 13 Many tests 3.0; 14 Causal designs 3.0; 15 Double ML 3.0; 16 How many years 2.5; 17 Industry + crisis 3.0; 18 Frontier 3.0; 19 House + outro 2.5. **Total 58 min, ≈ 8,120 words.**

Target `lecture_length.py quant6 --floor 50` at about 8,120 narration words (58 min at the part's measured 140 wpm). The floor leaves 8 minutes of slack; if it runs long, trim ch 2 and ch 4 to 3.0 before touching the labs.

## 8. Implementation notes

- **Scenes to keep and extend:** `s01_hook` (add the sixth bar and the era strip); `s02_overlap` → ch 2 and 5; `s03_gmm` → ch 8 and 9; `s04_event` → ch 10 (event part), its panel half → ch 4; `s05_sharpe` → ch 11 and 16; `s06_many` → ch 12 and 13; `s07_causal` → ch 14 and 15; `s08_house` + `s09_outro` → ch 19.
- Renaming scene modules invalidates the caches (CLAUDE.md). Keep the module names where a chapter continues, or accept a re-render.
- **Fix the hook and panel narration** per §1: within against between. Do not claim the 8× gap is only dispersion weighting.
- **Every new on-screen string** goes into `quant_text_zh.json`, with `narration_zh.json` lines. Glossary terms: 长期方差 (long-run variance), 固定b渐近 (fixed-b asymptotics), 聚类标准误 (clustered standard errors), 组内/组间 (within/between), 两步法 (two-pass), 弱识别 (weak identification), 事件研究 (event study), 累计异常收益 (CAR), 平稳自助法 (stationary bootstrap), 吉布斯抽样 (Gibbs sampling), 错误发现率 (FDR), 交错双重差分 (staggered DiD), 断点回归 (RD), 双重机器学习 (DML), 前视偏差 (look-ahead bias).
- **Chinese edition material:** A-share event study on CSRC/PBoC announcement days using `yahoo_daily("510500.SS")` (cached; CSI 500 ETF). One beat in ch 10 for the zh edition; the dates need transcription **(unverified availability)**.

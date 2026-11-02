# Quant, Built — Part 7: Time Series and Volatility

Part 7 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act II, the Mathematical Toolkit. Returns are nearly unpredictable; their size is
not. This part is a lecture course on the models that forecast it, from Yule's autoregression to time-series
foundation models, with every model fitted or trained on screen and judged out of sample.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`vol`](../../../explainer/quant/house/vol.py) module, tested in `tests/test_quant_house.py`) from public data:
Kenneth French's daily and monthly market returns and size deciles, FRED's Treasury yields (DTB3, DGS5, DGS10) and
VIX (VIXCLS), and Binance's one-minute, daily and perpetual-futures prices for Bitcoin. Simulations are seeded and
labeled on screen. Published results we did not run (the foundation-model comparison) are labeled as data from the
paper.

*An education in methods, not investment advice.*

## Chapters (about 59 minutes)

* **The river under the noise.** A century of the US market's daily moves, clusters lighting up (1929–33, 1987,
  2008, 2020); pause and predict: sign or size? The autocorrelation of returns is 0.05 at lag 1 and nothing after;
  of absolute returns 0.31 at lag 1, still 0.14 at lag 100 and 0.12 at lag 250 (24,896 days). Bitcoin's river drawn
  live by a Kalman filter. History: Yule 1927, Kalman 1960, Box–Jenkins 1970, Dickey–Fuller 1979, Engle 1982,
  Bollerslev 1986, Engle–Granger 1987, Hamilton 1989, RiskMetrics 1994, the 2003 Nobel, Corsi 2009, roughness 2018,
  foundation models 2024. Objectives; the House.
* **1. Stationarity, ARMA and Box–Jenkins.** An AR(1) on a slider (φ = 0 → 0.99) with its ACF and variance; weak
  stationarity; the derivation (MA(∞) form, variance, ACF, forecast and half-life, Ljung–Box); Wold; ACF/PACF
  fingerprints; the identify–estimate–check loop. **Lab:** `ar_fit` on log VIX 1990–2020 (7,810 days): φ = 0.982,
  half-life 39 days; AIC picks ARMA(2,1), whose residuals still fail Ljung–Box (Q₂₀ = 43): long memory. Ljung–Box
  on 94 years of returns: Q = 179; on squared returns Q = 14,593.
* **2. Unit roots and spurious regression.** Sixty stationary paths in a band against sixty random walks in a √t
  funnel. 20,000 simulated Dickey–Fuller t-statistics stream into a histogram left of N(0,1): mean −1.54, 46% below
  −1.645, 5% point −2.89. The limit derived (telescoping, Donsker, continuous mapping; P(W(1)² < 1) = 0.68).
  **Lab:** `adf` (5 lags): Bitcoin's log price t = −0.93, the US log index 0.64, the 10-year yield −1.03 (a unit root
  in practice), log VIX −6.48 (rejects). Granger–Newbold: 89% false rejections in levels, 5% in differences, median
  R² 0.17; Phillips (1986): median |t| grows from 3.0 at T = 50 to 20.1 at T = 2,000. Bitcoin on the US market: t = 24
  in levels, 6.7 in changes.
* **3. Cointegration.** Murray's (1994) drunk and her dog, simulated: ADF −0.95 on her position, −11.5 on the gap.
  Bitcoin spot and perpetual, 2020: ADF 0.96 and 0.94; Engle–Granger t = −7.2 (5%: −3.34); the basis is AR(1) with
  ρ = 0.55, half-life 1.2 days. ECM, Granger representation, the EG critical value, the VECM and Johansen's trace
  statistic derived. **3D:** daily 3-month, 5-year and 10-year yields 1990–2020 as a cloud seen edge-on: principal
  axes 95.2%, 4.7% and 0.15% of the variance; trace statistics 68.0, 8.0, 2.0 against 29.8, 15.5, 3.8: rank 1, two
  common trends, the leash a curvature-like combination (−0.36, 1, −0.74).
* **4. Hidden regimes.** Hamilton's filter as two jars of belief, predicted and updated month by month through 1929,
  then over the century; the filter, durations and stationary share derived. EM replay: the log-likelihood converges
  within five iterations. Calm +12%/13%/55 months, storm −15%/36%/10 months, 16% of the time in the storm. Pause:
  one −8% month moves the storm probability from 0.02 to 0.09.
* **5. The Kalman filter and stochastic volatility.** The belief bell: predict (widen), observe, update (product of
  bells, gain K). Derivation by completing the square; the steady-state gain K(q/r); Bitcoin q/r = 0.38, K = 0.45.
  **Lab:** `kalman_states`, the river redrawn with its band. Stochastic volatility by QML (Harvey–Ruiz–Shephard
  1994) on 94 years: φ = 0.992, σ_η = 0.125, half-life 88 days; correlation with GARCH volatility 0.88.
* **6. ARCH and GARCH by maximum likelihood.** Engle 1982; the leaky bucket (tap ω, leak 1 − β, splash αr²) simulated
  with US parameters; the long-run level, the EWMA unrolling, the likelihood, the term structure, GARCH as ARMA(1,1)
  for r², derived. **Lab:** `garch_filter` and its likelihood: α = 0.105, β = 0.884, log L 84,088, half-life 63
  days. **3D replay:** the variance-targeted likelihood surface over (α, β), a simplex search climbing the ridge in
  66 iterations to (0.104, 0.884); EWMA at the edge α + β = 1.
* **7. The GARCH zoo.** The (α, β) plane: the covariance-stationary triangle and Nelson's (1990) strict-stationarity
  boundary beyond it; pause: α + β = 1.05 both times, E ln(αz² + β) = −0.0074 (0.30, 0.75: stationary) and
  +0.0084 (0.25, 0.80: explosive). Derived: the unrolled product, the LLN argument, Jensen (IGARCH strictly
  stationary), the QMLE score. News-impact curves morph GARCH → GJR (a fall raises variance 4× a rise; log L 84,336)
  → EGARCH (84,342); Bitcoin γ = 0.14. Fat tails: GARCH residuals' kurtosis 7.8; Student-t ν = 5.6, log L +911.
* **8. Correlations that move.** One stock–bond covariance ellipse per year 1962–2020, breathing and tilting, with a
  correlation dial. VEC 51 million, BEKK 25,050, DCC 302 parameters for 100 assets; the DCC recursion and two-step
  likelihood; a = 0.029, b = 0.969; EWMA overlay. Pause: a 60/40 model assuming ρ = +0.3 in 2010 said 12.5%; the
  correlation was −0.49 and the portfolio's volatility 9.9%.
* **9. Realized volatility.** One wild Bitcoin day (26 June 2019) cut into squares at 30, 10, 5 and 1 minutes. The
  signature plot built point by point: in 2019, 1-minute RV reads 1.6% more than 5-minute; over the whole sample, 10%.
  Derived: RV → IV, the BNS CLT, the noise bias 2nη², Bandi–Russell's n* (median Δ* ≈ 9 minutes), TSRV, realized
  kernel. Averages: 106% (1-min), 96% (5-min), 93% (TSRV and kernel), 92% (bipower); the daily CLT band.
* **10. Jumps and HAR.** Squares against bipower rectangles; the BNS (2006) ratio test: 27% of days jump at 1%, 16%
  at 0.1%; 12 March 2020 has z = 0.05: a storm, not a jump. HAR as an AR(22) staircase against GARCH's geometric
  weights; the ACF of log RV against the simulated log-HAR and an AR(1). **Lab:** `har_fit`: b_d 0.41, b_w 0.03,
  b_m 0.43, R² 0.38; the rolling-year replay (the week and month trade places). HARQ attenuation derived; b_q = −3.0
  (t −0.7); HAR-CJ jump coefficient 1.50; log-HAR.
* **11. Is volatility rough?** fBm with H = 0.1 and 0.5, zoomed twice. **Lab:** `log_rv_scaling` recovers H = 0.11
  and 0.50 on simulated paths; Bitcoin's log RV gives H = 0.13. The RFSV predictor's power-law kernel; HAR as its
  cheap approximation; Part 14 builds the models.
* **12. Scoring forecasts honestly.** Hansen–Lunde. Expected-loss curves as the proxy gets noisier: QLIKE's minimum
  stays at the truth, MSE on volatility slides to 0.64 (Patton 2011, proved). Simulation (200 runs × 2,500 days):
  QLIKE and MSE on variance pick the truth under every proxy; MSE and MAE on volatility pick 0.8 × truth against
  squared returns. **Lab:** `qlike`, `diebold_mariano`; Mincer–Zarnowitz slopes (HAR 0.98, log-HAR 1.35). The model
  confidence set (Hansen–Lunde–Nason 2011): at 90% all nine survive; at 75% EWMA, HAR and GARCH drop out.
* **13. Training the networks.** LSTM, transformer and HARNet (Reisenhofer–Bayer–Hautsch 2022, initialised at
  log-HAR): 1,233, 2,625 and 111 parameters. Training replays with five-seed bands and the validation forecasts at
  epochs 0, 5, 10, 20, 40 and best; seed spreads (LSTM 0.366–0.378, transformer 0.401–0.433, HARNet 0.359–0.362);
  HARNet starts at validation loss 0.272 and ends at 0.270.
* **14. The race.** Train to June 2019, validate H2 2019, test 2020. A live leaderboard: EWMA leads until 11 March,
  12 March reshuffles everything. QLIKE: HARNet 0.360, log-HAR 0.363, LSTM 0.371, transformer 0.410, HARQ 0.426, HAR
  0.427, GJR 0.444, GARCH 0.452, EWMA 0.512; DM t against log-HAR: HARNet −0.99, LSTM +1.46. On MSE, GJR first. The
  2020 overlay.
* **15. Foundation models and the frontier.** Chronos's tokenisation drawn; a toy Chronos-style model trained here on 3,000 synthetic volatility series (128 bins, context 64, a 42,176-parameter numpy network, 3 seeds, replayed) and run zero-shot on Bitcoin 2020: QLIKE 0.416 against log-HAR's 0.363 (DM t = +1.7, within noise; between HAR and the transformer), its 10–90% fan covering 85% of days.
  Brini (2026), Table 6, h = 1, as published: TTM 0.982, HAR 0.998, Sundial 0.998, log-HAR 1.000, ARMA 1.000,
  Moirai-2.0-S 1.038, TimesFM-2.5 1.086, Moirai-MoE-S 1.090, Chronos-Bolt-S 1.110, Chronos-Bolt-B 1.121, Toto 1.214,
  Lag-Llama 1.532. The 2022–2026 papers.
* **16. March 2020.** The crisis file; every model's forecast for 12 March (62–76%) against 457%; the weeks
  around it; √T against GARCH's term structure (85% next day, 52% over a year, 18% long run).
* **17. Industry.** RiskMetrics (λ = 0.94 daily, 0.97 monthly; MSCI's 2010 acquisition): our λ grid on the US market
  1990–2020, RMSE best at the grid edge 0.85, QLIKE at 0.94. Barra USE4's longer correlation half-life and
  volatility regime adjustment (MSCI's words); our replica on ten size deciles peaks at 2.1 (1929–33), 2.7 (1987),
  2.2 (2020); QLIKE 1.70 → 1.66. Volatility targeting (Harvey et al. 2018; MOP 2012's 40% target and 60-day centre
  of mass): on the US market 1927–2020 at 10%, Sharpe 0.44 → 0.58, worst-1% mean −2.78% → −2.55%, max drawdown (log)
  1.04 → 0.67. The VIX above next-month realized on 85% of days (by 4.1 points); R² 0.52 (VIX), 0.50 (GARCH); both
  significant together (t 7.2 and 3.2).
* **18. The volatility forecaster.** The module table; Rule 8; eleven models registered in this part, the series' trial
  counter as read at build time. **Lab:** `forecast` on 31 Dec 2020: Bitcoin 91% tomorrow, 84% over 22 days; the US term structure
  9.1% (1 day) → 15.3% (1 year), long run 17.6%.
* **Recap, four desk questions, six problems, payoffs, references.**

## Textbook audit

| Book / section | Chapter |
|---|---|
| Tsay, *Analysis of Financial Time Series* (3e) ch. 1 (stylized facts) | Hook, 1 |
| Tsay ch. 2 (ACF, AR/MA/ARMA, Ljung–Box, unit roots; long memory) | 1, 2; long memory in 10 |
| Tsay ch. 3 (ARCH, GARCH, IGARCH, GARCH-M, EGARCH, TGARCH, SV) | 6, 7; SV in 5; GARCH-M named in 7 (Part 23) |
| Tsay ch. 4 (nonlinear: TAR, STAR, Markov switching, neural networks) | 4; networks in 13; TAR/STAR → Part 27 |
| Tsay ch. 5 (high-frequency: bid–ask bounce, nonsynchronous trading, durations) | 9; durations → Part 36 |
| Tsay ch. 7 (extreme values, VaR) | → Part 40 (said in 16) |
| Tsay ch. 8 (VAR, cointegration, ECM, pairs) | 3; pairs → Part 33 |
| Tsay ch. 10 (multivariate volatility: EWMA, BEKK, DCC) | 8 |
| Tsay ch. 11 (state space, Kalman filter and smoother) | 5 |
| Tsay ch. 12 (MCMC for SV) | named in 5 (QML used); Bayesian methods → Part 6 |
| Hamilton, *Time Series Analysis*, ch. 3–5 (ARMA, forecasting, MLE) | 1, 6 |
| Hamilton ch. 6 (spectral analysis) | named in 1 (same information in frequency); not used |
| Hamilton ch. 10–11 (VARs) | 3 (VECM); impulse responses → Part 32 |
| Hamilton ch. 13 (Kalman filter) | 5 |
| Hamilton ch. 15–17 (unit roots, functional CLT, DF asymptotics) | 2 |
| Hamilton ch. 18–20 (multivariate unit roots, cointegration, Johansen FIML) | 3 |
| Hamilton ch. 21 (ARCH/GARCH) | 6, 7 |
| Hamilton ch. 22 (regime switching) | 4 |
| Brockwell–Davis, *Introduction to Time Series and Forecasting* (stationarity, ARMA, forecasting; ARIMA; GARCH/SV; state space) | 1, 2, 6, 5 |
| Francq–Zakoian, *GARCH Models* (stationarity; EGARCH/GJR; QMLE; multivariate GARCH) | 7, 8 |
| Aït-Sahalia–Jacod, *High-Frequency Financial Econometrics* (IV without noise and its CLT; noise; jump tests) | 9, 10; spot volatility and irregular sampling named in 9; activity index → Part 13 |
| Andersen, Bollerslev, Christoffersen and Diebold (2006), "Volatility and correlation forecasting", *Handbook of Economic Forecasting* | 6–12, 17 |
| Campbell–Lo–MacKinlay ch. 12 (changing volatility, ANNs, data snooping) | 6, 13, 12 |
| McNeil–Frey–Embrechts, *QRM*, financial time series (stylized facts, GARCH, EWMA; filtered historical simulation) | Hook, 6, 17; FHS → Part 40 |

## Reading guide

Classics: Yule (1927); Kalman (1960); Box and Jenkins (1970); Granger and Newbold (1974); Ljung and Box (1978);
Dickey and Fuller (1979); Engle (1982); Bollerslev (1986, 1987); Phillips (1986); Engle and Granger (1987); Engle,
Lilien and Robins (1987); Hamilton (1989); Nelson (1990, 1991); Johansen (1991); Bollerslev and Wooldridge (1992);
Hall, Anderson and Granger (1992); Glosten, Jagannathan and Runkle (1993); Engle and Ng (1993); Murray (1994), "A
drunk and her dog: an illustration of cointegration and error correction", *The American Statistician* 48(1):37–39;
Harvey, Ruiz and Shephard (1994); Diebold and Mariano (1995); J.P. Morgan/Reuters, *RiskMetrics Technical Document*
(4th ed., 1996). Realized volatility: Andersen, Bollerslev, Diebold and Labys (2000, 2003); Barndorff-Nielsen and
Shephard (2002, 2004, 2006); Zhang, Mykland and Aït-Sahalia (2005); Andersen, Bollerslev and Diebold (2007);
Bandi and Russell (2008); Barndorff-Nielsen, Hansen, Lunde and Shephard (2008); Corsi (2009). Evaluation:
Mincer and Zarnowitz (1969); Hansen and Lunde (2005); Patton (2011); Hansen, Lunde and Nason (2011); Bollerslev,
Patton and Quaedvlieg (2016). Roughness: Gatheral, Jaisson and Rosenbaum (2018). Industry: Moskowitz, Ooi and
Pedersen (2012), *JFE* (40% ex-ante volatility per position, 60-day centre of mass, verified in the paper); Moreira and
Muir (2017); Harvey, Hoyle, Korgaonkar, Rattray, Sargaison and Van Hemert (2018), *JPM*; Bollerslev, Hood, Huss and
Pedersen (2018), *RFS*; Carr and Wu (2009); Christensen and Prabhala (1998); MSCI, "Market Factor: Not Just For Show"
(Dec. 2011). Frontier: Zhang, Zhang, Cucuringu and Qian (2022); Reisenhofer, Bayer and Hautsch (2022); Christensen,
Siggaard and Veliyev (2023), *JFEc* 21(5); Ansari et al. (2024, Chronos; 2025, Chronos-2); Das et al. (2024,
TimesFM); Woo et al. (2024, Moirai); Ekambaram et al. (2024, TTM); Goel, Pasricha, Magris and Kanniainen (2025);
Rahimikia, Ni and Wang (2025); Shi et al. (2025, Kronos); Brini (2026), arXiv 2607.05291.

## Build it

```bash
python -m videos.quant.quant7.compute                    # every number, cached in .cache/quant7/ (resumable)
EXPLAINER_TTS=silent python tools/qa_scene.py quant7 Race     # one chapter, silent, with a contact sheet
python tools/make.py quant7 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

Compute: about 25 CPU-minutes in all (networks about 4 minutes on one thread; the toy foundation model about 6, in numpy, because on the shared build machine the PyTorch version was repeatedly killed for memory).
Training uses one thread on purpose: with renders running, PyTorch's default thread pool was measured forty times
slower. The network runs are cached one file per seed in `.cache/quant7/training_runs/`.

**What a production run with the real foundation models would add.** Chronos-Bolt, TimesFM 2.5, TTM-r2 and Moirai
were not installed in this environment (and installing them was not possible here), so chapter 15 shows the published
comparison (Brini 2026) and a toy model of the same design trained here. A production run would add their zero-shot
forecasts of Bitcoin's 2020 realized variance from the same 2017–2019 context, scored by the same QLIKE, DM, MZ and MCS
as the race, with model revisions and weight hashes recorded, and a check that their pretraining corpora exclude 2020
market data (the leakage caveat on screen).

## Desk questions, with solutions

1. **Daily volatility is 1%.** With independent returns and constant variance, variances add: over a week
   1% × √5 ≈ 2.2%, over a year 1% × √252 ≈ 15.9%. The rule fails in three ways. Volatility mean-reverts, so from a
   high level the average over a horizon is lower than today's level (GARCH: E_t[σ²_{t+h}] = σ̄² +
   (α + β)^{h−1}(σ²_{t+1} − σ̄²)); chapter 16 shows 85% falling to 52% over a year. Autocorrelated returns change the
   sum's variance by the factor 1 + 2Σ(1 − k/h)ρ_k (Lo–MacKinlay's variance ratio). And quantiles of fat-tailed
   returns do not scale by √T, because the sum of fat-tailed returns is closer to normal than each one.
2. **A t of 24 between two prices.** First check both series for unit roots (ADF). If both have one, the t-statistic
   is meaningless (chapter 2: 89% false rejections, and it grows like √T). Test the residual of the levels regression
   with Engle–Granger critical values (about −3.34 at 5% for two series, not −2.86), or regress changes on changes.
3. **A model beats GARCH on MSE over a year with a crash in it.** Squared errors of variance forecasts are dominated
   by the largest days, so one day can decide the race. Score with QLIKE, which is robust to noise in the realized
   proxy (Patton 2011), compare against HAR rather than a weak benchmark, use a Diebold–Mariano test with a HAC
   variance and a model confidence set, and check that the ranking survives without the crisis weeks.
4. **A GARCH fit gives α + β = 1. Is the process stationary?** Not covariance-stationary: the unconditional variance
   ω/(1 − α − β) is infinite. But it is strictly stationary: unrolling gives σ_t² = ω Σ_k Π_{j≤k}(αz²_{t−j} + β),
   which converges when E ln(αz² + β) < 0 (Nelson 1990), and by Jensen E ln(αz² + β) < ln E(αz² + β) = ln(α + β) = 0.
   Forecasts of the variance never revert (the RiskMetrics EWMA is this case with ω = 0).

## Problems, with solutions

1. **GARCH's term structure.** Write σ̄² = ω/(1 − α − β). Since E_t[r²_{t+k}] = E_t[σ²_{t+k}], taking expectations of
   σ²_{t+k+1} − σ̄² = α(r²_{t+k} − σ̄²) + β(σ²_{t+k} − σ̄²) gives E_t[σ²_{t+k+1}] − σ̄² = (α + β)(E_t[σ²_{t+k}] − σ̄²),
   and by induction E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²). A shock halves after log 0.5/log(α + β)
   days: 63 days for the US market's 0.989.
2. **GARCH as ARMA, and its kurtosis.** Let ν_t = r_t² − σ_t², a martingale difference. Substituting σ_t² = r_t² − ν_t
   into the GARCH recursion gives r_t² = ω + (α + β)r²_{t−1} + ν_t − βν_{t−1}: an ARMA(1, 1) with autoregressive root
   α + β. With normal shocks, E[r⁴] = 3E[σ⁴]. Taking expectations of the squared recursion gives
   E[σ⁴](1 − (α + β)² − 2α²) = ω² + 2ωσ̄²(α + β), and the kurtosis is 3(1 − (α + β)²)/(1 − (α + β)² − 2α²). This
   exceeds 3 whenever α > 0, and is finite only if (α + β)² + 2α² < 1.
3. **Noise in realized variance, and the optimal sampling rate.** If observed log prices are p_i = p*_i + u_i with
   iid noise of variance η², observed returns are r_i = r*_i + u_i − u_{i−1}, and E[Σr_i²] = ∫σ²dt + 2nη²: the bias
   grows with n (the signature plot). The estimation error of RV without noise has variance 2IQ/n (BNS). The mean
   squared error is about (2nη²)² + 2IQ/n = 4n²η⁴ + 2IQ/n; setting its derivative 8nη⁴ − 2IQ/n² to zero gives
   n* = (IQ/(4η⁴))^{1/3} (Bandi and Russell 2008). Two-scale RV removes the bias instead: it averages K sparse grids
   (bias 2n̄η² each) and subtracts (n̄/n)RV_all, converging at rate n^{−1/6}.
4. **QLIKE.** E[h/ĥ − log(h/ĥ) − 1 | F] = E[h|F]/ĥ + log ĥ − E[log h | F] − 1. Its derivative in ĥ is
   −E[h|F]/ĥ² + 1/ĥ, which is zero only at ĥ = E[h|F], and the function is convex there. The loss depends on h only
   through E[h|F] plus a term free of ĥ, so an unbiased proxy (E[h̃|F] = E[h|F]) adds the same constant to every
   forecast's expected loss and preserves the ranking (Patton 2011). For MSE on volatility, argmin E(√h̃ − σ̂)² =
   E√h̃ < √E h̃ by Jensen: with a squared return as the proxy, the minimiser is (2/π)h ≈ 0.64h.
5. **The Kalman gain.** For x_t = x_{t−1} + w_t and y_t = x_t + v_t, with variances Q and R, the filter predicts
   P⁻ = P + Q, uses the gain K = P⁻/(P⁻ + R), and updates P = (1 − K)P⁻. In steady state KP⁻ = Q, and P⁻ solves
   P⁻² − QP⁻ − QR = 0. Dividing by R² and writing q = Q/R gives p = P⁻/R = (q + √(q² + 4q))/2 and K = p/(p + 1),
   a function of q alone. For Bitcoin's q = 0.38, K ≈ 0.45.
6. **The Dickey–Fuller limit.** With x_t = x_{t−1} + ε_t and x_0 = 0, squaring gives x_t² = x²_{t−1} + 2x_{t−1}ε_t + ε_t²,
   so Σx_{t−1}ε_t = ½(x_T² − Σε_t²). By Donsker, T^{−1/2}x_{⌊rT⌋} ⇒ σW(r), hence T^{−1}Σx_{t−1}ε_t ⇒ ½σ²(W(1)² − 1)
   and T^{−2}Σx²_{t−1} ⇒ σ²∫₀¹W(r)²dr; by continuous mapping T(ρ̂ − 1) ⇒ ½(W(1)² − 1)/∫W². Since W(1) ~ N(0, 1),
   P(W(1)² < 1) = P(|Z| < 1) ≈ 0.683, so the numerator is negative two times out of three and the distribution is
   skewed left (chapter 2's simulation: 5% point −2.89 with a constant).

## Data and reproducibility

* Binance (data.binance.vision): BTCUSDT one-minute and daily spot candles, August 2017 to December 2020, and the
  USD-M perpetual's daily closes for 2020. Every downloaded file is checksummed in
  [`../data/manifest.json`](../data/manifest.json).
* Kenneth French's daily market and size-decile returns and monthly factors, 1926–2020; FRED DTB3, DGS5, DGS10 and
  VIXCLS. The hold-out from 2021 is sealed.
* Registered with the trial counter before scoring: the forecasting race (8 models; log-HAR added after the first
  results and counted), HARNet (1) and the toy foundation model (2: a PyTorch version registered first and never scored, then the numpy version that was).
* Facts checked for this expansion: Murray (1994) is *The American Statistician* 48(1):37–39 (Crossref); Moskowitz,
  Ooi and Pedersen's 40% target and 60-day centre of mass (the *JFE* paper's text); MSCI's descriptions of USE4's
  half-lives and volatility regime adjustment (MSCI, Dec. 2011). Dropped as unverifiable here: the exact USE4
  regime-adjustment formula and half-lives (our replica is labeled as ours), and the Basel 1996 amendment's √10 text
  (the BIS document could not be retrieved; the chapter states only the mathematics).

---

# 量化金融，从零搭建 — 第7部分：时间序列与波动率

收益几乎无法预测，但收益的大小可以。本部分是一门关于预测它的模型的课程，从尤尔的自回归一直讲到时间序列基础模型；每个模型都在屏幕上拟合或训练，
并在样本外接受评判。所有数字都由本系列自己的代码根据公开数据算出；没有运行、直接引用的结果（基础模型的比较）标注为论文数据。

*讲的是方法，不构成投资建议。*

## 章节（约59分钟）

开场（波动聚集、收益与绝对收益的自相关、卡尔曼河流、历史）；1. 平稳性、ARMA与博克斯–詹金斯方法；2. 单位根与伪回归；3. 协整（醉汉与狗、
比特币基差、三维国债收益率的约翰森检验）；4. 隐藏机制；5. 卡尔曼滤波与随机波动率；6. 用最大似然估计ARCH与GARCH（漏水桶、三维似然面）；
7. GARCH家族（纳尔逊平稳性边界、新闻冲击曲线、学生t）；8. 会变的相关性（DCC）；9. 已实现波动率（签名图、噪声、最优采样）；10. 跳跃与HAR；
11. 波动率是粗糙的吗？；12. 诚实地给预测评分（QLIKE、DM、MZ、模型置信集）；13. 训练神经网络；14. 竞赛；15. 基础模型与前沿；16. 2020年3月；
17. 业界（RiskMetrics、Barra、波动率目标、VIX）；18. 波动率预测器；回顾、交易台问题与习题。各章数字见上面英文部分。

## 教材对照

见上面英文部分的表格：Tsay第1–5、7、8、10–12章，Hamilton第3–6、10–11、13、15–22章，Brockwell–Davis，Francq–Zakoian，
Aït-Sahalia–Jacod，Andersen等（2006）手册章节，CLM第12章，QRM，均对应到本部分的章节或本系列的其他部分。

## 交易台问题与解答

1. **日波动率为1%。** 若收益独立且方差恒定，方差可加：一周1% × √5 ≈ 2.2%，一年1% × √252 ≈ 15.9%。这个法则有三种失效方式。
   第一，波动率均值回归，从高位出发，一段期限内的平均低于今天的水平（GARCH：E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²)），
   第16章中85%在一年里降到52%。第二，收益自相关时，总和的方差会乘以1 + 2Σ(1 − k/h)ρ_k（Lo–MacKinlay方差比）。第三，厚尾收益的分位数不按√T缩放，
   因为厚尾收益之和比单个收益更接近正态。
2. **两个价格之间t = 24。** 先检验两个序列有没有单位根（ADF）。如果都有，这个t统计量没有意义（第2章：89%的错误拒绝，而且按√T增长）。
   对水平回归的残差做单位根检验，用恩格尔–格兰杰临界值（两个序列时5%水平约−3.34，而不是−2.86），或者用变化量对变化量回归。
3. **一个模型在包含崩盘的一年里按MSE胜过GARCH。** 方差预测的平方误差由最大的几天主导，一天就可能决定胜负。应当用QLIKE评分，
   它对已实现代理变量中的噪声稳健（Patton 2011）；对比HAR而不是弱基准；用带HAC方差的Diebold–Mariano检验和模型置信集；并检查去掉危机几周后排名是否依然成立。
4. **GARCH拟合得到α + β = 1。过程平稳吗？** 不是协方差平稳的：无条件方差ω/(1 − α − β)为无穷。但它是严平稳的：展开得
   σ_t² = ω Σ_k Π_{j≤k}(αz²_{t−j} + β)，当E ln(αz² + β) < 0时收敛（Nelson 1990），而由詹森不等式E ln(αz² + β) < ln E(αz² + β) = ln(α + β) = 0。
   方差预测永远不回归（RiskMetrics的EWMA就是ω = 0的这种情形）。

## 习题与解答

1. **GARCH的期限结构。** 记σ̄² = ω/(1 − α − β)。由于E_t[r²_{t+k}] = E_t[σ²_{t+k}]，对σ²_{t+k+1} − σ̄² = α(r²_{t+k} − σ̄²) + β(σ²_{t+k} − σ̄²)
   取期望，得E_t[σ²_{t+k+1}] − σ̄² = (α + β)(E_t[σ²_{t+k}] − σ̄²)，归纳得E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²)。
   冲击在log 0.5/log(α + β)天后减半：美国市场的0.989对应63天。
2. **GARCH即ARMA，及其峰度。** 令ν_t = r_t² − σ_t²，它是鞅差。把σ_t² = r_t² − ν_t代入GARCH递推，得r_t² = ω + (α + β)r²_{t−1} + ν_t − βν_{t−1}：
   自回归根为α + β的ARMA(1, 1)。正态冲击下E[r⁴] = 3E[σ⁴]。对递推式平方取期望得E[σ⁴](1 − (α + β)² − 2α²) = ω² + 2ωσ̄²(α + β)，
   峰度为3(1 − (α + β)²)/(1 − (α + β)² − 2α²)。只要α > 0它就大于3，且仅当(α + β)² + 2α² < 1时有限。
3. **已实现方差中的噪声与最优采样频率。** 若观测对数价格为p_i = p*_i + u_i，噪声独立同分布、方差η²，则观测收益为r_i = r*_i + u_i − u_{i−1}，
   E[Σr_i²] = ∫σ²dt + 2nη²：偏差随n增长（签名图）。无噪声时RV的估计误差方差为2IQ/n（BNS）。均方误差约为(2nη²)² + 2IQ/n = 4n²η⁴ + 2IQ/n；
   令导数8nη⁴ − 2IQ/n²为零得n* = (IQ/(4η⁴))^{1/3}（Bandi与Russell 2008）。双尺度RV则消除偏差：对K个稀疏网格取平均（各自偏差2n̄η²），
   再减去(n̄/n)RV_all，以n^{−1/6}的速度收敛。
4. **QLIKE。** E[h/ĥ − log(h/ĥ) − 1 | F] = E[h|F]/ĥ + log ĥ − E[log h | F] − 1。对ĥ的导数为−E[h|F]/ĥ² + 1/ĥ，只在ĥ = E[h|F]处为零，
   且函数在那里是凸的。损失只通过E[h|F]依赖于h，另加一项与ĥ无关的量，所以无偏代理（E[h̃|F] = E[h|F]）只给每个预测的期望损失加上同一个常数，
   排名不变（Patton 2011）。对波动率上的MSE，argmin E(√h̃ − σ̂)² = E√h̃ < √E h̃（詹森）：以平方收益为代理时，最小点是(2/π)h ≈ 0.64h。
5. **卡尔曼增益。** 对x_t = x_{t−1} + w_t、y_t = x_t + v_t，方差分别为Q与R，滤波器先预测P⁻ = P + Q，用增益K = P⁻/(P⁻ + R)，
   再更新P = (1 − K)P⁻。稳态时KP⁻ = Q，且P⁻满足P⁻² − QP⁻ − QR = 0。除以R²并记q = Q/R，得p = P⁻/R = (q + √(q² + 4q))/2，
   K = p/(p + 1)，只是q的函数。比特币的q = 0.38给出K ≈ 0.45。
6. **迪基–富勒极限。** 对x_t = x_{t−1} + ε_t、x_0 = 0，平方得x_t² = x²_{t−1} + 2x_{t−1}ε_t + ε_t²，所以Σx_{t−1}ε_t = ½(x_T² − Σε_t²)。
   由唐斯克定理T^{−1/2}x_{⌊rT⌋} ⇒ σW(r)，于是T^{−1}Σx_{t−1}ε_t ⇒ ½σ²(W(1)² − 1)，T^{−2}Σx²_{t−1} ⇒ σ²∫₀¹W(r)²dr；由连续映射，
   T(ρ̂ − 1) ⇒ ½(W(1)² − 1)/∫W²。由于W(1) ~ N(0, 1)，P(W(1)² < 1) = P(|Z| < 1) ≈ 0.683，所以分子三次中有两次为负，分布左偏
   （第2章的模拟：带常数项时5%分位点为−2.89）。
